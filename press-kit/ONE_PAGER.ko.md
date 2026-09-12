# CUBRID Python 생태계 — 원페이저

## Ecosystem Expansion (4 Languages)

| Language | Driver | ORM | Status |
|---|---|---|---|
| Python | pycubrid v1.7.0 | sqlalchemy-cubrid v1.7.0 | **Complete** |
| TypeScript | cubrid-client v1.1.0 | drizzle-cubrid v0.2.1 | In progress |
| Go | cubrid-go v0.2.1 | gorm-cubrid v0.1.0 | In progress |
| Rust | cubrid-rs v0.1.0 | sea-orm-cubrid v0.1.0 | In progress |

Community: SQLAlchemy Korea organizer (2020~) same playbook.

## 우리의 이야기

2020년 오픈소스 컨트리뷰톤(CNBT-41)에서 멘토-멘티로 만났습니다.
SQLAlchemy와 sqlalchemy-hana에 기여하며 방언 API를 배웠습니다.
SQLAlchemy 창시자 Mike Bayer가 2012년에 CUBRID 방언을 만들었지만 유지보수가 끊겼습니다.
해커톤에서 Mike를 만난 후, SQLAlchemy 2.0 기준으로 처음부터 다시 쓰고
드라이버도 순수 Python으로 새로 만들었습니다.

## 문제

한국 공공부문 DBMS 점유율 **10.6%가 CUBRID** (1,500+ 시스템, 2,300+ DB 인스턴스). 그런데 공식 Python 드라이버의 마지막 릴리스는 **2014년 5월** — asyncio 없음, SQLAlchemy 2.x 없음, 현대 Python 미지원. 수천 명의 개발자가 도구가 죽은 데이터베이스에 갇혀 있었습니다.

## 해결

4개 패키지, 순수 Python, `pip install` 한 줄로 끝.

```
pycubrid            드라이버 (DB-API 2.0, asyncio, TLS, 의존성 0)
sqlalchemy-cubrid   ORM (SQLAlchemy 2.0-2.2, Alembic, ENUM)
cubrid-cookbook     75개 예제 + 7개 템플릿 (FastAPI부터 AI 에이전트까지)
cubrid-mcp-server   AI/LLM 접근 (12개 도구, 읽기 전용 화이트리스트, 도메인 지식)
```

## 핵심 지표 (2026-09)

| | |
|---|---|
| GitHub 스타 | 111 |
| 유니크 클론 (14일) | 822명 |
| 병합된 PR | 450개 |
| PyPI 릴리스 | 35회 |
| 테스트 | 1,916개 (CI 강제) |
| CI 조합 | Python 5 × CUBRID 4 = 20개 |
| 문서 | 4개 사이트, 한국어 33페이지 |
| 라이선스 | MIT (4개 전부) |

**커뮤니티**: SQLAlchemy Korea 운영 (2020.10~, Gitter에서 Mike Bayer와 논의 후 개설)

## 성능 최적화 (벤치마킹 기반)

| 최적화 | 결과 |
|---|---|
| Native ping (CHECK_CAS) | SELECT 1 대비 **+280% 처리량** |
| SQLAlchemy pool_pre_ping | **+588% 처리량** |
| 대량 INSERT (1000행) | **12.3% faster** |
| 쿼리 select-all | **19.9% faster** |

벤치마크 저장소(cubrid-benchmark)에서 재현 가능한 비교 환경 제공.

## 차별점

1. **세계 유일**의 순수 Python CUBRID 드라이버 (C 확장 없음)
2. **세계 유일**의 CUBRID MCP 서버 (AI/LLM 접근)
3. **도메인 지식 내장** — MCP 서버가 LLM에게 CUBRID SQL 구문을 가르침
4. **450개 PR 검증** — AI 에이전트가 작성, 사람이 리뷰하는 워크플로우
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
