"""
main.py
=======
    1. Parsing do arquivo de entrada
    2. Construção do grafo bipartido
    3. Emparelhamento estável inicial (Gale-Shapley adaptado)
    4. 10 iterações de aumento via caminhos alternados, exibindo o grafo
       gerado a cada iteração
    5. Validação de estabilidade do emparelhamento final
    6. Cálculo de métricas (índice de preferência, matriz final)
    7. Exibição/exportação dos resultados finais
"""

import spa

# INPUT_FILE_PATH = "data/entradaProj2.26TAG.txt"
INPUT_FILE_PATH = "data/small_data1.txt"
N_ITERATIONS = 10


def main() -> None:
    """Ponto de entrada principal — executa o pipeline completo de alocação."""

    # 1. Parsing
    projetos, alunos = spa.parse_input_file(INPUT_FILE_PATH)
    # validate_parsed_data(projetos, alunos)

    # 2. Construção do grafo bipartido
    graph = spa.build_bipartite_graph(projetos, alunos)

    # 3. Emparelhamento estável inicial (Gale-Shapley adaptado)
    m, acp, reject, allocated, free = spa.run_gale_shapley(projetos, alunos)
    state = spa.build_matching_state(
        matching=m,
        rejected_edges=reject,
        allocated_projects=allocated,
        free_students=free,
        iteration=0,
    )

    # 4. Iterações de aumento via caminhos alternados
    iteration_states = spa.run_iterations(
        graph,
        state,
        free_students=state.free_students,
        n_iterations=N_ITERATIONS,
        on_iteration_end=spa.plot_bipartite_iteration,
    )
    final_state = iteration_states[-1]

    # 5. Validação
    assert spa.is_stable_matching(final_state, graph, projetos), (
        "Emparelhamento final não é estável — revisar critério de "
        "aceite/rejeição do Gale-Shapley ou a busca por caminhos "
        "aumentantes."
    )

    # 6. Métricas
    preference_indices = spa.compute_all_preference_indices(final_state, graph)
    matching_matrix = spa.build_final_matching_matrix(final_state, graph)

    # 7. Saída final
    spa.plot_preference_index_summary(preference_indices)
    print(matching_matrix)


def _debug() -> None:
    """Executa fluxo completo para debug — remover futuramente."""
    projetos, alunos = spa.parse_input_file(INPUT_FILE_PATH)
    m, acp, reject, allocated, free = spa.run_gale_shapley(
        alunos=alunos, projetos=projetos
    )
    print("=== Gale-Shapley ===")
    print(m)

    state = spa.build_matching_state(
        matching=m,
        rejected_edges=reject,
        allocated_projects=allocated,
        free_students=free,
        iteration=0,
    )
    print("\n=== MatchingState ===")
    print(state)

    graph = spa.build_bipartite_graph(projetos, alunos)
    spa.plot_bipartite_iteration(graph, state)
    print("\n=== Grafo Bipartido ===")
    print(f"Nós: {graph.number_of_nodes()} | Arestas: {graph.number_of_edges()}")
    for a, p, data in graph.edges(data=True):
        print(f"  {a} -> {p} | pref={data['preferencia']}")

    matrix = spa.build_final_matching_matrix(state, graph)
    spa.save_matching_matrix_csv(matrix, "output/final_matching_matrix.csv")
    print("\n=== Matriz de Emparelhamento ===")
    print(matrix.to_string(index=False))


if __name__ == "__main__":
    # main()
    _debug()
