# Smart Learn — 通用复习 Prompt

快速复习已学主题，不重走五步。

工具：
```bash
python -m smart_learn.knowledge list     # 列出所有主题
python -m smart_learn.knowledge search --query "关键词"  # 搜索
python -m smart_learn.knowledge weak     # 获取薄弱点（按最久未复习排序）
python -m smart_learn.knowledge stats    # 统计面板
```

流程：
1. 读笔记 → 生成复习卡片（核心公式 + 3 关键点 + 类比 + 关键词）
2. 薄弱点回顾（按距今天数排序，最久未复习优先）
3. 可选自测
