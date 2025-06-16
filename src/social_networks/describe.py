from statistics import mean

import matplotlib.pyplot as plt
import networkx as nx
import rich
from networkx.algorithms import diameter, radius


def describe_graph(g):
    avg_shortest_path = nx.average_shortest_path_length(g)
    rad = nx.radius(g)
    diam = nx.diameter(g)
    center = nx.center(g)
    periphery = nx.periphery(g)

    # print(f"Avg shortest path: {avg_shortest_path:.3f}")
    # print(f"Radius: {radius}")
    # print(f"Diameter: {diameter}")

    summary = {
        "avg_shortest_path": avg_shortest_path,
        "radius": rad,
        "diameter": diam,
        "center": center,
        "periphery": periphery,
    }
    rich.print(summary)
    return summary


def describe_graph_2(g: nx.MultiDiGraph, print_result=False):
    """Summary stats on the largest component subgraph of g"""
    summary = {
        "type": type(g).__name__,
        "directed": g.is_directed(),
        "multigraph": g.is_multigraph(),
        "num_nodes": g.number_of_nodes(),
        "num_edges": g.number_of_edges(),
    }

    # Degree statistics
    degrees = dict(g.degree())
    in_degrees = dict(g.in_degree()) if g.is_directed() else None
    out_degrees = dict(g.out_degree()) if g.is_directed() else None

    degree_stats = {"avg_degree": mean(degrees.values())}
    if in_degrees:
        degree_stats["max_in_degree"] = max(in_degrees.values())

    if out_degrees:
        degree_stats["max_out_degree"] = max(out_degrees.values())

    # Connected components
    components = {}
    try:
        if g.is_directed():
            wcc = list(nx.weakly_connected_components(g))
            scc = list(nx.strongly_connected_components(g))
            components["num_weakly_connected_components"] = len(wcc)
            components["largest_wcc_size"] = max(len(c) for c in wcc)
            components["num_strongly_connected_components"] = len(scc)
            components["largest_scc_size"] = max(len(c) for c in scc)
            component_subgraph = g.subgraph(max(wcc, key=len))
        else:
            cc = list(nx.connected_components(g))
            components["num_connected_components"] = len(cc)
            components["largest_component_size"] = max(len(c) for c in cc)
            component_subgraph = g.subgraph(max(cc, key=len))
    except Exception as e:
        print("[red]Component analysis failed:[/red]", e)
        component_subgraph = g

    # Shortest path metrics (on largest component)
    shortest_path_metrics = {}
    try:
        shortest_path_metrics["avg_shortest_path"] = nx.average_shortest_path_length(
            component_subgraph
        )
        shortest_path_metrics["radius"] = nx.radius(component_subgraph)
        shortest_path_metrics["diameter"] = nx.diameter(component_subgraph)
        shortest_path_metrics["center"] = nx.center(component_subgraph)
        shortest_path_metrics["periphery"] = nx.periphery(component_subgraph)
    except Exception as e:
        print("[yellow]Path metric calculation failed:[/yellow]", e)

    # Edge attribute summary (e.g., timestamps)
    edge_attribs = {}
    if g.number_of_edges() > 0:
        edge_attrs = list(next(iter(g.edges(data=True)))[2].keys())
        if "time" in edge_attrs:
            times = [
                d["time"] for _, _, _, d in g.edges(data=True, keys=True) if "time" in d
            ]
            edge_attribs["min_time"] = min(times)
            edge_attribs["max_time"] = max(times)
            edge_attribs["avg_time"] = int(mean(times))

            # # Optional: show histogram
            # plt.hist(times, bins=30)
            # plt.title("Edge Timestamp Distribution")
            # plt.xlabel("Time")
            # plt.ylabel("Frequency")
            # plt.show()

    result = {
        "summary": summary,
        "degree_stats": degree_stats,
        "components": components,
        "shortest_path": shortest_path_metrics,
        "edge_attrs": edge_attribs,
    }
    if print_result:
        rich.print("[bold blue]Graph Summary:[/bold blue]")
        rich.print(result)
    return result
