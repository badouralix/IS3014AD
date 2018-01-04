#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt


def main():
    cfg = nx.DiGraph()

    for i in range(1,6):
        cfg.add_node(i)
    cfg.add_node('_')

    cfg.add_edge(1, 2)
    cfg.add_edge(1, 3)
    cfg.add_edge(2, 4)
    cfg.add_edge(3, 4)
    cfg.add_edge(4, 5)
    cfg.add_edge(4, 6)
    cfg.add_edge(5, '_')
    cfg.add_edge(6, '_')

    nx.draw(cfg, with_labels=True, font_weight='bold')
    plt.show()


if __name__ == "__main__":
    main()
