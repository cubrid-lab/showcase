#!/usr/bin/env python3
"""Check that every Korean narration line in VIDEO_DESIGN.md fits its shot.

Reads the main-cut storyboard rows (``| <shot> | m:ss-m:ss | ...``) between the
``storyboard:main`` markers in VIDEO_DESIGN.md,
spells product names and acronyms the way the TTS voice reads them (LEXICON, which
is also the pronunciation list for synthesis), counts Korean syllables and compares
them with the shot length at the planning rate. It also checks that the shots are
contiguous and that the cut ends between 2:45 and 3:00.

    python3 demo-videos/intro-2026/narration_budget.py

Exit status 1 if a line is over budget, a Latin word has no reading, or the
timeline is broken. Standard library only.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOC = Path(__file__).with_name("VIDEO_DESIGN.md")
RATE = 4.5  # planned Korean syllables per second of shot, leaving room for music
MIN_TOTAL, MAX_TOTAL = 165, 180

# How the narrator says each Latin token. Longest keys are replaced first.
LEXICON = {
    "cubrid-cookbook-python": "큐브리드 쿡북 파이썬",
    "cubrid-mcp-server": "큐브리드 엠씨피 서버",
    "sqlalchemy-cubrid": "에스큐엘알케미 큐브리드",
    "cubrid-lab": "큐브리드 랩",
    "SQLAlchemy": "에스큐엘알케미",
    "pycubrid": "파이큐브리드",
    "asyncio": "에이싱크 아이오",
    "FastAPI": "패스트 에이피아이",
    "CUBRID": "큐브리드",
    "Python": "파이썬",
    "GitHub": "깃허브",
    "Alembic": "알렘빅",
    "Docker": "도커",
    "DB-API": "디비 에이피아이",
    "Django": "장고",
    "Flask": "플라스크",
    "Java": "자바",
    "Lab": "랩",
    "MCP": "엠씨피",
    "ORM": "오알엠",
    "MIT": "엠아이티",
    "TLS": "티엘에스",
    "LOB": "엘오비",
    "URL": "유알엘",
    "DDL": "디디엘",
    "SQL": "에스큐엘",
    "AI": "에이아이",
    "2.0": "이 점 영",
    "C": "씨",
}

ROW = re.compile(r"^\|\s*([A-Z]\d)\s*\|\s*(\d+):(\d\d)[–-](\d+):(\d\d)\s*\|")


def spoken(text: str) -> str:
    for key in sorted(LEXICON, key=len, reverse=True):
        text = re.sub(rf"(?<![A-Za-z0-9-]){re.escape(key)}(?![A-Za-z0-9-])", LEXICON[key], text)
    return text


def main() -> int:
    errors: list[str] = []
    rows = []
    doc = DOC.read_text(encoding="utf-8")
    section = doc.split("<!-- storyboard:main -->", 1)[-1].split("<!-- /storyboard:main -->", 1)[0]
    for line in section.splitlines():
        m = ROW.match(line)
        if not m:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        start = int(m[2]) * 60 + int(m[3])
        end = int(m[4]) * 60 + int(m[5])
        rows.append((m[1], start, end, cells[5]))  # column 6: Narration (KO)

    if not rows:
        print(f"no storyboard rows found in {DOC}", file=sys.stderr)
        return 1

    total_syl = 0
    prev_end = 0
    for shot, start, end, narration in rows:
        if start != prev_end:
            errors.append(f"{shot}: starts at {start}s, previous shot ends at {prev_end}s")
        prev_end = end
        text = "" if narration in {"—", "-", ""} else spoken(narration)
        leftover = re.findall(r"[A-Za-z]+", text)
        if leftover:
            errors.append(f"{shot}: no reading for {leftover}; add it to LEXICON")
        syl = len(re.findall(r"[가-힣]", text))
        total_syl += syl
        budget = (end - start) * RATE
        flag = "OVER" if syl > budget else "ok"
        if syl > budget:
            errors.append(f"{shot}: {syl} syllables > budget {budget:.0f}")
        print(f"{shot}  {end - start:>3}s  {syl:>3} syl  budget {budget:>4.0f}  {syl / (end - start):.2f}/s  {flag}")

    total = prev_end
    print(f"total {total // 60}:{total % 60:02d} ({total}s), {total_syl} syllables, "
          f"{total_syl / total:.2f} syl/s overall")
    if not MIN_TOTAL <= total <= MAX_TOTAL:
        errors.append(f"cut length {total}s outside {MIN_TOTAL}-{MAX_TOTAL}s")
    for e in errors:
        print(f"error: {e}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
