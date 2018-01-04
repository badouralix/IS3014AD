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


class BExp(AnyNode):
    """
    Arithmetic expressions.
    """

    def __init__(self, typename="BEXP", **kwargs):
        """[summary]

        Arguments:
            type -- type of the Aexp
            kwargs -- optional keywords
        """
        super().__init__()
        self.typename = typename


class BConstant(BExp):
    """
    Constant values, namely bool.
    """

    def __init__(self, value):
        super().__init__(typename="BCONSTANT")
        self.value = value

    def eval(self, state):
        return self.value


class BVariable(BExp):
    """
    Named variables.
    """

    def __init__(self, name):
        super().__init__(typename="BVARIABLE")
        self.name = name

    def eval(self, state):
        return state[self.name]


class BUnOp(BExp):
    """
    Unary operators.
    """

    def __init__(self, op, aexp):
        super().__init__(typename="BUNOP")
        if op in ['!']:
            self.op = op
        else:
            raise TypeError("Unknown unary boolean operator {}".format(self.op))
        aexp.parent = self

    def eval(self, state):
        value = self.children[0].eval(state)
        if self.op == '!':
            return not value
        else:
            raise TypeError("Unknown unary boolean operator {}".format(self.op))


class BBinOp(BExp):
    """
    Binary operators.
    """

    OPERATORS = {
        '&&': '__and__',
        '||': '__or__',
        '^':  '__xor__',
        '==': '__eq__',
        '<':  '__lt__',
        '<=': '__le__',
        '>':  '__gt__',
        '>=': '__ge__',
    }

    def __init__(self, op, left, right):
        super().__init__(typename="BBINOP")
        self.op = op
        left.parent = self
        right.parent = self

    def eval(self, state):
        nodes = self.children
        left = nodes[0].eval(state)
        right = nodes[1].eval(state)
        return getattr(left, self.OPERATORS[self.op])(right)


if __name__ == '__main__':
    from aexp import *
    from anytree import RenderTree
    ast = BBinOp('&&', BVariable('X'), BUnOp('!', BConstant(False)))
    print(RenderTree(ast))
    print(ast.eval({'X': True}))
