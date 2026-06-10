"""
Smart Learn 思维导图生成工具
=============================
零依赖，纯文本 Mermaid mindmap 格式。
每次步骤完成后重新生成完整导图，实现"同步更新"效果。
GitHub / VSCode / Notion / Obsidian 原生渲染。

用法:
  python mindmap_utils.py init     --topic X --output-dir Y
  python mindmap_utils.py update   --file X --step N --data-file Y
  python mindmap_utils.py finalize --file X --summary Y --weak-points Z --keywords W
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime


def _indent(text, level):
    return "  " * level + text


def _safe_id(text):
    """Mermaid 节点 ID 不能有特殊字符。加 hash 后缀防止重名冲突"""
    import hashlib
    base = text.replace(" ", "_").replace("(", "").replace(")", "").replace("：", "").replace(":", "").replace("-", "_")
    # 短 hash 防止 "API设计" 和 "API-设计" 碰撞
    suffix = hashlib.md5(text.encode()).hexdigest()[:4]
    return f"{base}_{suffix}"


def _short(text, max_len=20):
    """截断过长文本"""
    return text if len(text) <= max_len else text[:max_len-1] + "…"


def generate_mindmap(state):
    """
    根据 state 字典生成完整 Mermaid mindmap 文本。
    state 结构:
    {
      "topic": str,
      "concepts": [
        {
          "name": str, "difficulty": str, "purpose": str,
          "core": "", "analogy": "", "weak": false, "weak_reason": ""
        }
      ],
      "associations": [{"target": str, "relation": str}],
      "summary": "",
      "keywords": []
    }
    """
    lines = ["```mermaid", "mindmap"]
    topic = state.get("topic", "未命名")
    lines.append(f'  root(({topic}))')

    concepts = state.get("concepts", [])
    for c in concepts:
        label = f'{c["name"]}'
        if c.get("difficulty"):
            diff_map = {"入门": "🟢", "中等": "🟡", "进阶": "🔴"}
            label = f'{diff_map.get(c["difficulty"], "")} {c["name"]}'
        if c.get("weak"):
            label = f'{label} ⚠️'

        lines.append(_indent(f'{_safe_id(c["name"])}[{label}]', 1))

        if c.get("purpose"):
            lines.append(_indent(f'{_safe_id(c["name"])}_purpose[{_short(c["purpose"], 25)}]', 2))
        if c.get("core"):
            lines.append(_indent(f'{_safe_id(c["name"])}_core[💡{_short(c["core"], 25)}]', 2))
        if c.get("analogy"):
            lines.append(_indent(f'{_safe_id(c["name"])}_analogy[🏠{_short(c["analogy"], 25)}]', 2))
        if c.get("weak") and c.get("weak_reason"):
            lines.append(_indent(f'{_safe_id(c["name"])}_weak[⚠️{_short(c["weak_reason"], 25)}]', 2))

    # 关联
    associations = state.get("associations", [])
    if associations:
        lines.append(_indent("assoc[🔗 知识关联]", 1))
        for a in associations:
            rel = _short(a.get("relation", ""), 20)
            lines.append(_indent(f'assoc_{_safe_id(a["target"])}[→ {a["target"]}: {rel}]', 2))

    # 总结
    summary = state.get("summary", "")
    if summary:
        lines.append(_indent(f'summary[🎯 {_short(summary, 30)}]', 1))

    keywords = state.get("keywords", [])
    if keywords:
        kw_str = " ".join(f"#{k}" for k in keywords[:5])
        lines.append(_indent(f'keywords[{_short(kw_str, 35)}]', 1))

    lines.append("```")
    return "\n".join(lines)


def load_state(data_file):
    if os.path.exists(data_file):
        try:
            return json.loads(Path(data_file).read_text(encoding='utf-8'))
        except json.JSONDecodeError as e:
            backup = data_file + ".corrupted"
            try:
                os.rename(data_file, backup)
            except OSError:
                pass
            print(json.dumps({
                "status": "warn", "msg": f"状态文件损坏({e.msg})，已备份为 {backup}，使用空白状态重建"
            }, ensure_ascii=False))
    return {"topic": "", "concepts": [], "associations": [], "summary": "", "keywords": []}


def save_state(data_file, state):
    Path(data_file).parent.mkdir(parents=True, exist_ok=True)
    Path(data_file).write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')


def write_mindmap(filepath, mermaid_text):
    """将 Mermaid mindmap 写入 .md 文件（含渲染提示）"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    content = f"""# {Path(filepath).stem} — 思维导图

> 同步更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M')}
> 格式：Mermaid mindmap（GitHub / VSCode / Notion / Obsidian 原生渲染）

