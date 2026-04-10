#!/usr/bin/env python3
"""
小说文本预处理工具

功能：
1. 读取 txt/epub/pdf 格式的小说文件
2. 提取纯文本内容
3. 标记对话段落（用引号识别）
4. 统计角色出现次数
5. 输出统一格式的文本，供 LLM 分析

用法：
    python3 novel_parser.py --file novel.txt --character "雷姆" --output parsed.txt
    python3 novel_parser.py --file novel.epub --character "雷姆" --output parsed.txt
    python3 novel_parser.py --file novel.pdf --character "雷姆" --output parsed.txt
"""

import re
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

def parse_txt(file_path: str) -> str:
    """读取 txt 文件"""
    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def parse_epub(file_path: str) -> str:
    """读取 epub 文件（需要 ebooklib）"""
    try:
        import ebooklib
        from ebooklib import epub
        from bs4 import BeautifulSoup
    except ImportError:
        return "错误：需要安装 ebooklib 和 beautifulsoup4\npip install ebooklib beautifulsoup4"
    
    book = epub.read_epub(file_path)
    chapters = []
    for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
        soup = BeautifulSoup(item.get_content(), 'html.parser')
        text = soup.get_text()
        if text.strip():
            chapters.append(text)
    return '\n\n'.join(chapters)

