import unittest

from extract import extract_markdown_images, extract_markdown_links, extract_title


class TextExtract(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        )

        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_none_markdown_images(self):
        matches = extract_markdown_images(
            "This is a text with no images, this is just a ! [link](https://link.link)"
        )

        self.assertListEqual([], matches)

    def test_extract_wrong_images(self):
        matches = extract_markdown_images(
            "This text is supposed to have a valid ![image](https://oops.png but it doesn't."
        )

        self.assertListEqual([], matches)

    def test_extract_wrong_and_valid_images(self):
        matches = extract_markdown_images(
            "This text has an invalid ![image](https://ops.webp and a valid ![image](https://ok.png)"
        )

        self.assertListEqual([("image", "https://ok.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with only one link [hello world](https://hello.world.com)"
        )

        self.assertListEqual([("hello world", "https://hello.world.com")], matches)

    def test_extract_multiple_markdown_links(self):
        matches = extract_markdown_links(
            "This i text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )

        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_extract_none_markdown_links(self):
        matches = extract_markdown_links(
            "This is a text with no links this is just an ![image](~/Pictures/ScreenShots/boots.png)"
        )

        self.assertListEqual([], matches)

    def test_extract_wrong_links(self):
        matches = extract_markdown_links(
            "This text is supposed to have a valid [link](https://oops.com.uk but it doesn't."
        )

        self.assertListEqual([], matches)

    def test_extract_wrong_and_valid_links(self):
        matches = extract_markdown_links(
            "This text has an invalid [link](https://ops.webp and a valid [link](https://ok.com)"
        )

        self.assertListEqual([("link", "https://ok.com")], matches)

    def test_extract_title(self):
        md = """
# This is a title

This is not, and should be ignored.

# Too late.
"""
        title = extract_title(md)

        self.assertEqual(title, "This is a title")

    def test_extract_title_at_the_end(self):
        md = """
## This is not a title

This is not, and should be ignored.

# Too late.
"""
        title = extract_title(md)

        self.assertEqual(title, "Too late.")

    def test_extract_title_no_title(self):
        md = """
## This is not a valid title

This should be ignored.

"""

        self.assertRaises(ValueError, extract_title, md)

    def test_extract_title_with_spaces(self):
        md = """
## This is not a title

This is not, and should be ignored.

  # This is a title.   
"""
        title = extract_title(md)

        self.assertEqual(title, "This is a title.")
