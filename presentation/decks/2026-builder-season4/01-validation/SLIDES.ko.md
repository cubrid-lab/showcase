<OperatorSlide section="소개" index="01" total="17" source="README · Experimental" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md">

<div class="op-cover"><p class="op-kicker">STP IV · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID 운영을<br><span class="accent">Kubernetes의 언어로</span></h1><p class="op-lead">Pod를 띄우는 것을 넘어,<br>데이터베이스의 상태와 복구 과정을 설명하는 Operator.</p><div class="op-meta"><b>CUBRID Lab</b><span>CUBRID Kubernetes Operator</span></div></div>

</OperatorSlide>

<!--
[20초 · 소개]
안녕하세요. CUBRID Lab의 CUBRID Kubernetes Operator 프로젝트입니다. 저희가 풀려는 문제는 데이터베이스를 한 번 배포하는 데서 끝나지 않습니다. 장애 이후 어떤 상태인지 설명하고, 다시 운영 가능한 상태로 돌아오는 과정을 Kubernetes와 연결하려 합니다.
-->

---

<OperatorSlide section="팀과 개발 방식" index="02" total="17" source="Governance · Two maintainers" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/governance.md#maintainer-responsibilities">

<h1 class="op-title">두 명의 메인테이너,<br><span class="accent">함께 만들고 서로 검증합니다.</span></h1><div class="op-two"><div class="op-boundary"><b>CUBRID Lab</b><p class="op-lead">작은 변경 하나에<br>구현·테스트·리뷰를 함께 담습니다.</p></div><ul class="op-list"><li><b>공동 책임</b><small>범위·아키텍처·기여 검토·릴리스 판단</small></li><li><b>작성자가 검증</b><small>기능 작성자가 테스트와 운영 증거를 준비</small></li><li><b>상대가 리뷰</b><small>동작과 실패 경로를 다른 메인테이너가 확인</small></li></ul></div>

</OperatorSlide>

<!--
[25초 · 팀과 개발 방식]
저장소에 정리된 팀의 운영 방식은 두 명의 메인테이너가 범위와 아키텍처, 릴리스를 함께 책임지는 구조입니다. 기능을 만든 사람이 테스트와 증거까지 준비하고 상대가 리뷰합니다. 실제 팀원 이름과 개인별 고정 역할은 확인 전이라 단정하지 않았습니다. 오늘은 이 협업 방식과 프로젝트의 판단 기준을 중심으로 소개하겠습니다.
-->

---

<OperatorSlide section="문제 · 대상" index="03" total="17" source="README · Target-user hypothesis" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md#why-this-project">

<h1 class="op-title">먼저 돕고 싶은 사람은<br><span class="accent">CUBRID 운영자와 플랫폼 팀입니다.</span></h1><div class="op-two"><ul class="op-list"><li><b>DB 운영자</b><small>장애 뒤 어느 멤버의 역할과 데이터를 신뢰할지 판단</small></li><li><b>플랫폼 엔지니어</b><small>Pod·스토리지·접속 경로를 복구 절차와 연결</small></li></ul><div class="op-boundary"><p class="op-lead">반복하는 운영 판단을<br>선언·상태·재현 가능한 절차로.</p></div></div><p class="op-caption">대상 사용자 가설 · 실제 운영 환경과 우선 과제는 사용자 피드백으로 검증합니다.</p>

</OperatorSlide>

<!--
[35초 · 문제 · 대상]
먼저 돕고 싶은 사용자는 Kubernetes에서 CUBRID를 운영하려는 DB 운영자와 플랫폼 팀입니다. DB 운영자는 장애 뒤 어떤 멤버가 master인지, 돌아온 데이터가 믿을 만한지 판단해야 합니다. 플랫폼 팀은 Pod와 스토리지, 서비스의 수명주기를 맞춰야 합니다. 이 두 업무가 만나는 부분을 프로젝트의 대상으로 보고 있습니다. 다만 실제 인터뷰로 수요가 검증됐다는 주장은 하지 않습니다.
-->

---

<OperatorSlide section="문제 · 상태" index="04" total="17" source="DESIGN §4.3 · Database-aware health" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#43-database-aware">

