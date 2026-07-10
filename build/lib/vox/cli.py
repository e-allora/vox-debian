"""vox — CLI TTS reader for Debian using Piper via Speech Dispatcher."""

import argparse
import sys
from .reader import Reader
from .speaker import PiperSpeaker
from .config import load_config


def main():
    parser = argparse.ArgumentParser(
        prog="vox",
        description="CLI text-to-speech reader for text, markdown, PDF, and EPUB files.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sp = sub.add_parser("speak", help="Read a document aloud")
    sp.add_argument("file", help="Document to read")
    sp.add_argument("--rate", type=float, default=1.0, help="Speech rate (0.5-3.0)")
    sp.add_argument("--voice", help="Piper voice ID (e.g. en_US-male1)")
    sp.add_argument("--start", type=int, default=0, help="Start at paragraph N")
    sp.add_argument("--json", action="store_true", help="Machine-readable output")
    sp.add_argument("--quiet", action="store_true", help="Suppress status messages")

    info = sub.add_parser("info", help="Show document metadata")
    info.add_argument("file", help="Document to inspect")
    info.add_argument("--json", action="store_true")

    sub.add_parser("list-voices", help="List available Piper voices")

    args = parser.parse_args()
    config = load_config()

    if args.command == "list-voices":
        speaker = PiperSpeaker()
        for v in speaker.list_voices():
            print(f"{v['id']:20s} {v['name']}")
        return 0

    reader = Reader(args.file)
    meta = reader.metadata()

    if args.command == "info":
        if getattr(args, "json", False):
            import json

            print(json.dumps(meta))
        else:
            print(f"Title:     {meta['title']}")
            print(f"Author:    {meta['author']}")
            if meta.get("pages"):
                print(f"Pages:     {meta['pages']}")
            print(f"Paragraphs:{meta['paragraphs']}")
            print(f"Estimated: {meta['duration']}")

        return 0

    # speak
    speaker = PiperSpeaker(
        rate=getattr(args, "rate", config.get("defaults", {}).get("rate", 1.0)),
        voice=getattr(args, "voice", None)
        or config.get("defaults", {}).get("voice", "en_US-male1"),
    )

    if not getattr(args, "quiet", False):
        print(f"[INFO] {meta['title']} — {meta['author']}")
        print(f"[INFO] Paragraphs: {meta['paragraphs']} | Estimated: {meta['duration']}")

    paragraphs = reader.paragraphs()
    start = getattr(args, "start", 0)

    try:
        speaker.speak(paragraphs, start=start, quiet=getattr(args, "quiet", False))
    except KeyboardInterrupt:
        pass

    return 0


if __name__ == "__main__":
    sys.exit(main())
