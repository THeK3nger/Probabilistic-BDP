from unittest import TestCase

from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.model.agents.beliefs import AgentBeliefsModel
from pbdp.mcts.optimistic_policy import OptimisticPolicy

class TestOptimisticPolicy(TestCase):

    def setUp(self):
        self.base = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.base.generate_abstract_graph()
        self.beliefs = AgentBeliefsModel()
        self.beliefs.initialize(self.base, 0.4)

    def test_optimistic_search(self):
        # TODO: UPDATE ACCORDING RECENT CHANGES IN POLICY
        path, profile_data = OptimisticPolicy.search_path((5,5), (40, 40), self.base, self.beliefs, 0.1)
        self.assertFalse(path.is_empty())
        path, profile_data = OptimisticPolicy.search_path((5,5), (40, 40), self.base, self.beliefs, 0.5)
        self.assertTrue(path.is_empty())