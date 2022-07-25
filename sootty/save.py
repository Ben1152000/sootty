import os
import subprocess
import datetime
import yaml

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
            res = sorted(lines.items(), key = lambda x: x[1]["date"])
            print(res)
            #yaml.dump(lines, savefile)            # Dumping the overwritten query to the file, forcing no inline output
            exit(0)
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
