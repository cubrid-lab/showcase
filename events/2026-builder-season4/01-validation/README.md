# CUBRID Kubernetes Operator — 빌더 시즌4 1차 검증

아이디어와 프로젝트의 방향성을 검증하기 위한 발표 준비 공간입니다.
프로그램 공식 명칭은 확인 전이며, 폴더명은 전달받은 “시즌4 빌더” 공지를
기준으로 정했습니다.

## 발표자료 바로 열기

- [한국어 HTML 발표](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/ko/)
- [English HTML presentation](https://cubrid-lab.github.io/showcase/events/2026-builder-season4/01-validation/en/)
- [시즌4 전체 발표 목록](../README.md)

브라우저에서 바로 넘겨 볼 수 있는 HTML 발표입니다. 현재 내용은 작성 전
7장 골격이며, Markdown 원본은 아래 자료 표에서 확인할 수 있습니다.

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
| [SLIDES.ko.md](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.ko.md) | 한국어 웹 발표 원본과 발표자 메모 | 내용 작성 전 7장 골격 |
| [SLIDES.en.md](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.en.md) | 영어 웹 발표 원본과 발표자 메모 | 내용 작성 전 7장 골격 |
| [한국어 진입 파일](../../../presentation/operator-first-validation.ko.md) | 공통 테마·웹·출력 설정 | 원본을 불러오는 Slidev 설정 |
| [영어 진입 파일](../../../presentation/operator-first-validation.en.md) | 공통 테마·웹·출력 설정 | 원본을 불러오는 Slidev 설정 |
| `operator-first-validation.ko.pptx` / `.pdf` | 한국어 원본에서 생성할 출력물 | 최종 제출본 아님 |
| `operator-first-validation.en.pptx` / `.pdf` | 영어 원본에서 생성할 출력물 | 최종 제출본 아님 |

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
사용합니다. 현재 웹 원본에는 `[작성]`·`[확인]`이 남아 있어 출력 결과도 준비용입니다.

## 발표 시간 배분

| 슬라이드 | 필수 항목 | 시간 |
|---|---|---|
| 1 | 프로젝트 소개, 팀원 소개 | 60초 |
| 2 | 해결하려는 문제와 그 문제를 겪는 대상 | 90초 |
| 3 | 현재 해결 방식과 기존 오픈소스의 한계 | 90초 |
| 4 | 팀이 제안하는 해결 방법 | 90초 |
| 5 | 아키텍처 초안 | 120초 |
| 6 | 12주 로드맵, 팀원별 역할, 첫 버전 공개 범위 | 90초 |
| 7 | 함께 논의하거나 의견을 구하고 싶은 내용 | 60초 |
| 합계 | | 600초 |

## 작성 원칙과 근거

- 구현 사실과 검증 증거는 [Operator 저장소](https://github.com/cubrid-lab/cubrid-kubernetes-operator)를 기준으로 확인합니다.
- 아키텍처는 [DESIGN.md](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/DESIGN.md),
  구현·검증 상태는 [ROADMAP.md](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md),
  안전 제약은 [ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/main/docs/adr)을 확인한 후 요약합니다.
- 발표에 사용하는 근거의 커밋과 확인일을 기록합니다. 계획, 구현, 단위/envtest 결과,
  실제 환경 검증을 구분하고 Python 생태계의 대회 지표를 Operator 성과로 사용하지 않습니다.
- 팀원 이름, 역할, 12주 계획, 시즌 종료 시 공개 범위는 팀 확인 후 채웁니다.
- 한영 자료는 같은 슬라이드 번호, 범위, 수치, 증거를 사용합니다.

## 제출 전 확인

- [ ] 공식 프로그램명, 팀명, 팀원과 역할 확인
- [ ] 12주 시작일과 종료일, 주차별 목표, 첫 공개 버전 범위 합의
- [ ] 필수 7개 항목을 한영 자료에 모두 포함
- [ ] 주장·수치·아키텍처의 출처와 확인 시점 기록
- [ ] 한국어 발표 리허설 10분 이내, Q&A 10분 준비
- [ ] 웹 원본의 작성·확인 표시와 내부 발표자 메모 정리
- [ ] 한영 웹 빌드, PPTX·PDF 내보내기 후 페이지 수·한글 폰트·레이아웃·내용 일치 확인
- [ ] 최종 제출 PPTX를 PowerPoint에서 열어 확인
- [ ] 10월 29일 23:59 KST까지 두 파일을 팀 디스코드 채널에 각각 제출
- [ ] 최종 파일명, 제출 시각, 제출 메시지 링크 기록
