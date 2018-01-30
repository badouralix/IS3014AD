#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from astree.bexp import BConstant, BExp
from astree.com import CAssign
from collections import defaultdict
import networkx as nx
from itertools import chain
import copy

def get_assignments(cfg):
    """
    Returns the set of all the labels of assignment instructions.

    Arguments:
        cfg -- control flow graph of the input program

    Returns:
        result -- set of labels
    """

    result = set()

    for src, dest in cfg.edges:
        edge = cfg.edges[src, dest]
        if isinstance(edge['com'], CAssign):
            result.add(src)

    return result


def get_decisions(cfg):
    """
    Returns the set of labels whose instructions are in a conditional branch
    (if statement or while statement).

    TODO: currently, only the node following the branching is added to the
          result set. Adding all the nodes in the branch may be "sounder".

    Arguments:
        cfg -- control flow graph of the input program

    Returns:
        result -- set of labels
    """

    result = set()

    for src, dest in cfg.edges:
        edge = cfg.edges[src, dest]
        if not isinstance(edge['bexp'], BConstant):
            result.add(dest)

    return result


def get_distances(cfg):
    """
    Compute for each node the distance from the start node to it.
    Basically a breath first traversing of the graph.

    Arguments:
        cfg -- control flow graph of the input program

    Returns:
        result -- a dictionnary {node: distance to the start node}
    """

    reached_nodes = Queue()
    reached_nodes.put("START")

    result = {"START": 0}

    while not reached_nodes.empty():
        src = reached_nodes.get(block=False)
        for dest in cfg.successors(src):
            reached_nodes.put(dest)
            if not dest in result:
                result[dest] = result[src] + 1

    return result

def get_loop(cfg):
    result = set()

    for node, data in cfg.nodes().data():
        try:
            if data["type"] == "CWHILE":
                result.add(node)
        except:
            pass

    return result

def get_def(cfg, node):
    result = set()
    leaving_edges = cfg.out_edges(node, data=True)
    for edge in leaving_edges:
        if isinstance(edge[2]["com"], CAssign):
            result = result.union(edge[2]["com"].assigned_var)

    return result

def get_ref(cfg, node):
    result = set()
    leaving_edges = cfg.out_edges(node, data=True)
    for edge in leaving_edges:
        result = result.union(edge[2]["bexp"].vars)
        result = result.union(edge[2]["com"].vars)
    return result


def get_all_def(cfg):
    result = defaultdict(set)
    for node in cfg.nodes:
        for var in get_def(cfg, node):
            result[var].add(node)
    return result


def get_all_ref(cfg):
    result = defaultdict(set)
    for node in cfg.nodes:
        for var in get_ref(cfg, node):
            result[var].add(node)
    return result


def get_all_usages(cfg):
    result = defaultdict(dict)
    for var, def_nodes in get_all_def(cfg).items():
        for def_node in def_nodes:
            paths = list(nx.all_simple_paths(cfg, def_node, "END"))
            direct_usages = set()
            # Remove paths containing a def before a ref
            for path in paths:
                for node in path[1:]:
                    if var in get_def(cfg, node):
                        break
                    if var in get_ref(cfg, node):
                        direct_usages.add(node)
                        break
            result[var][def_node] = direct_usages.copy()

    return result

def get_all_du_paths(cfg):
    result = list()
    for var, def_nodes in get_all_def(cfg).items():
        for def_node in def_nodes:
            paths = list(nx.all_simple_paths(cfg, def_node, "END"))
            direct_usages = list()
            # Remove paths containing a def before a ref
            for path in paths:
                for idx, node in enumerate(path[1:]):
                    if var in get_def(cfg, node):
                        break
                    if var in get_ref(cfg, node):
                        if path[:idx+2] not in result:
                            result.append(path[:idx+2])
                        break

    return result
