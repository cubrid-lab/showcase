# 1차 검증 발표자료 — 문장 수정본과 출력 기록

문장 수정: **2026-10-21 KST, r2**. 시험 결과는 **2026-10-20** 기준입니다.
슬라이드의 추상적인 표현을 줄이고, 대본과 Q&A를 발표자가 직접 설명하는 말투로 고쳤습니다.
11장 구성과 10분 시간 배분, 기능과 지원 범위, v0.1 이후 계획은 유지했습니다.

## 현재 발표 파일

[11장 검수본 전체](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-21-r2)에서
한영 출력물과 대본·Q&A·근거·파일 식별 기록을 받습니다.

| 언어 | PowerPoint | PDF | 구성 |
|---|---|---|---|
| 한국어 | [한국어 PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-21-r2/operator-first-validation.ko.pptx) | [한국어 PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-21-r2/operator-first-validation.ko.pdf) | 11장 · 슬라이드별 발표자 메모 |
| English | [English PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-21-r2/operator-first-validation.en.pptx) | [English PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-21-r2/operator-first-validation.en.pdf) | 11 slides · notes per slide |

[패키지 ZIP](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-21-r2/builder-season4-validation-materials.zip)에는
네 출력물, 한국어 대본, Q&A, 근거 목록과 검수·파일 식별 기록을 담습니다.
`presentation-manifest.json`의 `sourceCommit`과 원본별 해시로 출력 원본을 확인합니다.
`operatorCommit`은 발표의 기술 근거이며 showcase 원본 커밋과 다릅니다.
`SHA256SUMS`로 개별 파일을, `ZIP_SHA256.txt`로 ZIP을 확인합니다.
이 배포는 **발표자료의 개정판**이며 Operator v0.1 소프트웨어 릴리스가 아닙니다.

PPTX는 Slidev 기본 출력으로 각 슬라이드 화면을 이미지로 담습니다. 발표자 메모는
텍스트이며, 본문을 PowerPoint에서 직접 편집하는 형식은 아닙니다. 수정은
[한국어](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.ko.md)·
[영어 원본](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.en.md)에 반영해 다시 출력합니다.

## 검수 범위

- 공지의 7개 항목을 두 언어 **각 11장**에 반영. 후속 방향은 10장, 의견 요청은 11장입니다.
- 두 언어의 슬라이드 순서·주장·범위와 600초 **계획**을 대조했습니다. 실측 발표 시간이 아닙니다.
- 한국어 별도 대본은 원본 메모와 일치하며, PPTX 두 파일의 11개 메모는 시간 표기를 포함해 원본과 대조했습니다.
- 기존 lockfile의 Slidev 53.0.0과 Chrome 145.0.7632.67로 전체 사이트 빌드와 한영 PPTX·PDF를 생성했습니다.
  기존 도구를 재사용하며 manifest·lockfile·의존성을 바꾸지 않았습니다.
- 실제 정적 웹 22장을 확인했습니다. 본문·표 셀과 패딩·도식 범위 넘침 0건,
  처리되지 않은 페이지 오류 0건, 외부 자산 요청 0건이며 로컬 Pretendard를 확인했습니다.
- 기존 Operator 레이아웃과 폰트를 그대로 사용했습니다. 문장이 달라진 슬라이드의 줄바꿈과
  표·도식 범위를 다시 확인했습니다. CSS·공통 테마·대회 원본·의존성은 변경하지 않았습니다.
- PPTX의 ZIP CRC/XML/내부 참조·11개 이미지 슬라이드·메모, PDF의 11페이지·16:9·본문·자체 포함 폰트와
  비어 있지 않은 렌더를 검수했습니다. 세부 결과와 해시는 배포 패키지에 포함합니다.

기존 공개본과 같은 선택적 Twoslash/FloatingVue 초기화 콘솔 경고가 있습니다.
처리되지 않은 페이지 오류와는 구분하며, 이 내용 개정에서 라이브러리 의존성은 변경하지 않았습니다.

## 이전 검수본 보존

[2026-10-20의 10장 자료](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-20)와
[2026-10-21의 내용 보강본](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-21),
[내용 보강 당시의 출력 기록](https://github.com/cubrid-lab/showcase/blob/fc5232a89a4fdfa3a603764dd005126fc7c2db5b/events/2026-builder-season4/01-validation/DELIVERY.md)은
그대로 보존합니다. 기존 태그나 첨부 파일을 덮어쓰지 않습니다.

## 실제 발표·제출 전에 남은 항목

- 한국어 실제 리허설로 10분 이내인지 측정. 600초는 시간 배분입니다.
- 두 PPTX를 실제 PowerPoint에서 열어 발표 장비·화면 비율·메모 표시 확인.
- 공식 프로그램명 확인. 전달받은 “빌더 시즌4” 표기를 사용합니다.
- **2026-10-29 23:59 KST까지** 팀 디스코드 채널에 한영 PPTX 각각 제출하고 시각·메시지 링크 기록.
  디스코드 전송은 수행하지 않았습니다.

v0.1 이후 내용은 방향안이며 후속 버전·완료일·운영 지원을 확약하지 않습니다.
VM 전원 장애·네트워크 분할·CSI·전체 S00–S15·장시간 부하 검증 완료나 운영 준비 완료를 주장하지 않습니다.
