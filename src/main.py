#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

from cfgraph.runners import run_test_set, reachable_nodes
from cfgraph.tester import Tester
from cfgraph.utils import *
from syntax.parser import parser
from utils.ast2cfg import ast2cfg
from utils.printer import print_ast, print_cfg


def main():
    source_filename = "input/example2.imp"
    source_file = open(source_filename)
    source_code = source_file.read()

    # print(source_code)

    ast = parser.parse(source_code)
    print_ast(ast)

    cfg = ast2cfg(ast)
    print_cfg(cfg)

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
    tester = Tester(cfg)
    print("= Testing assignements =")
    print(tester.test_assignments(run_test_set(cfg, test_set)))
    print("= Testing decisions =")
    print(tester.test_decisions(run_test_set(cfg, test_set)))
    print("= Testing i-loop (i=2) =")
    print(tester.test_i_loop(run_test_set(cfg, test_set), i=2))
    print("= Testing definitions =")
    print(tester.test_definitions(run_test_set(cfg, test_set)))
    print("= Testing usages =")
    print(tester.test_usages(run_test_set(cfg, test_set)))
    print("= Testing DU paths =")
    print(tester.test_du_paths(run_test_set(cfg, test_set)))


if __name__ == "__main__":
    main()
