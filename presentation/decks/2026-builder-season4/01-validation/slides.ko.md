---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="Opening · 프로젝트 소개" index="01" total="15" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">Kubernetes에서 CUBRID 설치부터 장애 후 복구 확인까지</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[20초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저희는 관계형 DBMS인 CUBRID를 Kubernetes에서 관리하는 Operator를 만들고 있습니다. 설치만 자동화하는 것이 아니라, 장애가 난 뒤 정말 복구됐는지 확인하는 과정까지 운영 흐름으로 묶는 것이 목표입니다.

이번 시즌에는 환경 하나를 정해서 직접 설치하고, 장애를 내고, 복구되는 것까지 확인한 v0.1을 내려고 합니다. 먼저 이 Operator가 무엇인지부터 말씀드리겠습니다.
-->

---

<OperatorSlide class="op-compact" section="1 · 무엇인가" index="02" total="15" source="Operator README·검증 기록" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md">

<h1 class="op-title">Kubernetes에서 CUBRID HA 클러스터를 운영하는 Operator</h1><p class="op-lead">YAML에 원하는 구성을 적으면 Operator가 클러스터를 만들고, 상태를 지켜보고, 백업·복원 같은 운영 작업을 조정합니다.</p><table class="op-comparison op-capabilities"><thead><tr><th>하는 일</th><th>지금 상태</th></tr></thead><tbody><tr><td>3멤버 HA 클러스터와 RW/RO 접속 만들기<small>CubridCluster</small></td><td><span class="op-status done">확인함</span>Kind·VM에서 설치·접속, 롤아웃 후 데이터 보존</td></tr><tr><td>멤버마다 역할을 조회해 상태로 기록<small>엇갈리면 “미확정”</small></td><td><span class="op-status">구현함</span>장애 중 RW 쓰기 차단은 아직 구현·검증 전</td></tr><tr><td>백업하고 새 클러스터로 복원<small>CubridBackup · 오브젝트 저장소</small></td><td><span class="op-status">첫 통과</span>VM 7회 중 5회 통과, 2회 판정 보류</td></tr><tr><td>장애 뒤 멤버 재합류·재구축</td><td><span class="op-status plan">v0.1 목표</span>재합류·재구축 시험 전</td></tr></tbody></table><p class="op-caption">실험 단계 프로젝트이며 운영 환경용이 아닙니다. 공식 CUBRID Operator를 대체하지 않습니다.</p>

</OperatorSlide>

<!--
[45초 · 1 · 무엇인가]
CUBRID Kubernetes Operator는 Kubernetes에서 CUBRID HA 클러스터를 배포하고 운영하는 실험 단계의 Operator입니다. 사용자가 YAML에 원하는 구성을 적으면, Operator가 멤버 세 개짜리 HA 클러스터와 쓰기·읽기 접속 주소를 만들고, 멤버마다 역할을 조회해 상태로 기록합니다. 백업을 만들고 그 백업으로 새 클러스터를 복원하는 일도 맡습니다.

오른쪽은 지금 어디까지 왔는지입니다. 설치와 접속은 직접 확인했고, 백업으로 새 클러스터를 복원하는 시험은 처음 통과했습니다. 역할 기록은 구현했지만, 장애 중에 쓰기를 막는 부분은 아직입니다. 장애 뒤 재합류와 재구축은 v0.1에서 검증할 목표입니다. 운영 환경용은 아니고, 공식 Operator를 대체하려는 것도 아닙니다.
-->

---

<OperatorSlide section="1 · 왜 필요한가" index="03" total="15" source="문제·사용자 가설" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">Pod가 살아났다고 DB가 복구된 건 아닙니다</h1><p class="op-kicker">Kubernetes는 Pod와 볼륨을 되살립니다. DB 서비스 복구는 역할 · 접속 · 데이터까지입니다</p><div class="op-scene"><div class="op-actor"><div class="op-bubble">Pod는 다시 떴어요.<br>이제 된 거죠?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>Kubernetes 플랫폼 담당자</b></div><div class="op-incident"><span>⚡</span><b>같은 장애</b></div><div class="op-actor op-actor-db"><div class="op-bubble">master는 누구죠?<br>데이터는 괜찮나요?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>CUBRID DB 담당자</b></div></div><p class="op-boundary">두 사람이 같은 화면에서 “복구됐다”를 함께 확인할 수 있게 하는 것이 우리의 목표입니다.</p>

