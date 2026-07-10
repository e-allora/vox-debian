# Test Plan: vox

**Stage 6 — QA**
**Skill:** debian-qa-skill

## Test Pyramid
```
/UI\          0 (CLI only, no GUI)
/--\
/Int\         3: info, list-voices, speak (integration with spd-say)
/----\
/Unit\        5: text/md/pdf/epub parsers + Reader class
/------\
```

## Unit Tests
| Test | What it verifies |
|------|-----------------|
| `test_text_parser` | Plain text split into paragraphs |
| `test_markdown_parser` | MD heading extraction, paragraph grouping |
| `test_reader_detection` | Format detection from file extension |
| `test_reader_unsupported` | Error on unknown format |
| `test_config_defaults` | Default config when no file exists |

## Integration Tests
| Test | What it verifies |
|------|-----------------|
| `test_info_command` | Metadata extraction for known formats |
| `test_list_voices` | spd-say voice enumeration |
| `test_speak_quiet` | Non-TTY speak completes without error |

## CI Pipeline
```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: pip install -e ".[all]"
      - run: pip install pytest
      - run: python3 -m pytest tests/ -v
      - run: shellcheck debian/rules
```
