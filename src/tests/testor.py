#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

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
        self.usages = get_all_usages(cfg)
        self.du_paths = get_all_du_paths(cfg)

    def test_assignments(self, paths):
        assignments = self.assignments.copy()
        for path in paths:
            assignments = assignments.difference(set(path))
        return assignments


    def test_decisions(self, paths):
        decisions = self.decisions.copy()
        for path in paths:
            for i in range(len(path) - 1):
                decisions.discard((path[i], path[i+1]))
        return decisions


    def test_k_path(self, paths, k):
        missing_k_paths = list()
        for k_path in gen_k_paths(self.cfg, k):
            if not k_path in paths:
                missing_k_paths.append(k_path)
        return missing_k_paths


    def test_i_loop(self, paths, i):
        missing_i_loops = list()
        for i_loop in gen_i_loops(self.cfg, i):
            if not i_loop in paths:
                missing_i_loops.append(i_loop)
        return missing_i_loops


    def test_definitions(self, paths):
        """
        Each variable definition must be followed by an usage (ref) of this var, with no def
        in between.
        :param run_result:
        :return: dict containing var:{unused def} entries
        """

        # Dict containing var:{all nodes defining var} entries
        all_defs = copy.deepcopy(self.all_defs)

        for path in paths:
            for var in all_defs.keys():
                # Get nodes defining var in path
                path_defs = [def_node for def_node in all_defs[var] if def_node in path]
                for def_node in path_defs:
                    def_node_pos = path.index(def_node)
                    if self.next_ref_pos(path, var, def_node_pos+1) > -1:
                        all_defs[var].remove(def_node)

        # Clean result
        all_defs = {var:def_nodes for var, def_nodes in all_defs.items() if len(def_nodes) != 0}

        return all_defs


    def test_usages(self, paths):
        # TODO: Probably does'nt work on loops (or does it ?)
        usages = copy.deepcopy(self.usages)

        for path in paths:
            for var in usages.keys():
                path_defs = [def_node for def_node in usages[var].keys() if def_node in path]
                for def_node in path_defs:
                    def_node_pos = path.index(def_node)
                    ref_node_pos = self.next_ref_pos(path, var, def_node_pos+1)
                    if ref_node_pos > -1:
                        usages[var][def_node].discard(path[ref_node_pos])

        # Clean result
        for var in usages.keys():
            usages[var] = {def_node: ref_nodes for def_node, ref_nodes in usages[var].items() if len(ref_nodes) != 0}
        usages = {var:usages for var, usages in usages.items() if len(usages) != 0}

        return usages


    def test_du_paths(self, paths):
        du_paths = copy.deepcopy(self.du_paths)
        for path in paths:
            local_du_paths = copy.deepcopy(du_paths)
            for du_path in local_du_paths:
                if Tester.path_in_path(du_path, path) > -1:
                    du_paths.remove(du_path)
        return du_paths


    @staticmethod
    def path_in_path(subpath, path):
        test_path = path[:]
        while subpath[0] in test_path:
            index = test_path.index(subpath[0])
            if subpath == test_path[index:index+len(subpath)]:
                return index
            else:
                test_path = path[index+1:]
        return -1


    def next_ref_pos(self, path, var, start_pos, allow_def=False):
        for idx, node in enumerate(path[start_pos:]):
            if not allow_def and var in get_def(self.cfg, node):
                return -1
            if var in get_ref(self.cfg, node):
                return idx+start_pos
        return -1


if __name__ == "__main__":
    from cfgraph.runners import run_test_set
    from syntax.parser import parser
    from utils.ast2cfg import ast2cfg

    filename = sys.argv[1]
    with open(filename) as f:
        source_code = f.read()

    ast = parser.parse(source_code)
    cfg = ast2cfg(ast)

    test_set= [{'x': 0},
               {'x': -1},
               {'x': +1}]

    print("== Running tests ==")
    paths = run_test_set(cfg, test_set)
    tester = Tester(cfg)
    print("= Testing assignements =")
    print(tester.test_assignments(paths))
    print("= Testing decisions =")
    print(tester.test_decisions(paths))
    print("= Testing k-path (k=10) =")
    print(tester.test_k_path(paths, k=10))
    print("= Testing i-loop (i=2) =")
    print(tester.test_i_loop(paths, i=2))
    print("= Testing definitions =")
    print(tester.test_definitions(paths))
    print("= Testing usages =")
    print(tester.test_usages(paths))
    print("= Testing DU paths =")
    print(tester.test_du_paths(paths))