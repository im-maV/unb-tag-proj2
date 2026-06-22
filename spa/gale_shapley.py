"""
spa.gale_shapley
=================
Implementação da variação do algoritmo de Gale-Shapley para o problema de
Student-Project Allocation (SPA), baseada em Abraham, Irving & Manlove
(2007). Produz um emparelhamento estável entre alunos e projetos.
"""

from models import MatchingState, Aluno, Projeto
import bisect



def propose(student, state: MatchingState, graph) -> None:
    """
    Faz o aluno propor ao seu projeto de maior preferência ainda não
    recusado. Atualiza o estado de propostas do aluno (avança para a
    próxima preferência na próxima tentativa, caso seja rejeitado).
    """
    pass


def evaluate_proposal(p_cod: str, aluno: Aluno, projetos: list[Projeto]):
    """
    Decide se o projeto aceita ou rejeita a proposta de um aluno, baseado na
    Nota Agregada e nas vagas disponíveis (vagas_max). Caso o projeto esteja
    cheio mas o novo aluno tenha nota melhor que algum já alocado, deve
    substituir o aluno de menor nota (retorna o aluno expulso, se houver).
    """
    projeto = buscar_projeto(projetos, p_cod)
    if (not projeto): return False, None

    if (projeto.num_vagas > 0):
        projeto.ranking_alunos.append(aluno)
        projeto.num_vagas -= 1
        return True, None

    last_aluno = projeto.ranking_alunos[-1]
    if aluno.nota > last_aluno.nota:
        reject_aluno = projeto.ranking_alunos.pop()
        inserir_aluno_ranking(projeto, aluno)
        return True, reject_aluno
    return False, None




def buscar_projeto(projetos: list[Projeto], cod):
    return next((p for p in projetos if p.cod == cod), None)


def inserir_aluno_ranking(projeto: Projeto, aluno: Aluno):
    notas = [-a.nota for a in projeto.ranking_alunos]
    pos = bisect.bisect_right(notas, -aluno.nota)
    projeto.ranking_alunos.insert(pos, aluno)


def run_gale_shapley(projetos: list[Projeto], alunos: list[Aluno]):
    """
    Executa o loop principal do algoritmo até que não existam mais alunos
    livres com propostas pendentes a fazer. Retorna o MatchingState final,
    que deve ser estável (sem pares bloqueantes).
    """
    alunos = sorted(alunos, key=lambda a: int(a.cod[1:]))
    print(alunos)

    
    matching = dict()
    alunos_emparelhados = []
    while (len(alunos) > 0):
        aluno = alunos.pop()
        # propose
        while len(aluno.projetos) > 0:
            p_cod = aluno.projetos.pop(0)
            accept, reject_aluno = evaluate_proposal(p_cod, aluno, projetos)
            if (reject_aluno): alunos.append(reject_aluno)
            if (accept):
                alunos_emparelhados.append(aluno)
                matching[aluno.cod] = p_cod
                break
    return matching, alunos_emparelhados
            


