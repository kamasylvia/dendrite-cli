import argparse
from pathlib import Path
import shutil
from sample.compose import compose
from sample.dendrite_init import dendrite_init


def parse_args():
    """
    :return: arguments
    """
    # create the top-level parser
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(title="commands", help="available commands")

    # create the parser for the "init" command
    parser_init = subparsers.add_parser("init", help="initialize dendrite configs")
    parser_init.add_argument(
        "--url",
        default="https://github.com/matrix-org/dendrite.git",
        metavar="",
        help="URL of remote repo",
    )
    parser_init.add_argument("--target", default=".", metavar="", help="target path")
    parser_init.add_argument(
        "--sparse-paths",
        nargs="+",
        metavar="",
        help="list of remote sparse paths",
    )
    parser_init.add_argument(
        "-d",
        "--delete-temp",
        type=bool,
        default=True,
        metavar="",
        help="delete temp repo after cloning",
    )
    parser_init.set_defaults(init=True)

    # create the parser for the "clean" command
    parser_clean = subparsers.add_parser("clean", help="clean local repo")
    parser_clean.add_argument(
        "-i", "--ignore", nargs="+", metavar="", help="ignore paths"
    )
    parser_clean.set_defaults(clean=True)

    # create the parser for the "compose" command
    parent_parser_compose = subparsers.add_parser(
        "compose", help="run dendrite with docker-compose"
    )
    parent_parser_compose.set_defaults(compose=True)

    parser_compose = parent_parser_compose.add_subparsers(
        title="compose commands", help="available commands"
    )

    # create the parser for the "up" command
    parser_compose_up = parser_compose.add_parser("up", help="docker-compose up -d")
    parser_compose_up.set_defaults(up=True)

    # create the parser for the "restart" command
    parser_compose_restart = parser_compose.add_parser(
        "restart", help="docker-compose restart"
    )
    parser_compose_restart.set_defaults(restart=True)

    # create the parser for the "down" command
    parser_compose_down = parser_compose.add_parser(
        "down", help="remove containers/images/all"
    )
    group = parser_compose_down.add_mutually_exclusive_group()
    group.add_argument(
        "-i",
        "--images",
        action="store_true",
        help="remove all images.",
    )
    group.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="remove containers, images, volumes, and networks",
    )
    parser_compose_down.set_defaults(down=True)

    return parser.parse_args()


def main():
    args = parse_args()

    if hasattr(args, "init"):
        dendrite_init(args)
    elif hasattr(args, "clean"):
        local = Path(".")
        ignores = [Path(".git"), Path(".vscode"), Path(".gitignore")]
        if args.ignore:
            ignores = [Path(".vscode"), Path(".gitignore")] + args.ignore

        for path in local.iterdir():
            if path.is_dir() and path not in ignores:
                shutil.rmtree(path, ignore_errors=True)
            if path.is_file() and path.suffix != ".py" and path not in ignores:
                path.unlink()
    elif hasattr(args, "compose"):
        compose(args)


if __name__ == "__main__":
    main()
