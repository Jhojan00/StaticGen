from pathlib import Path

from extract import extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(
    from_path: Path, template_path: Path, dest_path: Path, basepath: Path
):
    print(f"Generating page form {from_path} to {dest_path} using {template_path}.")

    with open(from_path, "r") as f:
        markdown = f.read()
        html = markdown_to_html_node(markdown).to_html()
        title = extract_title(markdown)

    with open(template_path, "r") as f:
        dest_html = f.read()
        dest_html = dest_html.replace("{{ Title }}", title)
        dest_html = dest_html.replace("{{ Content }}", html)

        finalpath = str(basepath).strip("/")

        if finalpath:
            dest_html = dest_html.replace('href="/', f'href="/{finalpath}/')
            dest_html = dest_html.replace('src="/', f'src="/{finalpath}/')

    parents = dest_path.parent
    parents.mkdir(parents=True, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(dest_html)


def generate_pages_recursively(
    dir_path_content: Path, template_path: Path, dest_dir_path: Path, basepath: Path
):

    for entry in dir_path_content.iterdir():
        if entry.is_file():
            target = dest_dir_path / Path(entry.stem + ".html")
            generate_page(entry, template_path, target, basepath)

        else:
            target = dest_dir_path / Path(entry.name)
            generate_pages_recursively(entry, template_path, target, basepath)
