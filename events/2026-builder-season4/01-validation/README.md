# CUBRID Kubernetes Operator — 빌더 시즌4 1차 검증

아이디어와 프로젝트 방향성을 설명하는 한국어·영어 **각 18장** 발표자료입니다.
2026-10-20 시험 결과를 기준으로 운영 사례와 v0.1 이후 계획을 담았습니다. 2026-10-22에 장애 시나리오, 사용자, 기존 대안, 안전성, 시험 근거를 추가해 발표 흐름을 확장했고, 2026-10-26에는 10월 25일 VM 백업 복원 결과를 12–13장에 더했습니다.
프로그램 공식 명칭은 확인 전이며, 폴더명은 전달받은 “시즌4 빌더” 공지를
기준으로 정했습니다.

## 발표자료 바로 열기

- [한국어 HTML 발표](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/ko/)
- [English HTML presentation](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/en/)
- [시즌4 전체 발표 목록](../README.md)

브라우저에서 바로 넘겨 볼 수 있는 HTML 발표입니다. 현재 내용은
한국어·영어 각 18장입니다. Markdown 원본과 출력 검증 기록은 아래에서 확인할 수 있습니다.

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
| [SLIDES.ko.md](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.ko.md) | 한국어 웹 발표 원본과 발표자 메모 | 18장 · 580초 시간 배분 · 발표자 메모 포함 |
| [SLIDES.en.md](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.en.md) | 영어 웹 발표 원본과 발표자 메모 | 18장 · 580초 시간 배분 · 발표자 메모 포함 |
| [한국어 진입 파일](../../../presentation/operator-first-validation.ko.md) | 공통 테마·웹·출력 설정 | 원본을 불러오는 Slidev 설정 |
| [영어 진입 파일](../../../presentation/operator-first-validation.en.md) | 공통 테마·웹·출력 설정 | 원본을 불러오는 Slidev 설정 |
| [SOURCES.md](SOURCES.md) | 고정된 근거·주장 경계·필수 항목 대응 | 10-20 고정 실행 근거 · 10-22 설명 확장 · 10-25 복원 근거 추가 |
| `operator-first-validation.ko.pptx` / `.pdf` | 한국어 발표·제출용 출력물 | [출력·검수 기록](DELIVERY.md) |
| `operator-first-validation.en.pptx` / `.pdf` | 영어 발표·제출용 출력물 | [출력·검수 기록](DELIVERY.md) |

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

출력 파일은 `presentation/`에 언어별로 생성되며 Git에서는 제외합니다.
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
| 1. 프로젝트·팀 소개 | 1 | 프로젝트 목표와 공동 메인테이너 | 20초 |
| 목차 | 2 | 발표 흐름 | 15초 |
| 2. 문제·대상 | 3–5 | Pod와 DB 복구의 차이, 실제 장애 예시, 사용자 가설 | 100초 |
| 3. 현재 해결 방식·OSS 한계 | 6–7 | 이미 있는 기능과 설계 비교 | 70초 |
| 4. 제안하는 해결 방법·검증 | 8, 12–13 | 상태·작업 처리 방식, 기록된 결과, 다음 시험 | 115초 |
| 5. 아키텍처·데이터 흐름 | 9–11 | 구성 요소, SQL·제어 경로, 쓰기 안전 | 110초 |
| 6. 12주 계획·팀 역할·첫 버전 | 14–17 | 로드맵, 개발/교차 검증, 범위, 이후 방향 | 125초 |
| 7. 함께 논의할 내용 | 18 | 사용자 경험과 재현 협력 요청 | 25초 |
| **합계** | **한국어·영어 각 18장** | **목표: 9분 40초 + 전환 여유 20초** | **580초** |

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

- [x] 공지의 필수 7개 항목을 한국어·영어 각 18장에 포함
- [x] 팀원 실명과 공동 메인테이너 역할 반영
- [x] 11월 29일 필수 시나리오·12월 27일 공개 **목표**와 첫 버전 범위 명시
- [x] 2026-10-20 근거 커밋·Kind/VM 결과·남은 검증 구분
- [x] 두 언어의 발표자 메모, 한국어 대본과 Q&A 준비
- [ ] **18장 개정판** 정적 웹 빌드·PPTX/PDF 재생성·페이지/메모/폰트/레이아웃 확인
- [x] 10월 21일 **이전 11장 버전** 출력 검수 기록 보존: [DELIVERY 기록](DELIVERY.md)
- [ ] 공식 프로그램명 최종 확인: 공지의 “빌더 시즌4” 표기 사용
- [ ] 한국어 발표 실제 리허설 10분 이내
- [ ] PPTX 두 파일을 실제 PowerPoint에서 열어 최종 확인
- [ ] 10월 29일 23:59 KST까지 팀 디스코드 채널에 각각 제출
- [ ] 제출 시각과 제출 메시지 링크 기록
