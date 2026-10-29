# CUBRID Kubernetes Operator — 빌더 시즌4 1차 검증

아이디어와 프로젝트 방향성을 설명하는 한국어·영어 **각 15장** 발표자료입니다.
2026-10-20 시험 결과를 기준으로 운영 사례와 v0.1 이후 계획을 담았습니다. 2026-10-22에 장애 시나리오, 사용자, 기존 대안, 안전성, 시험 근거를 추가해 발표 흐름을 확장했고, 2026-10-26에는 10월 25일 VM 백업 복원 결과를 더했습니다. 2026-10-27에 장마다 겹치는 문장을 덜어내고 마지막에 질의응답 장을 붙였습니다. 2026-10-28에는 처음 보는 청중이 서비스를 먼저 이해하도록 순서를 바꿨습니다: 무엇인가 → 왜 필요한가 → 구성도 → 장애 흐름 → 공식 Operator와 차이 → 근거 → 계획(#75). 2026-10-29에는 발표 순서 장을 넣고, 프로젝트 목표와 공식 Operator 비교표를 정리했습니다(#108). 같은 날 의견 요청 장을 빼고, 그 질문은 질의응답 장에서 말로 전합니다. 이어서 공지의 여섯 항목 순서로 장을 다시 배치하고, 아키텍처 초안에 제어 루프와 데이터 처리 과정 장을 더했습니다.
프로그램 공식 명칭은 확인 전이며, 폴더명은 전달받은 “시즌4 빌더” 공지를
기준으로 정했습니다.

## 발표자료 바로 열기

| 언어 | 최신 HTML (`main` 기준) | 제출용 PDF (16장) | 제출용 PPTX (16장) | 같은 버전 HTML ZIP |
|---|---|---|---|---|
| 한국어 | [한국어 HTML 발표](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/ko/) | [한국어 PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-29-r6/operator-first-validation.ko.pdf) | [한국어 PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-29-r6/operator-first-validation.ko.pptx) | [한국어 HTML ZIP](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-29-r6/operator-first-validation.ko-html.zip) |
| English | [English HTML presentation](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/en/) | [English PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-29-r6/operator-first-validation.en.pdf) | [English PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-29-r6/operator-first-validation.en.pptx) | [English HTML ZIP](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-29-r6/operator-first-validation.en-html.zip) |

PDF·PPTX는 [2026-10-29 제출본 릴리스](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r6)의 파일이며,
원본 커밋 `25b8961`에서 출력한 16장 제출본(r6, 공지 여섯 항목 순서)입니다. 직전 15장 제출본은 [r5 릴리스](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r5), 16장 제출본은 [r4 릴리스](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r4), 그 이전 15장 제출본은 [r3 릴리스](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-28-r3)에 보존합니다. 이전 18장 제출본은 [2026-10-28 릴리스](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-28)에 그대로 보존합니다. 디스코드에는 이 릴리스의 PPTX 두 개를 제출합니다.
HTML 발표는 `main`이 바뀔 때마다 다시 만들어지므로 이 고정본보다 새로울 수 있습니다.
HTML ZIP은 같은 커밋으로 만든 HTML이며, 압축을 풀고 `python3 -m http.server`로 열어 봅니다.
각 언어 16장입니다. Markdown 원본과 출력 검증 기록은 아래에서 확인할 수 있습니다.
[시즌4 전체 발표 목록](../README.md)

## 일정과 제출 요건

출처: 팀원이 전달한 「[빌더 공지] 10/31(토) 오전 10시 1차 검증 자료 제출 안내」.
연도는 이번 발표 준비 맥락에 따라 2026년으로 기록했고, 시간은 한국 시간(KST)입니다.

| 항목 | 내용 |
|---|---|
| 발표 | 2026-10-31(토) 오전 10시 |
| 장소 | 디캠프 선릉 6층 |
| 진행 | 팀별 발표 10분 + 질의응답 10분 |
| 발표 언어 | 한국어 |
| 제출물 | 한국어 PPTX 1개 + 영어 PPTX 1개 |
| 제출 기한 | 2026-10-29(목) 23:59 KST |
| 제출 위치 | 팀 디스코드 채널에 각각 제출 |
| 발표 순서 | 제출 시간 역순: 늦게 제출한 팀부터 진행 |
| 검증 목적 | 아이디어와 프로젝트 방향성 검증. 특별한 데모는 필요하지 않음 |

## 자료

| 파일 | 용도 | 준비 상태 |
|---|---|---|
| [slides.ko.md](../../../presentation/decks/2026-builder-season4/01-validation/slides.ko.md) | 한국어 웹 발표 원본과 발표자 메모 | 16장 · 560초 시간 배분 · 발표자 메모 포함 |
| [slides.en.md](../../../presentation/decks/2026-builder-season4/01-validation/slides.en.md) | 영어 웹 발표 원본과 발표자 메모 | 16장 · 560초 시간 배분 · 발표자 메모 포함 |
| [한국어 진입 파일](../../../presentation/2026-builder-season4-01-validation.ko.md) | 공통 테마·웹·출력 설정 | 원본을 불러오는 Slidev 설정 |
| [영어 진입 파일](../../../presentation/2026-builder-season4-01-validation.en.md) | 공통 테마·웹·출력 설정 | 원본을 불러오는 Slidev 설정 |
| [SOURCES.md](SOURCES.md) | 고정된 근거·주장 경계·필수 항목 대응 | 10-20 고정 실행 근거 · 10-22 설명 확장 · 10-25 복원 근거 추가 |
| `operator-first-validation.ko.pptx` / `.pdf` | 한국어 발표·제출용 출력물 | [16장 제출본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r6) · [출력·검수 기록](DELIVERY.md) |
| `operator-first-validation.en.pptx` / `.pdf` | 영어 발표·제출용 출력물 | [16장 제출본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r6) · [출력·검수 기록](DELIVERY.md) |

- [한국어 발표자 대본](SPEAKER_NOTES.ko.md): 슬라이드별 전환과 시간 배분
- [질의응답 준비](EXPECTED_QA.ko.md): 질문별 30–60초 답변과 근거
- [출력·검수 기록](DELIVERY.md): 원본 커밋, 파일, 형식·시각 확인 결과

## 웹 원본에서 발표와 내보내기

웹 기반 Slidev 발표를 원본으로 작성한 뒤 **같은 원본에서 PPTX와 PDF를 생성**합니다.
PPTX나 PDF를 직접 수정해 원본과 별도로 관리하지 않습니다.

저장소 루트에서 시작합니다.

```bash
cd presentation
npm ci
npm run dev:operator:ko       # 한국어 웹 발표 미리보기
npm run dev:operator:en       # 영어 웹 발표 미리보기
npm run build:operator       # 한영 정적 웹 빌드

# CLI 출력에 필요한 Slidev 선택적 브라우저 도구 (manifest/lockfile 변경 없음)
npm install --no-save playwright-chromium
npm run export:operator:pptx  # 한영 PPTX 각각 생성
npm run export:operator:pdf   # 한영 PDF 각각 생성
```

출력 파일은 `presentation/exports/`에 언어별로 생성되며 Git에서는 제외합니다. CI는 PR과 `main`마다 한영 PDF·PPTX를 출력해 장수·메모 수를 검사합니다.
정적 웹 빌드 경로, 브라우저 준비, 호스팅 경로 설정은
[공통 도구 안내](../../../presentation/README.md#operator-web--pdf--pptx)를 참조합니다.
최종 파일은 행사별 릴리스 첨부물로 보존하고 원본 커밋을 기록합니다.
디스코드 제출은 별도로 진행하며 이번 공지의 필수 제출물은 한영 PPTX 2개입니다.

기본 PPTX는 슬라이드를 이미지로 담으므로 웹 화면을 보존하지만 텍스트를 직접
편집할 수 없습니다. 웹 애니메이션과 상호작용은 정적으로 출력됩니다.
편집 가능한 PPTX가 필요하면 Slidev의 `pptx-editable` 출력과 별도 레이아웃 검토를
사용합니다. 두 PPTX에는 슬라이드별 발표자 메모가 포함됩니다.
실제 발표 리허설, PowerPoint에서의 최종 열기, 디스코드 제출은 자동 출력 검수와 별개입니다.

## 발표 시간 배분

| 공지 항목 | 슬라이드 | 핵심 설명 | 발표 시간 |
|---|---|---|---|
| 1. 프로젝트·팀 소개 | 1–3 | 표지의 팀 소개, 발표 순서, 프로젝트가 이루려는 네 가지 목표 | 80초 |
| 2. 해결하려는 문제·대상 | 4 | Pod 복구와 DB 서비스 복구의 차이, 두 담당자(사용자 가설) | 40초 |
| 3. 현재 해결 방식·기존 오픈소스 한계 | 5 | 공식 CUBRID Operator와 다른 점(비교표·공식 저장소 링크) | 50초 |
| 4. 제안하는 해결 방법 | 6–8 | 장애 뒤 네 가지 확인, master 미확정 원칙, 지금까지 확인한 결과 | 120초 |
| 5. 아키텍처 초안 | 9–10 | 연동 플랫폼·구성 요소 구성도, 제어 루프와 SQL·백업·상태 데이터 처리 과정 | 90초 |
| 6. 12주 로드맵·팀원별 역할·첫 버전 범위 | 11–15 | 12주 계획, 역할과 교차 검증, v0.1 필수 시험과 범위, 이후 방향 | 165초 |
| 7. 함께 논의할 내용 · 질의응답 | 16 | 감사 인사, 질문 받기, 장애 확인 경험과 첫 CSI 드라이버 의견 요청(발표자 메모) | 15초 |
| **합계** | **한국어·영어 각 16장** | **목표: 9분 20초 + 여유 40초** | **560초** |

발표는 10분, 질의응답은 별도 10분입니다. 상세 설명과 예외는 슬라이드의
발표자 메모·[한국어 대본](SPEAKER_NOTES.ko.md)·[Q&A 준비](EXPECTED_QA.ko.md)에 보존합니다.
시간은 예상 배분이며 실측 리허설 결과가 아닙니다.

## 작성 원칙과 근거

- 구현 사실과 검증 증거는 [Operator 저장소](https://github.com/cubrid-lab/cubrid-kubernetes-operator)를 기준으로 확인합니다.
- 아키텍처는 [DESIGN.md](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/DESIGN.md),
  구현·검증 상태는 [ROADMAP.md](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md),
  안전 제약은 [ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/main/docs/adr)을 확인한 후 요약합니다.
- 발표에 사용하는 근거의 커밋과 확인일을 기록합니다. 계획, 구현, 단위/envtest 결과,
  실제 환경 검증을 구분하고 Python 생태계의 대회 지표를 Operator 성과로 사용하지 않습니다.
- 12주 계획과 첫 공개 버전의 필수·조건부·제외 범위는 고정된 ROADMAP을 근거로 작성했습니다.
- 팀원 실명과 공동 메인테이너 역할은 저장소·프로필·기존 소개 자료로 확인했습니다. 담당자가 재현·구현·테스트·문서·근거를 준비하고 다른 메인테이너가 리뷰하는 책임 구조를 설명합니다. 확정되지 않은 개인별 기능 배정은 만들지 않습니다.
- v0.1 이후의 운영화·지원 환경 확대·장기 과제는 방향안입니다. 후속 날짜나 지원을 확약하거나 v0.1 필수 안전 조건을 미루지 않습니다.
- 모든 주장과 아직 충족하지 않은 제출 항목은 [SOURCES.md](SOURCES.md)에 기록했습니다.
- 한영 자료는 같은 슬라이드 번호, 범위, 수치, 증거를 사용합니다.

## 자료 작성과 제출 확인

자료 작성·자동 검수 결과는 [DELIVERY.md](DELIVERY.md)에 기록합니다.
아래의 실제 리허설·제출 항목은 실행한 것으로 표시하지 않았습니다.

- [x] 공지의 필수 항목을 공지 순서대로 한국어·영어 각 16장에 포함(7번은 질의응답 장의 발표자 메모)
- [x] 팀원 실명과 공동 메인테이너 역할 반영
- [x] 11월 29일 필수 시나리오·12월 27일 공개 **목표**와 첫 버전 범위 명시
- [x] 2026-10-20 근거 커밋·Kind/VM 결과·남은 검증 구분
- [x] 두 언어의 발표자 메모, 한국어 대본과 Q&A 준비
- [x] **16장 r6**(#113, 공지 여섯 항목 순서·아키텍처 흐름 장 추가) PPTX/PDF/HTML 재생성·장 수 확인: [16장 제출본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r6)
- [x] 이전 **15장 r5**(#111, 의견 요청 장 제거) PPTX/PDF/HTML 재생성·장 수 확인: [15장 제출본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r5)
- [x] 이전 **16장 개정판**(#108) PPTX/PDF/HTML 재생성·장 수/메모/레이아웃 확인: [16장 제출본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-29-r4)
- [x] 이전 **15장 개정판**(#75) PPTX/PDF/HTML 재생성·장 수/메모/레이아웃 확인: [15장 제출본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-28-r3)
- [x] 이전 **18장** 출력 보존: [2026-10-28 릴리스](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-28)
- [x] 10월 21일 **이전 11장 버전** 출력 검수 기록 보존: [DELIVERY 기록](DELIVERY.md)
- [ ] 공식 프로그램명 최종 확인: 공지의 “빌더 시즌4” 표기 사용
- [ ] 한국어 발표 실제 리허설 10분 이내
- [ ] PPTX 두 파일을 실제 PowerPoint에서 열어 최종 확인
- [ ] 10월 29일 23:59 KST까지 팀 디스코드 채널에 각각 제출
- [ ] 제출 시각과 제출 메시지 링크 기록
