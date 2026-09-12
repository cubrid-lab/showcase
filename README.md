# CUBRID Python Ecosystem — Showcase

Contest entries, presentations, demo materials, and promotional content
for the cubrid-lab Python ecosystem (pycubrid · sqlalchemy-cubrid ·
cubrid-cookbook-python · cubrid-mcp-server).

## Why This Repo Exists

Code repositories stay code-focused. This is where we put everything
that **shows** the work — slides, demo runbooks, metrics, contest
submissions, and brand assets. Judges, reviewers, and the curious
should be able to understand the full story from here without reading
source code.

## Structure

```
showcase/
├── README.md                     # You are here
├── contests/
│   └── 2026-ossdevcon/          # 2026 오픈소스 개발자대회
│       ├── SUBMISSION.md         # 출품 신청서 (개발보고서)
│       ├── SLIDES.md             # 발표 슬라이드 (12장)
│       ├── DEMO_RUNBOOK.md       # 데모 시나리오 + 리허설 체크리스트
│       ├── EXPECTED_QA.md        # 예상 질문과 답변
│       └── metrics/              # 발표용 지표 스냅샷
├── press-kit/
│   ├── LOGO.md                   # 로고·배지·스크린샷 모음
│   ├── ONE_PAGER.md              # 한장 요약 (영문)
│   └── ONE_PAGER.ko.md           # 한장 요약 (국문)
├── demo-videos/                   # 녹화 데모 (git-lfs 권장)
│   └── README.md                 # 비디오 목록과 링크
└── archive/                       # 과거 대회·발표 자료
```

## 2026 오픈소스 개발자대회

| 항목 | 상태 |
|---|---|
| 출품작 | pycubrid · sqlalchemy-cubrid · cubrid-cookbook-python · cubrid-mcp-server |
| 조직 | [cubrid-lab](https://github.com/cubrid-lab) |
| 일정 | 1차 서면 통과 → 2차 발표 (2026 Q4) |
| 배점 | 활용성 15 · OSS적절성 15 · PT 10 · 데모 10 · 기능테스트 10 · 커뮤니티 5 · 라이선스 5 |

### 핵심 스토리

> **한국 공공부문 DBMS 10.6%가 CUBRID인데, Python 드라이버는 2014년에 죽었습니다.**
> **국방·행안부·지자체에서 일하는 수천 명의 개발자가 갇혀 있었습니다.**
> **우리는 더 나은 DB를 만든 게 아닙니다. 갇힌 개발자들을 꺼내줬습니다.**

### 생태계 지표 (2026-09-12 기준)

| 지표 | 값 |
|---|---|
| GitHub 클론 유니크 (14일) | 647명 |
| 병합된 PR | 432개 |
| PyPI 릴리스 | 35회 (v1.7.0) |
| 문서 사이트 | 4/4 라이브 |
| CI 통합테스트 | Python 5 × CUBRID 4 = 20 조합 |
| 한국어 문서 | 33페이지 |

## Related

- [pycubrid](https://github.com/cubrid-lab/pycubrid) — Pure Python DB-API 2.0 driver
- [sqlalchemy-cubrid](https://github.com/cubrid-lab/sqlalchemy-cubrid) — SQLAlchemy 2.0–2.1 dialect
- [cubrid-cookbook-python](https://github.com/cubrid-lab/cubrid-cookbook-python) — 68 examples + 7 templates
- [cubrid-mcp-server](https://github.com/cubrid-lab/cubrid-mcp-server) — MCP server for AI/LLM

## License

Content in this repository is MIT licensed (same as the code projects).
