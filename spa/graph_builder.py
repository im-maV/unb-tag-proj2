"""
spa.graph_builder
==================
Constrói o grafo bipartido NetworkX a partir das estruturas geradas pelo
parser.
"""

import networkx as nx


def build_bipartite_graph(projetos: list, alunos: list):
    """
    Constrói o grafo bipartido G = (Alunos ∪ Projetos, E) usando NetworkX.

    Cada aluno recebe um nó com atributo 'bipartite' = 0 e 'nota'.
    Cada projeto recebe um nó com atributo 'bipartite' = 1, 'nota_min',
    'vagas_max' e 'candidatos'. Arestas existem apenas para projetos
    presentes na lista de preferência do aluno e carregam o atributo
    'preferencia'.
    """
    G = nx.Graph()

    # Nó de projeto
    for projeto in projetos:
        G.add_node(
            projeto.cod,
            bipartite=1,
            nota_min=projeto.nota_min,
            vagas_max=projeto.num_vagas,
            candidatos=[],
        )

    # Nós de alunos + arestas de preferência
    for aluno in alunos:
        G.add_node(aluno.cod, bipartite=0, nota=aluno.nota)
        for rank, projeto_cod in enumerate(aluno.preferencia, start=1):
            if not G.has_node(projeto_cod):
                continue
            G.add_edge(aluno.cod, projeto_cod, preferencia=rank)
            G.nodes[projeto_cod]["candidatos"].append(aluno.cod)

    if not nx.is_bipartite(G):
        raise ValueError("O grafo construído não é bipartido.")

    return G


def get_bipartite_sets(graph):
    """
    Retorna os dois conjuntos de vértices do grafo bipartido (alunos,
    projetos), separados a partir do atributo 'bipartite' de cada nó.
    """
    students = {n for n, data in graph.nodes(data=True) if data.get("bipartite") == 0}
    projects = {n for n, data in graph.nodes(data=True) if data.get("bipartite") == 1}
    return students, projects
