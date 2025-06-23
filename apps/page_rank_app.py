#!/usr/bin/env python3


import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import social_networks.page_rank as pg_rnk
import social_networks.visualize as viz
import streamlit as st

st.title("PageRank Visualizer")


def get_graph(G=None):
    """Get a default graph if one is not provided"""
    if G:
        return G

    # Example graph
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("D", "C")]

    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


# User input for number of iterations
k = st.sidebar.slider(
    label="Number of PageRank iterations", min_value=1, max_value=50, value=5
)
alpha = st.sidebar.slider(
    "Damping factor (alpha)", min_value=0.0, max_value=1.0, value=0.85, step=0.01
)
seed = st.sidebar.number_input("Layout seed", min_value=0, value=42, step=1)

# Compute pageRank
G = get_graph()
# pr = pg_rnk.pagerank_steps(G, k=k, alpha=alpha)
pr, history = pg_rnk.pagerank_steps_with_history(G, k=k, alpha=alpha)

# Layout and color setup
pos = nx.spring_layout(G, seed=seed)

# Scale node sizes based on PR (optional min size)
min_size = 700
node_sizes = [min_size + 2500 * pr[node] for node in G.nodes()]

# Use PR as a label (formatted to 3 decimals)
# labels = {node: f"{node}\n{pr[node]:.3f}" for node in G.nodes()}

# Normalize PR for coloring
pr_values = np.array(list(pr.values()))
vmin = pr_values.min()  # clip color range so not too light or dark
vmax = pr_values.max()
buffer = (vmax - vmin) * 0.25  # Shrink extremes by 20%
norm = mcolors.Normalize(vmin=vmin - buffer, vmax=vmax + buffer)
cmap = cm.get_cmap("Blues")
node_colors = [cmap(norm(pr[node])) for node in G.nodes()]


# Draw the graph
st.subheader("Directed Graph")
fig, ax = plt.subplots(figsize=(5, 4))


nx.draw_networkx_nodes(G, pos=pos, node_size=node_sizes, node_color=node_colors, ax=ax)
# nx.draw_networkx_labels(
#     G, pos, labels=labels, font_size=10, font_weight="normal", ax=ax
# )
for node in G.nodes():
    x, y = pos[node]
    color = cmap(norm(pr[node]))
    label_color = "white" if viz.is_dark(color) else "black"
    ax.text(
        x,
        y,
        f"{node}\n{pr[node]:.3f}",
        fontsize=10,
        # fontweight="bold",
        ha="center",
        va="center",
        color=label_color,
    )
nx.draw_networkx_edges(
    G,
    pos=pos,
    arrowstyle="-|>",
    arrowsize=20,
    connectionstyle="arc3,rad=0.15",
    edge_color="gray",
    ax=ax,
    min_source_margin=15,
    min_target_margin=20,  # to end arrows away from the center of the node
)
ax.set_axis_off()
st.pyplot(fig)

# Display PageRank values
st.subheader("PageRank Scores")
st.dataframe({"Node": list(pr.keys()), "PageRank": [round(v, 3) for v in pr.values()]})

# --- Convergence Plot ---
st.subheader("PageRank Convergence")

fig2, ax2 = plt.subplots(figsize=(6, 4))
nodes = list(G.nodes())
for node in nodes:
    ax2.plot([hist[node] for hist in history], label=node, linewidth=2)

ax2.set(
    xlabel="Iteration", ylabel="PageRank Value", title="PageRank Values Over Iterations"
)
ax2.legend()


st.pyplot(fig2)
