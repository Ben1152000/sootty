from lark import Lark, Tree, Token, Visitor

try:
    import importlib.resources as pkg_resources
except ImportError:
    import importlib_resources as pkg_resources

from . import static
parser = Lark(pkg_resources.open_text(static, "grammar.lark").read())


class Prune(Visitor):

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

    def __init__(self, expression):
        parsed = parser.parse(expression)
        self.tree = Prune().visit(parsed)

if __name__ == "__main__":

    print(LimitExpression("a + b & c - d + const 1").tree.pretty(' '))

    print(LimitExpression("after (acc clk == const 5) & ready & value & (3 next data == const 64)").tree)

    print(LimitExpression("D1 & D2").tree)