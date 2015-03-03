"""
Collection of algorithms to generate a graph abstraction over a LogicalMap.
"""

import math

from pbdp.model.map import LogicalMap
from pbdp.model.vector2d import Vec2d
from pbdp.search import astar


class UniformAbstraction(object):
    def __init__(self, original_map, fraction):
        """

        :param original_map: A reference to the original map.
        :type original_map: LogicalMap
        :param fraction: How big the grid abstraction will be (between 0 and 1 as a percentage of map's width.
        :type fraction: float
        :return: A searchable abstraction.
        """
        self.original_map = original_map
        self.gridsize = math.ceil(original_map.width * fraction)
        self.width = math.ceil(original_map.width / self.gridsize)
        self.height = math.ceil(original_map.height / self.gridsize)
        self.regions_map = [[0 for _ in range(original_map.width)] for _ in range(original_map.height)]

    def generate(self):
        # 1. Identify Sectors (sectors are set of tiles in the abstract grid).

        # 2. Identify Regions (regions are fully connected set of tiles in a sector).
        for s in range(self.width*self.height):
            self._identify_region(s)

        # 3. Identify edges between Regions.
        self._pretty_print()

    def _pretty_print(self):
        print('\n'.join([''.join(map(lambda x: str(x), row)) for row in self.regions_map]))

    def _sector_from_tile(self, tile):
        """
        :param tile:
        :type tile: Vec2d
        :return:
        """
        return math.floor(tile.y / self.gridsize) + self.width * math.floor(tile.x / self.gridsize)

    def _sector_to_rect(self, sector):
        sector_row = math.floor(sector / self.width)
        sector_col = sector % self.width
        first_row = sector_row * self.gridsize
        first_col = sector_col * self.gridsize
        last_row = min(first_row + self.gridsize, self.original_map.height)
        last_col = min(first_col + self.gridsize, self.original_map.width)
        return ((first_row, first_col), (last_row, last_col))

    def _tiles_in_sector(self, sector):
        rect = self._sector_to_rect(sector)
        first_row, first_col = rect[0]
        last_row, last_col = rect[1]
        return [(r, c) for r in range(first_row, last_row)
                for c in range(first_col, last_col)]

    def _is_in_sector(self, tile, sector):
        r, c = tile
        rect = self._sector_to_rect(sector)
        first_row, first_col = rect[0]
        last_row, last_col = rect[1]
        return first_row <= r < last_row and first_col <= c < last_col

    def _identify_region(self, sector):
        label_eq = UnionFind()
        nextLabel = 1

        # First Pass
        for tile in self._tiles_in_sector(sector):
            r, c = tile

            if self.original_map.is_traversable(tile):

                neighs = [(r - 1, c), (r, c - 1)]
                neighs = [n for n in neighs if self._is_in_sector(n, sector) and self.original_map.is_traversable(n)]

                if len(neighs) == 0:
                    self.regions_map[r][c] = nextLabel
                    label_eq.union(nextLabel)
                    nextLabel += 1
                else:
                    labels = [self.regions_map[n[0]][n[1]] for n in neighs]
                    self.regions_map[r][c] = min(labels)
                    for l in labels:
                        label_eq.union(l, min(labels))

        # Second Pass
        for tile in self._tiles_in_sector(sector):
            r, c = tile
            if self.original_map.is_traversable(tile):
                self.regions_map[r][c] = label_eq[self.regions_map[r][c]]

###########

"""UnionFind.py

Union-find data structure. Based on Josiah Carlson's code,
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/215912
with significant additional changes by D. Eppstein.
"""


class UnionFind:
    """Union-find data structure.

    Each unionFind instance X maintains a family of disjoint sets of
    hashable objects, supporting the following two methods:

    - X[item] returns a name for the set containing the given item.
      Each set is named by an arbitrarily-chosen one of its members; as
      long as the set remains unchanged it will keep the same name. If
      the item is not yet part of a set in X, a new singleton set is
      created for it.

    - X.union(item1, item2, ...) merges the sets containing each item
      into a single larger set.  If any item is not yet part of a set
      in X, it is added to X as one of the members of the merged set.
    """

    def __init__(self):
        """Create a new empty union-find structure."""
        self.weights = {}
        self.parents = {}

    def __getitem__(self, object):
        """Find and return the name of the set containing the object."""

        # check for previously unknown object
        if object not in self.parents:
            self.parents[object] = object
            self.weights[object] = 1
            return object

        # find path of objects leading to the root
        path = [object]
        root = self.parents[object]
        while root != path[-1]:
            path.append(root)
            root = self.parents[root]

        # compress the path and return
        for ancestor in path:
            self.parents[ancestor] = root
        return root

    def __iter__(self):
        """Iterate through all items ever found or unioned by this structure."""
        return iter(self.parents)

    def union(self, *objects):
        """Find the sets containing the objects and merge them all."""
        roots = [self[x] for x in objects]
        heaviest = max([(self.weights[r], r) for r in roots])[1]
        for r in roots:
            if r != heaviest:
                self.weights[heaviest] += self.weights[r]
                self.parents[r] = heaviest