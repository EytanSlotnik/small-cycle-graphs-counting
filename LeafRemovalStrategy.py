import networkx as nx
import numpy as np
from numpy import e

from Chain import Chain
from Strategy import Strategy


class LeafRemovalStrategy(Strategy):
    def step(self, chain: Chain):
        chain.g.find_weight()
        if chain.g.weight > chain.d * (len(chain.g.nodes()) - 1):
            return

        leaves = chain.g.find_leaves()
        if len(leaves) == 0:
            return
        v = chain.random.choice(leaves)
        u = list(chain.g.neighbors(v))[0]

        chain.g.find_g0_distance()
        distance_normalizer = sum(chain.g.distance_from_g0.values()) - 2
        try:  # TODO generalize to non uniform strategy distribution
            a = e ** chain.beta
            a /= chain.g.distance_from_g0[u] * len(leaves)
            a *= distance_normalizer
        except OverflowError:
            a = 1

        if chain.random.random() > a:
            return

        chain.g.remove_node(v)

        # nx.relabel_nodes(chain.g, {u: i for i, u in enumerate(chain.g.nodes())}, copy=False)

        chain.g.g0 = None
        chain.g.distance_from_g0 = None
        chain.g.path_beginning = None
        chain.g.leaves = None
