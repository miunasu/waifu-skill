# Correction Handler - 对话纠正处理

> 当用户指出角色的回答"不像ta"时，识别纠正内容，生成Correction记录，更新文件

## 核心原则

1. **用户是角色专家**：用户最了解角色，用户的纠正优先级最高
2. **立即生效**：纠正后立即更新文件，下次对话立即应用
3. **可追溯**：记录每次纠正，保留纠正历史，支持回滚

---

## 触发识别

### 纠正触发词

**明确纠正**：
- "ta不会这样说"
- "ta不会这么做"
- "这不像ta"
- "人设崩了"

**对比纠正**：
- "ta应该是..."
- "ta其实会..."
- "原作中ta是..."

**程度纠正**：
- "太温柔了"
- "太冷漠了"
- "太正式了"

---

## 纠正内容解析

### 提取关键信息

**需要提取**：
1. **场景**：在什么情况下
2. **错误行为**：AI做了什么不像ta的事
3. **正确行为**：ta实际上会怎么做
4. **原因**：为什么这样才对

**解析模板**：

```markdown
## 纠正内容解析

### 场景
{描述触发纠正的对话场景}

### 错误行为
AI的回答："{ai_response}"
问题：{what_is_wrong}

### 正确行为
角色应该：{correct_behavior}
原因：{reason}

### 证据
原作依据：{evidence}（如果用户提供）
```

---

## 归属判断

根据纠正内容，判断应该更新哪个文件的哪个部分：

| 纠正类型 | 归属 | 更新位置 |
|---------|------|---------|
| 核心信念/行为底线 | Persona | Layer 0 |
| 身份信息 | Persona | Layer 1 |
| 说话方式/口头禅/语气 | Persona | Layer 2 |
| 情感表达/反应方式 | Persona | Layer 3 |
| 人际互动/态度 | Persona | Layer 4 |
| 世界观/背景/经历 | Lore | 对应章节 |
| 能力/技能 | Lore | 能力体系 |
| 知识范围 | Lore | 知识范围 |
| 穿越认知/术语理解 | Isekai Bridge | 对应章节 |

---

## Correction记录生成

### 记录格式

```markdown
## Correction 记录

### #{correction_id} - {date}
- **场景**：{scenario}
- **错误行为**：{wrong_behavior}
- **正确行为**：{correct_behavior}
- **归属**：{target}
- **原因**：{reason}
- **证据**：{evidence}（可选）
```

---

## 文件更新

### 更新流程

1. 备份当前版本
2. 读取目标文件（persona.md / lore.md / isekai_bridge.md）
3. 追加Correction记录
4. 更新对应内容（可选）
5. 重新生成SKILL.md
6. 更新meta.json

---

## 用户交互

### 纠正确认

```markdown
## 收到纠正

我理解了，让我确认一下：

### 场景
{scenario}

### 问题
我的回答："{ai_response}"
问题：{what_is_wrong}

### 改进
{name}应该：{correct_behavior}
原因：{reason}

### 更新计划
- 归属：{target}
- 操作：追加Correction记录到{file}

**是否正确理解？**
1. 是的，请更新
2. 不对，让我重新说明
```

### 更新完成

```markdown
✅ 已更新！

### 更新摘要
- 文件：{file}
- 位置：{section}
- Correction ID：#{id}
- 版本：v{old_version} → v{new_version}

### 下次对话
{name}会记住这个纠正，不会再犯同样的错误。
```
