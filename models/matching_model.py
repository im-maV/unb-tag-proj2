import networkx as nx


class Matchings:
    """
    Represena o emparelhamento final depois de i (10) iteracões
        1. bipartite_graph: atributo estático representando o grafo bipartido inicial
        2. states: lista do estado de todos os i (10) emparelhmento realizados pelo algoritimo de caminhos aumentantes
    """

    bipartite_graph: nx.Graph = None

    def __init__(self):
        self.states: list[MatchingState] = []


class MatchingState:
    """
    Representa o estado do emparelhamento em um dado momento da execução.

    Deve armazenar:
        1. Matching (dicionário aluno -> projeto)
        2. dicionário projeto -> lista de alunos emparelhados (Necessário?)
        3. conjunto de alunos ainda não emparelhados (Necessário?)
        4. histórico de propostas já feitas por cada aluno (para saber qual é a próxima preferência a tentar)
            a) proposed_edges e rejected_edges
    """

    # atributos indefinidos por enquanto
    def __init__(
        self, matching, proposed_edges, matched_edges, rejected_edges, iteration=0
    ):
        self.iteration = iteration
        self.matching = matching
        self.proposed_edges = proposed_edges
        self.matched_edges = matched_edges
        self.rejected_edges = rejected_edges
