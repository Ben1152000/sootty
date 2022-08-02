import sys, argparse
import os, shlex
from sootty.exceptions import SoottyError
from . import save as sv
from .storage import WireTrace
from .visualizer import Visualizer


def main():

    reload_path = os.getenv("HOME") + "/.config/sootty/save/"
    if os.path.isdir(reload_path) is False:
        os.makedirs(reload_path)

    parser = argparse.ArgumentParser(
        description="Converts .vcd wiretraces to .svg format."
    )
    parser.add_argument(
        "-f",
        "--filename",
        metavar="FILENAME",
        required=False,
        type=str,
        help="input .vcd file. Required unless reloading.",
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
        "-x",
        "--axi",
        type=str,
        metavar="",
        dest="axi",
        help="Flag to define start of window as beginning of AXI transaction of two given argument wires"
    )
    parser.add_argument(
        "-S",
        "--save",
        type=str,
        metavar="SAVENAME",
        help="Save current query for reuse in a .txt file",
    )
    parser.add_argument(
        "-R",
        "--reload",
        type=str,
        metavar="SAVENAME",
        help="Loads a saved query. Requires query name as string.",
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
        reload_query(parser, args.reload, reload_path)
        exit(0)
    else:
        if args.filename is None:
            parser.print_usage()
            exit(0)

    compile(
        args.filename,
        args.wires,
        args.breakpoints,
        args.length,
        args.start,
        args.end,
        args.display,
    )


def compile(filename, wires, breakpoints, length, start, end, display):

    # Load vcd file into wiretrace object.
    wiretrace = WireTrace.from_vcd(filename)

    # Check that window bounds are well-defined.
    if end is not None and length is not None:
        raise Exception("Length and end flags should not be provided simultaneously.")

    if args.axi is not None:
        # axi arg 0 is start/end at axi transaction, arg 1 is ready signal, arg 2 is valid signal, arg 3 is clock signal
        axi = list([name.strip() for name in args.axi.split(",")])
        if axi[0] == "start":
            start = "(" + axi[1] + " && " + axi[2] + " == const 1) && " + axi[3] + " == const 1"
            args.start = start
        elif axi[0] == "end":
            end = "(" + axi[1] + " && " + axi[2] + " == const 1) && " + axi[3] + " == const 1"
            print(end)
            args.end = end
        else:
            raise Exception("Invalid AXI flag.")
    # Calculate window bounds.
    if end is not None:
        if start is not None:
            start, end = wiretrace.compute_limits(start, end)
        else:
            start, end = wiretrace.compute_limits("time 0", end)
        length = end - start
    else:
        if start is not None:
            start, end = wiretrace.compute_limits(start, "time 0")
        else:
            start = 0
        length = length if length is not None else wiretrace.length() - start

    # Calculate breakpoints
    breakpoints = None
    if breakpoints is not None:
        breakpoints = wiretrace.evaluate(breakpoints)

    if wires:
        wires = set([name.strip() for name in wires.split(",")])

    # Convert wiretrace to graphical vector image.
    image = Visualizer().to_svg(
        wiretrace, start=start, length=length, wires=wires, breakpoints=breakpoints
    )

    if wires is not None and len(wires):
        raise Exception(
            f"Unknown wires {wires.__repr__()}\nThe following wires were detected in the wiretrace:\n{wiretrace.get_wire_names()}"
        )

    if display:
        image.display()

    else:
        print(image.source)


def reload_query(parser, reload, reload_path):
    reload = reload_path + reload
    with open(reload, "r") as rf:
        cmd = rf.readline()
    args = parser.parse_args(shlex.split(cmd))  # using shlex to parse string correctly

    compile(
        args.filename,
        args.wires,
        args.breakpoints,
        args.length,
        args.start,
        args.end,
        args.display,
    )


if __name__ == "__main__":
    main()
