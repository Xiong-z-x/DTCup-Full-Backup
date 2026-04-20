from __future__ import annotations

import re
from html import escape
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_MD = ROOT / "大唐杯2026-Phase1-3备考总手册.md"
OUTPUT_PDF = ROOT / "大唐杯2026-Phase1-3备考总手册.pdf"

PHASE_FILES = [
    Path("Phase1-基础入门/Day1-通信发展史与5G场景.md"),
    Path("Phase1-基础入门/Day1-补充-大唐设备基础.md"),
    Path("Phase1-基础入门/Day2-5G网络架构.md"),
    Path("Phase1-基础入门/Day3-5G-NR帧结构.md"),
    Path("Phase1-基础入门/Day4-5G物理信道.md"),
    Path("Phase1-基础入门/Day5-5G信令流程.md"),
    Path("Phase1-基础入门/Day6-切换与网络规划.md"),
    Path("Phase1-基础入门/仿真操作指南.md"),
    Path("Phase2-强化提升/Day7-设备安装与参数规划.md"),
    Path("Phase2-强化提升/Day8-6G关键技术.md"),
    Path("Phase2-强化提升/Day8-补充-工程概论与项目管理.md"),
    Path("Phase2-强化提升/Day9-车联网与工业互联网.md"),
    Path("Phase2-强化提升/Day10-AI与5G节能.md"),
    Path("Phase2-强化提升/Day11-12-查缺补漏要点.md"),
    Path("Phase3-冲刺模拟/高频考点速查手册.md"),
    Path("Phase3-冲刺模拟/冲刺策略与得分技巧.md"),
]


def ordered_phase_files(root: Path = ROOT) -> list[Path]:
    return [root / rel_path for rel_path in PHASE_FILES]


def demote_headings(text: str) -> str:
    adjusted_lines = []
    for line in text.splitlines():
        if line.startswith("#"):
            adjusted_lines.append("#" + line)
        else:
            adjusted_lines.append(line)
    return "\n".join(adjusted_lines).strip()


def build_combined_markdown(root: Path = ROOT) -> str:
    lines = [
        "# 大唐杯2026 Phase1-3 备考总手册",
        "",
        "> 自动合并自 `dtcup-2026-prep/Phase1-基础入门`、`Phase2-强化提升`、`Phase3-冲刺模拟`。",
        "> 合并顺序按仓库 README 中的 Day 1-18 学习顺序排列。",
        "",
        "## 目录",
        "",
    ]

    for index, rel_path in enumerate(PHASE_FILES, start=1):
        label = rel_path.stem
        lines.append(f"{index}. {label}")

    for rel_path in PHASE_FILES:
        source_path = root / rel_path
        text = source_path.read_text(encoding="utf-8")
        lines.extend(
            [
                "",
                "\\newpage",
                "",
                f"<!-- SOURCE: {rel_path.as_posix()} -->",
                "",
                demote_headings(text),
                "",
            ]
        )

    return "\n".join(lines).rstrip() + "\n"


def strip_markdown_inline(text: str) -> str:
    text = re.sub(r"\[(.*?)\]\((.*?)\)", r"\1", text)
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = text.replace("~~", "")
    return text


def flush_paragraph(buffer: list[str], story: list[object], paragraph_style, spacer_cls) -> None:
    if not buffer:
        return
    text = strip_markdown_inline(" ".join(x.strip() for x in buffer if x.strip()))
    story.append(paragraph_style(text))
    story.append(spacer_cls)
    buffer.clear()


