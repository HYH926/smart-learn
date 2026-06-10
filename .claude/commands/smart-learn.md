---
description: 独立学习技能。基于费曼学习法五步闭环，所有步骤在主对话中内联透明执行。每学完一步同步更新 Mermaid 思维导图 + Word 文档（可选）。用法：/smart-learn 你想学的主题
allowed-tools: Read, Write, Bash, WebSearch, Glob, Grep, AskUserQuestion
---

启动 Smart Learn 学习技能。

用户想学的主题是：$ARGUMENTS

如果用户没有提供主题，友好地询问用户想学什么。
如果提供了主题，按 SKILL.md 中定义的五步工作流内联执行：

1. 初始化：创建 Mermaid 思维导图（零依赖） + Word 文档（可选，需 python-docx）
2. 步骤1 → 概念地图（搜索 + 拆解 + 用户确认 + 同步导图 + 写入 Word）
3. 步骤2 → 费曼解释（逐一讲解 + 逐概念确认 + 同步导图 + 写入 Word）
4. 步骤3 → 递进式自测（逐题提问 + 点评 + 薄弱点标注 + 同步导图 + 写入 Word）
5. 步骤4 → 关联内化（检索知识库 + 四维对比 + 同步导图 + 写入 Word）
6. 步骤5 → 巩固总结（精华笔记 + 保存 .md + 最终化导图 + 最终化 .docx）

记住：
- 不要使用 Agent 工具，所有步骤在主对话中直接执行
- 思维导图（Mermaid 格式）零依赖始终生成，GitHub/VSCode/Notion 原生渲染
- Word 文档可选，python-docx 未安装时静默跳过
- Markdown 笔记始终生成
- 所有路径使用相对路径（knowledge_store/），不硬编码绝对路径
