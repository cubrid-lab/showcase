"""Regenerate events/2026-ossdevcon/SLIDES.md (talk script) from the speaker
notes in presentation/decks/2026-ossdevcon/slides.md. Each note starts with "[N초 · criteria]" or
"[N분 · ...]"; slide time ranges are computed cumulatively from those."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "presentation/decks/2026-ossdevcon/slides.md"
OUT = ROOT / "events/2026-ossdevcon/SLIDES.md"

# Titles the extractor can't read cleanly (charts, code, lists)
TITLE_OVERRIDES = {
    9: "sqlalchemy-cubrid — 이렇게 씁니다 (코드)",
    17: "\"지워버리면요?\" 기본은 읽기 전용입니다",
    20: "CI를 통과해야 머지됩니다",
    24: "팀 밖의 62명이 보낸 PR 137개가 머지됐습니다",
    27: "Q&A — 질문에 맞는 근거로 이동합니다",
}

CRITERIA = [
    "| 활용성 | 15 | 멈춰 있던 dialect 발견 (5) → 연결 구조 (7) → SQLAlchemy 코드 (9) → 기존 드라이버의 걸림돌 (10) → pip install (12) → cookbook (13) → AI 접근 (15–17) → 외부 기여자 (24) |",
    "| OSS 적절성 | 15 | Mike Bayer의 README에 응답해 dialect 새 구현·호환성 테스트 (5, 8) → node-cubrid와 C 드라이버 소스 대조 (11) → 표준 (22) |",
    "| PT | 10 | 표지 (1) · 목차 (2) · 네 개 챕터 전환 (3, 6, 18, 23) · README 인용 (5)이 마지막 장 (26)의 답으로 이어지는 구조 |",
    "| 데모 | 10 | 라이브 데모 없음 — 실행해 본 코드 (9), 실제 문서·저장소·PR 화면 (13, 15, 19)으로 대신 |",
    "| 기능테스트 | 10 | 매일 실서버 예제 검증 (14) → 읽기 전용 설계 (17) → CI 게이트 (20) → 성능 비교 (21) |",
    "| 커뮤니티 | 5 | 컨트리뷰톤·SQLAlchemy Korea (4) → 이어받음 (5) → 에이전트와 사람의 역할 (19) → 외부 기여자 62명 (24) → 다음 계획 (25) → 마무리 (26) |",
    "| 라이선스 | 5 | 소스 참고 (11) → MIT × 4 · SBOM · 서드파티 라이선스 (22) |",
]


def clean(x):
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip()


def title_of(part):
    divider = re.search(r'<ChapterDivider\b[^>]*number="(\d+)"[^>]*title="([^"]+)"', part)
    if divider:
        return f"〔{divider.group(1)}〕 {divider.group(2)}", True
    m = re.search(r'<div class="chapter"><span class="no">(\d+)</span><h1>(.*?)</h1>', part)
    if m:
        return f"〔{m.group(1)}〕 {clean(m.group(2))}", True
    for pat in (r"<h1[^>]*>(.*?)</h1>", r"^## (.+)$", r"<h2[^>]*>(.*?)</h2>"):
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
    deck = json.loads((ROOT / "presentation/deck.json").read_text())
    snapshot = json.loads((ROOT / "presentation/snapshots" / f"{deck['snapshot']}.json").read_text())
    if snapshot["snapshotDate"] != deck["snapshot"]:
        raise ValueError("Snapshot date does not match presentation/deck.json")
    metrics = snapshot["metrics"]
    parts = re.split(r"\n---\n", SRC.read_text().split("\n---\n", 1)[1])
    main = next((i for i, p in enumerate(parts) if "발표 시간 외" in p), len(parts))
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
        "# 발표 대본 — 2026 오픈소스 개발자대회", "",
        f"> 「CUBRID, 이제 Python으로 — feat. CUBRID Python 생태계 구축기」 · 파이큐브리드팀 · 본 발표 {main}장 · 약 {fmt(t)} (12분 슬롯) · 뒤에 Q&A와 보조 자료 {len(parts) - main}장(발표 시간 외). 화면은 `presentation/decks/2026-ossdevcon/slides.md`, 이 문서는 그 발표자 노트를 모은 대본입니다 (`scripts/build_talk_script.py`로 생성).",
        "> 심사 기준은 화면에 표시하지 않고 이야기 흐름 안에 녹였습니다. 각 장면이 채우는 기준은 대본 머리와 맨 끝 표에 적었습니다.",
        f"> 채택 지표는 `presentation/deck.json`이 선택한 {snapshot['snapshotDate']} 스냅숏 기준입니다: GitHub stars {metrics['stars']['total']:,}개, merged PRs {metrics['mergedPRs']['total']:,}개, published GitHub Releases {metrics['publishedReleases']['total']:,}회입니다. fork와 clone traffic은 채택 지표에서 제외했습니다.",
        "> 사진 두 장(`presentation/public/photos/team-2020.jpg`, `team-now.jpg`)은 받는 대로 넣습니다.", "",
    ]
    for i, title, chapter, meta, body in rows:
        out += [("## " if chapter else "### ") + f"{i}. {title}", "", f"`{meta}`", ""]
        out += ["> " + line for line in body.splitlines()] + [""]
    out += ["---", "", "## 심사 기준이 녹아든 곳", "",
            "| 기준 | 배점 | 이야기 속 장면 (슬라이드 번호) |", "|---|---|---|"]
    out += [row.format(demo=demo) for row in CRITERIA] + [""]
    OUT.write_text("\n".join(out))
    print(f"{len(parts)} slides, {fmt(t)}")


if __name__ == "__main__":
    main()
