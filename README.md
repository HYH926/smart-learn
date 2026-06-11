# Smart Learn — Claude Code 内联学习技能

> 输入一个主题，AI 在主对话中一步步引导你真正掌握它。**所有步骤透明可见，问一部分就更新一部分 Word 文档。**

基于费曼学习法五步闭环：概念地图 → 费曼解释 → 自测检验 → 关联内化 → 巩固总结。

## 为什么选择 Smart Learn？

| | Smart Learn (内联模式) |
|---|---|---|
| 执行方式 || **主对话透明执行** |
| 你能看到讲解过程吗 || ✅ 每一步实时可见 |
| 交互方式 || **自然语言对话** |
| 外部依赖 || Markdown: 零 / Word: python-docx（可选） |
| 知识存储 || **增量 Word 文档 + Markdown** |
| 增量更新 || ✅ 每步实时写入同一 Word |
| 文件数 || 8 个文件 |

## 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/HYH926/smart-learn.git

# 2. 复制到你的 Claude Code 项目
cp -r smart-learn/.claude/*  你的项目路径/.claude/
```

完成。不需要 `pip install` 任何东西。

> **可选**：如需 Word 文档存储，安装 `pip install python-docx`。不安装则仅用 Markdown，不影响任何功能。

### 使用

在 Claude Code 中输入：

```
/smart-learn Kubernetes 网络模型
```

或自然语言：

```
教我 Rust 所有权机制
帮我系统学习 CAP 定理
```

AI 会一步步引导你，**并且每步实时写入 Word 文档**：

```
/smart-learn 主题
     │
     ├─ 准备 ──→ 📄 创建空白 Word 文档
     │
     ├─ 步骤1 ──→ 📄 写入「概念地图」
     │
     ├─ 步骤2 ──→ 📄 写入「概念A解释」
     │         ──→ 📄 写入「概念B解释」  （每概念实时写）
     │
     ├─ 步骤3 ──→ 📄 写入「问题+你的回答+点评」
     │         ──→ 📄 写入...            （每题实时写）
     │
     ├─ 步骤4 ──→ 📄 写入「关联分析」
     │
     └─ 步骤5 ──→ 📄 写入「总结+薄弱点」
                  📝 同时生成 Markdown 笔记
```

**Word 文档不是"结课证书"，而是你的全程学习日志。**

## 项目结构

```
├── README.md
├── LICENSE
├── plugin.json
├── marketplace.json
├── .gitignore
└── .claude/
    ├── commands/
    │   └── smart-learn.md              # /smart-learn 命令入口
    └── skills/
        └── smart-learn/
            ├── SKILL.md                # 核心技能定义 + 五步工作流
            ├── docx_utils.py           # Word 文档增量生成工具
            └── templates/
                ├── 1-concept-map.md    # 概念地图模板
                ├── 2-feynman.md        # 费曼解释模板
                ├── 3-self-test.md      # 递进式自测模板
                ├── 4-association.md    # 关联内化模板
                └── 5-summary.md        # 巩固总结模板
```

## 学习成果

| 格式 | 路径 | 特点 |
|------|------|------|
| 📄 Word (.docx) | `knowledge_store/主题名_学习笔记.docx` | **增量实时更新**，格式化排版 |
| 📝 Markdown (.md) | `knowledge_store/主题名.md` | 完整五步报告，便于检索 |

下次学相关主题时自动检索已有笔记并建立关联。

## 与其他方案的区别

| 方案 | 适用场景 |
|------|---------|
| 直接问 Claude "解释一下 XX" | 快速了解，不要求深度 |
| Smart Learn `/smart-learn` | **系统掌握**，检验真实理解 |
| ai-learn 插件 | 同上，但需要 Python 环境且交互不透明 |

## License

MIT
