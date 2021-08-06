
class Visualizer:

    TOP_MARGIN = 30
    LEFT_MARGIN = 30
    DATA_WIDTH = 50
    WIRE_HEIGHT = 20
    WIRE_MARGIN = 10
    TRANS_LENGTH = 5

    def wiretrace_to_svg(self, wiretrace, start=0, length=1):
        width = 2 * self.LEFT_MARGIN + (length + 1) * self.DATA_WIDTH
        height = 2 * self.TOP_MARGIN + sum([sum([1 for wire in wiregroup.wires]) for wiregroup in wiretrace.wiregroups]) * (self.WIRE_HEIGHT + self.WIRE_MARGIN)
        svg = f'<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg">' \
              f'<rect x="0" y="0" width="{width}" height="{height}" fill="white" />'
        for wiregroup in wiretrace.wiregroups:
            svg += self.wiregroup_to_svg(
                wiregroup = wiregroup, 
                left = self.LEFT_MARGIN,
                top = self.TOP_MARGIN,
                start = start,
                length = length)
        svg += '</svg>'
        return svg

    def wiregroup_to_svg(self, wiregroup, left, top, start, length):
        svg = ''
        for index in range(len(wiregroup.wires)):
            svg += self.wire_to_svg(
                wiregroup.wires[index],
                left = left,
                top = top + (index * (self.WIRE_HEIGHT + self.WIRE_MARGIN)),
                start = start,
                length = length)
        return svg

    def wire_to_svg(self, wire, left, top, start, length):
        svg = f'<text x="{left}" y="{top + 15}" class="small">{wire.name}</text>'
        for index in range(start, start + length):
            svg += self.value_to_svg(
                prev = (wire.data[index - 1] if index > 0 else wire.data[index]) if index < len(wire.data) else wire.data[-1],
                value = wire.data[index] if index < len(wire.data) else wire.data[-1],
                left = left + ((index + 1) * self.DATA_WIDTH),
                top = top,
                initial = (index == start))
        return svg

    def value_to_svg(self, prev, value, left, top, initial=False):
        prev_type = 'low' if prev == '0' else ('high' if prev == '1' else 'data')
        value_type = 'low' if value == '0' else ('high' if value == '1' else 'data')
        is_transitioning = (prev != value)

        if prev_type == 'low' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'low' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + self.TRANS_LENGTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top + self.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.WIRE_HEIGHT / 2}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'low' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top + self.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.WIRE_HEIGHT / 2}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'high' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + self.TRANS_LENGTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.WIRE_HEIGHT / 2}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'high' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'high' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.WIRE_HEIGHT / 2}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'low':
            return f'<line x1="{left}" x2="{left + self.TRANS_LENGTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'high':
            return f'<line x1="{left}" x2="{left + self.TRANS_LENGTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top + self.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'data' and not is_transitioning and not initial:
            return f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />'
        elif prev_type == 'data' and value_type == 'data':
            return f'<line x1="{left}" x2="{left + self.TRANS_LENGTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.WIRE_HEIGHT / 2}" x2="{left + self.DATA_WIDTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left}" x2="{left + self.TRANS_LENGTH}" y1="{top + self.WIRE_HEIGHT}" y2="{top + self.WIRE_HEIGHT}" stroke="black" />' \
                   f'<line x1="{left + self.TRANS_LENGTH}" x2="{left + self.WIRE_HEIGHT / 2}" y1="{top + self.WIRE_HEIGHT}" y2="{top}" stroke="black" />' \
                   f'<line x1="{left + self.WIRE_HEIGHT / 2}" x2="{left + self.DATA_WIDTH}" y1="{top}" y2="{top}" stroke="black" />' \
                   f'<text x="{left + 15}" y="{top + 15}" class="small">{value}</text>'
        else:
            return 'ERROR'
