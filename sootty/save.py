import os
from sootty.exceptions import SoottyError
import datetime
import yaml

def save_query(save, name, wires, br, length, start, end, display):
    savefile = os.getenv("HOME") + "/.config/sootty/save/queries.yaml"
    """
    Memory check for the file
    """
    with open(savefile) as f:
        lines = yaml.safe_load(f)
        if len(lines) >= 500:
            stat = lines.popitem(last=False)
            if stat is None:                                                # No lines to delete/Error
                raise SoottyError("Error deleting least recent query.")
            yaml.dump(lines, f, sort_keys = False)
    
    if is_save_file(savefile):
        with open(savefile, "a+") as stream:
            query_write(savefile, stream, save, name, wires, br, length, start, end, display)
    else:
        with open(savefile, "w") as stream:
            query_write(savefile, stream, save, name, wires, br, length, start, end, display)

def query_write(savefile_path, savefile, save, name, wires, br, length, start, end, display):
    with open(savefile_path, "r+") as stream:
        lines = yaml.safe_load(stream) 
        if save in lines:
            lines[save]["query"] = query_build(name, wires, br, length, start, end, display)
            lines[save]["date"] = str(datetime.datetime.now())
            stream.truncate(0)
            yaml.dump(lines, savefile, sort_keys = False)            # Dumping the overwritten query to the file, forcing no inline output
        else:
            savefile.write(save + ":\n")
            savefile.write("  query:")    
            savefile.write(query_build(name, wires, br, length, start, end, display))
            savefile.write("\n")
            savefile.write("  date: " + str(datetime.datetime.now()) + "\n")

def query_build(name, wires, br, length, start, end, display):
    """
    Constructing the query using conditionals
    """
    cmd = ""
    if name:
        cmd += ' -f "' + name + '"'
    if wires:
        cmd += ' -w "' + wires + '"'
    if br:
        cmd += ' -b "' + br + '"'
    if length:
        cmd += ' -l "' + str(length) + '"'
    if start:
        cmd += ' -s "' + start + '"'
    if end:
        cmd += ' -e "' + end + '"'
    if display:
        cmd += " -d"
    return cmd

def is_save_file(filename):
    return os.path.isfile(filename)
