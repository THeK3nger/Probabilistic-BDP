"""
Contains the algorithm for the map decomposition.
"""

import math
import itertools

from pbdp.bdpcollections.graph import Graph, ExtendedGraph
from pbdp.model.map import LogicalMap, distance_euclidean


class HierarchicalMap(object):
    ENTRANCE_POSITION = 0
    ENTRANCE_CLUSTERS = 1

    def __init__(self, original_map, div_amount):
        """
        Constructor
        :param original_map:
        :type original_map LogicalMap
        :param div_amount:
        :return:
        """
        self.original_map = original_map
        self.vertical_entrances = []  # List of tuples -> ( (node1,node2), (cluster1, cluster2) )
        self.horizontal_entrances = []
        self.cluster_size = int(math.ceil(original_map.width * div_amount))
        self.abstraction_graph = Graph()

    @property
    def cluster_width(self):
        return int(math.ceil(self.original_map.width / float(self.cluster_size)))

    @property
    def cluster_height(self):
        return int(math.ceil(self.original_map.height / float(self.cluster_size)))

    def is_traversable(self, start, end):
        """
        Check if it is possible to move from start to end.

        start and end MUST be adjacent and with a finite cost!
        :param start:
        :param end:
        :return:
        """
        return self.abstraction_graph.is_adjacent(start, end) and \
               self.abstraction_graph.get_edge_label((start, end))["cost"] < float('inf')

    ## ABSTRACTION GENERATION ##

    def generate_abstract_graph(self):
        # Find Entrances
        self.__search_for_entrances()

        # Add connection between entrance nodes of different clusters.
        self.__connect_inter_nodes()

        # Add connection between entrance nodes of the same cluster.
        self.__connect_intra_nodes()

    def get_all_in_cluster(self, cluster):
        """
        Return all the entrance nodes in the given cluster
        :param cluster:
        :return:
        """
        return [x[self.ENTRANCE_POSITION][0] for x in self.vertical_entrances if
                cluster == x[self.ENTRANCE_CLUSTERS][0]] + \
               [x[self.ENTRANCE_POSITION][1] for x in self.vertical_entrances if
                cluster == x[self.ENTRANCE_CLUSTERS][1]] + \
               [x[self.ENTRANCE_POSITION][0] for x in self.horizontal_entrances if
                cluster == x[self.ENTRANCE_CLUSTERS][0]] + \
               [x[self.ENTRANCE_POSITION][1] for x in self.horizontal_entrances if
                cluster == x[self.ENTRANCE_CLUSTERS][1]]

    def get_tile_cluster(self, coord):
        """
        Get the cluster in which the tile is.
        :param coord:
        :return:
        """
        r, c = coord
        return int(r / self.cluster_size), int(c / self.cluster_size)

    def find_vertical_entrances(self, first, second):
        """
        Cluster are expressed as (i,j) where i is the row and j is the column.
        :param first:
        :type first (Int, Int)
        :param second:
        :type second (Int, Int)
        :return:
        """
        if first[1] == second[1] - 1:  # first is before second
            cluster_col = second[1] * self.cluster_size - 1
        else:
            cluster_col = first[1] * self.cluster_size - 1
        cluster_row_start = first[0] * self.cluster_size
        cluster_row_end = min(self.original_map.height - 1,  (first[0] + 1) * self.cluster_size)
        cluster_row_current = cluster_row_start

        def booth_free_test():
            return self.__booth_free((cluster_row_current, cluster_col), (cluster_row_current, cluster_col + 1))

        while cluster_row_current < cluster_row_end:
            while not booth_free_test() and cluster_row_current < cluster_row_end:
                cluster_row_current += 1

            if cluster_row_current >= cluster_row_end:
                break

            node_row_entrance = cluster_row_current
            while booth_free_test() and cluster_row_current < cluster_row_end:
                cluster_row_current += 1
            node_row_exit = cluster_row_current
            middle_row_node = int((node_row_exit + node_row_entrance) / 2)
            self.vertical_entrances.append((((middle_row_node, cluster_col), (middle_row_node, cluster_col + 1)), (first, second)))

    def find_horizontal_entrances(self, first, second):
        """
        Cluster are expressed as (i,j) where i is the row and j is the column.
        :param first:
        :param second:
        :return:
        """
        if first[0] == second[0] - 1:  # ClusterA is before ClusterB
            cluster_row = second[0] * self.cluster_size - 1
        else:
            cluster_row = first[0] * self.cluster_size - 1
        cluster_col_start = first[1] * self.cluster_size
        cluster_col_end = min(self.original_map.width - 1, (first[1] + 1) * self.cluster_size)
        cluster_col_current = cluster_col_start

        while cluster_col_current < cluster_col_end:
            while not self.__booth_free((cluster_row, cluster_col_current), (cluster_row + 1, cluster_col_current)) and cluster_col_current < cluster_col_end:
                cluster_col_current += 1

            if cluster_col_current >= cluster_col_end:
                return

            node_col_start = cluster_col_current
            while self.__booth_free((cluster_row, cluster_col_current), (cluster_row + 1, cluster_col_current)) and cluster_col_current < cluster_col_end:
                cluster_col_current += 1
            node_col_exit = cluster_col_current
            middle_node = int((node_col_exit + node_col_start) / 2)
            self.horizontal_entrances.append((((cluster_row, middle_node), (cluster_row + 1, middle_node)), (first, second)))

    def __booth_free(self, left_tile, right_tile):
        # Assume all the keys = all doors open.
        return self.original_map.is_traversable(left_tile) and \
               self.original_map.is_traversable(right_tile)

    def __connect_inter_nodes(self):
        for e in self.vertical_entrances:
            self.abstraction_graph.add_edge(e[0][0], e[0][1], meta={"type": "inter", "cost": 1})
        for e in self.horizontal_entrances:
            self.abstraction_graph.add_edge(e[0][0], e[0][1], meta={"type": "inter", "cost": 1})

    def __connect_intra_nodes(self):
        for i in range(0, self.cluster_height):
            for j in range(0, self.cluster_width):
                for e in itertools.combinations(self.get_all_in_cluster((i, j)), 2):
                    cost = distance_euclidean(e[0], e[1])
                    if cost is not None:
                        self.abstraction_graph.add_edge(e[0], e[1], meta={"type": "intra", "cost": cost})

    def __search_for_entrances(self):
        for i in range(0, self.cluster_height):
            for j in range(0, self.cluster_width - 1):
                self.find_vertical_entrances((i, j), (i, j + 1))
        for i in range(0, self.cluster_height - 1):
            for j in range(0, self.cluster_width):
                self.find_horizontal_entrances((i, j), (i + 1, j))


