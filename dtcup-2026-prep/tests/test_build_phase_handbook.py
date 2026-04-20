from __future__ import annotations

from pathlib import Path

from scripts.build_phase_handbook import PHASE_FILES, build_combined_markdown, ordered_phase_files


def test_ordered_phase_files_follow_readme_sequence() -> None:
    files = ordered_phase_files(Path("/tmp/repo"))
    assert files[0].as_posix().endswith("Phase1-基础入门/Day1-通信发展史与5G场景.md")
    assert files[1].as_posix().endswith("Phase1-基础入门/Day1-补充-大唐设备基础.md")
    assert files[8].as_posix().endswith("Phase2-强化提升/Day7-设备安装与参数规划.md")
    assert files[-2].as_posix().endswith("Phase3-冲刺模拟/高频考点速查手册.md")
    assert files[-1].as_posix().endswith("Phase3-冲刺模拟/冲刺策略与得分技巧.md")


def test_build_combined_markdown_contains_toc_and_page_breaks(tmp_path: Path) -> None:
    for rel_path in PHASE_FILES:
        target = tmp_path / rel_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(f"# {rel_path.stem}\n\n内容\n", encoding="utf-8")

    merged = build_combined_markdown(tmp_path)

    assert "# 大唐杯2026 Phase1-3 备考总手册" in merged
    assert "1. Day1-通信发展史与5G场景" in merged
    assert "16. 冲刺策略与得分技巧" in merged
    assert merged.count("\\newpage") == len(PHASE_FILES)
    assert "<!-- SOURCE: Phase1-基础入门/Day1-通信发展史与5G场景.md -->" in merged
