#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfgraph.utils import get_assignments, get_decisions, get_distances, get_loop

class Tester():

    def __init__(self, cfg):
        self.assignments = get_assignments(cfg)
        self.decisions = get_decisions(cfg)
        self.distances = get_distances(cfg)
        self.loop = get_loop(cfg)

    def test_assignments(self, run_result):
        return self.assignments.difference(set(run_result))

    def test_decisions(self, run_result):
        return self.decisions.difference(set(run_result))

    def test_distance(self, run_result, k):
        k_nodes = set(node for node, distance in self.distances.items() if distance <= k)
        return k_nodes.difference(set(run_result))

    def test_k_path(self, run_result, k):
        pass

    def test_i_loop(self, run_result, i):
        """[summary]

        Arguments:
            run_result -- counter {node: int} for the test run
            i          -- max loop iteration

        Returns:
            result -- dict {node: {"status", "nb_iteration"}}
        """

        result = dict()

        for node in self.loop:
            # Number of the loop iterations is equal to the number of time the
            # CWHILE loop node is reached minus 1 (final bexp is evaluated to
            # false, thus breaking the loop).
            # TODO: this test is not sound on nested while loop
            result[node] = {"nb_iteration": run_result[node] - 1}
            if run_result[node] > i:
                result[node]["status"] = "failed"
            else:
                result[node]["status"] = "ok"

        return result
