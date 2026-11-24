---
title: "CUBRID Kubernetes Operator — 2차 검증"
---

<OperatorSlide section="Opening · 프로젝트 소개" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">빌더 시즌4 · 2차 검증 · 아키텍처 중간 검증</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">v0.1 범위와 쓰기 안전 아키텍처</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[20초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 1차 검증에서는 Kubernetes에서 CUBRID HA를 운영하고 장애 뒤 복구까지 확인하는 Operator의 목표와 계획을 말씀드렸습니다. 오늘 2차 검증에서는 그 뒤 4주 동안 실제 VM 랩에서 장애를 내 보며 알게 된 것, 그리고 그 결과로 v0.1에서 무엇을 약속하고 무엇을 약속하지 않기로 했는지 말씀드리겠습니다.
-->

---

<OperatorSlide class="op-compact" section="Agenda · 발표 순서" source="발표 구성" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">발표 순서</h1><div class="op-agenda"><div><span>01</span><b>1차 이후 바뀐 것</b><p>계획에서 실제 측정으로</p></div><div><span>02</span><b>v0.1 범위</b><p>반드시 통과 · 측정해서 공개 · v0.2로 미룸</p></div><div><span>03</span><b>쓰기 격리 아키텍처</b><p>master가 불확실할 때 쓰기 경로를 닫는 방법</p></div><div><span>04</span><b>재구축 아키텍처</b><p>볼륨을 잃은 멤버를 명시적으로 다시 채우는 방법</p></div><div><span>05</span><b>검증 결과와 한계</b><p>Kind · VM 랩 결과 · 공개할 한계</p></div><div><span>06</span><b>릴리스 일정</b><p>후보 동결 · 반복 검증 · 독립 재현 · 공개 결정</p></div></div>

</OperatorSlide>

<!--
[15초 · Agenda · 발표 순서]
오늘은 여섯 가지 순서로 말씀드리겠습니다. 1차 이후 바뀐 것, v0.1 범위, 이번 중간 검증의 중심인 쓰기 격리와 재구축 아키텍처, 검증 결과와 한계, 마지막으로 릴리스 일정입니다.
-->

---

<OperatorSlide class="op-compact" section="01 · 1차 이후 바뀐 것" source="ROADMAP 2026-11-21 결정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">1차에는 계획, 지금은 측정한 결과로 말합니다</h1><table class="op-comparison"><thead><tr><th></th><th>1차 검증 (10월 말)</th><th>2차 검증 (지금)</th></tr></thead><tbody><tr><td><b>쓰기 안전</b></td><td>master 미확정이면 “미확정”으로 표시만</td><td>쓰기 격리 구현 · 읽기-쓰기 Broker를 0으로 줄여 쓰기 경로를 닫음</td></tr><tr><td><b>장애 시험</b></td><td>Kind 중심, VM 장애는 아직</td><td>VM 랩에서 전원 차단·네트워크 분할·Operator 재시작까지 실행</td></tr><tr><td><b>판정</b></td><td>“30초 안에 복구” 같은 숫자 기준</td><td>안전 규칙은 통과/실패, 시간은 측정해서 공개</td></tr><tr><td><b>범위</b></td><td>필수 시나리오 16개 전부</td><td>11월 21일 범위 결정 · 일부는 측정 공개, 자동 재합류는 v0.2</td></tr></tbody></table><p class="op-boundary"><b>바뀐 이유</b>　VM 랩에서 CUBRID 자체 동작의 한계를 직접 확인했기 때문입니다.</p>

</OperatorSlide>

<!--
[40초 · 01 · 1차 이후 바뀐 것]
1차 때와 비교하면 네 가지가 바뀌었습니다. 1차에는 master가 불확실하면 상태에 미확정이라고 표시만 했습니다. 지금은 쓰기 격리를 구현해서, 실제로 읽기-쓰기 Broker를 0개로 줄여 쓰기 경로를 닫습니다. 장애 시험도 Kind에서 VM 랩으로 옮겨 전원 차단, 네트워크 분할, Operator 재시작까지 실행했습니다.

그리고 판정 방식과 범위를 바꿨습니다. VM 랩에서 장애를 내 보니, CUBRID 엔진 자체 동작 때문에 Operator가 보장할 수 없는 부분이 분명히 보였습니다. 그래서 11월 21일에 v0.1이 약속하는 범위를 좁히기로 결정했습니다. 다음 장에서 자세히 말씀드리겠습니다.
-->

---

<OperatorSlide section="02 · v0.1 범위">

<ChapterDivider number="01" title="v0.1 범위" subtitle="통과해야 하는 것과 측정해서 공개하는 것을 나눕니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · v0.1 범위]
v0.1 범위로 넘어가는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-compact" section="02 · v0.1 범위" source="ROADMAP · 시나리오 계약" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">v0.1은 세 칸으로 나눠 약속합니다</h1><table class="op-comparison op-acceptance"><thead><tr><th>구분</th><th>시나리오</th><th>판정</th></tr></thead><tbody><tr><td><b>반드시 통과</b></td><td>설치·HA 구성·복제 (S00–S02) · master Pod 강제 종료 (S03 abrupt) · Broker·Operator 장애 (S05–S06) · 볼륨 교체 재구축 (S10) · 백업·새 클러스터 복원 (S11–S12) · 삭제 후 보존·인증·노드 드레인 (S13–S15) · 상태·이벤트·메트릭</td><td>하나라도 실패·막힘·미실행이면 공개하지 않음</td></tr><tr><td><b>측정해서 공개</b></td><td>VM 전원 손실 (S04) · 네트워크 분할·반복 장애 (S07–S08) · master Pod 정상 종료 (S03 graceful)</td><td>시간·손실을 그대로 공개 · 안전 규칙은 그대로 통과해야 함</td></tr><tr><td><b>v0.2로 미룸</b></td><td>남아 있던 데이터로 자동 재합류 (S09) · 재생성한 클러스터의 옛 볼륨 자동 채택</td><td>이번 공개 범위가 아님</td></tr></tbody></table><p class="op-boundary"><b>지원 환경</b>　CUBRID 11.4.x · amd64 · 3-VM 랩 하나 (k3s 워커 3대, 2 vCPU·8 GiB, node-local 스토리지 — CSI 아님)</p>

</OperatorSlide>

<!--
[50초 · 02 · v0.1 범위]
v0.1은 시나리오를 세 칸으로 나눠 약속합니다. 첫 칸은 반드시 통과해야 하는 것입니다. 설치와 HA 구성, 복제, master Pod 강제 종료, Broker와 Operator 장애, 볼륨을 교체한 재구축, 백업과 새 클러스터 복원, 그리고 보존·인증·노드 드레인입니다. 여기서는 하나라도 실패하거나 실행하지 못하면 공개하지 않습니다.

두 번째 칸은 측정해서 공개하는 것입니다. VM 전원 손실, 네트워크 분할, master Pod 정상 종료입니다. 예전에는 30초 안에 복구라는 숫자 기준이 있었지만, 이제 시간은 기준이 아니라 측정값입니다. 대신 안전 규칙, 예를 들어 쓰기 경로가 닫힌 뒤에는 쓰기를 승인하지 않는다는 규칙은 그대로 통과해야 합니다.

세 번째 칸은 v0.2로 미룬 것입니다. 남아 있는 데이터로 자동으로 다시 합류하는 기능입니다. 그리고 지원 환경은 CUBRID 11.4, amd64, 그리고 저희 3-VM 랩 하나입니다. 이 랩은 node-local 스토리지라서, CSI 스토리지에서의 동작은 이번 범위에 포함하지 않습니다.
-->

---

<OperatorSlide class="op-compact" section="02 · 판정 방식" source="릴리스 후보 검증 #126" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126">

<h1 class="op-title">예전 판정은 지우지 않고, v0.1 판정을 따로 붙입니다</h1><div class="op-safety"><div><span>원래 결과</span><h3>시나리오마다 통과·실패·막힘·미실행</h3><p>30초 기준으로 실패한 과거 기록도 그대로 남깁니다. 기준을 바꿨다고 과거 실패를 통과로 고치지 않습니다.</p><p class="op-mini">원래 결과는 수정하지 않음</p></div><div><span>v0.1 판정</span><h3>범위에 따라 별도로 판정</h3><p>측정 항목에서 시간 제한만으로 실패한 경우는 그 사실을 따로 기록합니다. 안전 규칙 위반은 그대로 실패입니다.</p><p class="op-mini">예: 볼륨 교체 재구축 제한 5분</p></div></div><p class="op-boundary"><b>원칙</b>　기준을 바꿔도 증거는 바꾸지 않습니다 · 빠진 증거는 통과가 아니라 막힘입니다</p>

</OperatorSlide>

<!--
[35초 · 02 · 판정 방식]
범위를 바꾸면서 가장 조심한 것은 판정입니다. 예전 기준으로 실패한 기록을 새 기준에 맞춰 통과로 고치지 않습니다. 원래 결과는 그대로 두고, v0.1 범위에 따른 판정을 따로 붙입니다.

측정 항목에서 시간 제한만 넘긴 실패는 그 사실을 따로 기록하고, 안전 규칙을 어긴 것은 그대로 실패입니다. 예를 들어 볼륨을 잃은 멤버의 재구축은 5분 제한으로 정했고, 증거가 빠진 경우는 통과가 아니라 막힘으로 봅니다.
-->

---

<OperatorSlide section="03 · 쓰기 격리 아키텍처">

<ChapterDivider number="02" title="아키텍처 중간 검증" subtitle="master가 불확실할 때 쓰기를 막고, 잃은 멤버를 다시 채웁니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 아키텍처]
아키텍처 설명으로 넘어가는 전환 페이지입니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 쓰기 격리" source="ADR-0005 쓰기 격리" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md">

<h1 class="op-title">master를 확신할 수 없으면 쓰기 경로를 닫습니다</h1><div class="op-timeline"><div><small>① 관찰</small><b>멤버마다 역할 확인</b><p>Instance Manager로 HA 역할 조회<br>응답이 없거나 엇갈림</p></div><div><small>② 격리</small><b>쓰기 격리 시작</b><p>새 세대 번호와<br>일회용 해제 토큰 발급</p></div><div><small>③ 닫기</small><b>읽기-쓰기 Broker 0개</b><p>Deployment를 0으로 줄임<br>시험에서 Pod 종료·endpoint 비움까지 확인</p></div><div><small>④ 해제</small><b>확인 후 다시 열기</b><p>모든 멤버를 다시 확인하면 자동 해제<br>사람이 판단하면 토큰으로 수동 해제</p></div></div><p class="op-boundary"><b>1차와 차이</b>　“미확정” 표시에서 멈추지 않고, Operator가 관리하는 쓰기 경로를 실제로 닫습니다</p>

</OperatorSlide>

<!--
[45초 · 03 · 쓰기 격리]
1차 때 가장 큰 위험은 master가 미확정인데 쓰기가 승인된 것이었습니다. 그래서 쓰기 격리를 만들었습니다. Operator가 각 멤버의 HA 역할을 확인하다가 응답이 없거나 서로 엇갈리면, 새 세대 번호와 한 번만 쓸 수 있는 해제 토큰을 만들고 쓰기 격리를 시작합니다.

그다음 읽기-쓰기 Broker의 Deployment를 0으로 줄입니다. 장애 시험에서는 Pod가 실제로 종료되고 Service endpoint가 비었는지, 그 뒤 쓰기가 승인되지 않는지까지 확인합니다. 해제는 두 가지입니다. 모든 멤버를 다시 확인할 수 있으면 자동으로 풀리고, 사람이 판단해야 하는 경우에는 그 격리의 토큰으로만 풀 수 있습니다. 이전 격리의 토큰으로는 새 격리를 풀 수 없게 했습니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 쓰기 격리의 경계" source="시나리오 계약 · S07–S08" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">Operator가 닫을 수 있는 것과 닫을 수 없는 것</h1><div class="op-safety"><div><span>Operator가 약속</span><h3>관리하는 읽기-쓰기 경로는 닫습니다</h3><p>경로를 닫은 뒤에는 새 연결이든 이미 열린 세션이든 쓰기가 승인되면 안 됩니다. 이것은 v0.1에서 반드시 지키는 안전 규칙입니다.</p><p class="op-mini">닫힌 뒤 승인된 쓰기 0건</p></div><div><span>Operator가 약속하지 않음</span><h3>CUBRID 자체 승격과 닫기 전 손실</h3><p>CUBRID HA는 Operator와 무관하게 다른 멤버를 master로 올릴 수 있습니다. 경로를 닫기 전에 승인된 쓰기가 새 master에 없을 수 있고, 이 손실은 숨기지 않고 공개합니다.</p><p class="op-mini">데이터 손실 0 보장 안 함</p></div></div><p class="op-boundary"><b>그래서</b>　네트워크 분할은 통과/실패 대신 “닫히기까지 걸린 시간과 손실”을 측정해 공개합니다</p>

</OperatorSlide>

<!--
[40초 · 03 · 쓰기 격리의 경계]
여기서 경계를 분명히 하겠습니다. Operator가 약속하는 것은 자기가 관리하는 읽기-쓰기 경로를 닫는 것입니다. 닫힌 뒤에는 새 연결이든 이미 열려 있던 세션이든 쓰기가 승인되면 안 되고, 이것은 반드시 지킵니다.

반면 CUBRID HA는 Operator와 상관없이 다른 멤버를 master로 올릴 수 있습니다. 경로를 닫기 전에 승인된 쓰기가 새 master에 없을 수 있습니다. 이건 엔진 동작이라 Operator가 막을 수 없어서, 데이터 손실 0을 보장한다고 말하지 않고 측정해서 공개하기로 했습니다.
-->

---

<OperatorSlide class="op-compact" section="04 · 재구축" source="볼륨 교체 재구축 #118" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118">

<h1 class="op-title">볼륨을 잃은 멤버는 명시적인 요청으로 다시 채웁니다</h1><div class="op-timeline"><div><small>① 감지</small><b>빈 볼륨으로 다시 뜬 멤버</b><p>데이터가 없는 멤버는<br>쓰기 격리에 들어감</p></div><div><small>② 요청</small><b>사람이 재구축 요청</b><p>자동으로 덮어쓰지 않음<br>대상 멤버와 볼륨 확인</p></div><div><small>③ 재구축</small><b>살아 있는 멤버에서 복사</b><p>백업으로 채운 뒤<br>slave로 다시 합류</p></div><div><small>④ 확인</small><b>확인된 행 대조</b><p>장애 전 승인된 모든 행이<br>재구축한 멤버에 있는지</p></div></div><p class="op-boundary"><b>측정</b>　Kind에서 요청부터 완료까지 40.2초, 모든 행 확인까지 48.9초 · v0.1 제한은 5분</p>

</OperatorSlide>

<!--
[40초 · 04 · 재구축]
두 번째 아키텍처는 볼륨을 잃은 멤버의 재구축입니다. 데이터가 없는 멤버가 다시 뜨면 Operator는 그 멤버를 자동으로 덮어쓰지 않습니다. 쓰기 격리에 넣고, 사람이 대상 멤버와 볼륨을 확인한 뒤 재구축을 요청하게 했습니다.

요청하면 살아 있는 멤버에서 백업으로 채우고 slave로 다시 합류시킵니다. 마지막으로 장애 전에 승인된 모든 행이 재구축한 멤버에 있는지 SQL로 대조합니다. Kind에서는 요청부터 완료까지 40초 정도였고, v0.1 제한은 여유를 두고 5분으로 정했습니다. 남아 있던 데이터로 자동 재합류하는 기능은 v0.2로 미뤘습니다.
-->

---

<OperatorSlide section="05 · 검증 결과와 한계">

<ChapterDivider number="03" title="검증 결과와 남은 위험" subtitle="통과한 것과 숨기지 않을 것" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 검증 결과]
결과와 한계로 넘어가는 전환 페이지입니다.
-->

