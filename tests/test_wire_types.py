import pyrtl
from sootty import WireTrace, Visualizer


def test_data_types():
    wiretrace = WireTrace.from_vcd("example/wire_types.vcd")
    Visualizer().to_svg(wiretrace).display()


if __name__ == "__main__":
    test_data_types()
    print("Success!")