</OperatorSlide>

<!--
[40초 · 1 · 왜 필요한가]
왜 이게 필요한지 말씀드리겠습니다. Kubernetes는 Pod가 죽으면 다시 띄우고 볼륨을 다시 붙여 줍니다. 하지만 DB 서비스가 복구됐다는 것은 그보다 더 많은 뜻입니다. 지금 master가 누구인지, 쓰고 읽을 수 있는지, 장애 전 데이터가 남았는지까지 확인해야 합니다.

그래서 같은 장애를 두 팀이 다르게 봅니다. Kubernetes 플랫폼 담당자는 Pod가 다시 떴으니 됐다고 보고, CUBRID 담당자는 master와 데이터를 묻습니다. 저희는 이 두 팀을 첫 사용자로 가정합니다. 인터뷰로 확정한 것은 아니어서 오늘 운영 경험을 듣고 싶습니다. 두 사람이 같은 화면에서 복구를 확인할 수 있게 하는 것이 목표입니다.
-->

---

<OperatorSlide class="op-compact" section="2 · 구조" index="04" total="15" source="구성도·Broker 설계" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID는 HA를, Operator는 관찰과 조정을 맡습니다</h1><svg class="op-arch" viewBox="0 0 880 352" role="img" aria-label="Operator 구성도: YAML에서 Kubernetes API, Operator, Kubernetes 리소스로 이어지는 운영 경로와, 애플리케이션에서 RW/RO Service, Broker를 거쳐 CUBRID HA 멤버 3개로 가는 SQL 경로. 각 멤버에는 Instance Manager와 PVC가 있고, 백업 저장소와 연결됩니다.">
<defs><marker id="op-arch-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0f1b2d"/></marker><marker id="op-arch-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-arch-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="0" y="8" width="150" height="62" rx="8"/><text x="75" y="29" text-anchor="middle">YAML</text><text class="s" x="75" y="47" text-anchor="middle">CubridCluster</text><text class="s" x="75" y="62" text-anchor="middle">CubridBackup</text>
<rect class="box" x="180" y="8" width="150" height="62" rx="8"/><text x="255" y="44" text-anchor="middle">Kubernetes API</text>
<rect class="box op" x="360" y="8" width="200" height="62" rx="8"/><text class="b" x="460" y="33" text-anchor="middle">Operator</text><text class="s" x="460" y="54" text-anchor="middle">관찰·조정</text>
<rect class="box" x="590" y="8" width="290" height="62" rx="8"/><text x="735" y="33" text-anchor="middle">Kubernetes 리소스</text><text class="s" x="735" y="54" text-anchor="middle">StatefulSet · Broker · Service · PVC</text>
<path class="ctl" d="M150 39H176" marker-end="url(#op-arch-blue)"/><path class="ctl" d="M330 39H356" marker-end="url(#op-arch-blue)"/><path class="ctl" d="M560 39H586" marker-end="url(#op-arch-blue)"/>
<path class="ctl" d="M440 70V108" marker-end="url(#op-arch-blue)"/><text class="s b" x="450" y="94">Instance Manager에 작업 요청·역할 조회</text>
<path class="mgmt" d="M800 70V108" marker-end="url(#op-arch-mute)"/><text class="s" x="790" y="94" text-anchor="end">생성·관리</text>
<rect class="box ha" x="330" y="112" width="550" height="150" rx="10"/><text x="346" y="136">CUBRID HA — master 선출과 복제는 CUBRID가 직접</text>
<rect class="box ink" x="346" y="148" width="168" height="104" rx="7"/><text x="430" y="171" text-anchor="middle">멤버 0</text><rect class="box im" x="358" y="182" width="144" height="30" rx="5"/><text class="b" x="430" y="202" text-anchor="middle" style="font-size:13px">Instance Manager</text><text class="s" x="430" y="238" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="523" y="148" width="168" height="104" rx="7"/><text x="607" y="171" text-anchor="middle">멤버 1</text><rect class="box im" x="535" y="182" width="144" height="30" rx="5"/><text class="b" x="607" y="202" text-anchor="middle" style="font-size:13px">Instance Manager</text><text class="s" x="607" y="238" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="700" y="148" width="168" height="104" rx="7"/><text x="784" y="171" text-anchor="middle">멤버 2</text><rect class="box im" x="712" y="182" width="144" height="30" rx="5"/><text class="b" x="784" y="202" text-anchor="middle" style="font-size:13px">Instance Manager</text><text class="s" x="784" y="238" text-anchor="middle">CUBRID · PVC</text>
<rect class="box" x="0" y="112" width="230" height="40" rx="8"/><text x="115" y="137" text-anchor="middle">애플리케이션</text>
<path class="sql" d="M115 152V166" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="0" y="168" width="230" height="40" rx="8"/><text x="115" y="193" text-anchor="middle">RW / RO Service</text>
<path class="sql" d="M115 208V220" marker-end="url(#op-arch-ink)"/>
<rect class="box ink" x="0" y="222" width="230" height="52" rx="8"/><text x="115" y="243" text-anchor="middle">Broker (RW · RO)</text><text class="s" x="115" y="263" text-anchor="middle">DB와 분리 · RW가 master를 찾음</text>
<path class="sql" d="M230 242H326" marker-end="url(#op-arch-ink)"/><text x="278" y="233" text-anchor="middle" style="font-size:13px">SQL</text>
<rect class="box store" x="330" y="296" width="550" height="48" rx="8"/><text x="605" y="317" text-anchor="middle">백업 저장소</text><text class="s" x="605" y="335" text-anchor="middle">S3 호환 오브젝트 저장소 · 초기 복사 · 백업 · 복원</text>
<path class="mgmt" d="M605 266V292" marker-start="url(#op-arch-mute)" marker-end="url(#op-arch-mute)"/>
<path class="sql" d="M0 306H40"/><text class="s" x="48" y="310">SQL 경로 · Operator는 SQL을 중계하지 않음</text>
<path class="ctl" d="M0 330H40"/><text class="s" x="48" y="334">운영 경로 · 설정·작업 요청·상태</text>
</svg>

