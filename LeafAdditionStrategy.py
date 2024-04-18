import numpy as np
from numpy import e

from Chain import Chain
from Strategy import Strategy


class LeafAdditionStrategy(Strategy):
    def step(self, chain: Chain):
        distances = chain.g.find_g0_distance()
        distances_normalizer = sum(distances.values())

        v = chain.random.choice(list(chain.g.nodes()), p=[distances[v] / distances_normalizer for v in chain.g.nodes()])
        if chain.g.degree(v) == chain.d:
            return

        try:  # TODO generalize to non uniform strategy distribution
            a = e ** (-chain.beta)
            a *= distances_normalizer
            in_g0 = v in chain.g.find_g0().nodes()
            if in_g0:
                a /= distances[v] * (len(chain.g.find_leaves()) + 1)
            else:
                a /= distances[v] * len(chain.g.find_leaves())
        except OverflowError:
            a = 1

        if chain.random.random() > a:
            return

        chain.g.add_edge(v, max(chain.g.nodes())+1)

        chain.g.g0 = None
        chain.g.distance_from_g0 = None
        chain.g.path_beginning = None
        chain.g.leaves = None
