#!/usr/bin/env python3

"""For testing script capabilities. May consolidate to main.py"""

import sys


def format_menu(options, left_width, right_width):
    print("File_Organizer Help Menu".center(left_width + right_width, "-"))
    for opt, desc in options.items():
        print(opt.ljust(left_width, " ") + desc.rjust(right_width))


OPTIONS = {
    "-d [optstring], --desktop='optstring'": "set False by default. set True to clear your Desktop.",
    "-v, --verbose": "show logs",
    "-h, --help": "show menu",
}

format_menu(OPTIONS, 50, 5)