<h1 class="op-title">Pod가 살아 있어도,<br><span class="accent">DB가 안전한 것은 아닙니다.</span></h1><div class="op-two"><div class="op-stack"><div class="op-path"><div class="op-node ">Pod 0<small>Ready</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Pod 1<small>Ready</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Pod 2<small>Ready</small></div></div><p class="op-caption">상황 예시: Kubernetes에서 관찰한 준비 상태</p></div><ul class="op-list"><li><b>현재 master는 하나인가?</b><small>Pod 상태와 DB 역할은 다른 관찰입니다.</small></li><li><b>복제는 따라오고 있는가?</b><small>프로세스 생존과 로그 적용은 다른 문제입니다.</small></li><li><b>돌아온 데이터를 다시 써도 되는가?</b><small>재시작 성공만으로 재합류를 판단할 수 없습니다.</small></li></ul></div>

</OperatorSlide>

<!--
[35초 · 문제 · 상태]
예를 들어 세 Pod가 모두 Ready여도 데이터베이스가 안전하다고 결론 내릴 수는 없습니다. master가 하나인지, 복제가 따라오는지, 장애 후 돌아온 멤버의 데이터를 재사용해도 되는지는 별도 관찰이 필요합니다. Kubernetes의 준비 상태를 무시하겠다는 뜻이 아니라, 그 위에 데이터베이스 고유의 판단 근거를 연결하겠다는 뜻입니다.
-->

---

<OperatorSlide section="현재 방식과 남는 질문" index="05" total="17" source="Official Operator · Pinned source audit" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">이미 있는 도구에서,<br><span class="accent">운영 검증의 질문으로.</span></h1><table class="op-comparison"><thead><tr><th>현재 방식</th><th>이미 제공하는 것</th><th>우리가 검증할 질문</th></tr></thead><tbody><tr><td>YAML·스크립트</td><td>리소스와 설정 배포</td><td>장애 뒤 어떤 상태로 복귀하는가?</td></tr><tr><td>공식 CUBRID Operator</td><td>HA 역할 관찰·스토리지·예약 백업</td><td>관찰 누락·불일치를 어떻게 판단하는가?</td></tr><tr><td>CUBRID native HA</td><td>복제와 역할 전환</td><td>Kubernetes 수명주기와 어떻게 연결하는가?</td></tr></tbody></table><p class="op-caption">공식 Operator도 DB 역할을 관찰합니다. 포트 리슨 검사 자체는 SQL 성공·복제 일치의 증명이 아닙니다.</p>

</OperatorSlide>

<!--
[35초 · 현재 방식과 남는 질문]
공식 CUBRID Operator는 이미 있습니다. 배포만 하는 도구라고 설명하면 부정확합니다. 실제 HA 역할과 Broker 포트를 관찰하고 스토리지와 백업도 다룹니다. 저희가 추가로 검증하려는 것은 관찰이 불완전할 때의 판단, 실제 SQL의 성공, 장애 후 데이터 일치입니다. 공식 구현을 실행해 우열을 측정한 것은 아니므로, 공개 코드에서 확인한 기능과 이 실험의 질문을 구분하겠습니다.
-->

---

<OperatorSlide section="제안 · 선언과 관찰" index="06" total="17" source="DESIGN §2–4" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals">

<h1 class="op-title">원하는 상태는 선언하고,<br><span class="accent">실제 상태는 계속 확인합니다.</span></h1><div class="op-path"><div class="op-node project">운영 의도<small>CubridCluster</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">관찰<small>역할 · 복제 · 접속</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">조정<small>리소스 · 작업 수명주기</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">상태 보고<small>Conditions · Events</small></div></div><p class="op-caption">CUBRID HA의 책임을 보존하면서 Kubernetes 수명주기와 연결합니다.</p>

</OperatorSlide>

<!--
[25초 · 제안 · 선언과 관찰]
해결 방법의 중심은 선언과 관찰의 반복입니다. 사용자가 운영 의도를 선언하면 Operator는 DB 상태와 Kubernetes 상태를 함께 읽고 자원과 작업을 조정합니다. 그리고 무엇을 확인했고 무엇을 아직 모르는지 상태로 드러냅니다. 엔진의 HA 결정을 대신하는 것이 아니라 두 수명주기의 접점을 조정하는 제어면입니다.
-->

---

<OperatorSlide section="제안 · 사용자 경험" index="07" total="17" source="DESIGN §2 · API example excerpt" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals">

