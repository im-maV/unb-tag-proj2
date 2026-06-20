"""
spa.augmenting_path
====================
Implementa a busca por caminhos M-alternados/aumentantes, usada nas 10
iterações exigidas pelo enunciado para tentar aumentar o emparelhamento a
partir dos alunos que ficaram sem projeto na rodada anterior.
"""


def find_augmenting_path(start_student, graph, state) -> list | None:
    """
    Busca (BFS ou DFS alternada) um caminho M-aumentante a partir de um
    aluno livre, alternando entre arestas fora do emparelhamento e arestas
    dentro do emparelhamento, até alcançar um projeto com vaga disponível.
    Retorna a sequência de vértices do caminho, ou None se não existir.
    """
    pass


def augment_matching(path: list, state) -> None:
    """
    Aplica a operação de augmentação sobre o emparelhamento atual: inverte
    o status (dentro/fora de M) de cada aresta do caminho encontrado,
    aumentando o emparelhamento em 1.
    """
    pass


def run_iterations(
    graph,
    initial_state,
    n_iterations: int = 10,
    on_iteration_end=None,
) -> list:
    """
    Executa o loop de N iterações (determinístico, sem aleatoriedade).

    A cada iteração: percorre os alunos não emparelhados em ordem fixa (ex:
    matrícula crescente), tenta encontrar caminho aumentante para cada um, e
    aplica a augmentação quando encontrado. Registra o log de arestas por
    categoria (proposta ativa / emparelhamento temporário / rejeição) usado
    pela visualização.

    IMPORTANTE — exigência do enunciado: cada iteração deve ser MOSTRADA na
    saída do programa antes de seguir para a próxima, não apenas ao final.
    Por isso este loop aceita um callback `on_iteration_end(state,
    iteration_log, iteration_number)`, chamado ao término de cada rodada.
    Na IDE, o callback pode ser None (loop roda silencioso, útil para
    testes/debug); no notebook, deve receber
    `spa.visualization.plot_bipartite_iteration` para exibir o grafo da
    iteração imediatamente após ela ser computada.

    Retorna a lista de estados intermediários (um por iteração), para reuso
    posterior (ex: matriz final, índice de preferência).
    """
    pass
