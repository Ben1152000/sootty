from sys import stdout
from subprocess import call, Popen, STDOUT, PIPE

def display(svg_data):
    process = Popen("rsvg-convert -x 4 -y 4 | viu -", shell=True, stdin=PIPE, stdout=stdout)
    process.communicate(input=str.encode(svg_data))
