"""Knowledge store management — search, list, and retrieve learning records."""

import os
import re
import json
from pathlib import Path
from datetime import datetime


def list_topics(store_dir="knowledge_store"):
    """列出所有已学主题"""
    store = Path(store_dir)
    if not store.exists():
        return []
    topics = []
    for f in store.glob("*.md"):
        name = f.stem
        if "思维导图" in name or "checkpoint" in name or "mindmap_state" in name:
            continue
        stat = f.stat()
        # 提取核心公式
        core = ""
        content = f.read_text(encoding='utf-8')
        match = re.search(r'🎯\s*核心公式.*?\n(.+)', content)
        if match:
            core = match.group(1).strip()[:80]
        topics.append({
            "name": name,
            "file": str(f),
            "size": stat.st_size,
            "modified": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d"),
            "core_formula": core,
        })
    topics.sort(key=lambda t: t["modified"], reverse=True)
    return topics


def search(query, store_dir="knowledge_store"):
    """跨主题搜索"""
    store = Path(store_dir)
    if not store.exists():
        return {"query": query, "results": []}

    results = []
    for f in store.glob("*.md"):
        if "思维导图" in f.name or "checkpoint" in f.name:
            continue
        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            continue
        if query.lower() in content.lower():
            # 提取上下文
            idx = content.lower().find(query.lower())
            start = max(0, idx - 80)
            end = min(len(content), idx + len(query) + 120)
            snippet = content[start:end].replace('\n', ' ').strip()
            results.append({
                "file": str(f),
                "topic": f.stem,
                "snippet": f"...{snippet}...",
            })

    return {"query": query, "results": results}


def get_weak_points(store_dir="knowledge_store"):
    """获取所有薄弱点及时间戳"""
    store = Path(store_dir)
    weak_points = []
    for f in store.glob("*.md"):
        if "思维导图" in f.name or "checkpoint" in f.name:
            continue
        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            continue
        # 匹配薄弱点格式: - **名称**：说明（首次标记：YYYY-MM-DD）
        for match in re.finditer(r'-\s*\*\*(.+?)\*\*：(.+?)(?:（首次标记：(\d{4}-\d{2}-\d{2})）)?', content):
            name = match.group(1).strip()
            desc = match.group(2).strip()
            date_str = match.group(3)
            days_ago = None
            if date_str:
                try:
                    d = datetime.strptime(date_str, "%Y-%m-%d")
                    days_ago = (datetime.now() - d).days
                except ValueError:
                    pass
            weak_points.append({
                "topic": f.stem,
                "name": name,
                "description": desc,
                "first_marked": date_str,
                "days_ago": days_ago,
            })
    weak_points.sort(key=lambda w: w.get("days_ago") or 0, reverse=True)
    return weak_points


def get_stats(store_dir="knowledge_store"):
    """获取学习统计"""
    topics = list_topics(store_dir)
    weak_points = get_weak_points(store_dir)

    total_concepts = 0
    for t in topics:
        try:
            content = Path(t["file"]).read_text(encoding='utf-8')
            # 统计概念地图中的概念数
            concepts = len(re.findall(r'^\d+\.\s', content, re.MULTILINE))
            total_concepts += concepts
        except Exception:
            pass

    recent_7d = [w for w in weak_points if w.get("days_ago") is not None and w["days_ago"] <= 7]
    stale_14d = [w for w in weak_points if w.get("days_ago") is not None and w["days_ago"] > 14]

    return {
        "total_topics": len(topics),
        "total_concepts": total_concepts,
        "total_weak_points": len(weak_points),
        "reviewed_7d": len(recent_7d),
        "stale_14d": len(stale_14d),
        "review_rate": f"{len(recent_7d)}/{len(weak_points)}" if weak_points else "N/A",
        "topics": topics,
        "weak_points": weak_points,
    }


# CLI entry for Bash calls
def main():
    import sys
    if len(sys.argv) < 2:
        print("用法: python -m smart_learn.knowledge <command> [args]")
        print("  list     [--store-dir DIR]")
        print("  search   --query Q [--store-dir DIR]")
        print("  weak     [--store-dir DIR]")
        print("  stats    [--store-dir DIR]")
        sys.exit(1)

    cmd = sys.argv[1]
    args = _parse_args(sys.argv[2:])
    store = args.get("--store-dir", "knowledge_store")

    if cmd == "list":
        result = list_topics(store)
    elif cmd == "search":
        result = search(args.get("--query", ""), store)
    elif cmd == "weak":
        result = get_weak_points(store)
    elif cmd == "stats":
        result = get_stats(store)
    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


def _parse_args(argv):
    result = {}
    i = 0
    while i < len(argv):
        if argv[i].startswith("--"):
            key = argv[i]
            if i + 1 < len(argv) and not argv[i + 1].startswith("--"):
                result[key] = argv[i + 1]
                i += 2
            else:
                result[key] = ""
                i += 1
        else:
            i += 1
    return result


if __name__ == "__main__":
    main()
