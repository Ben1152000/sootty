import json
# from pyDigitalWaveTools.vcd.parser import VcdParser
from vcd.reader import *

from .exceptions import *
from .limits import LimitExpression


class Wire:

    def __init__(self, name, width=1, data=None):
        self.name = name
        self.width = width
        self.data = list() if data is None else data
    
    # @staticmethod
    # def _to_int(data):
    #     if data[0] == 'b':
    #         try:
    #             return int(data[1:], 2)
    #         except ValueError:
    #             return None
    #     else:
    #         try:
    #             return int(data)
    #         except ValueError:
    #             return None

    # @staticmethod
    # def from_vcd(vcd_data, base_name=""):
    #     wiredata = []
    #     source_data = sorted(vcd_data["data"])
    #     source_dict = dict(source_data)
    #     time = 0
    #     end = source_data[-1][0] if len(source_data) else 0
    #     while time <= end:
    #         if time in source_dict:
    #             wiredata.append(Wire._to_int(source_dict[time]))
    #         elif time > 0:
    #             wiredata.append(wiredata[-1])
    #         else:
    #             wiredata.append(None)
    #         time += 1
        
    #     return Wire(
    #         name=base_name + ('.' if len(base_name) else "") + vcd_data["name"],
    #         width=vcd_data["type"]["width"],
    #         data=wiredata
    #     )

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

    def __init__(self, name):
        self.name = name
        self.wires = []

    def add_wire(self, wire):
        self.wires.append(wire)

    def add_wires(self, wiregroup):
        for wire in wiregroup.wires:
            self.add_wire(wire)

    # @staticmethod
    # def from_vcd(vcd_data, base_name=None):
    #     name = "" if base_name == None else (base_name + ('.' if len(base_name) else "") + vcd_data["name"])
    #     wiregroup = WireGroup(
    #         name=vcd_data["name"] if len(name) == 0 else name
    #     )
    #     for child in vcd_data["children"]:
    #         if "data" in child:
    #             wiregroup.add_wire(
    #                 Wire.from_vcd(child, name)
    #             )
    #         else:
    #             wiregroup.add_wires(
    #                 WireGroup.from_vcd(child, name)
    #             )
    #     return wiregroup


