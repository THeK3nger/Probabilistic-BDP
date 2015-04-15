from pbdp.model.map import LogicalMap, distance_euclidean

class ExtendedPBDPAbstraction(object):
    """
    This is a persistent abstraction used to represent an extended Hierarchical Map with two more
    nodes (namely, start and destination). It is used to perform HPA on the abstraction without performing side-effect
    on the original abstraction. It includes a modified cost version who takes into account the degree of belief
    of each gate.

    The ExtendedPBDPAbstraction is searchable as well.
    """

    def __init__(self, abstraction, start, end):
        """

        :param abstraction:
        :type abstraction HierarchicalMap
        :param start:
        :param end:
        :return:
        """
        self.original_abstraction = abstraction
        self.start = start
        self.end = end

    def neighbours(self, node):
        if not self._is_node(node):
            return []

        # Neighbours of start
        start_cluster = self.original_abstraction.get_tile_cluster(self.start)
        if node == self.start:
            return self.original_abstraction.get_all_in_cluster(start_cluster)
        # Neighbours of end
        end_cluster = self.original_abstraction.get_tile_cluster(self.end)
        if node == self.end:
            return self.original_abstraction.get_all_in_cluster(end_cluster)

        node_cluster = self.original_abstraction.get_tile_cluster(node)

        # Add start to the neighbour in the same cluster of start.
        if node_cluster == start_cluster:
            return self.original_abstraction.abstraction_graph.neighbours(node) | {self.start}
        # Add end to the neighbour in the same cluster of end.
        if node_cluster == end_cluster:
            return self.original_abstraction.abstraction_graph.neighbours(node) | {self.end}

        return self.original_abstraction.abstraction_graph.neighbours(node)

    def cost(self, first, second):
        if first not in self.neighbours(second):
            return float('inf')
        edge_label = self.original_abstraction.abstraction_graph.get_edge_label((first, second))
        if edge_label is None:
            return distance_euclidean(first, second)
        if "degree" in edge_label.keys():
            return edge_label["cost"] * (2 - edge_label["degree"])
        return edge_label["cost"]

    def _is_node(self, node):
        return node == self.start or node == self.end or node in self.original_abstraction.abstraction_graph