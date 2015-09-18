from unittest import TestCase

from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.model.agents.agent import VirtualAgent
from pbdp.mcts.optimistic_policy import OptimisticPolicy


class TestAgent(TestCase):

    def setUp(self):
        self.base = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.base.generate_abstract_graph()
        # Build a simple OptimisticPolicy function.
        self.policy_function = lambda x, y, z, w: OptimisticPolicy.search_path(x, y, z, w, 0.2)
        self.virtual_agent = VirtualAgent(self.base, (5, 5), (40, 40), self.policy_function)

    def test_set_target(self):
        self.virtual_agent.set_target((39,39))
        self.assertTrue((39, 39) == self.virtual_agent.target)

    def test_satisfied(self):
        self.assertFalse(self.virtual_agent.satisfied())
        self.virtual_agent.set_target(self.virtual_agent.position)
        self.assertTrue(self.virtual_agent.satisfied())

    def test_policy_is_valid(self):
        self.assertFalse(self.virtual_agent.policy_is_valid())

    def test_compute_next_actions(self):
        actions = self.virtual_agent.compute_next_actions()
        print(actions)  # Results validity NOT VERIFIED.

    def test_update_beliefs(self):
        self.virtual_agent.update_beliefs()
        self.assertTrue(self.virtual_agent.beliefs[((9,5), (10,5))] == 1)

    def test_execute_step(self):
        while not self.virtual_agent.execute_step():
            pass
        self.assertNotEqual(self.virtual_agent.position, self.virtual_agent.history[0])