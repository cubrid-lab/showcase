# 기술 블로그 포스팅 초안

**제목**: "한국 공공시장 DBMS에 Python 문을 열다 — cubrid-lab 오픈소스 생태계 구축기"
**대상**: velog / OKKY / 테크블로그
**분량**: 약 2,000자 (5분 읽기)

---

## 한국 공공시장 DBMS에 Python 문을 열다

### 6년 전, 한 질문에서 시작했다

2020년, NIPA가 운영하는 오픈소스 컨트리뷰톤에서 두 사람이 만났다. 멘토와 멘티로. 그때 배운 것은 SQLAlchemy였고, 만난 사람은 Mike Bayer(SQLAlchemy 창시자)였다.

그러다 한 가지 사실을 발견했다: **CUBRID는 공공부문 DBMS 상위 5개 벤더 중 2위(2,367개 설치, 상위 5개 합계 대비 13.24%; 2025년 말, 행안부·NIA 보고서 표 46)인데, PyPI에 올라온 공식 Python 드라이버의 마지막 릴리스는 2014년 5월이었다.**

이후 버전(2025년 9월 v11.3.0.51까지)은 GitHub에서 받아 C 확장을 직접 빌드해야 했고, asyncio도 지원하지 않았다. `pip install`로 바로 쓸 수 있는 Python 드라이버가 없었던 셈이다.

### 무엇을 만들었나

4개의 패키지를 만들었다. 각 단계가 다음 단계를 자연스럽게 낳았다.

**① sqlalchemy-cubrid** (2021-22)

SQLAlchemy 창시자 Mike Bayer가 2012년에 만든 CUBRID dialect가 멈춰 있었다. 우리가 SQLAlchemy 2.0 기준으로 처음부터 재작성했다. schema reflection, MERGE, ON DUPLICATE KEY UPDATE, native ENUM 지원.

**② pycubrid** (2026)

dialect를 만들다 보니 드라이버가 문제였다. PyPI에는 2014년 이후 새 릴리스가 없는 C 확장. 그래서 순수 Python으로 새로 만들었다. CAS 바이너리 프로토콜 문서가 없어서 node-cubrid(BSD)와 공식 C 드라이버 소스를 교차 분석해 해독했다. 20개 패킷 타입, 30개 데이터 타입.

```bash
pip install pycubrid  # 한 줄, C 컴파일러 불필요, 의존성 0개
```

**③ cubrid-cookbook-python** (2026)

50여 개 예제와 7개 프로덕션 템플릿. 단순한 예제집이 아니라 **dogfooding 플랫폼**이다. 매일 밤 golden test가 실서버 CUBRID 11.4에서 예제를 실행한다(11.2는 주 1회). 드라이버에 버그가 있으면 cookbook이 가장 먼저 잡는다.

**④ cubrid-mcp-server** (2026)

AI 시대니까. **CUBRID MCP 서버**. 기본으로 읽기 도구 11개(쓰기 도구는 운영자가 켤 때만 추가), 읽기 전용 화이트리스트, AI 에이전트가 자연어로 CUBRID에 질의할 수 있다.

```bash
uvx cubrid-mcp-server
# Claude: "부처별 문서량 상위 5개 보여줘"
```

### 어떻게 품질을 보장하나

```
┌─────────────────────────────────────┐
│       Quality Gate System           │
├─────────────────────────────────────┤
│ Type Safety   mypy --strict, 0 err │
│ Coverage      ≥95% (CI 강제)        │
│ Lint/Format   ruff (CI 강제)       │
│ Property      hypothesis (난수)     │
│ API Compat    api-baseline.json    │
│ Golden Tests  예제 nightly (11.4)  │
│ SA Suite      공식 test suite      │
│ CI Matrix     Python 5 × CUBRID 4  │
└─────────────────────────────────────┘
```

2026-10-25 기준 병합된 PR 1,553개가 이 게이트를 통과했다.

### AI와 함께 일하는 방법

우리는 AI 에이전트가 코드를 작성하고 사람이 리뷰하는 워크플로우를 만들었다:

```
AGENTS.md (규칙) → AI 구현 → 사람 리뷰 → CI 게이트 → 사람 릴리스
```

드라이버와 dialect PR은 20조합 라이브 DB 테스트를 통과해야 병합된다.

### 숫자로 보는 성과

| 지표 | 값 |
|---|---|
| GitHub 스타 | 129 (4개 리포 합산) |
| 병합된 PR | 1,553개 |
| GitHub Releases | 61회 (패키지 3개 리포 합산) |
| 문서 사이트 | 4개 (한국어 문서 포함) |
| CI 조합 | Python 5 × CUBRID 4 = 20 |

※ 2026-10-25 스냅숏 기준입니다. GitHub 클론 수는 CI 러너 checkout이 대부분이라 채택 지표로 쓰지 않습니다.

### CUBRID는 니치 시장이다. 그래서 어떻게 하나

니치 시장에서는 사용자가 성능 문제를 알려주지 않는다. 그래서:

1. **직접 벤치마크한다** (cubrid-benchmark 저장서)
2. **직접 쓴다** (dogfooding, 매일 밤 실서버 검증)
3. **문서화한다** (4개 사이트, 한국어 문서 포함)
4. **AI-ready하게 만든다** (MCP + 도메인 지식 팩)

이게 니치 시장에서 OSS를 키우는 방법이라고 생각한다.

### 앞으로

TypeScript, Go, Rust 생태계도 진행 중이다. Python에서 검증한 플레이북을
동일하게 적용한다. **CUBRID 4개 언어 생태계**가 목표다.

---

**링크**
- GitHub: https://github.com/cubrid-lab
- Documentation: https://cubrid-lab.github.io/pycubrid/
- PyPI: https://pypi.org/project/pycubrid/
- MCP: https://pypi.org/project/cubrid-mcp-server/
- Benchmark: https://github.com/cubrid-lab/cubrid-benchmark
