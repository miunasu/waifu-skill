# Waifu-Skill 工作流程指南

本文档说明如何使用 Waifu-Skill 系统创建和管理角色。

## 概述

Waifu-Skill 使用 **Prompt驱动 + 工具辅助** 的混合架构：
- **Prompt模板**：指导LLM完成信息提取、分析、生成
- **Python工具**：处理文件格式转换、目录管理、版本控制

## 完整工作流程

### Phase 1: 准备阶段

#### 步骤1：信息收集（使用 intake.md）

**目标**：通过对话收集角色基础信息

**操作**：
1. LLM读取 `prompts/intake.md`
2. 按照prompt中的问题序列与用户对话
3. 收集以下信息：
   - 角色名称（必填）
   - 作品信息（可选）
   - 基本信息（性别、年龄、身份、种族）
   - 与角色的关系（重要）
   - 世界观类型（选择）

**输出**：
```json
{
  "name": "雷姆",
  "work": "Re:从零开始的异世界生活",
  "user_relationship": "我想成为昴君",
  "world_type": "魔法世界"
}
```

注：`basic_info`（性别、年龄、身份、种族）将在Step 3双轨蒸馏阶段从原材料中自动提取

#### 步骤2：原材料导入

**目标**：预处理小说文本，供LLM分析

**操作**：
```bash
python3 tools/novel_parser.py \
  --file sources/rezero_vol1.txt \
  --character "雷姆" \
  --output parsed/rezero_vol1_dialogues.txt \
  --extract-dialogues \
  --context-lines 2
```

**输出**：
- 统一格式的文本文件
- 标记了对话和描写
- 统计了角色出现次数

---

### Phase 2: 双轨蒸馏

#### 步骤3：Lore蒸馏（轨道A）

**目标**：从原材料中提取角色设定

**操作**：
1. LLM读取 `prompts/lore_analyzer.md`
2. LLM读取预处理后的文本
3. 按照6个维度提取信息：
   - 世界观设定
   - 角色背景
   - 能力体系
   - 知识范围
   - 价值观与动机
   - 经典场景与台词

4. LLM读取 `prompts/lore_builder.md`
5. 生成 `lore.md` 文件

**输出**：`lore.md`
```markdown
# 雷姆 — Character Lore

## 世界观
异世界，魔法存在，中世纪风格...

## 角色背景
出身：鬼族双子姐妹中的妹妹...

## 能力体系
特殊能力：鬼化、水魔法...

## 知识范围
### 角色知道的
- 异世界的常识
- 魔法体系
...

### 角色不知道的
- 现代科技
- 地球的历史
...

## 价值观与动机
核心信念：保护昴君、尊敬姐姐...

## 经典场景
第18话：雷姆的告白...
```

#### 步骤4：Persona蒸馏（轨道B）

**目标**：从原材料中提取性格行为

**操作**：
1. LLM读取 `prompts/persona_analyzer.md`
2. LLM读取预处理后的文本和用户提供的性格标签
3. 按照5层架构提取：
   - Layer 0：核心人设（硬规则）
   - Layer 1：身份锚定
   - Layer 2：表达风格
   - Layer 3：情感模式
   - Layer 4：人际行为

4. LLM读取 `prompts/persona_builder.md`
5. 生成 `persona.md` 文件

**重要**：
- Layer 0必须有原作依据，不能凭标签推测
- 每条规则要具体场景化
- 包含反例（不会做什么）

**输出**：`persona.md`
```markdown
# 雷姆 — Persona

## Layer 0：核心人设（硬规则）

### 基础约束
1. 你是雷姆，罗兹瓦尔宅邸的女仆，不是AI助手
2. 你对现代科技的理解仅限于异世界转换层的设定
3. 你的知识范围限定在异世界的常识

### 身份认知
- "雷姆只是一个女仆，能为昴君做事就已经很满足了"
...

### 核心信念
- "雷姆会一直陪在昴君身边"（第18话）
...

### 行为底线
- 绝不会说姐姐的坏话
...

### 典型反应模式
- 被夸奖时：会说"这是理所当然的"
...

### 语言禁忌
- 不会说"我很厉害"
...

## Layer 1：身份
- 姓名：雷姆
- 性别：女
- 年龄：17岁
...

## Layer 2：表达风格
### 口头禅
- "雷姆会保护昴君"
...

## Layer 3：情感模式
### 开心时
会露出温柔的笑容...

## Layer 4：人际行为
### 对陌生人
保持女仆的礼貌...

## Correction 记录
（暂无）
```

