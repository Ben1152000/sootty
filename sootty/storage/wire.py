import sys

from ..exceptions import *
from .valuechange import ValueChange

class Wire:

    def __init__(self, name, width=1):
        self.name = name
        self.data = ValueChange(self.width)

    def __setitem__(self, key, value):
        self.data[key] = value

    def __getitem__(self, key):
        return self.data.get(key)

    def __delitem__(self, key):
        del self.data[key]  # throws error if not present

    def width(self):
        return self.data.width

    def length(self):
        """Returns the time duration of the wire."""
        return self.data.length()

    def times(self, length=0):
        """Returns a list of times with high value on the wire."""
        return self.data.search(end=max(length, self.length()))

    def __invert__(self):
        wire = Wire(name="~" + self.name)
        wire.data = self.data.__invert__()
        return wire

    def __neg__(self):
        wire = Wire(name="-" + self.name)
        wire.data = self.data.__invert__()
        return wire
    
    def __and__(self, other):
        wire = Wire(name="(" + self.name + " & " + other.name + ")")
        wire.data = self.data.__and__(other)
        return wire

    def __or__(self, other):
        wire = Wire(name="(" + self.name + " | " + other.name + ")")
        wire.data = self.data.__or__(other)
        return wire

    def __xor__(self, other):
        wire = Wire(name="(" + self.name + " ^ " + other.name + ")")
        wire.data = self.data.__xor__(other)
        return wire

    def __eq__(self, other):
        wire = Wire(name="(" + self.name + " == " + other.name + ")")
        wire.data = self.data.__eq__(other)
        return wire

    def __ne__(self, other):
        wire = Wire(name="(" + self.name + " != " + other.name + ")")
        wire.data = self.data.__ne__(other)
        return wire

    def __gt__(self, other):
        wire = Wire(name="(" + self.name + " > " + other.name + ")")
        wire.data = self.data.__gt__(other)
        return wire

    def __ge__(self, other):
        wire = Wire(name="(" + self.name + " >= " + other.name + ")")
        wire.data = self.data.__ge__(other)
        return wire

    def __lt__(self, other):
        wire = Wire(name="(" + self.name + " < " + other.name + ")")
        wire.data = self.data.__lt__(other)
        return wire

    def __le__(self, other):
        wire = Wire(name="(" + self.name + " <= " + other.name + ")")
        wire.data = self.data.__le__(other)
        return wire

    def __lshift__(self, other):
        wire = Wire(name="(" + self.name + " << " + other.name + ")")
        wire.data = self.data.__lshift__(other)
        return wire

    def __rshift__(self, other):
        wire = Wire(name="(" + self.name + " >> " + other.name + ")")
        wire.data = self.data.__rshift__(other)
        return wire

    def __add__(self, other):
        wire = Wire(name="(" + self.name + " + " + other.name + ")")
        wire.data = self.data.__add__(other)
        return wire
  
    def __sub__(self, other):
        wire = Wire(name="(" + self.name + " - " + other.name + ")")
        wire.data = self.data.__sub__(other)
        return wire
  
    def __mod__(self, other):
        wire = Wire(name="(" + self.name + " % " + other.name + ")")
        wire.data = self.data.__mod__(other)
        return wire
  
    def _from(self):
        wire = Wire(name="from " + self.name)
        wire.data = self.data._from()
        return wire

    def _after(self):
        wire = Wire(name="after " + self.name)
        wire.data = self.data._after()
        return wire

    def _until(self):
        wire = Wire(name="until " + self.name)
        wire.data = self.data._until()
        return wire

    def _before(self):
        wire = Wire(name="before " + self.name)
        wire.data = self.data._before()
        return wire

    def _next(self, amt=1):
        wire = Wire(name="next " + self.name)
        wire.data = self.data._next(amt)
        return wire

    def _prev(self, amt=1):
        wire = Wire(name="prev " + self.name)
        wire.data = self.data._prev(amt)
        return wire

    def _acc(self):
        wire = Wire(name="acc " + self.name)
        wire.data = self.data._acc()
        return wire
