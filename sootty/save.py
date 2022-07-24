import os
import subprocess
import datetime

def save_query(save, name, wires, br, length, start, end, display):
    savefile = os.getenv("HOME") + "/.config/sootty/save/queries.yaml"
    """
    Memory check for the file
    """
    with open(savefile) as f:
        count = sum(1 for _ in f)
        if count >= 1500:
            status = subprocess.run("sed -i 1,3d " + savefile, shell=True)  # Deleting first 3 lines using sed instead of reading all lines
            if status.returncode != 0:                                      # sed operation failed
                raise Exception("Error deleting least recent query.")
                
    if is_save_file(savefile):
        with open(savefile, "a") as stream:
            query_write(stream, save, name, wires, br, length, start, end, display)
    else:
        with open(savefile, "w") as stream:
            query_write(stream, save, name, wires, br, length, start, end, display)

def query_write(savefile, save, name, wires, br, length, start, end, display):
    savefile.write(save + ":\n")
    savefile.write("  query:")
    """
    Constructing the query using conditionals
    """  
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
