"""
spa.visualization
==================
Funções de plotagem do grafo bipartido colorido por iteração, e de
visualizações auxiliares (índice de preferência, matriz final).
"""

from pathlib import Path
import re
from typing import Any, Mapping

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

import networkx as nx
from models.aluno_model import Aluno
from models.matching_model import MatchingState
from models.projeto_model import Projeto
from spa.graph_builder import get_bipartite_sets

try:
    from IPython import get_ipython  # type: ignore

    shell = get_ipython()
    if shell is None:
        matplotlib.use("Agg")
except (ImportError, NameError):
    matplotlib.use("Agg")

EdgePair = tuple[str, str]

Node = Aluno | Projeto
OUTPUT_DIR = Path("output")


class VisualConfig:
    """Configuração de visualização."""

    # Cores das arestas
    C_PROPOSED = "#EEBF1D"
    C_MATCHED = "#5ba8b5"
    C_REJECTED = "#D12F10"
    C_NEUTRAL = "#94a3b8"

    # Cores dos nós
    C_STUDENT = "#16426c"
    C_PROJECT = "#0d2b35"

    C_TEXT_MAIN = "#0f172a"
    C_TEXT_MUTED = "#334155"
    C_BORDER = "#94a3b8"
    C_BG_PANEL = "#f1f5f9"

    ALPHA = {C_MATCHED: 0.95, C_PROPOSED: 0.90, C_REJECTED: 0.75, C_NEUTRAL: 0.25}
    WIDTH = {C_MATCHED: 2.6, C_PROPOSED: 2.2, C_REJECTED: 1.4, C_NEUTRAL: 0.6}

    INCHES_PER_NODE = 0.42
    FIG_WIDTH = 18.0


class BipartiteLayout:
    """
    Layout para grafo bipartido, com alunos à direita e projetos à esquerda.
    A altura do layout é proporcional ao número máximo de nós em cada conjunto.
    """

    def __init__(self, students: list[Aluno], projects: list[Projeto]):
        self.students = students
        self.projects = projects
        self.n_max = max(len(students), len(projects), 1)

    @property
    def height(self) -> float:
        """Altura do layout em polegadas, proporcional ao número de nós."""
        return max(16.0, self.n_max * VisualConfig.INCHES_PER_NODE)

    def get_positions(self) -> dict[Node, tuple[float, float]]:
        """Retorna o dicionário de posições (x, y) para cada nó do grafo."""
        step = self.height / self.n_max
        pos: dict[Node, tuple[float, float]] = {}

        for i, node in enumerate(self.students):
            pos[node] = (1.0, -i * step)
        for i, node in enumerate(self.projects):
            pos[node] = (0.0, -i * step)

        return pos


def get_node_id(node: Node) -> str:
    """Extrai o identificador de texto único (matrícula ou código) de um nó do grafo."""
    val = getattr(node, "cod", node)
    return str(val)


def sort_node_key(node: Node) -> list[int | str]:
    """Extrai o identificador de texto único (matrícula ou código) de um nó do grafo."""
    return [
        int(text) if text.isdigit() else text.lower()
        for text in re.split(r"(\d+)", get_node_id(node))
    ]


def _normalize_edge(edge: tuple[Node, Node]) -> EdgePair:
    u, v = edge
    cod_u = get_node_id(u)
    cod_v = get_node_id(v)
    return (cod_u, cod_v) if cod_u <= cod_v else (cod_v, cod_u)


