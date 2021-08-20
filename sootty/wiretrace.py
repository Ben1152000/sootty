import json
from pyDigitalWaveTools.vcd.parser import VcdParser

from .display import display
from .limits import LimitExpression
from .visualizer import Visualizer

class TraceError(Exception):
    """ Raised on any user-facing error in this module. """
    pass

class Wire:

    def __init__(self, name, width=1, data=[]):
        self.name = name
        self.width = width
        self.data = data
    
    @staticmethod
    def _to_int(data):
        if data[0] == 'b':
            try:
                return int(data[1:], 2)
            except ValueError:
                return None
        else:
            try:
                return int(data)
            except ValueError:
                return None

    @staticmethod
    def from_vcd(vcd_data, base_name=""):
        wiredata = []
        source_data = sorted(vcd_data["data"])
        source_dict = dict(source_data)
        time = 0
        end = source_data[-1][0] if len(source_data) else 0
        while time <= end:
            if time in source_dict:
                wiredata.append(Wire._to_int(source_dict[time]))
            elif time > 0:
                wiredata.append(wiredata[-1])
            else:
                wiredata.append(None)
            time += 1
        
        return Wire(
            name=base_name + ('.' if len(base_name) else "") + vcd_data["name"],
            width=vcd_data["type"]["width"],
            data=wiredata
        )

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

    @staticmethod
    def from_vcd(vcd_data, base_name=None):
        name = "" if base_name == None else (base_name + ('.' if len(base_name) else "") + vcd_data["name"])
        wiregroup = WireGroup(
            name=vcd_data["name"] if len(name) == 0 else name
        )
        for child in vcd_data["children"]:
            if "data" in child:
                wiregroup.add_wire(
                    Wire.from_vcd(child, name)
                )
            else:
                wiregroup.add_wires(
                    WireGroup.from_vcd(child, name)
                )
        return wiregroup

class WireTrace:

    def __init__(self):
        self.wiregroups = []

    def add_wiregroup(self, wiregroup):
        self.wiregroups.append(wiregroup)

    @staticmethod
    def read_vcd(filename):
        with open(filename) as vcd_file:
            vcd = VcdParser()
            vcd.parse(vcd_file)
            return vcd.scope.toJson()  # dump json here for debugging
        
    @staticmethod
    def from_vcd_file(filename):
        vcd_data = WireTrace.read_vcd(filename)  # Read vcd data from file
        wiretrace = WireTrace()
        for child in vcd_data["children"]:
            wiretrace.add_wiregroup(
                WireGroup.from_vcd(child)
            )
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
        raise TraceError(f"Wire '{name}' does not exist.")
    
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

    def to_svg(self, start=0, length=1, wires=set()):
        return Visualizer.wiretrace_to_svg(self, start, length, wires)

    def display(self, start=0, length=1, wires=set()):
        display(self.to_svg(start, length, wires))