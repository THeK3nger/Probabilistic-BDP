__author__ = 'davide'


class Graph(object):
    """
    Represent an undirected graph.
    """

    def __init__(self):
        self.graph = {}
        self.vertex_labels = {}
        self.edge_labels = {}

    @property
    def vertices(self):
        return self.graph.keys()

    @property
    def edges(self):
        return [(x, y) for x in self.vertices for y in self.vertices if y in self.graph[x]]

    def add_node(self, node, meta=None):
        if node not in self.graph.keys():
            self.graph[node] = set([])
        if meta is not None:
            self.vertex_labels[node] = meta

    def update_node_label(self, node, meta):
        if node in self.vertices:
            self.vertex_labels[node] = meta

    def add_edge(self, first, second, meta=None):
        if first not in self.vertices:
            self.add_node(first)
        if second not in self.vertices:
            self.add_node(second)
        self.graph[first].add(second)
        self.graph[second].add(first)
        if meta is not None:
            self.edge_labels[(first, second)] = meta

    def update_edge_label(self, edge, meta):
        if edge in self.edges:
            self.edge_labels[edge] = meta

    def get_vertex_label(self, node):
        if node in self.vertices:
            return self.vertex_labels[node]

    def get_edge_label(self, edge):
        if edge in self.edges:
            swap = lambda t: (t[1], t[0])
            if edge in self.edge_labels.keys():
                return self.edge_labels[edge]
            if swap(edge) in self.edge_labels.keys():
                return self.edge_labels[swap(edge)]

    def neighbours(self, node):
        """
        Return all the vertices coming out from "node".
        :param node:
        :return:
        """
        return self.graph[node]

    def __getitem__(self, item):
        return self.neighbours(item)

    def __contains__(self, item):
        return item in self.graph.keys()
