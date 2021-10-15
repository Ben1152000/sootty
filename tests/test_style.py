from sootty import WireTrace, Visualizer, display, SiliconStyle

wiretrace = WireTrace.from_vcd_file("example/example1.vcd")

svg_data = Visualizer(SiliconStyle).to_svg(wiretrace, start=0, length=8)

display(svg_data)