</OperatorSlide>

<!--
[50초 · 2 · 구조]
전체 구성입니다. 위쪽 파란 점선이 운영 경로입니다. 사용자가 YAML을 Kubernetes API에 올리면 Operator가 그것을 보고 StatefulSet, Broker, Service, 볼륨을 만듭니다. DB 시작이나 백업 같은 작업은 각 멤버 안의 Instance Manager에 요청하고, 멤버마다 역할을 조회해 상태로 기록합니다.

왼쪽 실선이 애플리케이션의 SQL 경로입니다. RW나 RO Service에서 DB와 따로 떠 있는 Broker를 거쳐 CUBRID로 갑니다. RW Broker가 master를 직접 찾아가기 때문에 Operator는 SQL을 중계하지 않습니다. master 선출과 복제는 CUBRID HA가 직접 하고, 장애 때 Operator가 master를 고르지 않습니다. 초기 데이터 복사와 백업 파일은 아래쪽 오브젝트 저장소를 거칩니다.
-->

---

<OperatorSlide class="op-compact" section="2 · 장애 흐름 예시" index="05" total="15" source="장애 시 확인 순서" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#12-failover-and-split-brain-model">

<h1 class="op-title">master Pod가 사라지면, 네 가지를 따로 확인합니다</h1><p class="op-kicker">예: 실행 중이던 master의 Pod가 사라졌다가 다시 떴을 때 · 설계상 흐름</p><table class="op-comparison op-checks"><thead><tr><th>확인할 것</th><th>누가 답하나</th><th>무엇을 보나</th></tr></thead><tbody><tr><td>① Pod 가용성</td><td>Kubernetes</td><td>Pod가 다시 Ready인가 · 볼륨이 붙었나</td></tr><tr><td>② DB HA 상태</td><td>CUBRID HA가 전환<br>Operator가 기록</td><td>멤버마다 역할을 조회해 비교<br>빠지거나 엇갈리면 “미확정”</td></tr><tr><td>③ SQL 접속</td><td>Broker</td><td>RW Broker가 새 master로 연결되나<br>RW 쓰기 · RO 읽기가 되나</td></tr><tr><td>④ 데이터</td><td>E2E 시험</td><td>장애 전에 커밋한 행이 남았나<br>Operator가 자동으로 확인하지는 않음</td></tr></tbody></table><p class="op-boundary"><b>Kubernetes 모니터링은 ①까지</b>　②–④를 한 흐름으로 확인하는 것이 이 프로젝트의 핵심입니다.</p>

