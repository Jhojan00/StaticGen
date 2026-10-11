import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)

        self.assertEqual(node, node2)

    def test_neq_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a link node", TextType.BOLD)

        self.assertNotEqual(node, node2)

    def test_neq_types(self):
        node = TextNode("This is a node", TextType.BOLD)
        node2 = TextNode("This is a node", TextType.LINK)

        self.assertNotEqual(node, node2)

    def test_neq_url(self):
        node = TextNode("This is a link", TextType.LINK, "https://bye.world")
        node2 = TextNode("This is a link", TextType.LINK, "https://hello.world")

        self.assertNotEqual(node, node2)

    def test_none_url(self):
        node = TextNode("This is a link", TextType.LINK)
        node2 = TextNode("This is a link", TextType.LINK, "https://hello.world")

        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
