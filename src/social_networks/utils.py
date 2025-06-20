# Utility functions for exploring graphs

import networkx as nx
from networkx import Graph
from rich.columns import Columns
from rich.console import Console
from rich.table import Table


def top_n_by_dict_val(d: dict, k: int) -> list:
    """Return the top `k` elements of `d`, sorted by the values of `d`"""
    return sorted(d.items(), key=lambda x: float(x[1]), reverse=True)[:k]


def build_table(title, data):
    """Build Rich tables"""
    table = Table(title=title, show_header=True, header_style="bold yellow")
    table.add_column("Node", style="cyan", no_wrap=True)
    table.add_column("Score", justify="right", style="green")

    for node, score in data:
        table.add_row(str(node), f"{score:.3f}")
    return table


def print_top_hubs_auths(g: Graph, k: int | None = None) -> tuple:
    """
    Print out 2 side by side tables of the top Hubs and Authorities for graph g
    """
    hits_hubs, hits_auths = nx.hits(g)

    if k is None:
        k = len(hits_hubs)

    top_hubs = top_n_by_dict_val(hits_hubs, k)
    top_auths = top_n_by_dict_val(hits_auths, k)

    hub_table = build_table("Top Hubs", top_hubs)
    auth_table = build_table("Top Auths", top_auths)

    # Display side by
    console = Console()
    console.print(Columns([hub_table, auth_table]))

    return top_hubs, top_auths
