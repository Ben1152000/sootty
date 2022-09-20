from ..exceptions import *
from .wire import Wire


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

    def get_wires(self):
        """Returns a dictionary of all wires of this wiregroup or a list if this wiregroup is the innermost one."""
        if self.groups:
            wires = dict()
            if self.wires:
                wires[self.name] = self.wires
            for group in self.groups:
                wires[group.name] = group.get_wires()
        else:
            wires = self.wires
        return wires
