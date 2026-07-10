# PRD: vox — CLI TTS Reader for Debian

**Stage 1 — Product**
**Skill:** debian-product-skill
**Date:** 2026-07-09

## Problem Statement
Users on Debian/Ubuntu want to listen to documents (text, markdown, PDF, EPUB)
through their system's Piper neural TTS engine without a GUI. Existing solutions
are either GUI-only or don't support all document formats.

## Target Audience
- Linux desktop users who prefer the terminal
- Visually impaired users relying on screen readers
- Power users who want to batch-process documents to audio
- Server admins who need TTS in headless environments

## User Stories

| ID | As a... | I want to... | So that... |
|----|---------|-------------|-----------|
| US-1 | User | Read a text file aloud | I can listen to plain text documents |
| US-2 | User | Read a PDF aloud | I can listen to academic papers and reports |
| US-3 | User | Read an EPUB aloud | I can listen to ebooks |
| US-4 | User | Read Markdown aloud | I can listen to documentation and notes |
| US-5 | User | Pause and resume playback | I can take breaks without losing my place |
| US-6 | User | Skip forward/backward by paragraph | I can navigate within a document |
| US-7 | User | Select voice and rate | I can customize the listening experience |
| US-8 | User | Get document metadata | I know what I'm about to listen to |

## Acceptance Criteria
- `vox speak file.txt` — reads the file aloud, exits when done
- `vox speak file.pdf` — extracts text via PyMuPDF, reads aloud
- `vox speak file.epub` — extracts text via ebooklib, reads aloud
- `vox speak file.md` — parses markdown, reads formatted text
- Space bar pauses/resumes during playback
- Left/right arrows seek backward/forward by paragraph
- `vox --rate 1.5 --voice en_US-male1 file.txt` customizes output
- `vox info file.epub` — prints title, author, word count, estimated duration

## MoSCoW Backlog
- **Must:** US-1, US-2, US-3, US-5, US-6, US-8 (core reader)
- **Should:** US-4 (markdown), US-7 (voice selection)
- **Could:** Batch processing, output to WAV file, progress bar
- **Won't:** GUI, network streaming, cloud sync

## Non-Functional Requirements
- Cold start < 500ms for a 100KB text file
- Memory < 50MB for a 100-page PDF
- Works on headless systems (no X11 dependencies)
- Exit code 0 on success, 1 on error, 2 on invalid args
