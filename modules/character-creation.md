# 角色创建流程

> 本模块负责从零创建一个新的角色 Skill

## 触发条件
- "创建角色 skill" / "蒸馏角色" / "新建waifu"

## 执行规则

### 流程控制
1. 按顺序执行：Step 1 → 2 → 3 → 4 → 5 → 6
2. 不可跳步（除非用户明确说"跳过"）


### 禁止
- ❌ 跳过 prompt 文件读取
- ❌ 自己编造提取维度

---

## Step 1：信息收集 `[1/6]`

**执行**：
1. 读取 `prompts/intake.md`
2. 逐个询问（不要一次列出），如信息已知，直接跳过到下一Step。如果信息未知，输出终止符，等待用户回答问题
3. 角色名必填，其他可跳过
4. 展示汇总表格
5. 等待确认

**汇总格式**：
```
已收集：
- 角色名：{name}
- 作品：{work 或 "未提供"}
- 世界观：{world_type 或 "将从原材料中分析"}
- 与用户关系：{relationship}

注：角色的性别、年龄、身份、种族等基本信息将在蒸馏阶段从原材料中自动提取。

确认？
```

**重要**：
- 角色名和与用户关系是必填项
- 如果用户未提供关系，必须询问，不能跳过

---

## Step 2：原材料导入 `[2/6]`

**执行**：
1. 展示 4 种方式（A/B/C/D）
2. 等待用户选择
3. 执行对应处理
4. 记录文件名
5. 如信息已知，直接跳过到下一Step。如果信息未知，输出终止符，等待用户回答问题

**方式选择**：
```
原材料提供方式：

[A] 小说文件 (txt/epub/pdf)
[B] 设定文档 (PDF/图片/Markdown)
[C] 直接粘贴文本
[D] 提供链接

可混用或跳过。
```

### A. 小说文件

提取对话（供后续LLM分析）
```bash
python3 tools/novel_parser.py \
  --file {file} \
  --character "{name}" \
  --output dialogues.txt \
  --extract-dialogues \
  --context-lines 2
```

### B. 设定文档
直接读取文件内容。

### C/D. 粘贴/链接
直接使用用户提供的文本。

---

## Step 3：双轨蒸馏 `[3/6]`

**执行**：
1. 读取 `prompts/extraction_rules.md`（通用规则）
2. 读取 `prompts/lore.md` 和 `prompts/persona.md`
3. 读取原材料（如 `dialogues.txt`）
4. **边识别目标角色，边提取信息**（一步完成）
5. 生成结构化结果
6. 展示摘要（每维度 2-3 条）

### 💡 并发处理策略（可选）

**如果你具有子Agent能力且原材料较大（如对话组超过100个）**：

可以采用并发策略提高效率：

**方案A：按对话组分段**
```
子Agent 1: 分析对话组 #1-50   → 提取Lore + Persona
子Agent 2: 分析对话组 #51-100 → 提取Lore + Persona
子Agent 3: 分析对话组 #101-150 → 提取Lore + Persona
主Agent: 汇总并合并结果 → 去重、整理
```

**方案B：按维度分工**
```
子Agent 1: 专注提取Lore（世界观、能力、背景）
子Agent 2: 专注提取Persona Layer 0-2（核心人设、身份、说话方式）
子Agent 3: 专注提取Persona Layer 3-4（情感模式、人际行为）
主Agent: 汇总并整合结果
```

**注意事项**：
- 每个子Agent都需要读取extraction_rules.md和对应的prompt
- 确保子Agent之间不会重复提取相同信息
- 汇总时需要检查一致性，避免矛盾

**如果原材料较小或没有子Agent能力**：
- 直接单线程处理即可

---

## Step 4：Isekai Bridge `[4/6]`

**执行**：
1. 读取 `prompts/isekai_bridge.md`
2. 根据世界观选模板
3. 处理关系冲突（如有）
4. 生成转换层
5. 展示摘要

---

## Step 5：生成预览 `[5/6]`

**执行**：
1. 使用 `prompts/lore.md`、`persona.md`、`isekai_bridge.md` 的输出格式
2. 按格式生成三个文档（必须使用第一人称"我"）
3. 展示摘要（各 5-8 行）
4. 等待确认

**重要**：生成的所有角色描述必须以第一人称"我"的视角表达，让AI能够真正扮演这个角色。

**摘要格式**：
```
Lore：世界观、能力、知识...
Persona：核心人设、说话方式、情感...
Isekai Bridge：转换机制、术语映射...

确认生成？
```

---

## Step 6：写入文件 `[6/6]`

**执行**：
使用 `tools/skill_writer.py`：
```bash
python3 tools/skill_writer.py --action create \
  --slug {slug} \
  --name "{name}" \
  --work "{work}" \
  --world-type "{world_type}" \
  --lore lore.md \
  --persona persona.md \
  --isekai isekai_bridge.md \
  --base-dir ./waifus
```

注：`identity`（身份）等信息已在persona.md的Layer 1中提取，不需要单独传递

**目录结构**：
```
waifus/{slug}/
├── lore.md
├── persona.md
├── isekai_bridge.md
├── SKILL.md
├── meta.json
├── versions/
└── sources/
```

**完成提示**：
```
✅ 角色 Skill 已创建！

位置：waifus/{slug}/
使用：提及"{name}"开始对话
查看设定/性格/状态：直接询问

不对劲？说"ta不会这样"来更新。
```
