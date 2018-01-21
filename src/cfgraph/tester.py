#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from cfgraph.utils import *
from collections import Counter
import copy

class Tester():
    # TODO: Avoid checking non-reachable paths (e.g. if False ...)

    def __init__(self, cfg):
        self.cfg = cfg
        self.assignments = get_assignments(cfg)
        self.decisions = get_decisions(cfg)
        self.distances = get_distances(cfg)
        self.loop = get_loop(cfg)
        self.all_defs = get_all_def(cfg)
        self.usages = get_all_direct_usages(cfg)

    def test_assignments(self, paths):
        assignments = self.assignments.copy()
        for path in paths:
            assignments = assignments.difference(set(path))
        return assignments

    def test_decisions(self, paths):
        decisions = self.decisions.copy()
        for path in paths:
            decisions = decisions.difference(set(path))
        return decisions

    def test_distance(self, paths, k):
        k_nodes = set(node for node, distance in self.distances.items() if distance <= k)
        for path in paths:
            k_nodes = k_nodes.difference(set(path))
        return k_nodes

    def test_k_path(self, paths, k):
        pass

    def test_i_loop(self, paths, i):
        """[summary]

        Arguments:
            run_result -- counter {node: int} for the test run
            i          -- max loop iteration

        Returns:
            result -- dict {node: {"status", "nb_iteration"}}
        """

        loops = self.loop.copy()
        for path in paths:
            # Number of the loop iterations is equal to the number of time the
            # CWHILE loop node is reached minus 1 (final bexp is evaluated to
            # false, thus breaking the loop).
            # TODO: this test is not sound on nested while loop
            # TODO: this is most probably wrong. We should check that for each loop there are paths
            # in which the loop is made 1, 2, .. i times
            agg_path = Counter(path)
            for loop_node in loops:
                if agg_path[loop_node] <= i:
                    loops.discard(loop_node)

        return loops

    def test_definitions(self, paths):
        """
        Each variable definition must be followed by an usage of this var, with no def
        in between.
        :param run_result:
        :return:
        """
        all_defs = copy.deepcopy(self.all_defs)

        for path in paths:
            for var in all_defs.keys():
                path_defs = [def_node for def_node in all_defs[var] if def_node in path]
                for def_node in path_defs:
                    def_node_pos = path.index(def_node)
                    for following_node in path[def_node_pos+1:]:
                        if var in get_def(self.cfg, following_node):
                            break
                        if var in get_ref(self.cfg, following_node):
                            all_defs[var].remove(def_node)
                            break

        return all_defs

    def test_utilisations(self, paths):

        usages = copy.deepcopy(self.usages)

        for path in paths:
            for var in usages.keys():
                path_defs = [def_node for def_node in usages[var].keys() if def_node in path]
                for def_node in path_defs:
                    def_node_pos = path.index(def_node)
                    for following_node in path[def_node_pos+1:]:
                        if var in get_def(self.cfg, following_node):
                            break
                        if var in get_ref(self.cfg, following_node):
                            usages[var][def_node].discard(following_node)
                            break
        for var in usages.keys():
            usages[var] = {def_node: ref_nodes for def_node, ref_nodes in usages[var].items() if len(ref_nodes) != 0}
        usages = {var:usages for var, usages in usages.items() if len(usages) != 0}

        return usages
