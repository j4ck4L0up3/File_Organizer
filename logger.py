''' Module for logger functionality'''
import logging
import typing

# setup debug logger for dev -> debug.log
def get_debug_logger(file: typing.TextIO) -> logging.Logger:
    debug_formatter = logging.Formatter('%(asctime) - %(levelname) - %(message)')
    debug_handler = logging.StreamHandler(file)
    debug_handler.setFormatter(debug_formatter)

    debug_logger = logging.getLogger("Debug Logger")
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.addHandler(debug_handler)
    
    return debug_logger

# setup info sys.stdout stream logger for prod


# setup warning sys.stdout stream logger for prod


# setup error sys.stdout stream logger for prod