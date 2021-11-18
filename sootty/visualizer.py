import sys
from enum import Enum

from .display import VectorImage
from .exceptions import SoottyInternalError


class Style:
    """Container class for visualizer style settings."""

    class Default():
        TOP_MARGIN = 15
        LEFT_MARGIN = 15
        TEXT_WIDTH = 100
        DATA_WIDTH = 50
        WIRE_HEIGHT = 20
        WIRE_MARGIN = 10
        TRANS_START = 5
        TRANS_WIDTH = 5
        BLOCK_TRANS = False
        LINE_COLOR = "#FFFFFF" #line color now needs to be its own class (?) depending on wires and variables
        LINE_COLOR_HIGH = "#00FF00"
        LINE_COLOR_LOW = "#3DB8B8"
        LINE_COLOR_Z = "#FFFF00"
        LINE_COLOR_X = "#FF0000"
        LINE_COLOR_DATA = "#3DB8B8"
        TEXT_COLOR = "#FFFFFF"
        BKGD_COLOR = "#000000"
        #wires going from 0 and 1 are two different colors, x variable is red rectangle, z variable is yellow

    class Dark(Default):
        pass

    class Light(Default):
        LINE_COLOR = "#000000"
        LINE_COLOR_HIGH = "#2e9947"
        LINE_COLOR_LOW = "#1b7280"
        LINE_COLOR_Z = "#b5a600"
        LINE_COLOR_X = "#8a0000"
        TEXT_COLOR = "#000000"
        BKGD_COLOR = "#FFFFFF"

    class Silicon(Default):
        LINE_COLOR = "#000000"
        LINE_COLOR_HIGH = "#FFFFFF"
        LINE_COLOR_LOW = "#a8acad"
        LINE_COLOR_Z = "#7a5b1b"
        LINE_COLOR_X = "#faf6bb"
        #TEXT_COLOR = "#30FF30"
        TEXT_COLOR = "#FFFFFF"
        #BKGD_COLOR = "#003000"
        BKGD_COLOR = "#2b5e2b"


