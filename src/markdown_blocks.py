import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"


def markdown_to_blocks(markdown: str) -> list[str]:
    result = markdown.split("\n\n")
    result = [stripped for block in result if (stripped := block.strip())]

    return result


def block_to_block_type(block: str) -> BlockType:
    result: BlockType = BlockType.PARAGRAPH

    if re.match(r"^#{1,6}\s.+", block):
        result = BlockType.HEADING

    elif re.match(r"^```\r?\n.*?$\r?\n```", block, re.MULTILINE + re.DOTALL):
        result = BlockType.CODE

    elif block.startswith(">"):
        for part in block.split("\n"):
            if not part.startswith(">"):
                break
        else:
            result = BlockType.QUOTE

    elif block.startswith("- "):
        for part in block.split("\n"):
            if not part.startswith("- "):
                break

        else:
            result = BlockType.UNORDERED_LIST

    elif block.startswith("1. "):
        for i, s in enumerate(block.split("\n")):
            if not s.startswith(f"{i + 1}. "):
                break

        else:
            result = BlockType.ORDERED_LIST

    return result