{mermaid_text}

---
*此思维导图随学习进程同步更新*
"""
    Path(filepath).write_text(content, encoding='utf-8')


# ═══════════════════════════════════════
#  CLI 入口
# ═══════════════════════════════════════

def main():
    if len(sys.argv) < 2:
        print("用法: mindmap_utils.py <command> [options]")
        print("  init      --topic X --output-dir Y")
        print("  update    --file X --step N --data-file Y [--concept Z] [--core C] [--analogy A] [--weak W] [--assoc-target T]")
        print("  finalize  --file X --data-file Y --summary S --weak-points W --keywords K")
        sys.exit(1)

    cmd = sys.argv[1]
    args = _parse_args(sys.argv[2:])

    if cmd == "init":
        topic = args.get("--topic", "未命名")
        output_dir = args.get("--output-dir", ".")
        os.makedirs(output_dir, exist_ok=True)

        data_file = os.path.join(output_dir, f"{topic}_mindmap_state.json")
        state = {"topic": topic, "concepts": [], "associations": [], "summary": "", "keywords": []}
        save_state(data_file, state)

        mermaid = generate_mindmap(state)
        mindmap_file = os.path.join(output_dir, f"{topic}_思维导图.md")
        write_mindmap(mindmap_file, mermaid)

        print(json.dumps({
            "status": "ok", "action": "init",
            "mindmap_file": mindmap_file,
            "data_file": data_file
        }, ensure_ascii=False))

    elif cmd == "update":
        data_file = args["--data-file"]
        step = int(args.get("--step", 1))
        state = load_state(data_file)

        if step == 1:
            # 添加所有概念节点
            concepts_json = args.get("--concepts", "[]")
            concepts = json.loads(concepts_json)
            state["concepts"] = []
            for c in concepts:
                state["concepts"].append({
                    "name": c.get("name", ""),
                    "difficulty": c.get("difficulty", ""),
                    "purpose": c.get("purpose", ""),
                    "core": "",
                    "analogy": "",
                    "weak": False,
                    "weak_reason": ""
                })

        elif step == 2:
            # 更新单个概念的核心思想和类比
            concept_name = args.get("--concept", "")
            found = False
            for c in state["concepts"]:
                if c["name"] == concept_name:
                    if args.get("--core"):
                        c["core"] = args["--core"]
                    if args.get("--analogy"):
                        c["analogy"] = args["--analogy"]
                    found = True
                    break
            if not found and concept_name:
                concept_names = [c["name"] for c in state["concepts"]]
                print(json.dumps({
                    "status": "warn", "action": "update", "step": step,
                    "msg": f"概念「{concept_name}」未在步骤1注册。已注册：{concept_names}"
                }, ensure_ascii=False))
                return

        elif step == 3:
            # 标记薄弱点
            concept_name = args.get("--concept", "")
            weak_reason = args.get("--weak", "")
            found = False
            for c in state["concepts"]:
                if c["name"] == concept_name:
                    c["weak"] = True
                    c["weak_reason"] = weak_reason
                    found = True
                    break
            if not found and concept_name:
                concept_names = [c["name"] for c in state["concepts"]]
                print(json.dumps({
                    "status": "warn", "action": "update", "step": step,
                    "msg": f"概念「{concept_name}」未在步骤1注册。已注册：{concept_names}"
                }, ensure_ascii=False))
                return

        elif step == 4:
            # 添加关联（自动去重）
            target = args.get("--assoc-target", "")
            relation = args.get("--assoc-relation", "")
            if target:
                existing = [a for a in state["associations"] if a["target"] == target]
                if existing:
                    existing[0]["relation"] = relation  # 更新已有
                else:
                    state["associations"].append({"target": target, "relation": relation})

        save_state(data_file, state)
        mermaid = generate_mindmap(state)
        mindmap_file = args["--file"]
        write_mindmap(mindmap_file, mermaid)

        print(json.dumps({"status": "ok", "action": "update", "step": step, "file": mindmap_file}, ensure_ascii=False))

    elif cmd == "finalize":
        data_file = args["--data-file"]
        state = load_state(data_file)
        state["summary"] = args.get("--summary", "")
        state["weak_points"] = args.get("--weak-points", "")
        state["keywords"] = [k.strip() for k in args.get("--keywords", "").split(",") if k.strip()]

        save_state(data_file, state)
        mermaid = generate_mindmap(state)
        mindmap_file = args["--file"]
        write_mindmap(mindmap_file, mermaid)

        print(json.dumps({"status": "ok", "action": "finalize", "file": mindmap_file}, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


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
