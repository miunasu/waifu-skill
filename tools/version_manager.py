#!/usr/bin/env python3
"""
版本管理工具

功能：
1. 备份当前版本
2. 回滚到指定版本
3. 列出历史版本
4. 比较版本差异（可选）

用法：
    # 备份当前版本
    python3 version_manager.py --action backup --slug rem --base-dir ../waifus
    
    # 列出历史版本
    python3 version_manager.py --action list --slug rem --base-dir ../waifus
    
    # 回滚到指定版本
    python3 version_manager.py --action rollback --slug rem --version v2 --base-dir ../waifus
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

def read_meta(skill_dir: Path) -> Dict:
    """读取 meta.json"""
    meta_path = skill_dir / "meta.json"
    if not meta_path.exists():
        raise FileNotFoundError(f"meta.json 不存在：{meta_path}")
    
    with open(meta_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def write_meta(skill_dir: Path, meta: Dict):
    """写入 meta.json"""
    with open(skill_dir / "meta.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

def increment_version(version: str) -> str:
    """递增版本号"""
    # v1 -> v2
    if version.startswith('v'):
        num = int(version[1:])
        return f"v{num + 1}"
    return "v1"

def backup_version(base_dir: Path, slug: str, reason: str = "manual_backup") -> str:
    """备份当前版本"""
    skill_dir = base_dir / slug
    if not skill_dir.exists():
        raise FileNotFoundError(f"角色不存在：{slug}")
    
    print(f"正在备份角色：{slug}")
    
    # 读取当前版本号
    meta = read_meta(skill_dir)
    current_version = meta['version']
    
    # 生成新版本号
    new_version = increment_version(current_version)
    
    # 创建版本目录
    version_dir = skill_dir / "versions" / current_version
    version_dir.mkdir(parents=True, exist_ok=True)
    
    # 备份文件
    files_to_backup = ["lore.md", "persona.md", "isekai_bridge.md", "SKILL.md", "meta.json"]
    for file in files_to_backup:
        src = skill_dir / file
        if src.exists():
            dst = version_dir / file
            shutil.copy2(src, dst)
    
    # 记录备份信息
    backup_info = {
        "version": current_version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "reason": reason,
        "backed_up_files": files_to_backup
    }
    
    with open(version_dir / "backup_info.json", "w", encoding='utf-8') as f:
        json.dump(backup_info, f, indent=2, ensure_ascii=False)
    
    print(f"✓ 备份完成：{current_version}")
    print(f"  备份目录：{version_dir}")
    print(f"  备份文件：{', '.join(files_to_backup)}")
    
    return current_version

def rollback_version(base_dir: Path, slug: str, target_version: str):
    """回滚到指定版本"""
    skill_dir = base_dir / slug
    if not skill_dir.exists():
        raise FileNotFoundError(f"角色不存在：{slug}")
    
    # 检查版本是否存在
    version_dir = skill_dir / "versions" / target_version
    if not version_dir.exists():
        raise FileNotFoundError(f"版本不存在：{target_version}")
    
    print(f"正在回滚角色：{slug} → {target_version}")
    
    # 读取当前版本
    current_meta = read_meta(skill_dir)
    current_version = current_meta['version']
    
    # 备份当前版本（以防回滚错误）
    print(f"  备份当前版本：{current_version}")
    backup_version(base_dir, slug, reason=f"before_rollback_to_{target_version}")
    
    # 恢复文件
    files_to_restore = ["lore.md", "persona.md", "isekai_bridge.md", "SKILL.md", "meta.json"]
    for file in files_to_restore:
        src = version_dir / file
        if src.exists():
            dst = skill_dir / file
            shutil.copy2(src, dst)
            print(f"  ✓ 恢复 {file}")
    
    # 更新 meta.json 的时间戳
    meta = read_meta(skill_dir)
    meta['updated_at'] = datetime.now(timezone.utc).isoformat()
    write_meta(skill_dir, meta)
    
    print(f"\n✅ 回滚完成！")
    print(f"  从版本：{current_version}")
    print(f"  到版本：{target_version}")
    print(f"  当前版本已备份到：versions/{current_version}")

def list_versions(base_dir: Path, slug: str) -> List[Dict]:
    """列出所有版本"""
    skill_dir = base_dir / slug
    if not skill_dir.exists():
        raise FileNotFoundError(f"角色不存在：{slug}")
    
    versions_dir = skill_dir / "versions"
    if not versions_dir.exists():
        return []
    
    versions = []
    for version_path in sorted(versions_dir.iterdir()):
        if version_path.is_dir():
            backup_info_path = version_path / "backup_info.json"
            if backup_info_path.exists():
                with open(backup_info_path, 'r', encoding='utf-8') as f:
                    info = json.load(f)
                versions.append(info)
    
    return sorted(versions, key=lambda x: x['timestamp'], reverse=True)

def compare_versions(base_dir: Path, slug: str, version1: str, version2: str):
    """比较两个版本的差异（简单实现）"""
    skill_dir = base_dir / slug
    
    version1_dir = skill_dir / "versions" / version1
    version2_dir = skill_dir / "versions" / version2
    
    if not version1_dir.exists():
        raise FileNotFoundError(f"版本不存在：{version1}")
    if not version2_dir.exists():
        raise FileNotFoundError(f"版本不存在：{version2}")
    
    print(f"\n比较版本：{version1} vs {version2}\n")
    
    files_to_compare = ["lore.md", "persona.md", "isekai_bridge.md"]
    
    for file in files_to_compare:
        file1 = version1_dir / file
        file2 = version2_dir / file
        
        if file1.exists() and file2.exists():
            content1 = file1.read_text(encoding='utf-8')
            content2 = file2.read_text(encoding='utf-8')
            
            if content1 != content2:
                print(f"📝 {file} 有变化")
                print(f"  {version1} 字数：{len(content1)}")
                print(f"  {version2} 字数：{len(content2)}")
                print(f"  差异：{len(content2) - len(content1):+d} 字")
            else:
                print(f"✓ {file} 无变化")
        else:
            print(f"⚠ {file} 在某个版本中不存在")
        
        print()

def main():
    parser = argparse.ArgumentParser(description='版本管理工具')
    parser.add_argument('--action', required=True, 
                       choices=['backup', 'rollback', 'list', 'compare'],
                       help='操作类型')
    parser.add_argument('--base-dir', default='../waifus', help='角色目录')
    parser.add_argument('--slug', required=True, help='角色slug')
    parser.add_argument('--version', help='目标版本（用于rollback）')
    parser.add_argument('--version1', help='版本1（用于compare）')
    parser.add_argument('--version2', help='版本2（用于compare）')
    parser.add_argument('--reason', default='manual_backup', help='备份原因')
    
    args = parser.parse_args()
    base_dir = Path(args.base_dir)
    
    try:
        if args.action == 'backup':
            version = backup_version(base_dir, args.slug, args.reason)
            print(f"\n✅ 备份完成：{version}")
        
        elif args.action == 'rollback':
            if not args.version:
                print("错误：回滚需要指定 --version")
                return
            rollback_version(base_dir, args.slug, args.version)
        
        elif args.action == 'list':
            versions = list_versions(base_dir, args.slug)
            if not versions:
                print(f"角色 {args.slug} 暂无历史版本")
            else:
                print(f"\n角色 {args.slug} 的历史版本：\n")
                for info in versions:
                    print(f"版本：{info['version']}")
                    print(f"  时间：{info['timestamp']}")
                    print(f"  原因：{info['reason']}")
                    print(f"  文件：{', '.join(info['backed_up_files'])}")
                    print()
        
        elif args.action == 'compare':
            if not args.version1 or not args.version2:
                print("错误：比较需要指定 --version1 和 --version2")
                return
            compare_versions(base_dir, args.slug, args.version1, args.version2)
    
    except Exception as e:
        print(f"\n❌ 错误：{e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