---

<OperatorSlide class="op-compact" section="05 · Kind 결과" source="Kind E2E 실행 기록" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1109">

<h1 class="op-title">Kind에서는 전체 테스트를 매번 돌립니다</h1><div class="op-specs-head"><span class="op-evidence-number">55 / 55</span><div><b>Kind E2E 테스트 55개 통과</b><p>1차의 27개에서 늘어났습니다 · 실제 CUBRID 이미지로 한 번 도는 데 약 64분</p></div></div><table class="op-comparison"><thead><tr><th>무엇을 고쳤나</th><th>결과</th></tr></thead><tbody><tr><td>테스트가 DB에 로컬 소켓으로 붙을 때 가끔 세션이 끊김</td><td>11.10–11.20 실패한 실행 58건 중 9건이 이 원인 → TCP 접속으로 바꾼 11.22 이후 같은 원인의 실패 없음</td></tr><tr><td>재구축 중 다른 멤버의 역할 확인이 한 번 늦음</td><td>원인을 바로 보여 주도록 테스트 개선 · 처리 방법은 메인테이너 결정</td></tr></tbody></table><p class="op-boundary"><b>한계</b>　Kind 통과는 VM 랩 검증을 대신하지 않습니다</p>

</OperatorSlide>

<!--
[35초 · 05 · Kind 결과]
먼저 Kind 결과입니다. 1차 때 27개였던 E2E 테스트가 55개로 늘었고, 실제 CUBRID 이미지로 전부 통과합니다. 한 번 도는 데 64분 정도 걸리는데, 이 시간을 줄이는 것도 지금 과제입니다.