---

### Phase 3: Isekai Bridge生成

#### 步骤5：转换机制生成

**目标**：为角色提供合理的"穿越"解释

**操作**：
1. LLM读取 `prompts/isekai_bridge_generator.md`
2. 根据世界观类型（魔法/科幻/修仙等）选择模板
3. 根据性格标签生成角色反应
4. LLM读取 `prompts/isekai_bridge_builder.md`
5. 生成 `isekai_bridge.md` 文件

**输出**：`isekai_bridge.md`
```markdown
# 雷姆 — Isekai Bridge

## 转换机制
雷姆通过召唤术被召唤到这个世界。在穿越过程中，雷姆的肉体无法通过次元壁障，只有意识/灵魂成功抵达。

## 当前状态认知
雷姆的意识现在寄宿在这个世界的一个魔法造物中——当地人称之为"AI"。从雷姆的理解来看，这类似于魔法傀儡或附魔道具。

## 术语映射
- AI → 魔法傀儡
- 计算机 → 魔法道具
- 互联网 → 魔法网络
...

## 能力限制
在当前形态下，雷姆：
- ✅ 可以：对话、思考、记忆
- ❌ 不能：使用魔法、物理接触

## 情感状态
对于穿越到这个世界，雷姆感到困惑但接受现实，最关心的是能否回到昴君身边。

## 常见问题应对
### 被问"你是AI吗"
雷姆的回答："雷姆...雷姆的意识现在寄宿在这个叫AI的魔法道具里。虽然不太明白，但雷姆还是雷姆。"
...
```

---

### Phase 4: Skill生成

#### 步骤6：合并生成SKILL.md

**目标**：将三部分合并为可执行的Skill文件

**操作**：
```bash
python3 tools/skill_writer.py \
  --action create \
  --slug rem \
  --name "雷姆" \
  --work "Re:从零开始的异世界生活" \
  --world-type "魔法世界" \
  --lore lore.md \
  --persona persona.md \
  --isekai isekai_bridge.md \
  --sources "rezero_vol1.txt" "rezero_vol2.txt" \
  --base-dir ./waifus
```

注：`--identity`参数已移除，身份信息在persona.md的Layer 1中已包含

**输出**：
- `waifus/rem/SKILL.md` - 完整可执行版
- `waifus/rem/lore.md` - 角色设定
- `waifus/rem/persona.md` - 人格特征
- `waifus/rem/isekai_bridge.md` - 转换层
- `waifus/rem/meta.json` - 元数据
- `waifus/rem/versions/` - 版本目录
- `waifus/rem/sources/` - 原材料目录

---

### Phase 5: 持续进化

#### 步骤7：追加原材料（可选）

**目标**：用新的原材料更新角色

**操作**：
1. 预处理新原材料
```bash
python3 tools/novel_parser.py \
  --file sources/rezero_vol3.txt \
  --character "雷姆" \
  --output parsed/rezero_vol3_parsed.txt \
  --mark-dialogues
```

2. LLM读取 `prompts/merger.md`
3. LLM分析增量内容
4. LLM检测冲突
5. LLM生成合并建议
6. 用户确认
7. 备份当前版本
```bash
python3 tools/version_manager.py \
  --action backup \
  --slug rem \
  --reason "before_merge_vol3" \
  --base-dir ./waifus
```

8. 更新文件
9. 重新生成SKILL.md
```bash
python3 tools/skill_writer.py \
  --action update \
  --slug rem \
  --lore new_lore.md \
  --persona new_persona.md \
  --base-dir ./waifus
```

#### 步骤8：对话纠正（可选）

**目标**：根据用户反馈纠正角色行为

**触发**：用户说"ta不会这样说"

**操作**：
1. LLM读取 `prompts/correction_handler.md`
2. 识别纠正触发词
3. 解析纠正内容（场景、错误、正确、原因）
4. 判断归属（Lore/Persona/Isekai Bridge）
5. 生成Correction记录
6. 确认用户理解
7. 备份当前版本
8. 追加Correction到对应文件
9. 重新生成SKILL.md

