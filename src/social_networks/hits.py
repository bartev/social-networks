#!/usr/bin/env python3


import networkx as nx


# Hyperlink-Induced Topic Search
def hits_steps(G: nx.DiGraph, k: int = 10, normalize: bool = True):
    nodes = list(G.nodes())

    auth = {node: 1.0 for node in nodes}
    hub = {node: 1.0 for node in nodes}

    auth_history = [auth.copy()]
    hub_history = [hub.copy()]

    # Iterate k times
    for _ in range(k):
        new_auth = {
            node: sum(hub.get(neigh, 0) for neigh in G.predecessors(node))
            for node in nodes
        }
        new_hub = {
            node: sum(auth.get(neigh, 0) for neigh in G.successors(node))
            for node in nodes
        }

        if normalize:
            # norm_auth = sum(v**2 for v in new_auth.values())**0.5 or 1
            # norm_hub = sum(v**2 for v in new_hub.values())**0.5 or 1

            norm_auth = sum(new_auth.values())
            norm_hub = sum(new_hub.values())
            new_auth = {k: v / norm_auth for k, v in new_auth.items()}
            new_hub = {k: v / norm_hub for k, v in new_hub.items()}

        auth = new_auth
        hub = new_hub

        auth_history.append(auth.copy())
        hub_history.append(hub.copy())

    return auth, hub, auth_history, hub_history
