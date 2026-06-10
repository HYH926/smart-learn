---
description: 跨主题知识搜索。在所有学习笔记中搜索关键词，返回匹配结果及来源。用法：/smart-search 关键词
allowed-tools: Read, Glob, Grep
---

搜索你的个人知识库。

用户搜索的关键词是：$ARGUMENTS

## 搜索流程

### 1. 全量检索
用 Grep 在 `knowledge_store/` 下所有 `.md` 文件中搜索关键词（忽略思维导图和 checkpoint 文件）：

```bash
# 排除思维导图和状态文件，只搜学习笔记
grep -rli "$ARGUMENTS" knowledge_store/*.md --ignore-case 2>/dev/null | grep -v "思维导图" | grep -v "checkpoint" | grep -v "mindmap_state"
```

### 2. 展示结果
对每个匹配文件，提取包含关键词的上下文段落（前后各 1 行），按主题分组：

```
🔍 搜索「{关键词}」 — 找到 N 处匹配

📁 {主题A} → knowledge_store/{文件A}.md
   ┌ 上下文...
   │ ...{关键词}...
   └ ...

📁 {主题B} → knowledge_store/{文件B}.md
   ┌ 上下文...
   │ ...{关键词}...
   └ ...

🧠 思维导图中也找到匹配：
   - knowledge_store/{主题A}_思维导图.md
```

### 3. 附加操作
搜索完成后询问：
- "要打开某篇完整笔记复习吗？" → 用户选主题 → 切换到 `/smart-review 主题名` 流程
- 如果无结果 → "知识库中未找到「{关键词}」。用 /smart-learn 学习这个主题？"

### 约束
- 纯只读，不写任何文件
- 如果 knowledge_store 为空 → "知识库为空，用 /smart-learn 开始学习吧"
- 搜索范围：仅 `knowledge_store/` 目录下的 `.md` 文件
