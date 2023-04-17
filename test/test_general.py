import re, sys
from subprocess import call, Popen, STDOUT, PIPE
from sootty import WireTrace, Visualizer, VectorImage, Style

import unittest


class TestGeneral(unittest.TestCase):

    def test_svg_output(self):
        wiretrace = WireTrace.from_vcd("example/example1.vcd")

        assert type(wiretrace) == WireTrace

        image = Visualizer().to_svg(wiretrace, start=0, length=8)

        pattern = r"(?:<\?xml\b[^>]*>[^<]*)?(?:<!--.*?-->[^<]*)*(?:<svg|<!DOCTYPE svg)\b"
        prog = re.compile(pattern, re.DOTALL)
        assert prog.match(image.source) is not None

        image.display()


    def test_scope(self):
        wiretrace = WireTrace().from_vcd("example/example2.vcd")
        assert type(wiretrace) == WireTrace

        # def print_group(group, depth=0):
        #     for wire in group.wires:
        #         print('\t' * depth + wire.name)
        #     for group in group.groups:
        #         print('\t' * depth + group.name + ':')
        #         print_group(group, depth + 1)

        # print_group(wiretrace.root)

        assert wiretrace.num_wires() == 26
        image = Visualizer().to_svg(wiretrace, start=0, length=8)
        image.display()


if __name__ == "__main__":
    unittest.main()
