__author__ = 'davide'

import copy

from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.search.hpa import hpa_high_level
from pbdp.model.path import Path
from pbdp.model.policy import Policy

class OptimisticPolicy(object):

    @staticmethod
    def search_path(start, end, map_abstraction, beliefs_model, threshold):
        pruned = OptimisticPolicy.prune_map(map_abstraction, beliefs_model, threshold)
        hpath, cost, profile_data = hpa_high_level(pruned, start, end, distance_euclidean)
        path = Path((hpath, cost))
        p = Policy()
        p.add_path(path)
        return p

    @staticmethod
    def prune_map(map_abstraction, beliefs_model, threshold):
        map_copy = copy.deepcopy(map_abstraction)
        for edge in map_copy.abstraction_graph.edges:
            if edge in beliefs_model and beliefs_model[edge] < threshold:
                old_label = map_copy.abstraction_graph.get_edge_label(edge)
                old_label["cost"] = float('inf')
                map_copy.abstraction_graph.update_edge_label(edge, old_label)
        return map_copy



