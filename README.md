# Smart Learn — AI 交互式学习插件

> 基于费曼学习法五步闭环：概念地图 → 费曼解释 → 自测检验 → 关联内化 → 巩固总结。
> **支持所有主流大模型。零核心依赖。**

## 支持的大模型

| AI | 使用方式 |
|----|---------|
| **Claude Code** | 安装为 Skill，`/smart-learn 主题` |
| **ChatGPT / GPT-4** | `pip install .` + 复制 Prompt 模板 |
| **Gemini / DeepSeek** | 同上 |
| **通义千问 / 文心一言 / Kimi** | 同上 |
| **任意支持 Bash 的 AI** | pip install + 复制 Prompt |

## 快速开始

### Claude Code 用户

```bash
git clone https://github.com/HYH926/smart-learn.git
cp -r smart-learn/.claude/* 你的项目路径/.claude/
# 完成。无需 pip install。
```

输入 `/smart-learn Kubernetes 网络模型` 即可。

### 其他 AI 用户（GPT、Gemini、DeepSeek、通义千问等）

```bash
git clone https://github.com/HYH926/smart-learn.git
cd smart-learn
pip install .            # 安装 CLI 工具（零核心依赖）
pip install .[all]       # 或含 Word 文档支持

# 复制 prompts/universal-learn.md 内容，粘贴到任意 AI 聊天
# 告诉 AI：「使用 Smart Learn 学习 {你要学的主题}」
```

## 仓库结构（双版本合一）

```
smart-learn/
│
├── .claude/                       ← Claude Code Skill 版
│   ├── commands/                  # /smart-learn /smart-review /smart-search /smart-stats
│   └── skills/smart-learn/        # SKILL.md + 5 个模板
│
├── src/smart_learn/               ← Python 插件版（任意 AI 可用）
│   ├── mindmap.py                 # Mermaid 思维导图生成（零依赖）
│   ├── docx_gen.py                # Word 文档生成（可选 python-docx）
│   ├── knowledge.py               # 知识库搜索 + 统计 + 间隔复习
│   └── cli.py                     # 统一 CLI 入口
│
├── prompts/                       ← 通用 Prompt 模板（复制到任意 AI）
│   ├── universal-learn.md         # 五步学习 Prompt
│   ├── universal-review.md        # 快速复习 Prompt
│   └── universal-stats.md         # 学习统计 Prompt
│
├── pyproject.toml                 # pip install smart-learn
└── README.md
```

## 功能

| 功能 | Claude Code | 其他 AI |
|------|:---:|:---:|
| 五步学习 | `/smart-learn` | 复制 Prompt + CLI |
| 快速复习 | `/smart-review` | 复制 Prompt + CLI |
| 全知识库搜索 | `/smart-search` | `smart-learn knowledge search` |
| 学习统计 | `/smart-stats` | `smart-learn knowledge stats` |
| 间隔复习提醒 | 自动 | CLI 输出 |
| 前置评估 | 自然语言触发 | Prompt 内支持 |
| 思维导图 | Mermaid .md | Mermaid .md |
| Word 文档 | 可选 | 可选 |

## License

MIT
