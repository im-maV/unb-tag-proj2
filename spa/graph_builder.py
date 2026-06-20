"""
spa.graph_builder
==================
Constrói o grafo bipartido NetworkX a partir das estruturas geradas pelo
parser. 
"""


def build_bipartite_graph(projetos: list, alunos: list):
    """
    Constrói o grafo bipartido G = (Alunos ∪ Projetos, E) usando NetworkX.

    Deve adicionar um nó por aluno e um nó por projeto, marcando o atributo
    'bipartite' de cada lado (0 para alunos, 1 para projetos). Cada aresta
    (aluno, projeto) deve existir apenas se o projeto está na lista de
    preferências do aluno.
    """
    pass


def annotate_edge_preferences(graph, alunos: list) -> None:
    """
    Anota cada aresta do grafo com a posição de preferência do aluno
    (1ª, 2ª ou 3ª escolha), como atributo da aresta.
    """
    pass


def annotate_node_attributes(graph, projetos: list, alunos: list) -> None:
    """
    Anota atributos nos nós: vagas_min e vagas_max nos nós de projeto, e
    nota agregada nos nós de aluno. Usado posteriormente pelo algoritmo de
    Gale-Shapley para critério de aceite/rejeição.
    """
    pass


def get_bipartite_sets(graph):
    """
    Retorna os dois conjuntos de vértices do grafo bipartido (alunos,
    projetos), separados a partir do atributo 'bipartite' de cada nó.
    """
    pass
