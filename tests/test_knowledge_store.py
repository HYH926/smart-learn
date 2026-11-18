import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from smart_learn.knowledge import get_stats, list_topics


def test_corrupt_file_is_skipped(tmp_path):
    (tmp_path / "good.md").write_text(
        "# Good\n\n## 1. Concept\n\n🎯 核心公式\nKeep learning.\n",
        encoding="utf-8",
    )
    (tmp_path / "bad.md").write_bytes(b"\xff\xfe\x00")
    topics = list_topics(tmp_path)
    assert [item["name"] for item in topics] == ["good"]
    assert get_stats(tmp_path)["total_topics"] == 1
