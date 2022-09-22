import sys
from vcd.reader import *

from ..exceptions import *
from ..parser import parser
from .wiregroup import WireGroup
from .wire import Wire
from ..utils import evcd2vcd


class WireTrace:
    def __init__(self):
        self.root = WireGroup("__root__")

    @classmethod
    def from_vcd(cls, filename):
        """
        Construct a WireTrace object from a parsed vcd file, using the pyvcd library.

        Syntax of 4-state VCD file (IEEE 1800-2017 §21.7.2):

        value_change_dump_definitions ::=
             { declaration_command }{ simulation_command }
        declaration_command ::=
             $comment [ comment_text ] $end
           | $date [ date_text ] $end
           | $enddefinitions $end
           | $scope [ scope_type scope_identifier ] $end
           | $timescale [ time_number time_unit ] $end
           | $upscope $end
           | $var [ var_type size identifier_code reference ] $end
           | $version [ version_text system_task ] $end
        simulation_command ::=
             $dumpall { value_change } $end
           | $dumpoff { value_change } $end
           | $dumpon { value_change } $end
           | $dumpvars { value_change } $end
           | $comment [ comment_text ] $end
           | simulation_time
           | value_change
        scope_type ::=
             begin
           | fork
           | function
           | module
           | task
        time_number ::= 1 | 10 | 100
        time_unit ::= s | ms | us | ns | ps | fs
        var_type ::=
            event | integer | parameter | real | realtime | reg | supply0 | supply1 | time
           | tri | triand | trior | trireg | tri0 | tri1 | wand | wire | wor
        simulation_time ::= # decimal_number
        value_change ::=
             scalar_value_change
           | vector_value_change
        scalar_value_change ::= value identifier_code
        value ::= 0 | 1 | x | X | z | Z
        vector_value_change ::=
             b binary_number identifier_code
           | B binary_number identifier_code
           | r real_number identifier_code
           | R real_number identifier_code
        identifier_code ::= { ASCII character }
        size ::= decimal_number
        reference ::=
             identifier
           | identifier [ bit_select_index ]
           | identifier [ msb_index : lsb_index ]
        index ::= decimal_number
        scope_identifier ::= { ASCII character }
        comment_text ::= { ASCII character }
        date_text ::= { ASCII character }
        version_text ::= { ASCII character }
        system_task ::= ${ASCII character}
        """

        this = cls()
        this.metadata = dict()  # dictionary of vcd metadata
        wires = dict()  # map from id_code to wire object
        stack = [this.root]  # store stack of current group for scoping

        with open(filename, "rb") as stream:
            if filename.endswith(".evcd"):
                stream = evcd2vcd(stream)

            tokens = tokenize(stream)
            for token in tokens:
                if token.kind is TokenKind.COMMENT:
                    this.metadata["comment"] = token.comment
                elif token.kind is TokenKind.DATE:
                    this.metadata["date"] = token.date
                elif token.kind is TokenKind.ENDDEFINITIONS:
                    break  # end of definitions
                elif token.kind is TokenKind.SCOPE:
                    group = WireGroup(token.scope.ident)
                    stack[-1].add_group(group)
                    stack.append(group)
                elif token.kind is TokenKind.TIMESCALE:
                    this.metadata["timescale"] = token.timescale
                elif token.kind is TokenKind.UPSCOPE:
                    if len(stack) == 0:
                        raise SoottyError(f"Illegal end of scope.")
                    stack.pop()
                elif token.kind is TokenKind.VAR:
                    if token.var.id_code in wires:
                        stack[-1].add_wire(wires[token.var.id_code])
                    else:
                        wire = Wire(
                            name=token.var.reference,
                            width=token.var.size,
                        )
                        wires[token.var.id_code] = wire
                        stack[-1].add_wire(wire)
                elif token.kind is TokenKind.VERSION:
                    this.metadata["version"] = token.version
                else:
                    raise SoottyError(f"Invalid vcd token when parsing: {token}")

            time = None
            for token in tokens:
                if token.kind is TokenKind.CHANGE_TIME:
                    time = token.time_change
                elif token.kind is TokenKind.CHANGE_SCALAR:
                    value = token.scalar_change.value
                    value = int(value) if value in ("0", "1") else value
                    wires[token.scalar_change.id_code][time] = value
                elif token.kind is TokenKind.CHANGE_VECTOR:
                    value = token.vector_change.value
                    wires[token.vector_change.id_code][time] = value
                elif token.kind is TokenKind.CHANGE_REAL:
                    raise SoottyInternalError(
                        f"You forgot to implement token CHANGE_REAL."
                    )
                elif token.kind is TokenKind.CHANGE_STRING:
                    raise SoottyInternalError(
                        f"You forgot to implement token CHANGE_STRING."
                    )
                elif token.kind is TokenKind.DUMPALL:
                    pass  # not sure what to do here
                elif token.kind is TokenKind.DUMPOFF:
                    pass  # not sure what to do here
                elif token.kind is TokenKind.DUMPON:
                    pass  # not sure what to do here
                elif token.kind is TokenKind.DUMPVARS:
                    pass  # not sure what to do here
                elif token.kind is TokenKind.END:
                    pass  # not sure what to do here
                else:
                    raise SoottyError(f"Invalid vcd token when parsing: {token}")

            return this

    @classmethod
    def from_pyrtl(cls, sim_trace):
        """Parses a WireTrace object from a PyRTL SimulationTrace object.

        :param SimulationTrace sim_trace: The object that stores the PyRTL tracer.
        """
        trace = cls()
        for wirename in sim_trace.trace:
            print(sim_trace.trace[wirename], file=sys.stderr)
            trace.root.add_wire(
                Wire.from_data(
                    name=wirename,
                    width=sim_trace._wires[wirename].bitwidth,
                    data=sim_trace.trace[wirename],
                )
            )
        return trace

    def num_wires(self):
        """Returns total number of wires."""
        return self.root.num_wires()

    def length(self):
        """Returns the time duration of the longest wire."""
        return self.root.length()

    def find(self, name: str):
        """Returns the wire object with the given name, raises an error if not found."""
        return self.root.find(name)

    def get_wire_names(self):
        """Returns list of all wire names."""
        return self.root.get_names()

    def _compute_wire(self, node):
        """Evaluate a limit expression"""
        if node.data == "wire":
            return self.find(node.children[0])
        elif node.data == "call":
            name = node.children[0]
            args = list(map(self._compute_wire, node.children[1].children))
            if name == "AXI":
                if args.__len__() != 2:
                    raise SoottyError(f'Expected 2 arguments for called function "{name}".')
                return args[0] & args[1]
            raise SoottyError(f'Function "{name}" does not exist.')
        elif node.data.type == "NEG":
            return self._compute_wire(node.children[0]).__neg__()
        elif node.data.type == "INV":
            return self._compute_wire(node.children[0]).__invert__()
        elif node.data.type == "AND":
            return self._compute_wire(node.children[0]) & self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "OR":
            return self._compute_wire(node.children[0]) | self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "XOR":
            return self._compute_wire(node.children[0]) ^ self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "LNOT":
            return self._compute_wire(node.children[0])._logical_not()
        elif node.data.type == "LAND":
            return self._compute_wire(node.children[0])._logical_and(
                self._compute_wire(node.children[1])
            )
        elif node.data.type == "LOR":
            return self._compute_wire(node.children[0])._logical_or(
                self._compute_wire(node.children[1])
            )
        elif node.data.type == "EQ":
            return self._compute_wire(node.children[0]) == self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "NEQ":
            return self._compute_wire(node.children[0]) != self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "GT":
            return self._compute_wire(node.children[0]) > self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "GEQ":
            return self._compute_wire(node.children[0]) >= self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "LT":
            return self._compute_wire(node.children[0]) < self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "LEQ":
            return self._compute_wire(node.children[0]) <= self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "SL":
            return self._compute_wire(node.children[0]) << self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "SR":
            return self._compute_wire(node.children[0]) >> self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "ADD":
            return self._compute_wire(node.children[0]) + self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "SUB":
            return self._compute_wire(node.children[0]) - self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "MOD":
            return self._compute_wire(node.children[0]) % self._compute_wire(
                node.children[1]
            )
        elif node.data.type == "FROM":
            return self._compute_wire(node.children[0])._from()
        elif node.data.type == "AFTER":
            return self._compute_wire(node.children[0])._after()
        elif node.data.type == "UNTIL":
            return self._compute_wire(node.children[0])._until()
        elif node.data.type == "BEFORE":
            return self._compute_wire(node.children[0])._before()
        elif node.data.type == "NEXT":
            return self._compute_wire(node.children[0])._next()
        elif node.data.type == "PREV":
            return self._compute_wire(node.children[0])._prev()
        elif node.data.type == "ACC":
            return self._compute_wire(node.children[0])._acc()
        elif node.data.type == "CONST":
            return Wire.const(int(node.children[0]))
        elif node.data.type == "TIME":
            return Wire.time(int(node.children[0]))

    def compute_wire(self, expr: str):
        """Evaluate a limit expression to a wire."""
        return self._compute_wire(parser.parse(expr))

    def compute_wires(self, exprs: str):
        """Evaluate comma-separated limit expressions as a list of wires."""
        return list(map(self._compute_wire, parser.parse_list(exprs)))

    def evaluate(self, expr: str):
        return self.compute_wire(expr).times(self.length())

    def compute_limits(self, start_expr: str, end_expr: str):
        starts = self.evaluate(start_expr)
        start = starts[0] if len(starts) > 0 else 0
        ends = list(filter(lambda time: time > start, self.evaluate(end_expr)))
        end = ends[0] if len(ends) else self.length()
        return (start, end)

    def print_breakpoints(self, breakpoints: list):
        """
        Print a table of wires and their values.
        """

        def rec_print(wires):
            for scope, sub in wires.items():
                if type(sub) is dict:
                    print("scope\t" + scope)
                    rec_print(sub)
                else:  # is list
                    print("scope\t" + scope)
                    for wire in sub:
                        print(wire.name, end="\t")
                        for breakpoint in breakpoints:
                            print(str(wire._data.get(breakpoint)), end="\t")
                        print()

        print("time", *breakpoints, sep="\t")
        rec_print(self.root.get_wires())