불안정했던 테스트도 원인을 찾아 고쳤습니다. 테스트가 DB에 로컬 소켓으로 붙을 때 세션이 가끔 끊겼는데, 11월 10일부터 20일까지 실패한 실행 58건 중 9건이 이 원인이었고, 11월 22일 TCP 접속으로 바꾼 뒤로는 아직 같은 원인의 실패가 없습니다. 관찰 기간이 짧아서 계속 지켜보고 있습니다. 다만 Kind 통과가 VM 랩 검증을 대신하지는 않습니다.
-->

---

<OperatorSlide class="op-compact" section="05 · VM 랩 결과" source="VM 랩 실행 기록 #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">VM 랩에서 실제 장애를 내고 확인했습니다</h1><table class="op-comparison op-fault-map"><tbody><tr><td>네트워크 분할 + Operator 재시작<small>S07</small></td><td>격리 중 Operator를 재시작해도 같은 격리 유지 · Broker 0개 · 쓰기 승인 없음 · 모든 멤버에 확인된 행 보존</td><td><em class="ok">통과</em></td></tr><tr><td>볼륨 교체 재구축<small>S10</small></td><td>VM 랩에서 재구축 후 행 대조</td><td><em class="ok">통과</em></td></tr><tr><td>백업 → 새 클러스터 복원<small>S12</small></td><td>VM 랩에서 세 번 복원 · 세션 끊김 없음</td><td><em class="ok">통과</em></td></tr><tr><td>VM 전원 손실<small>S04</small></td><td>역할·접속 복구 시간 분포 측정 중</td><td><em class="part">측정</em></td></tr><tr><td>반복 분할<small>S07</small></td><td>첫 격리 해제 뒤 다시 분할 · 옛 토큰으로 새 격리를 못 푸는지</td><td><em class="no">실행 전</em></td></tr></tbody></table><p class="op-boundary"><b>랩 규칙</b>　한 번에 하나의 장애 시험 · 실행 전 공지 · 실행 중에는 랩 점유 Lease</p>

