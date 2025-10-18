"""Module for logger functionality"""

import logging
import sys


# setup debug logger for dev -> sys.stderr
def get_debug_logger() -> logging.Logger:
    """TODO: add docstring"""
    debug_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    debug_handler = logging.StreamHandler(sys.stderr)
    debug_handler.setFormatter(debug_formatter)

    debug_logger = logging.getLogger("Debug Logger")
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.addHandler(debug_handler)

    return debug_logger


# setup test logger -> sys.stderr
def get_test_logger() -> logging.Logger:
    """TODO: add docstring"""
    test_formatter = logging.Formatter(
        "%(asctime)s - TEST - %(levelname)s - %(message)s"
    )
    test_handler = logging.FileHandler("test.log")
    test_handler.setFormatter(test_formatter)

    test_logger = logging.getLogger("Test Logger")
    test_logger.setLevel(logging.DEBUG)
    test_logger.addHandler(test_handler)

    return test_logger


# setup sys.stdout stream logger for prod
def get_prod_logger(verbose: bool) -> logging.Logger:
    """TODO: add docstring"""
    prod_formatter = logging.Formatter("%(message)s")
    prod_handler = logging.StreamHandler(sys.stdout)
    prod_handler.setFormatter(prod_formatter)

    prod_logger = logging.getLogger("Prod Logger")

    if verbose:
        prod_logger.setLevel(logging.INFO)
    else:
        prod_logger.setLevel(logging.ERROR)

    prod_logger.addHandler(prod_handler)

    return prod_logger
