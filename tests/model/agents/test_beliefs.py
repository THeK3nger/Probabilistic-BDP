from unittest import TestCase

__author__ = 'davide'

from pbdp.model.agents.beliefs import AgentBeliefsModel

class TestAgentBeliefModel(TestCase):

    def test_create(self):
        beliefs = AgentBeliefsModel()

    def test_update(self):
        beliefs = AgentBeliefsModel()
        beliefs.update((1,2),0.5)
        beliefs.update((2,2),0.4)
        beliefs.update((1,2),0.3)
        self.assertEqual(beliefs[1,2],0.3)
        self.assertEqual(beliefs[2,2],0.4)
        self.assertRaises(ValueError,beliefs.update,(1,2),1.5)

    def test_decay(self):
        beliefs = AgentBeliefsModel()
        beliefs.update((1,2),0.5)
        beliefs.update((2,2),0.3)
        beliefs.update((3,3),0.9)
        beliefs.decay()
        self.assertEqual(beliefs[1,2],0.5)
        self.assertLess(beliefs[3,3],0.9)
        self.assertGreater(beliefs[2,2],0.3)
