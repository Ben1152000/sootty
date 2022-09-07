import sys

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
        """Returns a dictionary of all wire names of this wiregroup or a list if this wiregroup is the innermost one."""
        if self.groups:
            names = dict()
            if self.wires:
                names[self.name] = list()
                for wire in self.wires:
                    names[self.name].append(wire.name)
            for group in self.groups:
                names[group.name] = group.get_names()
        else:
            names = list()
            for wire in self.wires:
                names.append(wire.name)
        return names
