import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from vox.parsers.text import parse_text
from vox.reader import Reader


def test_text_parser():
    paras, meta = parse_text("/tmp/test.txt")
    assert len(paras) == 3
    assert "second paragraph" in paras[1]


def test_reader_unsupported():
    try:
        Reader("/tmp/test.xyz")
        assert False, "Should have raised"
    except ValueError as e:
        assert "Unsupported format" in str(e)


def test_reader_text():
    r = Reader("/tmp/test.txt")
    meta = r.metadata()
    assert meta["paragraphs"] == 3
    assert meta["format"] == "TXT"
