import pyrtl
from sootty import WireTrace, Visualizer

import unittest


class TestWires(unittest.TestCase):
    def test_data_types(self):
        wiretrace = WireTrace.from_vcd("example/wire_types.vcd")
        Visualizer().to_svg(wiretrace).display()


if __name__ == "__main__":
    unittest.main()
