from src.directory import Directory
from tests.test_node import TestNode


class TestDirectory(TestNode):
    def setUp(self) -> None:
        self.node = Directory("test")
