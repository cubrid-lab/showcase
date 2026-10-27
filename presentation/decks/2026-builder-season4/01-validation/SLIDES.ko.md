---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="Opening · 프로젝트 소개" index="01" total="18" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">Kubernetes에서 CUBRID 설치부터 장애 후 복구 확인까지</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[20초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저희는 관계형 DBMS인 CUBRID를 Kubernetes에서 관리하는 Operator를 만들고 있습니다. 설치만 자동화하는 것이 아니라, 장애가 난 뒤 정말 복구됐는지 확인하는 과정까지 운영 흐름으로 묶는 것이 목표입니다.

이번 시즌에는 환경 하나를 정해서 직접 설치하고, 장애를 내고, 복구되는 것까지 확인한 v0.1을 내려고 합니다. 먼저 오늘 어떤 순서로 말씀드릴지 짧게 보여드리겠습니다.
-->

---

<OperatorSlide class="op-compact" section="Agenda · 오늘의 흐름" index="02" total="18" source="발표 구성" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/README.md">

<h1 class="op-title">발표 순서</h1><div class="op-agenda"><div><span>01</span><b>왜 필요한가</b><p>Pod 복구와 DB 복구는 왜 다른가</p></div><div><span>02</span><b>어떻게 풀까</b><p>Operator · CUBRID HA · Instance Manager의 역할</p></div><div><span>03</span><b>어디까지 왔나</b><p>지금 확인한 것과 아직 남은 리스크</p></div><div><span>04</span><b>어디까지 내놓을까</b><p>12주 계획과 v0.1 공개 범위</p></div></div>

</OperatorSlide>

<!--
[15초 · Agenda · 오늘의 흐름]
오늘은 네 가지 순서로 말씀드리겠습니다. Pod가 살아나는 것만으로는 왜 부족한지, 이 문제를 어떤 구조로 푸는지, 지금 어디까지 확인했고 무엇이 남았는지, 12월 v0.1에서 어디까지 공개할지입니다. 마지막에는 여러분의 운영 경험도 여쭙겠습니다.
-->

---

<OperatorSlide section="1 · 문제" index="03" total="18" source="문제와 사용자" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">Pod가 살아났다고 DB가 복구된 건 아닙니다</h1><p class="op-kicker">예: 실행 중이던 master의 Pod가 사라졌다가 다시 떴다면?</p><div class="op-split"><div><p class="op-split-label">Kubernetes 모니터링은 Pod 상태까지</p><ol class="op-questions op-big"><li>Pod가 다시 떴나요?</li></ol></div><div><p class="op-split-label">DB를 알아야 답할 수 있음</p><ol class="op-questions op-big" start="2" style="counter-reset: discussion 1"><li>누가 master인가요?</li><li>쓰고 읽을 수 있나요?</li><li>데이터가 남았나요?</li></ol></div></div>

</OperatorSlide>

<!--
[35초 · 1 · 문제]
master Pod가 사라졌다가 다시 떴다고 해보겠습니다. Pod가 Ready이고 볼륨도 붙었습니다. Kubernetes 모니터링이 알려주는 건 여기까지입니다.

하지만 지금 master가 누구인지, 쓰고 읽을 수 있는지, 장애 전 데이터가 남았는지는 DB를 알아야 답할 수 있습니다. 무엇을 확인해야 복구됐다고 말할 수 있는지가 이 프로젝트의 핵심입니다.
-->

---

<OperatorSlide section="1 · 초기 사용자" index="04" total="18" source="문제·사용자 가설" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">두 팀이 같은 장애를 서로 다른 화면에서 봅니다</h1><div class="op-scene"><div class="op-actor"><div class="op-bubble">Pod는 다시 떴어요.<br>이제 된 거죠?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>Kubernetes 플랫폼 담당자</b></div><div class="op-incident"><span>⚡</span><b>같은 장애</b></div><div class="op-actor op-actor-db"><div class="op-bubble">master는 누구죠?<br>데이터는 괜찮나요?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>CUBRID DB 담당자</b></div></div><p class="op-boundary">두 사람이 같은 화면에서 “복구됐다”를 함께 확인할 수 있게 하는 것이 우리의 목표입니다.</p>

