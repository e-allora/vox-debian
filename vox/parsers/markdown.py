"""Markdown parser using mistune or plain text fallback."""

from typing import List, Tuple, Dict


def parse_markdown(path: str) -> Tuple[List[str], Dict]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    try:
        import mistune

        md = mistune.create_markdown(renderer=None)
        text = mistune.html_to_text(md(content))
    except ImportError:
        text = content

    # Split into paragraphs, skip empty lines and headings without body
    lines = text.split("\n")
    paragraphs = []
    buf = []
    for line in lines:
        stripped = line.strip()
        if stripped == "" and buf:
            paragraphs.append(" ".join(buf))
            buf = []
        elif stripped and not stripped.startswith("#"):
            buf.append(stripped)
    if buf:
        paragraphs.append(" ".join(buf))

    if not paragraphs:
        paragraphs = [text.strip()]

    # Try to extract title from first heading
    title = None
    for line in content.split("\n"):
        if line.startswith("# "):
            title = line[2:].strip()
            break

    return paragraphs, {"title": title, "author": None}
