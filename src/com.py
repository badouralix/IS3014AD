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
        var.parent = self
        exp.parent = self

    def exec(self, state):
        var, exp = self.children
        value = exp.eval(state)
        state[var.name] = value             # should var be a string or an aexp?
        return state


class CSequence(Com):
    def __init__(self, *args):
        super().__init__(typename="CSEQUENCE")
        for arg in args:
            arg.parent = self

    def exec(self, state):
        for child in list(self.children):
            child.exec(state)
        return state


class CIf(Com):
    def __init__(self, bexp, ctrue, cfalse=CSkip()):
        super().__init__(typename="CIF")
        bexp.parent = self
        ctrue.parent = self
        cfalse.parent = self

    def exec(self, state):
        bexp, ctrue, cfalse = self.children
        if bexp.eval(state):
            return ctrue.exec(state)
        else:
            return cfalse.exec(state)

class CWhile(Com):
    def __init__(self, bexp, com):
        super().__init__(typename="CWHILE")
        bexp.parent = self
        com.parent = self

    def exec(self, state):
        bexp, com = self.children
        if bexp.eval(state):
            com.exec(state)
            return self.exec(state)
        else:
            return state


if __name__ == '__main__':
    from aexp import *
    from bexp import *
    from anytree import RenderTree
    ast = CSequence(CSkip(), CSequence(CAssign(AVariable('X'), ABinOp('+', AConstant(1), AConstant(1))), CSkip()))
    ast = CIf(BBinOp('==', AVariable('X'), AConstant(0)), CAssign(AVariable('Y'), AConstant(1)))
    ast = CWhile(BBinOp('!=', AVariable('X'), AConstant(5)), CAssign(AVariable('X'), ABinOp('+', AVariable('X'), AConstant(1))))
    ast = CSequence(CAssign(AVariable('X'), AConstant('1')), CAssign(AVariable('Y'), AConstant('2')), CAssign(AVariable('Z'), AConstant('3')))
    print(RenderTree(ast))
    print(ast.exec({'X': 0}))
