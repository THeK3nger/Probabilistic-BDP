from pbdp.model.policy import Policy, PolicyValidityException
from pbdp.model.hierarchical_map import ExtendedAbstraction, HierarchicalMap
from pbdp.model.agents.beliefs import AgentBeliefsModel

class VirtualAgent(object):
    """
    A VirtualAgent is a simulation of a real NPC moving in the map. It took a policy
    and start executing it in the map. However, only high-level navigation and sensing
    are emulated by the class!

    version 1.0
    """

    def __init__(self, map_abstraction, starting_position, target, policy_function):
        self.position = starting_position
        self.map = map_abstraction
        self.map_extension = ExtendedAbstraction(map_abstraction, starting_position, target)
        self.target = target
        self.policy = None
        self.beliefs = AgentBeliefsModel()
        self.beliefs.initialize(map_abstraction)
        # policy_function is a function who takes the following parameters:
        # start, end, map_abstraction, beliefs_model
        self.policy_function = policy_function

    def set_target(self, target):
        if target != self.target:
            self.map_extension = ExtendedAbstraction(self.map, self.position, target)
            self.target = target

    def satisfied(self):
        return self.position == self.target

    def policy_is_valid(self):
        """
        Check if the policy is valid in the current state.

        A policy is valid if policy current point is the agent current position.
        :return:
        """
        return self.policy is not None and self.policy.is_valid(self.position)

    def compute_next_actions(self):
        """
        Returns a list of all the possible actions described by the policy
        sorted by scores.
        :return:
        """
        if not self.policy_is_valid():
            self.policy = self.policy_function(self.position, self.target, self.map, self.beliefs)
        scores = [(p, self.policy.next_action_score(p))
                  for p in self.map_extension.neighbours(self.position)]
        return sorted(scores, key=lambda x: x[1])

    def action_is_executable(self, action):
        """
        An action is action_is_executable if and only if is not None and can be executed.
        :return:
        """
        return action is not None and self.map.is_traversable(self.position, action)

    def execute_step(self):
        """
        Execute ONE step on the HIGH-LEVEL based on the current policy.
        :return:
        """
        # Find best action.
        next = self.compute_next_actions()



