# 2026 오픈소스 개발자대회

## 출품작
pycubrid · sqlalchemy-cubrid · cubrid-cookbook-python · cubrid-mcp-server

## 일정
- 1차 서면: 통과 ✅
- 2차 발표: 2026 Q4 예정

## 이 폴더에 넣을 것
- [ ] SUBMISSION.md — 개발보고서 (1차 제출본)
- [ ] SLIDES.md — 발표 슬라이드 12장 (마크다운 → PPTX/Reveal.js 변환)
- [ ] DEMO_RUNBOOK.md — 데모 시나리오 + 리허설 체크리스트
- [ ] EXPECTED_QA.md — 예상 질문과 답변 (§4-4 참고)
- [ ] metrics/ — 발표용 지표 스냅샷 (측정일 기준)

## VHS Demo Scripts

Terminal demo GIFs are generated from VHS (.tape) scripts in each repo:

| Repo | Script | Renders |
|---|---|---|
| pycubrid | `demos/pycubrid-demo.tape` | `docs/demo.gif` |
| sqlalchemy-cubrid | `demos/orm-demo.tape` | `docs/demo.gif` |
| cubrid-mcp-server | `demos/mcp-demo.tape` | `docs/demo.gif` |
| cubrid-cookbook | `demos/agent-state.tape` | `docs/demo-agent-state.gif` |
| cubrid-cookbook | `demos/mcp-toolchain.tape` | `docs/demo-mcp-toolchain.gif` |

To render on desktop:
```bash
brew install vhs  # or: go install github.com/charmbracelet/vhs@latest
cd <repo>
vhs demos/<script>.tape
```
