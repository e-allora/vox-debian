"""Plain text parser."""

from typing import List, Tuple, Dict


def parse_text(path: str) -> Tuple[List[str], Dict]:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    return paragraphs, {"title": None, "author": None}
