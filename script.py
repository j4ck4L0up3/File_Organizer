#!/usr/bin/env python3

"""For testing script capabilities. May consolidate to main.py"""

import sys


def format_menu(options, left_width, right_width):
    print("File_Organizer Help Menu".center(left_width + right_width, "-"))
    for opt, desc in options.items():
        print(opt.ljust(left_width, " ") + desc.rjust(right_width))


OPTIONS = {
    "-d, --desktop-flag BOOL": "set False by default. set True to clear your Desktop.",
    "-t, --trash-flag BOOL": "set False by default. set True to automatically delete compressed files from Downloads.",
    "-v, --verbose": "show verbose output",
    "-l, --log FILE": "output logs to a file",
    "-h, --help": "show menu",
}

# format_menu(OPTIONS, 50, 5)
