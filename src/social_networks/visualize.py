import matplotlib.pyplot as plt
import mplcursors
import networkx as nx
from matplotlib import cm as cm
from networkx import Graph, MultiDiGraph


def draw_pretty_hover(G: Graph, scale_by_degree=False, color_by_degree=False):
    """Draw a pretty graph with hover.

    Parameters:
    - G: networkx.Graph
    - scale_by_degree: bool, if True, scale node sizes by degree
    - color_by_degree: bool, if True, color nodes by degree
    """
    pos = nx.kamada_kawai_layout(G)

    fig, ax = plt.subplots()

    if scale_by_degree:
        node_sizes = [G.degree[n] * 100 for n in G.nodes()]
    else:
        node_sizes = 300  # fixed size

    cmap = cm.get_cmap("coolwarm")  # or viridis

    if color_by_degree:
        node_colors = [G.degree[n] for n in G.nodes()]
        cmap = cmap
    else:
        node_colors = ["skyblue"]  # fixed color
        cmap = None

    nodes = nx.draw_networkx_nodes(
        G,
        pos,
        node_size=node_sizes,
        node_color=node_colors,  # type: ignore
        cmap=cmap,
        edgecolors="black",
        alpha=0.8,
        ax=ax,
    )

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="gray", width=1.2, alpha=0.5)
    nx.draw_networkx_labels(
        G, pos, ax=ax, font_size=9, font_color="navy", font_weight="bold"
    )

    # plt.title("Customized Karate Club Graph", fontsize=18)
    plt.axis("off")

    cursor = mplcursors.cursor(nodes, hover=True)

    @cursor.connect("add")
    def on_add(sel):
        node_index = sel.index
        node_id = list(G.nodes())[node_index]
        sel.annotation.set_text(f"Node {node_id}\nDegree: {G.degree[node_id]}")
        sel.annotation.get_bbox_patch().set(fc="lightyellow", alpha=0.9)

    plt.tight_layout()
    plt.show()
    return fig


def draw_big_multi_directed(G: MultiDiGraph, figsize=(4, 3), seed=1):
    """Draw `G` with large nodes, curved arrows, and multi-edges"""
    plt.figure(figsize=figsize)
    plt.clf()
    plt.cla()
    pos = nx.spring_layout(G, seed=seed)

    nx.draw_networkx_nodes(G, pos=pos, node_size=1500, node_color="skyblue")
    nx.draw_networkx_labels(
        G, pos, font_size=16, font_color="white", font_weight="bold"
    )
    nx.draw_networkx_edges(
        G,
        pos=pos,
        arrowstyle="-|>",
        arrowsize=20,
        edge_color="black",
        connectionstyle="arc3, rad=0.2",
        min_source_margin=15,
        min_target_margin=20,  # to end arrows away from the center of the node
    )
    plt.axis("off")
    plt.tight_layout()
    plt.show()


def is_dark(rgb_color):
    """Convert RGB to perceived brightness (0=dark, 1=bright)"""
    r, g, b = rgb_color[:3]
    brightness = 0.299 * r + 0.587 * g + 0.114 * b
    return brightness < 0.5
