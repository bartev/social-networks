#!/usr/bin/env python3

import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

st.title("Graph Visualization with NetworkX")

choice_mpl = "Matplotlib"
choice_pyv = "Interactive (Pyvis)"
# Sidebar options
n = st.slider(label="Number of nodes", min_value=5, max_value=30, value=10)
p = st.slider(label="Probability of edge creation",  min_value=0.1, max_value=1.0, value=0.3)
view_option = st.sidebar.multiselect(
    label="Choose display format(s):",
    options=[choice_mpl, choice_pyv]
)

# Create a simple graph
G = nx.erdos_renyi_graph(n=n, p=p)

# Layout
pos = nx.spring_layout(G)

# Setup column layout depending on choice

if set(view_option) == {choice_mpl, choice_pyv}:
    col1, col2 = st.columns(2)
else:
    col1 = col2 = st.container() # Use full width if only 1 is selected

# Matplotlib graph

if choice_mpl in view_option:
    with col1:
        st.subheader("Matplotlib View")
        fig, ax = plt.subplots()

        nx.draw(G, with_labels=True, ax=ax, node_color="skyblue", edge_color="red", node_size=500)

        # Show the plot in Streamlit
        st.pyplot(fig)

# Pyvis interactive graph

if choice_pyv in view_option:
    with col2:
        st.subheader("Interactive View (Pyvis)")

        # Create network
        net = Network(notebook=False, height="500px", width="100%")
        net.from_nx(G)

        # Save and load it in Streamlit
        net.save_graph("graph.html")
        html_file = open("graph.html", "r", encoding="utf-8")
        components.html(html_file.read(), height=500)
