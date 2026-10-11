import re


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    pattern = r"(?<!\!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return re.findall(pattern, text)


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            return line.removeprefix("# ").strip()

    raise ValueError("Not title found, please add at least one header.")
