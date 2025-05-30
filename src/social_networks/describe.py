import networkx as nx
import rich
from networkx.algorithms import diameter, radius


def describe_graph(g):
    avg_shortest_path = nx.average_shortest_path_length(g)
    radius = nx.radius(g)
    diameter = nx.diameter(g)
    center = nx.center(g)
    periphery = nx.periphery(g)

    # print(f"Avg shortest path: {avg_shortest_path:.3f}")
    # print(f"Radius: {radius}")
    # print(f"Diameter: {diameter}")

    summary = {
        "avg_shortest_path": avg_shortest_path,
        "radius": radius,
        "diameter": diameter,
        "center": center,
        "periphery": periphery,
    }
    rich.print(summary)
    return summary
