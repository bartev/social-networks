#!/usr/bin/env python3


import networkx as nx


def pagerank_steps(G, k: int = 1, alpha: float = 0.85):
    """Calculate the basic page rank after `k` iterations
    k: number of steps to take
    alpha: damping factor
    """
    num_nodes = G.number_of_nodes()
    if num_nodes == 0:
        return {}

    pr = {node: 1 / num_nodes for node in G.nodes()}

    for _ in range(k):
        new_pr = {}
        dangling_sum = sum(pr[n] for n in G.nodes() if G.out_degree(n) == 0)

        for node in G.nodes():
            incoming = G.predecessors(node)
            rank_sum = sum(
                pr[neigh] / G.out_degree(neigh)
                for neigh in incoming
                if G.out_degree(neigh) > 0
            )
            new_pr[node] = (1 - alpha) / num_nodes + alpha * (
                rank_sum + dangling_sum / num_nodes
            )

        pr = new_pr

    return pr


def pagerank_steps_with_history(G, k=1, alpha=0.85):
    N = G.number_of_nodes()
    if N == 0:
        return {}, []

    pr = {node: 1 / N for node in G.nodes()}
    history = [pr.copy()]

    for _ in range(k):
        new_pr = {}
        dangling_sum = sum(pr[n] for n in G.nodes() if G.out_degree(n) == 0)
        for node in G.nodes():
            incoming = G.predecessors(node)
            rank_sum = sum(
                pr[neigh] / G.out_degree(neigh)
                for neigh in incoming
                if G.out_degree(neigh) > 0
            )
            new_pr[node] = (1 - alpha) / N + alpha * (rank_sum + dangling_sum / N)

        pr = new_pr
        history.append(pr.copy())

    return pr, history
