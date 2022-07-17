import os


def save_query(save, name, wires, br, length, start, end, display):
    save = os.getenv("HOME") + "/.config/sootty/save/" + save
    """
    Constructing the query using conditionals
    """
    with open(save, "w") as wf:
        wf.truncate(0)
        if name:
            wf.write(' -f "' + name + '"')
        if wires:
            wf.write(' -w "' + wires + '"')
        if br:
            wf.write(' -b "' + br + '"')
        if length:
            wf.write(' -l "' + str(length) + '"')
        if start:
            wf.write(' -s "' + start + '"')
        if end:
            wf.write(' -e "' + end + '"')
        if display:
            wf.write(" -d")


def is_save_file(filename):
    return os.path.isfile(filename)
