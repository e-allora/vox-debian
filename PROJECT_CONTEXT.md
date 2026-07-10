# PROJECT_CONTEXT — vox-debian

> Single source of truth for tech decisions. Update when an ADR changes a decision.

## App Identity
- **Name:** vox
- **Purpose:** CLI text-to-speech reader for text, markdown, PDF, and EPUB files using Piper neural TTS
- **Target distros:** Debian 12 (bookworm), Ubuntu 24.04 LTS
- **Architecture:** amd64
- **License:** MIT

## Tech Stack
- **Language:** Python 3.11+
- **Build system:** setuptools / pyproject.toml
- **Packaging:** dh_make + debhelper compat 13
- **TTS backend:** Piper via Speech Dispatcher (`spd-say`)
- **Testing:** pytest
- **CI:** GitHub Actions (ubuntu-latest)

## Architecture Decisions (ADRs)
- **ADR-1:** Python — best library support for PDF (pymupdf), EPUB (ebooklib), Markdown (stdlib + mistune)
- **ADR-2:** Single binary entry point — `vox` CLI with subcommands
- **ADR-3:** spd-say over direct piper binary — Speech Dispatcher handles voice management, avoids piper snap sandboxing issues
- **ADR-4:** No daemon — interactive CLI with keyboard controls (space=pause, q=quit, arrows=seek)

## Standards
- **Debian Policy:** 4.7.0
- **FHS:** /usr/bin/vox, /etc/vox/config.yaml, /usr/share/doc/vox/
- **Man page:** section 1

## Dependencies
- **Build-Depends:** debhelper-compat (= 13), python3, dh-python
- **Depends:** python3, speech-dispatcher, python3-pymupdf, python3-ebooklib
- **Recommends:** python3-mistune (optional, for markdown parsing)

## Configuration
- **System:** /etc/vox/config.yaml
- **User:** ~/.config/vox/config.yaml
- **Format:** YAML with voice, rate, and output device settings
