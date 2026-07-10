"""EPUB parser using ebooklib."""

from typing import List, Tuple, Dict
from html.parser import HTMLParser


class _TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip = False

    def handle_starttag(self, tag, attrs):
        if tag in ("script", "style"):
            self.skip = True

    def handle_endtag(self, tag):
        if tag in ("script", "style"):
            self.skip = False
        if tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6"):
            self.text.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.text.append(data)


def parse_epub(path: str) -> Tuple[List[str], Dict]:
    try:
        from ebooklib import epub
    except ImportError:
        raise RuntimeError(
            "ebooklib is required for EPUB support.\n"
            "Install: pip install ebooklib"
        )

    book = epub.read_epub(path)
    title = book.get_metadata("DC", "title")
    author = book.get_metadata("DC", "creator")

    full_text = []
    for item in book.get_items_of_type(9):
        extractor = _TextExtractor()
        extractor.feed(item.get_content().decode("utf-8", errors="replace"))
        full_text.append("".join(extractor.text))

    text = "\n".join(full_text)
    paragraphs = [p.strip() for p in text.split("\n") if p.strip()]

    return paragraphs, {
        "title": title[0][0] if title else None,
        "author": author[0][0] if author else None,
    }
