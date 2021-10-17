import sys

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
        LINE_COLOR = "#FFFFFF"
        TEXT_COLOR = "#FFFFFF"
        BKGD_COLOR = "#000000"

    class Dark(Default):
        pass

    class Light(Default):
        LINE_COLOR = "#000000"
        TEXT_COLOR = "#000000"
        BKGD_COLOR = "#FFFFFF"

    class Silicon(Default):
        LINE_COLOR = "#B0B0B0"
        TEXT_COLOR = "#30FF30"
        BKGD_COLOR = "#003000"


class Visualizer:
    """Converter for wiretrace objects to a svg vector image format."""

    def __init__(self, style=Style.Default):
        """Optionally pass in a style class to control how the visualizer looks."""
        self.style = style

    def to_svg(self, wiretrace, start=0, length=1, wires=set()):
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
                prev = bool(prev) if wire.width == 1 else prev,
                value = bool(value) if wire.width == 1 else value,
                left = left + ((index - start) * self.style.DATA_WIDTH) + self.style.TEXT_WIDTH,
                top = top,
                initial = (index == start))
        return svg

    def _value_to_svg(self, prev, value, left, top, initial=False):
        prev_type = 'low' if prev is False else ('high' if prev is True else 'data')
        value_type = 'low' if value is False else ('high' if value is True else 'data')
        is_transitioning = (prev != value)

        if prev_type == 'low' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'low' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + self.style.TRANS_START}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'low' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'high' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + self.style.TRANS_START}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS}" y1="{top}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START + self.style.TRANS_WIDTH * self.style.BLOCK_TRANS}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'high' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'high' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" y1="{top}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'data' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + self.style.TRANS_START}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" y1="{top}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'data' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + self.style.TRANS_START}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'data' and value_type == 'data' and not is_transitioning and not initial:
            return f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />'
        elif prev_type == 'data' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + self.style.TRANS_START}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" y1="{top}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" x2="{left + self.style.DATA_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left}" x2="{left + self.style.TRANS_START}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top + self.style.WIRE_HEIGHT}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START}" x2="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" y1="{top + self.style.WIRE_HEIGHT}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<line x1="{left + self.style.TRANS_START + self.style.TRANS_WIDTH}" x2="{left + self.style.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="{self.style.LINE_COLOR}" />' \
                   f'<text x="{left + self.style.TRANS_START + self.style.TRANS_WIDTH + 5}" y="{top + (self.style.WIRE_HEIGHT + self.style.WIRE_MARGIN) / 2}" class="small" fill="{self.style.TEXT_COLOR}">{"X" if value == None else hex(value)}</text>'
        else:
            raise SoottyInternalError("Invalid wire transition, unable to visualize.")
