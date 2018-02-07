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
    Boolean expressions.
    """

    def __init__(self, typename="BEXP", **kwargs):
        """[summary]

        Arguments:
            type -- type of the BExp
            kwargs -- optional keywords
        """
        super().__init__()
        self._typename = typename


class BConstant(BExp):
    """
    Constant values, namely bool.
    """

    def __init__(self, value):
        super().__init__(typename="BCONSTANT")
        self.value = value

    def eval(self, state):
        return self.value

    @property
    def vars(self):
        return {}

class BVariable(BExp):
    """
    Named variables.
    """

    def __init__(self, name):
        super().__init__(typename="BVARIABLE")
        self.name = name

    def eval(self, state):
        return state[self.name]

    @property
    def vars(self):
        return {self.name}

class BUnOp(BExp):
    """
    Unary operators.
    """

    def __init__(self, op, bexp):
        super().__init__(typename="BUNOP")
        if op in ['!']:
            self.op = op
        else:
            raise TypeError("Unknown unary boolean operator {}".format(self.op))
        bexp.parent = self

    def eval(self, state):
        value = self.child.eval(state)
        if self.op == '!':
            return not value
        else:
            raise TypeError("Unknown unary boolean operator {}".format(self.op))

    @property
    def child(self):
        return self.children[0]

    @property
    def vars(self):
        return self.child.vars

class BBinOp(BExp):
    """
    Binary operators.
    """

    OPERATORS = {
        '&&': lambda b1, b2: b1 and b2,
        '||': lambda b1, b2: b1 or b2,
        '^':  lambda b1, b2: b1 ^ b2,

        '==': lambda a1, a2: a1 == a2,
        '!=': lambda a1, a2: a1 != a2,
        '<':  lambda a1, a2: a1 < a2,
        '<=': lambda a1, a2: a1 <= a2,
        '>':  lambda a1, a2: a1 > a2,
        '>=': lambda a1, a2: a1 >= a2,
    }

    def __init__(self, op, left, right):
        super().__init__(typename="BBINOP")

        if op in ['&&', '||', '^'] + ['==', '!=', '<', '<=', '>', '>=']:
            self.op = op
        else:
            raise TypeError("Unknown binary boolean operator {}".format(self.op))

        left.parent = self
        right.parent = self

    def eval(self, state):
        left = self.left.eval(state)
        right = self.right.eval(state)
        return self.OPERATORS[self.op]( left, right )

    @property
    def subtypes(self):
        if self.op in ['==', '!=', '<', '<=', '>', '>=']:
            return "AEXP"
        elif self.op in ['&&', '||', '^']:
            return "BEXP"

    @property
    def left(self):
        return self.children[0]

    @property
    def right(self):
        return self.children[1]

    @property
    def vars(self):
        return set.union(self.left.vars, self.right.vars)

if __name__ == '__main__':
    from aexp import *
    from anytree import RenderTree
    ast = BBinOp('&&', BVariable('X'), BUnOp('!', BConstant(False)))
    print(RenderTree(ast))
    print(ast.eval({'X': True}))
    print(ast.vars)
