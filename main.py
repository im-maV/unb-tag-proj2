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

from spa import (
    parse_input_file,
    validate_parsed_data,
    build_bipartite_graph,
    run_gale_shapley,
    run_iterations,
    is_stable_matching,
    build_final_matching_matrix,
    compute_all_preference_indices,
)
from spa.visualization import plot_bipartite_iteration, plot_preference_index_summary

# INPUT_FILE_PATH = "data/entradaProj2.26TAG.txt"
INPUT_FILE_PATH = "data/small_data1.txt"
N_ITERATIONS = 10


def main() -> None:

    # 1. Parsing
    projetos, alunos = parse_input_file(INPUT_FILE_PATH)
    # validate_parsed_data(projetos, alunos)

    # 2. Construção do grafo bipartido
    graph = build_bipartite_graph(projetos, alunos)

    # 3. Emparelhamento estável inicial (Gale-Shapley adaptado)
    state = run_gale_shapley(projetos, alunos)

    # 4. Iterações de aumento via caminhos alternados
    iteration_states = run_iterations(
        graph,
        state,
        n_iterations=N_ITERATIONS,
        on_iteration_end=plot_bipartite_iteration,
    )
    final_state = iteration_states[-1]

    # 5. Validação
    assert is_stable_matching(final_state, graph, projetos), (
        "Emparelhamento final não é estável — revisar critério de "
        "aceite/rejeição do Gale-Shapley ou a busca por caminhos "
        "aumentantes."
    )

    # 6. Métricas
    preference_indices = compute_all_preference_indices(final_state, graph)
    matching_matrix = build_final_matching_matrix(final_state, graph)

    # 7. Saída final
    plot_preference_index_summary(preference_indices)
    print(matching_matrix)


if __name__ == "__main__":
    # main()
    projetos, alunos = parse_input_file(INPUT_FILE_PATH)
    m, acp, reject = run_gale_shapley(alunos=alunos, projetos=projetos)
    print(m)

    # debug only
    graph = build_bipartite_graph(projetos, alunos)
    print("Nós:", graph.number_of_nodes(), "| Arestas:", graph.number_of_edges())
    for a, p, data in graph.edges(data=True):
        print(f"{a} -> {p} | pref={data['preferencia']}")
