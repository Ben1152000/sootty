from sootty import WireTrace, Visualizer

trace = WireTrace.from_vcd('example/example2.vcd')

# for group in trace.wiregroups:
#     for wire in group.wires:
#         print(wire.data)

svg = Visualizer().to_svg(trace)

print(svg)

# svg.display()

# trace = WireTrace.from_vcd('example/example2.vcd')

# Visualizer().to_svg(trace).display()