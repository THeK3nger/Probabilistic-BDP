import sys

import yoshix.run_yoshi

import pbdp.benchmark as benchmark
from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.agents.beliefs import AgentBeliefsModel
from pbdp.mcts.optimistic_policy import OptimisticPolicy
from pbdp.model.agents.agent import VirtualAgent


def run_optimistic_policy_benchmark(maps, threshold):
    if not isinstance(threshold, (list, tuple)):
        threshold = [threshold]
    policy_function = lambda x, y, z, w: OptimisticPolicy.search_path(x, y, z, w, 0.2)
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
            # Initialize a Virtual Agent:
            # Start with an empty belief model (everything is 0.5).
            print("Initial Beliefs")
            virtual_agent = VirtualAgent(copymap, start, end, policy_function)
            while not virtual_agent.satisfied and False:  # TODO: DEACTIVATED UNTIL AGENT IS COMPLETED
                virtual_agent.execute_step()
            print(virtual_agent.profile_data)
            # SAVE BENCHMARK DATA IN A CSV FILE

def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    yoshix.run_yoshi.main(["./pbdp/experiments"])
    #run_optimistic_policy_benchmark(benchmark.maps_loader(), [0.2, 0.3, 0.4])

if __name__ == '__main__':
    # Load All Maps in Folder
    main()
