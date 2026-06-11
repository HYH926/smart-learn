"""Unified CLI entry point for smart-learn."""

import sys
import json


def main():
    if len(sys.argv) < 2:
        print("Smart Learn v2.0 — AI-powered interactive learning")
        print("")
        print("Commands:")
        print("  smart-learn init <topic> [--dir knowledge_store]")
        print("  smart-learn mindmap init|update|finalize ...")
        print("  smart-learn docx init|add|finalize ...")
        print("  smart-learn knowledge list|search|weak|stats")
        print("")
        print("Usage with AI:")
        print("  Copy a prompt from https://github.com/HYH926/smart-learn-plugin/prompts/")
        print("  Paste into any AI chat (Claude, GPT, Gemini, DeepSeek, Qwen...)")
        print("  The AI will call these CLI tools through the learning workflow.")
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "init":
        topic = sys.argv[2] if len(sys.argv) > 2 else "未命名"
        # Parse --dir
        args = {}
        for i, a in enumerate(sys.argv):
            if a == "--dir" and i + 1 < len(sys.argv):
                args["--output-dir"] = sys.argv[i + 1]
        from .mindmap import init_mindmap
        from .docx_gen import init_doc

        mm = init_mindmap(topic, args.get("--output-dir", "knowledge_store"))
        print(json.dumps(mm, ensure_ascii=False))
        # Try docx (optional)
        dw = init_doc(topic, args.get("--output-dir", "knowledge_store"))
        if dw:
            print(json.dumps(dw, ensure_ascii=False))

    elif cmd == "mindmap":
        from .mindmap import main as mm_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        mm_main()

    elif cmd == "docx":
        from .docx_gen import main as dx_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        dx_main()

    elif cmd == "knowledge":
        from .knowledge import main as kn_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        kn_main()

    else:
        print(f"未知命令: {cmd}")
        print("使用 'smart-learn' 查看帮助")
        sys.exit(1)
