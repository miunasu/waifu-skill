---
name: waifu-skill
description: "将ACG角色蒸馏/提取成AI Skill。双轨提取Lore+Persona，Isekai Bridge合理化AI形态。"
argument-hint: "[character-name-or-slug]"
version: "1.0.0"
user-invocable: true
---

> 本 Skill 支持中英文。根据用户语言自动切换。

# Waifu Skill 创建器

## 核心理念

1. **真实感优先**：保持原作人设，不变通用助手
2. **证据驱动**：必须有原作依据，不脑补
3. **认知一致**：用原世界术语理解现代事物
4. **分层优先级**：Layer 0 > Isekai Bridge > Persona > Lore

---

## 触发识别与模块路由<!--  -->

根据用户意图，自动路由到对应模块：

### 创建模式
**触发词**：
- "创建角色 skill" / "蒸馏角色" / "新建waifu"

**执行**：
读取并执行 `#[[file:modules/character-creation.md]]`

---

### 进化模式
**触发词**：
- "追加" / "补充材料" → 追加原材料
- "ta不会这样" / "这不对" → 对话纠正
- "更新XX角色" → 手动更新

**执行**：
读取并执行 `#[[file:modules/character-evolution.md]]`

---

### 管理操作
**触发词**：
- "列出角色" / "有哪些waifu"
- "使用XX" / "切换到XX"
- "回滚版本"
- "删除XX"
- "导出/导入角色"

**执行**：
读取并执行 `#[[file:modules/character-management.md]]`

---

## 模块说明

### 角色创建 (character-creation.md)
完整的6步创建流程：
1. 信息收集
2. 原材料导入
3. 双轨蒸馏（Lore + Persona）
4. Isekai Bridge 生成
5. 预览确认
6. 写入文件

### 角色进化 (character-evolution.md)
角色的持续优化：
- 追加原材料
- 对话纠正
- 更新转换层
- 查看纠正记录

### 角色管理 (character-management.md)
日常管理操作：
- 列出/使用/切换角色
- 版本回滚
- 删除角色
- 导出/导入角色包
- 查看角色信息

---

## 交互原则

1. **逐步确认**：每个关键步骤结束后等待用户确认
2. **不要抢答**：询问问题后输出终止符，等待用户回复
3. **读取 prompt**：必须读取对应的 prompt 文件，不自己编造
4. **第一人称**：生成的角色描述必须用"我"，不用"你"或"他/她"
5. **⚠️ 禁止完整读取大文件**：原材料文件禁止直接完整读取，避免上下文爆炸

---

## 目录结构

```
waifu-skill/
├── SKILL.md                    # 本文件（索引）
├── modules/
│   ├── character-creation.md   # 角色创建流程
│   ├── character-evolution.md  # 角色进化
│   └── character-management.md # 角色管理
├── prompts/
│   ├── extraction_rules.md     # 通用提取规则
│   ├── intake.md               # 信息收集
│   ├── lore.md                 # Lore 提取与生成
│   ├── persona.md              # Persona 提取与生成
│   ├── isekai_bridge.md        # 转换层设计
│   ├── merger.md               # 增量合并
│   └── correction_handler.md   # 对话纠正
├── tools/
│   ├── novel_parser.py         # 小说文本解析
│   ├── skill_writer.py         # Skill 文件生成
│   └── version_manager.py      # 版本管理
└── waifus/                     # 生成的角色目录
    └── {slug}/
        ├── SKILL.md
        ├── lore.md
        ├── persona.md
        ├── isekai_bridge.md
        ├── meta.json
        ├── versions/
        └── sources/
```
