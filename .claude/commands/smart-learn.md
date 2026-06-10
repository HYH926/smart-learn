---
description: 独立学习技能。基于费曼学习法五步闭环，所有步骤在主对话中内联透明执行。用法：/smart-learn 你想学的主题
allowed-tools: Read, Write, Bash, WebSearch, Glob, Grep, AskUserQuestion
---

启动 Smart Learn 学习技能。

用户想学的主题是：$ARGUMENTS

如果用户没有提供主题，友好地询问用户想学什么。
如果提供了主题，按 SKILL.md 中定义的五步工作流内联执行：

步骤1 → 概念地图（搜索 + 拆解 + 用户确认）
步骤2 → 费曼解释（逐一讲解 + 逐概念确认）
步骤3 → 递进式自测（逐题提问 + 点评 + 薄弱点标注）
步骤4 → 关联内化（检索知识库 + 四维对比）
步骤5 → 巩固总结（精华笔记 + 保存到 knowledge_store/）

记住：不要使用 Agent 工具。所有步骤在主对话中直接执行，输出实时可见。
