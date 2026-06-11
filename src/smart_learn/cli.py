"""Unified CLI entry point for smart-learn."""

import sys
import json
import os


def main():
    if len(sys.argv) < 2:
        print("Smart Learn v2.0 — AI-powered interactive learning")
        print("")
        print("Commands:")
        print("  smart-learn init <topic> [--dir DIR]")
        print("  smart-learn mindmap init|update|finalize ...")
        print("  smart-learn docx init|add-step|finalize ...")
        print("  smart-learn knowledge list|search|weak|stats")
        print("")
        print("Quick start:")
        print("  pip install .")
        print("  # Copy prompts/universal-learn.md into any AI chat")
        print("  # Works with: Claude, GPT, Gemini, DeepSeek, Qwen...")
        sys.exit(0)

    cmd = sys.argv[1]

    # Parse --dir from remaining args
    def get_dir(default="knowledge_store"):
        for i, a in enumerate(sys.argv):
            if a == "--dir" and i + 1 < len(sys.argv):
                return sys.argv[i + 1]
        return default

    if cmd == "init":
        topic = sys.argv[2] if len(sys.argv) > 2 else "未命名"
        output_dir = get_dir()

        # Mindmap (always works, zero dependency)
        from .mindmap import init_mindmap
        mm = init_mindmap(topic, output_dir)
        print(json.dumps(mm, ensure_ascii=False))

        # Word doc (optional, needs python-docx)
        from .docx_gen import init_doc
        dw = init_doc(topic, output_dir)
        if dw:
            print(json.dumps(dw, ensure_ascii=False))

    elif cmd == "mindmap":
        from .mindmap import main as sub_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        sub_main()

    elif cmd == "docx":
        from .docx_gen import main as sub_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        sub_main()

    elif cmd == "knowledge":
        from .knowledge import main as sub_main
        sys.argv = [sys.argv[0]] + sys.argv[2:]
        sub_main()

    else:
        print(f"Unknown command: {cmd}")
        print("Run 'smart-learn' without arguments for help.")
        sys.exit(1)
