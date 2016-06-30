import sys

import yoshix.run_yoshi

import pbdp.benchmark as benchmark
from pbdp.model.hierarchical_map import HierarchicalMap
from pbdp.model.agents.beliefs import AgentBeliefsModel
from pbdp.mcts.optimistic_policy import OptimisticPolicy
from pbdp.model.agents.agent import VirtualAgent


def main(args=None):
    """The main routine."""
    if args is None:
        args = sys.argv[1:]

    yoshix.run_yoshi.main(["./pbdp/experiments"])

if __name__ == '__main__':
    # Load All Maps in Folder
    main()