def render_pdf(markdown_text: str, output_path: Path) -> None:
    try:
        from reportlab.lib.enums import TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.pdfbase.pdfmetrics import registerFont
        from reportlab.platypus import PageBreak, Paragraph, Preformatted, SimpleDocTemplate, Spacer
    except ImportError as exc:
        raise SystemExit(
            "缺少 reportlab。请先执行 `python3 -m pip install --user reportlab` 再运行本脚本。"
        ) from exc

    registerFont(UnicodeCIDFont("STSong-Light"))
    styles = getSampleStyleSheet()
    base_font = "STSong-Light"
    normal_style = ParagraphStyle(
        "NormalCn",
        parent=styles["BodyText"],
        fontName=base_font,
        fontSize=10.5,
        leading=16,
        alignment=TA_LEFT,
        spaceAfter=4,
    )
    heading_styles = {
        1: ParagraphStyle("H1Cn", parent=styles["Heading1"], fontName=base_font, fontSize=20, leading=28, spaceAfter=10),
        2: ParagraphStyle("H2Cn", parent=styles["Heading2"], fontName=base_font, fontSize=16, leading=22, spaceAfter=8),
        3: ParagraphStyle("H3Cn", parent=styles["Heading3"], fontName=base_font, fontSize=13, leading=18, spaceAfter=6),
        4: ParagraphStyle("H4Cn", parent=styles["Heading4"], fontName=base_font, fontSize=11.5, leading=16, spaceAfter=6),
    }
    bullet_style = ParagraphStyle(
        "BulletCn",
        parent=normal_style,
        leftIndent=14,
        firstLineIndent=-10,
    )
    pre_style = ParagraphStyle(
        "PreCn",
        parent=normal_style,
        fontName=base_font,
        fontSize=9,
        leading=13,
        leftIndent=8,
    )

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=A4,
        leftMargin=16 * mm,
        rightMargin=16 * mm,
        topMargin=14 * mm,
        bottomMargin=14 * mm,
    )

    story: list[object] = []
    paragraph_buffer: list[str] = []
    table_buffer: list[str] = []
    code_buffer: list[str] = []
    in_code_block = False

    def add_paragraph(text: str, style: ParagraphStyle) -> None:
        story.append(Paragraph(escape(strip_markdown_inline(text)), style))
        story.append(Spacer(1, 3))

    def flush_table() -> None:
        nonlocal table_buffer
        if not table_buffer:
            return
        table_text = "\n".join(strip_markdown_inline(line) for line in table_buffer)
        story.append(Preformatted(table_text, pre_style))
        story.append(Spacer(1, 5))
        table_buffer = []

    def flush_code() -> None:
        nonlocal code_buffer
        if not code_buffer:
            return
        story.append(Preformatted("\n".join(code_buffer), pre_style))
        story.append(Spacer(1, 5))
        code_buffer = []

    for raw_line in markdown_text.splitlines():
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped == "```":
            flush_table()
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            in_code_block = not in_code_block
            if not in_code_block:
                flush_code()
            continue

        if in_code_block:
            code_buffer.append(line)
            continue

        if stripped == "\\newpage":
            flush_table()
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            story.append(PageBreak())
            continue

        if stripped.startswith("<!-- SOURCE:"):
            continue

        if not stripped:
            flush_table()
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            continue

        if stripped.startswith("|"):
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            table_buffer.append(line)
            continue

        flush_table()

        heading_match = re.match(r"^(#{1,6})\s+(.*)$", stripped)
        if heading_match:
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            level = min(len(heading_match.group(1)), 4)
            add_paragraph(heading_match.group(2), heading_styles[level])
            continue

        bullet_match = re.match(r"^(\d+\.)\s+(.*)$", stripped) or re.match(r"^[-*]\s+(.*)$", stripped)
        if bullet_match:
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            bullet_text = bullet_match.group(0)
            add_paragraph(bullet_text, bullet_style)
            continue

        if stripped.startswith(">"):
            flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
            add_paragraph(stripped.lstrip("> ").strip(), bullet_style)
            continue

        paragraph_buffer.append(stripped)

    flush_table()
    flush_paragraph(paragraph_buffer, story, lambda text: Paragraph(escape(text), normal_style), Spacer(1, 4))
    flush_code()
    doc.build(story)


def main() -> None:
    combined_markdown = build_combined_markdown(ROOT)
    OUTPUT_MD.write_text(combined_markdown, encoding="utf-8")
    render_pdf(combined_markdown, OUTPUT_PDF)
    print(f"Markdown: {OUTPUT_MD}")
    print(f"PDF: {OUTPUT_PDF}")


if __name__ == "__main__":
    main()
