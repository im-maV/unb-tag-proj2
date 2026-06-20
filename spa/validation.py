"""
spa.validation
==============
Funções de validação e checagem de corretude do emparelhamento final,
usadas tanto pelos testes automatizados quanto como sanity-check explícito
no notebook de entrega.
"""


def find_blocking_pairs(state, graph) -> list:
    """
    Procura por pares bloqueantes no emparelhamento final: um aluno e um
    projeto que, mesmo não emparelhados entre si, prefeririam mutuamente
    trocar de situação. Retorna a lista de pares encontrados (vazia se o
    emparelhamento é estável).
    """
    pass


def check_capacity_constraints(state, projetos: list) -> list:
    """
    Verifica se todos os projetos respeitam vagas_min e vagas_max no
    emparelhamento final. Retorna a lista de projetos que violam a
    restrição (vazia se tudo correto).
    """
    pass


def check_preference_consistency(state, graph) -> list:
    """
    Verifica se nenhum aluno foi alocado a um projeto fora de sua lista de
    preferências original. Retorna a lista de inconsistências encontradas.
    """
    pass


def is_stable_matching(state, graph, projetos: list) -> bool:
    """
    Roda todas as checagens acima e retorna True se o emparelhamento final
    é válido e estável, False caso contrário. Usado como critério de
    aceite final do projeto.
    """
    pass
