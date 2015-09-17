__author__ = 'davide'

from heapq import heappush, heappop


def astar(searchable, start, goal, heuristic, config=None):
    """ Performs A* over a searchable object.

    A searchable object is an object who exposes two methods:

        * `cost(start,end)`     : A function who returns the cost of moving between adjacent states, from start to end.
        * `neighbours(state)`   : A function who returns the adjacent states of `state`.

    PARAMS:
        * `searchable`  : A searchable data structure.
        * `start`       : The starting state.
        * `goal`        : The goal state.
        * `heuristic`   : An heuristic function between any state and the goal.
        * `config`      : A configuration dictionary.
    """

    config = {} if config is None else config
    path_only = config['path_only'] if 'path_only' in config else False
    profile = config['profile'] if 'profile' in config else False

    def _reconstruct(c, s, closed):
        """
           Reconstruct backwards path from current to start by following parent links.
        """
        p = [c]
        while not c == s:
            c = closed[c][3]  # TODO: Change with position enum.
            p.append(c)
        return list(reversed(p))

    profile_data = {'expanded': 0}

    if start == goal:
        return return_path(path_only, profile, profile_data, [start])

    openlist = []
    closedlist = {}    # dictionary of expanded nodes - key=coord, data = node

    # node = (f, g, coord, parent)  and start node has g=0 and f = h and no parent
    heappush(openlist, (heuristic(start, goal), 0, start, None))
    # print(openlist)
    while len(openlist) != 0:
        # pop best node from open list (lowest f)
        node = heappop(openlist)
        current_f, current_g, current, parent = node
        if current in closedlist or current_g == float('inf'):
            continue  # node has to be ignored: blocked or already visited

        # add node to closelist
        closedlist[current] = node

        # goal reached?
        if current == goal:
            # Rewind to find the final path!
            return return_path(path_only,profile,profile_data,_reconstruct(current, start, closedlist), current_f)

        if profile:
            profile_data['expanded'] += 1

        # expand current node by getting all successors and adding them to open list
        adjacents = searchable.neighbours(current)
        for a in adjacents:
            adjg = current_g + searchable.cost(a, current)
            adjf = adjg + heuristic(a, goal)
            adjnode = (adjf, adjg, a, current)
            if a in closedlist:
                if adjf < closedlist[a][0]:  # TODO: Change with F position enum.
                    # in case of inconsistent heuristic:
                    # if we've found a cheaper path, put updated node back on openlist
                    del(closedlist[a])
                    heappush(openlist, adjnode)
            else:
                heappush(openlist, adjnode)

    return return_path(path_only, profile, profile_data, [])


def return_path(path_only, profile, profile_data, path, cost=0):
    if path_only:
        return path
    elif profile:
        return path, cost, profile_data  # 0 steps, empty self.path
    else:
        return path, cost
