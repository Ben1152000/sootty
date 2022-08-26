import os, sys
from sootty.exceptions import SoottyError
import datetime
import yaml


savefile = os.getenv("HOME") + "/.config/sootty/save/queries.yaml"


def save_query(args):

    if is_save_file(savefile):
        """
        Memory check for the file
        """
        with open(savefile, "r+") as f:
            lines = yaml.safe_load(f)
        if lines is None:
            with open(savefile, "w") as stream:
                query_write(savefile, stream, args)
        else:
            if args.save in lines:
                pass
            else:
                if len(lines) >= 500:
                    print(
                        "Saved query limit reached. Deleting least recent query to accommodate new query.",
                        file=sys.stderr,
                    )
                    f.truncate(0)
                    for key in lines:
                        stat = lines.pop(key)
                        break
                    if stat is None:  # No lines to delete/Error
                        raise SoottyError("Error deleting least recent query.")
                    yaml.dump(lines, f, sort_keys=False, width=float("inf"))

            with open(savefile, "a+") as stream:
                query_write(savefile, stream, args)

    else:
        # Creating new savefile as no savefiles found for sootty
        print("Creating new savefile...", file=sys.stderr)
        with open(savefile, "w") as stream:
            query_write(savefile, stream, args)


def query_write(savefile_path, savefile, args):
    with open(savefile_path, "r") as stream:
        lines = yaml.safe_load(stream)
        if lines is None or (not args.save in lines):
            savefile.write(args.save + ":\n")
            savefile.write("  query:")
            savefile.write(query_build(args))
            savefile.write("\n")
            savefile.write("  date: " + str(datetime.datetime.now()) + "\n")
        else:
            del lines[args.save]  # Deleting outdated query
            overwrite_dict = {
                args.save: {
                    "query": query_build(args),
                    "date": str(datetime.datetime.now()),
                }
            }
            lines.update(overwrite_dict)  # Replace the old query with the new dict
            savefile.truncate(0)
            yaml.dump(
                lines, savefile, sort_keys=False, width=float("inf")
            )  # Dumping the overwritten query to the file, forcing no inline output


def query_build(args):
    """
    Constructing the query using conditionals
    """
    cmd = ""
    if args.filename:
        cmd += f' -f "{args.filename}"'
    if args.wires:
        cmd += f' -w "{args.wires}"'
    if args.breakpoints:
        cmd += f' -b "{args.breakpoints}"'
    if args.length:
        cmd += f' -l "{args.length}"'
    if args.start:
        cmd += f' -s "{args.start}"'
    if args.end:
        cmd += f' -e "{args.end}"'
    if args.output:
        cmd += f" -o"
    return cmd


def is_save_file(filename):
    return os.path.isfile(filename)
