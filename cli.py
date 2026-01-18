#!/usr/bin/env python3

"""For cli setup and running main."""

import argparse
import sys
from logging import FileHandler, StreamHandler
from pathlib import Path

from main import main
from tests.logger import get_prod_logger


# TODO: write integration test for cli
# TODO: add functionality for excluding certain directories from cleanup
def cli():
    parser = argparse.ArgumentParser()

    # add arguments
    parser.add_argument(
        "-d", "--desktop-flag", action="store_true", help="clears your Desktop"
    )
    parser.add_argument(
        "-t",
        "--trash-flag",
        action="store_true",
        help="automatically delete compressed files from Downloads",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="show verbose output"
    )
    parser.add_argument(
        "-l",
        "--log",
        action="store",
        type=argparse.FileType("wt"),
        help="output logs to file specified",
    )

    args = parser.parse_args()

    # set flags
    desktop_flag = args.desktop_flag
    trash_flag = args.trash_flag

    logger = get_prod_logger(args.verbose)

    if args.log:
        if not Path(args.log).exists():
            Path(args.log).touch()

        logger.removeHandler(StreamHandler(sys.stdout))
        logger.addHandler(FileHandler(args.log))

    main(desktop_flag=desktop_flag, trash_flag=trash_flag)


if __name__ == "__main__":
    cli()
