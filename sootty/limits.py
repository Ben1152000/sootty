from lark import Lark, Tree, Token, Visitor

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

# Read and interpret grammar file.
from . import static

parser = Lark(pkg_resources.open_text(static, "grammar.lark").read())


class Prune(Visitor):
    """Visitor class used to prune the parse tree to make it easier to interpret."""

    def binexp(self, tree):
        if len(tree.children) == 1:
            tree.data = tree.children[0].data
            tree.children = tree.children[0].children
        else:
            if type(tree.children[1] is Tree):
                tree.data = tree.children[1].children[0]
            else:
                tree.data = tree.children[1]
            tree.children = [tree.children[0], tree.children[2]]

    def start(self, tree):
        self.binexp(tree)

    def lexp(self, tree):
        self.binexp(tree)

    def rexp(self, tree):
        self.binexp(tree)

    def sexp(self, tree):
        self.binexp(tree)

    def aexp(self, tree):
        self.binexp(tree)

    def wire(self, tree):
        if len(tree.children) == 1:
            if type(tree.children[0]) is Tree:
                tree.data = tree.children[0].data
                tree.children = tree.children[0].children
        elif len(tree.children) == 2:
            if type(tree.children[0]) is Tree:
                tree.data = tree.children[0].children[0]
                tree.children = [tree.children[1]]
            elif type(tree.children[0]) is Token:
                tree.data = tree.children[0]
                tree.children = [tree.children[1]]
        elif len(tree.children) == 3:
            tree.data = tree.children[1].children[0]
            tree.children = [tree.children[0], tree.children[2]]


class LimitExpression:
    """Parses an expression representing the limits of a wiretrace window."""

    def __init__(self, expression):
        parsed = parser.parse(expression)
        self.tree = Prune().visit(parsed)