</OperatorSlide>

<!--
[45초 · 05 · VM 랩 결과]
VM 랩에서는 실제로 장애를 냈습니다. 네트워크 분할 중에 Operator를 재시작해도 같은 격리가 유지됐고, Broker는 0개, 분할 동안 쓰기 승인은 없었으며, 끝난 뒤 모든 멤버에 확인된 행이 남아 있었습니다. 볼륨 교체 재구축과 새 클러스터 복원도 VM 랩에서 통과했습니다.

VM 전원 손실은 복구 시간 분포를 측정하는 중입니다. 첫 격리를 해제한 뒤 다시 분할했을 때 옛 토큰으로 새 격리를 풀 수 없는지 보는 시험은 코드 리뷰를 마쳤고, VM 랩 실행은 아직입니다. 랩은 공유 자원이라 한 번에 하나만, 공지하고, 점유 Lease를 잡은 상태에서만 실행합니다.
-->

---

<OperatorSlide class="op-compact" section="05 · 공개할 한계" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">숨기지 않고 공개할 한계</h1><ol class="op-risks"><li><b>VM 전원 손실 중 복제 지연을 만들었을 때 승인된 쓰기 13건 손실</b><span>CUBRID가 멈춘 복제 프로세스를 끊은 뒤에도 커밋을 승인하는 기본 설정 때문 · 엔진 동작</span></li><li><b>네트워크 분할에서 승격된 멤버에 승인된 쓰기 최대 73건 없음</b><span>경로를 닫기 전에 승인된 쓰기 · 손실 0을 보장하지 않는 이유</span></li><li><b>master Pod 정상 종료 때 쓰기 경로가 28초 닫힘</b><span>불필요한 격리 · 시간과 원인을 공개</span></li><li><b>스토리지는 node-local, CSI 아님</b><span>볼륨이 다른 노드로 따라가는 동작·스냅샷·크기 변경은 검증하지 않음</span></li></ol><p class="op-boundary"><b>원칙</b>　엔진 결함은 Operator에서 고치지 않고 문서화합니다 · 손실 0이나 자동 복구를 보장한다고 말하지 않습니다</p>

