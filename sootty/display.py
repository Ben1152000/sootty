from sys import stdout
from subprocess import call, Popen, STDOUT, PIPE


class VectorImage:
    """Encapsulates logic to store and display an SVG to the terminal."""

    def __init__(self, source):
        self.source = source

    def __str__(self):
        return self.source
    
    def display(self):
        process = Popen("rsvg-convert -x 4 -y 4 | viu -", shell=True, stdin=PIPE, stdout=stdout)
        process.communicate(input=str.encode(self.source))
