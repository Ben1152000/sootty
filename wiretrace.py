from limit import LimitExpression

class Wire:

    def __init__(self, name, width=1, data=[]):
        self.name = name
        self.width = width
        self.data = data
    
    @staticmethod
    def str_to_int(data):
        if data[0] == 'b':
            return int(data[1:], 2)
        else:
            return int(data)

    @staticmethod
    def parse_vcd(vcd_data):
        wiredata = []
        source_data = sorted(vcd_data["data"])
        source_dict = dict(source_data)
        time = 0
        end = source_data[-1][0] if len(source_data) else 0
        while time <= end:
            if time in source_dict:
                wiredata.append(Wire.str_to_int(source_dict[time]))
            elif time > 0:
                wiredata.append(wiredata[-1])
            else:
                wiredata.append(None)
            time += 1
        
        return Wire(
            name=vcd_data["name"],
            width=vcd_data["type"]["width"],
            data=wiredata
        )
    
    def __add__(self, other):
        data = []
        length = max(len(self.data), len(other.data))
        for (a, b) in zip(self.data + [self.data[-1]] * (length - len(self.data)), 
                      other.data + [other.data[-1]] * (length - len(other.data))):
            data.append(a + b)
        
        return Wire(
            name="(" + self.name + " + " + other.name + ")",
            width=max(self.width, other.width),
            data=data
        )
    
    def __neg__(self):
        data = []
        for a in self.data:
            data.append(-a)
        
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
            data.append(a & b)
        
        return Wire(
            name="(" + self.name + " & " + other.name + ")",
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
            width=max(self.width, other.width),
            data=data
        )


class WireGroup:

    def __init__(self, name):
        self.name = name
        self.wires = []

    def add_wire(self, wire):
        self.wires.append(wire)
    
    def add_wires(self, wiregroup):
        self.wires += wiregroup.wires

    @staticmethod
    def parse_vcd(vcd_data):
        wiregroup = WireGroup(
            name=vcd_data["name"]
        )
        for child in vcd_data["children"]:
            if "data" in child:
                wiregroup.add_wire(
                    Wire.parse_vcd(child)
                )
            else:
                wiregroup.add_wires(
                    WireGroup.parse_vcd(child)
                )
        return wiregroup

class WireTrace:

    def __init__(self):
        self.wiregroups = []

    def add_wiregroup(self, wiregroup):
        self.wiregroups.append(wiregroup)

    @staticmethod
    def parse_vcd(vcd_data):
        wiretrace = WireTrace()
        for child in vcd_data["children"]:
            wiretrace.add_wiregroup(
                WireGroup.parse_vcd(child)
            )
        return wiretrace

    def length(self):
        limit = 0
        for wiregroup in self.wiregroups:
            for wire in wiregroup.wires:
                limit = max(limit, len(wire.data))
        return limit

    def find_wire(self, name):
        for wiregroup in self.wiregroups:
            for wire in wiregroup.wires:
                if wire.name == name:
                    return wire
    
    def compute_wire(self, expr):
        if expr.data == "wire":
            return self.find_wire(expr.children[0])
        elif expr.data.type == "AND":
            return self.compute_wire(expr.children[0]) & self.compute_wire(expr.children[1])
        elif expr.data.type == "ADD":
            return self.compute_wire(expr.children[0]) + self.compute_wire(expr.children[1])
        elif expr.data.type == "EQ":
            return self.compute_wire(expr.children[0]) == self.compute_wire(expr.children[1])
        elif expr.data.type == "CONST":
            return Wire(name=expr.data, width=0, data=[int(expr.children[0])])

    def compute_limits(self, start_expr: LimitExpression, end_expr: LimitExpression):
        return (self.compute_wire(start_expr.tree).data.index(1), 
            self.compute_wire(end_expr.tree).data.index(1))
