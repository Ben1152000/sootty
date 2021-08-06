
class Wire:

    def __init__(self, name, width=1, data=[]):
        self.name = name
        self.width = width
        self.data = data
    
    @staticmethod
    def parse_vcd(vcd_data):
        wiredata = []
        source_data = sorted(vcd_data["data"])
        source_dict = dict(source_data)
        time = 0
        end = source_data[-1][0] if len(source_data) else 0
        while time <= end:
            if time in source_dict:
                wiredata.append(source_dict[time])
            elif time > 0:
                wiredata.append(wiredata[-1])
            else:
                wiredata.append('x')
            time += 1
        
        return Wire(
            name=vcd_data["name"],
            width=vcd_data["type"]["width"],
            data=wiredata
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
