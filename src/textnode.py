from htmlnode import HTMLNode
from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not (isinstance(other, TextNode)):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:

    tag = None
    value = text_node.text
    props = None
    url = text_node.url if text_node.url is not None else ""

    if text_node.text_type == TextType.BOLD:
        tag = "b"

    elif text_node.text_type == TextType.ITALIC:
        tag = "i"

    elif text_node.text_type == TextType.CODE:
        tag = "code"

    elif text_node.text_type == TextType.LINK:
        tag = "a"
        props = {"href": url}

    elif text_node.text_type == TextType.IMAGE:
        tag = "img"
        props = {"src": url, "alt": value}
        value = ""

    return LeafNode(tag, value, props)
