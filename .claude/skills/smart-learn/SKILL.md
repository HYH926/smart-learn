---
name: smart-learn
description: 独立学习技能，基于费曼学习法的五步闭环。触发方式：输入 /smart-learn 主题，或说"教我XX"、"帮我系统学习XX"。每学完一步自动同步更新 Word 文档 + Mermaid 思维导图。
context: inline
---

# Smart Learn — 增量内联学习技能

基于费曼学习法五步闭环。纯 Markdown 零依赖可用；可选 `pip install python-docx` 获得 Word 文档功能。每一步学习成果同步更新到 **Word 文档** + **Mermaid 思维导图**，全程实时生长。

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
3. **自然对话** — 不用弹窗确认，用户用自然语言回应即可
4. **零外部依赖（核心）** — Markdown 学习 + 存储不依赖任何第三方包
5. **三格式持久化** — .md（知识库笔记，始终生成） + .docx（Word文档，可选） + Mermaid 思维导图（零依赖，始终生成）

---

## 初始化（Word 文档 + 思维导图）

学习开始前，同时初始化 Word 文档和 Mermaid 思维导图。Word 失败不影响核心流程；思维导图零依赖始终可用。

```bash
# 思维导图（零依赖，始终生成）
python .claude/skills/smart-learn/mindmap_utils.py init \
  --topic "主题名" \
  --output-dir "knowledge_store"

# Word 文档（可选，需 python-docx）
python .claude/skills/smart-learn/docx_utils.py init \
  --topic "主题名" \
  --output-dir "knowledge_store"
```

- 记录 `MINDMAP_FILE` 和 `MINDMAP_DATA` 路径，后续每步同步更新
- 如果 docx init 返回 `"status": "no_docx"` → 告知用户可 `pip install python-docx`，继续执行
- **学习中断恢复**：初始化时检查 `knowledge_store/{主题slug}_checkpoint.json` 是否存在：
  - 如果存在 → 告知用户"检测到上次未完成的学习（已完成步骤N）"，询问"继续上次 / 重新开始"
  - 如果选择继续 → 跳转到对应步骤继续执行，恢复已有状态
  - 每完成一步 → 更新 checkpoint（`{"topic":"...", "last_step": N, "mindmap_data":"...", "docx_path":"..."}`）

---

## 五步工作流

每一步的核心输出格式保持不变。Word 写入是每步末尾的附加操作。

---

### 步骤 1：概念地图

1. 调用 WebSearch 搜索该主题的最新资料（中文优先，确保准确性和及时性）
2. 读取 `templates/1-concept-map.md` 按模板执行
3. 将主题拆解为 5~8 个子概念，按学习依赖排序，标注难度

**固定输出格式**：
```
## 📊 概念地图：{主题}

1. {概念名}（{难度}）→ {一句话解决什么问题}
   ↓
2. {概念名}（{难度}）→ {一句话解决什么问题}
   ↓
...
```

输出后等待用户回应：
- "继续" / "OK" → 进入步骤2
- "调整XX" → 修改后重新确认

**→ 保存检查点**（中断恢复用）：
```bash
python -c "import json; json.dump({'topic':'{主题}','last_step':1}, open('knowledge_store/{主题slug}_checkpoint.json','w'))"
```

**→ 同步到思维导图**（始终执行）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 1 \
  --concepts '[{"name":"概念1","difficulty":"入门","purpose":"解决问题X"}, ...]'
```

**→ 写入 Word**（如果 DOCX_PATH 存在）：
```bash
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 1 --title "概念地图" \
  --content-file /tmp/smart-learn-step1.md
```

---

### 步骤 2：费曼解释

读取 `templates/2-feynman.md` 按模板执行。对步骤1中的每个概念，逐一用五维框架解释。

**每个概念的固定输出结构**：
```markdown
### {序号}. {概念名}

**为什么需要？** → {背景与动机，旧方案有什么问题}
**核心思想** → {一句话说清本质}
**类比理解** → {日常场景类比，完全非技术领域}
**示例** → {最小可运行的代码/真实场景}
**一句话** → {离开后能记住的那句}
```

每讲完一个概念，等待用户回应：
- "继续" / "下一个" → 讲下一个
- "换一个类比" / "没懂" → 用不同类比重讲（此时不写 Word，确认理解了再写）
- 任意提问 → 针对性解答

全部概念讲完后，用 3~5 句话串联串讲，然后进入步骤3。

**禁止**：
- 用未解释的术语解释另一个术语
- 从定义开始（必须从"为什么需要"开始）
- 类比用另一个技术概念

**→ 同步到思维导图**（每概念确认后更新核心思想 + 类比）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 2 \
  --concept "{概念名}" --core "{核心思想摘要}" --analogy "{类比关键词}"
```

**→ 写入 Word**（每个概念用户确认后立即写入）：
```bash
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 2 --title "{序号}. {概念名}" \
  --content-file /tmp/smart-learn-step2-concept.md
```

---

### 步骤 3：递进式自测

读取 `templates/3-self-test.md` 按模板执行。为每个概念出 1 道题，从三层中选最合适的一层：

| 层次 | 考察目标 | 适合什么概念 |
|------|---------|------------|
| 理解层 | 改变条件问变化 | 核心机制类（如缓存策略） |
| 应用层 | 新场景设计方案 | 工程实践类（如API设计） |
| 边界层 | 什么时候失效 | 理论约束类（如CAP定理） |

**逐个提问**，每次只出一道题。用户回答后给出：
- **点评**：具体评价哪里好、哪里不足
- **参考答案**：一个高质量的示范回答
- **掌握度**：✅ 已掌握 / ⚠️ 部分掌握 / ❌ 薄弱

