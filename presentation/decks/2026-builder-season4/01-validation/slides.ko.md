---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="Opening · 프로젝트 소개" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">Kubernetes에서 CUBRID HA를 운영하고, 장애 뒤 복구까지 확인합니다</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[20초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저희는 관계형 DBMS인 CUBRID를 Kubernetes에서 관리하는 Operator를 만들고 있습니다. 지금은 3노드 CUBRID HA 클러스터의 배포와 상태 확인까지 구현했고, 장애 뒤 복구 검증은 진행 중입니다. 설치에서 끝나지 않고, 장애가 난 뒤 정말 복구됐는지 확인하는 과정까지 운영 흐름으로 묶는 것이 목표입니다.

이번 시즌에는 환경 하나를 정해서 직접 설치하고, 장애를 내고, 복구되는 것까지 확인한 v0.1 공개를 목표로 합니다. 먼저 이 Operator가 무엇인지부터 말씀드리겠습니다.
-->

---

<OperatorSlide class="op-compact" section="Agenda · 발표 순서" source="발표 구성" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/README.md">

<h1 class="op-title">발표 순서</h1><div class="op-agenda"><div><span>01</span><b>프로젝트·팀 소개</b><p>프로젝트 목표 · 공동 메인테이너</p></div><div><span>02</span><b>해결하려는 문제</b><p>Pod 복구와 DB 복구의 차이 · 대상 사용자</p></div><div><span>03</span><b>기존 방식의 한계</b><p>공식 CUBRID Operator와 차이</p></div><div><span>04</span><b>제안하는 해결 방법</b><p>네 가지 확인 · 안전 원칙 · 확인한 결과</p></div><div><span>05</span><b>아키텍처 초안</b><p>연동 플랫폼 · 구성 요소 · 데이터 처리 과정</p></div><div><span>06</span><b>로드맵과 첫 버전</b><p>12주 계획 · 팀 역할 · v0.1 범위 · 이후 방향</p></div></div>

</OperatorSlide>

<!--
[15초 · Agenda · 발표 순서]
오늘은 공지된 여섯 항목 순서로 말씀드리겠습니다. 프로젝트와 팀, 해결하려는 문제, 기존 방식의 한계, 저희의 해결 방법, 아키텍처 초안, 그리고 12주 로드맵과 첫 버전 범위입니다.
-->

---

<OperatorSlide section="01 · 문제와 목표">

<ChapterDivider number="01" title="문제와 목표" subtitle="Kubernetes가 복구한 Pod와 실제 DB 복구는 다릅니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 문제와 목표]
이 페이지는 다음 주제를 알리는 시각적 전환입니다. 별도 설명을 추가하지 않고 바로 다음 장으로 이동합니다.
-->

---

<OperatorSlide class="op-compact" section="01 · 프로젝트 소개" source="Operator README·검증 기록" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md">

<h1 class="op-title">Kubernetes에서 CUBRID HA를 안전하게 운영하는 Operator</h1><p class="op-lead">설치 자동화에서 끝나지 않고, 장애 뒤 DB가 정말 복구됐는지까지 확인하는 것이 목표입니다.</p><div class="op-goals"><div><span>01</span><b>선언형 설치</b><p>YAML 하나로 3노드 CUBRID HA 클러스터와 RW/RO 접속을 구성</p></div><div><span>02</span><b>DB를 아는 상태 판단</b><p>노드마다 HA 역할을 확인하고, 확실하지 않으면 “미확정”으로 남김</p></div><div><span>03</span><b>추적되는 백업·복원</b><p>작업을 ID로 기록하고, 복원 전에 파일 목록과 체크섬을 확인</p></div><div><span>04</span><b>SQL로 확인하는 복구</b><p>Pod 상태가 아니라 실제 쓰기·읽기와 데이터로 복구를 판단</p></div></div><p class="op-caption">실험 단계 프로젝트로 운영 환경용이 아닙니다 · 공식 CUBRID Operator를 대체하지 않습니다 · 진행 상황은 10쪽</p>

</OperatorSlide>

<!--
[40초 · 01 · 프로젝트 소개]
CUBRID Kubernetes Operator는 Kubernetes에서 CUBRID HA 클러스터를 안전하게 운영하는 것을 목표로 하는 실험 단계의 Operator입니다. 설치를 자동화하는 데서 끝나지 않고, 장애 뒤 DB가 정말 복구됐는지까지 확인하는 운영 흐름을 만들려고 합니다.

목표는 네 가지입니다. 첫째, YAML 하나로 3노드 CUBRID HA 클러스터와 쓰기·읽기 접속을 구성합니다. 여기서 노드는 Kubernetes 워커 노드가 아니라 CUBRID HA를 이루는 DB 노드입니다. 둘째, 노드마다 HA 역할을 확인하고, 확실하지 않으면 추정하지 않고 미확정으로 남깁니다. 셋째, 백업과 복원을 작업 ID로 추적하고 복원 전에 파일과 체크섬을 확인합니다. 넷째, 복구는 Pod 상태가 아니라 실제 SQL과 데이터로 판단합니다. 지금 어디까지 확인했는지는 뒤에서 결과로 보여드리겠습니다.
-->

---

<OperatorSlide section="02 · 문제와 대상" source="문제·사용자 가설" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">Pod가 살아났다고 DB가 복구된 건 아닙니다</h1><p class="op-kicker">Pod 재시작과 볼륨 연결만으로 DB 복구를 확인할 수는 없습니다</p><div class="op-scene"><div class="op-actor"><div class="op-bubble">Pod는 다시 떴어요.<br>이제 된 거죠?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>Kubernetes 플랫폼 담당자</b></div><div class="op-incident"><span>⚡</span><b>같은 장애</b></div><div class="op-actor op-actor-db"><div class="op-bubble">master는 누구죠?<br>데이터는 괜찮나요?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>CUBRID DB 담당자</b></div></div><p class="op-boundary">두 담당자가 같은 기준으로 “복구됐다”고 판단할 수 있게 하는 것이 목표입니다.</p>

</OperatorSlide>

<!--
[40초 · 02 · 문제와 대상]
왜 이게 필요한지 말씀드리겠습니다. Pod가 죽으면 Kubernetes가 다시 띄우고 볼륨을 연결해 줄 수 있습니다. 하지만 Pod 재시작과 볼륨 연결만으로 DB가 복구됐다고 확인할 수는 없습니다. 지금 master가 누구인지, 쓰고 읽을 수 있는지, 장애 전 데이터가 남았는지까지 확인해야 합니다.

