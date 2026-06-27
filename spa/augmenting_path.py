"""
spa.augmenting_path
====================
Implementa a busca por caminhos M-alternados/aumentantes, usada nas 10
iterações exigidas pelo enunciado para tentar aumentar o emparelhamento a
partir dos alunos que ficaram sem projeto na rodada anterior.
"""

import copy
import networkx as nx
from collections import deque
from models.aluno_model import Aluno
from models.projeto_model import Projeto
from models.matching_model import MatchingState
from typing import Callable, List, Deque, Tuple 

Node = Aluno | Projeto

def find_augmenting_path(start_student: Aluno, graph: nx.Graph, state: MatchingState):
    """
    Busca (BFS ou DFS alternada) um caminho M-aumentante a partir de um
    aluno livre, alternando entre arestas fora do emparelhamento e arestas
    dentro do emparelhamento, até alcançar um projeto com vaga disponível.
    Retorna a sequência de vértices do caminho, ou None se não existir.
    """
    # Fila que contém o nó atual e uma lista com o caminho percorrido
    queue: Deque[Tuple[Node, List[Node]]] = deque([((start_student, [start_student]))])
    visited: set[Node] = {start_student}

    while queue:
        current_node, path = queue.popleft()
        is_student = isinstance(current_node, Aluno)

        if is_student:
            aluno: Aluno = current_node
            for project in graph.neighbors(aluno):
                if not state.is_matched(aluno, project):
                    if project not in visited:
                        visited.add(project)
                        queue.append((project, path + [project]))
        else:
            project: Projeto = current_node
            if state.has_capacity(project):
                return path

            allocated_students = state.get_allocated_students(project)

            for alloc_student in allocated_students:
                if alloc_student not in visited:
                    visited.add(alloc_student)
                    queue.append((alloc_student, path + [alloc_student]))
    return None


def augment_matching(path: List[Node], state: MatchingState) -> None:
    """
    Aplica a operação de augmentação sobre o emparelhamento atual: inverte
    o status (dentro/fora de M) de cada aresta do caminho encontrado,
    aumentando o emparelhamento em 1.
    """
    for i in range(len(path) - 1):
        node_a = path[i]
        node_b = path[i + 1]

        # Checa tipo
        if isinstance(node_a, Aluno):
            student, project = node_a, node_b
        else:
            project, student = node_a, node_b

        # Checa se a aresta já existe, se sim inverte para cobrir todo o
        # caminho encontrado
        if state.is_matched(student, project):
            state.remove_pair(student, project)
        # se não, adicionamos a aresta ao state (primeira e última do caminho)
        else:
            state.add_pair(student, project)

def run_iterations(
    graph: nx.Graph,
    initial_state: MatchingState,
    free_students: List[Aluno],
    n_iterations: int = 10,
    on_iteration_end: Callable[[MatchingState, dict, int], None] | None = None,
):
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
    state_history: list[MatchingState] = []
    current_state = initial_state

    for iteration in range(1, n_iterations + 1):
        current_state.iteration = iteration

        # isso é desnecessário se a função já receber o dicionário free students,
        # que pode ser implemntada no galey shapley com um 
        # free_students.append(aluno_ainda_nao_emparelhado) 
        free_students = [
             node for node in graph.nodes
             if isinstance(node, Aluno) and node not in current_state.matching
        ]


        free_students.sort(key=lambda x: x.cod)

        for student in free_students:
            path = find_augmenting_path(student, graph, current_state)

            if path:
                augment_matching(path, current_state)

        # Log visual
        interation_log = {
            "proposed_edges": current_state.proposed_edges,
            "matched_edges": [(s, p) for s, p in current_state.matching],
            "rejected_edges": current_state.rejected_edges,
        }

        # callback
        if on_iteration_end is not None:
            on_iteration_end(current_state, interation_log, iteration)
        
        snapshot = {
            'iteration': iteration,
            'matching': current_state.matching.copy(),
            'allocated_projects': {p: list(alunos) for p, alunos in current_state.allocated_projects.items()}
        }

        # adiciona o estado dessa iteração no histórico
        state_history.append(snapshot)
    
    return state_history
