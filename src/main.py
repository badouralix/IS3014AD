#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

from astree.aexp import *
from astree.bexp import *
from astree.com import *
from cfgraph.runners import run_test, reachable_nodes
from cfgraph.tester import Tester


def main():
    cfg = nx.DiGraph()

    cfg.add_node("START")
    for i in range(1,6):
        cfg.add_node(i)
    cfg.add_node("END")

    cfg.nodes[1]["typename"] = "CIF"
    cfg.nodes[4]["typename"] = "CIF"

    cfg.add_edge("START", 1, bexp=BConstant(True), com=CSkip())
    cfg.add_edge(1, 2, bexp=BBinOp('<=', AVariable('X'), AConstant(0)), com=CSkip())
    cfg.add_edge(1, 3, bexp=BUnOp('!', BBinOp('<=', AVariable('X'), AConstant(0))), com=CSkip())
    cfg.add_edge(2, 4, bexp=BConstant(True), com=CAssign(AVariable('X'), AUnOp('-', AVariable('X'))))
    cfg.add_edge(3, 4, bexp=BConstant(True), com=CAssign(AVariable('X'), ABinOp('-', AConstant(1), AVariable('X'))))
    cfg.add_edge(4, 5, bexp=BBinOp('==', AVariable('X'), AConstant(1)), com=CSkip())
    cfg.add_edge(4, 6, bexp=BUnOp('!', BBinOp('==', AVariable('X'), AConstant(1))), com=CSkip())
    cfg.add_edge(5, "END", bexp=BConstant(True), com=CAssign(AVariable('X'), AConstant(1)))
    cfg.add_edge(6, "END", bexp=BConstant(True), com=CAssign(AVariable('X'), ABinOp('+', AVariable('X'), AConstant(1))))

    # nx.draw(cfg, with_labels=True, font_weight='bold')
    # plt.show()

    # print(run_test(cfg, {'X': -1}))

    tester = Tester(cfg)
    print(tester.test_assignments(reachable_nodes(run_test(cfg, {'X': 0})[0])))
    print(tester.test_decisions(reachable_nodes(run_test(cfg, {'X': 0})[0])))
    print(tester.test_distance(reachable_nodes(run_test(cfg, {'X': 0})[0]), k=3))
    print(tester.test_i_loop(reachable_nodes(run_test(cfg, {'X': 0})[0]), i=2))

if __name__ == "__main__":
    main()
