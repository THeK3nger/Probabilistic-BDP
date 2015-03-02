__author__ = 'davide'

import math

from pbdp.model.vector2d import Vec2d


class LogicalMap(object):
    def __init__(self, map_path):
        def read_map(_map_path):
            """
            Internal. Generates matrix. Initialises info and populates costs.
            Called from init. Sets matrix to None if map load fails.
            Differentiates between uniform and non-uniform cost based on length
            map header.

            :type _map_path String
            """
            info = {}
            with open(_map_path, "r") as f:
                print("Parsing...")
                for line in f:
                    if line.strip() == 'map':
                        break
                    parsed = line.split()
                    key, value = parsed[0], parsed[1]
                    info[key] = value
                info["map"] = [list(line.rstrip()) for line in f]
                return info

        map_parsed = read_map(map_path)

        self.height = int(map_parsed["height"])
        self.width = int(map_parsed["width"])
        self.matrix = map_parsed["map"]

    def cost(self, start, end):
        """
        Returns the cost of the terrain type at coord, read from costs dictionary.
        If previous supplied, return val based on relative locations to prohibit corner-cutting

        :type start Vec2d
        :type end Vec2d
        """

        if self.is_traversable(start) and self.is_traversable(end):
            if start.is_diagonal_to(end):
                # diagonal move - need to check corner cutting
                delta = end - start

                # check corner cutting
                if self.is_traversable(start + (delta.x, 0)) and self.is_traversable(start + (0, delta.y)):
                    return 1 * math.sqrt(2)
            else:
                return 1
        return float('inf')

    def __getitem__(self, item):
        if isinstance(item, Vec2d):
            r = item.x
            c = item.y
        else:
            r, c = item
        return self.matrix[r][c]

    def enumerate(self):
        for r in range(self.height):
            for c in range(self.width):
                yield (self.matrix[r][c], (r, c))

    def is_traversable(self, tile):
        return self[tile] in "."


def distance_euclidean(start, end):
    """Compute euclidean distance between two points."""
    return (start - end).magnitude


def distance_manhattan(start, end):
    """Internal. Called as getH() WHEN HEURISTIC set to 'manhattan'"""
    return math.fabs((start[0] - end[0]) + (start[1] - end[1]))