</OperatorSlide>

<!--
[30초 · 1 · 초기 사용자]
누구를 위한 도구인지도 분명히 하고 싶습니다. 먼저 Kubernetes 플랫폼 담당자는 Pod와 볼륨 같은 인프라 상태를 잘 봅니다. CUBRID 담당자는 master와 replica 역할, 실제 SQL 결과와 데이터를 확인합니다. 문제가 생기면 같은 장애를 다른 화면에서 보고 대화해야 합니다.

저희는 두 팀을 첫 사용자로 가정하고 있습니다. 인터뷰로 불편의 우선순위를 확정한 것은 아니며, 그래서 오늘 운영 경험을 듣고 싶습니다. 두 사람이 같은 화면에서 복구를 함께 확인할 수 있게 하는 것이 저희의 목표입니다.
-->

---

<OperatorSlide section="1 · 현재 대안" index="05" total="18" source="공식 구현·비교 범위" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">공식 Operator가 이미 있는데, 왜 또 만들까요?</h1><div class="op-split"><div><p class="op-split-label">공식 CUBRID Operator가 이미 하는 일</p><ul class="op-list"><li><b>HA 상태 조회</b></li><li><b>스토리지 관리</b></li><li><b>예약 백업</b></li></ul></div><div><p class="op-split-label">우리가 더하려는 것</p><ul class="op-list"><li><b>한 멤버 말만 믿지 않기</b><small>멤버 응답이 없거나 서로 다르면 “미확정”으로 남김</small></li><li><b>끊긴 작업도 기록 남기기</b><small>백업·복원 요청과 결과를 ID로 추적</small></li><li><b>복구를 SQL과 데이터로 검증하기</b><small>Pod 상태에 더해 실제 쓰기·읽기로 시험</small></li></ul></div></div><p class="op-boundary">정확한 복구 판단을 도와 장애가 번지는 것을 막는 것이 목표입니다.</p>

</OperatorSlide>

<!--
[30초 · 1 · 현재 대안]
CUBRID에는 이미 공식 Operator가 있습니다. HA 상태 조회, 스토리지, 예약 백업까지 중요한 기능을 제공합니다. 그럼 저희는 왜 또 만들까요?

저희가 더하려는 건 세 가지입니다. 멤버 응답이 없거나 엇갈리면 master를 추정하지 않고 미확정으로 남깁니다. 백업처럼 오래 걸리는 작업은 중간에 끊겨도 요청과 결과를 기록으로 남깁니다. 그리고 복구는 Pod 상태가 아니라 실제 SQL과 데이터로 확인합니다. 이 차이가 실제 장애에서 의미가 있는지는 시험으로 보여드려야 합니다.
-->

---

<OperatorSlide class="op-compact" section="1 · 기존 방식 비교" index="06" total="18" source="공식 Operator·소스 비교" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">구체적으로 무엇을 다르게 하나요?</h1><table class="op-comparison"><thead><tr><th></th><th>공식 Operator (지금)</th><th>우리가 바꾸는 것</th></tr></thead><tbody><tr><td><b>master 멤버 확인</b></td><td>처음 응답한 멤버 하나의<br>노드 정보를 그대로 사용</td><td>모든 멤버의 최신 응답을 비교<br>빠지거나 엇갈리면 “미확정”으로 표시</td></tr><tr><td><b>백업 작업 기록</b></td><td>예약 백업을 Pod 안에서 명령으로 실행<br>백업 상태를 기록</td><td>Instance Manager에 요청하고 작업 ID를 볼륨에 기록<br>재시작으로 끊긴 작업은 “실패”로 남김</td></tr><tr><td><b>복원</b></td><td>대상 Pod·스크립트·저장소를 지정</td><td>복원 전에 파일 목록과 체크섬을 확인<br>항상 새 클러스터로 복원</td></tr><tr><td><b>복구 확인</b></td><td>포트 검사</td><td>포트 검사는 같음<br>시험에서 실제 SQL 쓰기·읽기와 데이터까지 확인</td></tr></tbody></table><p class="op-caption">확인한 소스 버전 기준의 비교입니다. 실제 장애에서 어느 쪽이 더 안정적인지는 아직 시험 전입니다.</p>

