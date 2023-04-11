from __future__ import annotations

import logging
from typing import Optional

from nodes import Directory, File  # type: ignore

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


class FileSystem:
    def __init__(self):
        self.root = Directory("root")
        self.current_directory = self.root

    def mkdir(self, name: str) -> Directory:
        """Create a new directory in the current directory."""
        logger.debug("Creating directory %r in %r", name, self.current_directory.path)
        directory = Directory(name, self.current_directory)
        self.current_directory.add_directory(directory)
        return directory

    def touch(self, name: str) -> File:
        """Create a new file in the current directory."""
        logger.debug("Creating file %r in %r", name, self.current_directory.path)
        file = File(name, self.current_directory)
        self.current_directory.add_file(file)
        return file

    def ls(self) -> None:
        """List the files and directories in the current directory."""
        logger.debug("Listing files and directories in %r", self.current_directory.path)
        for file in self.current_directory.files:
            print(file.name)
        for directory in self.current_directory.subdirectories:
            print(directory.name)

    def cd(self, path: str) -> None:
        """Change the current directory."""
        logger.debug("Changing directory to %r", path)
        if path == "..":
            if self.current_directory.parent is None:
                raise ValueError("Cannot go up from root directory")
            self.current_directory = self.current_directory.parent
            return
        for directory in self.current_directory.subdirectories:
            if directory.name == path:
                self.current_directory = directory
                return
        raise ValueError(f"Directory {path} not found")

    def find_directory(self, path: str) -> Optional[Directory]:
        """Find a directory in the file system."""
        logger.debug("Finding directory %r", path)
        if path == "/":
            return self.root
        if path.startswith("/"):
            path = path[1:]
        path_parts = path.split("/")
        current_directory = self.root
        for part in path_parts:
            for directory in current_directory.subdirectories:
                if directory.name == part:
                    current_directory = directory
                    break
            else:
                return None
        return current_directory


def main() -> None:
    fs = FileSystem()
    fs.mkdir("home")
    fs.mkdir("etc")
    fs.touch("README.md")
    fs.ls()
    fs.cd("home")
    fs.cd("..")
    fs.cd("home")
    fs.ls()


if __name__ == "__main__":
    main()
