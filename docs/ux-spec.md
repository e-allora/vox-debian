# UX/CLI Spec: vox

**Stage 3 — UX/CLI**
**Skill:** debian-ux-skill

## Command Structure
```
vox <command> [options] [file]

Commands:
  speak       Read a document aloud
  info        Show document metadata
  list-voices List available Piper voices
  help        Show help

Options (speak):
  --rate FLOAT      Speech rate (0.5-3.0, default 1.0)
  --voice STRING    Voice ID (e.g. en_US-male1)
  --start N         Start at paragraph N
```

## Interaction Flow
```
$ vox speak book.epub
[INFO] Title: The Great Gatsby
[INFO] Author: F. Scott Fitzgerald
[INFO] Paragraphs: 842 | Estimated: 4h 12m
[SPEAKING] Paragraph 1/842
─────────────────────────────────
Controls: [space] pause  [←→] seek  [q] quit
─────────────────────────────────

[User presses space]
[PAUSED] Paragraph 47/842  [space] resume  [q] quit

[User presses →]
[SPEAKING] Paragraph 48/842

[User presses q]
[INFO] Stopped at paragraph 48/842
```

## Output Formats

### speak
- Default: plain text status lines
- `--json`: machine-readable JSON output
- `--quiet`: suppress status, only speak

### info
```
$ vox info document.pdf
Title: My Document
Author: Unknown
Pages: 42
Word count: 12,450
Estimated duration: 1h 23m
Format: PDF
```

### list-voices
```
$ vox list-voices
en_US-male1    English (US) Male 1
en_US-female1  English (US) Female 1
en_GB-male1    English (UK) Male 1
```

## Error Messages
```
$ vox speak missing.xyz
[ERROR] Unsupported format: .xyz
[ERROR] Supported: .txt .md .pdf .epub
Exit code: 2

$ vox speak /nonexistent/file.txt
[ERROR] File not found: /nonexistent/file.txt
Exit code: 1

$ vox speak
[ERROR] Missing required argument: file
Usage: vox speak [options] <file>
Exit code: 2
```

## Exit Codes
| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Runtime error (file read, TTS engine failure) |
| 2 | Invalid arguments or unsupported format |

## Configuration
```yaml
# ~/.config/vox/config.yaml
defaults:
  voice: en_US-male1
  rate: 1.0

output:
  module: piper          # speech-dispatcher output module
  device: default        # pulseaudio device
```

## Man Page Outline
```
VOX(1)                    General Commands Manual                   VOX(1)

NAME
       vox — CLI text-to-speech reader

SYNOPSIS
       vox speak [--rate FLOAT] [--voice ID] [--start N] file
       vox info file
       vox list-voices

DESCRIPTION
       Vox reads text, PDF, EPUB, and Markdown files aloud using
       the Piper neural text-to-speech engine via Speech Dispatcher.

OPTIONS
       --rate FLOAT    Speech rate (0.5-3.0)
       --voice ID      Piper voice identifier
       --start N       Start at paragraph N
       --json          Machine-readable output
       --quiet         Suppress status messages

FILES
       ~/.config/vox/config.yaml    User configuration
       /etc/vox/config.yaml         System defaults

EXIT STATUS
       0    Success
       1    Runtime error
       2    Invalid arguments

SEE ALSO
       spd-say(1), piper(1), speech-dispatcher(7)
```