<h1 class="op-title">사용자는 <span class="accent">운영 의도</span>를 적습니다.</h1><div class="op-two"><pre class="op-code"><code>apiVersion: database.cubrid.io/v1alpha1
kind: CubridCluster
metadata: {name: app-db}
spec:
  version: &quot;11.4&quot;
  databases: [{name: appdb}]
  highAvailability: {enabled: true}
  topology: {promotableMembers: 3}
  storage:
    data: {size: 100Gi}</code></pre><ul class="op-list"><li><b>데이터베이스와 버전</b><small>appdb · CUBRID 11.4</small></li><li><b>HA 멤버 풀</b><small>승격 가능한 멤버 3개 · master는 런타임 결정</small></li><li><b>데이터 수명주기</b><small>PVC 크기와 보존·복구 정책을 선언</small></li></ul></div><p class="op-caption">설명용 발췌 · HA의 오브젝트 스토리지·Secret 등 필수 설정은 생략했습니다.</p>

</OperatorSlide>

<!--
[40초 · 제안 · 사용자 경험]
사용자는 이처럼 데이터베이스, 버전, HA 멤버 수와 저장소를 선언합니다. 세 멤버 중 누가 master인지를 선언하는 API는 아닙니다. 그 역할은 런타임에서 CUBRID가 결정합니다. 화면은 개념을 설명하기 위한 발췌이고, 실제 HA 구성에는 데이터 복제를 시작하기 위한 오브젝트 스토리지와 Secret 같은 설정이 더 필요합니다. 한 번 생성된 리소스뿐 아니라 이후의 상태도 계속 관찰하는 것이 목표입니다.
-->

---

<OperatorSlide section="아키텍처 · 구성 요소" index="08" total="17" source="DESIGN §7, §9, §10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">한 장으로 보면</h1><div class="op-stack"><div class="op-path"><div class="op-node ">CubridCluster<small>Kubernetes API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator<small>관찰 · 리소스 조정</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Kubernetes 자원<small>StatefulSet · Service · PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">DB 멤버 · CUBRID native HA</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>멤버 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 2 · PVC</small></div></div></div><div class="op-stack"><p class="op-kicker">분리된 접속 계층</p><div class="op-node ">Broker tier<small>중복 RW / RO Broker</small></div><div class="op-node storage">Object storage<small>bootstrap · backup · restore</small></div></div></div></div><p class="op-caption">IM은 DB 컨테이너의 통합 supervisor입니다. 별도 sidecar가 아니며, Operator와 인증된 HTTP API로 통신합니다.</p>

</OperatorSlide>

<!--
[55초 · 아키텍처 · 구성 요소]
전체 구조는 이렇습니다. 위쪽에서 CubridCluster가 Kubernetes API로 들어오고, Operator가 StatefulSet과 Service, PVC 같은 자원과 각 멤버의 작업을 조정합니다. 아래에는 CUBRID 세 멤버가 있고 각자 PVC를 가집니다. Instance Manager는 각 DB 컨테이너 안의 통합 supervisor이며, 인증된 HTTP API로 로컬 CUBRID 작업과 관찰을 제공합니다. Broker는 DB Pod와 분리된 접속 계층이고 RW와 RO를 중복 구성합니다. 오브젝트 스토리지는 초기 멤버 복제와 백업·복구 아티팩트의 경로입니다. master 역할을 특정 ordinal에 고정하지 않습니다.
-->

---

<OperatorSlide section="아키텍처 · 두 경로" index="09" total="17" source="DESIGN §9–10 · ADR-0002" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL은 Broker로,<br><span class="accent">제어는 Instance Manager로.</span></h1><div class="op-stack"><p class="op-kicker">데이터 경로 · 애플리케이션의 SQL</p><div class="op-path"><div class="op-node ">Application</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">RW / RO Service</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Broker</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>SQL 실행</small></div></div><p class="op-kicker">제어 경로 · 의도와 작업</p><div class="op-path"><div class="op-node ">CubridCluster</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Instance Manager<small>인증된 HTTP API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>로컬 작업 · 상태</small></div></div></div><p class="op-caption">역할·작업 관찰은 Operator의 Conditions·Events·Metrics로 이어집니다. 데이터 경로와 제어 경로를 분리합니다.</p>

</OperatorSlide>

<!--
[40초 · 아키텍처 · 두 경로]
아키텍처에서 구분할 것은 두 경로입니다. 애플리케이션의 SQL은 안정적인 RW와 RO Service를 거쳐 Broker와 CUBRID로 갑니다. 운영 의도와 제어 작업은 Kubernetes API, Operator, Instance Manager로 흐릅니다. Operator는 관찰을 Conditions와 Events, 지표로 돌려줍니다. SQL 경로가 Operator에 의존하도록 만들지 않고, 엔진과 Broker가 맡는 일을 유지하는 구분입니다.
-->

