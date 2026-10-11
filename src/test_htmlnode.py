import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props(self):
        node = HTMLNode(
            "p",
            "hello world",
            props={"href": "https://hello.world", "target": "_blank"},
        )

        expected = ' href="https://hello.world" target="_blank"'
        html_props = node.props_to_html()

        self.assertEqual(html_props, expected)

    def test_empty_props(self):
        node = HTMLNode("p", "hello world", props={})

        html_props = node.props_to_html()

        self.assertEqual(html_props, "")

    def test_null_props(self):
        node = HTMLNode("p", "hello world", props=None)

        html_props = node.props_to_html()

        self.assertEqual(html_props, "")
