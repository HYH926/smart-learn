---
name: smart-learn
description: 独立学习技能，基于费曼学习法的五步闭环。触发方式：输入 /smart-learn 主题，或说"教我XX"、"帮我系统学习XX"。每学完一步自动增量更新 Word 文档，所有步骤在主对话中内联透明执行。
context: inline
---

# Smart Learn — 增量内联学习技能

基于费曼学习法五步闭环。每学完一步，自动将内容**增量写入 Word 文档**。文档随学习进程实时生长，而非最后一次性生成。

## 触发

- `/smart-learn 主题名`
- "教我 Kubernetes 网络模型"
- "帮我系统学习 DDD"
- 任何表达出"想系统掌握一个复杂主题"的意图

### 不触发

- 简单定义（"X是什么"）
- 信息查询（"帮我查一下X"）
- 内容总结（"总结这篇文章"）

## 核心原则

1. **禁止使用 Agent 工具** — 所有步骤由主对话直接执行
2. **每步可见** — 输出实时展示，用户确认后进入下一步
3. **增量 Word 文档** — 每步确认后立即写入同一个 .docx 文件
4. **自然对话** — 不用弹窗确认，用户用自然语言回应即可
5. **双格式持久化** — .docx（Word文档） + .md（知识库笔记）

---

## 准备阶段：初始化 Word 文档

确认学习主题后，第一步是创建 Word 文档：

```bash
python .claude/skills/smart-learn/docx_utils.py init \
  --topic "主题名" \
  --output-dir "d:/future/knowledge_store"
```

如果输出 `"status": "no_docx"`，告知用户需要：
```
pip install python-docx
```
然后继续执行后续步骤（Word 功能静默跳过，Markdown 存储仍正常进行）。

如果初始化成功，告知用户文档路径。记录 `DOCX_PATH` 用于后续增量写入。

---

## 五步工作流

每一步完成后，调用 docx_utils.py 增量写入同一个 Word 文档。

---

### 步骤 1：概念地图

读取 `templates/1-concept-map.md`，搜索 + 拆解为 5~8 个子概念。

**输出后等待用户确认**：
- "继续" → 写入 Word → 进入步骤2
- "调整XX" → 修改后重新确认

**写入 Word**：
```bash
# 先将概念地图内容写入临时文件
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" \
  --step 1 \
  --title "概念地图" \
  --content-file /tmp/smart-learn-step1.md
```

---

### 步骤 2：费曼解释

读取 `templates/2-feynman.md`。**每讲完一个概念**，等用户回应后：
1. 把该概念的讲解内容追加入临时累积文件
2. 用户全部确认后，一次性写入 Word

或者更好的做法：每讲完一个概念就写入 Word，实现真正的"实时生长"。

**每个概念写入 Word**：
```bash
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" \
  --step 2 \
  --title "{序号}. {概念名}" \
  --content-file /tmp/smart-learn-step2-concept.md
```

**每个概念讲完后等待用户**：
- "继续/下一个" → 写 Word → 讲下一个
- "换类比/没懂" → 重讲（不写 Word，讲对了再写）
- 任意提问 → 解答

全部讲完后做 3~5 句串联串讲，写入 Word，进入步骤3。

**禁止**：用未解释的术语解释术语、从定义开始、类比用技术概念。

---

### 步骤 3：递进式自测

读取 `templates/3-self-test.md`。每个概念 1 道题，从三层中选最合适层。

**逐个提问**，用户回答后：
- 给出点评 + 参考答案 + 掌握度标记
- **立即写入 Word**（含题目、用户回答、点评、参考答案）

```bash
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" \
  --step 3 \
  --title "{概念名} — 自测" \
  --content-file /tmp/smart-learn-step3-q.md
```

全部完成后汇总薄弱点，询问：继续→步骤4 / 回顾薄弱概念→重讲。

---

### 步骤 4：关联内化

读取 `templates/4-association.md`。

1. Glob 检查 `d:\future\knowledge_store\` 下已有笔记
2. 有相关主题 → 四维对比（问题域/可迁移/差异点/位置关系）
3. 无关联 → 告知"第一个知识节点"
4. 输出知识网络图

**写入 Word**（含对比表格和网络图）。

---

### 步骤 5：巩固总结

读取 `templates/5-summary.md`。

输出精华笔记（≤500字）：核心公式 + 3 关键点 + 薄弱点 + 类比 + 关键词。

**持久化**：
1. 写入完整五步报告到 `d:\future\knowledge_store\{主题slug}.md`
2. **最终化 Word 文档**：
```bash
python .claude/skills/smart-learn/docx_utils.py finalize \
  --file "{DOCX_PATH}" \
  --summary "{核心公式}" \
  --weak-points "{薄弱点1; 薄弱点2}" \
  --keywords "{k1, k2, k3, k4, k5}"
```

告知用户：
- Word 文档路径 📄
- Markdown 笔记路径 📝
- 薄弱点列表 ⚠️

---

## 增量 Word 文档流程图

```
/smart-learn 主题
     │
     ├─ 准备 ──→ 📄 创建空白 Word
     │
     ├─ 步骤1 ──→ 📄 写入「概念地图」
     │
     ├─ 步骤2 ──→ 📄 写入「概念A解释」
     │         ──→ 📄 写入「概念B解释」
     │         ──→ ...（每概念实时写入）
     │
     ├─ 步骤3 ──→ 📄 写入「问题1+回答+点评」
     │         ──→ 📄 写入「问题2+回答+点评」
     │         ──→ ...（每题实时写入）
     │
     ├─ 步骤4 ──→ 📄 写入「关联分析」
     │
     └─ 步骤5 ──→ 📄 写入「总结+薄弱点+关键词」
                  📝 写入 Markdown 笔记
```

**核心理念**：Word 文档不是"结课证书"，而是你从步骤1到步骤5的**全程学习日志**。

---

## 知识连续性

- 学习前检查 `d:\future\knowledge_store/` 目录已有笔记
- 发现关键词匹配的旧笔记时，主动在步骤4做关联
- 所有笔记（.md + .docx）保存到同一目录，形成累积知识库

## 模板与工具

| 文件 | 用途 |
|------|------|
| `templates/1-concept-map.md` | 概念地图模板 |
| `templates/2-feynman.md` | 费曼解释模板 |
| `templates/3-self-test.md` | 递进式自测模板 |
| `templates/4-association.md` | 关联内化模板 |
| `templates/5-summary.md` | 巩固总结模板 |
| `docx_utils.py` | Word 文档增量生成工具 |
