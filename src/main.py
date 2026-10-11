import shutil
import sys
from pathlib import Path

from generation import generate_pages_recursively


def copy_contents(source: Path, target: Path) -> None:
    def helper(source: Path, target: Path) -> None:
        if source.is_file():
            source.copy_into(target)
            print(f"{source} -> {target}")
            return

        for entry in source.iterdir():
            child = Path(*entry.parts[1:])
            sub_dir = target

            if entry.is_dir():
                sub_dir = target / child
                sub_dir.mkdir()

            helper(entry, sub_dir)

    if not source.exists():
        raise OSError(f"Source {source} does not exists.")

    if target.exists():
        shutil.rmtree(target)

    target.mkdir()

    return helper(source, target)


def main():
    basepath = Path("/")
    if len(sys.argv) >= 2:
        basepath = Path(sys.argv[1])

    copy_contents(Path("static/"), Path("docs/"))
    generate_pages_recursively(
        Path("content/"), Path("template.html"), Path("docs/"), basepath
    )


if __name__ == "__main__":
    main()
