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
    source_code = '0 + (1 + 2) ** 3 * 4 / 5'

    ast = parser.parse(source_code)
    print_ast(ast)

    # cfg = ast2cfg(ast)
    # print_cfg(cfg)

    # nx.draw(cfg, with_labels=True, font_weight='bold')
    # plt.show()

    # print(run_test(cfg, {'X': -1}))

    # tester = Tester(cfg)
    # print(tester.test_assignments(reachable_nodes(run_test(cfg, {'X': 0})[0])))
    # print(tester.test_decisions(reachable_nodes(run_test(cfg, {'X': 0})[0])))
    # print(tester.test_distance(reachable_nodes(run_test(cfg, {'X': 0})[0]), k=3))
    # print(tester.test_i_loop(reachable_nodes(run_test(cfg, {'X': 0})[0]), i=2))

if __name__ == "__main__":
    main()
