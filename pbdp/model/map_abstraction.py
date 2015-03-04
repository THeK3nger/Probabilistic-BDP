"""
Collection of algorithms to generate a graph abstraction over a LogicalMap.
"""

import math
import collections
import random

from pbdp.model.map import LogicalMap
from pbdp.model.vector2d import Vec2d
from pbdp.search import astar

# Node = a tile.

class Edge(object):
    """
    Graph Edge
    """

    def __init__(self, node_a, node_b, metadata):
        self.pair = (node_a, node_b)
        self.metadata = metadata

    def __eq__(self, other):
        return self.pair == other.pair

    def __hash__(self):
        return hash(self.pair)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "E({},{})".format(self.pair[0], self.pair[1])

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
        self.id_to_tile = {}
        self.edges = set([])

    def generate(self):
        # 1. Identify Sectors (sectors are set of tiles in the abstract grid).

        # 2. Identify Regions (regions are fully connected set of tiles in a sector).
        for s in self.sectors():
            self._identify_region(s)

        # 2.1 For each region in sector add a node.
        self._register_regions()

        # 3. Identify edges between Regions.
        self._find_edges()

        print(self.edges)

        # Test Print
        self._pretty_print()

    def sectors(self):
        for s in range(self.width*self.height):
            yield s

    def _find_edges(self):
        # 3.1 Connect Vertical Edges
        for column_raw in range(1, self.width - 1):
            col = column_raw * self.gridsize - 1
            for row in range(self.original_map.height):
                if self.regions_map[row][col + 1] == 0 or self.regions_map[row][col] == 0:
                    continue
                t1 = self.id_to_tile[self._id_from_tile((row, col + 1))]
                t2 = self.id_to_tile[self._id_from_tile((row, col))]
                self.edges.add(Edge(t1, t2, None))

        # 3.1 Connect Horizontal Edges
        for row_raw in range(1, self.height - 1):
            row = row_raw * self.gridsize - 1
            for col in range(self.original_map.width):
                if self.regions_map[row][col] == 0 or self.regions_map[row + 1][col] == 0:
                    continue
                t1 = self.id_to_tile[self._id_from_tile((row + 1, col))]
                t2 = self.id_to_tile[self._id_from_tile((row, col))]
                self.edges.add(Edge(t1, t2, None))

    def _get_region(self, tile):
        return self.regions_map[tile[0]][tile[1]]

    def _register_regions(self):
        for s in self.sectors():
            labels_in_sector = set([self._get_region(t) for t in self._tiles_in_sector(s)])
            # Remove 0 if present.
            if 0 in labels_in_sector:
                labels_in_sector.remove(0)
            while len(labels_in_sector) != 0:
                label = labels_in_sector.pop()
                # Take a random tile with label.
                tile = random.choice([t for t in self._tiles_in_sector(s) if self._get_region(t) == label])
                self.id_to_tile[self._id_from_tile(tile)] = tile

    def _pretty_print(self):
        print('\n'.join([''.join(map(lambda x: str(x), row)) for row in self.regions_map]))

    def _sector_from_tile(self, tile):
        """
        :param tile:
        :type tile: Vec2d
        :return:
        """
        if not isinstance(tile, Vec2d):
            tile = Vec2d(tile)
        return math.floor(tile.y / self.gridsize) + self.width * math.floor(tile.x / self.gridsize)

    def _id_from_tile(self, tile):
        sector = self._sector_from_tile(tile)
        return "{}-{}".format(sector, self._get_region(tile))

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
                    labels = [self._get_region(n) for n in neighs]
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