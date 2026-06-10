# Smart Learn — Claude Code 内联学习技能

> 输入一个主题，AI 在主对话中一步步引导你真正掌握它。**所有步骤透明可见，不再黑盒。**

基于费曼学习法五步闭环：概念地图 → 费曼解释 → 自测检验 → 关联内化 → 巩固总结。

## 为什么选择 Smart Learn？

| | ai-learn 插件 (Agent 模式) | Smart Learn (内联模式) |
|---|---|---|
| 执行方式 | 子 Agent 黑盒执行 | **主对话透明执行** |
| 你能看到讲解过程吗 | ❌ 只有弹窗确认 | ✅ 每一步实时可见 |
| 交互方式 | 三按钮盲选 | **自然语言对话** |
| 外部依赖 | chromadb + sqlite3 + Python | **零依赖** |
| 知识存储 | SQLite + Chroma | Markdown 文件 |
| 文件数 | 11 个 + Python | **7 个纯 Markdown** |

## 快速开始

### 安装

```bash
# 1. 克隆仓库
git clone https://github.com/HYH926/smart-learn.git

# 2. 复制到你的 Claude Code 项目
cp -r smart-learn/.claude/*  你的项目路径/.claude/
```

完成。不需要 `pip install` 任何东西。

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

AI 会一步步引导你：

```
步骤1  概念地图 —— 搜索 + 拆解为 5~8 个子概念
        ↓   [你确认：合理继续 / 调整修改]
步骤2  费曼解释 —— 每个概念从 WHY 开始，用日常类比讲透
        ↓   [每讲完一个你都可以：继续 / 换个类比 / 追问]
步骤3  递进式自测 —— 逐题提问，点评 + 参考答案 + 薄弱点标注
        ↓   [薄弱点可选回步骤2重讲]
步骤4  关联内化 —— 检索你学过的旧知识，建立关联网络
        ↓
步骤5  巩固总结 —— 精华笔记保存到 knowledge_store/
```

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
            └── templates/
                ├── 1-concept-map.md    # 概念地图模板
                ├── 2-feynman.md        # 费曼解释模板
                ├── 3-self-test.md      # 递进式自测模板
                ├── 4-association.md    # 关联内化模板
                └── 5-summary.md        # 巩固总结模板
```

## 学习成果

所有学习笔记自动保存到 `项目/knowledge_store/` 目录。下次学相关主题时自动检索关联。

## 与其他方案的区别

| 方案 | 适用场景 |
|------|---------|
| 直接问 Claude "解释一下 XX" | 快速了解，不要求深度 |
| Smart Learn `/smart-learn` | **系统掌握**，检验真实理解 |
| ai-learn 插件 | 同上，但需要 Python 环境且交互不透明 |

## License

MIT
