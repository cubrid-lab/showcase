---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="1 · 프로젝트·팀 소개" index="01" total="11" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID Kubernetes<br>Operator</h1><p class="op-lead">CUBRID 설치부터 장애 복구까지,<br>Kubernetes에서 관리하려고 합니다.</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div><p class="op-caption">첫 버전은 12월 27일 공개를 목표로 하고 있습니다.</p></div>

</OperatorSlide>

<!--
[40초 · 1 · 프로젝트·팀 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저희는 관계형 DBMS인 CUBRID를 Kubernetes에서 관리하는 Operator를 만들고 있습니다. 설치뿐 아니라 장애가 난 뒤 복구하는 과정까지 다루려고 합니다.

이번 시즌에는 환경 하나를 정해서 직접 설치하고, 장애를 내고, 복구되는 것까지 확인한 v0.1을 내는 게 목표입니다. 먼저 어떤 문제를 풀려는지 말씀드리겠습니다.
-->

---

<OperatorSlide section="2 · 문제와 대상" index="02" total="11" source="문제와 사용자" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">Pod가 다시 떠도<br>확인할 일은 남습니다</h1><div class="op-two"><div class="op-stack"><p class="op-kicker">DB 멤버에 장애가 났다면</p><ul class="op-list"><li><b>Pod와 볼륨부터 확인</b><small>플랫폼 팀이 보는 Kubernetes 상태</small></li><li><b>DB 안쪽도 확인</b><small>DB 운영자가 보는 역할·복제·데이터</small></li></ul></div><div class="op-stack"><p class="op-kicker">복구됐다고 보기 전에</p><ul class="op-list"><li><b>지금 master가 누구인지</b><small>어느 멤버가 쓰기를 받는가?</small></li><li><b>커밋한 데이터가 남았는지</b><small>기존 행과 새로 쓴 행이 보이는가?</small></li><li><b>실제 접속도 잘되는지</b><small>RW로 쓰고 RO로 읽을 수 있는가?</small></li></ul></div></div><p class="op-caption">이 일을 맡는 CUBRID DB 운영자와 Kubernetes 플랫폼 팀을 먼저 생각하고 있습니다.</p>

</OperatorSlide>

<!--
[65초 · 2 · 문제와 대상]
DB가 있던 노드에 장애가 나서 Pod가 다시 떴다고 해보겠습니다. Pod가 Ready이고 볼륨도 붙었습니다. 그런데 그것만 보고 DB도 복구됐다고 말할 수 있을까요?

지금 master가 누구인지, 커밋한 행이 남아 있는지, RW로 쓴 행이 RO에서도 보이고, RO 쓰기는 거부되는지도 봐야 합니다. 플랫폼 팀은 Pod와 볼륨을 보고, DB 운영자는 역할과 복제, 데이터를 봅니다. 두 쪽을 함께 확인해야 하는 일입니다. 저희는 우선 이런 일을 맡는 운영자와 플랫폼 팀을 생각하고 있습니다. 현장에서 어떤 확인이 가장 번거로운지도 더 들어보고 싶습니다.
-->

---

<OperatorSlide class="op-compact" section="3 · 현재 방식과 한계" index="03" total="11" source="공식 Operator·소스 비교" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">기존 Operator와 다른 점</h1><table class="op-comparison"><thead><tr><th>비교할 부분</th><th>공식 Operator</th><th>이번 프로젝트</th></tr></thead><tbody><tr><td>HA 상태 조회</td><td>처음 성공한 CMS 응답의 노드 정보</td><td>각 멤버의 최신 상태 비교<br>응답이 없거나 모순되면 master 미확정</td></tr><tr><td>오래 걸리는 작업</td><td>예약 백업을 Pod exec로 실행<br>백업 상태 기록</td><td>IM API로 요청·작업 ID를 PVC에 기록<br>중단된 작업은 실패로 기록</td></tr><tr><td>백업 설정</td><td>대상 Pod·스크립트·저장소 지정</td><td>대상·요청 ID 보관<br>복원할 파일 목록·체크섬 확인</td></tr></tbody></table><p class="op-caption">공식 Operator도 HA·스토리지·예약 백업을 지원합니다. 확인한 소스 버전을 기준으로 비교했습니다.</p><p class="op-boundary">실제 SQL과 데이터도 별도로 검사합니다.</p>

</OperatorSlide>

<!--
[65초 · 3 · 현재 방식과 한계]
CUBRID에는 이미 HA가 있고 공식 Operator도 있습니다. 공식 Operator도 HA 상태를 보고 스토리지와 예약 백업을 관리합니다. 저희는 특히 응답이 안 오거나 작업이 중간에 끊겼을 때 어떻게 처리할지에 집중하고 있습니다.

표는 확인한 소스 기준입니다. CMS는 CUBRID Manager Server입니다. 공식 구현은 처음 성공한 CMS 응답의 노드 정보를 쓰고, 저희 쪽은 각 멤버의 최신 상태를 받아 비교합니다. 응답이 없거나 역할 정보가 서로 모순되면 master를 확정하지 않습니다. 백업 같은 작업은 Instance Manager, 줄여서 IM에 HTTP로 요청하고 작업 ID를 PVC에 기록합니다. IM이 다시 시작했을 때 끝나지 않은 작업은 실패로 남깁니다. 작업이 자동으로 이어진다는 뜻은 아닙니다.

실제 장애에서 어느 쪽이 더 안정적인지는 아직 비교하지 못했습니다. 두 쪽 모두 포트 검사를 쓰기 때문에 SQL과 데이터도 따로 확인합니다.
-->

---

<OperatorSlide section="4 · 제안하는 해결 방법" index="04" total="11" source="10월 20일 시험 결과" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">YAML로 구성을 정하고,<br>DB 상태와 작업 결과를 확인합니다</h1><div class="op-path"><div class="op-node project">YAML로 설정<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">DB 상태 조회<small>역할·복제·접속</small></div><div class="op-arrow">→</div><div class="op-node project">작업 요청·조회<small>작업 ID·진행·결과</small></div><div class="op-arrow">→</div><div class="op-node">상태 갱신<small>Conditions·Events</small></div></div><div class="op-evidence"><div><p class="op-kicker">여기까지 해봤습니다</p><p>Kind 테스트 27개 통과<br>VM에서 기존 행 보존·RW/RO SQL 확인</p></div><div><p class="op-kicker">아직 남은 일</p><p>VM 장애·네트워크 분할 때의 쓰기 차단<br>재합류·재구축·백업 복원·CSI 시험</p></div></div><p class="op-caption">DB 상태와 작업 결과를 Kubernetes에서 확인할 수 있게 만드는 것이 목표입니다.</p>

</OperatorSlide>

<!--
[60초 · 4 · 제안하는 해결 방법]
사용자는 YAML에 원하는 구성을 적습니다. Operator가 DB 상태를 읽고 필요한 작업을 요청한 뒤, 진행 상황과 결과를 갱신합니다. 백업처럼 오래 걸리는 작업은 ID로 다시 찾아볼 수 있게 합니다. 작업 기록을 읽을 수 없으면 새 작업을 임의로 시작하지 않게 하는 것도 중요한 부분입니다.

지금까지는 Kind 테스트 27개가 통과했고, VM에서도 기존 행이 남아 있는 것과 RW로 쓴 데이터를 RO에서 읽는 것, RO 쓰기가 거부되는 것을 확인했습니다. 여기서 27개는 테스트 spec 수입니다. 필수 시나리오 전체를 끝냈다는 뜻은 아닙니다. VM 전원 장애, 네트워크 분할, 재합류와 재구축, 실제 백업 복원, CSI 시험은 더 해야 합니다. 수치는 10월 20일에 확인한 결과를 가져왔습니다.
-->

---

<OperatorSlide class="op-compact" section="5 · 아키텍처 초안" index="05" total="11" source="구성도" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID, Operator, IM이 하는 일</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>상태 조회·리소스 관리</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes 리소스<small>StatefulSet·Service·PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID HA가 복제와 master 전환을 담당</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>멤버 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 2 · PVC</small></div></div></div><div class="op-stack"><div class="op-node">Broker<small>DB와 분리된 RW / RO 접속</small></div><div class="op-node storage">백업 저장소<small>S3 호환 · 초기 복사·백업·복원</small></div></div></div><p class="op-caption">IM은 DB 컨테이너 안에서 HTTP API로 작업을 받고 PVC에 기록합니다.<br>누가 master가 될지는 CUBRID가 정합니다.</p>

</OperatorSlide>

<!--
[70초 · 5 · 아키텍처 초안]
구성은 크게 Operator, DB 멤버와 IM, Broker, 백업 저장소입니다. Operator는 Kubernetes API를 통해 StatefulSet과 Service, PVC를 관리합니다. 각 DB 컨테이너 안에는 CUBRID와 IM이 같이 들어갑니다. IM은 별도 sidecar가 아니라 DB 컨테이너 안에서 실행되는 supervisor입니다.

DB를 시작하거나 백업 같은 로컬 작업을 할 때 IM의 인증된 HTTP API를 사용합니다. IM은 작업 ID와 상태를 PVC에 남깁니다. Broker는 DB와 따로 두고 RW와 RO 접속을 받습니다. 초기 데이터 복사와 백업·복원 파일은 S3 호환 저장소를 거칩니다.

복제와 master 전환은 CUBRID가 맡습니다. 멤버 0을 항상 master로 두는 것도 아닙니다. Operator가 임의로 master를 승격하거나, 갈라진 데이터 중 하나를 골라 덮어쓰지는 않습니다.
-->

---

<OperatorSlide class="op-compact" section="5 · 데이터와 제어 흐름" index="06" total="11" source="SQL과 운영 요청" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL은 Broker로, 운영 요청은 IM으로</h1><div class="op-stack"><p class="op-kicker">애플리케이션에서 SQL을 실행할 때</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">설정을 바꾸거나 DB 작업을 요청할 때</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">IM API<small>로컬 작업·작업 기록</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / PVC</div></div></div><p class="op-boundary"><b>master 장애 후 확인할 순서</b><br>엔진 역할 전환 → IM에서 조회 → Operator 상태 갱신 → SQL·데이터 확인</p><p class="op-caption">네트워크가 갈라졌을 때의 쓰기 차단은 아직 남은 작업입니다.</p>

</OperatorSlide>

<!--
[60초 · 5 · 데이터와 제어 흐름]
애플리케이션의 SQL은 위쪽 경로로 갑니다. RW나 RO Service에서 Broker를 거쳐 CUBRID로 들어갑니다. Operator는 SQL을 중계하지 않습니다. 아래쪽은 설정을 읽거나 DB 작업을 요청하는 경로입니다. Operator가 IM API를 호출하고 결과를 상태에 반영합니다.

master에 장애가 났을 때도 CUBRID의 역할 전환을 먼저 봅니다. IM에서 각 멤버를 조회하고, Operator 상태가 맞게 바뀌는지, SQL과 데이터가 실제로 맞는지 확인해야 합니다. 여기서 아직 남은 중요한 일이 쓰기 차단입니다. Kind에서는 master를 확정하지 못한 동안에도 RW 쓰기 요청에 성공 응답이 돌아왔습니다. 상태에 불명확하다고 적는 것만으로 쓰기가 막히지는 않았습니다. 네트워크가 갈라졌을 때의 쓰기 차단을 구현하고 실제 접속으로 확인해야 합니다.
-->

---

<OperatorSlide section="6 · 12주 로드맵" index="07" total="11" source="개발 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">11월 말까지 첫 전체 통과,<br>12월에는 반복 시험</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>기준 정하기</b><p>환경·시나리오 정리<br>단일 DB SQL 확인</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA와 실행 환경</b><p>3멤버·RW/RO<br>VM에서 실행<br>백업·복구 초기 시험</p></div><div><small>5–8주 · 11.02–11.29</small><b>장애·복구 시험</b><p>쓰기 차단·재합류<br>재구축·백업 복원<br>S00–S15 첫 통과 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>같은 RC로 반복</b><p>장애 반복·24시간 부하 목표<br>다른 사람이 문서대로 재현<br>문제 수정·배포 파일 정리</p></div></div><p class="op-boundary"><b>11.29</b> 필수 시나리오 첫 전체 통과 목표　→　<b>12.27</b> v0.1 공개 목표</p><p class="op-caption">어떤 커밋·이미지·환경에서 시험했는지, SQL 결과와 함께 남깁니다.</p>

</OperatorSlide>

<!--
[70초 · 6 · 12주 로드맵]
일정은 10월 5일부터 12월 27일까지 12주로 잡았습니다. 첫 주에는 환경과 시나리오를 정하고 단일 DB에서 SQL을 확인합니다. 2주부터 4주는 3멤버 HA와 RW/RO, VM 실행 환경과 백업·복구 초기 시험입니다. 지금 보여드린 Kind와 VM 결과도 이 단계에서 확인한 것들입니다.

11월 말, 정확히는 11월 29일까지 필수 시나리오를 한 번씩은 전부 통과시키는 게 목표입니다. 쓰기 차단, 재합류, 재구축, 백업에서 새 클러스터로 복원하는 것까지 들어갑니다. 12월에는 같은 RC로 장애 시험을 반복하고, 24시간 부하 시험과 다른 사람의 문서 재현을 해보려고 합니다. 나온 문제를 고치고 12월 27일 공개를 목표로 합니다. 어떤 커밋과 이미지로 시험했는지, 환경과 SQL 결과도 같이 남기겠습니다. 공개 여부는 이 시험 결과를 보고 판단하겠습니다.
-->

---

<OperatorSlide section="6 · 팀원별 역할" index="08" total="11" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">두 사람이 만들고 서로 리뷰합니다</h1><div class="op-meta"><b>최영선 @yeongseon</b><b>백경준 @paikend</b><span>공동 메인테이너</span></div><table class="op-comparison"><thead><tr><th>누가</th><th>무엇을 맡는지</th></tr></thead><tbody><tr><td>이슈를 맡은 사람</td><td>문제 재현부터 코드·테스트·문서·실험 기록까지</td></tr><tr><td>다른 한 사람</td><td>코드 리뷰와 실험 결과 확인</td></tr><tr><td>함께</td><td>설치·HA·복구 시험과 공개 여부 결정</td></tr></tbody></table><p class="op-caption">이슈마다 담당자를 정합니다. 공유 VM의 장애 시험은 한 번에 하나씩 진행합니다.<br>릴리스 전에는 다른 사람이 문서만 보고 설치·복구를 따라 해봅니다.</p>

</OperatorSlide>

<!--
[45초 · 6 · 팀원별 역할]
저희 둘이 함께 개발합니다. 이슈마다 담당자를 정합니다. 맡은 사람이 문제 재현부터 코드와 테스트, 문서, 실험 기록까지 준비하고 다른 한 사람이 리뷰합니다.

HA와 백업·복구, 설치 문서도 이 방식으로 진행합니다. VM 장애 시험은 같은 환경을 쓰기 때문에 한 번에 하나씩 합니다. 릴리스 전에는 다른 메인테이너가 문서만 보고 설치와 복구를 끝낼 수 있는지도 확인하겠습니다.
-->

---

<OperatorSlide class="op-compact" section="6 · 첫 버전 공개 범위" index="09" total="11" source="v0.1 범위" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1에서 공개할 것</h1><table class="op-comparison op-acceptance"><thead><tr><th>포함할 기능</th><th>어떻게 확인할지</th></tr></thead><tbody><tr><td>비루트·영속 DB<br>3멤버 HA·RW/RO</td><td>SQL을 실행하고 역할·커밋·데이터 확인</td></tr><tr><td>장애·쓰기 격리<br>재합류·재구축</td><td>Pod/VM/Broker/Operator 장애 뒤 상태와 데이터 확인</td></tr><tr><td>백업<br>새 클러스터 복원</td><td>백업으로 새 클러스터를 만들어 데이터 비교</td></tr><tr><td>보존·IM 인증<br>중단 정책·관측</td><td>S00–S15 시험과 설치·운영·복구 문서 재현</td></tr></tbody></table><p class="op-boundary"><b>함께 공개</b>　이미지·설치 매니페스트·지원 환경표·운영 문서·시험 결과</p><p class="op-caption">CUBRID 11.4.x / amd64 / Kubernetes·CSI 한 구성 · experimental · 호환 업데이트·disk-full 조건부</p>

</OperatorSlide>

<!--
[55초 · 6 · 첫 버전 공개 범위]
v0.1에서는 환경 하나를 정해서 설치부터 복구까지 확인하겠습니다. 3멤버 HA와 RW/RO에서 SQL을 실행하고, 장애를 낸 뒤 데이터와 역할을 확인합니다. 재합류와 재구축에서는 정상 데이터를 덮어쓰지 않아야 합니다. 백업으로 새 클러스터를 만들었을 때는 미리 준비한 데이터와 맞는지 비교합니다. 보존 정책과 IM 인증, 노드 중단 정책, 상태와 지표도 확인해야 합니다.

이미지와 설치 매니페스트, 지원 환경표, 운영 문서와 시험 결과를 함께 공개하려고 합니다. CUBRID 11.4.x와 amd64, Kubernetes와 CSI 한 구성이 기준입니다. 현재 VM은 local-path여서 CSI 시험은 따로 해야 합니다. 첫 버전은 experimental입니다. IM API 인증과는 별개로, 현재 DBA 암호는 비어 있고 통신도 암호화되지 않습니다. 호환 업데이트와 disk-full도 조건부로 남겨두었습니다.
-->

---

<OperatorSlide section="6 · v0.1 이후의 방향" index="10" total="11" source="v0.1 이후 계획" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">v0.1을 내고 나면</h1><div class="op-release"><div><h3>먼저, 써보면서 고치기</h3><ul class="op-list"><li><b>로그와 진단부터 손보기</b><small>반복되는 문제와 복구 절차 정리</small></li><li><b>실제로 쓰려면 필요한 기능</b><small>DB 인증·TLS·호환 업데이트</small></li></ul></div><div><h3>그다음, 지원 환경 늘리기</h3><ul class="op-list"><li><b>Kubernetes·CSI 조합 추가</b><small>조합마다 장애·복구 시험</small></li><li><b>arm64·여러 가용영역</b><small>지원 가능한지 별도로 확인</small></li></ul></div><div><h3>시간이 더 필요한 일</h3><ul class="op-list"><li><b>CUBRID 버전 변경</b><small>데이터 호환·중단·되돌리는 방법</small></li><li><b>복제 구성 추가</b><small>master로 승격되지 않는 읽기 복제본 등</small></li></ul></div></div><p class="op-boundary">v0.1을 먼저 검증하고, 사용자들이 어디에서 불편한지 본 뒤 우선순위를 정하려고 합니다.</p><p class="op-caption">후속 버전과 일정은 아직 정하지 않았습니다. v0.1의 필수 작업부터 끝내겠습니다.</p>

</OperatorSlide>

<!--
[40초 · 6 · v0.1 이후의 방향]
첫 버전을 내고 나면 실제로 써보면서 불편한 곳부터 고치고 싶습니다. 로그로 원인을 찾을 수 있는지, 복구 절차를 따라갈 수 있는지부터 보려고 합니다. DB 인증과 TLS, 호환 업데이트처럼 실제 도입에 필요한 기능도 검증해야 합니다.

그다음에는 Kubernetes와 CSI 조합을 하나씩 늘리고, 각 환경에서 장애와 복구를 다시 시험하겠습니다. arm64나 여러 가용영역에 걸친 구성은 별도로 확인할 일입니다. CUBRID 버전 변경과 master로 승격되지 않는 읽기 복제본을 추가하는 일도 길게 보고 있습니다. 후속 버전이나 날짜는 아직 정하지 않았습니다. 우선 v0.1의 필수 작업을 끝내고, 써본 분들의 의견을 받아 다음 순서를 정하려고 합니다.
-->

---

<OperatorSlide section="7 · 논의할 내용" index="11" total="11" source="의견·협력 요청" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">의견을 듣고 싶은 부분</h1><ol class="op-questions"><li>최근 장애를 떠올리면,<br>복구됐다고 판단하기 전에 무엇부터 확인하셨나요?</li><li>함께 시험할 Kubernetes·CSI 조합과<br>스토리지·장애 시험의 주의점을 알려주실 수 있나요?</li><li>12월에 설치·복구 문서를 따라 해보고,<br>막히는 부분을 알려주실 분이 계실까요?</li></ol>

</OperatorSlide>

<!--
[30초 · 7 · 논의할 내용]
마지막으로 운영 경험을 듣고 싶습니다. 최근 장애에서 무엇을 먼저 확인했고, 어떤 결과를 보고 복구됐다고 판단하셨는지 궁금합니다. 첫 시험 환경으로 쓸 Kubernetes와 CSI 조합, 스토리지나 장애 시험에서 주의할 점도 알려주시면 좋겠습니다.

12월에는 저희가 만든 설치·복구 문서를 다른 분이 따라 해봐 주셨으면 합니다. 어디에서 막히는지, 빠진 설명이 무엇인지 알려주시면 도움이 되겠습니다. 감사합니다.
-->
