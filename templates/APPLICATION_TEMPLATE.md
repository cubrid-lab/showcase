# [프로그램명] 신청서

> 이 템플릿을 복사해 매년/매 프로그램마다 숫자만 갱신하세요.
> 마지막 갱신: 2026-09-12

## 프로젝트 개요

| 항목 | 내용 |
|---|---|
| 프로젝트명 | CUBRID Python Ecosystem |
| 조직 | [cubrid-lab](https://github.com/cubrid-lab) |
| 구성원 | Yeongseon Choe, Gyeongjun Paik |
| 저장소 | 4개 (pycubrid · sqlalchemy-cubrid · cubrid-cookbook-python · cubrid-mcp-server) |
| 라이선스 | MIT ×4 |
| 언어 | Python (순수, C 확장 없음) |

## 핵심 성과 (매번 갱신)

| 지표 | 2026-09 기준 | 측정 방법 |
|---|---|---|
| GitHub 스타 | 87 (4개 리포 합산) | `gh repo view` |
| 유니크 클론 (14일) | 647명 | GitHub Traffic API |
| 병합된 PR | 432개 | `gh pr list --state merged` |
| PyPI 릴리스 | 35회 | PyPI API |
| CI 통합테스트 | 20 조합 (Python×CUBRID) | 워크플로 설정 |
| 문서 사이트 | 4개 (전부 라이브) | HTTP 200 확인 |
| 한국어 문서 | 33페이지 | mkdocs nav |

## 문제 정의

한국 공공부문 DBMS 점유율 10.6%가 CUBRID (행안부 2025 EA보고서).
그런데 공식 Python 드라이버는 2014년 5월 이후 12년간 방치.
국방·행안부·지자체 개발자가 Python으로 CUBRID에 접근할 방법이 없었음.

## 솔루션

```
pycubrid (드라이버) → sqlalchemy-cubrid (ORM) → cookbook (예제) → mcp-server (AI)
```

4계층으로 구성된 순수 Python 생태계. `pip install pycubrid` 한 줄로 해결.

## 차별성

1. **세계 유일**의 순수 Python CUBRID 드라이버 (C 확장 없음)
2. **세계 유일**의 CUBRID MCP 서버 (AI/LLM 접근)
3. SQLAlchemy 2.0–2.1 지원 (공식 드라이버는 미지원)
4. asyncio 네이티브 지원 (공식 드라이버는 미지원)
5. 20조합 (Python 5 × CUBRID 4) 통합테스트 CI
