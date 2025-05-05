#!/usr/bin/env python3


import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

n = st.slider(label="Number of nodes", min_value=5, max_value=30, value=10)
p= st.slider(label="Probability of edge creation",  min_value=0.1, max_value=1.0, value=0.3)

# Create a simple graph
G = nx.erdos_renyi_graph(n=n, p=p)

# Draw the graph using matplotlib
fig, ax = plt.subplots()
nx.draw(G, with_labels=True, ax=ax)

# Show the plot in Streamlit
st.pyplot(fig)
