#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
import networkx as nx

from astree.com import *

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

    cfg, dangling_edges = recursive_ast2cfg({("START", BConstant(True), CSkip())}, ast, cfg)

    add_end_node(cfg)

    for previous_node, bexp, com in dangling_edges:
        cfg.add_edge(previous_node, "END", bexp=bexp, com=com)

    return cfg


def recursive_ast2cfg(previous_edges, ast, cfg):
    """
        This function does the actual conversion from ast to cfg.
        It takes some half-edges (one node + edge properties) an ast, and a cfg.
        It returns an updated cfg and some other half-edges.
        Event if each type of AST should be treated differently, there are somme common points :
        CAssign, CIf and CWhile all create a node with the label of the assign/if/while instruction.
        This part is factorized for lisibility.
    """

    if not isinstance(ast, CSequence):
        # If ast is assign/if/while, we can create a top-level node and link dangling edges to it
        cfg.add_node(ast.label)
        for previous_node, bexp, com in previous_edges:
            cfg.add_edge(previous_node, ast.label, bexp=bexp, com=com)

    if isinstance(ast, CAssign):
        # Assign: simply return an half-edge with the assignment AST as com.
            return cfg, {(ast.label, BConstant(True), ast)}
    elif isinstance(ast, CIf):
        # If: convert "if condition true" ast, link top-level node to it with condition true,
        # then convert "if condition false" ast, link top-level node to it with ! (not) condition.
        bexp, ctrue, cfalse = ast.children
        cfg, true_branch_dangling_edges = recursive_ast2cfg(
            {
                (ast.label, bexp, CSkip())
            }, ctrue, cfg)
        cfg, false_branch_dangling_edges = recursive_ast2cfg(
            {
                (ast.label, BUnOp("!", bexp), CSkip())
            }, cfalse, cfg)
        # Gather all dangling edges leaving those newly converted cfg parts and return them
        true_branch_dangling_edges.update(false_branch_dangling_edges)
        return cfg, true_branch_dangling_edges
    elif isinstance(ast, CSequence):
        # Sequence is different : no top-level node.
        # We sequentially convert all sub-ast of sequence ast, passing dangling edges from one
        # to the next one
        # Copy previous_edges to avoid modifying it
        edges_to_transfer = copy.deepcopy(previous_edges)
        for sub_ast in list(ast.children):
            cfg, edges_to_transfer = recursive_ast2cfg(edges_to_transfer, sub_ast, cfg)
        # Return dangling edges at the end of the conversion
        return cfg, edges_to_transfer
    elif isinstance(ast, CWhile):
        # We convert the "condition true" sub ast
        bexp, ctrue = ast.children
        cfg, true_branch_dangling_edges = recursive_ast2cfg(
            {
                (ast.label, bexp, CSkip())
            }, ctrue, cfg
        )
        # And we link output dangling edges to the top level-node to actually create the loop
        for previous_node, bexp, com in true_branch_dangling_edges:
            cfg.add_edge(previous_node, ast.label, bexp=bexp, com=com)
        # Return an half-edge that will be followed if while condition does not apply
        return cfg, {(ast.label, BUnOp("!", ctrue), CSkip())}


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from utils.printer import print_ast, print_cfg
    from astree.aexp import *
    from astree.bexp import *


    true_ast = CAssign(AVariable('X'), AConstant(2), label=3)
    false_ast = CAssign(AVariable('Y'), AConstant(4), label=4)
    if_ast = CIf(BConstant(True), true_ast, false_ast, label=2)

    assign_ast = CAssign(AVariable('Z'), AVariable('X'), label=5)
    assign_ast_bis = CAssign(AVariable('Y'), AConstant('3'), label=6)
    seq_ast = CSequence(if_ast, assign_ast, assign_ast_bis)

    while_ast=CWhile(BConstant(True), seq_ast, label=1)

    cfg = ast2cfg(while_ast)
    print_cfg(cfg)
    pos = nx.spring_layout(cfg)
    nx.draw_networkx(cfg, pos=pos)
    nx.draw_networkx_edge_labels(cfg, pos=pos, font_size=4)
    limits = plt.axis("off")
    plt.show()