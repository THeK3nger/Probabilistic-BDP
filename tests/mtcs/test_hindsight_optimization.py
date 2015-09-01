from unittest import TestCase

from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.map import LogicalMap, distance_euclidean
from pbdp.model.agents.beliefs import AgentBeliefsModel
from pbdp.mcts.hindsight_optimization import HindsightOptimization

class TestHindsightOptimization(TestCase):

    def setUp(self):
        self.base = HierarchicalMap(LogicalMap("./maps/arena.map"), 0.2)
        self.base.generate_abstract_graph()
        self.beliefs = AgentBeliefsModel()
        for edge in self.base.abstraction_graph.edge_labels.keys():
            label = self.base.abstraction_graph.edge_labels[edge]
            if label["type"] == 'inter':
                self.beliefs.update(edge, 0.7)

    def test_hindsight_search(self):
        policy = HindsightOptimization.search_path((5,5), (40,40), self.base, self.beliefs, 50)
        print(policy)