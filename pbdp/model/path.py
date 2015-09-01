__author__ = 'davide'

from pbdp.model.vector2d import Vec2d
from pbdp.model.map import distance_euclidean

class Path(object):
    """
    The object represent a fixed path on the map. Can be high or low level.

    It is basically a list of Vec2d... but on steroid.

    In the high-level case length is an estimation of the real length.
    """

    def __init__(self, list=None):
        if list is not None:
            self._path = list[0]
            self._length = list[1]
        else:
            self._path = []
            self._length = -1

    def append(self, item):
        if not isinstance(item,Vec2d):
            raise TypeError("Wrong Type for a path element!")
        self._path.append(Vec2d)

    def is_empty(self):
        return len(self._path) < 2

    def to_tuple(self):
        return tuple(self._path)

    @property
    def length(self):
        if self._length == -1:
            if len(self._path) < 2:
                self._length = 0
            else:
                accumulator = 0.0
                for i in range(1, len(self._path)):
                    accumulator += distance_euclidean(self._path[i-1], self._path[i])
                self._length = accumulator
        return self._length

    def __eq__(self, other):
        return self._path == other._path