</OperatorSlide>

<!--
[45초 · 2 · 장애 흐름 예시]
이 구조에서 master Pod가 사라졌다가 다시 뜬다고 해 보겠습니다. 확인할 것이 네 가지입니다. 첫째, Pod가 다시 Ready이고 볼륨이 붙었는지는 Kubernetes가 알려 줍니다. 일반적인 Kubernetes 모니터링은 여기까지입니다.

둘째, master 전환은 CUBRID HA가 하고, Operator는 멤버마다 역할을 조회해 비교합니다. 응답이 빠지거나 엇갈리면 master를 추정하지 않고 미확정으로 둡니다. 셋째, RW Broker가 새 master로 연결돼 쓰기와 읽기가 되는지 봅니다. 넷째, 장애 전에 커밋한 데이터가 남았는지는 지금은 E2E 시험에서 확인합니다. Operator가 데이터를 자동으로 검증한다는 뜻은 아닙니다.
-->

---

<OperatorSlide section="2 · 장애 대응 원칙" index="06" total="15" source="쓰기 격리 이슈·ADR" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

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

<OperatorSlide class="op-compact" section="2 · 기존 방식과 차이" index="07" total="15" source="공식 Operator·소스 비교" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">공식 Operator가 이미 있는데, 무엇이 다른가요?</h1><p class="op-kicker">공식 CUBRID Operator도 HA 상태 조회 · 스토리지 · 예약 백업을 제공합니다</p><table class="op-comparison"><thead><tr><th></th><th>공식 Operator (지금)</th><th>우리가 바꾸는 것</th></tr></thead><tbody><tr><td><b>master 멤버 확인</b></td><td>처음 응답한 멤버 하나의<br>노드 정보를 그대로 사용</td><td>모든 멤버의 최신 응답을 비교<br>빠지거나 엇갈리면 “미확정”으로 표시</td></tr><tr><td><b>백업 작업 기록</b></td><td>예약 백업을 Pod 안에서 명령으로 실행<br>백업 상태를 기록</td><td>Instance Manager에 요청하고 작업 ID를 볼륨에 기록<br>재시작으로 끊긴 작업은 “실패”로 남김</td></tr><tr><td><b>복원</b></td><td>소스에서 복원 기능을 찾지 못함<br>(백업만 지원)</td><td>복원 전에 파일 목록과 체크섬을 확인<br>항상 새 클러스터로 복원</td></tr><tr><td><b>복구 확인</b></td><td>포트 검사</td><td>포트 검사는 같음<br>시험에서 실제 SQL 쓰기·읽기와 데이터까지 확인</td></tr></tbody></table><p class="op-caption">확인한 소스 버전 기준의 비교입니다. 실제 장애에서 어느 쪽이 더 안정적인지는 아직 시험 전입니다.</p>

</OperatorSlide>

<!--
[50초 · 2 · 기존 방식과 차이]
CUBRID에는 이미 공식 Operator가 있고, HA 상태 조회와 스토리지, 예약 백업을 제공합니다. 그럼 무엇이 다를까요? 표는 두 프로젝트의 소스를 직접 읽고 정리한 것입니다.

