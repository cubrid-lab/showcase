# CUBRID Python 생태계 — 원페이저

## 우리의 이야기

2020년 오픈소스 컨트리뷰톤(CNBT-41)에서 멘토-멘티로 만났습니다.
SQLAlchemy와 sqlalchemy-hana에 기여하며 dialect API를 배웠습니다.
SQLAlchemy 창시자 Mike Bayer가 2012년에 CUBRID dialect를 만들었지만 유지보수가 끊겼습니다.
Gitter에서 Mike와 교류한 후, SQLAlchemy 2.0 기준으로 처음부터 다시 쓰고
드라이버도 순수 Python으로 새로 만들었습니다.

## 문제

CUBRID는 **공공부문 DBMS 상위 5개 벤더 중 2위 — 2,367개 설치, 상위 5개 합계 대비 13.24%** (2025년 말, [행안부·NIA 보고서 인쇄면 57쪽 표 46](https://www.data.go.kr/data/3038513/fileData.do)). 그런데 PyPI에 올라온 공식 Python 드라이버의 마지막 릴리스는 **2014년 5월**입니다. 이후 버전(2025년 9월 v11.3.0.51까지)은 GitHub에서 받아 C 확장을 직접 빌드해야 하고 asyncio를 지원하지 않습니다. 이 시스템들을 운영하는 팀에게는 `pip install`로 바로 쓸 수 있는 Python 드라이버가 없었습니다.

## 해결

4개 패키지, 순수 Python, `pip install` 한 줄로 끝.

```
pycubrid            드라이버 (DB-API 2.0, asyncio, TLS, 의존성 0)
sqlalchemy-cubrid   ORM (SQLAlchemy 2.0-2.2, Alembic, ENUM)
cubrid-cookbook     50여 개 예제 + 7개 템플릿 (FastAPI부터 AI 에이전트까지)
cubrid-mcp-server   AI/LLM 접근 (읽기 도구 11개, 쓰기 도구는 켤 때만, 도메인 지식)
```

## 핵심 지표 (2026-10-25 스냅숏)

| | |
|---|---|
| GitHub 스타 | 129 (4개 저장소) |
| 병합된 PR | 1,553개 |
| GitHub Releases | 61회 (패키지 3개 저장소) |
| CI 조합 | Python 5 × CUBRID 4 = 20개 |
| 문서 | 4개 사이트, 한국어 문서 포함 |
| 라이선스 | MIT (4개 전부) |

**커뮤니티**: SQLAlchemy Korea 운영 (2020.10~, Gitter에서 Mike Bayer와 논의 후 개설)

## 성능 최적화 (벤치마킹 기반)

| 최적화 | 결과 |
|---|---|
| Native ping (CHECK_CAS) | SELECT 1 대비 **+280% 처리량** |
| SQLAlchemy pool_pre_ping | **+588% 처리량** |
| 대량 INSERT (1000행) | **12.3% faster** |
| 쿼리 select-all | **19.9% faster** |

위 결과는 과거 측정값이며 재측정하지 않았고, 측정 날짜와 버전은 기록되지 않았습니다.
2026-10-28에 같은 CUBRID 11.4.6 서버에서 공식 C 드라이버 `CUBRIDdb`와 다시 잰 결과, pycubrid 1.15.0은
PK 조회에 1.04배, 1만 행 조회에 1.17배의 시간이 걸렸습니다([측정 환경과 원본 결과](../../../events/2026-ossdevcon/metrics/benchmark-2026-10-28/README.md)).

벤치마크 저장소(cubrid-benchmark)에서 재현 가능한 비교 환경 제공.

## 생태계 확장 (4개 언어)

| 언어 | 드라이버 | ORM | 상태 |
|---|---|---|---|
| Python | pycubrid | sqlalchemy-cubrid | **완성** |
| TypeScript | cubrid-client | drizzle-cubrid | 진행 중 |
| Go | cubrid-go | gorm-cubrid | 진행 중 |
| Rust | cubrid-rs | sea-orm-cubrid | 진행 중 |

최신 버전은 각 저장소의 릴리스 페이지에서 확인합니다.

커뮤니티: SQLAlchemy Korea 운영 경험(2020~)으로, 언어마다 같은 순서(드라이버 → ORM → 예제 → AI)를 적용합니다.

## 차별점

1. **순수 Python** CUBRID 드라이버 (C 확장 없음, `pip install`)
2. **CUBRID MCP 서버** (AI/LLM 접근, 기본 읽기 전용)
3. **도메인 지식 내장** — MCP 서버가 LLM에게 CUBRID SQL 구문을 가르침
4. **병합된 PR 1,553개** (2026-10-25) — AI 에이전트가 작성하고 사람이 리뷰, CI 게이트를 통과
5. **프로덕션 준비 완료** — 7개 실행 가능한 템플릿, 골든 검증 예제

## 링크

| | |
|---|---|
| 드라이버 | github.com/cubrid-lab/pycubrid |
| ORM | github.com/cubrid-lab/sqlalchemy-cubrid |
| 예제 | github.com/cubrid-lab/cubrid-cookbook-python |
| AI/MCP | github.com/cubrid-lab/cubrid-mcp-server |
| 문서 | cubrid-lab.github.io/{pycubrid, sqlalchemy-cubrid, cubrid-mcp-server, cubrid-cookbook-python} |

**팀**: 최영선 & 백경준 (CUBRID Lab)
