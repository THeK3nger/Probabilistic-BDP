__author__ = 'davide'

import copy


class AgentBeliefsModel(object):
    """
    The AgentBeliefsModel is a datastructure to represent beliefs information over an HAG
    of the map.

    The data structure store a numerical value for each edge in the HAG representing the
    degree of belief that that edge is traversable.

    If an edge is not present in the ABM it is assumed that the edge is open and immutable
    (assuming that we check for edges that we know exists in the HAG).
    """

    def __init__(self):
        self._beliefs = {}  # Map from edge to a real number.
        self._decay_speed = 0.5  # For now, decay speed is the same for every edge.

    def initialize(self, map_abstraction, initial_value=0.5):
        """
        Initialize beliefs on the "inter" edges of a map abstraction.
        :param map_abstraction:
        :return:
        """
        for edge in map_abstraction.abstraction_graph.edge_labels.keys():
            label = map_abstraction.abstraction_graph.edge_labels[edge]
            if label["type"] == 'inter':
                self.update(edge, initial_value)

    def update(self, edge, value):
        """
        Update a particular edge with a new value for the belief degree.
        :param edge: The target edge.
        :param value: A value from 0.0 to 1.0 indicating the degree of belief that the
                      edge is traversable.
        :return: self
        """
        if 0.0 < value < 1.0:
            self._beliefs[edge] = value
        else:
            raise ValueError("Value is not a valid degree of belief. Must be in [0,1] interval.")
        return self

    def decay(self):
        """
        Execute a decay step. All degrees are pushed toward 0.5 by a small amount.
        """
        for edge in self._beliefs.keys():
            current = self._beliefs[edge]
            if isinstance(self._decay_speed, (int, float)):
                self._beliefs[edge] = current + self._decay_speed * (0.5 - current)
        return self

    def decayed(self):
        """
        Return a new instance with a decayed belief state.
        :return:
        """
        return self.clone().decay()

    def clone(self):
        """
        Create a deep copy of the current ABM instance.
        :return:
        """
        res = AgentBeliefsModel()
        res._beliefs = copy.deepcopy(self._beliefs)
        res._decay_speed = copy.deepcopy(self._decay_speed)
        return res

    def __getitem__(self, item):
        return self._beliefs[item]

    def __contains__(self, item):
        return item in self._beliefs.keys()