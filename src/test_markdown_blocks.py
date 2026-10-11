import unittest

from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks


class TestMarkdownConverter(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_many_newlines_to_block(self):
        md = """
This is **bolded** paragraph
\n\n\n\n


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line
\n\n\n
- This is a list
- with items
\n\n\n\n
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_with_whitespaces_to_block(self):
        md = """
      This is **bolded** paragraph    

   This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_header(self):
        blocks = {
            "# H1": BlockType.HEADING,
            "# #H1": BlockType.HEADING,
            "## H2": BlockType.HEADING,
            "### H3": BlockType.HEADING,
            "#### H4": BlockType.HEADING,
            "##### H5": BlockType.HEADING,
            "###### H6": BlockType.HEADING,
            "####### :(": BlockType.PARAGRAPH,
            "###-### :(": BlockType.PARAGRAPH,
            "### -### H3": BlockType.HEADING,
        }

        types: list[BlockType] = []

        for block in blocks:
            types.append(block_to_block_type(block))

        self.assertListEqual(types, list(blocks.values()))

    def test_block_to_block_type_code(self):
        blocks = {
            "```\nprint('Hello world')\n```": BlockType.CODE,
            "```\nprint('Hello world')\nprint('bye world')\n```": BlockType.CODE,
            "```\nprint(':(')```": BlockType.PARAGRAPH,
            "```print(':(')```": BlockType.PARAGRAPH,
        }

        types: list[BlockType] = []

        for block in blocks:
            types.append(block_to_block_type(block))

        self.assertListEqual(types, list(blocks.values()))

    def test_block_to_block_type_quote(self):
        blocks = {
            ">a\n>b\n>c": BlockType.QUOTE,
            ">a\n> b\n> c": BlockType.QUOTE,
            ">a\n\n> c": BlockType.PARAGRAPH,
        }

        types: list[BlockType] = []

        for block in blocks:
            types.append(block_to_block_type(block))

        self.assertListEqual(types, list(blocks.values()))

    def test_block_to_block_type_unordered_list(self):
        blocks = {
            "- a\n- b\n- c": BlockType.UNORDERED_LIST,
            "-a\n-b\n-c": BlockType.PARAGRAPH,
            "- a\n\n- c": BlockType.PARAGRAPH,
        }

        types: list[BlockType] = []

        for block in blocks:
            types.append(block_to_block_type(block))

        self.assertListEqual(types, list(blocks.values()))

    def test_block_to_block_type_ordered_list(self):
        blocks = {
            "1. a\n2. b\n3. c": BlockType.ORDERED_LIST,
            "2. a\1. b\n3. c": BlockType.PARAGRAPH,
            "1. a\n\n2. c": BlockType.PARAGRAPH,
        }

        types: list[BlockType] = []

        for block in blocks:
            types.append(block_to_block_type(block))

        self.assertListEqual(types, list(blocks.values()))
