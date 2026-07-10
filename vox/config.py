"""Configuration loader."""

import os
from pathlib import Path

try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_config(path: str = None) -> dict:
    config = {"defaults": {"voice": "en_US-male1", "rate": 1.0}}
    if not HAS_YAML:
        return config

    search = [path] if path else [
        os.path.expanduser("~/.config/vox/config.yaml"),
        "/etc/vox/config.yaml",
    ]
    for p in search:
        if p and Path(p).exists():
            try:
                with open(p) as f:
                    user = yaml.safe_load(f)
                    if user and isinstance(user, dict):
                        config.update(user)
            except Exception:
                pass
    return config
