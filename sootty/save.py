import os
import datetime

def save_query(save, name, wires, br, length, start, end, display):
    savefile = os.getenv("HOME") + "/.config/sootty/save.yaml"
    """
    Constructing the query using conditionals
    """
    with open(savefile, "a") as stream:
        stream.write(save + ":\n")
        stream.write("  query:")
        if name:
            stream.write(' -f "' + name + '"')
        if wires:
            stream.write(' -w "' + wires + '"')
        if br:
            stream.write(' -b "' + br + '"')
        if length:
            stream.write(' -l "' + str(length) + '"')
        if start:
            stream.write(' -s "' + start + '"')
        if end:
            stream.write(' -e "' + end + '"')
        if display:
            stream.write(" -d")
        stream.write("\n")
        stream.write("  date: " + str(datetime.datetime.now()) + "\n")

def is_save_file(filename):
    return os.path.isfile(filename)
