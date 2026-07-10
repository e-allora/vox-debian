"""Document reader: detects format and delegates to the right parser."""

import os
from pathlib import Path
from typing import Dict, List

from .parsers.text import parse_text
from .parsers.markdown import parse_markdown
from .parsers.pdf import parse_pdf
from .parsers.epub import parse_epub


class Reader:
    def __init__(self, path: str):
        self.path = Path(path)
        if not self.path.exists():
            raise FileNotFoundError(f"File not found: {path}")
        ext = self.path.suffix.lower()
        parsers = {
            ".txt": parse_text,
            ".md": parse_markdown,
            ".pdf": parse_pdf,
            ".epub": parse_epub,
        }
        if ext not in parsers:
            supported = ", ".join(parsers)
            raise ValueError(f"Unsupported format: {ext}\nSupported: {supported}")
        self.parser = parsers[ext]
        self._paragraphs = None
        self._meta = None

    def _parse(self):
        if self._paragraphs is None:
            self._paragraphs, self._meta = self.parser(str(self.path))

    def paragraphs(self) -> List[str]:
        self._parse()
        return self._paragraphs

    def metadata(self) -> Dict:
        self._parse()
        word_count = sum(len(p.split()) for p in self._paragraphs)
        minutes = max(1, round(word_count / 150))
        h, m = divmod(minutes, 60)
        duration = f"{h}h {m}m" if h else f"{m}m"
        return {
            "title": self._meta.get("title", self.path.stem),
            "author": self._meta.get("author", "Unknown"),
            "paragraphs": len(self._paragraphs),
            "word_count": word_count,
            "duration": duration,
            "format": self.path.suffix.upper().lstrip("."),
            **{k: v for k, v in self._meta.items() if k in ("pages",)},
        }
