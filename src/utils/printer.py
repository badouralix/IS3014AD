#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from anytree import RenderTree
from networkx import nx
import os
import pygraphviz
import time

def timeit(method):
    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print(f"{method.__name__} took {(te - ts) * 1000:.2f}ms")
        return result

    return timed


def print_ast(ast):
    print(RenderTree(ast))


def print_cfg(cfg):
    print(nx.drawing.nx_pydot.to_pydot(cfg))


def write_cfg(cfg, filename, layout="dot"):
    path = "output/" + os.path.splitext(filename)[0] + f".{layout}.png"
    graph = nx.drawing.nx_agraph.to_agraph(cfg)
    graph.layout(layout)
    graph.draw(path)
