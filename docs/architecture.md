# Architecture: vox

**Stage 2 — Architecture**
**Skill:** debian-architecture-skill

## Module Structure
```
vox/
├── __init__.py
├── __main__.py          # entry point: python3 -m vox
├── cli.py               # argparse CLI: vox speak/info/list-voices
├── reader.py            # core reader: parse → segment → speak
├── parsers/
│   ├── __init__.py
│   ├── text.py          # plain text parser
│   ├── markdown.py      # markdown parser (mistune)
│   ├── pdf.py           # PDF parser (pymupdf)
│   └── epub.py          # EPUB parser (ebooklib)
├── speaker.py           # TTS backend: spd-say wrapper
└── config.py            # YAML config loading
```

## Data Flow
```
File → Parser (text/md/pdf/epub) → [Paragraph] list → Speaker (spd-say per paragraph)
                                                              ↓
                                                         Keyboard input (pause/seek/quit)
```

## Dependency Graph
```
vox cli → reader → parsers (text|md|pdf|epub)
                → speaker → spd-say → speech-dispatcher → piper
                → config  → PyYAML
```

## ADRs

### ADR-1: Python
**Status:** Accepted
**Context:** Need PDF/EPUB parsing, CLI handling, TTS integration.
**Decision:** Python 3.11+ with setuptools.
**Consequences:** Rich ecosystem (pymupdf, ebooklib, mistune), subprocess for spd-say.
**Alternatives:** Rust (fewer doc parsing libs), Go (no mature PDF lib).

### ADR-2: spd-say over direct piper binary
**Status:** Accepted
**Context:** Piper is installed via snap (pied), binary isn't directly accessible.
**Decision:** Use `spd-say` (Speech Dispatcher CLI) which already has Piper as output module.
**Consequences:** Voice management handled by pied/speech-dispatcher, simpler code, no snap sandbox issues.

### ADR-3: Interactive CLI with raw terminal input
**Status:** Accepted
**Context:** Need keyboard controls during playback (pause, seek, quit).
**Decision:** Use `termios`/`tty` for raw terminal mode during playback. Read stdin in a thread.
**Consequences:** Works on any terminal, no curses dependency, handles signals cleanly.

## FHS File Placement
| Path | Purpose |
|------|---------|
| `/usr/bin/vox` | Main entry point (symlink to python script) |
| `/etc/vox/config.yaml` | System-wide defaults |
| `~/.config/vox/config.yaml` | User overrides |
| `/usr/share/doc/vox/` | README, changelog, copyright |
| `/usr/share/man/man1/vox.1` | Man page |
