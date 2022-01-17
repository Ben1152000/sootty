import json, sys
from vcd.reader import *

from ..exceptions import *
from ..limits import LimitExpression
from .wiregroup import WireGroup
from .wire import Wire


class WireTrace:
    def __init__(self):
        self.root = WireGroup("__root__")

    @classmethod
    def from_vcd(cls, filename):
        """
        Construct a WireTrace object from a parsed vcd file, using the pyvcd library.

        Syntax of four-state VCD file (IEEE 1364-2005 §18.2.1):

        value_change_dump_definitions ::=
            { declaration_command }{ simulation_command }
        declaration_command ::=
            declaration_keyword
            [ command_text ]
            $end
        simulation_command ::=
            simulation_keyword { value_change } $end
            | $comment [ comment_text ] $end
            | simulation_time
            | value_change
        declaration_keyword ::=
            $comment | $date | $enddefinitions | $scope | $timescale | $upscope
            | $var | $version
        simulation_keyword ::=
            $dumpall | $dumpoff | $dumpon | $dumpvars
        simulation_time ::=
            # decimal_number
        value_change ::=
            scalar_value_change
            | vector_value_change
        scalar_value_change ::=
            value identifier_code
        value ::=
            0 | 1 | x | X | z | Z
        vector_value_change ::=
            b binary_number identifier_code
            | B binary_number identifier_code
            | r real_number identifier_code
            | R real_number identifier_code
        identifier_code ::=
            { ASCII character }
        """

        this = cls()
        this.metadata = dict()  # dictionary of vcd metadata
        wires = dict()  # map from id_code to wire object
        stack = [this.root]  # store stack of current group for scoping

        with open(filename, "rb") as stream:
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

    def evaluate(self, expr: str):
        wire = self._compute_wire(LimitExpression(expr).tree)
        return wire.times(self.length())

    def _compute_wire(self, expr):
        """
        Evaluate a limit expression
        """
        if expr.data == "wire":
            return self.find(expr.children[0])
        elif expr.data.type == "NOT":
            return ~self._compute_wire(expr.children[0])
        elif expr.data.type == "NEG":
            return -self._compute_wire(expr.children[0])
        elif expr.data.type == "AND":
            return self._compute_wire(expr.children[0]) & self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "OR":
            return self._compute_wire(expr.children[0]) | self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "XOR":
            return self._compute_wire(expr.children[0]) ^ self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "EQ":
            return self._compute_wire(expr.children[0]) == self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "NEQ":
            return self._compute_wire(expr.children[0]) != self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "GT":
            return self._compute_wire(expr.children[0]) > self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "GEQ":
            return self._compute_wire(expr.children[0]) >= self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "LT":
            return self._compute_wire(expr.children[0]) < self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "LEQ":
            return self._compute_wire(expr.children[0]) <= self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "SL":
            return self._compute_wire(expr.children[0]) << self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "SR":
            return self._compute_wire(expr.children[0]) >> self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "ADD":
            return self._compute_wire(expr.children[0]) + self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "SUB":
            return self._compute_wire(expr.children[0]) - self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "MOD":
            return self._compute_wire(expr.children[0]) % self._compute_wire(
                expr.children[1]
            )
        elif expr.data.type == "FROM":
            return self._compute_wire(expr.children[0])._from()
        elif expr.data.type == "AFTER":
            return self._compute_wire(expr.children[0])._after()
        elif expr.data.type == "UNTIL":
            return self._compute_wire(expr.children[0])._until()
        elif expr.data.type == "BEFORE":
            return self._compute_wire(expr.children[0])._before()
        elif expr.data.type == "NEXT":
            return self._compute_wire(expr.children[0])._next()
        elif expr.data.type == "PREV":
            return self._compute_wire(expr.children[0])._prev()
        elif expr.data.type == "ACC":
            return self._compute_wire(expr.children[0])._acc()
        elif expr.data.type == "CONST":
            return Wire.const(int(expr.children[0]))
        elif expr.data.type == "TIME":
            return Wire.time(int(expr.children[0]))

    def compute_limits(self, start_expr: str, end_expr: str):
        starts = self.evaluate(start_expr)
        start = starts[0] if len(starts) > 0 else 0
        ends = list(filter(lambda time: time > start, self.evaluate(end_expr)))
        end = ends[0] if len(ends) else self.length()
        return (start, end)
