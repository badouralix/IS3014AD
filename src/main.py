#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt

from cfgraph.runners import run_test_set
from cfgraph.utils import *
from syntax.parser import parser
from tests.testor import Tester
from utils.ast2cfg import ast2cfg
from utils.printer import print_ast, print_cfg, write_cfg


def main():
    input_dir = "input"
    filename = "example.imp"
    with open(f"{input_dir}/{filename}") as f:
        source_code = f.read()

    print(source_code)

    ast = parser.parse(source_code)
    print_ast(ast)
    print()

    cfg = ast2cfg(ast)
    write_cfg(cfg, filename)
    print_cfg(cfg)


if __name__ == "__main__":
    main()
