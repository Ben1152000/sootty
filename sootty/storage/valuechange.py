import sys
from vcd.reader import *
from itertools import islice
from sortedcontainers import SortedDict, SortedList, SortedSet
# from ..exceptions import *


class ValueChange(SortedDict):
    
    def __init__(self, width=1):
        super().__init__(self)
        self.width = width

    def get(self, key):
        if key in self:
            return self[key]
        if len(self) < 1 or key < next(self.irange()):
            return None
        return self[next(islice(self.irange(maximum=key, reverse=True), 1))]

    def length(self):
        """Returns the time duration of the wire."""
        return next(self.irange(reverse=True))

    def search(self, value, start=None, end=None):
        """Returns a list of times with a specified value on the wire, between start and end times."""
        indices = []
        prev = None
        for i in self.irange(minimum=start, maximum=end):
            if prev is not None:
                indices.extend(range(prev + 1, i))
            if self[i] == value:
                indices.append(i)
                prev = i
            else:
                prev = None
        if prev is not None and end is not None and end > prev:
            indices.extend(range(prev + 1, end))
        return indices

    def __invert__(self):
        data = ValueChange(width=self.width)
        for key in self:
            data[key] = None if self[key] == None else (~self[key] & (2 << self.width - 1) - 1)
        return data

    def __neg__(self):
        data = ValueChange(width=self.width)
        for key in self:
            data[key] = None if self[key] == None else (-self[key])
        return data

    def _binop(self, other, binop, width):
        data = ValueChange(width=width)
        keys = SortedSet()
        keys.update(self.keys())
        keys.update(other.keys())
        values = [None, None, None]
        for key in keys:
            if key in self:
                values[0] = self[key]
            if key in other:
                values[1] = other[key]
            reduced = None if (values[0] is None or values[1] is None) else binop(values[0], values[1])
            if reduced != values[2]:
                values[2] = reduced
                data[key] = reduced
        return data

    def __and__(self, other):
        return self._binop(other, lambda x, y: x & y, max(self.width, other.width))

    def __or__(self, other):
        return self._binop(other, lambda x, y: x | y, max(self.width, other.width))

    def __xor__(self, other):
        return self._binop(other, lambda x, y: x ^ y, max(self.width, other.width))

    def __eq__(self, other):
        return self._binop(other, lambda x, y: int(x == y), 1)

    def __ne__(self, other):
        return self._binop(other, lambda x, y: int(x != y), 1)

    def __gt__(self, other):
        return self._binop(other, lambda x, y: int(x > y), 1)

    def __ge__(self, other):
        return self._binop(other, lambda x, y: int(x >= y), 1)

    def __lt__(self, other):
        return self._binop(other, lambda x, y: int(x < y), 1)

    def __le__(self, other):
        return self._binop(other, lambda x, y: int(x <= y), 1)

    def __lshift__(self, other):
        return self._binop(other, lambda x, y: int(x << y), self.width)

    def __rshift__(self, other):
        return self._binop(other, lambda x, y: int(x >> y), self.width)

    def __add__(self, other):
        return self._binop(other, lambda x, y: x + y, max(self.width, other.width) + 1)

    def __sub__(self, other):
        return self._binop(other, lambda x, y: x - y, max(self.width, other.width) + 1)
    
    def __mod__(self, other):
        return self._binop(other, lambda x, y: x % y, self.width)
    
    def _from(self):
        data = ValueChange(width=1)
        data[0] = 0
        for key in self:
            if self[key]:
                data[key] = 1
                break
        return data

    def _after(self):
        data = ValueChange(width=1)
        data[0] = 0
        for key in self:
            if self[key]:
                data[key + 1] = 1
                break
        return data

    def _until(self):
        data = ValueChange(width=1)
        data[0] = 1
        for key in self:
            if self[key]:
                data[key + 1] = 0
                break
        return data
    
    def _before(self):
        data = ValueChange(width=1)
        data[0] = 1
        for key in self:
            if self[key]:
                data[key] = 0
                break
        return data

    def _next(self, amt=1):
        data = ValueChange(width=self.width)
        data[0] = self.get(amt)
        for key in self.irange(minimum=amt):
            data[key - 1] = self[key]
        return data

    def _prev(self, amt=1):
        data = ValueChange(width=self.width)
        for key in self:
            data[key + 1] = self[key]
        return data

    def _acc(self):
        data = ValueChange(width=0)
        counter = 0
        data[0] = counter
        state = True
        for key in self:
            if self[key] and not state:
                state = True
                counter += 1
                data[key] = counter
            elif not self[key] and state:
                state = False
        return data
    
if __name__ == "__main__":
    vc = ValueChange(width=2)
    vc[0] = 2
    vc[1] = 2
    vc[2] = 3
    vc[9] = 1
    vc[12] = 3
    print(vc)
    # print(vc.get(0))
    # print(vc.search(True, end = 20))
    vc2 = ValueChange(width=2)
    vc2[0] = 1
    vc2[1] = 0
    vc2[6] = 1
    vc2[9] = 0
    vc2[10] = 1
    print(vc2)
    print(vc & vc2)
    print(vc2._before())
