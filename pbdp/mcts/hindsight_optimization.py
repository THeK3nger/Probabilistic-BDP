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
        global_profile_data = {'expanded': 0}
        for i in range(limit):
            roll = HindsightOptimization.rollout(map_abstraction, beliefs_model)
            hpath, cost, profile_data = hpa_high_level(roll, start, end, distance_euclidean)
            path = Path((hpath, cost))
            global_profile_data['expanded'] += profile_data['expanded']
            if path.is_empty():
                continue
            policy.add_path(path)
        return policy, global_profile_data

    @staticmethod
    def rollout(map_abstraction, beliefs_model):
        map_copy = copy.deepcopy(map_abstraction)
        for edge in map_copy.edges:
            if edge in beliefs_model and random.random() > beliefs_model[edge]:
                map_copy.close_edge(edge)
        return map_copy