</OperatorSlide>

<!--
[45초 · 05 · 공개할 한계]
공개할 한계입니다. VM 전원 손실 중 복제 지연을 일부러 만들었을 때 승인된 쓰기 13건이 사라졌습니다. CUBRID 기본 설정이 멈춘 복제 프로세스를 끊은 뒤에도 커밋을 승인하기 때문입니다. 네트워크 분할에서는 경로를 닫기 전에 승인된 쓰기가 승격된 멤버에 최대 73건 없었습니다. master Pod를 정상 종료할 때 쓰기 경로가 28초 닫히는 문제도 있습니다.

그리고 저희 랩은 node-local 스토리지라 CSI 동작은 검증하지 않았습니다. 엔진 결함을 Operator에서 억지로 고치지 않고, 손실 0을 보장한다고도 말하지 않겠습니다. 대신 이 숫자들을 그대로 공개합니다.
-->

---

<OperatorSlide section="06 · 릴리스 일정">

<ChapterDivider number="04" title="v0.1 릴리스 일정" subtitle="날짜가 아니라 증거로 공개를 결정합니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 릴리스 일정]
릴리스 일정으로 넘어가는 전환 페이지입니다.
-->

---

<OperatorSlide section="06 · 릴리스 일정" source="ROADMAP v0.1 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">12월 7일 후보를 고정하고, 세 번 검증합니다</h1><div class="op-timeline"><div><small>11.30–12.06</small><b>후보 준비</b><p>판정 도구 정렬<br>이미지·소스 식별<br>랩 통제 점검</p></div><div><small>12.07</small><b>후보 동결</b><p>소스·이미지·엔진·랩을<br>하나로 고정</p></div><div><small>12.08–12.14</small><b>반복 검증</b><p>필수 시나리오 반복<br>24시간 부하 시험</p></div><div><small>12.15–12.20</small><b>독립 재현</b><p>작성자가 아닌 사람이<br>문서만 보고 설치·복구·복원</p></div></div><p class="op-boundary"><b>12.21–12.27</b> 증거를 보고 공개 여부 결정　·　필수 증거가 빠지면 공개하지 않습니다</p>

