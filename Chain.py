import logging
import sys

import numpy as np

from Graph import Graph


class Chain:
    def __init__(self, g: Graph, d, beta, strategies, p=None, phi=None):
        self.strategies = strategies
        self.d = d
        if p is None:
            p = [1 / len(strategies) for s in strategies]
        if phi is None:
            def size_potential(g): return len(g.g0)

            phi = size_potential
        self.p = p
        self.phi = phi
        self.g = g
        self.beta = beta
        self.random = np.random.default_rng()

    def step(self, num_steps=1, check=True):
        if check:
            if max({self.g.degree[v] for v in self.g.nodes()}) > self.d:
                logging.error(
                    f"Degree constraint violated: {max({self.g.degree[v] for v in self.g.nodes()})} > {self.d}")
                sys.exit(1)
            w = self.g.find_weight()
            if w > self.d * len(self.g.nodes()):
                logging.error(f"Weight constraint violated: {w} > {self.d * len(self.g.nodes())}")
                sys.exit(1)

        strategies = self.random.integers(len(self.strategies), size=num_steps)
        for s in strategies:
            self.strategies[s].step(self)
        return self