공식 Operator는 처음 응답한 멤버 하나의 정보로 master를 판단합니다. 저희는 모든 멤버의 최신 응답을 비교하고, 빠지거나 엇갈리면 미확정으로 둡니다. 백업 같은 작업은 Instance Manager에 요청하고 작업 ID를 볼륨에 남겨서, 중간에 끊기면 실패로 기록합니다. 공식 Operator 소스에서는 복원 기능을 찾지 못했습니다. 저희는 복원 전에 파일 목록과 체크섬을 확인합니다. 운영 중 판단은 두 쪽 모두 포트 검사를 쓰기 때문에, 저희는 시험에서 SQL과 데이터를 따로 확인합니다. 실제 장애에서 어느 쪽이 더 안정적인지는 아직 비교하지 못했습니다.
-->

---

<OperatorSlide section="3 · 검증 근거" index="08" total="15" source="2026.10.20–25 실행 기록" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

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

<OperatorSlide section="3 · 다음 검증" index="09" total="15" source="v0.1 필수 안전 검증" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">다음 시험은 실패하는 순간을 겨냥합니다</h1>
<div class="op-gates">
  <div><span>01 · SAFE WRITES</span><b>master 불확실·네트워크 분할</b><p>쓰기 성공을 허용하지 않아야 할 순간에 실제 SQL 요청이 차단되는가?</p></div>
  <div><span>02 · RECOVERY</span><b>장애 후 재합류·재구축</b><p>정상 멤버와 이미 커밋한 데이터를 덮어쓰지 않고 복귀하는가?</p></div>
  <div><span>03 · RESTORE</span><b>복원 반복·중단</b><p>여러 번 반복하거나 복원 도중 재시작돼도 데이터가 일치하는가?</p></div>
  <div><span>04 · REPRODUCE</span><b>스토리지·환경·문서 재현</b><p>정한 Kubernetes·스토리지(CSI) 구성에서 다른 메인테이너도 동일한 결과를 얻는가?</p></div>
</div>
<p class="op-boundary">이 네 가지를 포함한 필수 시나리오를 모두 통과해야 v0.1을 공개합니다.</p>

</OperatorSlide>

<!--
[40초 · 3 · 다음 검증]
이제 어떤 시험이 남았는지 말씀드리겠습니다. 가장 먼저 master가 불명확하거나 네트워크가 분리된 상황에서 실제 쓰기를 막는지 검증해야 합니다. 그다음 손상된 멤버가 다시 합류하거나 재구축할 때 기존 정상 데이터를 지키는지 확인합니다.

앞서 말씀드린 대로 백업을 새 클러스터로 복원하는 시험은 처음 통과했습니다. 남은 일은 세션이 끊긴 원인을 찾고, 더 많은 조건에서 반복해 보는 것입니다. 마지막으로 Kubernetes와 CSI 구성을 고정하고 다른 메인테이너가 문서대로 같은 결과를 낼 수 있어야 합니다. 이 조건을 모두 채워야 v0.1을 공개할 수 있습니다.
-->

---

<OperatorSlide section="3 · 12주 로드맵" index="10" total="15" source="개발 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">11월엔 한 번 완주, 12월엔 같은 조건으로 반복</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>기준 정하기</b><p>환경·시나리오 정리<br>단일 DB SQL 확인</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA와 실행 환경</b><p>3멤버·RW/RO<br>VM에서 실행<br>백업·복구 초기 시험</p></div><div><small>5–8주 · 11.02–11.29</small><b>장애·복구 시험</b><p>쓰기 차단·재합류<br>재구축·백업 복원<br>필수 시나리오 첫 통과 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>같은 후보 버전으로 반복</b><p>장애 반복·24시간 부하 목표<br>다른 사람이 문서대로 재현<br>문제 수정·배포 파일 정리</p></div></div><p class="op-boundary"><b>11.29</b> 필수 시나리오 첫 전체 통과 목표　→　<b>12.27</b> v0.1 공개 목표</p>

</OperatorSlide>

<!--
[40초 · 3 · 12주 로드맵]
일정은 10월 5일부터 12월 27일까지 12주로 잡았습니다. 첫 주에는 환경과 시나리오를 정하고 단일 DB에서 SQL을 확인합니다. 2주부터 4주는 3멤버 HA와 RW/RO, VM 실행 환경과 백업·복구 초기 시험입니다. 지금 보여드린 Kind와 VM 결과도 이 단계에서 확인한 것들입니다.

