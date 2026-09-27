"""Regenerate contests/2026-ossdevcon/SLIDES.md (talk script) from the speaker
notes in presentation/slides.md. Each note starts with "[N초 · criteria]" or
"[N분 · ...]"; slide time ranges are computed cumulatively from those."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "presentation/slides.md"
OUT = ROOT / "contests/2026-ossdevcon/SLIDES.md"

# Titles the extractor can't read cleanly (charts, code, lists)
TITLE_OVERRIDES = {
    4: "SQLAlchemy를 배웠고, Mike Bayer와 대화했고, SQLAlchemy Korea를 만들었습니다",
    6: "CUBRID는 공공 DBMS 2위였습니다 (점유율 차트)",
    11: "sqlalchemy-cubrid — 이렇게 씁니다 (코드)",
    14: "pycubrid — 문서 대신 두 드라이버의 소스를 나란히 놓고 읽었습니다",
    23: "2,200개의 테스트를 통과 못 하면, 머지되지 않습니다 (패키지별 차트)",
    24: "직접 쟀습니다 — 성능 비교 차트",
    27: "기본은 읽기 전용입니다",
    30: "MIT × 4 — 누구나 가져다 쓸 수 있게",
    32: "부풀리지 않은 숫자만 가져왔습니다 (PR · 릴리스 차트)",
}

CRITERIA = [
    "| 활용성 | 15 | 멈춰 있던 dialect 발견 (5) → 공공 2위·5년 상승 차트 (6) → 한 장 구조도 (9) → SQLAlchemy 코드 (11) → 2014년에 멈춘 드라이버 (12) → pip install (15) → cookbook (16) → AI 접근 (18–19) → PR·릴리스 차트 (32) |",
    "| OSS 적절성 | 15 | Mike Bayer의 README에 응답해 dialect 재작성·공식 test suite (5, 10) → 오픈소스 소스를 읽어 프로토콜 해독 (14) → 표준 위에 (29) |",
    "| PT | 10 | 표지 (1) · 장 제목 6개 · 전환 문장 (7, 13, 22) · 처음과 끝이 이어지는 구조 (3 ↔ 35) |",
    "| 데모 | 10 | 온나라 데모 ({demo}) → 반려의 원리 (27) — DEMO_RUNBOOK.md |",
    "| 기능테스트 | 10 | 매일 밤 실서버 golden test (17) → 2,200 테스트·패키지별 차트 (23) → 성능 비교 차트 (24) → 직접 확인 (31) |",
    "| 커뮤니티 | 5 | 컨트리뷰톤·SQLAlchemy Korea (3–4) → \"관심 있는 사람이 있다면\" → 이어받음 (5, 7) → AI+사람 리뷰 (21) → 다음 언어·good-first-issue (34) → 다음 사람에게 (35) |",
    "| 라이선스 | 5 | BSD 소스 참고 (14) → MIT × 4 · GPL 없음 · SBOM (30) |",
]


def clean(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()


def title_of(part):
    m = re.search(r'<div class="chapter"><span class="no">(\d+)</span><h1>(.*?)</h1>', part)
    if m:
        return f"〔{m.group(1)}〕 {clean(m.group(2))}", True
    for pat in (r"<h1>(.*?)</h1>", r"^## (.+)$", r"<h2>(.*?)</h2>"):
        m = re.search(pat, part, re.S | re.M)
        if m:
            return clean(m.group(1)), False
    return "?", False


def seconds(meta):
    m = re.match(r"(\d+)분", meta)
    return int(m.group(1)) * 60 if m else int(re.match(r"(\d+)초", meta).group(1))


def fmt(t):
    return f"{t // 60}:{t % 60:02d}"


def main():
    parts = re.split(r"\n---\n", SRC.read_text().split("\n---\n", 1)[1])
    t, rows, demo = 0, [], ""
    for i, part in enumerate(parts, 1):
        title, chapter = title_of(part)
        title = TITLE_OVERRIDES.get(i, title)
        note = (re.findall(r"<!--(.*?)-->", part, re.S) or [""])[0].strip()
        m = re.match(r"\[(.*?)\]\s*", note)
        meta, body = m.group(1), note[m.end():]
        start, t = t, t + seconds(meta)
        if "DEMO_RUNBOOK" in meta:
            demo = f"{i}, {fmt(start)}–{fmt(t)}"
        rows.append((i, title, chapter, f"{fmt(start)}–{fmt(t)} · {meta}", body))

    out = [
        "# 발표 대본 — 2026 오픈소스 개발자대회 본선", "",
        f"> 「공공 DBMS에 Python 문을 열다」 · {len(parts)}장 · 약 {fmt(t)} (12분 슬롯). 화면은 `presentation/slides.md`, 이 문서는 그 발표자 노트를 모은 대본입니다 (`scripts/build_talk_script.py`로 생성).",
        "> 심사 기준은 화면에 표시하지 않고 이야기 흐름 안에 녹였습니다. 각 장면이 채우는 기준은 대본 머리와 맨 끝 표에 적었습니다.",
        "> 숫자는 2026-09-12 스냅숏 기준이며 발표 당일 재측정합니다. 사진 두 장(`presentation/public/photos/team-2020.jpg`, `team-now.jpg`)은 받는 대로 넣습니다.", "",
    ]
    for i, title, chapter, meta, body in rows:
        out += [("## " if chapter else "### ") + f"{i}. {title}", "", f"`{meta}`", ""]
        out += ["> " + line for line in body.splitlines()] + [""]
    out += ["---", "", "## 심사 기준이 녹아든 곳", "",
            "| 기준 | 배점 | 이야기 속 장면 (슬라이드 번호) |", "|---|---|---|"]
    out += [row.format(demo=demo) for row in CRITERIA] + [""]
    OUT.write_text("\n".join(out))
    print(f"{len(parts)} slides, {fmt(t)}, demo at slide {demo}")


if __name__ == "__main__":
    main()