</OperatorSlide>

<!--
[40초 · 1 · 기존 방식 비교]
5장에서 말씀드린 차이를 조금 더 구체적으로 보여드리겠습니다. 표는 두 프로젝트의 소스를 직접 읽고 정리한 것입니다.

공식 Operator는 처음 응답한 멤버 하나의 정보로 master를 판단합니다. 저희는 모든 멤버의 최신 응답을 비교하고, 빠지거나 엇갈리면 미확정으로 둡니다. 백업 같은 작업은 Instance Manager에 요청하고 작업 ID를 볼륨에 남겨서, 중간에 끊기면 실패로 기록합니다. 복원 전에는 파일 목록과 체크섬을 확인합니다. 운영 중 판단은 두 쪽 모두 포트 검사를 쓰기 때문에, 저희는 시험에서 SQL과 데이터를 따로 확인합니다. 실제 장애에서 어느 쪽이 더 안정적인지는 아직 비교하지 못했습니다.
-->

---

<OperatorSlide section="2 · 접근" index="07" total="18" source="설계 문서" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">YAML만 쓰면 나머지는 Operator가 이어줍니다</h1><div class="op-path"><div class="op-node project">YAML로 설정<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">DB 상태 조회<small>역할·복제·접속</small></div><div class="op-arrow">→</div><div class="op-node project">작업 요청·조회<small>작업 ID·진행·결과</small></div><div class="op-arrow">→</div><div class="op-node">상태 갱신<small>Conditions·Events</small></div></div>

</OperatorSlide>

<!--
[35초 · 2 · 접근]
사용자는 YAML에 원하는 구성을 적습니다. Operator가 DB 상태를 읽고 필요한 작업을 요청한 뒤, 진행 상황과 결과를 갱신합니다. 백업처럼 오래 걸리는 작업은 ID로 다시 찾아볼 수 있게 합니다. 작업 기록을 읽을 수 없으면 새 작업을 임의로 시작하지 않게 하는 것도 중요한 부분입니다.
-->

---

<OperatorSlide class="op-compact" section="2 · 구조" index="08" total="18" source="구성도" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID는 HA를, Operator는 관찰과 조정을 맡습니다</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>상태 조회·리소스 관리</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes 리소스<small>StatefulSet·Service·볼륨</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID HA가 복제와 master 전환을 담당</p><div class="op-peer-group"><div class="op-node engine">CUBRID + Instance Manager<small>멤버 0 · 볼륨</small></div><div class="op-node engine">CUBRID + Instance Manager<small>멤버 1 · 볼륨</small></div><div class="op-node engine">CUBRID + Instance Manager<small>멤버 2 · 볼륨</small></div></div></div><div class="op-stack"><div class="op-node">Broker<small>DB와 분리된 RW / RO 접속</small></div><div class="op-node storage">백업 저장소<small>오브젝트 저장소 · 초기 복사·백업·복원</small></div></div></div>

</OperatorSlide>

<!--
[40초 · 2 · 구조]
구성은 크게 Operator, DB 멤버, Broker, 백업 저장소입니다. Operator는 Kubernetes API로 StatefulSet과 Service, 볼륨을 관리합니다. 각 DB 컨테이너 안에는 CUBRID와 Instance Manager가 함께 돌고, DB 시작이나 백업 같은 작업은 Instance Manager에 요청합니다.

Broker는 DB와 따로 두고 RW와 RO 접속을 받습니다. 초기 데이터 복사와 백업 파일은 오브젝트 저장소를 거칩니다. 복제와 master 전환은 CUBRID가 맡고, Operator가 직접 master를 바꾸지는 않습니다.
-->

---

<OperatorSlide class="op-compact" section="2 · 데이터·제어 흐름" index="09" total="18" source="SQL과 운영 요청" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL 경로와 운영 경로를 분리했습니다</h1><div class="op-stack"><p class="op-kicker">애플리케이션에서 SQL을 실행할 때</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">설정을 바꾸거나 DB 작업을 요청할 때</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">Instance Manager<small>DB 작업·작업 기록</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / 볼륨</div></div></div><p class="op-boundary"><b>master 장애 뒤 확인 순서</b>　CUBRID 역할 전환 → 멤버별 조회 → Operator 상태 갱신 → SQL·데이터 확인</p>

