import importlib.util
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / ".claude" / "skills" / "smart-learn"


def load_runtime_utils():
    spec = importlib.util.spec_from_file_location(
        "runtime_utils", SKILL_DIR / "runtime_utils.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_safe_slug_blocks_path_traversal():
    runtime = load_runtime_utils()
    slug = runtime.safe_slug("../../CON")
    assert slug
    assert "/" not in slug
    assert "\\" not in slug
    assert ".." not in slug
    assert not slug.upper().startswith("CON")


def test_atomic_write_text_creates_parent(tmp_path):
    runtime = load_runtime_utils()
    target = tmp_path / "nested" / "note.md"
    runtime.atomic_write_text(target, "hello")
    assert target.read_text(encoding="utf-8") == "hello"
    assert not list(target.parent.glob("*.tmp"))


def test_mindmap_init_uses_safe_filename(tmp_path):
    result = subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "mindmap_utils.py"),
            "init",
            "--topic",
            "../../CON",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["status"] == "ok"
    for key in ("mindmap_file", "data_file"):
        path = Path(payload[key])
        assert path.parent == tmp_path
        assert ".." not in path.name
        assert not path.name.upper().startswith("CON")


def test_mindmap_rejects_unknown_step(tmp_path):
    init = subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "mindmap_utils.py"),
            "init",
            "--topic",
            "demo",
            "--output-dir",
            str(tmp_path),
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    init_payload = json.loads(init.stdout.strip().splitlines()[-1])
    result = subprocess.run(
        [
            sys.executable,
            str(SKILL_DIR / "mindmap_utils.py"),
            "update",
            "--file",
            init_payload["mindmap_file"],
            "--data-file",
            init_payload["data_file"],
            "--step",
            "99",
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    payload = json.loads(result.stdout.strip().splitlines()[-1])
    assert payload["status"] == "error"
    assert payload["code"] == "INVALID_STEP"
