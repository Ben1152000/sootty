import json, sys
# from pyDigitalWaveTools.vcd.parser import VcdParser
from vcd.reader import *

from .exceptions import *
from .limits import LimitExpression


class Wire:

    def __init__(self, name, width=1, data=None):
        self.name = name
        self.width = width
        self.data = list() if data is None else data
    
    def length(self):
        """Returns the time duration of the wire."""
        return len(self.data)

    def times(self, length=0):
        """Returns a list of times with high value on the wire."""
        times = []
        for time in range(len(self.data)):
            value = self.data[time]
            if type(value) is int and value > 0:
                times.append(time)
        # pad to desired length:
        if (len(self.data) - 1) in times:
            for time in range(len(self.data), length):
                times.append(time)
        return times

    def __invert__(self):
        data = []
        for a in self.data:
            data.append(None if a == None else ~a)
        
        return Wire(
            name="~" + self.name,
            width=self.width,
            data=data
        )

    def __neg__(self):
        data = []
        for a in self.data:
            data.append(None if a == None else -a)
        
        return Wire(
            name="-" + self.name,
            width=self.width,
            data=data
        )
    
    def __and__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else a & b)
        
        return Wire(
            name="(" + self.name + " & " + other.name + ")",
            width=max(self.width, other.width),
            data=data
        )

    def __or__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else a | b)
        
        return Wire(
            name="(" + self.name + " | " + other.name + ")",
            width=max(self.width, other.width),
            data=data
        )

    def __xor__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else a ^ b)
        
        return Wire(
            name="(" + self.name + " ^ " + other.name + ")",
            width=max(self.width, other.width),
            data=data
        )

    def __eq__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a == b))
        
        return Wire(
            name="(" + self.name + " == " + other.name + ")",
            width=1,
            data=data
        )

    def __ne__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a != b))
        
        return Wire(
            name="(" + self.name + " != " + other.name + ")",
            width=1,
            data=data
        )

    def __gt__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a > b))
        
        return Wire(
            name="(" + self.name + " > " + other.name + ")",
            width=1,
            data=data
        )

    def __ge__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a >= b))
        
        return Wire(
            name="(" + self.name + " >= " + other.name + ")",
            width=1,
            data=data
        )

    def __lt__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a < b))
        
        return Wire(
            name="(" + self.name + " < " + other.name + ")",
            width=1,
            data=data
        )

    def __le__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a <= b))
        
        return Wire(
            name="(" + self.name + " <= " + other.name + ")",
            width=1,
            data=data
        )

    def __lshift__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a << b))
        
        return Wire(
            name="(" + self.name + " << " + other.name + ")",
            width=self.width,
            data=data
        )

    def __rshift__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else int(a >> b))
        
        return Wire(
            name="(" + self.name + " >> " + other.name + ")",
            width=self.width,
            data=data
        )

    def __add__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else a + b)
        
        return Wire(
            name="(" + self.name + " + " + other.name + ")",
            width=max(self.width, other.width),
            data=data
        )
    
    def __sub__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else a - b)
        
        return Wire(
            name="(" + self.name + " - " + other.name + ")",
            width=max(self.width, other.width),
            data=data
        )
    
    def __mod__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(None if a == None or b == None else a % b)
        
        return Wire(
            name="(" + self.name + " % " + other.name + ")",
            width=self.width,
            data=data
        )
    
    def _from(self):
        data = []
        triggered = False
        for a in self.data:
            if a:
                triggered = True
            data.append(int(triggered))
        
        return Wire(
            name="from " + self.name,
            width=1,
            data=data
        )

    def _after(self):
        data = []
        triggered = False
        for a in self.data:
            data.append(int(triggered))
            if a:
                triggered = True
        
        return Wire(
            name="after " + self.name,
            width=1,
            data=data
        )

    def _until(self):
        data = []
        triggered = True
        for a in self.data:
            data.append(int(not triggered))
            if a:
                triggered = False
        
        return Wire(
            name="until " + self.name,
            width=1,
            data=data
        )

    def _before(self):
        data = []
        triggered = True
        for a in self.data:
            if a:
                triggered = False
            data.append(int(not triggered))
            
        return Wire(
            name="before " + self.name,
            width=1,
            data=data
        )

    def _next(self, amt=1):
        return Wire(
            name="next " + self.name,
            width=self.width,
            data=self.data[amt:]
        )

    def _prev(self, amt=1):
        return Wire(
            name="prev " + self.name,
            width=self.width,
            data=[None] * amt + self.data
        )

    def _acc(self):
        data = []
        counter = 0
        state = True
        for a in self.data:
            if a and not state:
                state = True
                counter += 1
            elif not a and state:
                state = False
            data.append(counter)
        
        return Wire(
            name="acc " + self.name,
            width=0,
            data=data
        )


class WireGroup:

    def __init__(self, name: str):
        self.name = name
        self.groups = []
        self.wires = []

    def add_wire(self, wire):
        self.wires.append(wire)

    def add_group(self, group):
        self.groups.append(group)

    def num_wires(self):
        """Returns total number of wires."""
        return len(self.wires) + sum([group.num_wires() for group in self.groups])

    def length(self):
        """Returns the time duration of the longest wire."""
        length = 0
        for wire in self.wires:
            length = max(length, wire.length())
        for group in self.groups:
            length = max(length, group.length())
        return length

    def find(self, name: str):
        """Returns the first wire object with the given name, if it exists."""
        for wire in self.wires:
            if wire.name == name:
                return wire
        for group in self.groups:
            return group.find(name)
        raise SoottyError(f"Wire '{name}' does not exist.")

    def get_names(self):
        """Returns list of all wire names."""
        names = set()
        for wire in self.wires:
            names.add(wire.name)
        for group in self.groups:
            names.update(group.get_names())
        return names


