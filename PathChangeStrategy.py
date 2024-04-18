import networkx as nx
import numpy as np

from Graph import Graph
from Strategy import Strategy


class PathChangeStrategy(Strategy):
    def step(self, chain):
        path_beginning = chain.g.find_path_beginning()
        if path_beginning is None:
            return
        chain.g.find_g0()
        path_length = len(chain.g.nodes()) - len(chain.g.g0.nodes())
        new_graph = Graph(path_beginning=path_beginning, weight=chain.g.weight, g0=chain.g.g0)
        new_graph.add_nodes_from(chain.g.g0.nodes())
        new_graph.add_edges_from(chain.g.g0.edges())
        vertices_map = {v: i for i, v in enumerate(chain.g.nodes())}
        new_graph = nx.relabel_nodes(new_graph, vertices_map)

        v = chain.random.choice(new_graph)
        if new_graph.degree(v) == chain.d:
            return
        new_graph.path_beginning = v
        new_graph.add_edge(v, len(new_graph.nodes()))
        for u in range(len(new_graph.nodes()) - 1, len(new_graph.nodes()) - 2 + path_length):
            new_graph.add_edge(u, u + 1)

        chain.g = new_graph
        chain.g.g0 = None
        chain.g.distance_from_g0 = None
        chain.g.path_beginning = None
        chain.g.leaves = None