</OperatorSlide>

<!--
[35초 · 2 · 데이터·제어 흐름]
애플리케이션의 SQL은 위쪽 경로로 갑니다. RW나 RO Service에서 Broker를 거쳐 CUBRID로 들어갑니다. Operator는 SQL을 중계하지 않습니다. 아래쪽은 설정을 바꾸거나 DB 작업을 요청하는 경로로, Operator가 Instance Manager를 호출하고 결과를 상태에 반영합니다.

master에 장애가 나면 CUBRID의 역할 전환을 먼저 보고, 멤버별로 조회해 Operator 상태가 맞게 바뀌는지 확인한 뒤, 마지막으로 SQL과 데이터를 확인합니다.
-->

---

<OperatorSlide section="2 · 장애 대응 원칙" index="10" total="18" source="쓰기 격리 이슈·ADR" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">master를 모를 때는 성공보다 안전이 먼저입니다</h1>
<div class="op-safety">
  <div><span>현재 설계와 구현</span><h3>정보가 부족하면 master 미확정</h3><p>멤버 응답이 빠졌거나 역할 정보가 충돌하면, 한 멤버를 임의로 master라고 표시하지 않습니다.</p><p class="op-mini">상태: 미확정으로 관측</p></div>
  <div><span>v0.1 필수 검증</span><h3>그동안 RW 쓰기도 막혀야 함</h3><p>잘못된 쓰기 성공 응답을 막으려면 실제 Broker·SQL 경로에 쓰기 격리가 적용되는지 확인해야 합니다.</p><p class="op-mini">상태: 아직 구현·검증 전</p></div>
</div>
<p class="op-boundary"><b>중요한 구분</b>　상태에 “모름”이라고 기록하는 것만으로 SQL 쓰기가 막히지는 않습니다.</p>

</OperatorSlide>

<!--
[35초 · 2 · 장애 대응 원칙]
이 장은 아직 부족한 부분을 숨기지 않기 위해 넣었습니다. Operator는 각 멤버의 관측값이 충분하지 않으면 master를 미확정으로 둡니다. 그러나 그것은 상태 표시일 뿐, 실제 서비스의 쓰기 경로가 자동으로 막혔다는 뜻은 아닙니다.

10월에 기록한 Kind 시험에서도 master를 확정하지 못하는 동안 RW 쓰기 성공 응답이 나왔습니다. 그래서 쓰기 격리와 네트워크 분할 시험은 v0.1의 필수 조건입니다. 안전하다고 주장하기 전에 SQL로 확인해야 합니다.
-->

---

