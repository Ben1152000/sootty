import os, sys
from sootty.exceptions import SoottyError
import time
import yaml


PATH = os.getenv("HOME") + "/.config/sootty/save/"
SAVEFILE = PATH + "queries.yaml"
QUERYLIMIT = 500


def get_queries():
    """Reads list of queries from yaml config file."""
    if os.path.isdir(PATH) is False:
        os.makedirs(PATH)
    if not os.path.isfile(SAVEFILE):  # Create file if not found
        open(SAVEFILE, "a").close()

    with open(SAVEFILE, "r") as f:  # Read the existing saved queries
        data = yaml.safe_load(f)
        if data is None:
            data = dict()
    return data


def save_query(args):
    """Saves args to config file as a yaml dictionary object."""
    queries = get_queries()
    queries.update(
        {
            args.save: {
                "query": vars(args),
                "date": int(time.time() * 1000),
            }
        }
    )

    if len(queries) > QUERYLIMIT:
        print(
            "Saved query limit reached. Deleting least recent query to accommodate new query.",
            file=sys.stderr,
        )
        keys = sorted(queries, key=lambda key: queries[key]["date"], reverse=True)[
            :QUERYLIMIT
        ]
        queries = dict(zip(keys, map(lambda key: queries[key], keys)))

    with open(SAVEFILE, "w") as stream:
        yaml.dump(queries, stream, width=float("inf"))


def reload_query(parser, args):
    """Loads the saved query from the config file (throws exception if not found)."""
    data = get_queries()
    if args.reload not in data:
        raise SoottyError(
            f'Cannot reload query "{args.reload}", saved query not found.'
        )

    query = data[args.reload]["query"]
    data[args.reload]["date"] = int(
        time.time() * 1000
    )  # Update timestamp for this query
    with open(SAVEFILE, "w") as stream:
        yaml.dump(data, stream, width=float("inf"))

    # Update specifc flags for a relaoded query
    for key in query:
        if not hasattr(args, key) or getattr(args, key) is None:
            setattr(args, key, query[key])

    return args
