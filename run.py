import sys
from wiretrace import WireTrace
from parser import parse_vcd
from visualizer import Visualizer

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('Give me a vcd file to parse')
        sys.exit(-1)
    
    print(Visualizer().wiretrace_to_svg(
            wiretrace=parse_vcd(sys.argv[1]),
            length=20))