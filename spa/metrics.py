"""
spa.metrics
===========
Calcula métricas derivadas do emparelhamento final: índice de preferência
por projeto, e a matriz/tabela final de classificações cruzadas
"""

import pandas as pd


def _nodes_by_side(graph, side: int) -> set:
    return {n for n, d in graph.nodes(data=True) if d.get("bipartite") == side}


def _edge_attr(graph, u, v) -> dict | None:
    return graph.get_edge_data(u, v) or graph.get_edge_data(v, u)


def _student_sort_key(cod: str):
    try:
        return int(cod[1:])
    except (ValueError, TypeError):
        return cod


def _format_student_rank(rank: int | None, total: int) -> str:
    if rank is None:
        return "-"
    return f"{rank}º (Top {rank} de {total})"


def compute_preference_index(project, state, graph) -> float:
    """
    Calcula o índice de preferência agregado de um projeto, resumindo quão
    bem ele foi atendido em termos da posição de preferência média dos
    alunos que nele foram alocados.
    """
    ranks = [
        project_rank_in_student_list(aluno, project, graph)
        for aluno, proj in state.matching.items()
        if proj == project
    ]
    ranks = [r for r in ranks if r is not None]
    return sum(ranks) / len(ranks) if ranks else None


def compute_all_preference_indices(state, graph) -> dict:
    """Índice de preferência para todos os projetos. Retorna {codigo_projeto: indice}."""
    return {
        proj: idx
        for proj in _nodes_by_side(graph, side=1)
        if (idx := compute_preference_index(proj, state, graph)) is not None
    }


def student_rank_in_project_list(student, project, graph) -> int | None:
    """Posição do aluno entre os candidatos do projeto, ordenado por nota."""
    candidatos = graph.nodes[project].get("candidatos", [])
    if not candidatos:
        return None

    ranked = sorted(
        candidatos, key=lambda a: graph.nodes[a].get("nota", 0), reverse=True
    )
    try:
        return ranked.index(student) + 1
    except ValueError:
        return None


def project_rank_in_student_list(student, project, graph) -> int | None:
    """Posição do projeto na lista de preferências do aluno (1ª, 2ª, 3ª)."""
    edge = _edge_attr(graph, student, project)
    return edge.get("preferencia") if edge else None


def build_final_matching_matrix(state, graph):
    """
    Monta a tabela final com colunas:
        - Aluno
        - Projeto Emparelhado
        - Classificação do Aluno (Lista de Preferência do Projeto)
        - Classificação do Projeto (Lista de Preferência do Aluno)
    Inclui alunos não emparelhados com '-'.
    """
    alunos = sorted(_nodes_by_side(graph, side=0), key=_student_sort_key)
    rows = []

    for aluno in alunos:
        project = state.matching.get(aluno)
        if project:
            rank_aluno = student_rank_in_project_list(aluno, project, graph)
            rank_projeto = project_rank_in_student_list(aluno, project, graph)
            total = len(graph.nodes[project].get("candidatos", []))
            rows.append(
                {
                    "Aluno": aluno,
                    "Projeto Emparelhado": project,
                    "Classificação do Aluno": _format_student_rank(rank_aluno, total),
                    "Classificação do Projeto": (
                        f"{rank_projeto}º" if rank_projeto else "-"
                    ),
                }
            )
        else:
            rows.append(
                {
                    "Aluno": aluno,
                    "Projeto Emparelhado": "-",
                    "Classificação do Aluno": "-",
                    "Classificação do Projeto": "-",
                }
            )

    return pd.DataFrame(rows)


def save_matching_matrix_csv(df, filepath: str) -> None:
    """Salva a matriz de emparelhamento final em CSV para visualização/exame externo."""
    df.to_csv(filepath, index=False)
