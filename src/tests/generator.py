#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cfgraph.utils import get_assignments, \
                          get_decisions, \
                          gen_k_paths, \
                          gen_i_loops, \
                          get_all_def, \
                          get_all_ref, \
                          get_all_du_paths
from tests.solver import generate_test
from utils.printer import timeit


@timeit
def gen_ta(cfg):
    assign_nodes = get_assignments(cfg)
    tests = list()

    for node in assign_nodes:
        for path in gen_i_loops(cfg, i=1, start="START", end=node):
            test = generate_test(cfg, path)
            if not test is None:
                tests.append(test)
                break
        else:
            print(f"Node {node} is unreachable")

    if assign_nodes:
        print(f"Feasibility of {len(tests) / len(assign_nodes) * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_td(cfg):
    edges = get_decisions(cfg)
    tests = list()

    for edge in edges:
        for path in gen_i_loops(cfg, i=1, start="START", end=edge[0]):
            path.append(edge[1])
            test = generate_test(cfg, path)
            if not test is None:
                tests.append(test)
                break
        else:
            print(f"Edge {edge} is unreachable")

    if edges:
        print(f"Feasibility of {len(tests) / len(edges) * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")



@timeit
def gen_ktc(cfg, k):
    tests = list()
    counter = 0

    for path in gen_k_paths(cfg, k):
        counter += 1

        test = generate_test(cfg, path)
        if test is None:
            print(f"Path {path} is infeasible")
        else:
            tests.append(test)

    if counter:
        print(f"Feasibility of {len(tests) / counter * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_itb(cfg, i):
    tests = list()
    counter = 0

    for path in gen_i_loops(cfg, i):
        counter += 1

        test = generate_test(cfg, path)
        if test is None:
            print(f"Path {path} is infeasible")
        else:
            tests.append(test)

    print(f"Feasibility of {len(tests) / counter * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_tdef(cfg):
    def_nodes = set()
    du_paths = get_all_du_paths(cfg)
    tests = list()

    for nodes in get_all_def(cfg).values():
        def_nodes.update(nodes)

    for subpath in du_paths:
        # TODO: we should avoid non simple paths there
        if subpath[0] in def_nodes:
            for prefixpath in gen_i_loops(cfg, i=1, start="START", end=subpath[0]):
                for suffixpath in gen_i_loops(cfg, i=1, start=subpath[-1], end="END"):
                    path = prefixpath + subpath[1:] + suffixpath[1:]
                    path = prefixpath + subpath[1:]
                    test = generate_test(cfg, path)
                    if not test is None:
                        tests.append(test)
                        def_nodes.remove(subpath[0])
                        break
                else:
                    continue
                break

    if def_nodes:
        print(f"No tests found for def {def_nodes}")

    if len(tests) + len(def_nodes) != 0:
        print(f"Feasibility of {len(tests) / (len(tests) + len(def_nodes)) * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_tu(cfg):
    ref_nodes = set()
    du_paths = get_all_du_paths(cfg)
    tests = list()

    for nodes in get_all_ref(cfg).values():
        ref_nodes.update(nodes)

    for subpath in du_paths:
        if subpath[-1] in ref_nodes:
            for prefixpath in gen_i_loops(cfg, i=1, start="START", end=subpath[0]):
                for suffixpath in gen_i_loops(cfg, i=1, start=subpath[-1], end="END"):
                    path = prefixpath + subpath[1:] + suffixpath[1:]
                    test = generate_test(cfg, path)
                    if not test is None:
                        tests.append(test)
                        ref_nodes.remove(subpath[-1])
                        break
                else:
                    continue
                break

    if ref_nodes:
        print(f"No tests found for ref {ref_nodes}")

    if len(tests) + len(ref_nodes) != 0:
        print(f"Feasibility of {len(tests) / (len(tests) + len(ref_nodes)) * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_tdu(cfg):
    paths = get_all_du_paths(cfg)
    tests = list()

    for subpath in paths:
        for prefixpath in gen_i_loops(cfg, i=1, start="START", end=subpath[0]):
            for suffixpath in gen_i_loops(cfg, i=1, start=subpath[-1], end="END"):
                path = prefixpath + subpath[1:] + suffixpath[1:]
                test = generate_test(cfg, path)
                if not test is None:
                    tests.append(test)
                    break
            else:
                continue
            break
        else:
            print(f"Simple path {subpath} is infeasible")

    if paths:
        print(f"Feasibility of {len(tests) / len(paths) * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


if __name__ == "__main__":
    from syntax.parser import parser
    from utils.ast2cfg import ast2cfg

    filename = sys.argv[1]
    with open(filename) as f:
        source_code = f.read()

    ast = parser.parse(source_code)
    cfg = ast2cfg(ast)

    gen_ta(cfg)
    gen_td(cfg)
    gen_ktc(cfg, 10)
    gen_itb(cfg, 1)
    gen_tdef(cfg)
    gen_tu(cfg)
    gen_tdu(cfg)
