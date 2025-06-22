#!/usr/bin/env python3

"""Visualize PageRank or HITS in a streamlit app"""

import random

import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import social_networks.hits as hits
import social_networks.page_rank as pg_rnk
import social_networks.visualize as viz
import streamlit as st
from altair.vegalite.v5.schema.core import ScaleInvalidDataShowAsValuestrokeWidth

st.title("Network Centrality Visualizer")


def get_graph(G=None):
    """Get a default graph if one is not provided"""
    if G:
        return G

    # Example graph
    edges = [("A", "B"), ("A", "C"), ("B", "C"), ("C", "A"), ("D", "C")]

    G = nx.DiGraph()
    G.add_edges_from(edges)
    return G


# Sidebar controls

st.sidebar.header("Settings")

algorithm = st.sidebar.radio("Centrality Algorithm", ["PageRank", "HITS"])
# User input for number of iterations
k = st.sidebar.slider(label="Number of iterations", min_value=1, max_value=25, value=5)
seed = st.sidebar.number_input("Layout seed", min_value=0, value=42, step=1)
d = st.sidebar.slider(
    "Damping factor (alpha) (PageRank)",
    min_value=0.0,
    max_value=1.0,
    value=0.85,
    step=0.01,
)

# Compute pageRank
G = get_graph()

pr_values, pr_hist = pg_rnk.pagerank_steps_with_history(G, k=k, d=d)
auths, hubs, auth_hist, hub_hist = hits.hits_steps(G=G, k=k, with_history=True)
if algorithm == "PageRank":
    score_name = "PageRank"
    values = pr_values
    history_list = pr_hist
else:
    score_name = st.sidebar.radio("Use HITS:", ["Authority", "Hub"])
    values = auths if score_name == "Authority" else hubs
    history_list = auth_hist if score_name == "Authority" else hub_hist

# Draw the graph

st.subheader(f"Directed Graph ({score_name})")


def draw_nodes_and_values(
    G, values, buffer_pct: float = 0.25, color_map: str = "Blues", seed: int = 42
):
    """Draw the nodes and values for G, colored/sized by value"""
    # Layout and color setup
    node_vals = np.array(list(values.values()))
    # Normalize values for coloring
    vmin, vmax = (
        node_vals.min(),
        node_vals.max(),
    )  # clip color range so not too light/dark
    buffer = (vmax - vmin) * buffer_pct
    norm = mcolors.Normalize(vmin=vmin - buffer, vmax=vmax + buffer)
    cmap = cm.get_cmap(color_map)
    node_colors = [cmap(norm(values[node])) for node in G.nodes()]
    min_size = 700
    node_sizes = [min_size + 2500 * values[node] for node in G.nodes()]

    pos = nx.spring_layout(G, seed=seed)
    fig, ax = plt.subplots(figsize=(5, 4))
    nx.draw_networkx_nodes(
        G, pos=pos, node_size=node_sizes, node_color=node_colors, ax=ax
    )
    # Drawing the labels is a little more complicated due to the label_color
    # Determing label color based on the node color's brightness
    for node in G.nodes():
        x, y = pos[node]
        color = cmap(norm(values[node]))
        label_color = "white" if viz.is_dark(color) else "black"
        ax.text(
            x,
            y,
            f"{node}\n{values[node]:.3f}",
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


draw_nodes_and_values(G=G, values=values, seed=seed)

# Data Table


def draw_single_data_table(score_name: str):
    """Add a data table for the displayed scores"""
    st.subheader(f"{score_name} Scores")
    st.dataframe(
        {
            "Node": list(values.keys()),
            score_name: [round(v, 3) for v in values.values()],
        }
    )


def draw_data_table(pr_scores, auth_scores, hub_scores):
    """Add a data table containing PageRank, Authority and Hub scores"""
    st.subheader("Node Centrality Scores")
    nodes = list(pr_scores.keys())
    df = pd.DataFrame(
        {
            "Node": nodes,
            "PageRank": [round(pr_scores[n], 3) for n in nodes],
            "Authority": [round(auth_scores[n], 3) for n in nodes],
            "Hub": [round(hub_scores[n], 3) for n in nodes],
        }
    ).set_index("Node")

    st.dataframe(df)


draw_single_data_table(score_name=score_name)
draw_data_table(pr_scores=pr_values, auth_scores=auths, hub_scores=hubs)

# Convergence Plot


def jitter(epsilon: float = 1e-4):
    """Offset v by a tiny amount"""
    x = random.randint(-100, 100)
    return x * epsilon


def draw_convergence(score_name: str):
    """Draw a plot of the score histories"""
    st.subheader(f"{score_name} Convergence")
    fig, ax = plt.subplots(figsize=(5, 4))

    epsilon = st.sidebar.number_input(
        "Jitter epsilon (for convergence plot)",
        min_value=0.0,
        max_value=0.01,
        value=0.0001,
        step=0.0001,
        format="%g",
    )
    nodes = list(G.nodes())
    markers = ["o", "s", "D", "^", "v", "<", ">", "x", "*", "+"]
    for i, node in enumerate(nodes):
        ax.plot(
            [hist[node] + jitter(epsilon) for hist in history_list],
            label=node,
            linewidth=2,
            marker=markers[i % len(markers)],
            markersize=5,
        )

    ax.set(
        xlabel="Iteration",
        ylabel=score_name,
        title=f"{score_name} Over Iterations",
    )
    ax.legend()
    st.pyplot(fig)


draw_convergence(score_name=score_name)
