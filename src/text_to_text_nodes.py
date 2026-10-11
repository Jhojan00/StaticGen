from splitter import split_nodes_delimiter, split_nodes_image, split_nodes_link
from textnode import TextNode, TextType


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_link(
        nodes,
    )

    nodes = split_nodes_image(
        nodes,
    )

    types: dict[str, TextType] = {
        "`": TextType.CODE,
        "**": TextType.BOLD,
        "_": TextType.ITALIC,
    }

    for deli, typ in types.items():
        nodes = split_nodes_delimiter(nodes, deli, typ)

    return nodes