class Visualizer:
    """Converter for wiretrace objects to a svg vector image format."""

    def __init__(self, style=Style.Default):
        """Optionally pass in a style class to control how the visualizer looks."""
        self.style = style

    def to_svg(self, wiretrace, start=0, length=None, wires=set()):
        if length is None:
            length = wiretrace.length()
        """Converts the provided wiretrace object to a VectorImage object (svg)."""
        return VectorImage(self._wiretrace_to_svg(wiretrace, start, length, wires))

    def _wiretrace_to_svg(self, wiretrace, start, length, wires=None):
        width = 2 * self.style.LEFT_MARGIN + self.style.TEXT_WIDTH + length * self.style.DATA_WIDTH
        height = 2 * self.style.TOP_MARGIN + (len(wires) + 1) * (self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN) - self.style.WIRE_MARGIN
        if len(wires) == 0:
            wires = None
            height += sum([sum([1 for wire in wiregroup.wires]) for wiregroup in wiretrace.wiregroups]) * (self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN)
        
        svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">' \
              f'<rect x="0" y="0" width="{width}" height="{height}" fill="{self.style.BKGD_COLOR}" />'
        
        lines = 1
        svg += self._timestamps_to_svg(
            left = self.style.LEFT_MARGIN + self.style.TEXT_WIDTH, 
            top = self.style.TOP_MARGIN,
            start = start,
            length = length)
        
        for wiregroup in wiretrace.wiregroups:
            svg += self._wiregroup_to_svg(
                wiregroup = wiregroup, 
                left = self.style.LEFT_MARGIN,
                top = self.style.TOP_MARGIN + self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN,
                start = start,
                length = length,
                wires = wires)
        svg += '</svg>'
        return svg

    def _timestamps_to_svg(self, left, top, start, length):
        svg = ''
        for index in range(start, start + length):
            svg += f'<text x="{left + (index - start + 1/2) * self.style.DATA_WIDTH}" y="{top + (self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN) / 2}" class="small" fill="{self.style.TEXT_COLOR}" text-anchor="middle">{index}</text>'
        return svg

    def _wiregroup_to_svg(self, wiregroup, left, top, start, length, wires=None):
        svg = ''
        index = 0
        for wire in wiregroup.wires:
            if wires == None or wire.name in wires:
                svg += self._wire_to_svg(
                    wire,
                    left = left,
                    top = top + (index * (self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN)),
                    start = start,
                    length = length)
                if wires:
                    wires.remove(wire.name)
                index += 1
        return svg

    def _wire_to_svg(self, wire, left, top, start, length):
        svg = f'<text x="{left}" y="{top + 15}" class="small" fill="{self.style.TEXT_COLOR}">{wire.name}</text>'
        for index in range(start, start + length):
            prev = (wire.data[index - 1] if index > 0 else wire.data[index]) if index < len(wire.data) else wire.data[-1]
            value = wire.data[index] if index < len(wire.data) else wire.data[-1]
            svg += self._value_to_svg(
                prev = prev,
                value = value,
                width = wire.width,
                left = left + ((index - start) * self.style.DATA_WIDTH) + self.style.TEXT_WIDTH,
                top = top,
                initial = (index == start))
        return svg

    class ValueType(Enum):
        LOW = 0
        HIGH = 1
        DATA = 2
        X = 3
        Z = 4

    @staticmethod
    def type_from_value(value, width=1):
        if width == 1:
            if value in (0, '0'):
                return Visualizer.ValueType.LOW
            elif value in (1, '1'):
                return Visualizer.ValueType.HIGH
            elif value in ('x', 'X'):
                return Visualizer.ValueType.X
            elif value in ('z', 'Z'):
                return Visualizer.ValueType.Z
            else:
                raise SoottyInternalError(f'Invalid wire value, unable to visualize: {value}')
        else:
            if 'x' in str(value):
                return Visualizer.ValueType.X
            else:
                return Visualizer.ValueType.DATA

    def _value_to_svg(self, prev, value, width, left, top, initial=False):
        # deduce types from wire width and value:
        prev_type = Visualizer.type_from_value(prev, width)
        value_type = Visualizer.type_from_value(value, width)
        is_transitioning = (prev != value)

        # The following code builds a list of svg objects depending on the 
        # current and previous value of the wire.
        shapes = []
        if prev_type is Visualizer.ValueType.LOW and value_type is Visualizer.ValueType.LOW:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_LOW,
            })
        elif prev_type is Visualizer.ValueType.LOW and value_type is Visualizer.ValueType.HIGH:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_LOW,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top,
                'stroke': self.style.LINE_COLOR_HIGH,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_HIGH,
            })
        elif prev_type is Visualizer.ValueType.HIGH and value_type is Visualizer.ValueType.LOW:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_HIGH,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS,
                'y1': top,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_LOW,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_LOW,
            })
        elif prev_type is Visualizer.ValueType.HIGH and value_type is Visualizer.ValueType.HIGH:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_HIGH,
            })
        elif prev_type is Visualizer.ValueType.LOW and value_type is Visualizer.ValueType.DATA:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
        elif prev_type is Visualizer.ValueType.HIGH and value_type is Visualizer.ValueType.DATA:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
        elif prev_type is Visualizer.ValueType.DATA and value_type is Visualizer.ValueType.LOW:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_LOW,
            })
        elif prev_type is Visualizer.ValueType.DATA and value_type is Visualizer.ValueType.HIGH:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_HIGH,
            })
        elif prev_type is Visualizer.ValueType.DATA and value_type is Visualizer.ValueType.DATA and not is_transitioning and not initial:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
        elif prev_type is Visualizer.ValueType.DATA and value_type is Visualizer.ValueType.DATA:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.TRANS_START,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START,
                'x2': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'line',
                'x1': left + self.style.TRANS_START + self.style.TRANS_WIDTH,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_DATA,
            })
            shapes.append({
                'name': 'text',
                'x': left + self.style.TRANS_START + self.style.TRANS_WIDTH + 5,  # TODO: generalize formula
                'y': top + (self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN) / 2,
                'class': 'small',
                'fill': self.style.TEXT_COLOR,
                'content': value
            })
        # TODO: figure out how to display X values in svg:
        elif prev_type is Visualizer.ValueType.LOW and value_type is Visualizer.ValueType.X:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.HIGH and value_type is Visualizer.ValueType.X:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.DATA and value_type is Visualizer.ValueType.X:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.X and value_type is Visualizer.ValueType.LOW:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.X and value_type is Visualizer.ValueType.HIGH:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.X and value_type is Visualizer.ValueType.DATA:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.X and value_type is Visualizer.ValueType.X:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        # TODO: figure out how to display Z values in svg:
        elif prev_type is Visualizer.ValueType.LOW and value_type is Visualizer.ValueType.Z:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.HIGH and value_type is Visualizer.ValueType.Z:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.DATA and value_type is Visualizer.ValueType.Z:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_X,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_X,
            })
        elif prev_type is Visualizer.ValueType.X and value_type is Visualizer.ValueType.Z:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.Z and value_type is Visualizer.ValueType.LOW:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.Z and value_type is Visualizer.ValueType.HIGH:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.Z and value_type is Visualizer.ValueType.DATA:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.Z and value_type is Visualizer.ValueType.X:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        elif prev_type is Visualizer.ValueType.Z and value_type is Visualizer.ValueType.Z:
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top + self.style.WIRE_HEIGHT,
                'y2': top + self.style.WIRE_HEIGHT,
                'stroke': self.style.LINE_COLOR_Z,
            })
            shapes.append({
                'name': 'line',
                'x1': left,
                'x2': left + self.style.DATA_WIDTH,
                'y1': top,
                'y2': top,
                'stroke': self.style.LINE_COLOR_Z,
            })
        else:
            raise SoottyInternalError(f"Invalid wire transition, unable to visualize: {prev_type} to {value_type}")
        
        svg_data = ''
        for shape in shapes:
            start_tag = '<' + str(shape['name'])
            end_tag = ' />'
            for prop in shape:
                if prop == 'content':
                    end_tag = '>' + str(shape['content']) + '</' + str(shape['name']) + '>'
                elif prop != 'name':
                    start_tag += ' ' + prop + '="' + str(shape[prop]) + '"'
            svg_data += start_tag + end_tag
        return svg_data
