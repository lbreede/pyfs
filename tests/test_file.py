from src.file import File
from tests.test_node import TestNode


class TestFile(TestNode):
    def setUp(self) -> None:
        self.node = File("test")

    def test_content(self) -> None:
        modified_before = self.node.modified
        self.assertEqual(self.node.read(), "")
        self.node.write("Hello World!")
        self.assertEqual(self.node.read(), "Hello World!")
        self.node.append(" How are you?")
        self.assertEqual(self.node.read(), "Hello World! How are you?")
        self.node.write("Goodbye!")
        self.assertEqual(self.node.read(), "Goodbye!")
        self.assertGreater(self.node.modified, modified_before)
