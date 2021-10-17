from sootty import WireTrace, Visualizer, Style

wiretrace = WireTrace.from_vcd_file("example/example1.vcd")

Visualizer(Style.Silicon).to_svg(wiretrace, start=0, length=8).display()

Visualizer(Style.Dark).to_svg(wiretrace, start=0, length=8).display()

Visualizer(Style.Light).to_svg(wiretrace, start=0, length=8).display()

print("Success!")