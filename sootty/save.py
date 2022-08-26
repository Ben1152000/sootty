import os, sys
from sootty.exceptions import SoottyError
import time
import yaml


SAVEFILE = os.getenv("HOME") + "/.config/sootty/save/queries.yaml"
QUERYLIMIT = 500


def save_query(args):
    if not os.path.isfile(SAVEFILE):  # Create file if not found
        open(SAVEFILE, "a").close()

    with open(SAVEFILE, "r") as f:  # Read the existing saved queries
        data = yaml.safe_load(f)
        if data is None:
            data = dict()

    data.update(
        {
            args.save: {
                "query": build_query(args),
                "date": int(time.time() * 1000),
            }
        }
    )

    if len(data) > QUERYLIMIT:
        print(
            "Saved query limit reached. Deleting least recent query to accommodate new query.",
            file=sys.stderr,
        )
        keys = sorted(data, key=lambda key: data[key]["date"], reverse=True)[
            :QUERYLIMIT
        ]
        data = dict(zip(keys, map(lambda key: data[key], keys)))

    with open(SAVEFILE, "w") as stream:
        yaml.dump(data, stream, width=float("inf"))


def build_query(args):
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
