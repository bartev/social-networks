#!/usr/bin/env python3

# Create a simple graph
import networkx as nx
import streamlit as st
import matplotlib as mpl
import matplotlib.pyplot as plt


# Create a simple graph
G = nx.erdos_renyi_graph(n=10, p=0.3)

# Draw the graph using matplotlib
fig, ax = plt.subplots()
nx.draw(G, with_labels=True, ax=ax)

# Show the plot in Streamlit
st.pyplot(fig)
