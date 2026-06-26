"""
spa.graph_builder
==================
Constrói o grafo bipartido NetworkX a partir das estruturas geradas pelo
parser.
"""

import networkx as nx
from models.aluno_model import Aluno
from models.projeto_model import Projeto


def build_bipartite_graph(projetos: list[Projeto], alunos: list[Aluno]) -> nx.Graph:
    """
    Constrói o grafo bipartido G = (Alunos ∪ Projetos, E) usando NetworkX.
 
    Cada aluno recebe um nó com atributo 'bipartite' = 0 e 'nota'.
    Cada projeto recebe um nó com atributo 'bipartite' = 1, 'nota_min',
    'vagas_max' e 'candidatos'. Arestas existem apenas para projetos
    presentes na lista de preferência do aluno e carregam o atributo
    'preferencia'.
 
    Nós são os objetos Aluno/Projeto diretamente (hasheáveis via id()).
    """
    graph = nx.Graph()
 
    # Índice auxiliar para resolver projeto_cod -> Projeto durante a
    # construção das arestas, sem percorrer a lista a cada aresta
    projetos_por_cod: dict[str, Projeto] = {p.cod: p for p in projetos}
 
    # Nós de projeto
    for projeto in projetos:
        graph.add_node(
            projeto,
            bipartite=1,
            nota_min=projeto.nota_min,
            vagas_max=projeto.num_vagas,
            candidatos=[],
        )
 
    # Nós de alunos + arestas de preferência
    for aluno in alunos:
        graph.add_node(aluno, bipartite=0, nota=aluno.nota)
        for rank, projeto_cod in enumerate(aluno.preferencia, start=1):
            projeto = projetos_por_cod.get(projeto_cod)
            if projeto is None:
                continue
            graph.add_edge(aluno, projeto, preferencia=rank)
            graph.nodes[projeto]["candidatos"].append(aluno)
 
    if not nx.is_bipartite(graph):
        raise ValueError("O grafo construído não é bipartido.")
 
    return graph
 
 
def get_bipartite_sets(
    graph: nx.Graph,
) -> tuple[set[Aluno], set[Projeto]]:
    """
    Retorna os dois conjuntos de vértices do grafo bipartido (alunos,
    projetos), separados a partir do atributo 'bipartite' de cada nó.
    """
    students: set[Aluno] = {
        n for n, data in graph.nodes(data=True) if data.get("bipartite") == 0
    }
    projects: set[Projeto] = {
        n for n, data in graph.nodes(data=True) if data.get("bipartite") == 1
    }
    return students, projects