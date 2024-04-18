import networkx as nx
import numpy as np

from Chain import Chain
from Graph import Graph
from Strategy import Strategy


class FlipEdgeStrategy(Strategy):
    def step(self, chain: Chain):
        if chain.g.find_path_beginning() is None:
            return

        w = chain.g.find_weight()
        path_size = len(chain.g.nodes()) - len(chain.g.find_g0().nodes())

        r = max(0, np.ceil((w - (chain.d * len(chain.g.find_g0().nodes()))) / chain.d))
        e = path_size - r
        if e == 0:
            return


        u = chain.random.choice(list(chain.g.nodes()), 2, replace=False)
        u, v = u[0], u[1]
        new_g = Graph()
        new_g.add_edges_from(chain.g.edges())
        if (u, v) in new_g.edges():
            new_g.remove_edge(u, v)
            if not nx.is_connected(new_g):
                return
        else:
            if chain.g.degree(u) == chain.d or chain.g.degree(v) == chain.d:
                return
            if chain.g.degree(u) == 1 or chain.g.degree(v) == 1:
                return
            new_g.add_edge(u, v)
        p = new_g.find_path_beginning()
        if p is None:
            return
        new_g0 = new_g.find_g0()
        new_g = Graph(path_beginning=p)
        new_g.add_edges_from(new_g0.edges(), g0=new_g0)
        new_g.add_nodes_from(new_g0.nodes())
        new_w = new_g.find_weight()
        new_r = max(0, np.ceil((new_w - (chain.d * len(new_g0.nodes()))) / chain.d))
        node = p
        new_node = max(new_g.nodes()) + 1
        for _ in range(int(new_r) + int(e)):
            new_g.add_edge(node, new_node)
            node = new_node
            new_node += 1

        try:
            a = e ** (chain.beta * (len(chain.g.nodes()) - len(new_g.nodes())))
            a *= len(chain.g.nodes()) * (len(chain.g.nodes()) - 1)
            a /= len(new_g.nodes()) * (len(new_g.nodes()) - 1)
        except OverflowError:
            a = 1

        if chain.random.random() > a:
            return
        chain.g = new_g
