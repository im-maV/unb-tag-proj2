"""
spa.metrics
===========
Calcula métricas derivadas do emparelhamento final: índice de preferência
por projeto, e a matriz/tabela final de classificações cruzadas
"""

from pathlib import Path
from typing import Any

import networkx as nx
import pandas as pd

from spa.visualization import get_node_id, sort_node_key
from models import Aluno, MatchingState, Projeto

Node = Aluno | Projeto
OUTPUT_DIR = Path("output")


def _get_bipartite_nodes(graph: nx.Graph, side: int) -> set:
    """Retorna nós da partição 0 (Alunos) ou 1 (Projetos)."""
    return {n for n, d in graph.nodes(data=True) if d.get("bipartite") == side}


def _get_edge_data_safe(graph: nx.Graph, u: Any, v: Any) -> dict | None:
    return graph.get_edge_data(u, v) or graph.get_edge_data(v, u)


def _format_student_rank(rank: int | None, total: int, proj_cod: str) -> str:
    if rank is None:
        return "-"
    return f"{rank}º (Top {rank} de {total} alunos na lista {proj_cod})"


def _format_project_choice(rank: int | None, aluno_cod: str) -> str:
    """Formato exato da tabela do PDF: '1º (Primeira escolha do Aluno 105)'."""
    if rank is None:
        return "-"
    ordinais = {1: "Primeira", 2: "Segunda", 3: "Terceira"}
    texto = ordinais.get(rank, f"{rank}ª")
    return f"{rank}º ({texto} escolha do Aluno {aluno_cod})"


def compute_preference_index(
    project: Projeto, state: MatchingState, graph: nx.Graph
) -> float | None:
    """
    Calcula o índice de preferência agregado de um projeto, resumindo quão
    bem ele foi atendido em termos da posição de preferência média dos
    alunos que nele foram alocados.
    """
    ranks = [
        rank
        for aluno, proj in state.matching
        if proj == project
        if (rank := project_rank_in_student_list(aluno, project, graph)) is not None
    ]
    return sum(ranks) / len(ranks) if ranks else None


def compute_all_preference_indices(
    state: MatchingState, graph: nx.Graph
) -> dict[Any, float]:
    """Índice de preferência para todos os projetos. Retorna {projeto: indice}."""
    projects = _get_bipartite_nodes(graph, side=1)
    return {
        proj: idx
        for proj in projects
        if (idx := compute_preference_index(proj, state, graph)) is not None
    }


def student_rank_in_project_list(
    student: Aluno, project: Projeto, graph: nx.Graph
) -> int | None:
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


def project_rank_in_student_list(
    student: Aluno, project: Projeto, graph: nx.Graph
) -> int | None:
    """Posição do projeto na lista de preferências do aluno (1ª, 2ª, 3ª)."""
    edge = _get_edge_data_safe(graph, student, project)
    return edge.get("preferencia") if edge else None


def build_final_matching_matrix(state: MatchingState, graph: nx.Graph):
    """
    Monta a tabela final com colunas:
        - Aluno
        - Projeto Emparelhado
        - Classificação do Aluno (Lista de Preferência do Projeto)
        - Classificação do Projeto (Lista de Preferência do Aluno)
    Inclui alunos não emparelhados com '-'.
    """
    alunos = sorted(_get_bipartite_nodes(graph, side=0), key=sort_node_key)
    matching_index = dict(state.matching)  # O(1) Lookup instantâneo

    rows: list[dict] = []

    col_aluno = "Aluno"
    col_projeto = "Projeto Emparelhado"
    col_aluno_rank = "Classificação do Aluno"
    col_proj_rank = "Classificação do Projeto"

    for aluno in alunos:
        aluno_cod = get_node_id(aluno)
        project = matching_index.get(aluno)

        if project:
            proj_cod = get_node_id(project)
            rank_aluno = student_rank_in_project_list(aluno, project, graph)
            rank_projeto = project_rank_in_student_list(aluno, project, graph)
            total_candidatos = len(graph.nodes[project].get("candidatos", []))

            rows.append(
                {
                    col_aluno: aluno_cod,
                    col_projeto: proj_cod,
                    col_aluno_rank: _format_student_rank(
                        rank_aluno, total_candidatos, proj_cod
                    ),
                    col_proj_rank: _format_project_choice(rank_projeto, aluno_cod),
                }
            )
        else:
            rows.append(
                {
                    col_aluno: aluno_cod,
                    col_projeto: "-",
                    col_aluno_rank: "-",
                    col_proj_rank: "-",
                }
            )

    return pd.DataFrame(rows)


def save_matching_matrix_csv(df: pd.DataFrame) -> None:
    """Salva a matriz de emparelhamento final em CSV para visualização/exame externo."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_DIR / "matching_matrix.csv", index=False)
