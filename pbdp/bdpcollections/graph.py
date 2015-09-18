__author__ = 'davide'

import itertools

class Graph(object):
    """
    The Graph class represents a generic undirected labeled graph.
    """

    def __init__(self):
        self.graph = {}
        self.vertex_labels = {}
        self.edge_labels = {}

    @property
    def vertices(self):
        """
        :return: Returns the list of vertices in the graph.
        """
        return (x for x in self.graph.keys())

    @property
    def edges(self):
        """
        :return: Returns the list of edges in the graph.
        """
        return ((x, y) for x in self.vertices for y in self.vertices if y in self.graph[x])

    def add_node(self, node, meta=None):
        """
        Add a node to the graph.
        :param node: The node element.
        :param meta: The optional meta-information for the node.
        """
        if node not in self.graph.keys():
            self.graph[node] = set([])
        if meta is not None:
            self.vertex_labels[node] = meta

    def update_node_label(self, node, meta):
        """
        Update the node meta-information. It does nothing if the node does not exist.
        :param node: The target node.
        :param meta: The new meta-information object.
        """
        if node in self.vertices:
            self.vertex_labels[node] = meta

    def add_edge(self, first, second, meta=None):
        """
        Add an edge between two nodes. If the nodes do not exist, the function adds them.
        :param first: The first node.
        :param second: The second node.
        :param meta: The optional meta-information for the edge.
        """
        if first not in self.vertices:
            self.add_node(first)
        if second not in self.vertices:
            self.add_node(second)
        self.graph[first].add(second)
        self.graph[second].add(first)
        if meta is not None:
            self.edge_labels[(first, second)] = meta

    def update_edge_label(self, edge, meta):
        """
        Update the edge meta-information object. It does nothing if the edge does not exist.
        :param edge: The target edge.
        :param meta: The new meta-information object.
        """
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
        :param node: The target node.
        :return: The list of vertices adjacent to the target node.
        """
        return self.graph[node]

    def is_adjacent(self, node_a, node_b):
        return (node_a, node_b) in self.edges

    def __getitem__(self, item):
        return self.neighbours(item)

    def __contains__(self, item):
        return item in self.graph.keys()

class ExtendedGraph(object):
    """
    Extended Graph is a graph with some nodes (and edges added) it is used to extend
    a graph with more nodes without generate a full new graph.
    """

    def __init__(self,original_graph):
        """
        Create a new Extended Graph using an existing Graph.
        :param original_graph: The original Graph.
        """
        self._original_graph = original_graph
        self.extension = {}
        self.ext_edge_labels = {}

    @property
    def ext_vertices(self):
        return (x for x in self.extension.keys())

    @property
    def vertices(self):
        """
        :return: Returns the list of vertices in the graph.
        """
        return itertools.chain(self.ext_vertices, self._original_graph.vertices)

    @property
    def ext_edges(self):
        swap = lambda t: (t[1], t[0])
        edges = ((x, y) for x in self.ext_vertices for y in self.extension[x])
        return itertools.chain(edges, (swap(x) for x in edges))

    @property
    def edges(self):
        """
        :return: Returns the list of edges in the graph.
        """
        return itertools.chain(self._original_graph.edges, self.ext_edges)

    @property
    def boundary_vertices(self):
        """
        This are the vertex that are in the original graph BUT are adjacent with the extended one.
        :return:
        """
        b_vertex = set()
        for nodes in self.extension.values():
            b_vertex = b_vertex.union(nodes)
        return b_vertex

    def add_extended_node(self,new_node, adjacent_nodes, labels=None):
        """
        Add a note to the extension.
        :param new_node: A new node. This node must not be included in the original graph.
        :param adjacent_nodes: A list of adjacent nodes.
        """
        if new_node not in self._original_graph:
            # TODO: Check if ALL adjacent vertex are in the original graph.
            self.extension[new_node] = adjacent_nodes
            if labels is not None:
                for i in range(len(adjacent_nodes)):
                    self.ext_edge_labels[(new_node,adjacent_nodes[i])] = labels[i]

    def get_edge_label(self, edge):
        swap = lambda t: (t[1], t[0])
        if edge in self.ext_edge_labels.keys():
            return self.ext_edge_labels[edge]
        if swap(edge) in self.ext_edge_labels.keys():
            return self.ext_edge_labels[swap(edge)]
        return self._original_graph.get_edge_label(edge)

    def neighbours(self, node):
        if node in self.ext_vertices:
            return self.extension[node]
        original_neighbours = self._original_graph.neighbours(node)
        if node in self.boundary_vertices:
            extended_adjacent = set([x for x in self.ext_vertices if node in self.extension[x]])
            return extended_adjacent.union(original_neighbours)
        else:
            return original_neighbours
