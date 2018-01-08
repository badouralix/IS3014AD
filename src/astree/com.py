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
    def __init__(self, typename="COM", label=None, **kwargs):
        """[summary]

        Arguments:
            typename -- type of the Com
            label    -- label of the Com for the labeled WHILE language
            kwargs   -- optional keywords
        """
        super().__init__()
        self._typename = typename
        if label is not None:
            self.label = label

    def __repr__(self):
        try:
            return "{}(label={})".format(self.__class__.__name__, self.label)
        except:
            return "{}()".format(self.__class__.__name__)


class CSkip(Com):
    def __init__(self, label=None):
        super().__init__(typename="CSKIP", label=label)

    def exec(self, state):
        return state


class CAssign(Com):
    def __init__(self, var, exp, label=None):
        super().__init__(typename="CASSIGN", label=label)
        var.parent = self
        exp.parent = self

    def exec(self, state):
        var, exp = self.children
        value = exp.eval(state)
        state[var.name] = value             # should var be a string or an aexp?
        return state


class CSequence(Com):
    def __init__(self, *args, label=None):
        super().__init__(typename="CSEQUENCE", label=label)
        for arg in args:
            arg.parent = self

    def exec(self, state):
        for child in list(self.children):
            child.exec(state)
        return state


class CIf(Com):
    def __init__(self, bexp, ctrue, cfalse=CSkip(), label=None):
        super().__init__(typename="CIF", label=label)
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
    def __init__(self, bexp, com, label=None):
        super().__init__(typename="CWHILE", label=label)
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
    import os, sys
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from astree.aexp import *
    from astree.bexp import *
    from utils.printer import print_ast
    ast = CSequence(CSkip(), CSequence(CAssign(AVariable('X'), ABinOp('+', AConstant(1), AConstant(1)), label=2), CSkip(), label=1), label=0)
    ast = CIf(BBinOp('==', AVariable('X'), AConstant(0)), CAssign(AVariable('Y'), AConstant(1)), label=0)
    ast = CWhile(BBinOp('!=', AVariable('X'), AConstant(5)), CAssign(AVariable('X'), ABinOp('+', AVariable('X'), AConstant(1)), label=1), label=0)
    ast = CSequence(CAssign(AVariable('X'), AConstant(1), label=1), CAssign(AVariable('Y'), AConstant(2), label=2), CAssign(AVariable('Z'), AConstant(3), label=3), label=0)
    print_ast(ast)
    print(ast.exec({'X': 0}))
