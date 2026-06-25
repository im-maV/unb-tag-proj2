"""
spa.visualization
==================
Funções de plotagem do grafo bipartido colorido por iteração, e de
visualizações auxiliares (índice de preferência, matriz final).
"""

import networkx as nx
from pathlib import Path
from typing import Any, Mapping, Sequence, Set, Tuple

import matplotlib
import matplotlib.pyplot as plt

from matplotlib.lines import Line2D
from spa.graph_builder import get_bipartite_sets

matplotlib.use("Agg")
EdgePair = Tuple[str, str]

OUTPUT_DIR = Path("output")

# Cores das arestas
COLOR_PROPOSED = "#f3d364"
COLOR_MATCHED = "#5ba8b5"
COLOR_REJECTED = "#f05a3e"
COLOR_NEUTRAL = "#B0Bac4"

# Cores dos nós
COLOR_STUDENT = "#16426c"
COLOR_PROJECT = "#0d2b35"


def _normalize_edge(edge: tuple[Any, Any]) -> EdgePair:
    return tuple(sorted((str(edge[0]), str(edge[1]))))


def _extract_edge_pairs(raw_edges: Any) -> Set[EdgePair]:
    edges: Set[EdgePair] = set()
    if raw_edges is None:
        return edges

    if isinstance(raw_edges, dict):
        raw_edges = [raw_edges]

    if isinstance(raw_edges, Sequence) and not isinstance(raw_edges, (str, bytes)):
        for item in raw_edges:
            if isinstance(item, tuple) and len(item) == 2:
                edges.add(_normalize_edge(item))
            elif isinstance(item, dict):
                aluno = item.get("aluno") or item.get("student")
                projeto = item.get("projeto") or item.get("project")
                if aluno is not None and projeto is not None:
                    edges.add(_normalize_edge((aluno, projeto)))
    return edges


def _ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _save_figure(filename: str) -> None:
    _ensure_output_dir()
    path = OUTPUT_DIR / filename
    plt.savefig(path, bbox_inches="tight")
    plt.close()


def get_edge_colors(graph: nx.Graph, state: Any) -> Mapping[EdgePair, str]:
    """Retorna o dicionário de cores para cada aresta do grafo."""
    matched = _extract_edge_pairs(getattr(state, "matched_edges", None))
    rejected = _extract_edge_pairs(getattr(state, "rejected_edges", None))
    proposed = _extract_edge_pairs(getattr(state, "proposed_edges", None))

    colors: dict[EdgePair, str] = {}
    for u, v in graph.edges():
        edge = _normalize_edge((u, v))
        if edge in matched:
            colors[edge] = COLOR_MATCHED
        elif edge in rejected:
            colors[edge] = COLOR_REJECTED
        elif edge in proposed:
            colors[edge] = COLOR_PROPOSED
        else:
            colors[edge] = COLOR_NEUTRAL
    return colors


def _build_edge_color_list(
    graph: nx.Graph, edge_colors: Mapping[EdgePair, str]
) -> list[str]:
    return [
        edge_colors.get(_normalize_edge((u, v)), COLOR_NEUTRAL)
        for u, v in graph.edges()
    ]


def _draw_legend() -> None:
    legend_items = [
        Line2D([0], [0], color=COLOR_PROPOSED, lw=4, label="Proposta ativa"),
        Line2D([0], [0], color=COLOR_MATCHED, lw=4, label="Emparelhamento atual"),
        Line2D([0], [0], color=COLOR_REJECTED, lw=4, label="Rejeição"),
        Line2D([0], [0], color=COLOR_NEUTRAL, lw=4, label="Não proposta"),
    ]
    plt.legend(
        handles=legend_items, loc="upper center", bbox_to_anchor=(0.5, 1.05), ncol=4
    )


def plot_bipartite_iteration(graph: nx.Graph, state: Any) -> None:
    """Plota uma única iteração do grafo bipartido."""
    edge_colors = get_edge_colors(graph, state)
    students, projects = get_bipartite_sets(graph)
    pos = nx.bipartite_layout(graph, projects)
    colors = _build_edge_color_list(graph, edge_colors)

    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=sorted(students),
        node_color=COLOR_STUDENT,
        node_size=700,
        node_shape="o",
    )
    nx.draw_networkx_nodes(
        graph,
        pos,
        nodelist=sorted(projects),
        node_color=COLOR_PROJECT,
        node_size=900,
        node_shape="o",
    )
    nx.draw_networkx_edges(
        graph, pos, edgelist=list(graph.edges()), edge_color=colors, width=2
    )
    nx.draw_networkx_labels(graph, pos, font_size=10, font_color="white")
    _draw_legend()

    iteration = getattr(state, "iteration", "?")
    title = "Gale-Shapley (iteração 0)" if iteration == 0 else f"Iteração {iteration}"
    plt.title(title, pad=40)
    plt.axis("off")
    plt.tight_layout()
    _save_figure(f"iteracao_{iteration}.png")


def plot_all_iterations(graph: nx.Graph, states: Sequence[Any]) -> None:
    """Plota todas as iterações em sequência."""
    for state in states:
        plot_bipartite_iteration(graph, state)


def plot_preference_index_summary(preference_indices: Mapping[str, float]) -> None:
    """Desenha o gráfico de barras do índice de preferência por projeto."""
    if not preference_indices:
        return

    codes = sorted(preference_indices)
    values = [preference_indices[code] for code in codes]

    plt.figure(figsize=(10, 5))
    plt.bar(codes, values, color="#1ABC9C")
    plt.xlabel("Projeto")
    plt.ylabel("Índice de preferência")
    plt.title("Índice de preferência por projeto")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    _save_figure("preference_index.png")
