#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from aexp import *
from bexp import *
from com import *

import networkx as nx
import matplotlib.pyplot as plt


def main():
    cfg = nx.DiGraph()

    for i in range(1,6):
        cfg.add_node(i)
    cfg.add_node('_')

    cfg.add_edge(1, 2, bexp=BBinOp('<=', AVariable('X'), AConstant(0)), com=CSkip())
    cfg.add_edge(1, 3, bexp=BUnOp('!', BBinOp('<=', AVariable('X'), AConstant(0))), com=CSkip())
    cfg.add_edge(2, 4, bexp=BConstant(True), com=CAssign(AVariable('X'), AUnOp('-', AVariable('X'))))
    cfg.add_edge(3, 4, bexp=BConstant(True), com=CAssign(AVariable('X'), ABinOp('-', AConstant(1), AVariable('X'))))
    cfg.add_edge(4, 5, bexp=BBinOp('==', AVariable('X'), AConstant(1)), com=CSkip())
    cfg.add_edge(4, 6, bexp=BUnOp('!', BBinOp('==', AVariable('X'), AConstant(1))), com=CSkip())
    cfg.add_edge(5, '_', bexp=BConstant(True), com=CAssign(AVariable('X'), AConstant(1)))
    cfg.add_edge(6, '_', bexp=BConstant(True), com=CAssign(AVariable('X'), ABinOp('+', AVariable('X'), AConstant(1))))

    nx.draw(cfg, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == "__main__":
    main()
