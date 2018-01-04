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

    def eval(self):
        return self.value


class AUnOp(AExp):
    """
    Unary operators.
    """

    def __init__(self, op, aexp):
        super().__init__(typename="AUNOP")
        self.op = op
        aexp.parent = self

    def eval(self):
        value = self.children[0].eval()
        if self.op == '-':
            return (- value)
        else:
            raise TypeError("Undefined unary operator {op}".format(op=self.op))


class ABinOp(AExp):
    """
    Binary operators.
    """

    OPERATORS = {
        '+': '__add__',
        '-': '__sub__',
        '*': '__mul__',
        '/': '__div__',
        '%': '__mod__',
    }

    def __init__(self, op, left, right):
        super().__init__(typename="ABINOP")
        self.op = op
        left.parent = self
        right.parent = self

    def eval(self):
        nodes = self.children
        left = nodes[0].eval()
        right = nodes[1].eval()
        return getattr(left, self.OPERATORS[self.op])(right)


if __name__ == '__main__':
    from anytree import RenderTree
    ast = ABinOp('+', AConstant(1), AUnOp('-', AConstant(2)))
    print(RenderTree(ast))
    print(ast.eval())
