import sys, argparse

from sootty.exceptions import SoottyError
from . import save as sv
from .storage import WireTrace
from .visualizer import Visualizer


def main():

    parser = argparse.ArgumentParser(
        description="Converts .vcd wiretraces to .svg format."
    )
    parser.add_argument(
        "-f",
        "--filename",
        metavar="FILENAME",
        required=False,
        type=str,
        help="input .vcd file",
    )
    parser.add_argument(
        "-s",
        "--start",
        type=str,
        metavar="FORMULA",
        dest="start",
        help='formula for the start of the window (ex: \
        "time 4", \
        "after time 2 & clk", \
        "x == y | z == const 15")',
    )
    parser.add_argument(
        "-e",
        "--end",
        type=str,
        metavar="FORMULA",
        dest="end",
        help="formula for the end of the window",
    )
    parser.add_argument(
        "-b",
        "--break",
        type=str,
        metavar="FORMULA",
        dest="breakpoints",
        help="formula for the points in time to be highlighted",
    )
    parser.add_argument(
        "-l", "--length", type=int, dest="length", help="number of cycles to display"
    )
    parser.add_argument(
        "-d", "--display", action="store_true", help="display to command line"
    )
    parser.add_argument(
        "-w",
        "--wires",
        type=str,
        metavar="LIST",
        dest="wires",
        help="comma-separated list of wires to view",
    )
    parser.add_argument(
        "-S",
        "--save",
        type=str,
        metavar="",
        help="Save current query for reuse in a .txt file",
    )
    parser.add_argument(
        "-R", "--reload", type=str, metavar="", help="Loads the saved query"
    )
    args = parser.parse_args()

    if args.save is not None:
        if args.reload:
            raise SoottyError(
                f"Save and Reload flags should not be provided simultaneously."
            )
        sv.save_query(
            args.save,
            args.filename,
            args.wires,
            args.breakpoints,
            args.length,
            args.start,
            args.end,
            args.display,
        )

    if args.reload is not None:
        sv.reload_query(args.reload)
        exit(0)
    else:
        if args.filename is None:
            raise Exception("No input file provided.")

    # Load vcd file into wiretrace object.
    wiretrace = WireTrace.from_vcd(args.filename)

    # Check that window bounds are well-defined.
    if args.end is not None and args.length is not None:
        raise Exception("Length and end flags should not be provided simultaneously.")

    # Calculate window bounds.
    if args.end is not None:
        if args.start is not None:
            start, end = wiretrace.compute_limits(args.start, args.end)
        else:
            start, end = wiretrace.compute_limits("time 0", args.end)
        length = end - start
    else:
        if args.start is not None:
            start, end = wiretrace.compute_limits(args.start, "time 0")
        else:
            start = 0
        length = args.length if args.length is not None else wiretrace.length() - start

    # Calculate breakpoints
    breakpoints = None
    if args.breakpoints is not None:
        breakpoints = wiretrace.evaluate(args.breakpoints)

    wires = None
    if args.wires:
        wires = set([name.strip() for name in args.wires.split(",")])

    # Convert wiretrace to graphical vector image.
    image = Visualizer().to_svg(
        wiretrace, start=start, length=length, wires=wires, breakpoints=breakpoints
    )

    if wires is not None and len(wires):
        raise Exception(
            f"Unknown wires {wires.__repr__()}\nThe following wires were detected in the wiretrace:\n{wiretrace.get_wire_names()}"
        )

    if args.display:
        image.display()

    else:
        print(image.source)


if __name__ == "__main__":
    main()