그래서 같은 장애를 두 팀이 다르게 봅니다. Kubernetes 플랫폼 담당자는 Pod가 다시 떴으니 됐다고 보고, CUBRID 담당자는 master와 데이터를 묻습니다. 저희는 이 두 팀을 첫 사용자로 가정합니다. 인터뷰로 확정한 것은 아니어서 오늘 운영 경험을 듣고 싶습니다. 두 사람이 같은 화면에서 복구를 확인할 수 있게 하는 것이 목표입니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 기존 방식의 한계" source="공식·CUBRID Lab 아키텍처 비교" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">같은 CUBRID HA, 다른 관리·접속 구조</h1>
<p class="op-kicker">두 Operator 모두 master 선출과 복제는 CUBRID 자체 HA에 맡깁니다.</p>

<div class="op-compare-layout">
  <section class="op-compare-side">
    <header class="op-compare-side-header"><b>공식 CUBRID Operator</b><span>DB Pod 안에서 관리·접속</span></header>
    <svg class="op-compare-svg" viewBox="0 0 460 265" role="img" aria-label="공식 Operator: Application에서 Broker Service로 연결하고 DB Pod 내부 Broker를 통해 CUBRID DB에 SQL을 보냅니다. Operator는 같은 DB Pod 안의 CMS API를 통해 관리합니다. DB, CMS, Broker는 같은 컨테이너 안에 있습니다.">
      <defs>
        <marker id="op-cmp-off-sql" markerWidth="6" markerHeight="6" refX="5.6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#1f4e8c"/></marker>
        <marker id="op-cmp-off-ctl" markerWidth="6" markerHeight="6" refX="5.6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#5b6b82"/></marker>
      </defs>
      <rect class="op-compare-sqlbox" x="18" y="5" width="160" height="41" rx="8"/>
      <text x="98" y="23" text-anchor="middle">Application</text><text class="op-compare-small" x="98" y="38" text-anchor="middle">SQL 요청</text>
      <rect class="op-compare-ctlbox" x="283" y="5" width="160" height="41" rx="8"/>
      <text x="363" y="23" text-anchor="middle">Operator</text><text class="op-compare-small" x="363" y="38" text-anchor="middle">CMS API · pods/exec</text>
      <rect class="op-compare-sqlbox" x="18" y="74" width="160" height="40" rx="8"/>
      <text x="98" y="92" text-anchor="middle">Broker Service</text><text class="op-compare-small" x="98" y="107" text-anchor="middle">애플리케이션 접속</text>
      <rect class="op-compare-pod" x="18" y="154" width="425" height="104" rx="10"/>
      <text class="op-compare-pod-title" x="184" y="179">DB Pod ×3</text>
      <rect class="op-compare-sqlbox" x="36" y="197" width="118" height="42" rx="7"/><text x="95" y="223" text-anchor="middle">Broker</text>
      <rect class="op-compare-dbbox" x="177" y="197" width="118" height="42" rx="7"/><text x="236" y="223" text-anchor="middle">CUBRID DB</text>
      <rect class="op-compare-ctlbox" x="316" y="197" width="111" height="42" rx="7"/><text x="371" y="223" text-anchor="middle">CMS</text>
      <path class="op-compare-sql-line" d="M98 46V71" marker-end="url(#op-cmp-off-sql)"/>
      <path class="op-compare-sql-line" d="M98 114V193" marker-end="url(#op-cmp-off-sql)"/>
      <path class="op-compare-sql-line" d="M154 218H173" marker-end="url(#op-cmp-off-sql)"/>
      <path class="op-compare-control-line" d="M363 46V193" marker-end="url(#op-cmp-off-ctl)"/>
    </svg>
  </section>
  <section class="op-compare-side op-compare-side-lab">
    <header class="op-compare-side-header"><b>CUBRID Lab Operator</b><span>DB 관리와 SQL 접속 분리</span></header>
    <svg class="op-compare-svg" viewBox="0 0 460 265" role="img" aria-label="CUBRID Lab Operator: Application에서 RW/RO Service를 거쳐 별도의 Broker Pod로 접속한 다음 DB Pod 안의 CUBRID DB에 SQL을 보냅니다. Operator는 DB와 같은 컨테이너의 Instance Manager API로 관리합니다.">
      <defs>
        <marker id="op-cmp-lab-sql" markerWidth="6" markerHeight="6" refX="5.6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#1f4e8c"/></marker>
        <marker id="op-cmp-lab-ctl" markerWidth="6" markerHeight="6" refX="5.6" refY="3" orient="auto"><path d="M0 0L6 3L0 6Z" fill="#5b6b82"/></marker>
      </defs>
      <rect class="op-compare-sqlbox" x="18" y="5" width="160" height="41" rx="8"/>
      <text x="98" y="23" text-anchor="middle">Application</text><text class="op-compare-small" x="98" y="38" text-anchor="middle">SQL 요청</text>
      <rect class="op-compare-ctlbox" x="283" y="5" width="160" height="41" rx="8"/>
      <text x="363" y="23" text-anchor="middle">Operator</text><text class="op-compare-small" x="363" y="38" text-anchor="middle">IM API</text>
      <rect class="op-compare-sqlbox" x="18" y="74" width="160" height="40" rx="8"/>
      <text x="98" y="92" text-anchor="middle">RW/RO Service</text><text class="op-compare-small" x="98" y="107" text-anchor="middle">애플리케이션 접속</text>
      <rect class="op-compare-pod" x="18" y="154" width="196" height="104" rx="10"/>
      <text class="op-compare-pod-title" x="116" y="179">Broker Pods</text>
      <rect class="op-compare-sqlbox" x="36" y="197" width="160" height="42" rx="7"/><text x="116" y="214" text-anchor="middle">RW Broker</text><text x="116" y="231" text-anchor="middle">RO Broker</text>
      <rect class="op-compare-pod" x="238" y="154" width="205" height="104" rx="10"/>
      <text class="op-compare-pod-title" x="252" y="179">DB Pod ×3</text>
      <rect class="op-compare-ctlbox" x="256" y="195" width="172" height="25" rx="6"/><text class="op-compare-node-text" x="342" y="212" text-anchor="middle">Instance Manager</text>
      <rect class="op-compare-dbbox" x="256" y="232" width="172" height="23" rx="6"/><text class="op-compare-node-text" x="342" y="248" text-anchor="middle">CUBRID DB</text>
      <path class="op-compare-sql-line" d="M98 46V71" marker-end="url(#op-cmp-lab-sql)"/>
      <path class="op-compare-sql-line" d="M98 114V193" marker-end="url(#op-cmp-lab-sql)"/>
      <path class="op-compare-sql-line" d="M196 219H225V244H252" marker-end="url(#op-cmp-lab-sql)"/>
      <path class="op-compare-control-line" d="M363 46V191" marker-end="url(#op-cmp-lab-ctl)"/>
    </svg>
  </section>
