"""Tests for vox parsers and reader."""

import os
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vox.parsers.text import parse_text
from vox.reader import Reader


def _write_temp_file(name: str, content: str) -> str:
    p = Path(tempfile.gettempdir()) / name
    p.write_text(content)
    return str(p)


def test_text_parser():
    path = _write_temp_file("vox_test.txt", "Hello world.\n\nSecond paragraph.\n\nThird one.")
    paras, meta = parse_text(path)
    assert len(paras) == 3
    assert "Second paragraph" in paras[1]


def test_reader_unsupported():
    path = _write_temp_file("vox_test.xyz", "dummy")
    try:
        Reader(path)
        assert False, "Should have raised"
    except ValueError as e:
        assert "Unsupported format" in str(e)


def test_reader_text():
    path = _write_temp_file("vox_test2.txt", "Para one.\n\nPara two.")
    r = Reader(path)
    meta = r.metadata()
    assert meta["paragraphs"] == 2
    assert meta["format"] == "TXT"
