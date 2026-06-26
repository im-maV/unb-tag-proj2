"""
spa.gale_shapley
=================
Implementação da variação do algoritmo de Gale-Shapley para o problema de
Student-Project Allocation (SPA), baseada em Abraham, Irving & Manlove
(2007). Produz um emparelhamento estável entre alunos e projetos.
"""

from collections import deque
from typing import Dict, List, Tuple, Deque
from models.aluno_model import Aluno
from models.matching_model import MatchingState
from models.projeto_model import Projeto


def propose(
    aluno: Aluno,
    projetos: list[Projeto],
    free_alunos: Deque[Aluno],
    matching: List[Tuple[Aluno, Projeto]],
    rejects_edges: list[Dict],
) -> None:
    """
    Faz o aluno propor ao próximo projeto em sua lista de preferência.
    Atualiza matching, fila de livres e lista de rejeições conforme resultado.
    """
    if not aluno.tem_mais_preferencias():
        return

    projeto_cod = aluno.proxima_preferencia()
    aluno.prox_preferencia += 1

    accept, reject_aluno, projeto = evaluate_proposal(projeto_cod, aluno, projetos)

    if accept:
        matching.append((aluno, projeto))
        if reject_aluno:
            # Remove emparelhamento do aluno expulso e recoloca na fila)
            matching = [
                (a, b) for a, b in matching
                if a.cod != reject_aluno.cod
            ]
            # reject_aluno.prox_preferencia
            free_alunos.append(reject_aluno)
            rejects_edges.append({"aluno": reject_aluno.cod, "projeto": projeto_cod})
    else:
        if aluno.tem_mais_preferencias():
            free_alunos.append(aluno)
        rejects_edges.append({"aluno": aluno.cod, "projeto": projeto_cod})


def buscar_projeto(projetos: list[Projeto], cod: str) -> Projeto | None:
    """Retorna projeto válido a partir de um código ou None."""
    return next((p for p in projetos if p.cod == cod), None)


def evaluate_proposal(p_cod: str, aluno: Aluno, projetos: list[Projeto]):
    """
    Decide se o projeto aceita ou rejeita a proposta de um aluno, baseado na
    nota e nas vagas disponíveis do projeto. Caso o projeto esteja
    cheio mas o novo aluno tenha nota melhor que algum já alocado, deve
    substituir o aluno de menor nota

    return:
        Aceito: boolean
        Aluno expulso: Aluno | None
        project: Projeto associado ao Aluno
    """
    projeto = buscar_projeto(projetos, p_cod)
    if not projeto:
        return False, None, None
    # elegibilidade minima
    if not projeto.aceita_nota(aluno.nota):
        return False, None, None

    # vaga disponivel: aceita diretamente
    if projeto.tem_vaga():
        projeto.inserir_aluno(aluno)
        return True, None, projeto

    # sem vaga: compara com pior aluno aceito
    pior = projeto.pior_aluno()
    if pior and aluno.nota > pior.nota:
        projeto.aluno_aceitos.remove(pior)
        projeto.inserir_aluno(aluno)
        return True, pior, projeto

    return False, None, None


def verificar_minimo_por_projeto(projetos: list[Projeto], matching: List[Tuple[Aluno, Projeto]]) -> list[str]:
    """
    Cada projeto deve ter ao menos 1 aluno.
    Retorna lista de projetos que ficaram sem alunos.
    """
    projetos_com_aluno = {p.cod for a,p in matching}
    return [p.cod for p in projetos if p.cod not in projetos_com_aluno]


def run_gale_shapley(projetos: list[Projeto], alunos: list[Aluno]):
    """
    SPA-Students com variação.
    Executa o loop principal do algoritmo até que não existam mais alunos
    livres com propostas pendentes a fazer.
    - Propostas partem dos alunos
    - Rejeições consideram a nota do aluno vs pior nota do aluno aceito no projeto
    - OBS: Verifica se existe no mínimo 1 aluno por projeto

    return:
        matching:           lista de pares (Aluno, Projeto) - onde Aluno e Projeto são objetos
        alunos_emparelhados: lista de alunos alocados
        rejects_edges:      lista de rejeições
        allocated_projects: dict projeto -> lista de alunos aceitos
        free_students:      lista de objetos Aluno sem alocação
    """
    alunos = sorted(alunos, key=lambda a: int(a.cod[1:]))
    free_alunos = deque(alunos)
    matching: List[Tuple[Aluno, Projeto]] = []
    rejects_edges = []

    while free_alunos:
        aluno = free_alunos.popleft()
        propose(aluno, projetos, free_alunos, matching, rejects_edges)

    alunos_emparelhados = {a for a,p in matching}
    sem_alunos = verificar_minimo_por_projeto(projetos, matching)
    if sem_alunos:
        print(f"[AVISO] Projetos sem nenhum aluno alocado: {sem_alunos}")

    allocated_projects = {proj.cod: proj.aluno_aceitos for proj in projetos}
    free_students: list[Aluno] = [a for a in alunos if a.cod not in matching]

    return (
        matching,
        alunos_emparelhados,
        rejects_edges,
        allocated_projects,
        free_students,
    )


def build_matching_state(
    matching: List[Tuple[str, str]],
    proposed_edges: List[dict] | None = None,
    rejected_edges: List[dict] | None = None,
    allocated_projects: Dict[str, List[Aluno]] | None = None,
    free_students: List[Aluno] | None = None,
    iteration: int = 0,
) -> MatchingState:
    """
    Constrói um `MatchingState` a partir dos componentes do emparelhamento.
    """
    proposed_edges = proposed_edges or []
    rejected_edges = rejected_edges or []
    allocated_projects = allocated_projects or {}
    free_students = free_students or set()

    return  MatchingState(
        matching=matching,
        proposed_edges=proposed_edges or [],
        rejected_edges=rejected_edges or [],
        allocated_projects=allocated_projects or {},
        free_students={a.cod for a in free_students} if free_students else set(),
        iteration=iteration,
    )