class WireTrace:

    def __init__(self):
        self.wiregroups = []

    def add_wiregroup(self, wiregroup):
        self.wiregroups.append(wiregroup)

    # @staticmethod
    # def read_vcd(filename):
    #     with open(filename) as vcd_file:
    #         vcd = VcdParser()
    #         vcd.parse(vcd_file)
    #         return vcd.scope.toJson()  # dump json here for debugging
        
    # @staticmethod
    # def from_vcd_file(filename):
    #     vcd_data = WireTrace.read_vcd(filename)  # Read vcd data from file
    #     wiretrace = WireTrace()
    #     for child in vcd_data["children"]:
    #         wiretrace.add_wiregroup(
    #             WireGroup.from_vcd(child)
    #         )
    #     return wiretrace

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
                    pass  # implement scoping
                elif token.kind is TokenKind.TIMESCALE:
                    this.metadata['timescale'] = token.timescale
                elif token.kind is TokenKind.UPSCOPE:
                    pass  # implement scoping
                elif token.kind is TokenKind.VAR:
                    wires[token.var.id_code] = Wire(
                        name=token.var.reference,
                        width=token.var.size,
                    )
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
                    print(token.real_change)
                    raise SoottyInternalError(f'You forgot to implement token CHANGE_REAL.')
                elif token.kind is TokenKind.CHANGE_STRING:
                    print(token.string_change)
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

            group = WireGroup("")
            for wire in wires:
                group.add_wire(wires[wire])
            this.add_wiregroup(group)

            return this

    @staticmethod
    def from_pyrtl(sim_trace):
        """Parses a WireTrace object from a PyRTL SimulationTrace object.

        :param SimulationTrace sim_trace: The object that stores the PyRTL tracer.
        """
        wiretrace = WireTrace()
        wiregroup = WireGroup('main')
        for wirename in sim_trace.trace:
            wiregroup.add_wire(Wire(
                name = wirename,
                width = sim_trace._wires[wirename].bitwidth,
                data = sim_trace.trace[wirename]
            ))
        wiretrace.add_wiregroup(wiregroup)
        return wiretrace

    # Returns the time of the last entry in data
    def length(self):
        limit = 0
        for wiregroup in self.wiregroups:
            for wire in wiregroup.wires:
                limit = max(limit, len(wire.data))
        return limit

    # Gets a wire object based on the name
    def find_wire(self, name):
        for wiregroup in self.wiregroups:
            for wire in wiregroup.wires:
                if wire.name == name:
                    return wire
        raise SoottyInternalError(f"Wire '{name}' does not exist.")
    
    def get_wire_names(self):
        names = []
        for wiregroup in self.wiregroups:
            for wire in wiregroup.wires:
                names.append(wire.name)
        return names
    
    def compute_wire(self, expr):
        if expr.data == "wire":
            return self.find_wire(expr.children[0])
        elif expr.data.type == "NOT":
            return ~self.compute_wire(expr.children[0])
        elif expr.data.type == "NEG":
            return -self.compute_wire(expr.children[0])
        elif expr.data.type == "AND":
            return self.compute_wire(expr.children[0]) & self.compute_wire(expr.children[1])
        elif expr.data.type == "OR":
            return self.compute_wire(expr.children[0]) | self.compute_wire(expr.children[1])
        elif expr.data.type == "XOR":
            return self.compute_wire(expr.children[0]) ^ self.compute_wire(expr.children[1])
        elif expr.data.type == "EQ":
            return self.compute_wire(expr.children[0]) == self.compute_wire(expr.children[1])
        elif expr.data.type == "NEQ":
            return self.compute_wire(expr.children[0]) != self.compute_wire(expr.children[1])
        elif expr.data.type == "GT":
            return self.compute_wire(expr.children[0]) > self.compute_wire(expr.children[1])
        elif expr.data.type == "GEQ":
            return self.compute_wire(expr.children[0]) >= self.compute_wire(expr.children[1])
        elif expr.data.type == "LT":
            return self.compute_wire(expr.children[0]) < self.compute_wire(expr.children[1])
        elif expr.data.type == "LEQ":
            return self.compute_wire(expr.children[0]) <= self.compute_wire(expr.children[1])
        elif expr.data.type == "SL":
            return self.compute_wire(expr.children[0]) << self.compute_wire(expr.children[1])
        elif expr.data.type == "SR":
            return self.compute_wire(expr.children[0]) >> self.compute_wire(expr.children[1])
        elif expr.data.type == "ADD":
            return self.compute_wire(expr.children[0]) + self.compute_wire(expr.children[1])
        elif expr.data.type == "SUB":
            return self.compute_wire(expr.children[0]) - self.compute_wire(expr.children[1])
        elif expr.data.type == "MOD":
            return self.compute_wire(expr.children[0]) % self.compute_wire(expr.children[1])
        elif expr.data.type == "FROM":
            return self.compute_wire(expr.children[0])._from()
        elif expr.data.type == "AFTER":
            return self.compute_wire(expr.children[0])._after()
        elif expr.data.type == "UNTIL":
            return self.compute_wire(expr.children[0])._until()
        elif expr.data.type == "BEFORE":
            return self.compute_wire(expr.children[0])._before()
        elif expr.data.type == "NEXT":
            return self.compute_wire(expr.children[0])._next()
        elif expr.data.type == "PREV":
            return self.compute_wire(expr.children[0])._prev()
        elif expr.data.type == "ACC":
            return self.compute_wire(expr.children[0])._acc()
        elif expr.data.type == "CONST":
            return Wire(name=expr.data, width=0, data=[int(expr.children[0])])
        elif expr.data.type == "TIME":
            return Wire(name=f"t_{expr.data}", width=1, data=[0] * int(expr.children[0]) + [1, 0])

    def compute_limits(self, start_expr, end_expr):
        try:
            start = self.compute_wire(LimitExpression(start_expr).tree).data.index(1)
        except ValueError:
            start = 0
        try:
            end = self.compute_wire(LimitExpression(end_expr).tree).data[start:].index(1) + start
        except ValueError:
            end = self.length()
        return (start, end)
