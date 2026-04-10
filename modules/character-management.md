# 角色管理模块

> 本模块负责角色的日常管理操作

## 触发条件
- "列出角色" / "有哪些waifu" → 列出所有角色
- "使用XX" / "切换到XX" → 使用对应 skill
- "回滚版本" → 版本回滚
- "删除XX" → 删除角色

---

## 列出角色

**执行**：
```bash
python3 tools/skill_writer.py --action list --base-dir ./waifus
```

**输出示例**：
```
已创建的角色：
1. 雷姆 (rem) - 《Re:从零开始的异世界生活》
2. 初音未来 (miku) - 《VOCALOID》
3. 阿尔托莉雅 (artoria) - 《Fate》
```

---

## 使用角色

**执行**：
1. 确认角色存在
2. 读取 `waifus/{slug}/SKILL.md`
3. 加载角色设定
4. 开始对话

**提示**：
```
已切换到 {name}
可以开始对话了！
```

---

## 回滚版本

**适用场景**：更新后发现问题，需要恢复到之前的版本

**列出版本**：
```bash
python3 tools/version_manager.py --action list --slug {slug} --base-dir ./waifus
```

**输出示例**：
```
版本历史：
- v5 (2024-03-15 14:30) - 对话纠正：修正语气
- v4 (2024-03-14 10:20) - 追加原材料
- v3 (2024-03-13 16:45) - 更新转换层
- v2 (2024-03-12 09:15) - 对话纠正：修正能力描述
- v1 (2024-03-10 20:00) - 初始创建
```

**回滚到指定版本**：
```bash
python3 tools/version_manager.py --action rollback --slug {slug} --version {v} --base-dir ./waifus
```

**确认流程**：
1. 显示目标版本信息
2. 警告：回滚后当前版本将丢失
3. 询问确认
4. 执行回滚

---

## 删除角色

**执行流程**：
1. 确认角色存在
2. 显示角色信息
3. 警告：删除后无法恢复
4. 二次确认（输入角色名）
5. 删除 `waifus/{slug}/` 目录

**确认对话**：
```
确定要删除 {name} 吗？
此操作无法撤销！

请输入角色名以确认：
```

---

## 查看角色信息

**触发条件**：
- "查看XX的设定"
- "XX的性格"
- "XX的能力"

**执行**：
1. 读取 `waifus/{slug}/meta.json`
2. 根据询问内容读取对应文件：
   - 设定/背景/能力 → `lore.md`
   - 性格/说话方式 → `persona.md`
   - 转换层 → `isekai_bridge.md`
3. 展示相关内容

---

## 导出角色

**触发条件**：
- "导出XX角色"
- "打包XX"

**执行**：
```bash
python3 tools/skill_writer.py --action export --slug {slug} --output {name}.zip --base-dir ./waifus
```

**包含内容**：
- 所有配置文件
- 版本历史
- 原材料（如果保存了）

---

## 导入角色

**触发条件**：
- "导入角色"
- "安装角色包"

**执行**：
```bash
python3 tools/skill_writer.py --action import --file {name}.zip --base-dir ./waifus
```

**冲突处理**：
- 如果角色已存在，询问是否覆盖
- 提供重命名选项
