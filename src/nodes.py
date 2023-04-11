from __future__ import annotations

from datetime import datetime
from typing import Optional


class Node:
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        self.name = name
        self.parent = parent
        self._created = datetime.now()
        self._modified = self.created

    def rename(self, new_name: str) -> None:
        """Rename this file system object and update the modified time."""
        self.name = new_name
        self.update_modified()

    @property
    def path(self) -> str:
        """Get the path of this file system object."""
        if self.parent is None:
            return f"/{self.name}"
        return f"{self.parent.path}/{self.name}"

    @property
    def created(self) -> datetime:
        """Get the creation time of this file system object."""
        return self._created

    @property
    def modified(self) -> datetime:
        """Get the modified time of this file system object."""
        return self._modified

    def update_modified(self) -> None:
        """Update the modified time of this file system object."""
        self._modified = datetime.now()

    def __repr__(self) -> str:
        return f"Node({self.name}, parent={self.parent})"

    def __str__(self) -> str:
        return self.path


class Directory(Node):
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        super().__init__(name, parent)
        self.files: list[File] = []
        self.subdirectories: list[Directory] = []

    def add_file(self, file: File) -> None:
        """Add a file to this directory."""
        self.files.append(file)

    def add_directory(self, directory: Directory) -> None:
        """Add a directory to this directory."""
        self.subdirectories.append(directory)


class File(Node):
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        super().__init__(name, parent)
        self.content = ""

    def read(self) -> str:
        return self.content

    def write(self, content: str) -> None:
        self.content = content
        self.update_modified()

    def append(self, content: str) -> None:
        self.content += content
        self.update_modified()
