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
├── contests/                      # 대회·공모전 (연도별)
│   ├── 2026-ossdevcon/           # 2026 오픈소스 개발자대회
│   │   ├── SUBMISSION.md          # 출품 신청서 (개발보고서)
│   │   ├── SLIDES.md              # 발표 슬라이드 (12장)
│   │   ├── DEMO_RUNBOOK.md        # 데모 시나리오 + 체크리스트
│   │   ├── EXPECTED_QA.md         # 예상 질문과 답변
│   │   └── metrics/               # 발표용 지표
│   └── archive/                   # 과거 대회 자료 (회고 포함)
├── programs/                      # 지원사업·그랜트 신청
│   ├── README.md                  # 신청 가능 프로그램 목록
│   └── templates/                 # 재사용 신청서·발표 템플릿
├── press-kit/                     # 로고·원페이저 (모든 신청에 재사용)
│   ├── ONE_PAGER.md               # 영문 한장 요약
│   └── ONE_PAGER.ko.md            # 국문 한장 요약
├── demo-videos/                   # 녹화 데모 (git-lfs 권장)
└── archive/                       # 레거시 자료
```

### 장기 운영 원칙
- **연도별 폴더**: 대회 종료 → `contests/archive/`로 이동 + 회고 작성
- **템플릿 재사용**: `programs/templates/`에 신청서 골격 유지 → 매년 숫자만 갱신
- **지표는 스냅샷**: `metrics/`에 측정일자와 함께 저장 → 추세 비교 가능
- **프레스 킷은 상시 갱신**: 로고·원페이저는 최신 상태 유지 → 어떤 신청에도 즉시 사용

## Our Story

We met at an OSS contribution hackathon as mentor and mentee, contributed to
SQLAlchemy and sqlalchemy-hana, then asked "why doesn't CUBRID have this?"
This project is the answer.

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
