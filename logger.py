''' Module for logger functionality'''
import logging
import typing
import sys

# setup debug logger for dev -> debug.log
def get_debug_logger(file: typing.TextIO) -> logging.Logger:
    ''' TODO: add docstring '''
    debug_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    debug_handler = logging.StreamHandler(file)
    debug_handler.setFormatter(debug_formatter)

    debug_logger = logging.getLogger("Debug Logger")
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.addHandler(debug_handler)
    
    return debug_logger

# TODO: setup sys.stdout stream logger for prod


