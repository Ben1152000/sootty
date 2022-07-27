import os, sys
from sootty.exceptions import SoottyError
import datetime
import yaml


def save_query(save, name, wires, br, length, start, end, display):
    savefile = os.getenv("HOME") + "/.config/sootty/save/queries.yaml"

    if is_save_file(savefile):
        """
        Memory check for the file
        """
        with open(savefile, "r") as f:
            lines = yaml.safe_load(f)
        if save in lines:
            pass
        else:
            with open(savefile, "w") as stream:
                if len(lines) >= 500:
                    print(
                        "Saved query limit reached. Deleting least recent query to accommodate new query.",
                        file=sys.stderr,
                    )
                    stream.truncate(0)
                    for key in lines:
                        stat = lines.pop(key)
                        break
                    if stat is None:  # No lines to delete/Error
                        raise SoottyError("Error deleting least recent query.")
                    yaml.dump(lines, stream, sort_keys=False, width=float("inf"))

        with open(savefile, "a+") as stream:
            query_write(
                savefile, stream, save, name, wires, br, length, start, end, display
            )

    else:
        # Creating new savefile as no savefiles found for sootty
        with open(savefile, "w") as stream:
            query_write(
                savefile, stream, save, name, wires, br, length, start, end, display
            )


def query_write(
    savefile_path, savefile, save, name, wires, br, length, start, end, display
):
    with open(savefile_path, "r+") as stream:
        lines = yaml.safe_load(stream)
        if save in lines:
            del lines[save]  # Deleting outdated query
            overwrite_dict = {
                save: {
                    "query": query_build(name, wires, br, length, start, end, display),
                    "date": str(datetime.datetime.now()),
                }
            }
            lines.update(
                overwrite_dict
            )  # Essentially replacing the old query with the new dict
            stream.truncate(0)
            yaml.dump(
                lines, savefile, sort_keys=False, width=float("inf")
            )  # Dumping the overwritten query to the file, forcing no inline output
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
