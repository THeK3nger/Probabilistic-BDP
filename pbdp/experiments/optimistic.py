from yoshix import YoshiExperiment
from yoshix.exporter import YoshiEggCSVExporter

import pbdp.benchmark as benchmark
from pbdp.mcts.optimistic_policy import OptimisticPolicy
from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.agents.agent import VirtualAgent

class OptimisticPolicyBaseExperiment(YoshiExperiment):

    def setup(self):
        self.setup_egg(("Map", "Start", "End", "ExpandedNodes"))
        self.assign_generators("Map", benchmark.maps_loader().items())
        self.assign_generators("Start", range(1, 10))
        self.assign_generators("End", range(1,4))
        self.assign_transformer("Map", lambda x: x[0])

    def single_run(self, params):
        print("Single Run {}".format(self.run_counter))
        policy_function = lambda x, y, z, w: OptimisticPolicy.search_path(x, y, z, w, 0.2)
        map_abstraction = HierarchicalMap(params["Map"][1], 0.2)
        map_abstraction.generate_abstract_graph()
        copymap = benchmark.randomize_map(map_abstraction)
        start, end = benchmark.random_path(params["Map"][1], copymap)
        virtual_agent = VirtualAgent(copymap, start, end, policy_function)
        self.partial_egg["ExpandedNodes"] = virtual_agent.profile_data["expanded"]

    def after_run(self):
        YoshiEggCSVExporter(self.egg, "badresults.csv").export()
