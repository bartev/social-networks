import matplotlib.pyplot as plt
import mplcursors
import networkx as nx
from matplotlib import cm as cm


def draw_pretty_hover(G, scale_by_degree=False, color_by_degree=False):
    """Draw a pretty graph with hover.

    Parameters:
    - G: networkx.Graph
    - scale_by_degree: bool, if True, scale node sizes by degree
    - color_by_degree: bool, if True, color nodes by degree
    """
    pos = nx.kamada_kawai_layout(G)

    fig, ax = plt.subplots(figsize=(10, 8))

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
