import sys

from ..exceptions import *


class Wire:

    def __init__(self, name, width=1, data=None):
        self.name = name
        self.width = width
        self.data = list() if data is None else data
    
    def length(self):
        """Returns the time duration of the wire."""
        return len(self.data)

    def times(self, length=0):
        """Returns a list of times with high value on the wire."""
        times = []
        for time in range(len(self.data)):
            value = self.data[time]
            if type(value) is int and value > 0:
                times.append(time)
        # pad to desired length:
        if (len(self.data) - 1) in times:
            for time in range(len(self.data), length):
                times.append(time)
        return times

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
