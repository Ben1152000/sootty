import json
from pyDigitalWaveTools.vcd.parser import VcdParser

from .wiretrace import WireTrace

DEBUG = False

def parse_vcd(filename):
    with open(filename) as vcd_file:
        vcd = VcdParser()
        vcd.parse(vcd_file)
        data = vcd.scope.toJson()  # dump json here for debugging
        if DEBUG:
            with open('dump.json', 'w') as writefile:
                writefile.write(json.dumps(data, indent=2, sort_keys=True))
        return WireTrace.parse_vcd(data)
