# Smart Learn — AI 交互式学习插件

> 基于费曼学习法五步闭环：概念地图 → 费曼解释 → 自测检验 → 关联内化 → 巩固总结。
> **支持所有主流大模型。核心学习流程零第三方依赖；本地持久化和导图同步需要 Python 3.9+，Word 导出需要可选的 python-docx。**

## 在线体验

无需克隆即可体验五步流程的第三方演示：

https://socialistic.ai/en/skill/smart-learn-80f5d1?utm_source=github&utm_medium=issue&utm_campaign=20260612-summer-vibe-coding-learners&utm_content=badge

> 该演示由第三方提供，不在本仓库控制范围内。不要输入敏感或私人学习内容；如果链接不可用，使用下方本地安装方式或复制 prompts/universal-learn.md。

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

## 运行前提与降级策略

- 核心五步流程不依赖第三方包；本地导图和 checkpoint 需要 Python 3.9+。
- 没有 Bash、Python 或写权限时：继续在对话中输出 Markdown 和 Mermaid 源码，但明确说明“未写入文件”，不要声称已同步。
- 没有 python-docx 时：跳过 Word，不影响五步学习。
- 主题名会转换为安全 slug 后再用作文件名；不要把学习笔记提交到公开仓库。
- 知识库或 checkpoint 损坏时：保留备份并提示恢复/重开，不静默覆盖。
- 第三方在线演示不可用时：使用本地安装或通用 Prompt。

## License

MIT