def parse_pdf(file_path: str) -> str:
    """读取 pdf 文件（需要 PyPDF2）"""
    try:
        import PyPDF2
    except ImportError:
        return "错误：需要安装 PyPDF2\npip install PyPDF2"
    
    with open(file_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        pages = []
        for page in reader.pages:
            text = page.extract_text()
            if text.strip():
                pages.append(text)
    return '\n\n'.join(pages)

def extract_dialogues_with_context(text: str, context_lines: int = 2) -> List[Dict]:
    """提取所有对话及其上下文
    
    Args:
        text: 原始文本
        context_lines: 上下文行数（默认2行）
    
    Returns:
        对话列表，每个对话包含：
        - dialogue_lines: 对话内容（可能是连续多句）
        - context_before: 对话前的上下文
        - context_after: 对话后的上下文
        - start_line: 起始行号
    """
    lines = text.split('\n')
    dialogues = []
    
    # 对话引号模式
    dialogue_patterns = [
        r'"[^"]+?"',  # 双引号
        r'「[^」]+?」',  # 日式引号
        r'『[^』]+?』',  # 日式书名号
        r'"[^"]+?"',  # 中文引号
        r"'[^']+?'",  # 单引号
    ]
    
    # 章节标记模式
    chapter_pattern = r'^---\s*chapter\d+\s*---$'
    
    def is_dialogue(line: str) -> bool:
        return any(re.search(p, line) for p in dialogue_patterns)
    
    def is_chapter_marker(line: str) -> bool:
        return re.match(chapter_pattern, line, re.IGNORECASE) is not None
    
    i = 0
    processed_indices = set()
    
    while i < len(lines):
        if i in processed_indices:
            i += 1
            continue
            
        line = lines[i].strip()
        if not line or is_chapter_marker(line):
            i += 1
            continue
        
        if is_dialogue(line):
            # 找到对话组的起始位置
            dialogue_start = i
            
            # 收集前N行作为上文（不包含对话和章节标记）
            context_before = []
            for j in range(context_lines, 0, -1):
                if dialogue_start - j >= 0:
                    prev = lines[dialogue_start - j].strip()
                    if prev and not is_dialogue(prev) and not is_chapter_marker(prev):
                        context_before.append(prev)
            
            # 收集所有连续的对话
            dialogue_lines = []
            while i < len(lines):
                curr = lines[i].strip()
                if not curr:
                    i += 1
                    continue
                if is_chapter_marker(curr):
                    break
                if is_dialogue(curr):
                    dialogue_lines.append(curr)
                    processed_indices.add(i)
                    i += 1
                else:
                    break
            
            # 收集后N行作为下文（不包含对话和章节标记）
            context_after = []
            for j in range(context_lines):
                if i + j < len(lines):
                    next_line = lines[i + j].strip()
                    if next_line and not is_dialogue(next_line) and not is_chapter_marker(next_line):
                        context_after.append(next_line)
            
            # 保存对话组
            dialogues.append({
                'dialogue_lines': dialogue_lines,
                'context_before': context_before,
                'context_after': context_after,
                'start_line': dialogue_start + 1  # 1-indexed
            })
        else:
            i += 1
    
    return dialogues

def format_dialogues_for_llm(dialogues: List[Dict], character_name: str) -> str:
    """格式化对话供LLM分析
    
    Args:
        dialogues: 对话列表
        character_name: 目标角色名称
    
    Returns:
        格式化的文本
    """
    result = []
    result.append(f"# 对话提取结果\n")
    result.append(f"目标角色：{character_name}\n")
    result.append(f"总对话组数：{len(dialogues)}\n")
    result.append(f"\n请分析以下对话，识别并提取目标角色「{character_name}」说的话。\n")
    result.append(f"注意：每个对话组可能包含多个角色的对话，请仔细区分。\n")
    result.append(f"\n---\n")
    
    for idx, dialogue in enumerate(dialogues, 1):
        result.append(f"\n## 对话组 #{idx} (行号: {dialogue['start_line']})\n")
        
        # 上文
        if dialogue['context_before']:
            result.append(f"\n### 上文\n")
            for line in dialogue['context_before']:
                result.append(f"{line}\n")
        
        # 对话
        result.append(f"\n### 对话内容\n")
        for line in dialogue['dialogue_lines']:
            result.append(f"{line}\n")
        
        # 下文
        if dialogue['context_after']:
            result.append(f"\n### 下文\n")
            for line in dialogue['context_after']:
                result.append(f"{line}\n")
        
        result.append(f"\n---\n")
    
    return ''.join(result)

def extract_character_mentions(text: str, character_name: str) -> Dict:
    """统计角色出现次数和位置"""
    lines = text.split('\n')
    mentions = []
    dialogue_count = 0
    description_count = 0
    
    for i, line in enumerate(lines):
        if character_name in line:
            context = line[:200] if len(line) > 200 else line
            mentions.append({
                'line_number': i + 1,
                'content': context
            })
            
            # 统计对话和描写中的出现次数
            if line.startswith('[对话]'):
                dialogue_count += 1
            elif line.startswith('[描写]'):
                description_count += 1
    
    return {
        'total_mentions': len(mentions),
        'dialogue_mentions': dialogue_count,
        'description_mentions': description_count,
        'sample_mentions': mentions[:50]  # 只返回前50个
    }

def clean_text(text: str) -> str:
    """清理文本，去除多余空行和特殊字符"""
    # 去除行首行尾空格
    lines = [line.strip() for line in text.split('\n')]
    # 过滤空行
    lines = [line for line in lines if line]
    # 合并为单个换行
    text = '\n'.join(lines)
    # 最后确保段落之间只有一个换行
    text = re.sub(r'\n{2,}', '\n', text)
    return text

def main():
    parser = argparse.ArgumentParser(description='小说文本预处理工具')
    parser.add_argument('--file', required=True, help='输入文件路径')
    parser.add_argument('--character', required=True, help='角色名称')
    parser.add_argument('--output', required=True, help='输出文件路径')
    parser.add_argument('--extract-dialogues', action='store_true', 
                       help='提取所有对话及上下文（供LLM分析目标角色）')
    parser.add_argument('--context-lines', type=int, default=2,
                       help='上下文行数（默认2行）')
    parser.add_argument('--clean', action='store_true', help='清理文本')
    
    args = parser.parse_args()
    
    file_path = Path(args.file)
    if not file_path.exists():
        print(f"错误：文件不存在 {file_path}")
        return
    
    # 根据文件类型选择解析器
    ext = file_path.suffix.lower()
    print(f"正在解析 {ext} 文件...")
    
    if ext == '.txt':
        text = parse_txt(str(file_path))
    elif ext == '.epub':
        text = parse_epub(str(file_path))
    elif ext == '.pdf':
        text = parse_pdf(str(file_path))
    else:
        print(f"不支持的文件格式：{ext}")
        print("支持的格式：.txt, .epub, .pdf")
        return
    
    # 清理文本（可选）
    if args.clean:
        text = clean_text(text)
    
    # 输出
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    if args.extract_dialogues:
        # 提取对话模式
        print(f"正在提取对话及上下文（前后各{args.context_lines}行）...")
        dialogues = extract_dialogues_with_context(text, args.context_lines)
        formatted_text = format_dialogues_for_llm(dialogues, args.character)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)
        
        print(f"\n✅ 对话提取完成！")
        print(f"结果已写入：{args.output}")
        print(f"\n统计信息：")
        print(f"  - 提取对话组数：{len(dialogues)}")
        print(f"  - 上下文行数：前后各{args.context_lines}行")
        print(f"\n下一步：")
        print(f"  1. 让LLM读取 {args.output}")
        print(f"  2. LLM分析并识别目标角色「{args.character}」说的话")
        print(f"  3. LLM提取目标角色的对话及上下文用于蒸馏")
    else:
        # 原有的统计模式
        stats = extract_character_mentions(text, args.character)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"# 小说文本提取结果\n\n")
            f.write(f"## 统计信息\n\n")
            f.write(f"- 来源文件：{args.file}\n")
            f.write(f"- 角色名称：{args.character}\n")
            f.write(f"- 角色出现次数：{stats['total_mentions']}\n")
            f.write(f"- 总字数：{len(text)}\n")
            f.write(f"- 总行数：{len(text.split(chr(10)))}\n\n")
            f.write("---\n\n")
            f.write(text)
        
        print(f"\n✅ 预处理完成！")
        print(f"结果已写入：{args.output}")
        print(f"\n统计信息：")
        print(f"  - 角色 '{args.character}' 出现 {stats['total_mentions']} 次")
        print(f"  - 总字数：{len(text)}")

if __name__ == '__main__':
    main()
