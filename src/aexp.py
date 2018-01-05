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


class AExp(AnyNode):
    """
    Arithmetic expressions.
    """

    def __init__(self, typename="AEXP", **kwargs):
        """[summary]

        Arguments:
            type -- type of the Aexp
            kwargs -- optional keywords
        """
        super().__init__()
        self.typename = typename


class AConstant(AExp):
    """
    Constant values, namely integers.
    """

    def __init__(self, value):
        super().__init__(typename="ACONSTANT")
        self.value = value

    def eval(self, state):
        return self.value


class AVariable(AExp):
    """
    Named variables.
    """

    def __init__(self, name):
        super().__init__(typename="AVARIABLE")
        self.name = name

    def eval(self, state):
        return state[self.name]


class AUnOp(AExp):
    """
    Unary operators.
    """

    OPERATORS = {
        '+': '__pos__',
        '-': '__neg__',
        '.': '__abs__',
    }

    def __init__(self, op, aexp):
        super().__init__(typename="AUNOP")
        self.op = op
        aexp.parent = self

    def eval(self, state):
        value = self.children[0].eval(state)
        return getattr(value, self.OPERATORS[self.op])()

class ABinOp(AExp):
    """
    Binary operators.
    """

    OPERATORS = {
        '+': '__add__',
        '-': '__sub__',
        '*': '__mul__',
        '//': '__floordiv__',
        '%': '__mod__',
        '**': '__pow__',
    }

    def __init__(self, op, left, right):
        super().__init__(typename="ABINOP")
        self.op = op
        left.parent = self
        right.parent = self

    def eval(self, state):
        nodes = self.children
        left = nodes[0].eval(state)
        right = nodes[1].eval(state)
        return getattr(left, self.OPERATORS[self.op])(right)


if __name__ == '__main__':
    from anytree import RenderTree
    ast = ABinOp('//', AVariable('X'), AUnOp('+', AConstant(2)))
    print(RenderTree(ast))
    print(ast.eval({'X': 3}))
