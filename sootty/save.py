import os
import subprocess

def save_query(save, name, wires, br, length, start, end, display):
    save = os.getenv("HOME") + "/.config/sootty/save/" + save
    if is_save_file(save) is True:
        val = input("A save file with this name already exists. Are you sure you want to overwrite it (y/n)?")
        if val is 'y':
            with open(save, 'w') as wf:
                wf.truncate(0)
                if name:
                    wf.write("sootty -f \"" + name + "\"")
                if wires:
                    wf.write(" -w \"" + wires + "\"")
                if br:
                    wf.write(" -b \"" + br + "\"")
                if length:
                    wf.write(" -l \"" + length + "\"")
                if start:
                    wf.write(" -s \"" + start + "\"")
                if end:
                    wf.write(" -e \"" + end + "\"")
                if display:
                    wf.write(" -d")
        else:
            val_2 = input("Would you like to enter another file name (y/n)?")
            if val_2 is 'y':
                save = input("Enter the filename:")
                save_query(save, name, wires, br, length, start, end, display)
            else:
                exit(0)
    else:
        with open(save, 'w') as wf:
                wf.truncate(0)
                if name:
                    wf.write("sootty -f \"" + name + "\"")
                if wires:
                    wf.write(" -w \"" + wires + "\"")
                if br:
                    wf.write(" -b \"" + br + "\"")
                if length:
                    wf.write(" -l \"" + length + "\"")
                if start:
                    wf.write(" -s \"" + start + "\"")
                if end:
                    wf.write(" -e \"" + end + "\"")
                if display:
                    wf.write(" -d")

def reload_query(reload):
    reload = os.getenv("HOME") + "/.config/sootty/save/" + reload
    with open(reload, 'r') as rf:
        cmd  = rf.readline()
        process = subprocess.run(cmd, shell=True)

def is_save_file(filename):
    return os.path.isfile(filename)
    