#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from queue import Queue
from astree.bexp import BConstant, BExp
from astree.com import CAssign
from collections import defaultdict, deque
import networkx as nx
from itertools import chain
import copy

###############################################################################

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
            if not dest in result:
                reached_nodes.put(dest)
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


def get_nested_cwhile(cfg):
    """
    Build a dict {cwhile node: [cwhile nodes nested in body]}
    """
    result = defaultdict(set)
    visited = set()

    def rec_nested_cwhile(current_node, body_ancestors):
        if current_node in visited:
            return

        visited.add(current_node)

        if "type" in cfg.nodes[current_node] and cfg.nodes[current_node]["type"] == "CWHILE":
            for body_ancestor in body_ancestors:
                result[body_ancestor].add(current_node)
            successors = list(cfg.successors(current_node))
            # The following relies on the internal structure of the cfg, namely
            # the body of a while statement is the first successor.
            # TODO: need to be independent from this kind of knowledge
            rec_nested_cwhile(successors[0], body_ancestors + [current_node])
            rec_nested_cwhile(successors[1], body_ancestors)
        else:
            for succ in cfg.successors(current_node):
                rec_nested_cwhile(succ, body_ancestors)

    rec_nested_cwhile("START", [])

    return result

###############################################################################

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


def get_k_paths(cfg, k):
    """
    Generator for valid paths from START to END, of length less than k.
    Implement a depth-first search.

    WARNING: an oracle is needed to throw away unfeasible paths.

    Arguments:
        cfg -- Control flow graph of the input program
        k   -- Max length for relevant paths
    """
    assert(k >= 0)

    next_nodes = deque() # next_nodes is a stack of tuples (node, distance of node from START)
    next_nodes.append( ("START", 0) )

    # Holding current valid path
    current_path = list()

    while next_nodes:
        node, node_k = next_nodes.pop()
        current_path = current_path[:node_k] + [node]

        if current_path[-1] == "END":
            yield current_path
        elif node_k + 1 <= k:
            successors = list(cfg.successors(node))
            if "type" in cfg.nodes[node] and cfg.nodes[node]["type"] == "CIF":
                successors.reverse()
            for succ in successors:
                next_nodes.append( (succ, node_k + 1) )


def get_i_loops(cfg, i):
    """
    Generator for valid paths from START to END, with at most i loop executions.
    Implement a depth-first search.

    WARNING: an oracle is needed to throw away unfeasible paths.

    Arguments:
        cfg -- Control flow graph of the input program
        i   -- Max number of iterations for each loop
    """
    assert(i >= 0)

    state = defaultdict(int)        # Counter for cwhile nodes (may it reach i, prevent the loop body to be executed)

    nested_cwhile = get_nested_cwhile(cfg)

    current_path = list()

    next_nodes = deque()            # Stack (node, node_position in valid path, current state when node added to stack)
    next_nodes.append( ("START", 0, state) )

    while next_nodes:
        node, node_position, state = next_nodes.pop()
        current_path = current_path[:node_position] + [node]

        if current_path[-1] == "END":
            yield current_path

        else:
            successors = list(cfg.successors(node))

            if "type" in cfg.nodes[node]:

                if cfg.nodes[node]["type"] == "CIF":
                    successors.reverse()

                elif cfg.nodes[node]["type"] == "CWHILE":
                    # print("successors before", successors)
                    # The following relies on the internal structure of the cfg, namely
                    # the body of a while statement is the first successor.
                    # TODO: need to be independent from this kind of knowledge

                    if state[node] < i:
                        state[node] = state[node] + 1
                    else:
                        successors = successors[1:]

            # Update state
            new_state = state.copy()
            # Reset counters for inner loops
            for cwhile in nested_cwhile[node]:
                new_state[cwhile] = 0

            # Provision next_nodes stack
            for succ in successors:
                next_nodes.append( (succ, node_position + 1, new_state) )
