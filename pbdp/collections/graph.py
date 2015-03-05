__author__ = 'davide'


class MultiGraph(object):
    """
    Represent an undirected multigraph.

    In a multigraph pair of nodes can be connected by multiple edges.
    """

    def __init__(self):
        self.vertices = set([])
        self.edges = set([])  # (node, node, metadata)
        self.vertex_labels = {}
        self.edge_labels = {}

    def add_node(self, node, meta=None):
        self.vertices.add(node)
        if meta is not None:
            self.vertex_labels[node] = meta

    def update_node_label(self, node, meta):
        if node in self.vertices:
            self.vertex_labels[node] = meta

    def add_edge(self, first, second, id=None, meta=None):
        if first not in self.vertices:
            self.add_node(first)
        if second not in self.vertices:
            self.add_node(second)
        if id is None:
            id = hash((first, second))
        self.edges.add((id, (first, second)))
        if meta is not None:
            self.edge_labels[(id, (first, second))] = meta

    def update_edge_label(self, edge, meta):
        if edge in self.edges:
            self.edge_labels[edge] = meta

    def get_vertex_label(self, node):
        if node in self.vertices:
            return self.vertex_labels[node]

    def get_edge_label(self, edge):
        if edge in self.edges:
            return self.edge_labels[edge]

    def neighbours(self, node):
        """
        Return all the vertices coming out from "node".
        :param node:
        :return:
        """
        return set([n for n in self.edges if n[1][0] == node or n[1][1] == node])

    def __getitem__(self, item):
        return self.neighbours(item)

    def __contains__(self, item):
        return item in self.vertices
