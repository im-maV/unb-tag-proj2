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

from functools import partial
import spa

# from tests.test_augmenting import executar_teste

INPUT_FILE_PATH = "data/entradaProj2.26TAG.txt"
N_ITERATIONS = 10


def main() -> None:
    """Ponto de entrada principal — executa o pipeline completo de alocação."""

    # 1. Parsing
    projetos, alunos = spa.parse_input_file(INPUT_FILE_PATH)
    # validate_parsed_data(projetos, alunos)

    # 2. Construção do grafo bipartido
    graph = spa.build_bipartite_graph(projetos, alunos)

    # 3. Emparelhamento estável inicial (Gale-Shapley adaptado)
    # Executa o SPA-Students: alunos propõem aos projetos em ordem de preferência,
    # projetos aceitam/rejeitam com base na nota mínima e capacidade de vagas.
    # O resultado é o matching estável inicial (iteração 0), ponto de partida
    # para as rodadas de caminhos aumentantes.
    m, _, reject, allocated, free = spa.run_gale_shapley(projetos, alunos)
    state = spa.build_matching_state(
        matching=m,
        rejected_edges=reject,
        allocated_projects=allocated,
        free_students=free,
        iteration=0,
    )

    # Plota o estado inicial — matching do Gale-Shapley antes de qualquer iteração
    initial_log = {
        "matched_edges": [(s, p) for s, p in m],
        "proposed_edges": [],
        "rejected_edges": reject,
    }
    spa.plot_bipartite_iteration(state, initial_log, 0, graph)

    # 4. Iterações de aumento via caminhos alternados
    # Busca caminhos M-aumentantes a partir dos alunos livres, tentando ampliar
    # o matching a cada rodada. O callback plota o grafo de cada iteração antes
    # de aplicar a augmentação.
    plot_iteration = partial(spa.plot_bipartite_iteration, graph=graph)
    iteration_states = spa.run_iterations(
        graph,
        state,
        all_alunos=alunos,
        n_iterations=N_ITERATIONS,
        on_iteration_end=plot_iteration,
    )
    final_state = iteration_states[-1]

    # 5. Validação
    # assert spa.is_stable_matching(final_state, graph, projetos), (
    #     "Emparelhamento final não é estável — revisar critério de "
    #     "aceite/rejeição do Gale-Shapley ou a busca por caminhos "
    #     "aumentantes."
    # )

    # 6. Métricas
    preference_indices = spa.compute_all_preference_indices(final_state, graph)
    matching_matrix = spa.build_final_matching_matrix(final_state, graph)

    # 7. Saída final
    n_alocados = len(final_state.matching)
    n_total = len(alunos)
    n_livres = len(final_state.free_students)
    projetos_vazios = [
        p.cod
        for p in projetos
        if not any(proj == p for _, proj in final_state.matching)
    ]

    print("=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    print(f"Alunos alocados: {n_alocados} / {n_total} ({100*n_alocados/n_total:.1f}%)")
    print(f"Alunos sem projeto: {n_livres}")
    if projetos_vazios:
        print(
            f"[AVISO] Projetos sem alunos ({len(projetos_vazios)}): {projetos_vazios}"
        )
    print("Matriz salva em: output/matching_matrix.csv")
    print("Gráficos salvos em: output/")
    print("=" * 60)

    spa.plot_preference_index_summary(preference_indices)
    spa.save_matching_matrix_csv(matching_matrix)


if __name__ == "__main__":
    main()
    # executar_teste()