class WireTrace:

    def __init__(self):
        self.root = WireGroup("__root__")

    @staticmethod
    def from_vcd(filename):
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

        this = WireTrace()
        this.metadata = dict()  # dictionary of vcd metadata
        wires = dict()  # map from id_code to wire object
        stack = [this.root]  # store stack of current group for scoping

        with open(filename, 'rb') as stream:
            tokens = tokenize(stream)
            for token in tokens:
                if token.kind is TokenKind.COMMENT:
                    this.metadata['comment'] = token.comment
                elif token.kind is TokenKind.DATE:
                    this.metadata['date'] = token.date
                elif token.kind is TokenKind.ENDDEFINITIONS:
                    break  # end of definitions
                elif token.kind is TokenKind.SCOPE:
                    group = WireGroup(token.scope.ident)
                    stack[-1].add_group(group)
                    stack.append(group)
                elif token.kind is TokenKind.TIMESCALE:
                    this.metadata['timescale'] = token.timescale
                elif token.kind is TokenKind.UPSCOPE:
                    if len(stack) == 0:
                        raise SoottyError(f'Illegal end of scope.')
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
                    this.metadata['version'] = token.version
                else:
                    raise SoottyError(f'Invalid vcd token when parsing: {token}')
        
            time = None
            for token in tokens:
                if token.kind is TokenKind.CHANGE_TIME:
                    time = token.time_change
                elif token.kind is TokenKind.CHANGE_SCALAR:
                    value = token.scalar_change.value
                    value = int(value) if value in ('0', '1') else value
                    wires[token.scalar_change.id_code].data.append(value)  # TODO: fix to use time
                elif token.kind is TokenKind.CHANGE_VECTOR:
                    value = token.vector_change.value
                    wires[token.vector_change.id_code].data.append(value)  # TODO: fix to use time
                elif token.kind is TokenKind.CHANGE_REAL:
                    raise SoottyInternalError(f'You forgot to implement token CHANGE_REAL.')
                elif token.kind is TokenKind.CHANGE_STRING:
                    raise SoottyInternalError(f'You forgot to implement token CHANGE_STRING.')
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
                    raise SoottyError(f'Invalid vcd token when parsing: {token}')

            return this

    @staticmethod
    def from_pyrtl(sim_trace):
        """Parses a WireTrace object from a PyRTL SimulationTrace object.

        :param SimulationTrace sim_trace: The object that stores the PyRTL tracer.
        """
        trace = WireTrace()
        for wirename in sim_trace.trace:
            trace.root.add_wire(Wire(
                name = wirename,
                width = sim_trace._wires[wirename].bitwidth,
                data = sim_trace.trace[wirename]))
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
            return self._compute_wire(expr.children[0]) & self._compute_wire(expr.children[1])
        elif expr.data.type == "OR":
            return self._compute_wire(expr.children[0]) | self._compute_wire(expr.children[1])
        elif expr.data.type == "XOR":
            return self._compute_wire(expr.children[0]) ^ self._compute_wire(expr.children[1])
        elif expr.data.type == "EQ":
            return self._compute_wire(expr.children[0]) == self._compute_wire(expr.children[1])
        elif expr.data.type == "NEQ":
            return self._compute_wire(expr.children[0]) != self._compute_wire(expr.children[1])
        elif expr.data.type == "GT":
            return self._compute_wire(expr.children[0]) > self._compute_wire(expr.children[1])
        elif expr.data.type == "GEQ":
            return self._compute_wire(expr.children[0]) >= self._compute_wire(expr.children[1])
        elif expr.data.type == "LT":
            return self._compute_wire(expr.children[0]) < self._compute_wire(expr.children[1])
        elif expr.data.type == "LEQ":
            return self._compute_wire(expr.children[0]) <= self._compute_wire(expr.children[1])
        elif expr.data.type == "SL":
            return self._compute_wire(expr.children[0]) << self._compute_wire(expr.children[1])
        elif expr.data.type == "SR":
            return self._compute_wire(expr.children[0]) >> self._compute_wire(expr.children[1])
        elif expr.data.type == "ADD":
            return self._compute_wire(expr.children[0]) + self._compute_wire(expr.children[1])
        elif expr.data.type == "SUB":
            return self._compute_wire(expr.children[0]) - self._compute_wire(expr.children[1])
        elif expr.data.type == "MOD":
            return self._compute_wire(expr.children[0]) % self._compute_wire(expr.children[1])
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
            return Wire(name=expr.data, width=0, data=[int(expr.children[0])])
        elif expr.data.type == "TIME":
            return Wire(name=f"t_{expr.data}", width=1, data=[0] * int(expr.children[0]) + [1, 0])

    def compute_limits(self, start_expr: str, end_expr: str):
        starts = self.evaluate(start_expr)
        start = starts[0] if len(starts) > 0 else 0
        ends = list(filter(lambda time: time > start, self.evaluate(end_expr)))
        end = ends[0] if len(ends) else self.length()
        return (start, end)
