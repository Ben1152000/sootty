import sys
from limit import LimitExpression
from wiretrace import WireTrace
from parser import parse_vcd
from visualizer import Visualizer
from subprocess import Popen, STDOUT
from tempfile import TemporaryFile

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('Give me a vcd file to parse')
        sys.exit(-1)
    
    wiretrace = parse_vcd(sys.argv[1])

    start_expr = LimitExpression("D0 & D1")
    end_expr = LimitExpression("Data == const 15")
    start, end = wiretrace.compute_limits(start_expr, end_expr)

    svg_data = Visualizer.wiretrace_to_svg(
        wiretrace=wiretrace, start=start, length=end-start)
    
    print(svg_data)
