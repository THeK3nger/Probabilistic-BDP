from yoshix import YoshiExperiment
from yoshix.exporter import YoshiEggCSVExporter

import pbdp.benchmark as benchmark

class OptimisticPolicyBaseExperiment(YoshiExperiment):

    def setup(self):
        self.setup_egg(("Map", "Start", "End", "ExpandedNodes"))
        self.assign_generators("Map", benchmark.maps_loader().items())
        self.assign_generators("Start", range(1, 10))
        self.assign_generators("End", range(1,4))
        self.assign_transformer("Map", lambda x: x[0])

    def single_run(self, params):
        print("Single Run {}".format(self.run_counter))
        print(params["Map"][1].width)
        self.partial_egg["ExpandedNodes"] = 3.45

    def after_run(self):
        YoshiEggCSVExporter(self.egg, "badresults.csv").export()
