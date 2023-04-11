from __future__ import annotations

from typing import Optional

from src.directory import Directory, Node


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
