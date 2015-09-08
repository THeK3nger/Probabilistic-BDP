import model.map

import pbdp.benchmark as benchmark
from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.agents.beliefs import AgentBeliefsModel
from pbdp.mcts.optimistic_policy import OptimisticPolicy

def run_optimistic_policy_benchmark(maps, threshold):
    if not isinstance(threshold, (list, tuple)):
        threshold = [threshold]
    for m in maps.values():
        map_abstraction = HierarchicalMap(m, 0.2)
        map_abstraction.generate_abstract_graph()
        for t in threshold:
            # Find a random real map (open or close randomly connections).
            print("Randomize Map")
            copymap = benchmark.randomize_map(map_abstraction)
            # Extract a random feasible path in the map (High-Level Only).
            print("Find START and END")
            start, end = benchmark.random_path(m, copymap)
            # Start with an empty belief model (everything is 0.5).
            print("Initial Beliefs")
            beliefs = AgentBeliefsModel()
            beliefs.initialize(map_abstraction)
            # Reach the destination. (High-Level Simulation).
            print("OptimisticPolicy Run")
            OptimisticPolicy.search_path(start, end, map_abstraction, beliefs, t)
            # SAVE BENCHMARK DATA IN A CSV FILE

if __name__ == '__main__':
    # Load All Maps in Folder
    run_optimistic_policy_benchmark(benchmark.maps_loader(), [0.2,0.3,0.4])