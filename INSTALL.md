# Waifu-Skill 安装指南

## 系统要求

- Python 3.8+
- pip（Python包管理器）
- 支持的操作系统：Windows, macOS, Linux

## 安装步骤

### 1. 克隆或下载项目

```bash
# 如果使用Git
git clone <repository-url>
cd waifu-skill

# 或者直接下载ZIP并解压
```

### 2. 安装Python依赖

```bash
pip install -r requirements.txt
```

**依赖包说明**：
- `ebooklib` - 用于解析EPUB格式电子书
- `beautifulsoup4` - 用于解析HTML内容
- `PyPDF2` - 用于解析PDF文件

### 3. 验证安装

```bash
# 测试novel_parser
python3 tools/novel_parser.py --help

# 测试skill_writer
python3 tools/skill_writer.py --help

# 测试version_manager
python3 tools/version_manager.py --help
```

如果看到帮助信息，说明安装成功。

## 目录结构

安装后的目录结构：

```
waifu-skill/
├── SKILL.md                # AgentSkills入口
├── README.md               # 项目说明
├── LICENSE                 # MIT许可证
├── INSTALL.md              # 本文件
├── requirements.txt        # Python依赖
├── prompts/                # Prompt模板
│   ├── intake.md
│   ├── lore_analyzer.md
│   ├── persona_analyzer.md
│   ├── isekai_bridge_generator.md
│   ├── lore_builder.md
│   ├── persona_builder.md
│   ├── isekai_bridge_builder.md
│   ├── merger.md
│   └── correction_handler.md
├── tools/                  # Python工具
│   ├── novel_parser.py
│   ├── skill_writer.py
│   └── version_manager.py
├── waifus/                 # 生成的角色（初始为空）
├── templates/              # Isekai Bridge模板库（可选）
└── docs/                   # 文档
    ├── WORKFLOW.md
    └── EXAMPLE.md
```

## 快速开始

### 创建第一个角色

1. **准备原材料**

创建 `sources/` 目录并放入小说文本：
```bash
mkdir -p sources
# 将小说文件放入 sources/ 目录
```

2. **预处理文本**

```bash
python3 tools/novel_parser.py \
  --file sources/your_novel.txt \
  --character "角色名" \
  --output parsed/dialogues.txt \
  --extract-dialogues \
  --context-lines 2
```

3. **使用LLM进行蒸馏**

- 让LLM读取 `prompts/intake.md` 收集基础信息
- 让LLM读取 `prompts/lore_analyzer.md` 和预处理文本，生成 `lore.md`
- 让LLM读取 `prompts/persona_analyzer.md` 和预处理文本，生成 `persona.md`
- 让LLM读取 `prompts/isekai_bridge_generator.md`，生成 `isekai_bridge.md`

4. **生成Skill文件**

```bash
python3 tools/skill_writer.py \
  --action create \
  --slug your-character \
  --name "角色名" \
  --work "作品名" \
  --world-type "魔法世界" \
  --lore lore.md \
  --persona persona.md \
  --isekai isekai_bridge.md \
  --base-dir ./waifus
```

注：`--identity`参数已移除，身份信息在persona.md的Layer 1中已包含

5. **在AgentSkills中使用**

将生成的 `waifus/your-character/SKILL.md` 添加到AgentSkills系统中，使用 `/your-character` 触发。

## 常见问题

### Q: 安装依赖时出错

A: 尝试使用虚拟环境：
```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Q: 无法解析EPUB文件

A: 确保安装了 `ebooklib` 和 `beautifulsoup4`：
```bash
pip install ebooklib beautifulsoup4
```

### Q: 无法解析PDF文件

A: 确保安装了 `PyPDF2`：
```bash
pip install PyPDF2
```

### Q: 工具提示"文件不存在"

A: 检查文件路径是否正确，使用相对路径或绝对路径。

### Q: 生成的SKILL.md格式不对

A: 检查 `lore.md`, `persona.md`, `isekai_bridge.md` 的格式是否正确。

## 升级

如果有新版本发布：

```bash
# 备份现有角色
cp -r waifus waifus_backup

# 更新代码
git pull  # 或重新下载

# 重新安装依赖
pip install -r requirements.txt --upgrade

# 恢复角色
cp -r waifus_backup/* waifus/
```

## 卸载

```bash
# 删除虚拟环境（如果使用）
rm -rf venv

# 删除项目目录
cd ..
rm -rf waifu-skill
```

## 下一步

- 阅读 [WORKFLOW.md](docs/WORKFLOW.md) 了解完整工作流程
- 阅读 [EXAMPLE.md](docs/EXAMPLE.md) 查看完整示例
- 查看 [README.md](README.md) 了解项目概述

## 技术支持

如果遇到问题，请：
1. 检查本文档的常见问题部分
2. 查看项目文档
3. 提交Issue（如果使用Git仓库）

## 许可证

本项目使用MIT许可证，详见 [LICENSE](LICENSE) 文件。
