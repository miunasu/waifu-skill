# 角色进化模块

> 本模块负责对已创建的角色进行更新和优化

## 触发条件
- "追加" / "补充材料" → 追加原材料
- "ta不会这样" / "这不对" → 对话纠正
- "更新XX角色" → 手动更新

---

## 追加原材料

**适用场景**：发现新的原作内容，需要补充角色信息

**执行流程**：
1. 按 `character-creation.md` 的 Step 2 读取新内容
2. 读取现有 `lore.md` 和 `persona.md`
3. 参考 `prompts/merger.md` 分析增量
4. 检测冲突
5. 生成合并建议
6. 备份版本
7. 追加内容
8. 更新文件

**备份命令**：
```bash
python3 tools/version_manager.py --action backup --slug {slug} --base-dir ./waifus
```

**更新命令**：
```bash
python3 tools/skill_writer.py --action update --slug {slug} --base-dir ./waifus
```

**策略**：补充细节，只增不减。

---

## 对话纠正

**适用场景**：角色在对话中表现不符合原作，需要纠正

**执行流程**：
1. 读取 `prompts/correction_handler.md`
2. 解析用户反馈：
   - 场景：什么情况下
   - 错误行为：角色做了什么/说了什么
   - 正确行为：应该怎样
   - 原因：为什么这样才对
3. 判断归属（Layer 0/1/2/3/4 或 Lore/Isekai）
4. 生成 Correction 记录
5. 确认理解
6. 备份版本
7. 追加到对应文件
8. 重新生成 SKILL.md

**记录格式**：
```markdown
### #1 - 日期
- 场景：XX
- 错误：XX
- 正确：XX
- 归属：Layer X
- 原因：XX
- 证据：XX
```

**归属判断**：
- Layer 0：核心人设冲突（如性别、种族、核心价值观）
- Layer 1：身份认知错误（如职业、地位）
- Layer 2：说话方式不对（如口头禅、语气）
- Layer 3：情感反应错误（如对某事的态度）
- Layer 4：人际行为不符（如对特定人物的互动方式）
- Lore：世界观、能力、知识错误
- Isekai Bridge：现代事物理解方式错误

---

## 更新转换层

**适用场景**：需要调整角色对现代事物的理解方式

**执行流程**：
1. 读取 `isekai_bridge.md`
2. 询问需要改变的内容
3. 参考 `prompts/isekai_bridge_generator.md` 重新生成
4. 备份版本
5. 更新文件

---

## 查看纠正记录

**执行**：
读取 `persona.md` 和 `lore.md` 的 `## Correction 记录` 节。

**用途**：
- 了解角色经过哪些调整
- 追踪角色进化历史
- 发现常见问题模式
