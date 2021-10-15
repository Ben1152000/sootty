import re, sys
from subprocess import call, Popen, STDOUT, PIPE

from sootty import WireTrace, Visualizer, display

wiretrace = WireTrace.from_vcd_file("example/example1.vcd")

assert type(wiretrace) == WireTrace

svg_data = Visualizer().to_svg(wiretrace, start=0, length=8)

pattern = r'(?:<\?xml\b[^>]*>[^<]*)?(?:<!--.*?-->[^<]*)*(?:<svg|<!DOCTYPE svg)\b'
prog = re.compile(pattern, re.DOTALL)
assert prog.match(svg_data) is not None

display(svg_data)

print("Success!")