</div>
<div class="op-compare-takeaway"><b>차이점</b><span>공식: CMS + Broker가 DB Pod 내부</span><span>우리: IM은 DB Pod 내부, Broker는 별도 Pod</span></div>


</OperatorSlide>

<!--
[45초 · 03 · 기존 방식의 한계]
CUBRID에는 이미 공식 Operator가 있고, HA 상태 조회와 스토리지, 예약 백업을 제공합니다. 그래서 무엇을 다르게 설계했는지 구조로 비교하겠습니다.

왼쪽 공식 Operator는 각 DB Pod 안에서 CUBRID DB와 CMS, Broker가 함께 실행됩니다. Operator는 CMS API와 Pod 내부 명령 실행으로 DB를 관리하고, 애플리케이션은 DB Pod 안의 Broker를 거쳐 접속합니다.

오른쪽 저희 구조에서는 DB와 Instance Manager가 같은 컨테이너에 있지만, RW와 RO Broker는 별도의 Deployment에서 실행됩니다. Operator는 IM API로 각 DB의 상태를 조회하고 작업을 요청합니다. 각 멤버의 관측값을 비교하고, 관리 작업 ID도 볼륨에 기록합니다.

두 방식 모두 master 선출과 복제는 CUBRID HA가 담당합니다. 별도 IM이나 Broker 구조가 실제로 더 안정적인지는 아직 비교 검증하지 않았습니다.
-->

---

<OperatorSlide section="02 · 해결 방식과 설계">

<ChapterDivider number="02" title="해결 방식과 아키텍처" subtitle="무엇을 관찰하고, 어디까지 자동화할 것인가" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 해결 방식과 설계]
안전 원칙과 아키텍처를 연결하는 전환 페이지입니다. 별도 발화 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-compact" section="04 · 해결 방법" source="장애 시 확인 순서" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#12-failover-and-split-brain-model">

<h1 class="op-title">master Pod가 사라지면 네 가지를 확인합니다</h1><p class="op-kicker">예시: 실행 중인 master Pod가 사라졌다가 다시 뜬 경우 · 설계 기준</p><table class="op-comparison op-checks"><thead><tr><th>확인할 것</th><th>누가 답하나</th><th>무엇을 보나</th></tr></thead><tbody><tr><td>① Pod 가용성</td><td>Kubernetes</td><td>Pod가 다시 Ready인가 · 볼륨이 붙었나</td></tr><tr><td>② DB HA 상태</td><td>CUBRID HA가 전환<br>Operator가 기록</td><td>노드마다 역할을 조회해 비교<br>빠지거나 엇갈리면 “미확정”</td></tr><tr><td>③ SQL 접속</td><td>Broker</td><td>RW Broker가 새 master로 연결되나<br>RW 쓰기 · RO 읽기가 되나</td></tr><tr><td>④ 데이터</td><td>E2E 시험</td><td>장애 전에 커밋한 행이 남았나<br>Operator가 자동으로 확인하지는 않음</td></tr></tbody></table><p class="op-boundary"><b>핵심</b>　Pod 상태(①)에서 멈추지 않고 HA 역할·SQL 접속·데이터(②–④)까지 한 흐름으로 확인합니다.</p>

</OperatorSlide>

<!--
[45초 · 04 · 해결 방법]
저희의 해결 방법은 장애 뒤 확인할 것을 네 가지로 나눠 한 흐름으로 보는 것입니다. 실행 중인 master Pod가 사라졌다가 다시 뜬다고 해 보겠습니다. 첫째, Pod가 다시 Ready이고 볼륨이 붙었는지는 Kubernetes가 알려 줍니다. 하지만 Pod 상태만으로는 HA 역할이나 SQL 접속, 데이터까지는 알 수 없습니다.

둘째, master 전환은 CUBRID HA가 하고, Operator는 노드마다 역할을 조회해 비교합니다. 응답이 빠지거나 엇갈리면 master를 추정하지 않고 미확정으로 둡니다. 셋째, RW Broker가 새 master로 연결돼 쓰기와 읽기가 되는지 봅니다. 넷째, 장애 전에 커밋한 데이터가 남았는지는 지금은 E2E 시험에서 확인합니다. Operator가 데이터를 자동으로 검증한다는 뜻은 아닙니다.
-->

---

<OperatorSlide section="04 · 안전 원칙" source="쓰기 격리 이슈·ADR" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">master를 확신할 수 없으면 추정하지 않습니다</h1>
<div class="op-safety">
  <div><span>현재 설계와 구현</span><h3>정보가 부족하면 “미확정”으로 표시</h3><p>노드 응답이 빠졌거나 역할 정보가 충돌하면, 한 노드를 임의로 master로 표시하지 않습니다.</p><p class="op-mini">상태: 미확정으로 표시</p></div>
  <div><span>v0.1 필수 검증</span><h3>미확정인 동안 실제 SQL 쓰기 차단</h3><p>잘못된 쓰기 성공 응답을 막으려면, Broker를 거치는 실제 SQL 쓰기가 차단되는지 확인해야 합니다.</p><p class="op-mini">상태: 구현·검증 예정</p></div>
</div>
<p class="op-boundary"><b>중요한 구분</b>　상태에 “미확정”이라고 기록하는 것만으로 SQL 쓰기가 막히지는 않습니다.</p>

</OperatorSlide>

<!--
[35초 · 04 · 안전 원칙]
이 장은 아직 부족한 부분을 숨기지 않기 위해 넣었습니다. Operator는 각 노드의 관측값이 충분하지 않으면 master를 미확정으로 둡니다. 그러나 그것은 상태 표시일 뿐, 실제 서비스의 쓰기 경로가 자동으로 막혔다는 뜻은 아닙니다.

