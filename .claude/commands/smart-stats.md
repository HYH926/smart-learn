---
description: 查看学习统计：已学主题数、学习时长、薄弱点分布、知识图谱总览。用法：/smart-stats
allowed-tools: Read, Bash, Glob, Grep
---

显示 Smart Learn 学习统计数据。

## 统计维度

### 1. 学习概览
用 Glob 扫描 `knowledge_store/` 目录：

```bash
# 统计 .md 笔记数量（排除思维导图和checkpoint）
ls knowledge_store/*.md 2>/dev/null | grep -v "思维导图" | grep -v "checkpoint" | wc -l
```

输出：
- 📚 总学习主题数
- 🧠 总概念数（从各笔记的概念地图中提取）
- ⚠️ 总薄弱点数（从各笔记中提取 ⚠️ 标记）

### 2. 主题列表
列出每个已学主题的关键信息：

| 主题 | 学习日期 | 概念数 | 薄弱点 | 关键词 |
|------|---------|--------|--------|--------|
| {主题1} | {日期} | {N} | {N} | {kw} |
| ... | ... | ... | ... | ... |

### 3. 薄弱点总览
聚合所有主题的薄弱点：
```
⚠️ 薄弱点分布
├── {主题A}
│   ├── {薄弱点1}
│   └── {薄弱点2}
├── {主题B}
│   └── {薄弱点3}
└── ...
```
提示："建议用 /smart-review {主题名} 针对性复习薄弱点"

### 4. 知识地图总览
如果存在多个主题，输出跨主题关联：
```
🗺️ 知识网络
{主题A} ──关联── {主题B}
{主题A} ──关联── {主题C}
...
```

### 5. 知识库路径
- 📝 Markdown 笔记：`knowledge_store/`
- 🧠 思维导图：`knowledge_store/*_思维导图.md`
- 📄 Word 文档：`knowledge_store/*_学习笔记.docx`（如有）

## 约束
- 纯只读，不写任何文件
- 如果 knowledge_store 为空，告知"还没有学习记录，用 /smart-learn 开始学习吧"
- 所有数据从已有 Markdown 笔记和 checkpoint 文件中提取
