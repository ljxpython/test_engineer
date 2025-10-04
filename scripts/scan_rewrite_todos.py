#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扫描 resume_template 下的 Markdown，自动生成“改写待办”清单：
- 规则：
  1) 命中“标准回答”关键字，或
  2) 同一小节内存在三引号代码围栏（```），且邻近出现“问题：”/“标准回答：”
- 过滤：若小节已存在“回答（口述版，STAR）”且无代码围栏，则视为已改写，跳过
- 输出：写入 resume_template/auto_rewrite_todo.md（覆盖写入）

使用：
  python scripts/scan_rewrite_todos.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "resume_template"
OUT = BASE / "auto_rewrite_todo.md"

# 忽略文件（避免自引用与非面试输出）
IGNORE_NAMES = {
    "auto_rewrite_todo.md",
    "interview_rewrite_tracker.md",
    "interview_flashcards.md",
    "metrics_glossary_and_sources.md",
}
# 忽略目录名（顶层或任意子路径名匹配即忽略）
IGNORE_DIRS = {
    "03-面试策略指南",
}
# 白名单目录（仅扫描这些目录）
ALLOW_DIRS = {
    "02-技术专题库",
    "04-题库与答案",
}

HEADING_RE = re.compile(r"^(#{2,3})\s+(.*)")
STD_ANSWER_RE = re.compile(r"标准回答")
STAR_ANSWER_RE = re.compile(r"回答（口述版")

# 简易优先级评估
def classify_priority(title: str) -> str:
    flames = title.count("🔥")
    stars = title.count("⭐")
    if flames >= 2 or stars >= 3:
        return "高"
    if flames >= 1 or stars >= 2:
        return "中"
    return "低"

QUESTION_RE = re.compile(r"问题：")
CODE_FENCE_RE = re.compile(r"^```")

MAX_CONTEXT = 30  # 同一小节内前后文窗口


def nearest_heading(lines, idx):
    """向上找到最近的二/三级标题。返回 1-based 行号、层级与标题。"""
    for i in range(idx, -1, -1):
        m = HEADING_RE.match(lines[i])
        if m:
            level = len(m.group(1))
            title = m.group(2).strip()
            return (i + 1, level, title)
    return (None, None, None)


def find_next_heading(lines, start_idx):
    """从 start_idx+1 向下找到下一个标题（任意层级）。返回 0-based 行号或 len(lines)。"""
    for j in range(start_idx + 1, len(lines)):
        if HEADING_RE.match(lines[j]):
            return j
    return len(lines)


def get_section_slice(lines, heading_line_1based):
    """基于标题行（1-based）返回该小节的文本切片与是否含代码围栏。"""
    if not heading_line_1based:
        return "", False
    h0 = heading_line_1based - 1
    end = find_next_heading(lines, h0)
    section_lines = lines[h0:end]
    section_text = "\n".join(section_lines)
    has_code_fence = any(CODE_FENCE_RE.match(ln) for ln in section_lines)
    return section_text, has_code_fence


def scan_file(path: Path):
    text = path.read_text(encoding="utf-8", errors="ignore")
    lines = text.splitlines()
    hits = []

    code_fence_lines = [i for i, ln in enumerate(lines) if CODE_FENCE_RE.match(ln)]
    std_answer_lines = [i for i, ln in enumerate(lines) if STD_ANSWER_RE.search(ln)]

    # 1) 直接命中“标准回答”
    for i in std_answer_lines:
        h_line, level, title = nearest_heading(lines, i)
        section_text, has_code = get_section_slice(lines, h_line)
        # 若已是口述版且无代码，则跳过（视为已改写）
        if STAR_ANSWER_RE.search(section_text) and not has_code:
            continue
        hits.append({
            "reason": "标准回答",
            "heading": title or "(未命名小节)",
            "line": h_line or (i + 1),
        })

    # 2) 存在代码围栏，且邻近出现“问题：/标准回答：”
    for i in code_fence_lines:
        start = max(0, i - MAX_CONTEXT)
        end = min(len(lines), i + MAX_CONTEXT)
        window = "\n".join(lines[start:end])
        # 收紧规则：同一窗口内必须同时出现“问题：”与“标准回答”才命中
        if QUESTION_RE.search(window) and STD_ANSWER_RE.search(window):
            h_line, level, title = nearest_heading(lines, i)
            section_text, has_code = get_section_slice(lines, h_line)
            # 若该小节已是口述版（存在“回答（口述版”），则跳过
            if STAR_ANSWER_RE.search(section_text):
                continue
            hits.append({
                "reason": "代码围栏+问答语义(双条件)",
                "heading": title or "(未命名小节)",
                "line": h_line or (i + 1),
            })

    # 去重（按 heading+line 聚合）
    uniq = {}
    for h in hits:
        key = (h["heading"], h["line"])
        if key not in uniq:
            uniq[key] = h
    hits = list(uniq.values())
    if not hits:
        return None

    # 构造 markdown 片段
    rel = path.relative_to(ROOT)
    lines_out = [f"- {rel}"]
    for h in sorted(hits, key=lambda x: x["line"]):
        prio = classify_priority(h['heading'] or '')
        lines_out.append(f"  - 小节：{h['heading']} (行 {h['line']}) | 原因：{h['reason']} | 优先级：{prio}")
    return "\n".join(lines_out)


def main():
    if not BASE.exists():
        print(f"目录不存在：{BASE}", file=sys.stderr)
        sys.exit(1)

    md_files = [
        p for p in BASE.rglob("*.md")
        if p.name not in IGNORE_NAMES
        and not any(part in IGNORE_DIRS for part in p.parts)
        and any(part in ALLOW_DIRS for part in p.parts)
    ]
    md_files.sort()

    sections = []
    for p in md_files:
        frag = scan_file(p)
        if frag:
            sections.append(frag)

    header = [
        "# 自动扫描改写待办",
        "",
        "> 说明：以下条目由脚本根据‘标准回答’关键字与‘代码围栏+问答语义’规则自动汇总，仅供参考。",
        "> 建议结合 interview_rewrite_tracker.md 的范围与排除规则人工复核。",
        "",
    ]

    content = "\n\n".join([*header, *sections]) if sections else "\n".join([*header, "(未发现疑似改写条目)"])
    OUT.write_text(content, encoding="utf-8")
    print(f"已生成：{OUT}")


if __name__ == "__main__":
    main()