11월 말, 정확히는 11월 29일까지 필수 시나리오를 한 번씩은 전부 통과시키는 게 목표입니다. 쓰기 차단, 재합류, 재구축, 백업에서 새 클러스터로 복원하는 것까지 들어갑니다. 12월에는 같은 후보 버전으로 장애 시험을 반복하고, 24시간 부하 시험과 다른 사람의 문서 재현을 해보려고 합니다. 나온 문제를 고치고 12월 27일 공개를 목표로 합니다. 공개 여부는 이 시험 결과를 보고 판단하겠습니다.
-->

---

<OperatorSlide section="3 · 개발 방식" index="11" total="15" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">두 명이 만들지만, 혼자 통과시키지 않습니다</h1><div class="op-people"><div><p class="op-kicker">IMPLEMENTER · 이슈별 담당자</p><b>재현부터 근거까지 책임</b><p>문제 재현 → 코드 → 테스트 → 문서 → 실험 기록을 한 작업으로 묶습니다.</p></div><div><p class="op-kicker">REVIEWER · 다른 메인테이너</p><b>코드와 실행 결과를 교차 검증</b><p>변경과 증거를 확인하고, 공개 전에는 문서만 보고 설치·복구를 재현합니다.</p></div></div><p class="op-boundary"><b>작성자 ≠ 최종 검증자</b>　공유 VM의 장애 시험은 한 번에 하나씩 진행하고, 공개 여부는 함께 결정합니다.</p>

</OperatorSlide>

<!--
[25초 · 3 · 개발 방식]
저희 둘이 함께 개발합니다. 이슈마다 담당자를 정하고, 맡은 사람이 문제 재현부터 코드와 테스트, 문서, 실험 기록까지 준비합니다. 하지만 그 작업을 혼자 통과시키지는 않습니다. 다른 한 사람이 코드와 실험 결과를 다시 확인합니다.

HA와 백업·복구, 설치 문서도 같은 방식으로 진행합니다. VM 장애 시험은 같은 환경을 쓰기 때문에 한 번에 하나씩 합니다. 릴리스 전에는 다른 메인테이너가 문서만 보고 설치와 복구를 끝낼 수 있는지도 확인하겠습니다.
-->

---

<OperatorSlide class="op-compact" section="4 · v0.1 범위" index="12" total="15" source="v0.1 범위" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1은 기능 수보다 검증 가능한 범위로 자릅니다</h1><table class="op-comparison op-acceptance"><thead><tr><th>포함할 기능</th><th>어떻게 확인할지</th></tr></thead><tbody><tr><td>root 없이 실행·데이터 보존<br>3멤버 HA·RW/RO</td><td>SQL을 실행하고 역할·커밋·데이터 확인</td></tr><tr><td>장애·쓰기 격리<br>재합류·재구축</td><td>Pod/VM/Broker/Operator 장애 뒤 상태와 데이터 확인</td></tr><tr><td>백업<br>새 클러스터 복원</td><td>백업으로 새 클러스터를 만들어 데이터 비교</td></tr><tr><td>볼륨 보존·Instance Manager 인증<br>노드 점검 중 보호·상태 지표</td><td>필수 시나리오 시험과 설치·운영·복구 문서 재현</td></tr></tbody></table><p class="op-boundary"><b>함께 공개</b>　이미지·설치 매니페스트·지원 환경표·운영 문서·시험 결과</p><p class="op-caption">지원 범위: CUBRID 11.4.x · amd64 · Kubernetes·스토리지 한 구성 · 실험 버전 · DB 암호·TLS는 v0.1 이후</p>

</OperatorSlide>

<!--
[40초 · 4 · v0.1 범위]
v0.1에서는 환경 하나를 정해서 설치부터 복구까지 확인하겠습니다. 3멤버 HA와 RW/RO에서 SQL을 실행하고, 장애를 낸 뒤 데이터와 역할을 확인합니다. 재합류와 재구축에서는 정상 데이터를 덮어쓰지 않아야 합니다. 백업으로 새 클러스터를 만들었을 때는 미리 준비한 데이터와 맞는지 비교합니다. 보존 정책과 Instance Manager 인증, 노드 점검 중 보호 정책, 상태와 지표도 확인해야 합니다.