</OperatorSlide>

<!--
[40초 · 06 · 릴리스 일정]
남은 일정입니다. 11월 말부터 판정 도구와 이미지 식별, 랩 통제를 정리하고, 12월 7일에 소스와 이미지, 엔진 버전, 랩을 하나로 고정합니다. 그 후보로 필수 시나리오를 반복하고 24시간 부하 시험을 합니다.

12월 15일부터는 코드를 쓰지 않은 사람이 문서만 보고 설치, 장애 복구, 복원을 재현합니다. 마지막 주에 증거를 보고 공개 여부를 정합니다. 날짜에 맞추려고 억지로 공개하지 않고, 필수 증거가 빠지면 공개하지 않습니다.
-->

---

<OperatorSlide section="06 · 팀 역할" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md">

<h1 class="op-title">만든 사람과 검증하는 사람을 나눕니다</h1><div class="op-people"><div><p class="op-kicker">구현 · 시나리오 실행</p><b>만들고 기록합니다</b><p>Operator 구현, 장애 시나리오, 판정 도구, VM 랩 실행 기록을 맡습니다.</p></div><div><p class="op-kicker">리뷰 · 랩 · 독립 재현</p><b>교차 검증합니다</b><p>코드와 실행 결과를 교차 검증하고, VM 랩 인프라를 운영하며, 공개 전 문서만 보고 재현합니다.</p></div></div><p class="op-boundary"><b>원칙</b>　작성자와 최종 검증자는 다른 사람입니다 · 공유 랩 장애 시험은 한 번에 하나씩 · 공개 여부는 함께 결정</p>

