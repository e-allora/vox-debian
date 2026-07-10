"""PDF parser using PyMuPDF (fitz)."""

from typing import List, Tuple, Dict


def parse_pdf(path: str) -> Tuple[List[str], Dict]:
    try:
        import fitz
    except ImportError:
        raise RuntimeError(
            "PyMuPDF (fitz) is required for PDF support.\n"
            "Install: sudo apt install python3-pymupdf"
        )

    doc = fitz.open(path)
    meta = {
        "title": doc.metadata.get("title") or None,
        "author": doc.metadata.get("author") or None,
        "pages": doc.page_count,
    }

    paragraphs = []
    for page in doc:
        text = page.get_text("text")
        for para in text.split("\n\n"):
            cleaned = para.strip().replace("\n", " ")
            if cleaned:
                paragraphs.append(cleaned)

    doc.close()
    return paragraphs, meta
