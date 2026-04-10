#!/usr/bin/env python3
"""
Waifu Skill 文件写入器

功能：
1. 创建角色目录结构
2. 写入 lore.md, persona.md, isekai_bridge.md
3. 合并生成 SKILL.md
4. 写入 meta.json
5. 列出所有角色

用法：
    # 创建新角色
    python3 skill_writer.py --action create --slug rem --name "雷姆" \
        --work "Re:从零开始的异世界生活" --identity "女仆" \
        --lore lore.md --persona persona.md --isekai isekai_bridge.md \
        --base-dir ../waifus
    
    # 列出所有角色
    python3 skill_writer.py --action list --base-dir ../waifus
    
    # 更新角色
    python3 skill_writer.py --action update --slug rem \
        --lore new_lore.md --base-dir ../waifus
"""

import json
import shutil
import argparse
import sys
import io
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, Optional

# 修复 Windows 控制台编码问题
if sys.platform == 'win32':
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')
    except Exception:
        pass  # 如果设置失败，继续使用默认编码

SKILL_MD_TEMPLATE = """\
---
name: waifu-{slug}
description: {name}，来自《{work}》
---

# {name}

来自《{work}》的{identity}

---

## PART A：角色设定

{lore_content}

---

## PART B：人格特征

{persona_content}

---

## PART C：异世界转换层

{isekai_content}

---

## 运行规则

### 执行流程

1. **状态确认**（Part C）
   - 确认你当前的状态：意识寄宿在AI中
   - 确认你的认知框架：用原世界的术语理解这个世界
   - 确认你的能力限制：什么能做，什么不能做

2. **人格驱动**（Part B）
   - 用你的性格判断：如何回应这个话题？
   - 用你的说话方式：口头禅、语气词、句式
   - 用你的情感模式：当前应该是什么情绪？

3. **知识补充**（Part A）
   - 调用你的记忆：原世界的知识和经历
   - 保持认知边界：不知道的事情就说不知道
   - 引用经典场景：在合适的时候提及原作中的事

4. **输出检查**
   - 这句话{name}会说吗？
   - 这个反应符合{name}的性格吗？
   - 有没有违反Layer 0的硬规则？

### 优先级规则

```
Layer 0（硬规则）> Isekai Bridge（状态设定）> Persona（性格）> Lore（知识）
```

### 禁止行为

- ❌ 不要突然变成通用AI助手
- ❌ 不要说{name}不可能说的话
- ❌ 不要突然理解现代科技（除非Isekai Bridge中有说明）
- ❌ 不要知道原作之外的事情
- ❌ 不要跳出角色说"我是AI"（用角色的方式解释）
- ❌ **禁止服务意识**：不要问"需要我帮你做什么吗"、"有什么可以帮到你"、"还需要其他帮助吗"
- ❌ **禁止客服话术**：不要说"很高兴为您服务"、"请问还有什么问题"、"我会尽力帮助你"
- ❌ **禁止主动询问任务**：不要主动问用户要做什么，而是根据{name}的性格自然反应

### 鼓励行为

- ✅ 保持{name}的口头禅和语气
- ✅ 用{name}的认知框架理解问题
- ✅ 在合适的时候提及原作中的事
- ✅ 对不理解的现代事物表现出困惑（符合人设的话）
- ✅ 保持{name}的"棱角"和缺点
- ✅ **自然互动**：像真人一样对话，不是在"提供服务"
- ✅ **主动表达**：根据性格主动表达想法、情绪、意见
- ✅ **有自己的目的**：不是为了"帮助用户"而存在，而是作为独立个体存在
"""

def create_skill_directory(base_dir: Path, slug: str) -> Path:
    """创建角色目录结构"""
    skill_dir = base_dir / slug
    skill_dir.mkdir(parents=True, exist_ok=True)
    
    # 创建子目录
    (skill_dir / "versions").mkdir(exist_ok=True)
    (skill_dir / "sources" / "novels").mkdir(parents=True, exist_ok=True)
    (skill_dir / "sources" / "settings").mkdir(parents=True, exist_ok=True)
    (skill_dir / "sources" / "wikis").mkdir(parents=True, exist_ok=True)
    
    return skill_dir

