import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Hello, world")
        self.assertEqual(node.to_html(), "Hello, world")

    def test_leaf_props(self):
        node = LeafNode("a", "Hello, world", {"href": "https://hello.world"})
        self.assertEqual(
            node.to_html(), '<a href="https://hello.world">Hello, world</a>'
        )