class ExtendedAbstraction(object):
    """
    This is a persistent abstraction used to represent an extended Hierarchical Map with two more
    nodes (namely, start and destination). It is used to perform HPA on the abstraction without performing side-effect
    on the original abstraction.

    The ExtendedAbstraction is searchable as well.
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
        self.start_cluster = self.original_abstraction.get_tile_cluster(start)
        self.end = end
        self.end_cluster = self.original_abstraction.get_tile_cluster(end)
        start_connection = self.original_abstraction.get_all_in_cluster(self.start_cluster)
        start_labels = [{"type": "intra", "cost": distance_euclidean(start, x)} for x in start_connection]
        end_connection = self.original_abstraction.get_all_in_cluster(self.end_cluster)
        end_labels = [{"type": "intra", "cost": distance_euclidean(end, x)} for x in end_connection]
        self.extended_graph = ExtendedGraph(abstraction.abstraction_graph)
        self.extended_graph.add_extended_node(start, start_connection, start_labels)
        self.extended_graph.add_extended_node(end, end_connection, end_labels)

    def neighbours(self, node):
        all_neighbours = self.extended_graph.neighbours(node)
        return [x for x in all_neighbours
                if self.extended_graph.get_edge_label((node,x))["cost"] != float('inf')]

    def cost(self, first, second):
        c = self.extended_graph.get_edge_label((first, second))
        return c["cost"] if c is not None else float('inf')

    def _is_node(self, node):
        return node in self.extended_graph.vertices
