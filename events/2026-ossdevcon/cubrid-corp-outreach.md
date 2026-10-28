# CUBRID Corp 등재 문의 이메일

**To:** CUBRID Corporation (담당자: 개발자 관계팀 or 오픈소스 담당)
**Subject:** [제안] CUBRID Python 생태계 오픈소스 프로젝트 — 도구 목록 등재 및 협업 제안

---

안녕하십니까.

저희는 cubrid-lab이라는 오픈소스 그룹에서 CUBRID의 Python 생태계를 구축한
최영선, 백경준입니다.

## 소개

2020년 NIPA 오픈소스 컨트리뷰톤에서 멘토-멘티로 만나 SQLAlchemy와
sqlalchemy-hana에 기여하면서 데이터베이스 dialect 개발을 시작했습니다.
그 경험을 바탕으로 CUBRID의 Python 생태계를 구축했습니다.

## 구축한 생태계 (4개 패키지)

| 패키지 | 설명 | PyPI |
|---|---|---|
| pycubrid | 순수 Python DB-API 2.0 드라이버 (asyncio, TLS) | 공개 |
| sqlalchemy-cubrid | SQLAlchemy 2.0 dialect (ORM, Alembic, ENUM) | 공개 |
| cubrid-cookbook-python | 50여 개 예제 + 7 템플릿 (FastAPI~AI Agent) | — |
| cubrid-mcp-server | **CUBRID MCP 서버** (AI/LLM 접근, 기본 읽기 전용) | 공개 |

## 요청 사항

1. **cubrid.org 도구 목록 등재**: 기존 드라이버 목록에 pycubrid와
   sqlalchemy-cubrid를 추가해 주시면 감사하겠습니다.
   - https://www.cubrid.org/manual/en/11.0/api.html 맥락에서

2. **기술 블로그 게스트 포스팅**: CUBRID Python 생태계 구축 경험을
   CUBRID 블로그에 공유하고 싶습니다.

3. **피드백**: 실제 CUBRID 사용 사례에서 우리 드라이버가 활용될 수
   있는지, 개선이 필요한 부분이 있는지 의견을 듣고 싶습니다.

## 참고 자료

- GitHub: https://github.com/cubrid-lab
- Documentation: https://cubrid-lab.github.io/pycubrid/
- PyPI: https://pypi.org/project/pycubrid/
- MCP Server: https://pypi.org/project/cubrid-mcp-server/
- CI: Python 5 × CUBRID 4 = 20개 조합 라이브 DB 테스트
- 오픈소스 개발자대회 출품작 (2026, 1차 통과)

## 왜 중요한가

CUBRID 공식 Python 드라이버는 2014년 이후 PyPI에 새 릴리스가 없고, 이후 버전은
GitHub에서 받아 C 확장을 직접 빌드해야 해서 Python 개발자들이 CUBRID를 쓰기 어려웠습니다. 저희 생태계는:

- `pip install pycubrid` 한 줄로 설치 (C 컴파일러 불필요)
- asyncio 네이티브 지원 (공식 드라이버 미지원)
- Python 3.10~3.14 지원
- MCP를 통한 AI/LLM 접근 (기본 읽기 전용)
- CI에서 커버리지 95% 하한과 20개 조합 라이브 DB 테스트로 검증

이것이 공공부문 CUBRID 사용자(2,367개 설치, 2025년 말 행안부·NIA 보고서 표 46)에게 Python + AI 접근 경로를
열어줄 것이라 믿습니다.

감사합니다.

최영선 드림
yeongseon.choe@gmail.com
https://github.com/yeongseon

백경준 드림
https://github.com/paikend

---

cubrid-lab: https://github.com/cubrid-lab
