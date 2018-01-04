#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sources
-------

- https://arxiv.org/pdf/1603.08949.pdf
- https://ruslanspivak.com/lsbasi-part7/
- https://tomassetti.me/parsing-in-python/#parseTree

"""

from anytree import AnyNode


class Com(AnyNode):
    def __init__(self, typename="COM", **kwargs):
        """[summary]

        Arguments:
            type -- type of the Aexp
            kwargs -- optional keywords
        """
        super().__init__()
        self.typename = typename


class CSkip(Com):
    def __init__(self):
        super().__init__(typename="CSKIP")

    def exec(self, state):
        return state


class CAssign(Com):
    def __init__(self, var, exp):
        super().__init__(typename="CASSIGN")
        self.var = var
        exp.parent = self

    def exec(self, state):
        value = self.children[0].eval(state)
        state[self.var] = value
        return state


class CSequence(Com):
    def __init__(self, left, right):
        super().__init__(typename="CSEQUENCE")
        left.parent = self
        right.parent = self

    def exec(self, state):
        left, right = self.children
        left.exec(state)
        right.exec(state)
        return state


if __name__ == '__main__':
    from aexp import *
    from anytree import RenderTree
    ast = CSequence(CSkip(), CSequence(CAssign('X', ABinOp('+', AConstant(1), AConstant(1))), CSkip()))
    print(RenderTree(ast))
    print(ast.exec({}))
