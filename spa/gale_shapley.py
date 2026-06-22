"""
spa.gale_shapley
=================
Implementação da variação do algoritmo de Gale-Shapley para o problema de
Student-Project Allocation (SPA), baseada em Abraham, Irving & Manlove
(2007). Produz um emparelhamento estável entre alunos e projetos.
"""

from models import MatchingState, Aluno, Projeto

def initialize_matching(graph) -> MatchingState:
    """
    Cria o estado inicial do emparelhamento: todos os alunos livres, todos
    os projetos sem alunos alocados, nenhuma proposta feita ainda.
    """
    pass


def propose(student, state: MatchingState, graph) -> None:
    """
    Faz o aluno propor ao seu projeto de maior preferência ainda não
    recusado. Atualiza o estado de propostas do aluno (avança para a
    próxima preferência na próxima tentativa, caso seja rejeitado).
    """
    pass


def evaluate_proposal(project, student, state: MatchingState, graph) -> bool:
    """
    Decide se o projeto aceita ou rejeita a proposta de um aluno, baseado na
    Nota Agregada e nas vagas disponíveis (vagas_max). Caso o projeto esteja
    cheio mas o novo aluno tenha nota melhor que algum já alocado, deve
    substituir o aluno de menor nota (retorna o aluno expulso, se houver).
    """
    pass


def run_gale_shapley(projetos: list[Projeto], alunos: list[Aluno]) -> MatchingState:
    """
    Executa o loop principal do algoritmo até que não existam mais alunos
    livres com propostas pendentes a fazer. Retorna o MatchingState final,
    que deve ser estável (sem pares bloqueantes).
    """
    pass
