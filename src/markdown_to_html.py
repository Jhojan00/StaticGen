from collections.abc import Callable

from htmlnode import HTMLNode
from markdown_blocks import BlockType, block_to_block_type, markdown_to_blocks
from parentnode import ParentNode
from text_to_text_nodes import text_to_text_nodes
from textnode import TextNode, TextType, text_node_to_html_node


def text_to_children(text: str) -> list[HTMLNode]:
    text_nodes = text_to_text_nodes(text)
    html_nodes = [text_node_to_html_node(node) for node in text_nodes]

    return html_nodes


def split_apply(block: str, key: Callable[[str], str], sep="\n") -> list[str]:
    result = []
    for line in block.split(sep):
        result.append(key(line))

    return result


def block_to_html_node(block: str) -> HTMLNode:
    typ = block_to_block_type(block)

    match typ:
        case BlockType.PARAGRAPH:
            trim = block.replace("\n", " ")
            children = text_to_children(trim)
            return ParentNode("p", children)

        case BlockType.HEADING:
            level = 0
            for i in range(len(block)):
                if block[i] != "#" or i > 5:
                    break

                level = i + 1

            trim = block.removeprefix("#" * level).strip()
            children = text_to_children(trim)
            return ParentNode(f"h{level}", children)

        case BlockType.CODE:
            trim = block.removeprefix("```\n").removesuffix("```")
            node = TextNode(trim, TextType.CODE)
            leaf = text_node_to_html_node(node)
            return ParentNode("pre", [leaf])

        case BlockType.QUOTE:
            trim = split_apply(block, lambda e: e[1:].strip())
            trim = " ".join(trim)
            children = text_to_children(trim)
            return ParentNode("blockquote", children)

        case BlockType.UNORDERED_LIST:
            trim = split_apply(block, lambda e: e[1:].strip())
            children = [ParentNode("li", text_to_children(t)) for t in trim]
            return ParentNode("ul", children)

        case BlockType.ORDERED_LIST:
            trim = split_apply(block, lambda e: e.split(" ", 1)[1].strip())
            children = [ParentNode("li", text_to_children(t)) for t in trim]
            return ParentNode("ol", children)


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    nodes: list[HTMLNode] = []

    for block in blocks:
        node = block_to_html_node(block)
        nodes.append(node)

    main = ParentNode("div", nodes)

    return main