---

<OperatorSlide section="안전 · 책임 경계" index="10" total="17" source="ADR-0005 · ROADMAP evidence boundary" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/adr/0005-failover-split-brain.md">

<h1 class="op-title">승격은 <span class="accent">CUBRID가 결정합니다.</span></h1><div class="op-two"><ul class="op-list"><li><b>CUBRID native HA</b><small>복제 · 역할 전환</small></li><li><b>Operator</b><small>관찰 · 상태 판단 · Kubernetes 자원 조정</small></li></ul><div class="op-stack"><div class="op-node ">master 1개 + 모두 관찰됨<small>유일한 master를 확인</small></div><div class="op-node project">관찰 누락 / master 여러 개<small>판단 보류 · 모호함 보고</small></div></div></div><p class="op-caption">ordinal 0 고정 master, 임의 승격, 갈라진 데이터 중 승자 선택을 하지 않습니다. SQL 쓰기 격리의 달성과는 별개입니다.</p>

</OperatorSlide>

<!--
[45초 · 안전 · 책임 경계]
여기서 책임의 경계가 중요합니다. 복제와 역할 전환은 CUBRID native HA가 맡습니다. Operator는 모든 멤버의 관찰을 확인하고 상태와 Kubernetes 자원을 조정합니다. 한 멤버가 안 보이거나 master가 여러 개면 임의로 승자를 고르지 않습니다. ordinal 0을 영구 master로 간주하지도 않습니다. 이 원칙은 Operator가 근거 없이 역할을 바꾸지 않게 하는 설계입니다. 이것만으로 실제 SQL 쓰기 격리가 완성됐다고 말하지는 않습니다.
-->

---

<OperatorSlide section="복구 · 수명주기" index="11" total="17" source="ADR-0006, 0008 · ROADMAP" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#v01-scope">

<h1 class="op-title">복구는 <span class="accent">재시작보다 긴 과정입니다.</span></h1><div class="op-stack"><div class="op-path"><div class="op-node ">PVC 유지 멤버<small>기존 데이터</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">역할·로그·데이터 검증</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">재합류<small>검증 후 진행</small></div></div><div class="op-path"><div class="op-node ">PVC 유실<small>데이터 없음</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">명시적 rebuild</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">멤버 복원</div></div><div class="op-path"><div class="op-node ">백업 아티팩트</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">새 클러스터 bootstrap</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">데이터 확인</div></div></div><p class="op-caption">설계·첫 버전 요구사항입니다. 통합 재합류·재구축·백업/복구 검증은 남은 과제입니다.</p>

</OperatorSlide>

<!--
[40초 · 복구 · 수명주기]
복구를 Pod 재시작 하나로 표현하면 중요한 구분이 사라집니다. 데이터가 남은 멤버는 역할과 로그, 데이터 상태를 확인한 뒤 재합류해야 합니다. PVC를 잃었다면 명시적으로 재구축해야 합니다. 백업에서 복원할 때는 새 클러스터를 만드는 경로로 다룹니다. 이 그림은 현재 설계와 첫 버전의 요구사항이며, 이 전체 흐름이 실제 환경에서 검증 완료됐다는 뜻은 아닙니다.
-->

---

<OperatorSlide class="op-compact" section="진행 상황 · 증거" index="12" total="17" source="ROADMAP · Snapshot 2026-10-15" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#implementation-and-validation-inventory">

<h1 class="op-title">확인한 것과,<br><span class="accent">아직 확인할 것을 나눕니다.</span></h1><div class="op-evidence"><div><h3>Kind CI에 기록된 시나리오</h3><ul class="op-list"><li><b>S00 · 단일 DB</b><small>실제 SQL · Pod 교체 뒤 데이터 유지</small></li><li><b>S01–S03 · HA와 master Pod 장애</b><small>3멤버 복제 · RW/RO · 트랜잭션 확인</small></li><li><b>S05·S06·S14</b><small>Broker/Operator 장애 · 인증·네트워크·토큰</small></li></ul></div><div><h3>릴리스까지 남은 검증</h3><ul class="op-list"><li><b>쓰기 격리 · 재합류 · 재구축</b><small>기존 연결을 포함한 실제 SQL 동작</small></li><li><b>백업 · 새 클러스터 복원</b><small>아티팩트와 데이터셋 검증</small></li><li><b>VM 장애 · 참조 환경</b><small>Kind를 넘어서는 실제 환경 근거</small></li></ul></div></div><p class="op-boundary"><b>현재 쓰기 격리는 상태 보고까지입니다.</b> SQL 차단이 검증된 상태로 발표하지 않습니다.</p>

