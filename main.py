from itertools import combinations, count, groupby
from random import choice, randint, random, sample
from queue import PriorityQueue

import networkx as nx
from matplotlib import pyplot as plt


def dijkstra(G: nx.Graph, start: int):
    visited = set()
    distances = {v: float('inf') for v in range(len(G.nodes))}
    distances[start] = 0
    pq = PriorityQueue()
    pq.put((0, start))
    while not pq.empty():
        dist, current_vertex = pq.get()
        visited.add(current_vertex)
        for neighbor in G.neighbors(current_vertex):
            current_dist = G[current_vertex][neighbor]["weight"]
            if neighbor not in visited:
                old_cost = distances[neighbor]
                # This line was modified to choose the edge with the biggest cost to assign to neighbour vertex
                # instead of assigning the sum between all visited vertexes in the current path so far.
                # (or distance between cities as it was specified in the problem)
                new_cost = max(distances[current_vertex], current_dist)
                if new_cost < old_cost:
                    pq.put((new_cost, neighbor))
                    distances[neighbor] = new_cost
    return distances

# Functions under this comment are only used to generate and test the algorithm. Currently generates 10 graphs.
# Number can be changed lower.

def get_random_connected_graph(n: int, p: float, max_w: int):
    all_edges = combinations(range(n), 2)
    G = nx.Graph()
    G.add_nodes_from(range(n))
    if p <= 0:
        return G
    if p >= 1:
        return nx.complete_graph(n, create_using=G)
    for _, node_edges in groupby(all_edges, key=lambda x: x[0]):
        node_edges = list(node_edges)
        random_edge = choice(node_edges)
        G.add_edge(*random_edge)
        for e in node_edges:
            if random() < p:
                G.add_edge(*e)
    for e in G.edges():
        G[e[0]][e[1]]["weight"] = randint(1, max_w)
    return G


def main():
    # You can modify range to generate more/less graphs.
    for it in range(0, 10):
        n = randint(2, 10)
        p = random()
        source, target = sample(range(n), 2)
        color_map = ["blue" for _ in range(n)]
        color_map[source] = "green"
        color_map[target] = "red"
        G = get_random_connected_graph(n, p, 15)
        layout = nx.spring_layout(G, k=10)
        nx.draw(G, layout, with_labels=True, node_color=color_map)
        labels = {e: G.edges[e]["weight"] for e in G.edges}
        nx.draw_networkx_edge_labels(G, layout, edge_labels=labels)
        print("-" * 30)
        print(f"Configuration {it + 1}")
        print(f"Vertex count: {n}")
        print(f"Vertex s: {source}")
        print(f"Vertex t: {target}")
        print(f"Optimal KM count from s to t is: {dijkstra(G, source)[target]}")
        plt.show()


if __name__ == "__main__":
    main()
