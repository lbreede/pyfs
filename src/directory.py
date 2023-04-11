from __future__ import annotations

from datetime import datetime
from typing import Optional

from src.protocols import File


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

    def get_path(self) -> str:
        """Get the path of this file system object."""
        if self.parent is None:
            return f"/{self.name}"
        return f"{self.parent.get_path()}/{self.name}"

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
        return self.get_path()


class Directory(Node):
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        super().__init__(name, parent)
        self.files: list[File] = []
        self.subdirectories: list[Directory] = []
