"""
spa.visualization
==================
Funções de plotagem do grafo bipartido colorido por iteração, e de
visualizações auxiliares (índice de preferência, matriz final).

"""


def get_edge_colors(graph, state, iteration_log) -> dict:
    """
    Define a cor de cada aresta do grafo para uma dada iteração, conforme a
    legenda exigida: proposta ativa, emparelhamento temporário, ou
    rejeição. Retorna um dicionário {(u, v): cor}.
    """
    pass


def plot_bipartite_iteration(graph, state, iteration_log, iteration_number: int) -> None:
    """
    Plota o grafo bipartido de uma iteração específica, com alunos de um
    lado e projetos do outro, arestas coloridas conforme
    get_edge_colors(), título indicando o número da iteração, e legenda de
    cores.
    """
    pass


def plot_all_iterations(graph, iteration_states: list) -> None:
    """
    Gera a sequência completa de plots para as 10 iterações, chamando
    plot_bipartite_iteration() para cada uma em ordem.
    """
    pass


def plot_preference_index_summary(preference_indices: dict) -> None:
    """
    Gera um gráfico resumo (barras ou similar) do índice de preferência por
    projeto, calculado em spa.metrics.
    """
    pass
