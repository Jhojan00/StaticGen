from extract import extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    result: list[TextNode] = []

    for old in old_nodes:
        if old.text_type != TextType.TEXT:
            result.append(old)
            continue

        split = old.text.split(delimiter)

        for i in range(len(split)):
            if not split[i]:
                continue

            node = TextNode(split[i], TextType.TEXT)

            if i % 2 == 1:
                node.text_type = text_type

            result.append(node)

    return result


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []

    for node in old_nodes:
        if not node.text:
            continue

        images = extract_markdown_images(node.text)
        if not images:
            result.append(node)

        current_text = node.text
        for image in images:
            split = current_text.split("![{}]({})".format(*image), maxsplit=1)
            first, rest = split

            if first:
                new_node = TextNode(first, TextType.TEXT)
                result.append(new_node)

            image_node = TextNode(image[0], TextType.IMAGE, image[1])

            result.append(image_node)

            current_text = rest

            if (
                image == images[-1] and rest
            ):  # In case there is more text after the image.
                new_node = TextNode(rest, TextType.TEXT)
                result.append(new_node)

    return result


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    result: list[TextNode] = []

    for node in old_nodes:
        if not node.text:
            continue

        links = extract_markdown_links(node.text)
        if not links:
            result.append(node)

        current_text = node.text
        for link in links:
            split = current_text.split("[{}]({})".format(*link), maxsplit=1)
            first, rest = split

            if first:
                new_node = TextNode(first, TextType.TEXT)
                result.append(new_node)

            link_node = TextNode(link[0], TextType.LINK, link[1])

            result.append(link_node)

            current_text = rest

            if link == links[-1] and rest:
                new_node = TextNode(rest, TextType.TEXT)
                result.append(new_node)

    return result
