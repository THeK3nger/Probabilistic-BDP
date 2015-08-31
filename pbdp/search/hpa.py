"""
Implement Hierarchical Pathfinding over a map abstraction.
"""

from pbdp.search.astar import astar
from pbdp.model.hierarchical_map import ExtendedAbstraction, HierarchicalMap
from pbdp.model.vector2d import Vec2d


def hpa(searchable, start, goal, heuristic):
    """

    :param searchable:
    :type searchable HierarchicalMap
    :param start:
    :param goal:
    :param heuristic:
    :return:
    """
    high_level = hpa_high_level(searchable, start, goal, heuristic)

    def merge_sub_path(accumulator, first, second):
        return accumulator + astar(searchable.original_map, Vec2d(first), Vec2d(second), heuristic)

    path = []
    i = 0
    while i < len(high_level)-1:
        path = merge_sub_path(path, high_level[i], high_level[i+1])
        i += 1

    print(path)
    return path

def hpa_high_level(searchable, start, goal, heuristic):
    extended = ExtendedAbstraction(searchable, start, goal)
    high_level = astar(extended, start, goal, heuristic)
    return high_level