10월에 기록한 Kind 시험에서도 master를 확정하지 못하는 동안 RW 쓰기 성공 응답이 나왔습니다. 그래서 쓰기 격리와 네트워크 분할 시험은 v0.1의 필수 조건입니다. 안전하다고 주장하기 전에 SQL로 확인해야 합니다.
-->

---

<OperatorSlide section="04 · 확인한 결과" source="2026.10.20–25 실행 기록" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">지금까지 확인한 결과입니다</h1>
<div class="op-evidence-list">
  <div><span class="op-evidence-number">27 / 27</span><div><b>Kind E2E 테스트 항목 통과</b><p>2026.10.20 실행 기준 · 테스트 항목 수이며, 필수 복구 시나리오 완료 수는 아닙니다.</p></div></div>
  <div><span class="op-evidence-number">RW / RO</span><div><b>VM 접속과 롤아웃 후 기존 데이터 확인</b><p>k3s / CUBRID 11.4.6 · 기존 볼륨·행 보존, RW 쓰기 / RO 읽기 / RO 쓰기 거부 확인 · VM 전원 장애 시험은 아님</p></div></div>
  <div><span class="op-evidence-number">5 / 7</span><div><b>VM 백업 → 새 클러스터 복원 시험 중 5회 통과</b><p>2026.10.25 실행 기준 · 나머지 2회는 세션 끊김(원인 조사 중, #238)으로 판정 보류 · 변조한 백업은 복원 거부</p></div></div>
</div>
<p class="op-boundary">동작하는 경로는 확인했고, 장애·복원 전체 검증은 다음 단계입니다.</p>

</OperatorSlide>

<!--
[40초 · 04 · 확인한 결과]
현재까지 직접 확인한 결과입니다. 첫째, 10월 20일 기준 Kind E2E 테스트 항목 27개 중 27개가 통과했습니다. 테스트 항목 수일 뿐, S00부터 S15까지 필수 시나리오 16개를 모두 통과했다는 뜻은 아닙니다.

둘째, k3s VM에서 접속과 SQL, 롤아웃 전후 기존 데이터와 RW/RO 동작을 확인했습니다. 셋째, 로드맵에서 2~4주차 목표로 잡은 백업 복원 초기 시험을 10월 25일 VM에서 일곱 번 했습니다. 다섯 번 통과했고, 두 번은 데이터 확인을 마친 뒤 DB 세션이 끊겨 판정을 보류했습니다. 세션이 끊긴 원인은 아직 찾는 중입니다. 백업 파일을 일부러 변조했을 때는 복원을 거부했습니다. 다만 이 결과를 어떤 장애에서도 복구된다는 증거로 보지는 않겠습니다.
-->

---

<OperatorSlide class="op-compact" section="05 · 전체 아키텍처" source="전체 아키텍처·Broker 설계" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">HA는 CUBRID가, 상태 확인과 운영 작업은 Operator가 맡습니다</h1><svg class="op-arch" style="max-height:372px" viewBox="0 0 900 384" role="img" aria-label="전체 아키텍처: 사용자가 Kubernetes API에 YAML을 적용하면 Operator가 spec을 읽고 Kubernetes 리소스를 만들며, 각 노드의 Instance Manager에 역할을 조회하고 결과를 status에 기록합니다. 애플리케이션 SQL은 RW/RO Service와 Broker를 거쳐 CUBRID HA 3노드로 가고, 백업은 S3 호환 저장소에 저장됩니다.">
<defs><marker id="op-arch-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0f1b2d"/></marker><marker id="op-arch-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-arch-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="150" y="0" width="750" height="328" rx="10" style="fill:none;stroke-dasharray:3 4"/><text class="s" x="162" y="16">Kubernetes 클러스터</text>
<rect class="box" x="0" y="14" width="130" height="50" rx="8"/><text x="65" y="35" text-anchor="middle">사용자</text><text class="s" x="65" y="53" text-anchor="middle">kubectl · YAML 적용</text>
<path class="ctl" d="M130 39H166" marker-end="url(#op-arch-blue)"/><text class="s b" x="148" y="32" text-anchor="middle">①</text>
<rect class="box" x="170" y="24" width="120" height="62" rx="8"/><text x="230" y="46" text-anchor="middle">Kubernetes API</text><text class="s" x="230" y="63" text-anchor="middle">CubridCluster</text><text class="s" x="230" y="78" text-anchor="middle">CubridBackup</text>
<path class="ctl" d="M290 44H336" marker-end="url(#op-arch-blue)"/><text class="s b" x="313" y="37" text-anchor="middle">② spec</text>
<path class="ctl" d="M338 70H292" marker-end="url(#op-arch-blue)"/><text class="s b" x="315" y="84" text-anchor="middle">④ status</text>
<rect class="box op" x="340" y="20" width="290" height="96" rx="8"/><text class="b" x="485" y="43" text-anchor="middle">CUBRID Kubernetes Operator</text><text class="s" x="485" y="64" text-anchor="middle">CubridCluster · CubridBackup 컨트롤러</text><text class="s" x="485" y="81" text-anchor="middle">HA · 서비스 · 스토리지 · 백업 · 업데이트</text><text class="s" x="485" y="101" text-anchor="middle">→ 하나의 상태 머신으로 조정</text>
<path class="mgmt" d="M630 50H656" marker-end="url(#op-arch-mute)"/>
<rect class="box" x="660" y="24" width="228" height="62" rx="8"/><text x="774" y="46" text-anchor="middle">관측</text><text class="s" x="774" y="63" text-anchor="middle">cubrid_cluster_* · cubrid_instance_*</text><text class="s" x="774" y="78" text-anchor="middle">Events · JSON 로그</text>
<path class="mgmt" d="M400 116V136" marker-end="url(#op-arch-mute)"/><text class="s" x="392" y="131" text-anchor="end">생성·관리</text>
<path class="ctl" d="M600 116V150" marker-end="url(#op-arch-blue)"/><text class="s b" x="610" y="135">③ 역할 조회·작업 요청 (토큰 인증)</text>
<rect class="box" x="170" y="138" width="262" height="84" rx="8"/><text x="301" y="159" text-anchor="middle">Kubernetes 리소스</text><text class="s" x="301" y="177" text-anchor="middle">StatefulSet · PVC · Secret</text><text class="s" x="301" y="194" text-anchor="middle">Service: headless · 노드별 alias</text><text class="s" x="301" y="211" text-anchor="middle">NetworkPolicy · Broker Deployment</text>
<rect class="box ha" x="450" y="152" width="440" height="152" rx="10"/><text x="464" y="174">CUBRID HA 3노드 — master 선출과 복제는 CUBRID가 직접</text>
<rect class="box ink" x="462" y="184" width="126" height="108" rx="7"/><text class="b" x="525" y="205" text-anchor="middle">노드 0 · master</text><rect class="box im" x="467" y="215" width="116" height="28" rx="5"/><text class="b" x="525" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="525" y="270" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="604" y="184" width="126" height="108" rx="7"/><text x="667" y="205" text-anchor="middle">노드 1 · slave</text><rect class="box im" x="609" y="215" width="116" height="28" rx="5"/><text class="b" x="667" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="667" y="270" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="746" y="184" width="126" height="108" rx="7"/><text x="809" y="205" text-anchor="middle">노드 2 · slave</text><rect class="box im" x="751" y="215" width="116" height="28" rx="5"/><text class="b" x="809" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="809" y="270" text-anchor="middle">CUBRID · PVC</text>
<path class="sql" d="M588 262H602" marker-end="url(#op-arch-ink)"/><path class="sql" d="M730 262H744" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="0" y="240" width="130" height="46" rx="8"/><text x="65" y="268" text-anchor="middle">애플리케이션</text>
<path class="sql" d="M130 263H166" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="170" y="243" width="128" height="40" rx="8"/><text x="234" y="268" text-anchor="middle">RW / RO Service</text>
<path class="sql" d="M298 263H310" marker-end="url(#op-arch-ink)"/>
<rect class="box ink" x="312" y="235" width="126" height="56" rx="8"/><text x="375" y="257" text-anchor="middle">Broker (RW · RO)</text><text class="s" x="375" y="277" text-anchor="middle">RW가 master를 찾음</text>
<path class="sql" d="M438 263H458" marker-end="url(#op-arch-ink)"/>
<path class="mgmt" d="M670 304V340" marker-start="url(#op-arch-mute)" marker-end="url(#op-arch-mute)"/><text class="s" x="680" y="326">백업 업로드 · 복원</text>
<rect class="box store" x="450" y="342" width="440" height="40" rx="8"/><text x="670" y="360" text-anchor="middle">S3 호환 오브젝트 저장소</text><text class="s" x="670" y="376" text-anchor="middle">초기 복사 · 백업 파일 · 파일 목록·체크섬</text>
<path class="sql" d="M0 346H40"/><text class="s" x="48" y="350">SQL 경로 · 복제 (Operator는 SQL을 중계하지 않음)</text>
<path class="ctl" d="M0 364H40"/><text class="s" x="48" y="368">운영 경로 ①–④ (12쪽의 제어 루프)</text>
<path class="mgmt" d="M0 382H40"/><text class="s" x="48" y="386">생성·관리 · 백업 데이터 · 관측</text>
</svg>

</OperatorSlide>

<!--
[45초 · 05 · 전체 아키텍처]
이제 아키텍처 초안입니다. 한 장에 전체를 담았습니다. 사용자가 YAML을 Kubernetes API에 적용하면, Operator가 spec을 읽고 StatefulSet과 볼륨, Secret, Service, Broker, NetworkPolicy를 만듭니다. Operator 안의 두 컨트롤러가 HA, 서비스, 스토리지, 백업, 업데이트를 하나의 상태 머신으로 조정합니다. 내부는 다음 장에서 보여드리겠습니다. 각 노드의 Instance Manager에 토큰 인증으로 역할을 묻고 작업을 요청하며, 결과를 다시 CubridCluster status에 기록합니다. 메트릭과 Events, 로그도 여기서 나옵니다.

아래쪽 실선은 애플리케이션의 SQL 경로입니다. RW나 RO Service에서 DB와 따로 떠 있는 Broker를 거쳐 CUBRID로 갑니다. Operator는 SQL을 중계하지 않고, master 선출과 복제는 CUBRID HA가 직접 합니다. 초기 데이터 복사와 백업 파일은 오른쪽 아래 S3 호환 저장소를 거칩니다.
-->

---

<OperatorSlide class="op-compact" section="05 · 제어·데이터 흐름" source="아키텍처·관측·보안 설계" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">Operator는 관찰하고, 기록하고, 다시 조정합니다</h1><p class="op-kicker">11쪽 그림의 ①–④ 제어 루프와 데이터 처리 과정 · 설계 기준</p><div class="op-timeline"><div><small>① 원하는 상태</small><b>YAML로 선언</b><p>CubridCluster·CubridBackup<br>spec에 원하는 구성</p></div><div><small>② 조정</small><b>두 컨트롤러</b><p>CubridCluster · CubridBackup<br>HA·서비스·스토리지·백업·업데이트를<br>하나의 상태 머신으로</p></div><div><small>③ 관찰</small><b>Instance Manager</b><p>노드마다 HA 역할 조회<br>토큰 인증 · pods/exec 미사용</p></div><div><small>④ 기록</small><b>status·Conditions</b><p>currentPrimary · 엇갈리면 “미확정”<br>Events·메트릭·로그<br>→ ②로 돌아가 다시 조정</p></div></div><table class="op-comparison"><thead><tr><th>데이터</th><th>처리 과정</th></tr></thead><tbody><tr><td><b>SQL</b></td><td>앱 → RW/RO Service → Broker → CUBRID · 복제와 master 전환은 CUBRID HA</td></tr><tr><td><b>백업·복원</b></td><td>Instance Manager가 S3 호환 저장소에 업로드 → 파일 목록·체크섬 확인 → 새 CubridCluster로 복원</td></tr><tr><td><b>상태</b></td><td>Instance Manager 응답 → Operator → CubridCluster status · 메트릭(cubrid_cluster_*, cubrid_instance_*)</td></tr></tbody></table>

</OperatorSlide>

<!--
[40초 · 05 · 제어·데이터 흐름]
아키텍처를 동작 순서로 보면 네 단계입니다. 사용자가 YAML로 원하는 상태를 선언하면, Operator의 두 컨트롤러가 HA, 서비스, 스토리지, 백업, 업데이트를 따로 움직이지 않고 하나의 상태 머신으로 조정합니다. 각 노드의 Instance Manager에 역할을 묻고, 그 결과를 status와 Conditions에 기록합니다. 노드 응답이 엇갈리면 master를 추정하지 않고 미확정으로 남긴 뒤 다시 조정합니다.

데이터는 세 갈래입니다. SQL은 Broker를 거쳐 CUBRID로 가고 Operator를 지나지 않습니다. 백업은 Instance Manager가 S3 호환 저장소에 올리고, 복원은 파일 목록과 체크섬을 확인한 뒤 새 클러스터를 만드는 방식입니다. 상태 정보는 Operator가 모아 status와 메트릭으로 보여 줍니다. 이 흐름은 설계 기준이고, 실제로 확인한 범위는 앞에서 보여드린 결과까지입니다.
-->

---

<OperatorSlide class="op-compact" section="05 · Operator 내부" source="Operator 소스 986b775" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/986b77521a1a2fa2a9da5a3ccce4e5a0c0b2fdd7/internal/controller">

<h1 class="op-title">Operator 내부: 두 컨트롤러와 Instance Manager</h1><svg class="op-arch" style="max-height:384px" viewBox="0 0 900 388" role="img" aria-label="Operator 내부 아키텍처: Operator Pod 안의 controller-runtime 매니저가 CubridCluster와 CubridBackup 컨트롤러를 실행합니다. 클러스터 컨트롤러는 Service, Secret, ConfigMap, NetworkPolicy, StatefulSet을 차례로 맞춘 뒤 HA 상태와 복원, 업데이트, Broker를 처리하고 status를 기록합니다. 두 컨트롤러는 HTTP와 Bearer 토큰으로 각 DB Pod의 Instance Manager를 호출하고, Instance Manager는 CUBRID와 S3 호환 저장소를 다룹니다.">
<defs><marker id="op-in-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-in-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="0" y="0" width="150" height="74" rx="8"/><text x="75" y="24" text-anchor="middle">Kubernetes API</text><text class="s" x="75" y="44" text-anchor="middle">CubridCluster</text><text class="s" x="75" y="62" text-anchor="middle">CubridBackup</text>
<path class="ctl" d="M150 28H180" marker-end="url(#op-in-blue)"/><path class="ctl" d="M180 52H152" marker-end="url(#op-in-blue)"/><text class="s b" x="0" y="92">감시: CR + 소유 리소스</text><text class="s b" x="0" y="110">기록: status · Events</text>
<rect class="box" x="0" y="140" width="150" height="104" rx="8"/><text x="75" y="162" text-anchor="middle">소유 리소스</text><text class="s" x="75" y="184" text-anchor="middle">StatefulSet · Deployment</text><text class="s" x="75" y="202" text-anchor="middle">Service · ConfigMap</text><text class="s" x="75" y="220" text-anchor="middle">Secret · NetworkPolicy</text>
<path class="mgmt" d="M182 192H154" marker-end="url(#op-in-mute)"/>
<rect class="box" x="0" y="262" width="150" height="66" rx="8"/><text x="75" y="284" text-anchor="middle">관측</text><text class="s" x="75" y="303" text-anchor="middle">cubrid_* 메트릭</text><text class="s" x="75" y="320" text-anchor="middle">Events · JSON 로그</text>
<path class="mgmt" d="M182 296H154" marker-end="url(#op-in-mute)"/>
<rect class="box op" x="170" y="0" width="460" height="388" rx="10" style="fill:none"/><text class="b" x="184" y="20">Operator Pod</text><text class="s" x="184" y="36">controller-runtime 매니저 · leader election · metrics · health probe</text>
<rect class="box op" x="182" y="46" width="436" height="214" rx="8"/><text x="196" y="66">CubridClusterReconciler <tspan class="s" style="font-weight:400;fill:#5b6b82">(조정 순서)</tspan></text><text class="s" x="196" y="88">1. Service: headless · 노드별 alias</text><text class="s" x="196" y="110">2. Instance Manager 토큰 Secret · HA 설정 ConfigMap</text><text class="s" x="196" y="132">3. NetworkPolicy · StatefulSet</text><text class="s" x="196" y="154">4. HA 부트스트랩 → 노드별 역할 조회 → master 판단(엇갈리면 미확정)</text><text class="s" x="196" y="176">5. 백업에서 복원 · 엔진 버전 확인 · slave부터 롤링 교체</text><text class="s" x="196" y="198">6. Broker 계층과 Broker Condition</text><text class="s" x="196" y="220">7. status·Conditions 기록 · Events · 메트릭</text>
<rect class="box op" x="182" y="268" width="436" height="56" rx="8"/><text x="196" y="288">CubridBackupReconciler</text><text class="s" x="196" y="310">대상 노드 선택(역할 조회) → 백업 요청(멱등 키) → 작업 조회 → 완료·실패 기록</text>
<rect class="box im" x="182" y="332" width="436" height="48" rx="8"/><text class="b" x="196" y="351">Instance Manager 클라이언트</text><text class="s" x="196" y="370">역할 조회 · 백업·복원 요청 · HTTP + Secret의 Bearer 토큰</text>
<path class="ctl" d="M618 356H644V120H668" marker-end="url(#op-in-blue)"/>
<rect class="box ha" x="660" y="0" width="240" height="306" rx="10"/><text x="672" y="20">DB Pod (HA 노드마다)</text>
<rect class="box im" x="672" y="30" width="216" height="198" rx="8"/><text class="b" x="684" y="52">Instance Manager</text><text class="s" x="684" y="74">GET /v1/role · /v1/ha/status</text><text class="s" x="684" y="93">GET /v1/ha/convergence</text><text class="s" x="684" y="112">POST /v1/ha/bootstrap · /v1/backup</text><text class="s" x="684" y="131">POST /v1/restore/prepare</text><text class="s" x="684" y="150">GET /v1/operations</text><text class="s" x="684" y="169">POST /v1/shutdown</text><text class="s" x="684" y="188">작업 기록(볼륨) · 볼륨 잠금</text><text class="s" x="684" y="207">업로드·검증 · watchdog</text>
<path class="mgmt" d="M780 228V238" marker-end="url(#op-in-mute)"/>
<rect class="box ink" x="672" y="240" width="216" height="54" rx="8"/><text x="780" y="262" text-anchor="middle">CUBRID</text><text class="s" x="780" y="282" text-anchor="middle">DB 서버 · HA · 데이터 볼륨</text>
<path class="mgmt" d="M780 306V334" marker-start="url(#op-in-mute)" marker-end="url(#op-in-mute)"/><text class="s" x="790" y="324">업로드 · 복원 준비</text>
<rect class="box store" x="660" y="336" width="240" height="48" rx="8"/><text x="780" y="356" text-anchor="middle">S3 호환 저장소</text><text class="s" x="780" y="374" text-anchor="middle">백업 파일 · 파일 목록·체크섬</text>
</svg>

</OperatorSlide>

<!--
[35초 · 05 · Operator 내부]
Operator 안을 조금 더 들여다보겠습니다. 현재 코드 기준입니다. Operator Pod에서 controller-runtime 매니저가 두 컨트롤러를 실행합니다. CubridCluster 컨트롤러는 매번 같은 순서로 맞춥니다. Service와 Secret, HA 설정, NetworkPolicy, StatefulSet을 만든 뒤, HA 부트스트랩과 노드별 역할 조회로 master를 판단하고, 복원과 롤링 업데이트, Broker를 처리한 다음 status와 Conditions, Events, 메트릭을 남깁니다. CubridBackup 컨트롤러는 대상 노드를 고르고 백업을 요청한 뒤 작업 결과를 기록합니다.

두 컨트롤러 모두 Secret에 있는 토큰으로 각 DB Pod의 Instance Manager를 HTTP로 호출합니다. Instance Manager는 역할 조회, HA 부트스트랩, 백업, 복원 준비, 종료를 맡고, 작업 기록을 볼륨에 남겨 중간에 끊겨도 같은 작업을 다시 찾을 수 있게 합니다.
-->

---

<OperatorSlide section="03 · 검증과 다음 단계">

<ChapterDivider number="03" title="검증 계획과 다음 단계" subtitle="기능보다 먼저 복구와 안전성을 검증합니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 검증과 다음 단계]
이 페이지에서는 새 주장이나 일정을 설명하지 않습니다. 다음 장의 로드맵으로 진행합니다.
-->

---

<OperatorSlide section="06 · 12주 계획" source="개발 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">11월에는 한 번 통과, 12월에는 반복 검증</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>기준 정하기</b><p>환경·시나리오 정리<br>단일 DB SQL 확인</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA와 실행 환경</b><p>3노드 HA·RW/RO<br>VM에서 실행<br>백업·복구 초기 시험</p></div><div><small>5–8주 · 11.02–11.29</small><b>장애·복구 시험</b><p>쓰기 차단·재합류<br>재구축·백업 복원<br>필수 시나리오 첫 통과 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>같은 후보 버전으로 반복</b><p>장애 반복·24시간 부하 목표<br>다른 사람이 문서대로 재현<br>문제 수정·배포 파일 정리</p></div></div><p class="op-boundary"><b>11.29</b> 필수 시나리오 첫 전체 통과 목표　→　<b>12.27</b> v0.1 공개 목표</p>

</OperatorSlide>

<!--
[40초 · 06 · 12주 계획]
일정은 10월 5일부터 12월 27일까지 12주로 잡았습니다. 첫 주에는 환경과 시나리오를 정하고 단일 DB에서 SQL을 확인합니다. 2주부터 4주는 3노드 HA와 RW/RO, VM 실행 환경과 백업·복구 초기 시험입니다. 지금 보여드린 Kind와 VM 결과도 이 단계에서 확인한 것들입니다.

11월 말, 정확히는 11월 29일까지 필수 시나리오를 한 번씩은 전부 통과시키는 게 목표입니다. 쓰기 차단, 재합류, 재구축, 백업에서 새 클러스터로 복원하는 것까지 들어갑니다. 12월에는 같은 후보 버전으로 장애 시험을 반복하고, 24시간 부하 시험과 다른 사람의 문서 재현을 해보려고 합니다. 나온 문제를 고치고 12월 27일 공개를 목표로 합니다. 공개 여부는 이 시험 결과를 보고 판단하겠습니다.
-->

---

<OperatorSlide section="06 · 팀 역할" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">두 명이 만들고, 서로 검증합니다</h1><div class="op-people"><div><p class="op-kicker">구현 · 이슈 담당자</p><b>재현부터 근거까지 책임</b><p>문제 재현 → 코드 → 테스트 → 문서 → 실험 기록을 한 작업으로 묶습니다.</p></div><div><p class="op-kicker">검증 · 다른 메인테이너</p><b>코드와 실행 결과를 교차 검증</b><p>변경과 증거를 확인하고, 공개 전에는 문서만 보고 설치·복구를 재현합니다.</p></div></div><p class="op-boundary"><b>원칙</b>　작성자와 최종 검증자는 다른 사람입니다 · 공유 VM 장애 시험은 한 번에 하나씩 · 공개 여부는 함께 결정</p>

</OperatorSlide>

<!--
[25초 · 06 · 팀 역할]
저희 둘이 함께 개발합니다. 이슈마다 담당자를 정하고, 맡은 사람이 문제 재현부터 코드와 테스트, 문서, 실험 기록까지 준비합니다. 하지만 그 작업을 혼자 통과시키지는 않습니다. 다른 한 사람이 코드와 실험 결과를 다시 확인합니다.

HA와 백업·복구, 설치 문서도 같은 방식으로 진행합니다. VM 장애 시험은 같은 환경을 쓰기 때문에 한 번에 하나씩 합니다. 릴리스 전에는 다른 메인테이너가 문서만 보고 설치와 복구를 끝낼 수 있는지도 확인하겠습니다.
-->

---

<OperatorSlide section="06 · v0.1 필수 시험" source="v0.1 필수 안전 검증" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">v0.1 전에 장애 상황에서도 안전한지 확인합니다</h1>
<div class="op-gates">
  <div><span>01 · 쓰기 차단</span><b>master가 불확실하거나 네트워크가 나뉘었을 때</b><p>쓰기를 받으면 안 되는 상황에서 실제 SQL 쓰기가 차단되는가?</p></div>
  <div><span>02 · 재합류·재구축</span><b>장애가 난 노드가 다시 합류하거나 재구축될 때</b><p>정상 노드와 이미 커밋한 데이터를 덮어쓰지 않고 복귀하는가?</p></div>
  <div><span>03 · 반복 복원</span><b>복원을 반복하거나 도중에 끊겼을 때</b><p>여러 번 복원하거나 도중에 재시작해도 데이터가 일치하는가?</p></div>
  <div><span>04 · 재현</span><b>정한 환경에서 다른 사람이 따라 했을 때</b><p>정한 Kubernetes·스토리지(CSI) 구성에서 다른 메인테이너도 동일한 결과를 얻는가?</p></div>
</div>
<p class="op-boundary">이 네 가지를 포함한 필수 시나리오를 모두 통과해야 v0.1을 공개합니다.</p>

</OperatorSlide>

<!--
[40초 · 06 · v0.1 필수 시험]
이제 어떤 시험이 남았는지 말씀드리겠습니다. 가장 먼저 master가 불명확하거나 네트워크가 분리된 상황에서 실제 쓰기를 막는지 검증해야 합니다. 그다음 장애가 난 노드가 다시 합류하거나 재구축할 때 기존 정상 데이터를 지키는지 확인합니다.

앞서 말씀드린 대로 백업을 새 클러스터로 복원하는 초기 시험은 7번 중 5번 통과했습니다. 남은 일은 세션이 끊긴 원인을 찾고, 더 많은 조건에서 반복해 보는 것입니다. 마지막으로 Kubernetes와 CSI 구성을 고정하고 다른 메인테이너가 문서대로 같은 결과를 낼 수 있어야 합니다. 이 조건을 모두 채워야 v0.1을 공개할 수 있습니다.
-->

---

<OperatorSlide class="op-compact" section="06 · v0.1 범위" source="v0.1 범위" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1은 기능을 늘리기보다 검증에 집중합니다</h1><table class="op-comparison op-acceptance"><thead><tr><th>포함할 기능</th><th>어떻게 확인할지</th></tr></thead><tbody><tr><td>root 없이 실행·데이터 보존<br>3노드 HA·RW/RO</td><td>SQL을 실행하고 역할·커밋·데이터 확인</td></tr><tr><td>장애·쓰기 격리<br>재합류·재구축</td><td>Pod/VM/Broker/Operator 장애 뒤 상태와 데이터 확인</td></tr><tr><td>백업<br>새 클러스터 복원</td><td>백업으로 새 클러스터를 만들어 데이터 비교</td></tr><tr><td>볼륨 보존·Instance Manager 인증<br>Kubernetes 노드 점검 중 보호·상태 지표</td><td>필수 시나리오 시험과 설치·운영·복구 문서 재현</td></tr></tbody></table><p class="op-boundary"><b>함께 공개</b>　이미지·설치 매니페스트·지원 환경표·운영 문서·시험 결과</p><p class="op-caption">지원 범위: CUBRID 11.4.x · amd64 · Kubernetes·스토리지 한 구성 · 실험 버전 · DB 암호·TLS는 v0.1 이후</p>

</OperatorSlide>

<!--
[40초 · 06 · v0.1 범위]
v0.1에서는 환경 하나를 정해서 설치부터 복구까지 확인하는 것을 목표로 합니다. 3노드 HA와 RW/RO에서 SQL을 실행하고, 장애를 낸 뒤 데이터와 역할을 확인합니다. 재합류와 재구축에서는 정상 데이터를 덮어쓰지 않아야 합니다. 백업으로 새 클러스터를 만들었을 때는 미리 준비한 데이터와 맞는지 비교합니다. 보존 정책과 Instance Manager 인증, Kubernetes 노드 점검 중 보호 정책, 상태와 지표도 확인해야 합니다.

이미지와 설치 매니페스트, 지원 환경표, 운영 문서와 시험 결과를 함께 공개하려고 합니다. CUBRID 11.4.x와 amd64, Kubernetes와 CSI 한 구성이 기준입니다. 현재 VM은 local-path여서 CSI 시험은 따로 해야 합니다. 첫 버전은 experimental입니다. Instance Manager 인증과는 별개로, 현재 DBA 암호는 비어 있고 통신도 암호화되지 않습니다. 호환 업데이트와 disk-full도 조건부로 남겨두었습니다.
-->

---

<OperatorSlide section="06 · 이후 방향" source="v0.1 이후 계획" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">v0.1 이후에는 사용자 피드백부터 반영합니다</h1><div class="op-release"><div><h3>먼저, 사용해 보며 불편한 점 고치기</h3><ul class="op-list"><li><b>로그와 진단부터 손보기</b><small>반복되는 문제와 복구 절차 정리</small></li><li><b>실사용에 필요한 기능</b><small>DB 인증·TLS·호환 업데이트</small></li></ul></div><div><h3>그다음, 지원 환경 늘리기</h3><ul class="op-list"><li><b>Kubernetes·CSI 조합 추가</b><small>조합마다 장애·복구 시험</small></li><li><b>arm64·여러 가용영역</b><small>지원 가능한지 별도로 확인</small></li></ul></div><div><h3>더 오래 걸리는 일 · 일정 미정</h3><ul class="op-list"><li><b>CUBRID 버전 변경</b><small>데이터 호환·중단·되돌리는 방법</small></li><li><b>복제 구성 추가</b><small>master로 승격되지 않는 replica 등</small></li></ul></div></div><p class="op-boundary">v0.1을 먼저 검증하고, 사용자들이 어디에서 불편한지 본 뒤 다음 우선순위를 정하려고 합니다.</p>

</OperatorSlide>

<!--
[20초 · 06 · 이후 방향]
v0.1을 공개한 뒤에는 사용자 피드백을 받아 불편한 곳부터 고치려고 합니다. 로그와 복구 절차, DB 인증과 TLS를 먼저 보려고 합니다.

그다음 Kubernetes와 CSI 조합을 하나씩 늘리고 조합마다 장애와 복구를 다시 시험하겠습니다. 후속 버전과 날짜는 아직 정하지 않았습니다.
-->

---

<OperatorSlide section="Q&amp;A · 질의응답" source="예상 질문" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 프로젝트입니다. CUBRID는 해당 권리자의 상표입니다.</p></div>

</OperatorSlide>

<!--
[15초 · Q&A · 질의응답]
감사합니다. 질문 받겠습니다. 장애 뒤 무엇을 먼저 확인하시는지, 먼저 지원했으면 하는 Kubernetes CSI 드라이버가 무엇인지도 들려주시면 v0.1에 반영하겠습니다.
-->
