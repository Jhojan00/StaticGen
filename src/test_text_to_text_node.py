import unittest

from text_to_text_nodes import text_to_text_nodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_text_only(self):
        text = "This is text, just normal text."
        split = text_to_text_nodes(text)

        self.assertListEqual([TextNode(text, TextType.TEXT)], split)

    def test_specific_type(self):
        text = "**This is text, just bold text.**"
        split = text_to_text_nodes(text)

        self.assertListEqual(
            [TextNode("This is text, just bold text.", TextType.BOLD)], split
        )

    def test_multiple_text_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        split = text_to_text_nodes(text)

        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            split,
        )
