"""
spa.augmenting_path
====================
Implementa a busca por caminhos M-alternados/aumentantes, usada nas 10
iterações exigidas pelo enunciado para tentar aumentar o emparelhamento a
partir dos alunos que ficaram sem projeto na rodada anterior.
"""

import copy
from collections import deque
from typing import Callable, Deque, Tuple
import networkx as nx
from models.aluno_model import Aluno
from models.matching_model import MatchingState
from models.projeto_model import Projeto

Node = Aluno | Projeto


def find_augmenting_path(start_student: Aluno, graph: nx.Graph, state: MatchingState):
    """
    Busca (BFS ou DFS alternada) um caminho M-aumentante a partir de um
    aluno livre, alternando entre arestas fora do emparelhamento e arestas
    dentro do emparelhamento, até alcançar um projeto com vaga disponível.
    Retorna a sequência de vértices do caminho, ou None se não existir.
    """
    # Fila que contém o nó atual e uma lista com o caminho percorrido
    queue: Deque[Tuple[Node, list[Node]]] = deque([(start_student, [start_student])])
    visited: set[Node] = {start_student}

    while queue:
        current_node, path = queue.popleft()
        is_student = isinstance(current_node, Aluno)

        if is_student:
            aluno: Aluno = current_node
            for project in graph.neighbors(aluno):
                if not state.is_matched(aluno, project):
                    # Se o projeto tem nota min e o aluno não cumpre - Proposta NEGADA
                    if project and (aluno.nota < project.nota_min):
                        state.rejected_edges.append(
                            {"aluno": aluno.cod, "projeto": project.cod}
                        )
                        continue

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


def augment_matching(path: list[Node], state: MatchingState) -> None:
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
            assert isinstance(node_b, Projeto)
            student, project = node_a, node_b
        else:
            assert isinstance(node_a, Projeto)
            assert isinstance(node_b, Aluno)
            project, student = node_a, node_b

        # Checa se a aresta já existe, se sim inverte para cobrir todo o
        # caminho encontrado
        if state.is_matched(student, project):
            state.remove_pair(student, project)
            # adiciona aresta removida ao reject_edges (REJEIÇAO)
            state.rejected_edges.append({"aluno": student.cod, "projeto": project.cod})
        # se não, adicionamos a aresta ao state (primeira e última do caminho)
        else:
            state.add_pair(student, project)


def run_iterations(
    graph: nx.Graph,
    initial_state: MatchingState,
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
    current_state = copy.deepcopy(initial_state)

    for iteration in range(1, n_iterations + 1):
        current_state.iteration = iteration
        # Limpa logs da iteração anterior
        current_state.proposed_edges = []
        current_state.rejected_edges = []

        free_students = list(current_state.free_students)
        free_students.sort(key=lambda x: x.cod)
        found_augmeting_path = None

        for student in free_students:
            found_augmeting_path = find_augmenting_path(student, graph, current_state)
            if found_augmeting_path:
                break

        if found_augmeting_path:
            # Adiciona caminho (Separa as arestas de IDA - [(Aluno -> Projeto)])
            for idx in range(0, len(found_augmeting_path) - 1, 2):
                u, v = found_augmeting_path[idx], found_augmeting_path[idx + 1]
                current_state.proposed_edges.append({"aluno": u.cod, "projeto": v.cod})

            # Log visual
            iteration_log = {
                "matched_edges": [(s, p) for s, p in current_state.matching],
                "proposed_edges": current_state.proposed_edges,
                "rejected_edges": current_state.rejected_edges,
            }

            # callback
            if on_iteration_end is not None:
                on_iteration_end(current_state, iteration_log, iteration)

            # Aplica Caminho M-Aumentanate
            augment_matching(found_augmeting_path, current_state)

        # adiciona o estado dessa iteração no histórico
        state_history.append(copy.deepcopy(current_state))
        print(f"Iteração[{iteration}]:\n{current_state}")

    return state_history
