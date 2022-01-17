import sys
from subprocess import call, Popen, STDOUT, PIPE
from re import match


class VectorImage:
    """Encapsulates logic to store and display an SVG to the terminal."""

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return self.source

    def display(self):
        # TODO: fix!!! these lines are for hacking together width relative to display
        # result = match(r'<svg viewBox="0 0 (\d+) (\d+)".*', self.source)
        # ratio = float(result.group(2)) / float(result.group(1))
        # width = 24000
        # height = int(ratio * width * 5 / 12)
        process = Popen(
            f"rsvg-convert -z 4 | viu -", shell=True, stdin=PIPE, stdout=sys.stdout
        )
        process.communicate(input=str.encode(self.source))