</OperatorSlide>

<!--
[35초 · 진행 상황 · 증거]
실제 진행 상황도 구분해서 말씀드리겠습니다. 로드맵에는 Kind에서 실제 CUBRID로 단일 DB, HA와 복제, master Pod와 Broker, Operator 장애, 인증 관련 시나리오를 검증하는 기록이 있습니다. 반면 상태가 불확실하다고 보고하는 동안에도 RW 쓰기가 계속된 관찰이 있습니다. 따라서 쓰기 격리는 보고와 실제 차단을 구분해야 합니다. VM 장애와 재합류, 백업·복구의 통합 증거도 릴리스까지 해결해야 할 과제입니다.
-->

---

<OperatorSlide section="12주 로드맵" index="13" total="17" source="ROADMAP · STP IV delivery stages" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">12주를 <span class="accent">검증 가능한 결과</span>로 나눕니다.</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>범위와 기준</b><p>시나리오·환경 확정<br>단일 DB 실제 SQL</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA alpha</b><p>3멤버 HA·RW/RO<br>백업·복구 알파</p></div><div><small>5–8주 · 11.02–11.29</small><b>복구 검증</b><p>쓰기 격리<br>재합류·재구축</p></div><div><small>9–12주 · 11.30–12.27</small><b>릴리스 준비</b><p>반복 실험·회귀 수정<br>재현 문서·증거</p></div></div><p class="op-caption">2026.10.05–12.27 · 완료 표시가 아닌 목표 일정입니다. 필수 안전 게이트를 일정 때문에 줄이지 않습니다.</p>

</OperatorSlide>

<!--
[40초 · 12주 로드맵]
시즌은 10월 5일부터 12월 27일까지 12주입니다. 첫 주는 범위와 시나리오 기준, 환경을 정리합니다. 2주에서 4주는 세 멤버 HA와 접속 경로, 백업·복구 알파를 목표로 합니다. 5주에서 8주는 쓰기 격리와 재합류, 재구축의 실제 검증에 집중합니다. 마지막 네 주는 반복 실험, 회귀 수정과 다른 사람이 재현할 수 있는 문서, 릴리스 증거를 준비합니다. 날짜가 지났다는 이유로 완료로 표시하지는 않습니다.
-->

---

<OperatorSlide section="팀원별 역할과 협업" index="14" total="17" source="ROADMAP · Two-maintainer start order" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#two-maintainer-start-order">

<h1 class="op-title">작성자가 검증하고,<br><span class="accent">서로 리뷰합니다.</span></h1><div class="op-stack"><div class="op-path"><div class="op-node ">런타임 작업<small>기능 작성자</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">구현 + 테스트</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">상대 메인테이너 리뷰</div></div><div class="op-path"><div class="op-node ">검증 작업<small>시나리오 작성자</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">장애 주입 + 증거</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">상대의 기대 결과 검토</div></div></div><p class="op-boundary"><b>개인별 고정 배정 대신 이슈마다 담당을 정합니다.</b> 1인 1개 이슈 · 전체 VM 랩 실험은 한 번에 하나.</p>

</OperatorSlide>

<!--
[30초 · 팀원별 역할과 협업]
팀원별 역할은 기능과 테스트를 사람별로 분리하는 방식이 아닙니다. 각 이슈의 작성자가 구현과 테스트를 함께 책임지고, 상대가 실패 경로와 기대 결과를 검토합니다. 런타임, 검증 인프라, 공유 랩은 작업 흐름이지 세 명의 고정 담당자를 뜻하지 않습니다. 한 사람은 하나의 이슈에 집중하고, 세 VM 전체를 사용하는 실험은 한 번에 하나씩 진행합니다. 개인별 고정 역할은 팀 합의가 확인되면 반영하겠습니다.
-->

---

<OperatorSlide section="첫 공개 버전의 범위" index="15" total="17" source="ROADMAP · Required / Conditional / Future" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#v01-scope">