def _save_figure(filename: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    plt.savefig(OUTPUT_DIR / filename, dpi=140, bbox_inches="tight")
    plt.close()


def _extract_edge_pairs(raw_edges: Any) -> set[EdgePair]:
    if not raw_edges:
        return set()

    if isinstance(raw_edges, dict):
        return {
            _normalize_edge((u, v))
            for u, v in raw_edges.items()
            if u is not None and v is not None
        }

    pairs = set()
    for item in raw_edges:
        ends = _get_edge_ends(item)
        if ends:
            pairs.add(_normalize_edge(ends))
    return pairs


def _get_edge_ends(item: Any) -> tuple[Any, Any] | None:
    if isinstance(item, tuple) and len(item) == 2:
        return item[0], item[1]
    if isinstance(item, dict):
        u = item.get("aluno") or item.get("student")
        v = item.get("projeto") or item.get("project")
        if u is not None and v is not None:
            return u, v
    return None


def _get_edge_colors(
    graph: nx.Graph,
    state: MatchingState,
    iteration_log: dict | None = None,
) -> Mapping[EdgePair, str]:
    """
    Retorna um dicionário de cores para cada aresta do grafo,
    baseado no estado atual do emparelhamento.
    """
    source = iteration_log if iteration_log is not None else state.__dict__

    matched = _extract_edge_pairs(source.get("matched_edges"))
    rejected = _extract_edge_pairs(source.get("rejected_edges"))
    proposed = _extract_edge_pairs(source.get("proposed_edges"))

    colors: dict[EdgePair, str] = {}
    for u, v in graph.edges():
        norm_e = _normalize_edge((u, v))
        if norm_e in matched:
            colors[norm_e] = VisualConfig.C_MATCHED
        elif norm_e in rejected:
            colors[norm_e] = VisualConfig.C_REJECTED
        elif norm_e in proposed:
            colors[norm_e] = VisualConfig.C_PROPOSED
        else:
            colors[norm_e] = VisualConfig.C_NEUTRAL

    return colors


def plot_bipartite_iteration(
    state: MatchingState,
    iteration_log: dict[str, Any] | None,
    iteration: int,
    graph: nx.Graph,
) -> None:
    """
    Plota o grafo bipartido para uma iteração específica,
    colorindo as arestas de acordo com o estado do emparelhamento.
    """
    students_raw, projects_raw = get_bipartite_sets(graph)
    students = sorted(students_raw, key=sort_node_key)
    projects = sorted(projects_raw, key=sort_node_key)

    layout = BipartiteLayout(students, projects)
    pos = layout.get_positions()
    edgelist = list(graph.edges())

    fig, ax = plt.subplots(figsize=(VisualConfig.FIG_WIDTH, layout.height))

    color_map = _get_edge_colors(graph, state, iteration_log)
    edges_by_color: dict[str, list] = {c: [] for c in VisualConfig.ALPHA}

    for u, v in edgelist:
        c = color_map.get(_normalize_edge((u, v)), VisualConfig.C_NEUTRAL)
        edges_by_color[c].append((u, v))

    draw_order = [
        VisualConfig.C_NEUTRAL,
        VisualConfig.C_REJECTED,
        VisualConfig.C_PROPOSED,
        VisualConfig.C_MATCHED,
    ]

    for cat_color in draw_order:
        if cat_edges := edges_by_color[cat_color]:
            nx.draw_networkx_edges(
                graph,
                pos,
                edgelist=cat_edges,
                edge_color=cat_color,
                width=VisualConfig.WIDTH[cat_color],
                alpha=VisualConfig.ALPHA[cat_color],
                style="--" if cat_color == VisualConfig.C_REJECTED else "-",
                ax=ax,
            )

    node_configs = [
        (projects, VisualConfig.C_PROJECT, 320, "s", 7.5),
        (students, VisualConfig.C_STUDENT, 230, "o", 5.5),
    ]

    for nodelist, color, size, shape, font_size in node_configs:
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=nodelist,
            node_color=color,
            node_size=size,
            node_shape=shape,
            ax=ax,
        )
        nx.draw_networkx_labels(
            graph,
            pos,
            labels={n: get_node_id(n) for n in nodelist},
            font_size=font_size,
            font_color="white",
            font_weight="bold",
            ax=ax,
        )

    col_headers = [(0.0, "Projetos (■)"), (1.0, "Alunos (●)")]
    for x_pos, text in col_headers:
        ax.text(
            x_pos,
            1.0,
            text,
            color=VisualConfig.C_TEXT_MAIN,
            fontsize=12,
            fontweight="bold",
            ha="center",
            va="bottom",
            transform=ax.transAxes,
        )

    legend_patches = [
        mpatches.Patch(color=VisualConfig.C_MATCHED, label="Emparelhamento atual"),
        mpatches.Patch(color=VisualConfig.C_PROPOSED, label="Proposta ativa"),
        mpatches.Patch(color=VisualConfig.C_REJECTED, label="Rejeição"),
        mpatches.Patch(color=VisualConfig.C_NEUTRAL, label="Não proposta"),
        mpatches.Patch(color=VisualConfig.C_PROJECT, label="Projeto"),
        mpatches.Patch(color=VisualConfig.C_STUDENT, label="Candidato"),
    ]

    ax.legend(
        handles=legend_patches,
        loc="upper center",
        bbox_to_anchor=(0.5, 1.0),
        ncol=6,
        frameon=True,
        facecolor=VisualConfig.C_BG_PANEL,
        edgecolor=VisualConfig.C_NEUTRAL,
        fontsize=9.5,
        labelcolor=VisualConfig.C_TEXT_MAIN,
    )

    n_matched = len(edges_by_color[VisualConfig.C_MATCHED])
    iteration_number = iteration if iteration is not None else state.iteration
    ax.set_title(
        f"Iteração {iteration_number}  —  Alocação Atual: {n_matched} de {len(students)} Alunos",
        color=VisualConfig.C_TEXT_MAIN,
        fontsize=14,
        fontweight="bold",
        pad=5,
    )

    # Descobre a coordenada Y exata do nó mais alto e do mais baixo
    coords_y = [coord[1] for coord in pos.values()]
    y_topo, y_base = max(coords_y), min(coords_y)
    span = y_topo - y_base

    # Margem automática de 5% para apenas 1.2%
    respiro = span * 0.012

    ax.set_ylim(y_base - respiro, y_topo + respiro)
    ax.axis("off")
    _save_figure(f"iteracao_{state.iteration}.png")


