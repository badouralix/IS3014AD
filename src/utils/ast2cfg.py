#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import networkx as nx

from astree.bexp import *
from astree.stmt import *

def add_start_node(cfg):
    cfg.add_node("START")
    return cfg


def add_end_node(cfg):
    cfg.add_node("END")
    return cfg


def ast2cfg(ast):
    ast = copy.deepcopy(ast)
    cfg = nx.DiGraph()

    add_start_node(cfg)

    cfg, dangling_edges = recursive_ast2cfg({("START", BConstant(True), SSkip())}, ast, cfg)

    add_end_node(cfg)

    for previous_node, bexp, stmt in dangling_edges:
        cfg.add_edge(previous_node, "END", bexp=bexp, stmt=stmt)

    return cfg


def recursive_ast2cfg(previous_edges, ast, cfg):
    """
        This function does the actual conversion from ast to cfg.
        It takes some half-edges (one node + edge properties) an ast, and a cfg.
        It returns an updated cfg and some other half-edges.
        Event if each type of AST should be treated differently, there are somme common points :
        SAssign, SIf and SWhile all create a node with the label of the assign/if/while instruction.
        This part is factorized for lisibility.

        TODO: SSkip needs to be properly handled
    """

    if not isinstance(ast, SSequence):
        # If ast is assign/if/while, we can create a top-level node and link dangling edges to it
        if isinstance(ast, SWhile):
            cfg.add_node(ast.label, type="SWHILE")
        elif isinstance(ast, SIf):
            cfg.add_node(ast.label, type="SIF")
        else:
            cfg.add_node(ast.label)
        for previous_node, bexp, stmt in previous_edges:
            cfg.add_edge(previous_node, ast.label, bexp=bexp, stmt=stmt)

    if isinstance(ast, SAssign) or isinstance(ast, SInput) or isinstance(ast, SPrint):
        # Assign: simply return an half-edge with the assignment AST as stmt.
            return cfg, {(ast.label, BConstant(True), ast)}
    elif isinstance(ast, SIf):
        # If: convert "if condition true" ast, link top-level node to it with condition true,
        # then convert "if condition false" ast, link top-level node to it with ! (not) condition.
        bexp, ctrue, cfalse = ast.children
        cfg, true_branch_dangling_edges = recursive_ast2cfg(
            {
                (ast.label, bexp, SSkip())
            }, ctrue, cfg)
        if not isinstance(cfalse, SSkip):
            cfg, false_branch_dangling_edges = recursive_ast2cfg(
                {
                    (ast.label, BUnOp("!", bexp), SSkip())
                }, cfalse, cfg)
            # Gather all dangling edges leaving those newly converted cfg parts and return them
            true_branch_dangling_edges.update(false_branch_dangling_edges)
        else:
            true_branch_dangling_edges.update([(ast.label, BUnOp("!", bexp), SSkip())])
        return cfg, true_branch_dangling_edges
    elif isinstance(ast, SSequence):
        # Sequence is different : no top-level node.
        # We sequentially convert all sub-ast of sequence ast, passing dangling edges from one
        # to the next one
        # Copy previous_edges to avoid modifying it
        edges_to_transfer = copy.deepcopy(previous_edges)
        for sub_ast in list(ast.children):
            cfg, edges_to_transfer = recursive_ast2cfg(edges_to_transfer, sub_ast, cfg)
        # Return dangling edges at the end of the conversion
        return cfg, edges_to_transfer
    elif isinstance(ast, SWhile):
        # We convert the "condition true" sub ast
        bexp, ctrue = ast.children
        cfg, true_branch_dangling_edges = recursive_ast2cfg(
            {
                (ast.label, bexp, SSkip())
            }, ctrue, cfg
        )
        # And we link output dangling edges to the top level-node to actually create the loop
        for previous_node, bexp, stmt in true_branch_dangling_edges:
            cfg.add_edge(previous_node, ast.label, bexp=bexp, stmt=stmt)
        # Return an half-edge that will be followed if while condition does not apply
        return cfg, {(ast.label, BUnOp("!", ast.children[0]), SSkip())}


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from utils.printer import print_ast, print_cfg
    from astree.aexp import *
    from astree.bexp import *


    true_ast = SAssign(AVariable('X'), AConstant(2), label=3)
    false_ast = SAssign(AVariable('Y'), AConstant(4), label=4)
    if_ast = SIf(BConstant(True), true_ast, false_ast, label=2)

    assign_ast = SAssign(AVariable('Z'), AVariable('X'), label=5)
    assign_ast_bis = SAssign(AVariable('Y'), AConstant('3'), label=6)
    seq_ast = SSequence(if_ast, assign_ast, assign_ast_bis)

    while_ast=SWhile(BConstant(True), seq_ast, label=1)

    cfg = ast2cfg(while_ast)
    print_cfg(cfg)
    pos = nx.spring_layout(cfg)
    nx.draw_networkx(cfg, pos=pos)
    nx.draw_networkx_edge_labels(cfg, pos=pos, font_size=4)
    limits = plt.axis("off")
    plt.show()