<h1 class="op-title">첫 공개 버전은 <span class="accent">경계부터 명확하게.</span></h1><div class="op-release"><div><h3>필수 · 증거로 완료</h3><ul class="op-list"><li><b>수명주기 · HA · RW/RO</b><small>장애 · 쓰기 격리 · 재합류 · 재구축</small></li><li><b>백업 · 새 클러스터 복원</b><small>보존 · 인증 · 자발적 중단 정책</small></li><li><b>관측 · 재현 가능한 검증</b><small>S00–S15 · 릴리스 증거</small></li></ul></div><div><h3>조건부</h3><ul class="op-list"><li><b>호환 이미지·설정 업데이트</b><small>필수 복구 검증 이후</small></li><li><b>디스크 가득 참</b><small>크기 제한·복구 경로가 검증될 때</small></li></ul></div><div><h3>초기 범위 밖</h3><ul class="op-list"><li><b>엔진 버전 마이그레이션</b><small>비승격 replica 확장</small></li><li><b>넓은 환경 지원</b><small>다중 존·다중 플랫폼 보장</small></li></ul></div></div><p class="op-caption">초기 참조 목표: CUBRID 11.4.x / amd64 + 하나의 Kubernetes·CSI 구성. 필수 증거가 없으면 v0.1 완료로 선언하지 않습니다.</p>

</OperatorSlide>

<!--
[40초 · 첫 공개 버전의 범위]
첫 공개 버전은 기능 수보다 검증 경계로 설명하겠습니다. 수명주기와 HA, 접속, 장애와 쓰기 격리, 재합류와 재구축, 백업과 새 클러스터 복원, 보존과 인증, 관측과 재현 증거가 필수입니다. 호환 업데이트와 디스크 가득 참은 추가 게이트를 충족해야 합니다. 엔진 버전 이동이나 넓은 플랫폼 지원은 초기 범위 밖입니다. 참조 환경은 하나로 고정하고, 필수 증거가 부족하면 달력에 맞추려고 v0.1 완료로 선언하지 않습니다.
-->

---

<OperatorSlide section="함께 논의하고 싶은 것" index="16" total="17" source="README · ROADMAP · Scenario contracts" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/testing/scenario-contract.md">

<h1 class="op-title">이 세 가지를 <span class="accent">함께 검증하고 싶습니다.</span></h1><ol class="op-questions"><li>가장 먼저 줄여야 할 CUBRID 운영 업무는 무엇인가요?</li><li>쓰기 격리·복구의 합격 기준은 충분한가요?</li><li>참조 환경과 운영 문서를 함께 재현해 볼 수 있나요?</li></ol><p class="op-caption">대상 사용자·문제 우선순위, 실패 시 판단 기준, 외부 재현 경험을 구합니다.</p>

</OperatorSlide>

<!--
[35초 · 함께 논의하고 싶은 것]
오늘 세 가지에 대해 의견을 구하고 싶습니다. 첫째, 실제 CUBRID 운영에서 가장 먼저 줄이고 싶은 반복 업무는 무엇인지입니다. 둘째, 기존 연결까지 포함한 쓰기 격리와 복구의 합격 기준이 운영 관점에서 충분한지입니다. 셋째, 하나의 참조 환경과 문서를 다른 운영자가 함께 재현해 볼 수 있을지입니다. 이 피드백으로 12주 동안 검증할 문제의 순서와 판단 기준을 더 분명하게 만들고 싶습니다.
-->

---

<OperatorSlide section="마무리" index="17" total="17" source="Project · Experimental" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md">

<div class="op-cover"><p class="op-kicker">CUBRID KUBERNETES OPERATOR</p><h1 class="op-title">배포 가능한 DB에서,<br><span class="accent">운영을 설명할 수 있는 DB로.</span></h1><p class="op-lead">상태를 관찰하고, 책임을 구분하고,<br>복구 결과를 실제 SQL과 증거로 확인하겠습니다.</p><div class="op-meta"><b>Experimental project</b><a href="https://github.com/cubrid-lab/cubrid-kubernetes-operator">github.com/cubrid-lab/cubrid-kubernetes-operator</a></div></div>

</OperatorSlide>

<!--
[25초 · 마무리]
저희가 만들고 싶은 것은 한 번 배포할 수 있는 DB에서, 장애 이후의 상태와 복구 과정을 설명할 수 있는 DB 운영 경험으로 가는 도구입니다. CUBRID가 잘하는 HA를 보존하고, Kubernetes와 만나는 판단과 절차를 증거로 검증하겠습니다. 공개된 설계와 시나리오를 함께 검토해 주시면 좋겠습니다. 감사합니다.
-->
