#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

from cfgraph.runners import run_test_set, reachable_nodes
from cfgraph.utils import *
from syntax.parser import parser
from tests.tester import Tester
from utils.ast2cfg import ast2cfg
from utils.printer import print_ast, print_cfg


def main():
    source_filename = "input/simple_while.imp"
    source_file = open(source_filename)
    source_code = source_file.read()

    # print(source_code)

    ast = parser.parse(source_code)
    print_ast(ast)

    print()

    cfg = ast2cfg(ast)
    print_cfg(cfg)

    # print()

    # print(get_ordered_cwhile(cfg))

    # print()

    # for path in get_i_loops(cfg, i=2):
    #     print(path)

    # pos = nx.spring_layout(cfg)
    # nx.draw_networkx(cfg, pos=pos)
    # nx.draw_networkx_edge_labels(cfg, pos=pos, font_size=4)
    # limits = plt.axis("off")
    # plt.show()

    # print(run_test(cfg, {'X': -1}))

    # print("== Running tests ==")
    # tester = Tester(cfg)
    # print("= Testing assignements =")
    # print(tester.test_assignments(run_test(cfg, {'x': 0})[0]))
    # print("= Testing decisions =")
    # print(tester.test_decisions(run_test(cfg, {'x': 0})[0]))
    # print("= Testing i-loop (i=2) =")
    # print(tester.test_i_loop(run_test(cfg, {'x': 0})[0], i=2))
    # print("= Testing definitions =")
    # print(tester.test_definitions(run_test(cfg, {'x': 0})[0]))

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


if __name__ == "__main__":
    main()
