import sys
from itertools import compress, chain

from ..exceptions import *
from .valuechange import ValueChange


class Wire:
    def __init__(self, name, width=1):
        self.name = name
        self._data = ValueChange(width)

    @classmethod
    def from_data(cls, name, data, width=1):
        wire = cls(name=name, width=width)
        for key in compress(
            range(len(data)),
            map(lambda pair: pair[0] != pair[1], zip(chain([None], data), data)),
        ):
            wire[key] = data[key]
        return wire

    def __setitem__(self, key, value):
        self._data[key] = value

    def __getitem__(self, key):
        return self._data.get(key)

    def __delitem__(self, key):
        del self._data[key]  # throws error if not present

    def width(self):
        return self._data.width

    def length(self):
        """Returns the time duration of the wire."""
        return self._data.length()

    def end(self):
        """Returns the final value on the wire"""
        return self._data[self._data.length()]

    def times(self, length=0):
        """Returns a list of times with high value on the wire."""
        return self._data.search(end=max(length, self.length()))

    @classmethod
    def const(cls, value):
        wire = cls(name=f"c_{value}", width=0)
        wire[0] = value
        return wire

    @classmethod
    def time(cls, value):
        wire = cls(name=f"t_{value}", width=1)
        wire[0] = 0
        wire[value] = 1
        wire[value + 1] = 0
        return wire

    def __invert__(self):
        wire = Wire(name="~" + self.name)
        wire._data = self._data.__invert__()
        return wire

    def __neg__(self):
        wire = Wire(name="-" + self.name)
        wire._data = self._data.__invert__()
        return wire

    def __and__(self, other):
        wire = Wire(name="(" + self.name + " & " + other.name + ")")
        wire._data = self._data.__and__(other._data)
        return wire

    def __or__(self, other):
        wire = Wire(name="(" + self.name + " | " + other.name + ")")
        wire._data = self._data.__or__(other._data)
        return wire

    def __xor__(self, other):
        wire = Wire(name="(" + self.name + " ^ " + other.name + ")")
        wire._data = self._data.__xor__(other._data)
        return wire

    def __eq__(self, other):
        wire = Wire(name="(" + self.name + " == " + other.name + ")")
        wire._data = self._data.__eq__(other._data)
        return wire

    def __ne__(self, other):
        wire = Wire(name="(" + self.name + " != " + other.name + ")")
        wire._data = self._data.__ne__(other._data)
        return wire

    def __gt__(self, other):
        wire = Wire(name="(" + self.name + " > " + other.name + ")")
        wire._data = self._data.__gt__(other._data)
        return wire

    def __ge__(self, other):
        wire = Wire(name="(" + self.name + " >= " + other.name + ")")
        wire._data = self._data.__ge__(other._data)
        return wire

    def __lt__(self, other):
        wire = Wire(name="(" + self.name + " < " + other.name + ")")
        wire._data = self._data.__lt__(other._data)
        return wire

    def __le__(self, other):
        wire = Wire(name="(" + self.name + " <= " + other.name + ")")
        wire._data = self._data.__le__(other._data)
        return wire

    def __lshift__(self, other):
        wire = Wire(name="(" + self.name + " << " + other.name + ")")
        wire._data = self._data.__lshift__(other._data)
        return wire

    def __rshift__(self, other):
        wire = Wire(name="(" + self.name + " >> " + other.name + ")")
        wire._data = self._data.__rshift__(other._data)
        return wire

    def __add__(self, other):
        wire = Wire(name="(" + self.name + " + " + other.name + ")")
        wire._data = self._data.__add__(other._data)
        return wire

    def __sub__(self, other):
        wire = Wire(name="(" + self.name + " - " + other.name + ")")
        wire._data = self._data.__sub__(other._data)
        return wire

    def __mod__(self, other):
        wire = Wire(name="(" + self.name + " % " + other.name + ")")
        wire._data = self._data.__mod__(other._data)
        return wire

    def _from(self):
        wire = Wire(name="from " + self.name)
        wire._data = self._data._from()
        return wire

    def _after(self):
        wire = Wire(name="after " + self.name)
        wire._data = self._data._after()
        return wire

    def _until(self):
        wire = Wire(name="until " + self.name)
        wire._data = self._data._until()
        return wire

    def _before(self):
        wire = Wire(name="before " + self.name)
        wire._data = self._data._before()
        return wire

    def _next(self, amt=1):
        wire = Wire(name="next " + self.name)
        wire._data = self._data._next(amt)
        return wire

    def _prev(self, amt=1):
        wire = Wire(name="prev " + self.name)
        wire._data = self._data._prev(amt)
        return wire

    def _acc(self):
        wire = Wire(name="acc " + self.name)
        wire._data = self._data._acc()
        return wire
