---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="Opening · 프로젝트 소개" index="01" total="18" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID Kubernetes<br>Operator</h1><p class="op-lead">설치부터 장애 후 복구 확인까지,<br>CUBRID 운영을 Kubernetes 흐름으로 묶고 있습니다.</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div><p class="op-caption">첫 버전은 12월 27일 공개를 목표로 하고 있습니다.</p></div>

</OperatorSlide>

<!--
[20초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저희는 관계형 DBMS인 CUBRID를 Kubernetes에서 관리하는 Operator를 만들고 있습니다. 설치만 자동화하는 것이 아니라, 장애가 난 뒤 정말 복구됐는지 확인하는 과정까지 운영 흐름으로 묶는 것이 목표입니다.

이번 시즌에는 환경 하나를 정해서 직접 설치하고, 장애를 내고, 복구되는 것까지 확인한 v0.1을 내려고 합니다. 먼저 오늘 어떤 순서로 말씀드릴지 짧게 보여드리겠습니다.
-->

---

<OperatorSlide class="op-compact" section="Agenda · 오늘의 흐름" index="02" total="18" source="발표 구성" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/README.md">

<h1 class="op-title">오늘은 네 가지만<br>말씀드리겠습니다</h1><div class="op-agenda"><div><span>01</span><b>왜 필요한가</b><p>Pod 복구와 DB 복구는 왜 다른가</p></div><div><span>02</span><b>어떻게 풀까</b><p>Operator · CUBRID HA · IM의 역할</p></div><div><span>03</span><b>어디까지 왔나</b><p>지금 확인한 것과 아직 남은 리스크</p></div><div><span>04</span><b>어디까지 내놓을까</b><p>12주 계획과 v0.1 공개 범위</p></div></div><p class="op-boundary">마지막에는 실제 운영 경험과 함께 검증해보고 싶은 세 가지를 여쭙겠습니다.</p>

</OperatorSlide>

<!--
[15초 · Agenda · 오늘의 흐름]
오늘은 네 가지 순서로 말씀드리겠습니다. 먼저 왜 Kubernetes에서 Pod가 살아나는 것만으로는 충분하지 않은지, 그 다음 이 문제를 어떤 구조로 풀고 있는지 설명드리겠습니다. 그리고 현재까지 어디까지 확인했고 무엇이 아직 남아 있는지, 마지막으로 12월 v0.1에서 어디까지 공개할지를 말씀드리겠습니다.
-->

---

<OperatorSlide section="1 · 문제" index="03" total="18" source="문제와 사용자" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">Pod가 살아났다고<br>DB가 복구된 건 아닙니다</h1><div class="op-two"><div class="op-stack"><p class="op-kicker">DB 멤버에 장애가 났다면</p><ul class="op-list"><li><b>Pod와 볼륨부터 확인</b><small>플랫폼 팀이 보는 Kubernetes 상태</small></li><li><b>DB 안쪽도 확인</b><small>DB 운영자가 보는 역할·복제·데이터</small></li></ul></div><div class="op-stack"><p class="op-kicker">복구됐다고 보기 전에</p><ul class="op-list"><li><b>지금 master가 누구인지</b><small>어느 멤버가 쓰기를 받는가?</small></li><li><b>커밋한 데이터가 남았는지</b><small>기존 행과 새로 쓴 행이 보이는가?</small></li><li><b>실제 접속도 잘되는지</b><small>RW로 쓰고 RO로 읽을 수 있는가?</small></li></ul></div></div><p class="op-caption">이 일을 맡는 CUBRID DB 운영자와 Kubernetes 플랫폼 팀을 먼저 생각하고 있습니다.</p>

</OperatorSlide>

<!--
[35초 · 1 · 문제]
DB가 있던 노드에 장애가 나서 Pod가 다시 떴다고 해보겠습니다. Pod가 Ready이고 볼륨도 붙었습니다. 그런데 그것만 보고 DB도 복구됐다고 말할 수 있을까요?

지금 master가 누구인지, 커밋한 행이 남아 있는지, RW로 쓴 행이 RO에서도 보이고, RO 쓰기는 거부되는지도 봐야 합니다. 플랫폼 팀은 Pod와 볼륨을 보고, DB 운영자는 역할과 복제, 데이터를 봅니다. 두 쪽을 함께 확인해야 하는 일입니다. 저희는 우선 이런 일을 맡는 운영자와 플랫폼 팀을 생각하고 있습니다. 현장에서 어떤 확인이 가장 번거로운지도 더 들어보고 싶습니다.
-->

---

<OperatorSlide section="1 · 장애 시나리오" index="04" total="18" source="복구 판단 기준" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">장애가 나면 운영자는<br>네 가지 답을 기다립니다</h1>
<p class="op-kicker">예시: 실행 중이던 master 멤버의 Pod가 사라졌다면?</p>
<div class="op-steps">
  <div><span>01</span><b>Pod가 다시 떴나요?</b><small>재스케줄링·PVC 연결 확인</small></div>
  <div><span>02</span><b>누가 master인가요?</b><small>멤버별 역할과 합의된 상태 확인</small></div>
  <div><span>03</span><b>쓰기·읽기가 되나요?</b><small>RW / RO 경로에서 실제 SQL 실행</small></div>
  <div><span>04</span><b>데이터가 남았나요?</b><small>장애 전 커밋한 행과 새 행 비교</small></div>
</div>
<p class="op-boundary"><b>핵심</b>　①은 Kubernetes가 확인해 줍니다. ②–④는 데이터베이스를 이해해야 답할 수 있습니다.</p>
<p class="op-caption">실제 고객 장애 기록이 아닌, 검증해야 할 상황을 단순화한 예시입니다.</p>

</OperatorSlide>

<!--
[35초 · 1 · 장애 시나리오]
가령 운영 중 master Pod가 사라졌다가 다시 뜬 상황을 생각해 보겠습니다. 플랫폼 관점에서는 Pod와 볼륨 복구가 첫 관문입니다. 그러나 DB가 정상이라는 결론을 내려면 새 master 역할, 실제 접속, 장애 이전 데이터 보존까지 확인해야 합니다.

이 예시를 넣은 이유는 Kubernetes의 자동 재시작을 데이터의 정상 복구와 동일하게 말하지 않기 위해서입니다. 무엇을 검사해야 복구됐다고 판단할지 자체가 이번 프로젝트의 핵심입니다.
-->

---

<OperatorSlide section="1 · 초기 사용자" index="05" total="18" source="문제·사용자 가설" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">두 팀이 같은 장애를<br>서로 다른 화면에서 봅니다</h1>
<div class="op-personas">
  <div><span>PLATFORM ENGINEER</span><h3>Kubernetes 플랫폼 담당자</h3><p>Pod·노드·스토리지 상태를 보고<br>재배치와 리소스 이상을 확인합니다.</p><strong>질문: 서비스가 다시 뜬 다음엔?</strong></div>
  <div><span>DB OPERATOR</span><h3>CUBRID 데이터베이스 담당자</h3><p>HA 역할·복제·접속·데이터를 보고<br>업무 복귀 가능 여부를 판단합니다.</p><strong>질문: DB도 안전하게 돌아왔나?</strong></div>
</div>
<div class="op-bridge"><b>우리가 잇고 싶은 부분</b><span>플랫폼 상태 ↔ DB 상태 ↔ 작업 결과를 같은 운영 흐름에서 확인하기</span></div>
<p class="op-caption">초기 대상 사용자 가설입니다. 실제 현장의 우선순위는 이번 검증에서 더 확인하려고 합니다.</p>

</OperatorSlide>

<!--
[30초 · 1 · 초기 사용자]
누구를 위한 도구인지도 분명히 하고 싶습니다. 먼저 Kubernetes 플랫폼 담당자는 Pod와 볼륨 같은 인프라 상태를 잘 봅니다. CUBRID 담당자는 master와 replica 역할, 실제 SQL 결과와 데이터를 확인합니다. 문제가 생기면 같은 장애를 다른 화면에서 보고 대화해야 합니다.

저희는 두 팀을 첫 사용자로 가정하고 있습니다. 인터뷰로 불편의 우선순위를 확정한 것은 아니며, 그래서 오늘 운영 경험을 듣고 싶습니다.
-->

---

<OperatorSlide section="1 · 현재 대안" index="06" total="18" source="공식 구현·비교 범위" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">이미 있는 도구도<br>많은 일을 해냅니다</h1>
<div class="op-alternatives">
  <div><span>01 · KUBERNETES</span><h3>StatefulSet</h3><p>Pod와 저장소의 원하는 구성을 유지하고, 장애 시 실행 환경을 복구합니다.</p></div>
  <div><span>02 · CUBRID</span><h3>기본 HA 기능</h3><p>DB 복제와 master 역할 전환은 CUBRID 엔진의 책임입니다.</p></div>
  <div><span>03 · OPEN SOURCE</span><h3>공식 CUBRID Operator</h3><p>HA 상태 조회, 스토리지, 예약 백업 등 이미 중요한 기능을 제공합니다.</p></div>
</div>
<p class="op-boundary"><b>그래서 우리 질문은</b>　“새 Operator가 필요한가?”보다 “애매한 장애와 끊긴 작업을 어떻게 확인할까?”입니다.</p>

</OperatorSlide>

<!--
[30초 · 1 · 현재 대안]
여기서 기존 프로젝트를 못한다고 설명하면 정확하지 않습니다. Kubernetes StatefulSet은 Pod와 PVC를 다루고, CUBRID는 HA와 역할 전환을 맡습니다. 공식 CUBRID Operator도 HA 조회, 스토리지, 예약 백업을 이미 제공하고 있습니다.

저희가 고른 초점은 데이터베이스 상황이 애매할 때 결론을 서두르지 않는 것, 그리고 오래 걸리는 운영 작업의 요청과 종료 결과를 추적하는 것입니다. 이것이 기존 프로젝트와 실제로 어느 정도 차이를 만드는지는 장애 시험을 통해 검증해야 합니다.
-->

---

<OperatorSlide class="op-compact" section="1 · 기존 방식 비교" index="07" total="18" source="공식 Operator·소스 비교" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">차이는 ‘모르는 상태’를<br>어떻게 다루느냐입니다</h1><table class="op-comparison"><thead><tr><th>비교할 부분</th><th>공식 Operator</th><th>이번 프로젝트</th></tr></thead><tbody><tr><td>HA 상태 조회</td><td>처음 성공한 CMS 응답의 노드 정보</td><td>각 멤버의 최신 상태 비교<br>응답이 없거나 모순되면 master 미확정</td></tr><tr><td>오래 걸리는 작업</td><td>예약 백업을 Pod exec로 실행<br>백업 상태 기록</td><td>IM API로 요청·작업 ID를 PVC에 기록<br>중단된 작업은 실패로 기록</td></tr><tr><td>백업 설정</td><td>대상 Pod·스크립트·저장소 지정</td><td>대상·요청 ID 보관<br>복원할 파일 목록·체크섬 확인</td></tr></tbody></table><p class="op-caption">공식 Operator도 HA·스토리지·예약 백업을 지원합니다. 확인한 소스 버전을 기준으로 비교했습니다.</p><p class="op-boundary"><b>핵심 원칙</b>　확신할 수 없으면 master를 추정하지 않고, 실제 SQL과 데이터도 별도로 검사합니다.</p>

</OperatorSlide>

<!--
[40초 · 1 · 기존 방식 비교]
CUBRID에는 이미 HA가 있고 공식 Operator도 있습니다. 공식 Operator도 HA 상태를 보고 스토리지와 예약 백업을 관리합니다. 저희가 특히 집중하는 부분은 응답이 안 오거나 작업이 중간에 끊겼을 때, 모르는 상태를 억지로 정상이라고 만들지 않는 것입니다.

표는 확인한 소스 기준입니다. CMS는 CUBRID Manager Server입니다. 공식 구현은 처음 성공한 CMS 응답의 노드 정보를 쓰고, 저희 쪽은 각 멤버의 최신 상태를 받아 비교합니다. 응답이 없거나 역할 정보가 서로 모순되면 master를 확정하지 않습니다. 백업 같은 작업은 Instance Manager, 줄여서 IM에 HTTP로 요청하고 작업 ID를 PVC에 기록합니다. IM이 다시 시작했을 때 끝나지 않은 작업은 실패로 남깁니다. 작업이 자동으로 이어진다는 뜻은 아닙니다.

실제 장애에서 어느 쪽이 더 안정적인지는 아직 비교하지 못했습니다. 두 쪽 모두 포트 검사를 쓰기 때문에 SQL과 데이터도 따로 확인합니다.
-->

---

<OperatorSlide section="2 · 접근" index="08" total="18" source="10월 20일 시험 결과" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Operator는 결정을 대신하기보다,<br>상태와 작업을 이어줍니다</h1><div class="op-path"><div class="op-node project">YAML로 설정<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">DB 상태 조회<small>역할·복제·접속</small></div><div class="op-arrow">→</div><div class="op-node project">작업 요청·조회<small>작업 ID·진행·결과</small></div><div class="op-arrow">→</div><div class="op-node">상태 갱신<small>Conditions·Events</small></div></div><div class="op-principles"><div><b>역할은 임의로 바꾸지 않기</b><small>HA 전환은 CUBRID가 결정</small></div><div><b>작업 기록은 지우지 않기</b><small>ID·진행·종료 결과를 PVC에 보관</small></div><div><b>불확실하면 드러내기</b><small>상태와 SQL 결과를 따로 검증</small></div></div><p class="op-caption">DB 상태와 작업 결과를 Kubernetes에서 읽을 수 있게 만드는 것이 목표입니다.</p>

</OperatorSlide>

<!--
[35초 · 2 · 접근]
사용자는 YAML에 원하는 구성을 적습니다. Operator가 DB 상태를 읽고 필요한 작업을 요청한 뒤, 진행 상황과 결과를 갱신합니다. 백업처럼 오래 걸리는 작업은 ID로 다시 찾아볼 수 있게 합니다. 작업 기록을 읽을 수 없으면 새 작업을 임의로 시작하지 않게 하는 것도 중요한 부분입니다.

지금까지는 Kind 테스트 27개가 통과했고, VM에서도 기존 행이 남아 있는 것과 RW로 쓴 데이터를 RO에서 읽는 것, RO 쓰기가 거부되는 것을 확인했습니다. VM 전원 장애, 네트워크 분할, 재합류와 재구축, CSI 시험은 더 해야 합니다. 백업 복원 결과는 뒤에서 따로 말씀드리겠습니다.
-->

---

<OperatorSlide class="op-compact" section="2 · 구조" index="09" total="18" source="구성도" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID는 HA를,<br>Operator는 관찰과 조정을 맡습니다</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>상태 조회·리소스 관리</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes 리소스<small>StatefulSet·Service·PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID HA가 복제와 master 전환을 담당</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>멤버 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 2 · PVC</small></div></div></div><div class="op-stack"><div class="op-node">Broker<small>DB와 분리된 RW / RO 접속</small></div><div class="op-node storage">백업 저장소<small>S3 호환 · 초기 복사·백업·복원</small></div></div></div><p class="op-caption">IM은 DB 컨테이너 안에서 HTTP API로 작업을 받고 PVC에 기록합니다. 누가 master가 될지는 CUBRID가 정합니다.</p>

</OperatorSlide>

<!--
[40초 · 2 · 구조]
구성은 크게 Operator, DB 멤버와 IM, Broker, 백업 저장소입니다. Operator는 Kubernetes API를 통해 StatefulSet과 Service, PVC를 관리합니다. 각 DB 컨테이너 안에는 CUBRID와 IM이 같이 들어갑니다. IM은 별도 sidecar가 아니라 DB 컨테이너 안에서 실행되는 supervisor입니다.

DB를 시작하거나 백업 같은 로컬 작업을 할 때 IM의 인증된 HTTP API를 사용합니다. IM은 작업 ID와 상태를 PVC에 남깁니다. Broker는 DB와 따로 두고 RW와 RO 접속을 받습니다. 초기 데이터 복사와 백업·복원 파일은 S3 호환 저장소를 거칩니다.

복제와 master 전환은 CUBRID가 맡습니다. 멤버 0을 항상 master로 두는 것도 아닙니다. Operator가 임의로 master를 승격하거나, 갈라진 데이터 중 하나를 골라 덮어쓰지는 않습니다.
-->

---

<OperatorSlide class="op-compact" section="2 · 데이터·제어 흐름" index="10" total="18" source="SQL과 운영 요청" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL 경로와 운영 경로를<br>분리했습니다</h1><div class="op-stack"><p class="op-kicker">애플리케이션에서 SQL을 실행할 때</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">설정을 바꾸거나 DB 작업을 요청할 때</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">IM API<small>로컬 작업·작업 기록</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / PVC</div></div></div><p class="op-boundary"><b>master 장애 후 확인 순서</b><br>엔진 역할 전환 → IM에서 조회 → Operator 상태 갱신 → SQL·데이터 확인</p><p class="op-caption">네트워크가 갈라졌을 때의 쓰기 차단은 아직 남은 작업입니다.</p>

</OperatorSlide>

<!--
[35초 · 2 · 데이터·제어 흐름]
애플리케이션의 SQL은 위쪽 경로로 갑니다. RW나 RO Service에서 Broker를 거쳐 CUBRID로 들어갑니다. Operator는 SQL을 중계하지 않습니다. 아래쪽은 설정을 읽거나 DB 작업을 요청하는 경로입니다. Operator가 IM API를 호출하고 결과를 상태에 반영합니다.

master에 장애가 났을 때도 CUBRID의 역할 전환을 먼저 봅니다. IM에서 각 멤버를 조회하고, Operator 상태가 맞게 바뀌는지, SQL과 데이터가 실제로 맞는지 확인해야 합니다. 여기서 아직 남은 중요한 일이 쓰기 차단입니다. Kind에서는 master를 확정하지 못한 동안에도 RW 쓰기 요청에 성공 응답이 돌아왔습니다. 상태에 불명확하다고 적는 것만으로 쓰기가 막히지는 않았습니다. 네트워크가 갈라졌을 때의 쓰기 차단을 구현하고 실제 접속으로 확인해야 합니다.
-->

---

<OperatorSlide section="2 · 장애 대응 원칙" index="11" total="18" source="쓰기 격리 이슈·ADR" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">master를 모를 때는<br>성공보다 안전이 먼저입니다</h1>
<div class="op-safety">
  <div><span>현재 설계와 구현</span><h3>정보가 부족하면 master 미확정</h3><p>멤버 응답이 빠졌거나 역할 정보가 충돌하면, 한 노드를 임의로 master라고 표시하지 않습니다.</p><p class="op-mini">상태: 미확정으로 관측</p></div>
  <div><span>v0.1 필수 검증</span><h3>그동안 RW 쓰기도 막혀야 함</h3><p>잘못된 write 성공 응답을 막으려면 실제 Broker·SQL 경로에 쓰기 격리가 적용되는지 확인해야 합니다.</p><p class="op-mini">상태: 아직 검증/완료되지 않음</p></div>
</div>
<p class="op-boundary"><b>중요한 구분</b>　상태에 “모름”이라고 기록하는 것만으로 SQL 쓰기가 막히지는 않습니다.</p>
<p class="op-caption">Kind에서는 master 미확정 동안 RW 쓰기 성공이 관찰되었습니다. 격리 구현과 장애 시험이 남아 있습니다.</p>

</OperatorSlide>

<!--
[35초 · 2 · 장애 대응 원칙]
이 장은 아직 부족한 부분을 숨기지 않기 위해 넣었습니다. Operator는 각 멤버의 관측값이 충분하지 않으면 master를 미확정으로 둡니다. 그러나 그것은 상태 표시일 뿐, 실제 서비스의 쓰기 경로가 자동으로 막혔다는 뜻은 아닙니다.

10월에 기록한 Kind 시험에서도 master를 확정하지 못하는 동안 RW 쓰기 성공 응답이 나왔습니다. 그래서 쓰기 격리와 네트워크 분할 시험은 v0.1의 필수 조건입니다. 안전하다고 주장하기 전에 SQL로 확인해야 합니다.
-->

---

<OperatorSlide section="3 · 검증 근거" index="12" total="18" source="2026.10.20–25 실행 기록" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">실제로 확인한 결과는<br>여기까지입니다</h1>
<div class="op-evidence-list">
  <div><span class="op-evidence-number">27 / 27</span><div><b>Kind E2E 테스트 spec 통과</b><p>2026.10.20 실행 기준 · 테스트 spec 수이며 필수 복구 시나리오 완료 수는 아닙니다.</p></div></div>
  <div><span class="op-evidence-number">RW / RO</span><div><b>VM 접속과 롤아웃 후 기존 데이터 확인</b><p>k3s / CUBRID 11.4.6 · 기존 PVC·행 보존, RW 쓰기 / RO 읽기 / RO 쓰기 거부 확인 · VM 전원 장애 시험은 아님</p></div></div>
  <div><span class="op-evidence-number">5 / 7</span><div><b>VM에서 백업으로 새 클러스터 복원 통과</b><p>2026.10.25 실행 기준 · 나머지 2회는 세션 끊김(원인 조사 중, #238)으로 판정 보류 · 변조한 백업은 복원 거부</p></div></div>
</div>
<p class="op-boundary"><b>검증 범위</b>　동작한 일부 경로를 확인했습니다. 실제 장애·복원 전체가 통과했다는 뜻은 아닙니다.</p>

</OperatorSlide>

<!--
[40초 · 3 · 검증 근거]
현재까지 직접 확인한 결과입니다. 첫째, 10월 20일 기준 Kind E2E 테스트 spec 27개가 통과했습니다. S00부터 S15까지 필수 시나리오 16개를 모두 통과했다는 뜻은 아닙니다.

둘째, k3s VM에서 접속과 SQL, 롤아웃 전후 기존 데이터와 RW/RO 동작을 확인했습니다. 셋째, 로드맵에서 2~4주차 목표로 잡은 백업 복원 초기 시험을 10월 25일 VM에서 일곱 번 했습니다. 다섯 번 통과했고, 두 번은 데이터 확인을 마친 뒤 DB 세션이 끊겨 판정을 보류했습니다. 세션이 끊긴 원인은 아직 찾는 중입니다. 백업 파일을 일부러 변조했을 때는 복원을 거부했습니다. 다만 이 결과를 어떤 장애에서도 복구된다는 증거로 보지는 않겠습니다.
-->

---

<OperatorSlide section="3 · 다음 검증" index="13" total="18" source="v0.1 필수 안전 검증" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">다음 시험은<br>실패하는 순간을 겨냥합니다</h1>
<div class="op-gates">
  <div><span>01 · SAFE WRITES</span><b>master 불확실·네트워크 분할</b><p>쓰기 성공을 허용하지 않아야 할 순간에 실제 SQL 요청이 차단되는가?</p></div>
  <div><span>02 · RECOVERY</span><b>장애 후 재합류·재구축</b><p>정상 멤버와 이미 커밋한 데이터를 덮어쓰지 않고 복귀하는가?</p></div>
  <div><span>03 · RESTORE</span><b>복원 반복·중단</b><p>여러 번 반복하거나 복원 도중 재시작돼도 데이터가 일치하는가?</p></div>
  <div><span>04 · REPRODUCE</span><b>CSI·환경·문서 재현</b><p>정한 Kubernetes/CSI 구성에서 다른 사람도 동일한 결과를 얻는가?</p></div>
</div>
<p class="op-caption">Pod·VM·Broker·Operator 장애와 S00–S15 증거를 반복 가능한 시험 기록으로 남길 계획입니다.</p>

</OperatorSlide>

<!--
[40초 · 3 · 다음 검증]
이제 어떤 시험이 남았는지 말씀드리겠습니다. 가장 먼저 master가 불명확하거나 네트워크가 분리된 상황에서 실제 쓰기를 막는지 검증해야 합니다. 그다음 손상된 멤버가 다시 합류하거나 재구축할 때 기존 정상 데이터를 지키는지 확인합니다.

앞서 말씀드린 대로 백업을 새 클러스터로 복원하는 시험은 처음 통과했습니다. 남은 일은 세션이 끊긴 원인을 찾고, 더 많은 조건에서 반복해 보는 것입니다. 마지막으로 Kubernetes와 CSI 구성을 고정하고 다른 메인테이너가 문서대로 같은 결과를 낼 수 있어야 합니다. 이 조건을 모두 채워야 v0.1을 공개할 수 있습니다.
-->

---

<OperatorSlide section="3 · 12주 로드맵" index="14" total="18" source="개발 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">11월엔 끝까지 한 번,<br>12월엔 같은 조건으로 반복합니다</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>기준 정하기</b><p>환경·시나리오 정리<br>단일 DB SQL 확인</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA와 실행 환경</b><p>3멤버·RW/RO<br>VM에서 실행<br>백업·복구 초기 시험</p></div><div><small>5–8주 · 11.02–11.29</small><b>장애·복구 시험</b><p>쓰기 차단·재합류<br>재구축·백업 복원<br>S00–S15 첫 통과 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>같은 RC로 반복</b><p>장애 반복·24시간 부하 목표<br>다른 사람이 문서대로 재현<br>문제 수정·배포 파일 정리</p></div></div><p class="op-boundary"><b>11.29</b> 필수 시나리오 첫 전체 통과 목표　→　<b>12.27</b> v0.1 공개 목표</p><p class="op-caption">어떤 커밋·이미지·환경에서 시험했는지, SQL 결과와 함께 남깁니다.</p>

</OperatorSlide>

<!--
[40초 · 3 · 12주 로드맵]
일정은 10월 5일부터 12월 27일까지 12주로 잡았습니다. 첫 주에는 환경과 시나리오를 정하고 단일 DB에서 SQL을 확인합니다. 2주부터 4주는 3멤버 HA와 RW/RO, VM 실행 환경과 백업·복구 초기 시험입니다. 지금 보여드린 Kind와 VM 결과도 이 단계에서 확인한 것들입니다.

11월 말, 정확히는 11월 29일까지 필수 시나리오를 한 번씩은 전부 통과시키는 게 목표입니다. 쓰기 차단, 재합류, 재구축, 백업에서 새 클러스터로 복원하는 것까지 들어갑니다. 12월에는 같은 RC로 장애 시험을 반복하고, 24시간 부하 시험과 다른 사람의 문서 재현을 해보려고 합니다. 나온 문제를 고치고 12월 27일 공개를 목표로 합니다. 어떤 커밋과 이미지로 시험했는지, 환경과 SQL 결과도 같이 남기겠습니다. 공개 여부는 이 시험 결과를 보고 판단하겠습니다.
-->

---

<OperatorSlide section="3 · 개발 방식" index="15" total="18" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">두 명이 만들지만,<br>혼자 통과시키지 않습니다</h1><div class="op-people"><div><p class="op-kicker">IMPLEMENTER · 이슈별 담당자</p><b>재현부터 근거까지 책임</b><p>문제 재현 → 코드 → 테스트 → 문서 → 실험 기록을 한 작업으로 묶습니다.</p></div><div><p class="op-kicker">REVIEWER · 다른 메인테이너</p><b>코드와 실행 결과를 교차 검증</b><p>변경과 증거를 확인하고, 공개 전에는 문서만 보고 설치·복구를 재현합니다.</p></div></div><p class="op-boundary"><b>작성자 ≠ 최종 검증자</b>　공유 VM의 장애 시험은 한 번에 하나씩 진행하고, 공개 여부는 함께 결정합니다.</p><p class="op-caption">최영선(@yeongseon) · 백경준(@paikend) 공동 메인테이너. 고정 기능 담당이 아닌 이슈별 교차 리뷰입니다.</p>

</OperatorSlide>

<!--
[25초 · 3 · 개발 방식]
저희 둘이 함께 개발합니다. 이슈마다 담당자를 정하고, 맡은 사람이 문제 재현부터 코드와 테스트, 문서, 실험 기록까지 준비합니다. 하지만 그 작업을 혼자 통과시키지는 않습니다. 다른 한 사람이 코드와 실험 결과를 다시 확인합니다.

HA와 백업·복구, 설치 문서도 같은 방식으로 진행합니다. VM 장애 시험은 같은 환경을 쓰기 때문에 한 번에 하나씩 합니다. 릴리스 전에는 다른 메인테이너가 문서만 보고 설치와 복구를 끝낼 수 있는지도 확인하겠습니다.
-->

---

<OperatorSlide class="op-compact" section="4 · v0.1 범위" index="16" total="18" source="v0.1 범위" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1은 기능 수보다<br>검증 가능한 범위로 자릅니다</h1><table class="op-comparison op-acceptance"><thead><tr><th>포함할 기능</th><th>어떻게 확인할지</th></tr></thead><tbody><tr><td>비루트·영속 DB<br>3멤버 HA·RW/RO</td><td>SQL을 실행하고 역할·커밋·데이터 확인</td></tr><tr><td>장애·쓰기 격리<br>재합류·재구축</td><td>Pod/VM/Broker/Operator 장애 뒤 상태와 데이터 확인</td></tr><tr><td>백업<br>새 클러스터 복원</td><td>백업으로 새 클러스터를 만들어 데이터 비교</td></tr><tr><td>보존·IM 인증<br>중단 정책·관측</td><td>S00–S15 시험과 설치·운영·복구 문서 재현</td></tr></tbody></table><p class="op-boundary"><b>함께 공개</b>　이미지·설치 매니페스트·지원 환경표·운영 문서·시험 결과</p><p class="op-caption">CUBRID 11.4.x / amd64 / Kubernetes·CSI 한 구성 · experimental · 호환 업데이트·disk-full 조건부</p>

</OperatorSlide>

<!--
[40초 · 4 · v0.1 범위]
v0.1에서는 환경 하나를 정해서 설치부터 복구까지 확인하겠습니다. 3멤버 HA와 RW/RO에서 SQL을 실행하고, 장애를 낸 뒤 데이터와 역할을 확인합니다. 재합류와 재구축에서는 정상 데이터를 덮어쓰지 않아야 합니다. 백업으로 새 클러스터를 만들었을 때는 미리 준비한 데이터와 맞는지 비교합니다. 보존 정책과 IM 인증, 노드 중단 정책, 상태와 지표도 확인해야 합니다.

이미지와 설치 매니페스트, 지원 환경표, 운영 문서와 시험 결과를 함께 공개하려고 합니다. CUBRID 11.4.x와 amd64, Kubernetes와 CSI 한 구성이 기준입니다. 현재 VM은 local-path여서 CSI 시험은 따로 해야 합니다. 첫 버전은 experimental입니다. IM API 인증과는 별개로, 현재 DBA 암호는 비어 있고 통신도 암호화되지 않습니다. 호환 업데이트와 disk-full도 조건부로 남겨두었습니다.
-->

---

<OperatorSlide section="4 · 이후 방향" index="17" total="18" source="v0.1 이후 계획" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">v0.1 이후는 확장보다<br>피드백 순서입니다</h1><div class="op-release"><div><h3>먼저, 써보면서 고치기</h3><ul class="op-list"><li><b>로그와 진단부터 손보기</b><small>반복되는 문제와 복구 절차 정리</small></li><li><b>실제로 쓰려면 필요한 기능</b><small>DB 인증·TLS·호환 업데이트</small></li></ul></div><div><h3>그다음, 지원 환경 늘리기</h3><ul class="op-list"><li><b>Kubernetes·CSI 조합 추가</b><small>조합마다 장애·복구 시험</small></li><li><b>arm64·여러 가용영역</b><small>지원 가능한지 별도로 확인</small></li></ul></div><div><h3>시간이 더 필요한 일</h3><ul class="op-list"><li><b>CUBRID 버전 변경</b><small>데이터 호환·중단·되돌리는 방법</small></li><li><b>복제 구성 추가</b><small>master로 승격되지 않는 읽기 복제본 등</small></li></ul></div></div><p class="op-boundary">v0.1을 먼저 검증하고, 사용자들이 어디에서 불편한지 본 뒤 다음 우선순위를 정하려고 합니다.</p><p class="op-caption">후속 버전과 일정은 아직 정하지 않았습니다. v0.1의 필수 작업부터 끝내겠습니다.</p>

</OperatorSlide>

<!--
[20초 · 4 · 이후 방향]
첫 버전을 내면 써보면서 불편한 곳부터 고치겠습니다. 로그와 복구 절차, DB 인증과 TLS가 먼저입니다.

그다음 Kubernetes와 CSI 조합을 하나씩 늘리고 조합마다 장애와 복구를 다시 시험하겠습니다. 후속 버전과 날짜는 아직 정하지 않았습니다.
-->

---

<OperatorSlide section="Closing · 함께 검증" index="18" total="18" source="의견·협력 요청" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">세 가지를 같이<br>검증해주시면 좋겠습니다</h1><ol class="op-questions"><li>최근 장애를 떠올리면,<br>복구됐다고 판단하기 전에 무엇부터 확인하셨나요?</li><li>함께 시험할 Kubernetes·CSI 조합과<br>스토리지·장애 시험의 주의점을 알려주실 수 있나요?</li><li>12월에 설치·복구 문서를 따라 해보고,<br>막히는 부분을 알려주실 분이 계실까요?</li></ol>

</OperatorSlide>

<!--
[25초 · Closing · 함께 검증]
마지막으로 운영 경험을 듣고 싶습니다. 최근 장애에서 무엇을 먼저 확인했고, 어떤 결과를 보고 복구됐다고 판단하셨는지 궁금합니다. 첫 시험 환경으로 쓸 Kubernetes와 CSI 조합, 스토리지나 장애 시험에서 주의할 점도 알려주시면 좋겠습니다.

12월에는 저희가 만든 설치·복구 문서를 다른 분이 따라 해봐 주셨으면 합니다. 어디에서 막히는지, 빠진 설명이 무엇인지 알려주시면 도움이 되겠습니다. 감사합니다.
-->
