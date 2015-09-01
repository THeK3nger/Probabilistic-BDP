__author__ = 'davide'

import copy
import random

from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.search.hpa import hpa_high_level
from pbdp.model.path import Path
from pbdp.model.policy import Policy

class HindsightOptimization(object):
    """
    This class implement the Hindsight Optimization over the HAG according the
    Agent's Beliefs Model.
    """

    @staticmethod
    def search_path(start, end, map_abstraction, beliefs_model, limit):
        policy = Policy()
        for i in range(limit):
            roll = HindsightOptimization.rollout(map_abstraction, beliefs_model)
            path = Path(hpa_high_level(roll, start, end, distance_euclidean))
            if path.is_empty():
                continue
            policy.add_path(path)
        return policy

    @staticmethod
    def rollout(map_abstraction, beliefs_model):
        map_copy = copy.deepcopy(map_abstraction)
        for edge in map_copy.abstraction_graph.edges:
            if edge in beliefs_model and random.random() > beliefs_model[edge]:
                old_label = map_copy.abstraction_graph.get_edge_label(edge)
                old_label["cost"] = float('inf')
                map_copy.abstraction_graph.update_edge_label(edge, old_label)
        return map_copy
