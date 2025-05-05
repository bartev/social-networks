#!/usr/bin/env python3

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

st.title("Graph Visualization")

n = st.slider(label="Number of nodes", min_value=5, max_value=30, value=10)
p = st.slider(label="Probability of edge creation",  min_value=0.1, max_value=1.0, value=0.3)

# Create a simple graph
G = nx.erdos_renyi_graph(n=n, p=p)

# Draw the graph using matplotlib
fig, ax = plt.subplots()
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, ax=ax, node_color="skyblue", edge_color="red", node_size=500)

# Show the plot in Streamlit
st.pyplot(fig)


# Create network
net = Network(notebook=False, height="500px", width="100%")
net.from_nx(G)

# Save and load it in Streamlit
net.save_graph("graph.html")
components.html(open("graph.html", "r").read(), height=500)

