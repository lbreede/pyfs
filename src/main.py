from __future__ import annotations

from src.directory import Directory
from src.file import File


class FileSystem:
    def __init__(self):
        self.root = Directory("root")
        self.current_directory = self.root

    def mkdir(self, name: str) -> Directory:
        """Create a new directory in the current directory."""
        directory = Directory(name, self.current_directory)
        self.current_directory.subdirectories.append(directory)
        return directory

    def touch(self, name: str) -> File:
        """Create a new file in the current directory."""
        file = File(name, self.current_directory)
        self.current_directory.files.append(file)
        return file

    def ls(self) -> None:
        """List the files and directories in the current directory."""
        for file in self.current_directory.files:
            print(file.name)
        for directory in self.current_directory.subdirectories:
            print(directory.name)

    def cd(self, path: str) -> None:
        """Change the current directory."""
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


def main() -> None:
    fs = FileSystem()
    fs.mkdir("home")
    fs.mkdir("etc")
    fs.touch("README.md")
    fs.cd("home")
    fs.mkdir("user")
    fs.cd("user")
    fs.touch("profile.txt")
    fs.cd("..")
    fs.cd("..")
    fs.cd("etc")
    fs.touch("hosts")
    fs.cd("home")
    fs.cd("user")
    fs.touch("todo.txt")
    fs.cd("todo.txt")
    fs.write("Buy milk")


if __name__ == "__main__":
    main()
