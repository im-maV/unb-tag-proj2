import networkx as nx


class Matchings:
    """
    Represena o emparelhamento final depois de i (10) iteracões
        1. bipartite_graph: atributo estático representando o grafo bipartido inicial
        2. states: lista do estado de todos os i (10) emparelhmento realizados pelo algoritimo de caminhos aumentantes
    """

    def __init__(self, bipartite_graph: nx.Graph):
        self.bipartite_graph = bipartite_graph
        self.states: list[MatchingState] = []


class MatchingState:
    """
    Representa o estado do emparelhamento em um dado momento da execução.

    Deve armazenar:
        1. Matching (dicionário aluno -> projeto)
        2. dicionário projeto -> lista de alunos emparelhados (Necessário?)
        3. conjunto de alunos ainda não emparelhados
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
        allocated_projects = {}
        free_students = {}      # tem que adequar isso no galey shapley

    # Define representação legível do objeto para debug (print/debugger)
    def __repr__(self):
        return (
            f"MatchingState(iteration={self.iteration},\n"
            f"  matching={self.matching},\n"
            f"  matched_edges={self.matched_edges},\n"
            f"  rejected_edges={self.rejected_edges})"
        )

    def is_matched(self, aluno, projeto) -> bool:
        """
        Verifica se um dado aluno está atualmente alocado a um dado projeto neste estado.
        """
        return self.matching.get(aluno) == projeto
    
    
    def has_capacity(self, projeto) -> bool:
        """
        Verifica se um dado projeto ainda tem vagas disponíveis.
        """
        current_students = self.allocated_projects.get(projeto, [])
        return len(current_students) < projeto.num_vagas