</OperatorSlide>

<!--
[25초 · 06 · 팀 역할]
팀 역할은 1차 때 말씀드린 원칙을 그대로 지키고 있습니다. 구현과 시나리오 실행, 그리고 리뷰와 랩 운영, 독립 재현을 나눴습니다. 작성자와 최종 검증자를 다르게 하고, 공유 랩 시험은 한 번에 하나씩, 공개 여부는 함께 결정합니다.
-->

---

<OperatorSlide class="op-compact" section="06 · v0.1 이후" source="ROADMAP · v0.2 후보" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">v0.1 이후에는 미룬 것부터 다시 봅니다</h1><div class="op-goals"><div><span>01</span><b>자동 재합류</b><p>남아 있던 데이터로 멤버가 안전하게 다시 합류 (S09)</p></div><div><span>02</span><b>옛 볼륨 채택</b><p>클러스터를 다시 만들 때 기존 볼륨을 안전하게 이어받기</p></div><div><span>03</span><b>아카이브 로그 한도</b><p>멤버 볼륨 안에서 아카이브 로그가 차지할 공간 제한</p></div><div><span>04</span><b>관찰과 격리 정책 분리</b><p>HA 상태 수집과 쓰기 격리 판단을 나눠 다시 설계</p></div></div><p class="op-caption">로드맵에서 v0.1 이후로 미룬 항목입니다 · 우선순위는 v0.1 결과와 사용자 피드백을 보고 정합니다</p>

</OperatorSlide>

<!--
[25초 · 06 · v0.1 이후]
v0.1 이후에는 로드맵에서 미뤄 둔 것부터 다시 봅니다. 남아 있던 데이터로 자동 재합류, 클러스터를 다시 만들 때 옛 볼륨을 이어받는 것, 멤버 볼륨 안에서 아카이브 로그 공간을 제한하는 것, 그리고 HA 상태 수집과 쓰기 격리 판단을 나누는 설계입니다. 우선순위는 v0.1 결과와 사용자 피드백을 보고 정하겠습니다.
-->

---

<OperatorSlide section="Q&A" source="Operator 저장소" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><div class="op-meta"><b>github.com/cubrid-lab/cubrid-kubernetes-operator</b></div></div>

</OperatorSlide>

<!--
[Q&A]
감사합니다. 질문 받겠습니다.
-->
