import os
import datetime

def save_query(save, name, wires, br, length, start, end, display):
    savefile = os.getenv("HOME") + "/.config/sootty/save/queries.yaml"
    """
    Constructing the query using conditionals
    """
    if is_save_file(savefile):
        with open(savefile, "a") as stream:
            query_write(stream, save, name, wires, br, length, start, end, display)
    else:
        with open(savefile, "w") as stream:
            query_write(stream, save, name, wires, br, length, start, end, display)

def query_write(savefile, save, name, wires, br, length, start, end, display):
    savefile.write(save + ":\n")
    savefile.write("  query:")
    if name:
        savefile.write(' -f "' + name + '"')
    if wires:
        savefile.write(' -w "' + wires + '"')
    if br:
        savefile.write(' -b "' + br + '"')
    if length:
        savefile.write(' -l "' + str(length) + '"')
    if start:
        savefile.write(' -s "' + start + '"')
    if end:
        savefile.write(' -e "' + end + '"')
    if display:
        savefile.write(" -d")
    savefile.write("\n")
    savefile.write("  date: " + str(datetime.datetime.now()) + "\n")


def is_save_file(filename):
    return os.path.isfile(filename)
