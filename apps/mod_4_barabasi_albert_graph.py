#!/usr/bin/env python3

# Plot the barabasi_albert graph (preferential attachement model)

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

st.title("Preferential Attachment Model\nBarabasi Albert Graph")

# Sidebar options

# n = st.number_input(
#     label="Number of nodes", min_value=10, max_value=1_000_000, value=1000, step=100
# )
log_n = st.slider("log₁₀(Number of nodes)", 1, 6, 3)
n = 10**log_n

m = st.slider(label="Number of edges per step", min_value=1, max_value=10, value=1)

# Create a graph
G = nx.barabasi_albert_graph(n, m)

degrees = dict(G.degree())
degree_values = sorted(set(degrees.values()))
num_nodes = nx.number_of_nodes(G)
histogram = [list(degrees.values()).count(i) / num_nodes for i in degree_values]


fig, ax = plt.subplots()
ax.plot(degree_values, histogram, "o")
ax.set(
    xlabel="Degree",
    ylabel="Fraction of Nodes",
    title=f"Distribution in Preferential Attachment Model\n({n=:,}, {m=})",
)
ax.set(xscale="log", yscale="log")
st.pyplot(fig)
