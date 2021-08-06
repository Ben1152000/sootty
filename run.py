import sys
from wiretrace import WireTrace
from parser import parse_vcd
from visualizer import Visualizer
from subprocess import Popen, STDOUT
from tempfile import TemporaryFile

if __name__ == "__main__":
    
    if len(sys.argv) < 2:
        print('Give me a vcd file to parse')
        sys.exit(-1)
    
    svg_data = Visualizer().wiretrace_to_svg(
        wiretrace=parse_vcd(sys.argv[1]), length=20)
    
    print(svg_data)
    
    # with open('temp.svg', 'w') as svg_file:
    #     svg_file.write(svg_data)
    
    # with open('temp.svg', 'r') as svg_file:
    #     process = Popen(
    #         'rsvg-convert | kitty +kitten icat', 
    #         stdin=svg_file, 
    #         stdout=sys.stdout, 
    #         stderr=sys.stderr, 
    #         shell=True
    #     )
