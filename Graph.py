import networkx as nx


class Graph(nx.Graph):
    def __init__(self, g: nx.Graph = None, weight=None, path_beginning=None, distance_from_g0=None, leaves=None,
                 g0=None):
        super().__init__()
        if g is not None:
            self.add_edges_from(g.edges())
            self.add_nodes_from(g.nodes())
        self.g0 = g0
        self.leaves = leaves
        self.distance_from_g0 = distance_from_g0
        self.path_beginning = path_beginning
        self.weight = weight

    def find_g0(self):
        if self.g0 is not None:
            return self.g0
        if len(self.nodes()) == 1:
            self.g0 = nx.Graph(self)
            return self.g0
        # make a copy
        G0 = nx.Graph(self.edges())
        good_bridges = []
        bad_bridges = []

        bridges = list(nx.bridges(G0))
        # find bridges
        for e in bridges:
            c = [cc for cc in nx.connected_components(G0) if ((e[0] in cc) and (e[1] in cc))][0]
            subg0 = G0.subgraph(c).copy()
            subg0.remove_edges_from([e])
            for cc in nx.connected_components(subg0):
                if nx.is_tree(subg0.subgraph(cc)):
                    bad_bridges.append(e)
                    break
                else:
                    good_bridges.append(e)

        g0 = nx.Graph(self.edges())
        g0.remove_edges_from(bad_bridges)
        # remove all isolated nodes
        g0.remove_nodes_from(list(nx.isolates(g0)))
        if len(g0.nodes()) == 0:
            g0.add_node(min(self.nodes()))
        self.g0 = g0
        return g0

    def find_g0_distance(self):
        if self.g0 is None:
            self.find_g0()

        if len(self.g0.nodes()) == 0:
            return {v: 1 for v in self.nodes()}

        def relationships(u, v):
            return (u in self.g0.nodes()) and (v in self.g0.nodes())

        GqG0 = nx.quotient_graph(self, relationships)

        # make g0 the root
        sp = nx.single_source_shortest_path(GqG0, frozenset(self.g0.nodes()))
        distances = {}
        for v in sp.keys():
            for vv in v:
                distances[vv] = len(sp[v])
        self.distance_from_g0 = distances
        return distances

    def find_leaves(self):
        if self.leaves is None:
            self.leaves = [v for v in self.nodes() if self.degree(v) == 1]
        return self.leaves

    def find_path_beginning(self):
        if self.g0 is None:
            self.find_g0()
        if self.nodes == self.g0.nodes:
            return None
        if self.path_beginning is not None:
            return self.path_beginning
        if self.distance_from_g0 is None:
            self.find_g0_distance()
        if sorted(self.find_g0_distance().values()) != \
                [1 for i in range(len(self.g0.nodes()))] + \
                [i + 2 for i in range(len(self.nodes()) - len(self.g0.nodes()))]:
            return None
        v = [v for v in self.g0.nodes() if
             len([u for u in self.neighbors(v) if self.distance_from_g0[u] == 2]) == 1][0]

        self.path_beginning = v
        return v

    def find_weight(self):
        if self.weight is None:
            self.weight = sum([len(c) for c in nx.minimum_cycle_basis(self)])
        return self.weight