이미지와 설치 매니페스트, 지원 환경표, 운영 문서와 시험 결과를 함께 공개하려고 합니다. CUBRID 11.4.x와 amd64, Kubernetes와 CSI 한 구성이 기준입니다. 현재 VM은 local-path여서 CSI 시험은 따로 해야 합니다. 첫 버전은 experimental입니다. Instance Manager 인증과는 별개로, 현재 DBA 암호는 비어 있고 통신도 암호화되지 않습니다. 호환 업데이트와 disk-full도 조건부로 남겨두었습니다.
-->

---

<OperatorSlide section="4 · 이후 방향" index="13" total="15" source="v0.1 이후 계획" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">v0.1 이후는 확장보다 피드백 순서입니다</h1><div class="op-release"><div><h3>먼저, 써보면서 고치기</h3><ul class="op-list"><li><b>로그와 진단부터 손보기</b><small>반복되는 문제와 복구 절차 정리</small></li><li><b>실제로 쓰려면 필요한 기능</b><small>DB 인증·TLS·호환 업데이트</small></li></ul></div><div><h3>그다음, 지원 환경 늘리기</h3><ul class="op-list"><li><b>Kubernetes·CSI 조합 추가</b><small>조합마다 장애·복구 시험</small></li><li><b>arm64·여러 가용영역</b><small>지원 가능한지 별도로 확인</small></li></ul></div><div><h3>시간이 더 필요한 일</h3><ul class="op-list"><li><b>CUBRID 버전 변경</b><small>데이터 호환·중단·되돌리는 방법</small></li><li><b>복제 구성 추가</b><small>master로 승격되지 않는 읽기 복제본 등</small></li></ul></div></div><p class="op-boundary">v0.1을 먼저 검증하고, 사용자들이 어디에서 불편한지 본 뒤 다음 우선순위를 정하려고 합니다.</p>

</OperatorSlide>

<!--
[20초 · 4 · 이후 방향]
첫 버전을 내면 써보면서 불편한 곳부터 고치겠습니다. 로그와 복구 절차, DB 인증과 TLS가 먼저입니다.

그다음 Kubernetes와 CSI 조합을 하나씩 늘리고 조합마다 장애와 복구를 다시 시험하겠습니다. 후속 버전과 날짜는 아직 정하지 않았습니다.
-->

---

<OperatorSlide section="Closing · 함께 검증" index="14" total="15" source="의견·협력 요청" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">세 가지를 여쭙고 싶습니다</h1><ol class="op-questions op-big"><li>최근 장애에서 복구됐다고 판단하기 전에, 무엇부터 확인하셨나요?</li><li>첫 지원으로 원하시는 Kubernetes CSI 드라이버는 무엇인가요?</li><li>12월에 설치·복구 문서를 먼저 따라 해 봐 주실 수 있을까요?</li></ol>

</OperatorSlide>

<!--
[25초 · Closing · 함께 검증]
마지막으로 세 가지를 여쭙고 싶습니다. 최근 장애에서 복구됐다고 판단하기 전에 무엇부터 확인하셨는지, 그리고 v0.1이 처음 지원했으면 하는 Kubernetes CSI 드라이버가 무엇인지 듣고 싶습니다. 그 환경에서 장애 시험을 할 때 주의할 점도 알려 주시면 좋겠습니다.

그리고 12월에 설치·복구 문서를 먼저 따라 해 보고 막히는 곳을 알려 주실 분이 계시면 좋겠습니다.
-->

---

<OperatorSlide section="Q&amp;A · 질의응답" index="15" total="15" source="예상 질문" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 프로젝트입니다. CUBRID는 해당 권리자의 상표입니다.</p></div>

</OperatorSlide>

<!--
[5초 · Q&A · 질의응답]
감사합니다. 질문 받겠습니다.
-->