<OperatorSlide section="3 · 검증 근거" index="11" total="18" source="2026.10.20–25 실행 기록" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">실제로 확인한 결과는 여기까지입니다</h1>
<div class="op-evidence-list">
  <div><span class="op-evidence-number">27 / 27</span><div><b>Kind E2E 테스트 spec 통과</b><p>2026.10.20 실행 기준 · 테스트 spec 수이며 필수 복구 시나리오 완료 수는 아닙니다.</p></div></div>
  <div><span class="op-evidence-number">RW / RO</span><div><b>VM 접속과 롤아웃 후 기존 데이터 확인</b><p>k3s / CUBRID 11.4.6 · 기존 볼륨·행 보존, RW 쓰기 / RO 읽기 / RO 쓰기 거부 확인 · VM 전원 장애 시험은 아님</p></div></div>
  <div><span class="op-evidence-number">5 / 7</span><div><b>VM에서 백업으로 새 클러스터 복원 통과</b><p>2026.10.25 실행 기준 · 나머지 2회는 세션 끊김(원인 조사 중, #238)으로 판정 보류 · 변조한 백업은 복원 거부</p></div></div>
</div>
<p class="op-boundary">동작하는 경로는 확인했고, 장애·복원 전체 검증은 다음 단계입니다.</p>

</OperatorSlide>

<!--
[40초 · 3 · 검증 근거]
현재까지 직접 확인한 결과입니다. 첫째, 10월 20일 기준 Kind E2E 테스트 spec 27개가 통과했습니다. S00부터 S15까지 필수 시나리오 16개를 모두 통과했다는 뜻은 아닙니다.

둘째, k3s VM에서 접속과 SQL, 롤아웃 전후 기존 데이터와 RW/RO 동작을 확인했습니다. 셋째, 로드맵에서 2~4주차 목표로 잡은 백업 복원 초기 시험을 10월 25일 VM에서 일곱 번 했습니다. 다섯 번 통과했고, 두 번은 데이터 확인을 마친 뒤 DB 세션이 끊겨 판정을 보류했습니다. 세션이 끊긴 원인은 아직 찾는 중입니다. 백업 파일을 일부러 변조했을 때는 복원을 거부했습니다. 다만 이 결과를 어떤 장애에서도 복구된다는 증거로 보지는 않겠습니다.
-->

---

<OperatorSlide section="3 · 다음 검증" index="12" total="18" source="v0.1 필수 안전 검증" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">다음 시험은 실패하는 순간을 겨냥합니다</h1>
<div class="op-gates">
  <div><span>01 · SAFE WRITES</span><b>master 불확실·네트워크 분할</b><p>쓰기 성공을 허용하지 않아야 할 순간에 실제 SQL 요청이 차단되는가?</p></div>
  <div><span>02 · RECOVERY</span><b>장애 후 재합류·재구축</b><p>정상 멤버와 이미 커밋한 데이터를 덮어쓰지 않고 복귀하는가?</p></div>
  <div><span>03 · RESTORE</span><b>복원 반복·중단</b><p>여러 번 반복하거나 복원 도중 재시작돼도 데이터가 일치하는가?</p></div>
  <div><span>04 · REPRODUCE</span><b>스토리지·환경·문서 재현</b><p>정한 Kubernetes·스토리지(CSI) 구성에서 다른 사람도 동일한 결과를 얻는가?</p></div>
</div>
<p class="op-boundary">이 네 가지를 모두 통과해야 v0.1을 공개합니다.</p>

</OperatorSlide>

<!--
[40초 · 3 · 다음 검증]
이제 어떤 시험이 남았는지 말씀드리겠습니다. 가장 먼저 master가 불명확하거나 네트워크가 분리된 상황에서 실제 쓰기를 막는지 검증해야 합니다. 그다음 손상된 멤버가 다시 합류하거나 재구축할 때 기존 정상 데이터를 지키는지 확인합니다.

앞서 말씀드린 대로 백업을 새 클러스터로 복원하는 시험은 처음 통과했습니다. 남은 일은 세션이 끊긴 원인을 찾고, 더 많은 조건에서 반복해 보는 것입니다. 마지막으로 Kubernetes와 CSI 구성을 고정하고 다른 메인테이너가 문서대로 같은 결과를 낼 수 있어야 합니다. 이 조건을 모두 채워야 v0.1을 공개할 수 있습니다.
-->

---

<OperatorSlide section="3 · 12주 로드맵" index="13" total="18" source="개발 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">11월엔 한 번 완주, 12월엔 같은 조건으로 반복</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>기준 정하기</b><p>환경·시나리오 정리<br>단일 DB SQL 확인</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA와 실행 환경</b><p>3멤버·RW/RO<br>VM에서 실행<br>백업·복구 초기 시험</p></div><div><small>5–8주 · 11.02–11.29</small><b>장애·복구 시험</b><p>쓰기 차단·재합류<br>재구축·백업 복원<br>필수 시나리오 첫 통과 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>같은 후보 버전으로 반복</b><p>장애 반복·24시간 부하 목표<br>다른 사람이 문서대로 재현<br>문제 수정·배포 파일 정리</p></div></div><p class="op-boundary"><b>11.29</b> 필수 시나리오 첫 전체 통과 목표　→　<b>12.27</b> v0.1 공개 목표</p>

</OperatorSlide>

<!--
[40초 · 3 · 12주 로드맵]
일정은 10월 5일부터 12월 27일까지 12주로 잡았습니다. 첫 주에는 환경과 시나리오를 정하고 단일 DB에서 SQL을 확인합니다. 2주부터 4주는 3멤버 HA와 RW/RO, VM 실행 환경과 백업·복구 초기 시험입니다. 지금 보여드린 Kind와 VM 결과도 이 단계에서 확인한 것들입니다.

11월 말, 정확히는 11월 29일까지 필수 시나리오를 한 번씩은 전부 통과시키는 게 목표입니다. 쓰기 차단, 재합류, 재구축, 백업에서 새 클러스터로 복원하는 것까지 들어갑니다. 12월에는 같은 후보 버전으로 장애 시험을 반복하고, 24시간 부하 시험과 다른 사람의 문서 재현을 해보려고 합니다. 나온 문제를 고치고 12월 27일 공개를 목표로 합니다. 공개 여부는 이 시험 결과를 보고 판단하겠습니다.
-->

---

<OperatorSlide section="3 · 개발 방식" index="14" total="18" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">두 명이 만들지만, 혼자 통과시키지 않습니다</h1><div class="op-people"><div><p class="op-kicker">IMPLEMENTER · 이슈별 담당자</p><b>재현부터 근거까지 책임</b><p>문제 재현 → 코드 → 테스트 → 문서 → 실험 기록을 한 작업으로 묶습니다.</p></div><div><p class="op-kicker">REVIEWER · 다른 메인테이너</p><b>코드와 실행 결과를 교차 검증</b><p>변경과 증거를 확인하고, 공개 전에는 문서만 보고 설치·복구를 재현합니다.</p></div></div><p class="op-boundary"><b>작성자 ≠ 최종 검증자</b>　공유 VM의 장애 시험은 한 번에 하나씩 진행하고, 공개 여부는 함께 결정합니다.</p>

</OperatorSlide>

<!--
[25초 · 3 · 개발 방식]
저희 둘이 함께 개발합니다. 이슈마다 담당자를 정하고, 맡은 사람이 문제 재현부터 코드와 테스트, 문서, 실험 기록까지 준비합니다. 하지만 그 작업을 혼자 통과시키지는 않습니다. 다른 한 사람이 코드와 실험 결과를 다시 확인합니다.

HA와 백업·복구, 설치 문서도 같은 방식으로 진행합니다. VM 장애 시험은 같은 환경을 쓰기 때문에 한 번에 하나씩 합니다. 릴리스 전에는 다른 메인테이너가 문서만 보고 설치와 복구를 끝낼 수 있는지도 확인하겠습니다.
-->

---

<OperatorSlide class="op-compact" section="4 · v0.1 범위" index="15" total="18" source="v0.1 범위" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1은 기능 수보다 검증 가능한 범위로 자릅니다</h1><table class="op-comparison op-acceptance"><thead><tr><th>포함할 기능</th><th>어떻게 확인할지</th></tr></thead><tbody><tr><td>root 없이 실행·데이터 보존<br>3멤버 HA·RW/RO</td><td>SQL을 실행하고 역할·커밋·데이터 확인</td></tr><tr><td>장애·쓰기 격리<br>재합류·재구축</td><td>Pod/VM/Broker/Operator 장애 뒤 상태와 데이터 확인</td></tr><tr><td>백업<br>새 클러스터 복원</td><td>백업으로 새 클러스터를 만들어 데이터 비교</td></tr><tr><td>볼륨 보존·Instance Manager 인증<br>노드 점검 중 보호·상태 지표</td><td>필수 시나리오 시험과 설치·운영·복구 문서 재현</td></tr></tbody></table><p class="op-boundary"><b>함께 공개</b>　이미지·설치 매니페스트·지원 환경표·운영 문서·시험 결과</p><p class="op-caption">지원 범위: CUBRID 11.4.x · amd64 · Kubernetes·스토리지 한 구성 · 실험 버전</p>

</OperatorSlide>

<!--
[40초 · 4 · v0.1 범위]
v0.1에서는 환경 하나를 정해서 설치부터 복구까지 확인하겠습니다. 3멤버 HA와 RW/RO에서 SQL을 실행하고, 장애를 낸 뒤 데이터와 역할을 확인합니다. 재합류와 재구축에서는 정상 데이터를 덮어쓰지 않아야 합니다. 백업으로 새 클러스터를 만들었을 때는 미리 준비한 데이터와 맞는지 비교합니다. 보존 정책과 Instance Manager 인증, 노드 점검 중 보호 정책, 상태와 지표도 확인해야 합니다.

이미지와 설치 매니페스트, 지원 환경표, 운영 문서와 시험 결과를 함께 공개하려고 합니다. CUBRID 11.4.x와 amd64, Kubernetes와 CSI 한 구성이 기준입니다. 현재 VM은 local-path여서 CSI 시험은 따로 해야 합니다. 첫 버전은 experimental입니다. Instance Manager 인증과는 별개로, 현재 DBA 암호는 비어 있고 통신도 암호화되지 않습니다. 호환 업데이트와 disk-full도 조건부로 남겨두었습니다.
-->

---

<OperatorSlide section="4 · 이후 방향" index="16" total="18" source="v0.1 이후 계획" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">v0.1 이후는 확장보다 피드백 순서입니다</h1><div class="op-release"><div><h3>먼저, 써보면서 고치기</h3><ul class="op-list"><li><b>로그와 진단부터 손보기</b><small>반복되는 문제와 복구 절차 정리</small></li><li><b>실제로 쓰려면 필요한 기능</b><small>DB 인증·TLS·호환 업데이트</small></li></ul></div><div><h3>그다음, 지원 환경 늘리기</h3><ul class="op-list"><li><b>Kubernetes·CSI 조합 추가</b><small>조합마다 장애·복구 시험</small></li><li><b>arm64·여러 가용영역</b><small>지원 가능한지 별도로 확인</small></li></ul></div><div><h3>시간이 더 필요한 일</h3><ul class="op-list"><li><b>CUBRID 버전 변경</b><small>데이터 호환·중단·되돌리는 방법</small></li><li><b>복제 구성 추가</b><small>master로 승격되지 않는 읽기 복제본 등</small></li></ul></div></div><p class="op-boundary">v0.1을 먼저 검증하고, 사용자들이 어디에서 불편한지 본 뒤 다음 우선순위를 정하려고 합니다.</p>

</OperatorSlide>

<!--
[20초 · 4 · 이후 방향]
첫 버전을 내면 써보면서 불편한 곳부터 고치겠습니다. 로그와 복구 절차, DB 인증과 TLS가 먼저입니다.

그다음 Kubernetes와 CSI 조합을 하나씩 늘리고 조합마다 장애와 복구를 다시 시험하겠습니다. 후속 버전과 날짜는 아직 정하지 않았습니다.
-->

---

<OperatorSlide section="Closing · 함께 검증" index="17" total="18" source="의견·협력 요청" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">세 가지를 여쭙고 싶습니다</h1><ol class="op-questions op-big"><li>최근 장애에서 복구됐다고 판단하기 전에, 무엇부터 확인하셨나요?</li><li>첫 지원으로 원하시는 Kubernetes CSI 드라이버는 무엇인가요?</li><li>12월에 설치·복구 문서를 먼저 따라 해 봐 주실 수 있을까요?</li></ol>

</OperatorSlide>

<!--
[25초 · Closing · 함께 검증]
마지막으로 세 가지를 여쭙고 싶습니다. 최근 장애에서 복구됐다고 판단하기 전에 무엇부터 확인하셨는지, 그리고 v0.1이 처음 지원했으면 하는 Kubernetes CSI 드라이버가 무엇인지 듣고 싶습니다. 그 환경에서 장애 시험을 할 때 주의할 점도 알려 주시면 좋겠습니다.

그리고 12월에 설치·복구 문서를 먼저 따라 해 보고 막히는 곳을 알려 주실 분이 계시면 좋겠습니다.
-->

---

<OperatorSlide section="Q&amp;A · 질의응답" index="18" total="18" source="예상 질문" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div></div>

</OperatorSlide>

<!--
[5초 · Q&A · 질의응답]
감사합니다. 질문 받겠습니다.
-->