全部完成后汇总薄弱点，询问用户：
- "继续" → 进入步骤4
- "回顾薄弱概念" → 对每个 ❌ 薄弱概念：
  1. 用不同的类比重新解释该概念（不重复步骤2的原版）
  2. 出一道新的同类层级的题目
  3. 用户回答后点评
  4. 直到掌握度变为 ✅/⚠️ 或用户说"先继续"
  5. 更新思维导图移除该概念的 ⚠️ 标记（如果已掌握）

**→ 同步到思维导图**（每题点评后，如果标记为 ❌ 薄弱则更新）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 3 \
  --concept "{概念名}" --weak "{薄弱原因摘要}"
```

**→ 写入 Word**（每题点评后立即写入，含题目+用户回答+点评+参考答案）：
```bash
python .claude/skills/smart-learn/docx_utils.py add-step \
  --file "{DOCX_PATH}" --step 3 --title "{概念名} — 自测" \
  --content-file /tmp/smart-learn-step3-q.md
```

---

### 步骤 4：关联内化

读取 `templates/4-association.md` 按模板执行。

1. 用 Glob 检查 `knowledge_store/` 下已有的学习笔记
2. 如果有相关主题，做四维对比：
   - 解决的是同一个问题吗？
   - 哪些经验可以直接迁移？
   - 新概念有什么独特性？
   - 知识地图中位置关系？
3. 如果没有，告知"这是该领域的第一个知识节点"
4. 输出文本版知识网络图

输出后等待用户回应：
- "继续" → 进入步骤5
- "补充关联" → 用户提出更多关联角度，追加分析

**→ 同步到思维导图**（每个关联主题添加一个连接）：
```bash
python .claude/skills/smart-learn/mindmap_utils.py update \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" --step 4 \
  --assoc-target "{关联主题名}" --assoc-relation "{一句话关系}"
```

**→ 写入 Word**（含对比表格和网络图）

---

### 步骤 5：巩固总结并保存

读取 `templates/5-summary.md` 按模板执行。

**输出精华笔记**（≤500 字）：
```markdown
## 🎯 核心公式
{一句"懂了就懂了80%"的话}

## 🔑 三个关键点
1. {洞察一}
2. {洞察二}
3. {洞察三}

## ⚠️ 薄弱点
- **{具体薄弱点}**：{为什么容易搞混} → {正确理解}

## 🏗️ 一句话类比
{日常场景一句话总结}

## 🏷️ 关键词
`{k1}` `{k2}` `{k3}` `{k4}` `{k5}`
```

输出精华笔记后等待用户回应：
- "保存" → 写入所有文件
- "修改XX" → 调整后重新确认

**持久化**（用户确认后执行）：
1. **必做**：将完整五步报告写入 `knowledge_store/{主题slug}.md`
2. **必做**：最终化思维导图：
```bash
python .claude/skills/smart-learn/mindmap_utils.py finalize \
  --file "{MINDMAP_FILE}" --data-file "{MINDMAP_DATA}" \
  --summary "{核心公式}" \
  --weak-points "{薄弱点1; 薄弱点2}" \
  --keywords "{k1, k2, k3, k4, k5}"
```
3. **可选**：最终化 Word 文档：
```bash
python .claude/skills/smart-learn/docx_utils.py finalize \
  --file "{DOCX_PATH}" \
  --summary "{核心公式}" \
  --weak-points "{薄弱点1; 薄弱点2}" \
  --keywords "{k1, k2, k3, k4, k5}"
```

最后告知用户：
- 📝 Markdown 笔记路径（始终生成）
- 🧠 思维导图路径（始终生成，Mermaid 格式）
- 📄 Word 文档路径（如有）
- ⚠️ 薄弱点列表（建议回顾）

**→ 清理临时文件和检查点**（学习完成）：
```bash
rm -f /tmp/smart-learn-step*.md /tmp/smart-learn-concept*.md
rm -f knowledge_store/{主题slug}_checkpoint.json
```

---

## 同步更新流程图

```
/smart-learn 主题
     │
     ├─ 初始化 ──→ 🧠 创建空白思维导图 + 📄 创建 Word（可选）
     │
     ├─ 步骤1 ──→ 🧠 写入概念节点 + 📄 写入概念地图
     │
     ├─ 步骤2 ──→ 🧠 每概念追加核心思想/类比 + 📄 写入解释
     │
     ├─ 步骤3 ──→ 🧠 标记薄弱点 ⚠️ + 📄 写入问答记录
     │
     ├─ 步骤4 ──→ 🧠 追加知识关联 🔗 + 📄 写入对比分析
     │
     └─ 步骤5 ──→ 🧠 最终化思维导图 + 📄 最终化 Word + 📝 Markdown
```

---

## 知识连续性

- 学习前检查 `knowledge_store/` 目录已有笔记
- 发现关键词匹配的旧笔记时，主动在步骤4做关联
- 所有笔记（.md + .docx + 思维导图.md）保存到同一目录，形成累积知识库

## 模板与工具

| 文件 | 用途 | 依赖 |
|------|------|------|
| `templates/1-concept-map.md` | 概念地图模板 | 无 |
| `templates/2-feynman.md` | 费曼解释模板 | 无 |
| `templates/3-self-test.md` | 递进式自测模板 | 无 |
| `templates/4-association.md` | 关联内化模板 | 无 |
| `templates/5-summary.md` | 巩固总结模板 | 无 |
| `mindmap_utils.py` | Mermaid 思维导图同步生成 | **零依赖** |
| `docx_utils.py` | Word 文档增量生成 | python-docx（可选） |
