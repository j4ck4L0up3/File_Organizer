''' Module with classes for special exception behavior '''
import logging
from pathlib import Path

class EmptyDirectory(Exception):
    ''' TODO: add docstring '''
    def __init__(self, logger: logging.Logger, directory: Path, func_name: str):
        self.logger = logger
        self.directory = directory
        self.func_name = func_name

    def log_empty_dir_memo(self):
        ''' TODO: add docstring '''
        self.logger.warning(
            'Directory %s is empty in %s', 
            self.directory,
            self.func_name
        )