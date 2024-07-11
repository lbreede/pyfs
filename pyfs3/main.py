from __future__ import annotations
from datetime import datetime
from typing import Optional
import time


class FileSystemObject:
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        self.name = name
        self.parent = parent
        self.created = datetime.now()
        self.modified = datetime.now()

    def rename(self, new_name: str) -> None:
        """Rename this file system object and update the modified time."""
        self.name = new_name
        self.modified = datetime.now()

    def get_path(self) -> str:
        """Get the path of this file system object."""
        if self.parent is None:
            return f"/{self.name}"
        return f"{self.parent.get_path()}/{self.name}"

    def delete(self) -> None:
        """Delete this file system object."""
        if self.parent is None:
            raise ValueError("Cannot delete root directory.")
        if isinstance(self, Directory):
            if self.subdirectories or self.files:
                raise ValueError("Cannot delete non-empty directory.")
            self.parent.subdirectories.remove(self)
        else:
            self.parent.files.remove(self)
        self.parent = None

    def __repr__(self) -> str:
        return f"FileSystemObject({self.name})"

    def __str__(self) -> str:
        return self.get_path()


class Directory(FileSystemObject):
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        super().__init__(name, parent)
        self.files: list[File] = []
        self.subdirectories: list[Directory] = []

    def add_subdirectory(self, directory: Directory) -> None:
        """Add a subdirectory to this directory."""
        if directory.parent is not None:
            directory.parent.subdirectories.remove(directory)
        directory.parent = self
        self.subdirectories.append(directory)

    def add_file(self, file_: File) -> None:
        """Add a file to this directory."""
        if file_.parent is not None:
            file_.parent.files.remove(file_)
        file_.parent = self
        self.files.append(file_)


class File(FileSystemObject):
    def __init__(self, name: str, parent: Optional[Directory] = None) -> None:
        super().__init__(name, parent)
        self.content = ""

    def read(self) -> str:
        """Read the content of this file."""
        return self.content

    def write(self, content: str) -> None:
        """Write the content to this file."""
        self.content = content

    def append(self, content: str) -> None:
        """Append the content to this file."""
        self.content += content


def main() -> None:
    root = Directory("root")
    print(root)
    home = Directory("home")
    root.add_subdirectory(home)
    bin_ = Directory("bin", parent=root)
    print(home)
    print(bin_)
    file_1 = File("file_1.txt", parent=home)
    file_2 = File("file_2.txt")
    home.add_file(file_2)
    print(file_1)
    print(file_2)

    print(file_1.read())
    file_1.write("Hello")
    print(file_1.read())
    file_1.append(", World!")
    print(file_1.read())
    file_1.write("Goodbye!")
    print(file_1.read())

    print(file_1.created)
    print(file_1.modified)

    time.sleep(5.0)

    file_1.rename("file_1_renamed.txt")
    print(file_1)

    print(file_1.created)
    print(file_1.modified)


if __name__ == "__main__":
    main()
