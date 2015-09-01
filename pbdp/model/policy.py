__author__ = 'davide'

class Policy(object):

    def __init__(self):
        self._policy_table = {}

    def add_path(self, path):
        path_key = path.to_tuple()
        if path_key in self._policy_table.keys():
            count = self._policy_table[path_key]["count"] + 1
        else:
            count = 1
        self._policy_table[path_key] = {"cost": path.length, "count": count}

    def next_action_score(self, destination):
        total_rollouts = 0
        different_costs = []
        for path in self._policy_table.keys():
            if path[1] == destination:
                total_rollouts += self._policy_table[path]["count"]
                different_costs.append((self._policy_table[path]["count"], self._policy_table[path]["cost"]))
        return sum([x[0]*x[1] for x in different_costs])/total_rollouts

    def __str__(self):
        base = ""
        for item in self._policy_table.items():
            base += str(item[0]) + " || " + str(item[1]) + "\n"
        return base

