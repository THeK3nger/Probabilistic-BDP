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
        for edge in self.base.abstraction_graph.edge_labels.keys():
            label = self.base.abstraction_graph.edge_labels[edge]
            if label["type"] == 'inter':
                self.beliefs.update(edge, 0.4)

    def test_optimistic_search(self):
        path = OptimisticPolicy.search_path((5,5), (40,40), self.base, self.beliefs, 0.1)
        self.assertTrue(path.length > 0)
        path = OptimisticPolicy.search_path((5,5), (40,40), self.base, self.beliefs, 0.5)
        self.assertTrue(path.length == 0)