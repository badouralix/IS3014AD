#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Sources
-------

- https://arxiv.org/pdf/1603.08949.pdf
- https://ruslanspivak.com/lsbasi-part7/
- https://tomassetti.me/parsing-in-python/#parseTree
- http://fsl.cs.illinois.edu/images/0/0d/CS522-Spring-2011-PL-book-imp.pdf

"""

from anytree import AnyNode
from astree.aexp import AVariable


class Stmt(AnyNode):
    def __init__(self, typename="STMT", label=None, **kwargs):
        """[summary]

        Arguments:
            typename -- type of the statement
            label    -- label of the statement for the labeled WHILE language
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


class SSkip(Stmt):
    def __init__(self, label=None):
        super().__init__(typename="SSKIP", label=label)

    def exec(self, state=dict(), verbose=True):
        return state

    @property
    def vars(self):
        return set()


class SAssign(Stmt):
    def __init__(self, var, aexp, label=None):
        super().__init__(typename="SASSIGN", label=label)

        self.var = var
        var.parent = self

        self.aexp = aexp
        aexp.parent = self

    def exec(self, state=dict(), verbose=True):
        value = self.aexp.eval(state)
        state[self.var.name] = value
        return state

    def eval(self, state=dict(), verbose=True):
        self.exec(state, verbose)
        return state[self.var.name]

    @property
    def def_var(self):
        return self.children[0].vars

    @property
    def vars(self):
        return self.children[1].vars


class SSequence(Stmt):
    def __init__(self, *args, label=None):
        super().__init__(typename="SSEQUENCE", label=label)
        for arg in args:
            arg.parent = self

    def exec(self, state=dict(), verbose=True):
        for child in list(self.children):
            child.exec(state, verbose)
        return state


class SIf(Stmt):
    def __init__(self, bexp, strue, sfalse=SSkip(), label=None):
        super().__init__(typename="SIF", label=label)
        bexp.parent = self
        strue.parent = self
        sfalse.parent = self

    def exec(self, state=dict(), verbose=True):
        bexp, strue, sfalse = self.children
        if bexp.eval(state):
            return strue.exec(state, verbose)
        else:
            return sfalse.exec(state, verbose)


class SWhile(Stmt):
    def __init__(self, bexp, stmt, label=None):
        super().__init__(typename="SWHILE", label=label)
        bexp.parent = self
        stmt.parent = self

    def exec(self, state=dict(), verbose=True):
        bexp, stmt = self.children
        if bexp.eval(state):
            stmt.exec(state, verbose)
            return self.exec(state, verbose)
        else:
            return state


class SInput(Stmt):
    def __init__(self, aexp, label=None):
        super().__init__(typename="SINPUT", label=label)
        aexp.parent = self

    def exec(self, state=dict(), verbose=True):
        if isinstance(self.child, AVariable):
            if verbose:
                value = input("Input : {varname} = ".format(varname=self.child.name))
                state[self.child.name] = int(value)     # TODO: try except
        else:
            raise TypeError("Input type is {type} at node {label}".format(type=self.child.typename, label=self.label))
        return state

    @property
    def child(self):
        return self.children[0]

    @property
    def def_var(self):
        return self.child.vars

    @property
    def vars(self):
        return set()


class SPrint(Stmt):
    def __init__(self, aexp, label=None):
        super().__init__(typename="SPRINT", label=label)
        aexp.parent = self

    def exec(self, state=dict(), verbose=True):
        if verbose:
            print(self.child.eval(state))
        return state

    @property
    def child(self):
        return self.children[0]

    @property
    def vars(self):
        return self.child.vars


if __name__ == '__main__':
    import os, sys
    sys.path.insert(1, os.path.join(sys.path[0], '..'))
    from astree.aexp import *
    from astree.bexp import *
    from utils.printer import print_ast
    ast = SSequence(SSkip(), SSequence(SAssign(AVariable('X'), ABinOp('+', AConstant(1), AConstant(1)), label=2), SSkip(), label=1), label=0)
    ast = SIf(BBinOp('==', AVariable('X'), AConstant(0)), SAssign(AVariable('Y'), AConstant(1)), label=0)
    ast = SWhile(BBinOp('!=', AVariable('X'), AConstant(5)), SAssign(AVariable('X'), ABinOp('+', AVariable('X'), AConstant(1)), label=1), label=0)
    ast = SSequence(SAssign(AVariable('X'), AConstant(1), label=1), SAssign(AVariable('Y'), AConstant(2), label=2), SAssign(AVariable('Z'), AConstant(3), label=3), label=0)
    ast = SPrint(AVariable('X'))
    print_ast(ast)
    print(ast.exec({'X': 0}))
