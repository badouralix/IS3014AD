#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Add parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cfgraph.utils import get_assignments, get_decisions, get_distances

class Tester():

    def __init__(self, cfg):
        self.assignments = get_assignments(cfg)
        self.decisions = get_decisions(cfg)
        self.distances = get_distances(cfg)

    def test_assignments(self, run_result):
        return self.assignments.difference(set(run_result))

    def test_decisions(self, run_result):
        return self.decisions.difference(set(run_result))

    def test_distance(self, run_result, k):
        k_nodes = set(node for node, distance in self.distances.items() if distance <= k)
        return k_nodes.difference(set(run_result))

