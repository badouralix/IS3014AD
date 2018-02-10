#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from cfgraph.utils import get_assignments, get_decisions, gen_k_paths, gen_i_loops, get_all_du_paths
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
            print(f"Path {path} is unfeasible")
        else:
            tests.append(test)

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
            print(f"Path {path} is unfeasible")
        else:
            tests.append(test)

    print(f"Feasibility of {len(tests) / counter * 100:.2f}%")

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_tdef(cfg):
    tests = list()

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_tu(cfg):
    tests = list()

    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


@timeit
def gen_tdu(cfg):
    paths = get_all_du_paths(cfg)
    tests = list()

    for simple_path in paths:
        for prefixpath in gen_i_loops(cfg, i=1, start="START", end=simple_path[0]):
            path = prefixpath + simple_path[1:]
            test = generate_test(cfg, path)
            if not test is None:
                tests.append(test)
                break
        else:
            print(f"Simple path {simple_path} is unfeasible")

    print(f"Feasibility of {len(tests) / len(paths) * 100:.2f}%")


    tests = [dict(item) for item in set(tuple(test.items()) for test in tests)]
    print(f"Generated test : {tests}")


if __name__ == "__main__":
    from cfgraph.utils import gen_k_paths
    from syntax.parser import parser
    from utils.ast2cfg import ast2cfg

    input_dir = "input"
    filename = "example3.imp"
    with open(f"{input_dir}/{filename}") as f:
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
