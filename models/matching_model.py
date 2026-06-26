"""Modelos de emparelhamento para grafo bipartido e estados do algoritmo."""

import networkx as nx
from typing import List, Tuple, Dict, Set
from models.aluno_model import Aluno
from models.projeto_model import Projeto

class Matchings:
    """
    Represena o emparelhamento final depois de i (10) iteracões
        1. bipartite_graph: atributo estático representando o grafo bipartido inicial
        2. states: lista do estado de todos os i (10) emparelhmento realizados
            pelo algoritimo de caminhos aumentantes
    """

    def __init__(self, bipartite_graph: nx.Graph):
        self.bipartite_graph = bipartite_graph
        self.states: list[MatchingState] = []


class MatchingState:
    """
    Representa o estado do emparelhamento em um dado momento da execução.

    Deve armazenar:
        1. Matching (dicionário aluno -> projeto)
        2. dicionário projeto -> lista de alunos emparelhados
        3. conjunto de alunos ainda não emparelhados
        4. histórico de propostas já feitas por cada aluno
            (para saber qual é a próxima preferência a tentar)
            a) proposed_edges e rejected_edges
    """

    # atributos indefinidos por enquanto
    def __init__(
        self, 
        matching:List[Tuple[Aluno, Projeto]], 
        proposed_edges: List[Dict], 
        rejected_edges: List[Dict], 
        allocated_projects: Dict[str, List[Aluno]],
        free_students: Set[str],
        iteration=0
    ):
        self.iteration = iteration
        self.matching = matching
        self.proposed_edges = proposed_edges
        self.rejected_edges = rejected_edges
        self.allocated_projects = allocated_projects
        self.free_students = free_students
        # indice auxiliar -> codAluno: Projeto
        self._index: dict[str, Projeto] = {
            aluno.cod: projeto for aluno, projeto in matching
        }


    def is_matched(self, aluno: Aluno, projeto: Projeto) -> bool:
        """Verifica se um aluno está atualmente emparelhado com um dado projeto."""
        return self._index.get(aluno.cod) is projeto
 
    def has_capacity(self, projeto: Projeto) -> bool:
        """Verifica se um projeto ainda tem vagas disponíveis."""
        current = self.allocated_projects.get(projeto.cod, [])
        return len(current) < projeto.num_vagas
    
    def get_allocated_students(self, projeto: Projeto) -> list[Aluno]:
        """Retorna a lista de alunos atualmente alocados a um projeto."""
        return self.allocated_projects.get(projeto.cod, [])

    def add_pair(self, aluno: Aluno, projeto: Projeto) -> None:
        """Adiciona o par (Aluno, Projeto) ao emparelhamento."""
        self.matching.append((aluno, projeto))
        self._index[aluno.cod] = projeto
        # Como não podemos deixar projetos sem alocação creio que
        # essa verificação é válida (adiciona aluno na lista de alunos do projeto)
        self.allocated_projects.setdefault(projeto.cod, []).append(aluno)
        self.free_students.discard(aluno.cod)
    
    def remove_pair(self, aluno: Aluno, projeto: Projeto) -> None:
        """Remove o par (Aluno, Projeto) do emparelhamento."""
        self.matching = [
            (a, p) for a, p in self.matching if a is not aluno or p is not projeto
        ]
        self._index.pop(aluno.cod, None)
        alocados = self.allocated_projects.get(projeto.cod, [])
        if aluno in alocados:
            alocados.remove(aluno)
        self.free_students.add(aluno.cod)


    def __deepcopy__(self, memo: dict) -> MatchingState:
        """
        Copia apenas as estruturas de controle do estado, mantendo as
        referências originais aos objetos Aluno e Projeto.

        Por que isso importa: Aluno e Projeto são usados como nós no grafo
        NetworkX, que os indexa por identidade (id()). Um deepcopy ingênuo
        criaria novas instâncias com o mesmo __repr__ mas id() diferente —
        tornando-os invisíveis ao grafo e causando KeyError em
        graph.neighbors().
        """
        new_state = MatchingState.__new__(MatchingState)
        memo[id(self)] = new_state

        # Primitivos — cópia direta
        new_state.iteration = self.iteration

        # Listas/sets de controle — cópia rasa das estruturas,
        # mas as referências internas (Aluno, Projeto) são preservadas
        new_state.matching = list(self.matching)
        new_state.proposed_edges = [e.copy() for e in self.proposed_edges]
        new_state.rejected_edges = [e.copy() for e in self.rejected_edges]
        new_state.free_students = set(self.free_students)
        new_state.allocated_projects = {
            cod: list(alunos)
            for cod, alunos in self.allocated_projects.items()
        }

        # Índice auxiliar — reconstruído a partir dos pares copiados
        new_state._index = {
            aluno.cod: projeto for aluno, projeto in new_state.matching
        }

        return new_state

    # Define representação legível do objeto para debug (print/debugger)
    def __repr__(self) -> str:
        pairs = [(a.cod, p.cod) for a, p in self.matching]
        return (
            f"MatchingState(iteration={self.iteration},\n"
            f"  matching={pairs},\n"
            f"  free_students={self.free_students})"
        )