# 1차 검증 발표자료 — 출력·검수 기록

작성·근거 기준: **2026-10-20 KST**. 한국어 발표와 영어 제출용 자료를 같은
Slidev 원본에서 생성했습니다. 발표·제출 완료 기록과 구분합니다.

## 발표 파일

[검수본 전체](https://github.com/cubrid-lab/showcase/releases/tag/builder-season4-validation-2026-10-20)에서
출력 파일, 대본·Q&A, 원본 커밋과 SHA256 목록을 받습니다.

| 언어 | PowerPoint | PDF | 구성 |
|---|---|---|---|
| 한국어 | [한국어 PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-20/operator-first-validation.ko.pptx) | [한국어 PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-20/operator-first-validation.ko.pdf) | 10장 · 슬라이드별 발표자 메모 |
| English | [English PPTX](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-20/operator-first-validation.en.pptx) | [English PDF](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-20/operator-first-validation.en.pdf) | 10 slides · speaker notes per slide |

[전체 패키지 ZIP](https://github.com/cubrid-lab/showcase/releases/download/builder-season4-validation-2026-10-20/builder-season4-validation-materials.zip)에는
두 언어의 PPTX·PDF, 한국어 대본, Q&A, 근거 목록과 파일 식별 기록을 담습니다.
`presentation-manifest.json`의 `sourceCommit`은 실제 출력에 사용한 showcase 원본
커밋이며, `operatorCommit`은 발표에서 설명하는 Operator 코드 기준입니다.
두 커밋은 서로 다른 저장소의 식별자입니다. `SHA256SUMS`로 파일을 확인할 수 있습니다.

PPTX는 각 슬라이드의 화면을 이미지로 담는 Slidev 기본 형식입니다. 발표자 메모는
텍스트로 들어가며, 슬라이드 본문 텍스트를 PowerPoint에서 직접 편집하는 형식은 아닙니다.
수정은 [한국어](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.ko.md)·
[영어 원본](../../../presentation/decks/2026-builder-season4/01-validation/SLIDES.en.md)에 반영하고 다시 출력합니다.

## 확인한 항목

- 공지의 7개 항목, 두 언어 각 10장, 동일한 600초 **계획**과 대응하는 주장·수치.
- 한국어 별도 대본과 원본 발표자 메모의 일치, PPTX별 메모 10개 포함.
- 고정 lockfile의 Slidev 53.0.0으로 전체 사이트 빌드와 두 언어 PPTX·PDF 출력.
  내보내기용 선택 도구는 별도로 사용했으며 프로젝트 manifest·lockfile은 바꾸지 않았습니다.
- Chrome 145.0.7632.67에서 한국어·영어 정적 웹 20장 확인. 텍스트 경계 넘침 0건,
  처리되지 않은 페이지 오류 0건, 외부 자산 요청 0건. 로컬 Pretendard 로드 확인.
- ZIP/XML·내부 참조, 각 파일의 10장/10페이지와 16:9 비율, 모든 페이지의 비어 있지 않은
  이미지·본문, PDF의 자체 포함 글리프와 한영 문서 제목 확인.
- 기존 흰 바탕·파란 강조·서체를 유지한 시각 검수. 기존 대회 원본·공통 테마는 수정하지 않았습니다.
- 원본 첫 슬라이드의 제목 메타데이터를 보완해 PPTX의 기본 생성기 제목을 교체했습니다.
  보완 전후 20개 슬라이드 PNG는 바이트 단위로 같아 레이아웃 변경이 없었습니다.

기존 공개본과 같은 선택적 Twoslash/FloatingVue 툴팁 초기화 콘솔 경고가 있습니다.
예외는 라이브러리 내부에서 처리되며, 위의 웹 렌더·폰트·본문·내보내기 검사는
통과했습니다. 이 자료 완성 작업에서 공통 도구 의존성을 변경하지 않았습니다.

## 실제 발표·제출 전에 남은 항목

- 한국어 실제 발표 리허설로 10분 이내인지 측정. 600초 시간표는 실측 기록이 아닙니다.
- 두 PPTX를 실제 PowerPoint에서 열어 발표 장비·화면 비율·메모 표시 최종 확인.
- 공지의 공식 프로그램명 확인. 본문은 전달받은 “빌더 시즌4” 표기를 사용합니다.
- **2026-10-29 23:59 KST까지** 팀 디스코드 채널에 한국어·영어 PPTX를 각각 제출하고,
  실제 제출 시각과 메시지 링크를 기록. 디스코드 전송은 이 작업에 포함하지 않았습니다.

VM SQL 연결 결과는 [고정 근거](SOURCES.md)에서 확인합니다. VM 전원 장애·네트워크
분할·CSI·전체 S00–S15·장시간 부하 검증 완료나 운영 준비 완료를 주장하지 않습니다.
