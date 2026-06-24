"""
Pacote spa — Student-Project Allocation.

Reúne os módulos de parsing, construção de grafo, algoritmo de
emparelhamento estável (Gale-Shapley adaptado), iterações por caminhos
aumentantes, métricas e visualização.

Importar deste pacote no notebook (`from spa import ...`) garante que IDE e
notebook usem exatamente o mesmo código-fonte, sem duplicação de lógica.
"""

from spa.parser import parse_input_file, validate_parsed_data
from spa.graph_builder import build_bipartite_graph, get_bipartite_sets
from spa.gale_shapley import run_gale_shapley, build_matching_state
from spa.augmenting_path import run_iterations, find_augmenting_path
from spa.metrics import build_final_matching_matrix, compute_all_preference_indices
from spa.visualization import plot_all_iterations, plot_preference_index_summary
from spa.validation import is_stable_matching, find_blocking_pairs
