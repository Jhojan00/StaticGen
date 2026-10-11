import unittest

from splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_bold_split(self):
        node = TextNode("Hello, **beautiful** world.", TextType.TEXT)
        parsed = split_nodes_delimiter([node], "**", TextType.BOLD)

        self.assertEqual(
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("beautiful", TextType.BOLD),
                TextNode(" world.", TextType.TEXT),
            ],
            parsed,
        )

    def test_italic_split(self):
        node = TextNode("Hello, _beautiful_ world.", TextType.TEXT)
        parsed = split_nodes_delimiter([node], "_", TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("beautiful", TextType.ITALIC),
                TextNode(" world.", TextType.TEXT),
            ],
            parsed,
        )

    def test_code_split(self):
        node = TextNode("Hello, `print('beautiful')` world.", TextType.TEXT)
        parsed = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("print('beautiful')", TextType.CODE),
                TextNode(" world.", TextType.TEXT),
            ],
            parsed,
        )

    def test_multiple_nodes(self):
        node = TextNode("Hello, _beautiful_ world.", TextType.TEXT)
        node2 = TextNode("Good afternoon, beautiful world.", TextType.TEXT)
        node3 = TextNode("_Bye_, _horrible_ _world_.", TextType.TEXT)
        parsed = split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("Hello, ", TextType.TEXT),
                TextNode("beautiful", TextType.ITALIC),
                TextNode(" world.", TextType.TEXT),
                TextNode("Good afternoon, beautiful world.", TextType.TEXT),
                TextNode("Bye", TextType.ITALIC),
                TextNode(", ", TextType.TEXT),
                TextNode("horrible", TextType.ITALIC),
                TextNode(" ", TextType.TEXT),
                TextNode("world", TextType.ITALIC),
                TextNode(".", TextType.TEXT),
            ],
            parsed,
        )

    def test_specific_nodes(self):
        node = TextNode("Hello, world.", TextType.ITALIC)
        node2 = TextNode("Good afternoon, beautiful world.", TextType.BOLD)
        node3 = TextNode("print('bye horrible world'", TextType.CODE)
        parsed = split_nodes_delimiter([node, node2, node3], "_", TextType.ITALIC)

        self.assertEqual(
            [
                TextNode("Hello, world.", TextType.ITALIC),
                TextNode("Good afternoon, beautiful world.", TextType.BOLD),
                TextNode("print('bye horrible world'", TextType.CODE),
            ],
            parsed,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_with_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_images_no_more_text(self):
        node = TextNode("![image](https://just_an_image.png)", TextType.TEXT)

        new_nodes = split_nodes_image([node])

        self.assertListEqual(
            [TextNode("image", TextType.IMAGE, "https://just_an_image.png")], new_nodes
        )

    def test_split_links_with_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [node],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links_no_more_text(self):
        node = TextNode("[link](https://just_a_link.png)", TextType.TEXT)

        new_nodes = split_nodes_link([node])

        self.assertListEqual(
            [TextNode("link", TextType.LINK, "https://just_a_link.png")], new_nodes
        )
