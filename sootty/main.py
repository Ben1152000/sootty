import sys, argparse

from .display import display
from .wiretrace import WireTrace

def main():

    parser = argparse.ArgumentParser(description='Converts .vcd wiretraces to .svg format.')
    parser.add_argument('filename', metavar='FILENAME', type=str, help='input .vcd file')
    parser.add_argument('-s', '--start', type=str, metavar='FORMULA', dest='start', help='formula for the start of the window')
    parser.add_argument('-e', '--end', type=str, metavar='FORMULA', dest='end', help='formula for the end of the window')
    parser.add_argument('-l', '--length', type=int, dest='length', help='number of cycles to display')
    parser.add_argument('-d', '--display', action='store_true', help='display to command line')
    parser.add_argument('-w', '--wires', type=str, metavar='LIST', dest='wires', help='comma-separated list of wires to view')
    args = parser.parse_args()

    wiretrace = WireTrace.from_vcd_file(args.filename)

    if args.end is not None and args.length is not None:
        raise Exception('Length and end flags should not be provided simultaneously.')
    
    if args.end is not None:
        if args.start is not None:
            start, end = wiretrace.compute_limits(args.start, args.end)
        else:
            start, end = wiretrace.compute_limits('time 0', args.end)
        length = end - start
    else:
        if args.start is not None:
            start, end = wiretrace.compute_limits(args.start, 'time 0')
        else:
            start = 0
        length = args.length if args.length is not None else wiretrace.length() - start
    
    wires = set()
    if args.wires:
        wires = set(args.wires.split(','))
    
    svg_data = wiretrace.to_svg(start=start, length=length, wires=wires)

    if len(wires):
        raise Exception(f'Unknown wires {wires.__repr__()}\nThe following wires were detected in the wiretrace:\n{wiretrace.get_wire_names()}')
    
    if args.display:
        display(svg_data)
    
    else:
        print(svg_data)