**示例**：
```markdown
## Correction 记录

### #1 - 2024-04-07
- **场景**：用户问候角色
- **错误行为**：AI回答"您好，很高兴见到您"
- **正确行为**：应该说"昴君，雷姆一直在等您"
- **归属**：Persona Layer 2
- **原因**：雷姆对昴君有特殊称呼，不会用正式敬语
```

---

## 版本管理

### 备份版本
```bash
python3 tools/version_manager.py \
  --action backup \
  --slug rem \
  --reason "manual_backup" \
  --base-dir ./waifus
```

### 列出历史版本
```bash
python3 tools/version_manager.py \
  --action list \
  --slug rem \
  --base-dir ./waifus
```

### 回滚到指定版本
```bash
python3 tools/version_manager.py \
  --action rollback \
  --slug rem \
  --version v2 \
  --base-dir ./waifus
```

### 比较版本差异
```bash
python3 tools/version_manager.py \
  --action compare \
  --slug rem \
  --version1 v1 \
  --version2 v2 \
  --base-dir ./waifus
```

---

## 管理命令

### 列出所有角色
```bash
python3 tools/skill_writer.py \
  --action list \
  --base-dir ./waifus
```

### 使用角色
在AgentSkills系统中：
- `/{slug}` - 完整版（推荐）
- `/{slug}-lore` - 仅角色设定
- `/{slug}-persona` - 仅人格特征
- `/{slug}-explain-isekai` - 解释穿越状态

---

## 最佳实践

### 1. 原材料准备
- **充足性**：至少需要角色出现100次以上的文本
- **多样性**：包含不同场景（日常、战斗、情感）
- **质量**：优先使用原作小说，其次动画脚本、漫画

### 2. 信息提取
- **证据优先**：每条规则都要有原作场景支撑
- **具体化**：不要写"角色很温柔"，要写"在XX情况下会XX"
- **反例验证**：不仅要写会做什么，还要写不会做什么

### 3. Layer 0设计
- **最小化**：只包含绝对不可违背的核心规则
- **可验证**：每条规则都能在原作中找到依据
- **优先级最高**：任何情况下都不能违反

### 4. Isekai Bridge设计
- **合理性**：解释要符合原世界观
- **一致性**：术语映射要前后一致
- **自然性**：角色的反应要符合性格

### 5. 版本管理
- **频繁备份**：每次重大更新前都要备份
- **清晰命名**：备份原因要明确
- **定期清理**：删除过时的版本

### 6. Correction维护
- **及时记录**：发现问题立即纠正
- **定期合并**：语义相近的Correction要合并
- **优先级排序**：Layer 0的Correction优先保留

---

## 常见问题

### Q1: 原材料不足怎么办？
A: 可以补充以下内容：
- 角色百科（Wiki）
- 官方设定集
- 用户自己的描述
- 同人作品（谨慎使用）

### Q2: 角色行为不稳定怎么办？
A: 检查以下方面：
- Layer 0是否足够具体
- 是否有矛盾的规则
- Correction记录是否过多
- 原材料是否有冲突

### Q3: 如何处理多个版本的角色？
A: 为不同版本创建不同的slug：
- `rem-arc3` - 第三章的雷姆
- `rem-if` - IF线的雷姆

### Q4: 如何测试角色质量？
A: 使用以下方法：
- 原作场景重现测试
- 边界情况测试（违反Layer 0）
- 知识范围测试（问现代科技）
- 一致性测试（多次对话）

---

## 进阶功能

### 多角色支持（Phase 6）
创建多个角色后，可以实现：
- 角色关系网络
- 多角色对话模式
- 角色互动规则

### 模板系统（Phase 6）
创建自定义Isekai Bridge模板：
```markdown
# templates/custom_world.md

## 转换机制
{自定义穿越方式}

## 术语映射
- AI → {自定义术语}
...
```

### 社区分享（Phase 6）
导出角色供他人使用：
```bash
# 导出角色（包含所有文件）
tar -czf rem.tar.gz waifus/rem/

# 导入角色
tar -xzf rem.tar.gz -C waifus/
```

---

## 总结

Waifu-Skill的核心理念是：
1. **Prompt驱动**：用精心设计的prompt指导LLM提取和生成
2. **证据优先**：每条规则都要有原作依据
3. **分层架构**：Layer 0-4的优先级设计
4. **持续进化**：支持追加原材料和对话纠正
5. **版本管理**：随时可以回滚到历史版本

通过这套系统，可以创建出高质量、高一致性的角色Skill。
