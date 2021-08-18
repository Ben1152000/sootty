import sys
class Visualizer:

    TOP_MARGIN = 15
    LEFT_MARGIN = 15
    TEXT_WIDTH = 100
    DATA_WIDTH = 50
    WIRE_HEIGHT = 20
    WIRE_MARGIN = 10
    TRANS_LENGTH = 5

    @staticmethod
    def wiretrace_to_svg(wiretrace, start=0, length=1, wires=set()):
        width = 2 * Visualizer.LEFT_MARGIN + Visualizer.TEXT_WIDTH + length * Visualizer.DATA_WIDTH
        height = 2 * Visualizer.TOP_MARGIN + len(wires) * (Visualizer.WIRE_HEIGHT + Visualizer.WIRE_MARGIN) - Visualizer.WIRE_MARGIN
        if len(wires) == 0:
            wires = None
            height += sum([sum([1 for wire in wiregroup.wires]) for wiregroup in wiretrace.wiregroups]) * (Visualizer.WIRE_HEIGHT + Visualizer.WIRE_MARGIN)
        
        svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">' \
              f'<rect x="0" y="0" width="{width}" height="{height}" fill="white" />'
        
        for wiregroup in wiretrace.wiregroups:
            svg += Visualizer.wiregroup_to_svg(
                wiregroup = wiregroup, 
                left = Visualizer.LEFT_MARGIN,
                top = Visualizer.TOP_MARGIN,
                start = start,
                length = length,
                wires = wires)
        svg += '</svg>'
        return svg

    @staticmethod
    def wiregroup_to_svg(wiregroup, left, top, start, length, wires=None):
        svg = ''
        index = 0
        for wire in wiregroup.wires:
            if wires == None or wire.name in wires:
                svg += Visualizer.wire_to_svg(
                    wire,
                    left = left,
                    top = top + (index * (Visualizer.WIRE_HEIGHT + Visualizer.WIRE_MARGIN)),
                    start = start,
                    length = length)
                if wires:
                    wires.remove(wire.name)
                index += 1
        return svg

    @staticmethod
    def wire_to_svg(wire, left, top, start, length):
        svg = f'<text x="{left}" y="{top + 15}" class="small">{wire.name}</text>'
        for index in range(start, start + length):
            prev = (wire.data[index - 1] if index > 0 else wire.data[index]) if index < len(wire.data) else wire.data[-1]
            value = wire.data[index] if index < len(wire.data) else wire.data[-1]
            svg += Visualizer.value_to_svg(
                prev = bool(prev) if wire.width == 1 else prev,
                value = bool(value) if wire.width == 1 else value,
                left = left + ((index - start) * Visualizer.DATA_WIDTH) + Visualizer.TEXT_WIDTH,
                top = top,
                initial = (index == start))
        return svg

    @staticmethod
    def value_to_svg(prev, value, left, top, initial=False):
        prev_type = 'low' if prev is False else ('high' if prev is True else 'data')
        value_type = 'low' if value is False else ('high' if value is True else 'data')
        is_transitioning = (prev != value)

        if prev_type == 'low' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'low' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + Visualizer.TRANS_LENGTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.WIRE_HEIGHT / 2}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'low' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.WIRE_HEIGHT / 2}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'high' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + Visualizer.TRANS_LENGTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.WIRE_HEIGHT / 2}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'high' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'high' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.WIRE_HEIGHT / 2}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + Visualizer.TRANS_LENGTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + Visualizer.TRANS_LENGTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'data' and not is_transitioning and not initial:
            return f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + Visualizer.TRANS_LENGTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.WIRE_HEIGHT / 2}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + Visualizer.TRANS_LENGTH}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top + Visualizer.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.TRANS_LENGTH}" x2="{left + Visualizer.WIRE_HEIGHT / 2}" y1="{top + Visualizer.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + Visualizer.WIRE_HEIGHT / 2}" x2="{left + Visualizer.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<text x="{left + 15}" y="{top + 15}" class="small">{"X" if value == None else hex(value)}</text>'
        else:
            return 'ERROR'