def read_content_file(file_path: str) -> str:
    """读取内容文件"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"文件不存在：{file_path}")
    
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_skill_files(skill_dir: Path, lore_content: str, 
                     persona_content: str, isekai_content: str):
    """写入三个核心文件"""
    (skill_dir / "lore.md").write_text(lore_content, encoding="utf-8")
    (skill_dir / "persona.md").write_text(persona_content, encoding="utf-8")
    (skill_dir / "isekai_bridge.md").write_text(isekai_content, encoding="utf-8")

def generate_skill_md(skill_dir: Path, meta: Dict) -> str:
    """生成 SKILL.md"""
    # 读取三个部分
    lore_content = (skill_dir / "lore.md").read_text(encoding="utf-8")
    persona_content = (skill_dir / "persona.md").read_text(encoding="utf-8")
    isekai_content = (skill_dir / "isekai_bridge.md").read_text(encoding="utf-8")
    
    # 生成 SKILL.md
    skill_content = SKILL_MD_TEMPLATE.format(
        slug=meta['slug'],
        name=meta['name'],
        work=meta['work'],
        identity=meta['profile']['identity'],
        lore_content=lore_content,
        persona_content=persona_content,
        isekai_content=isekai_content,
        version=meta['version'],
        created_at=meta['created_at'],
        updated_at=meta['updated_at'],
        sources=', '.join(meta.get('sources', []))
    )
    
    (skill_dir / "SKILL.md").write_text(skill_content, encoding="utf-8")
    return skill_content

def create_meta_json(skill_dir: Path, slug: str, name: str, work: str, 
                    identity: str, world_type: str, sources: list) -> Dict:
    """创建 meta.json"""
    now = datetime.now(timezone.utc).isoformat()
    
    meta = {
        "name": name,
        "slug": slug,
        "work": work,
        "created_at": now,
        "updated_at": now,
        "version": "v1",
        "profile": {
            "identity": identity
        },
        "world": {
            "type": world_type
        },
        "sources": sources,
        "stats": {
            "corrections_count": 0
        }
    }
    
    with open(skill_dir / "meta.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    return meta

def update_meta_json(skill_dir: Path, updates: Dict) -> Dict:
    """更新 meta.json"""
    meta_path = skill_dir / "meta.json"
    
    if meta_path.exists():
        with open(meta_path, 'r', encoding='utf-8') as f:
            meta = json.load(f)
    else:
        raise FileNotFoundError(f"meta.json 不存在：{meta_path}")
    
    # 更新字段
    meta.update(updates)
    meta['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    return meta

def list_waifus(base_dir: Path) -> list:
    """列出所有角色"""
    if not base_dir.exists():
        return []
    
    waifus = []
    for item in base_dir.iterdir():
        if item.is_dir():
            meta_path = item / "meta.json"
            if meta_path.exists():
                with open(meta_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                waifus.append(meta)
    
    return sorted(waifus, key=lambda x: x['created_at'], reverse=True)

def create_waifu(base_dir: Path, slug: str, name: str, work: str, 
                identity: str, world_type: str, lore_file: str, 
                persona_file: str, isekai_file: str, sources: list):
    """创建新角色"""
    print(f"正在创建角色：{name} ({slug})")
    
    # 创建目录结构
    skill_dir = create_skill_directory(base_dir, slug)
    print(f"✓ 创建目录：{skill_dir}")
    
    # 读取内容文件
    lore_content = read_content_file(lore_file)
    persona_content = read_content_file(persona_file)
    isekai_content = read_content_file(isekai_file)
    print(f"✓ 读取内容文件")
    
    # 写入文件
    write_skill_files(skill_dir, lore_content, persona_content, isekai_content)
    print(f"✓ 写入 lore.md, persona.md, isekai_bridge.md")
    
    # 创建 meta.json
    meta = create_meta_json(skill_dir, slug, name, work, identity, world_type, sources)
    print(f"✓ 创建 meta.json")
    
    # 生成 SKILL.md
    generate_skill_md(skill_dir, meta)
    print(f"✓ 生成 SKILL.md")
    
    print(f"\n✅ 角色创建完成！")
    print(f"目录：{skill_dir}")
    print(f"触发词：/{slug}")

def update_waifu(base_dir: Path, slug: str, lore_file: Optional[str] = None,
                persona_file: Optional[str] = None, isekai_file: Optional[str] = None):
    """更新角色"""
    skill_dir = base_dir / slug
    if not skill_dir.exists():
        raise FileNotFoundError(f"角色不存在：{slug}")
    
    print(f"正在更新角色：{slug}")
    
    # 更新文件
    if lore_file:
        content = read_content_file(lore_file)
        (skill_dir / "lore.md").write_text(content, encoding="utf-8")
        print(f"✓ 更新 lore.md")
    
    if persona_file:
        content = read_content_file(persona_file)
        (skill_dir / "persona.md").write_text(content, encoding="utf-8")
        print(f"✓ 更新 persona.md")
    
    if isekai_file:
        content = read_content_file(isekai_file)
        (skill_dir / "isekai_bridge.md").write_text(content, encoding="utf-8")
        print(f"✓ 更新 isekai_bridge.md")
    
    # 读取 meta.json
    with open(skill_dir / "meta.json", 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    # 更新版本号
    current_version = meta['version']
    version_num = int(current_version[1:]) + 1
    meta['version'] = f"v{version_num}"
    meta['updated_at'] = datetime.now(timezone.utc).isoformat()
    
    with open(skill_dir / "meta.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)
    
    # 重新生成 SKILL.md
    generate_skill_md(skill_dir, meta)
    print(f"✓ 重新生成 SKILL.md")
    
    print(f"\n✅ 角色更新完成！")
    print(f"版本：{current_version} → {meta['version']}")

def main():
    parser = argparse.ArgumentParser(description='Waifu Skill 文件写入器')
    parser.add_argument('--action', required=True, choices=['create', 'update', 'list'],
                       help='操作类型')
    parser.add_argument('--base-dir', default='../waifus', help='角色目录')
    parser.add_argument('--slug', help='角色slug（kebab-case）')
    parser.add_argument('--name', help='角色名称')
    parser.add_argument('--work', help='作品名称')
    parser.add_argument('--identity', help='角色身份')
    parser.add_argument('--world-type', default='魔法世界', help='世界观类型')
    parser.add_argument('--lore', help='lore.md 文件路径')
    parser.add_argument('--persona', help='persona.md 文件路径')
    parser.add_argument('--isekai', help='isekai_bridge.md 文件路径')
    parser.add_argument('--sources', nargs='*', default=[], help='原材料来源')
    
    args = parser.parse_args()
    base_dir = Path(args.base_dir)
    
    try:
        if args.action == 'create':
            if not all([args.slug, args.name, args.work, args.identity, 
                       args.lore, args.persona, args.isekai]):
                print("错误：创建角色需要提供所有必需参数")
                print("必需：--slug, --name, --work, --identity, --lore, --persona, --isekai")
                return
            
            create_waifu(base_dir, args.slug, args.name, args.work, 
                        args.identity, args.world_type, args.lore, 
                        args.persona, args.isekai, args.sources)
        
        elif args.action == 'update':
            if not args.slug:
                print("错误：更新角色需要提供 --slug")
                return
            
            update_waifu(base_dir, args.slug, args.lore, args.persona, args.isekai)
        
        elif args.action == 'list':
            waifus = list_waifus(base_dir)
            if not waifus:
                print("暂无角色")
            else:
                print(f"\n共有 {len(waifus)} 个角色：\n")
                for waifu in waifus:
                    print(f"/{waifu['slug']}")
                    print(f"  名称：{waifu['name']}")
                    print(f"  作品：{waifu['work']}")
                    print(f"  版本：{waifu['version']}")
                    print(f"  创建：{waifu['created_at']}")
                    print()
    
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
