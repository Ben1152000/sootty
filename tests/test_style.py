from sootty import WireTrace, Visualizer, Style


def test_style_class():

    wiretrace = WireTrace.from_vcd("example/example1.vcd")

    Visualizer(Style.Silicon).to_svg(wiretrace, start=0, length=8).display()

    Visualizer(Style.Dark).to_svg(wiretrace, start=0, length=8).display()

    Visualizer(Style.Light).to_svg(wiretrace, start=0, length=8).display()


if __name__ == "__main__":
    test_style_class()
    print("Success!")
