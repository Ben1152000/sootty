import polars as pl

from ..exceptions import *
from .wire import Wire


class WireGroup:
    def __init__(self, name: str):
        self.name = name
        self.groups = []
        self.wires = []

        self.groups_df = pl.DataFrame()
        self.wires_df = pl.DataFrame([], schema={'name':pl.String, 'time': pl.Int64, 'value': pl.Int64, 'length': pl.Int64, 'width': pl.Int64})

    def add_wire(self, wire):
        self.wires.append(wire)

        # this prints out null because time doesn't exist in the value change dictionary yet

        # print(wire.__getitem__('time')) 
        temp_wire_df = pl.DataFrame({
            'name': wire.name,
            'time': wire.__getitem__('time'),
            'value': wire.__getitem__('value'),
            'length': wire.length(),
            'width': wire.width(),
        })
        self.wires_df.extend(temp_wire_df)
        print(self.wires_df)

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
        """dataframe version"""
        find_wires_df = self.wires_df.filter(pl.col("name") == name)
        # print(find_wires_df)

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
