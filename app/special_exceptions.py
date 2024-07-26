""" Module with classes for special exception behavior """

from pathlib import Path


class EmptyDirectory(Exception):
    """TODO: add docstring"""

    def __init__(self, directory: Path, func_name: str):
        self.directory = directory
        self.func_name = func_name
        super().__init__(self.directory, self.func_name)

        def __str__(self):
            """TODO: add docstring"""
            return f"Directory {self.directory} is empty in {self.func_name}"
