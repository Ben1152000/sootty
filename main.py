import sys, argparse
from limit import LimitExpression
from wiretrace import WireTrace
from parser import parse_vcd
from visualizer import Visualizer
from subprocess import Popen, STDOUT
from tempfile import TemporaryFile

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Converts .vcd wiretraces to .svg format.')
    parser.add_argument('filename', metavar='FILENAME', type=str, help='input .vcd file')
    parser.add_argument('-s', '--start', type=str, metavar='FORMULA', dest='start', help='formula for the start of the window')
    parser.add_argument('-e', '--end', type=str, metavar='FORMULA', dest='end', help='formula for the end of the window')
    parser.add_argument('-l', '--length', type=int, dest='length', help='number of cycles to display')
    args = parser.parse_args()

    wiretrace = parse_vcd(args.filename)

    if args.end is not None and args.length is not None:
        raise Exception('Length and end flags should not be provided simultaneously.')
    
    if args.end is not None:
        if args.start is not None:
            start, end = wiretrace.compute_limits(LimitExpression(args.start), LimitExpression(args.end))
        else:
            start, end = wiretrace.compute_limits(LimitExpression('time 0'), LimitExpression(args.end))
        length = end - start
    else:
        if args.start is not None:
            start, end = wiretrace.compute_limits(LimitExpression(args.start), LimitExpression('time 0'))
        else:
            start = 0
        length = args.length if args.length is not None else wiretrace.length() - start
    
    svg_data = Visualizer.wiretrace_to_svg(
        wiretrace=wiretrace, start=start, length=length)
    
    print(svg_data)
