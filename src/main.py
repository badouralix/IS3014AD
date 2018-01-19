#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

from cfgraph.runners import run_test, reachable_nodes
from cfgraph.tester import Tester
from syntax.parser import parser
from utils.ast2cfg import ast2cfg
from utils.printer import print_ast, print_cfg


def main():
    source_filename = "input/example.imp"
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

    # tester = Tester(cfg)
    # print(tester.test_assignments(reachable_nodes(run_test(cfg, {'X': 0})[0])))
    # print(tester.test_decisions(reachable_nodes(run_test(cfg, {'X': 0})[0])))
    # print(tester.test_distance(reachable_nodes(run_test(cfg, {'X': 0})[0]), k=3))
    # print(tester.test_i_loop(reachable_nodes(run_test(cfg, {'X': 0})[0]), i=2))

if __name__ == "__main__":
    main()
