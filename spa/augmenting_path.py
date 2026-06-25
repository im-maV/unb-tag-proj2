"""
spa.augmenting_path
====================
Implementa a busca por caminhos M-alternados/aumentantes, usada nas 10
iterações exigidas pelo enunciado para tentar aumentar o emparelhamento a
partir dos alunos que ficaram sem projeto na rodada anterior.
"""
import copy
from models import Aluno
from collections import deque

def find_augmenting_path(start_student, graph, state) -> list | None:
    """
    Busca (BFS ou DFS alternada) um caminho M-aumentante a partir de um
    aluno livre, alternando entre arestas fora do emparelhamento e arestas
    dentro do emparelhamento, até alcançar um projeto com vaga disponível.
    Retorna a sequência de vértices do caminho, ou None se não existir.
    """
    # Fila que contém o nó atual e uma lista com o caminho percorrido
    queue = deque([start_student, [start_student]])
    visited = {start_student}

    while queue:
        current_node, path = queue.popleft()
        is_student = (type(current_node) == Aluno)

        if is_student:
            for project in graph.neighbors(current_node):
                if not state.is_matched(current_node, project):
                    if project not in visited:
                        visited.add(project)
                        queue.append((project, path + [project]))
        else: 
            if state.has_capacity(current_node): 
                return path
            
            allocated_students = state.get_allocated_students(current_node)
            
            for alloc_student in allocated_students:
                if alloc_student not in visited:
                    visited.add(alloc_student)
                    queue.append((alloc_student, path + [alloc_student]))
    return None


def augment_matching(path: list, state) -> None:
    """
    Aplica a operação de augmentação sobre o emparelhamento atual: inverte
    o status (dentro/fora de M) de cada aresta do caminho encontrado,
    aumentando o emparelhamento em 1.
    """
    for i in range(len(path) - 1):
        node_a = path[i]
        node_b = path[i + 1]

        # Checa tipo
        if(type(node_a) == Aluno): 
            student, project = node_a, node_b
        else:
            project, student = node_a, node_b

        # Checa se a aresta já existe, se sim inverte para cobrir todo o 
        # caminho encontrado
        if(state.is_matched(student, project)):
            del state.matching[student]
            if student in state.allocated_projects.get(project, []):
                state.allocated_projects[project].remove(student)
        # se não, adicionamos a aresta ao state (primeira e última do caminho)
        else: 
            state.matching[student] = project
            # Como não podemos deixar projetos sem alocação creio que 
            # essa verificação é válida
            if project not in state.allocated_projects:
                state.allocated_projects[project] = []
            state.allocated_projects[project].append(student)

def run_iterations(
    graph,
    initial_state,
    free_students,
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
    state_history = []
    current_state = copy.deepcopy(initial_state)

    for iteration in range(1, n_iterations + 1): 
        current_state.iteration = iteration

        free_students.sort(key=lambda x: x.cod)

        for student in free_students:
            path = find_augmenting_path(student, graph, current_state)

            if path: 
                augment_matching(path, current_state)
        
        # Log visual
        interation_log = {
            'proposed_edges': current_state.proposed_edges,
            'matched_edges': [(s, p) for s, p in current_state.matchings.items()],
            'rejected_edges': current_state.rejected_edges
        }

        # callback
        if on_iteration_end is not None:
            on_iteration_end(current_state, interation_log, iteration)
        
        # adiciona o estado dessa iteração no histórico
        state_history.append(copy.deepcopy(current_state))
    
    return state_history