def plot_preference_index_summary(preference_indices: Mapping[Projeto, float]) -> None:
    """Desenha o gráfico de barras do índice de preferência por projeto."""
    if not preference_indices:
        return

    items = sorted(preference_indices.items(), key=lambda kv: sort_node_key(kv[0]))
    codes, values = zip(*[(get_node_id(k), v) for k, v in items])

    fig, ax = plt.subplots(figsize=(15, 5.5))

    bars = ax.bar(codes, values, color=VisualConfig.C_MATCHED, width=0.65, zorder=3)
    ax.axhline(
        y=1.0,
        color=VisualConfig.C_REJECTED,
        linestyle="--",
        alpha=0.8,
        label="Preferência Máxima Ideal (1.0)",
        zorder=4,
    )

    for rectangle, val in zip(bars, values):
        ax.text(
            rectangle.get_x() + rectangle.get_width() / 2,
            rectangle.get_height() + 0.03,
            f"{val:.2f}",
            ha="center",
            va="bottom",
            fontsize=7.5,
            color=VisualConfig.C_TEXT_MUTED,
            fontweight="bold",
        )

    ax.set_xlabel(
        "Código do Projeto",
        fontweight="bold",
        color=VisualConfig.C_TEXT_MAIN,
        labelpad=10,
    )
    ax.set_ylabel(
        "Índice Médio de Preferência",
        fontweight="bold",
        color=VisualConfig.C_TEXT_MAIN,
        labelpad=10,
    )
    ax.set_title(
        "Índice de Preferência Agregado por Projeto",
        color=VisualConfig.C_TEXT_MAIN,
        fontsize=13,
        fontweight="bold",
        pad=15,
    )

    ax.tick_params(colors=VisualConfig.C_TEXT_MUTED)
    ax.spines[:].set_color(VisualConfig.C_BORDER)
    ax.grid(axis="y", linestyle=":", alpha=0.6, color=VisualConfig.C_BORDER, zorder=0)

    ax.set_xticks(range(len(codes)))
    ax.set_xticklabels(codes, rotation=45, ha="right", fontsize=8.5)
    ax.legend(
        fontsize=9.5,
        labelcolor=VisualConfig.C_TEXT_MAIN,
        facecolor=VisualConfig.C_BG_PANEL,
        edgecolor=VisualConfig.C_NEUTRAL,
    )

    plt.tight_layout()
    _save_figure("preference_index.png")
