"""
spa.gale_shapley
=================
Implementação da variação do algoritmo de Gale-Shapley para o problema de
Student-Project Allocation (SPA), baseada em Abraham, Irving & Manlove
(2007). Produz um emparelhamento estável entre alunos e projetos.
"""

from models import MatchingState, Aluno, Projeto
from collections import deque
import bisect


def propose(
    aluno: Aluno,
    projetos: list[Projeto],
    free_alunos: deque,
    matching: dict,
    rejects_edges: list,
) -> None:
    """
    Faz o aluno propor ao próximo projeto em sua lista de preferência.
    Atualiza matching, fila de livres e lista de rejeições conforme resultado
    """
    if aluno.prox_preferencia >= len(aluno.preferencia):
        return
    projeto_cod = aluno.preferencia[aluno.prox_preferencia]
    aluno.prox_preferencia += 1

    # propose
    accept, reject_aluno = evaluate_proposal(projeto_cod, aluno, projetos)

    if accept:
        matching[aluno.cod] = projeto_cod

        if reject_aluno:
            # Remove emparelhamento do aluno expulso e recoloca na fila
            matching.pop(reject_aluno.cod, None)
            # reject_aluno.prox_preferencia
            free_alunos.append(reject_aluno)
            rejects_edges.append({"aluno": reject_aluno.cod, "projeto": projeto_cod})

    # se ainda há preferencias
    else:
        if aluno.prox_preferencia < len(aluno.preferencia):
            free_alunos.append(aluno)
        rejects_edges.append({"aluno": aluno.cod, "projeto": projeto_cod})


def buscar_projeto(projetos: list[Projeto], cod):
    """Retorna projeto válido a partir de um codigo ou None"""
    return next((p for p in projetos if p.cod == cod), None)


def pior_aluno_do_projeto(projeto: Projeto) -> Aluno | None:
    """Retorna o aluno de menor nota aceito no projeto"""
    if not projeto.aluno_aceitos:
        return None
    return min(projeto.aluno_aceitos, key=lambda a: a.nota)


def inserir_aluno_projeto(projeto: Projeto, aluno: Aluno):
    """Insere aluno mantendo ordem decrescente de nota (melhor primeiro)"""
    notas = [-a.nota for a in projeto.aluno_aceitos]
    pos = bisect.bisect_right(notas, -aluno.nota)
    projeto.aluno_aceitos.insert(pos, aluno)


def evaluate_proposal(p_cod: str, aluno: Aluno, projetos: list[Projeto]):
    """
    Decide se o projeto aceita ou rejeita a proposta de um aluno, baseado na
    nota e nas vagas disponíveis do projeto. Caso o projeto esteja
    cheio mas o novo aluno tenha nota melhor que algum já alocado, deve
    substituir o aluno de menor nota

    return:
        Aceito: boolean
        Aluno expulso: Aluno | None
    """
    projeto = buscar_projeto(projetos, p_cod)
    if not projeto:
        return False, None

    # elegibilidade minima
    if aluno.nota < projeto.nota_min:
        return False, None

    # vaga disponivel: aceita diretamente
    if len(projeto.aluno_aceitos) < projeto.num_vagas:
        inserir_aluno_projeto(projeto, aluno)
        return True, None

    # sem vaga: compara com pior aluno aceito
    pior_aluno = pior_aluno_do_projeto(projeto)
    if pior_aluno and aluno.nota > pior_aluno.nota:
        projeto.aluno_aceitos.remove(pior_aluno)
        inserir_aluno_projeto(projeto, aluno)
        return True, pior_aluno

    return False, None


def verificar_minimo_por_projeto(projetos: list[Projeto], matching: dict) -> list[str]:
    """
    Cada projeto deve ter ao menos 1 aluno.
    Retorna lista de projetos que ficaram sem alunos.
    """
    alocados_por_projeto = {}
    for aluno_cod, proj_cod in matching.items():
        alocados_por_projeto.setdefault(proj_cod, []).append(aluno_cod)

    sem_alunos = [p.cod for p in projetos if p.cod not in alocados_por_projeto]
    return sem_alunos


def run_gale_shapley(projetos: list[Projeto], alunos: list[Aluno]):
    """
    SPA-Students com variação
    Executa o loop principal do algoritmo até que não existam mais alunos
    livres com propostas pendentes a fazer.
    - Propostas partem dos alunos
    - Rejeições consideram a nota do aluno vs pior nota do aluno aceito no projeto
    - OBS: Verifica se existe no mínimo 1 aluno por projeto

    return:
        emparelhamento estável
        lisa de alunos emparelhados
        lista de rejeições (aluno -> projeto)
    """
    alunos = sorted(alunos, key=lambda a: int(a.cod[1:]))
    free_alunos = deque(alunos)
    matching = dict()
    alunos_emparelhados = []
    rejects_edges = []

    while free_alunos:
        aluno = free_alunos.popleft()
        propose(aluno, projetos, free_alunos, matching, rejects_edges)

    # alunos emparelhados
    alunos_emparelhados = [a for a in alunos if a.cod in matching]
    sem_alunos = verificar_minimo_por_projeto(projetos, matching)
    if sem_alunos:
        print(
            f"[AVISO] Projetos sem nenhum aluno alocado (violação do enunciado): {sem_alunos}"
        )

    return MatchingState(
        matching=matching,
        proposed_edges=[],
        matched_edges=[(a, p) for a, p in matching.items()],
        rejected_edges=rejects_edges,
        iteration=0,
    )
