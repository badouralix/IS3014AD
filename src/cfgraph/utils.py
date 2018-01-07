#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Add parentdir to import path
import os, sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))

from queue import Queue
from astree.com import *


def get_assignments(cfg):
    result = set()

    for src, dest in cfg.edges:
        edge = cfg.edges[src, dest]
        if isinstance(edge['com'], CAssign):
            result.add(src)

    return result

# def get_k(cfg):
#     reached_nodes = Queue()
#     reached_nodes.put("START")

#     result = set()

#     while not reached_nodes.empty():
#         node = reached_nodes.get(block=False)

