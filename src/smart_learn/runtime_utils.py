"""Runtime safety helpers for Smart Learn.

This module is intentionally dependency-free and safe for the Claude Code
skill's copied .claude directory.
"""

import hashlib
import json
import os
import re
import tempfile
from pathlib import Path

WINDOWS_RESERVED = {
    "CON", "PRN", "AUX", "NUL",
    "COM1", "COM2", "COM3", "COM4", "COM5", "COM6", "COM7", "COM8", "COM9",
    "LPT1", "LPT2", "LPT3", "LPT4", "LPT5", "LPT6", "LPT7", "LPT8", "LPT9",
}


def safe_slug(text, max_len=60):
    """Return a filesystem-safe, stable topic slug.

    The original topic remains inside generated file contents; this value is
    only used for filenames. A short hash prevents collisions after cleanup.
    """
    raw = str(text).strip()
    name = re.sub(r'[\\/:*?"<>|\x00-\x1f]+', "_", raw)
    name = name.replace("..", "_")
    name = re.sub(r"\s+", "_", name).strip("._ ")
    if not name:
        name = "topic"
    if name.upper() in WINDOWS_RESERVED:
        name = "_" + name
    digest = hashlib.md5(raw.encode("utf-8")).hexdigest()[:6]
    return f"{name[:max(1, max_len)]}_{digest}"


def atomic_write_text(path, text, encoding="utf-8"):
    """Write text through a same-directory temporary file and os.replace."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        dir=str(target.parent),
        prefix=f".{target.name}.",
        suffix=".tmp",
    )
    try:
        with os.fdopen(fd, "w", encoding=encoding) as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, target)
    finally:
        try:
            if os.path.exists(temp_name):
                os.unlink(temp_name)
        except OSError:
            pass


def atomic_write_json(path, data):
    atomic_write_text(path, json.dumps(data, ensure_ascii=False, indent=2))


def error_payload(code, message, hint=None):
    payload = {"status": "error", "code": code, "message": str(message)}
    if hint:
        payload["hint"] = hint
    return payload
