---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="1 · 프로젝트·팀 소개" index="01" total="11" source="Project · Team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID Kubernetes<br>Operator</h1><p class="op-lead">Pod 복구 이후의 DB 상태와 운영 작업을<br>Kubernetes에서 함께 확인합니다.</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div><p class="op-caption">시즌 목표: 한정된 환경에서 설치·장애·복구를 재현하는 v0.1</p></div>

</OperatorSlide>

<!--
[40초 · 1 · 프로젝트·팀 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 관계형 DBMS CUBRID의 Kubernetes Operator를 함께 개발하고 있습니다. 이번 시즌의 목표는 DB를 컨테이너로 띄우는 데서 나아가, 장애 뒤에 DB 상태와 복구 작업을 확인할 수 있는 첫 버전을 공개하는 것입니다.

한 가지 질문을 따라 설명하겠습니다. Pod가 다시 떴을 때 운영자는 쓰기를 재개해도 될까요? 이 판단에 필요한 정보와 작업을 어떻게 연결할지, 지금 확인한 결과와 v0.1 이후의 방향까지 말씀드리겠습니다.
-->

---

<OperatorSlide section="2 · 문제와 대상" index="02" total="11" source="Problem · User hypothesis" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">Pod가 돌아왔습니다.<br>쓰기를 재개해도 될까요?</h1><div class="op-two"><div class="op-stack"><p class="op-kicker">운영 상황 예시</p><ul class="op-list"><li><b>DB 멤버 장애 → Pod 재생성</b><small>Ready만으로 서비스 복귀를 판단하기 어려움</small></li><li><b>두 팀이 함께 판단</b><small>DB 운영자: 역할·복제·데이터<br>플랫폼 팀: Pod·볼륨·Service</small></li></ul></div><div class="op-stack"><p class="op-kicker">복귀 전에 확인할 세 가지</p><ul class="op-list"><li><b>역할</b><small>현재 쓰기를 받는 master는 누구인가?</small></li><li><b>데이터</b><small>기존 행과 커밋한 쓰기가 남아 있는가?</small></li><li><b>접속</b><small>RW/RO에서 실제 SQL이 의도대로 동작하는가?</small></li></ul></div></div><p class="op-caption">대상 가설: Kubernetes에서 CUBRID를 운영하려는 DB 운영자·플랫폼 팀</p>

</OperatorSlide>

<!--
[65초 · 2 · 문제와 대상]
DB 멤버가 있던 노드에 장애가 나고 Pod가 재생성된 상황을 생각해 보겠습니다. 플랫폼 팀은 Pod가 Ready이고 볼륨이 연결됐다고 확인할 수 있습니다. 하지만 DB 운영자는 지금 누가 master인지, 복제와 기존 데이터는 어떤지, 실제 접속 경로로 읽고 쓸 수 있는지를 추가로 확인해야 합니다.

예를 들어 접속 포트가 열려 있어도, 그것만으로 직전에 커밋한 데이터가 모든 멤버에 있다고 판단할 수는 없습니다. 복구 완료를 판단할 정보가 Kubernetes 상태, DB 상태와 SQL 결과로 나뉘는 것이 저희가 풀려는 문제입니다. 초기 대상은 이 판단을 함께 해야 하는 DB 운영자와 플랫폼 팀입니다. 실제 고객 장애 사례나 인터뷰로 검증한 수요라고 주장하지 않으며, 이 운영 상황의 중요도를 이번 자리에서 확인하고 싶습니다.
-->

---

<OperatorSlide class="op-compact" section="3 · 현재 방식과 한계" index="03" total="11" source="Pinned upstream · Design" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">관찰과 작업의 실패 경계를 명시합니다</h1><table class="op-comparison"><thead><tr><th>설계 지점</th><th>공식 구현에서 확인</th><th>이번 설계</th></tr></thead><tbody><tr><td>HA 관찰</td><td>첫 성공 CMS 응답의 노드 정보</td><td>멤버별 최신 관찰 집계<br>누락·충돌 시 primary 미확정</td></tr><tr><td>장시간 작업</td><td>예약·Pod exec와 백업 상태 기록</td><td>IM HTTP API·PVC 영속 작업 ID<br>중단은 실패로 남겨 후속 판단</td></tr><tr><td>백업 정보</td><td>대상 Pod·스크립트·스토리지 지정</td><td>대상·요청 ID 기록<br>manifest·체크섬으로 복원 입력 검증</td></tr></tbody></table><p class="op-caption">공식 Operator도 HA 관찰·스토리지·예약 백업을 제공합니다. 고정 소스의 구현 모델 비교이며 안정성 우열을 뜻하지 않습니다.</p><p class="op-boundary"><b>공통 주의점</b>　포트·Ready 검사와 실제 SQL·데이터 검증은 별개입니다.</p>

</OperatorSlide>

<!--
[65초 · 3 · 현재 방식과 한계]
이미 CUBRID native HA와 공식 CUBRID Operator가 있습니다. native HA는 복제와 역할 전환을 담당하고, 공식 Operator도 HA 역할을 관찰하며 스토리지와 예약 백업을 제공합니다. 기존 도구에 HA나 백업이 없다는 설명은 정확하지 않습니다.

CMS는 기존 CUBRID Manager Server이고, IM은 이 프로젝트의 Instance Manager입니다. 저희가 별도 구조로 실험하는 부분은 DB 로컬 작업을 인증된 HTTP API와 영속 작업 ID로 관리하고, 중단 이후에도 같은 요청과 결과를 대조하는 방식입니다. 작업 기록을 읽지 못하면 새 작업을 임의로 시작하지 않는 등의 실패 경계도 중요합니다. 또한 상태 보고와 실제 SQL·데이터 검증을 분리합니다. 양쪽 Operator 모두 포트 기반 검사를 사용하므로 저희 Ready 상태가 곧 SQL 검증이라는 뜻은 아닙니다. 공식 프로젝트보다 안정적이라는 비교 결과는 없고, 구조와 검증 결과를 공개해 개선 논의의 근거로 삼으려 합니다.
-->

---

<OperatorSlide section="4 · 제안하는 해결 방법" index="04" total="11" source="Design · Recorded evidence" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">의도·관찰·작업 결과를<br>하나의 운영 흐름으로 연결합니다</h1><div class="op-path"><div class="op-node project">구성 선언<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">DB 관찰<small>역할·복제·접속</small></div><div class="op-arrow">→</div><div class="op-node project">작업 관리<small>작업 ID·진행·결과</small></div><div class="op-arrow">→</div><div class="op-node">상태 보고<small>Conditions·Events</small></div></div><div class="op-evidence"><div><p class="op-kicker">구현·확인한 근거</p><p>Kind 27/27 specs 통과<br>VM에서 알려진 행 보존·RW/RO SQL 확인</p></div><div><p class="op-kicker">아직 입증해야 할 결과</p><p>VM 장애·분할 시 쓰기 격리<br>재합류·재구축·백업 복원·CSI 검증</p></div></div><p class="op-caption">기대 가치: 운영자가 같은 상태·작업 기록과 재현 가능한 SQL 근거로 복귀를 판단</p>

</OperatorSlide>

<!--
[60초 · 4 · 제안하는 해결 방법]
사용자는 CubridCluster로 원하는 구성을 선언하고, Operator는 현재 DB 상태를 관찰해 Kubernetes 자원과 로컬 작업을 조정합니다. 장시간 작업은 단순 명령 실행 여부가 아니라 작업 ID와 진행 상태, 결과로 확인합니다. 중단된 작업은 실패로 남을 수 있으며, 영속 기록이 있다고 작업이 저절로 성공하거나 모든 작업이 자동 재개되는 것은 아닙니다.

코드 기준 39b1cb6과 연결된 Kind 실행에서는 27개 spec이 통과했습니다. 실제 VM Kubernetes에서도 단일 DB와 HA의 알려진 데이터 보존, 새 RW 커밋과 RO 읽기·쓰기 거부를 확인했습니다. 그러나 이 결과는 전체 필수 시나리오나 네트워크 분할, VM 장애와 CSI 검증의 완료가 아닙니다. 기대하는 변화는 운영자가 같은 상태와 작업 기록을 보고, 별도로 남긴 SQL·데이터 근거로 복귀 여부를 판단할 수 있게 하는 것입니다.
-->

---

<OperatorSlide class="op-compact" section="5 · 아키텍처 초안" index="05" total="11" source="DESIGN · ADR 0003 / 0005" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">역할 전환·자원 조정·DB 작업의<br>책임을 나눕니다</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>관찰·자원·작업 조정</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes 자원<small>StatefulSet·Service·PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID native HA · 복제와 역할 전환</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>멤버 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 2 · PVC</small></div></div></div><div class="op-stack"><div class="op-node">Broker tier<small>분리된 RW / RO 접속 계층</small></div><div class="op-node storage">Object storage<small>초기 복사·백업·복원</small></div></div></div><p class="op-caption">IM: DB 컨테이너 안의 supervisor · 인증된 HTTP API · PVC에 작업 기록<br>Operator는 master를 승격하거나 갈라진 데이터의 승자를 고르지 않습니다.</p>

</OperatorSlide>

<!--
[70초 · 5 · 아키텍처 초안]
플랫폼은 Kubernetes와 CUBRID native HA, S3 호환 오브젝트 스토리지입니다. Operator는 API에서 구성을 읽고 StatefulSet, Service와 PVC를 조정합니다. 각 DB 컨테이너에는 CUBRID와 Instance Manager가 함께 있습니다. IM은 별도 sidecar가 아니라 통합 supervisor이며, 인증된 HTTP API로 DB 로컬 작업과 작업 상태를 제공합니다.

이 분리에는 이유가 있습니다. 역할 전환과 복제는 엔진이 결정하고, Operator는 Kubernetes 수명주기를 연결합니다. 로컬 작업은 IM이 맡아 작업 ID와 PVC의 기록으로 추적합니다. Broker는 DB 멤버와 분리돼 RW/RO 접속을 제공하고, 오브젝트 스토리지는 초기 복사와 백업·복원 아티팩트를 전달합니다. 멤버 0이 영구 master인 구조가 아니며, 관찰이 부족할 때 Operator가 임의로 승격하거나 데이터의 승자를 고르지 않습니다.
-->

---

<OperatorSlide class="op-compact" section="5 · 데이터와 제어 흐름" index="06" total="11" source="DESIGN · Fault contract" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL과 운영 제어는 다른 경로로 흐릅니다</h1><div class="op-stack"><p class="op-kicker">데이터 · 애플리케이션의 SQL</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">제어 · 운영 의도와 멤버 작업</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">IM API<small>로컬 작업·작업 기록</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / PVC</div></div></div><p class="op-boundary"><b>master 장애 시 검증할 흐름</b><br>엔진 역할 전환 → IM 관찰 → Operator 상태 조정 → SQL·데이터 대조</p><p class="op-caption">상태 미확정 표시와 실제 쓰기 차단은 별개입니다. 분할 시 쓰기 격리는 필수 검증 과제입니다.</p>

</OperatorSlide>

<!--
[60초 · 5 · 데이터와 제어 흐름]
위쪽 데이터 경로에서는 애플리케이션의 SQL이 RW 또는 RO Service와 Broker를 거쳐 CUBRID로 갑니다. Operator가 SQL을 중계하지 않습니다. 아래 제어 경로에서는 운영 의도와 요청이 Operator를 거쳐 IM으로 가고, 역할과 작업 상태가 돌아와 Conditions, Events와 Metrics에 반영됩니다. 백업·복원의 데이터 아티팩트는 DB 작업과 오브젝트 스토리지 사이를 이동합니다.

처음의 장애 상황으로 돌아가면, 엔진의 역할 전환을 IM으로 관찰하고 Operator 상태가 맞게 수렴하는지, 실제 SQL과 데이터가 그 결과와 일치하는지 확인해야 합니다. 특히 상태를 Unknown으로 표시하는 것만으로 쓰기가 막히지는 않습니다. 기존 Kind 실행에서도 역할이 미확정인 구간에 RW 쓰기가 계속된 결과가 기록돼 있습니다. 분할 상황의 새 연결과 기존 연결 쓰기 동작을 확인하고 격리 정책을 구현·검증하는 것이 첫 버전의 남은 필수 과제입니다.
-->

---

<OperatorSlide section="6 · 12주 로드맵" index="07" total="11" source="ROADMAP · Delivery gates" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">12주 계획은 기능 목록보다<br>단계별 통과 결과로 관리합니다</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>기준 고정</b><p>환경·시나리오 정의<br>단일 DB SQL 근거</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA alpha</b><p>3멤버·RW/RO<br>실제 VM 실행 경로<br>백업·복구 알파</p></div><div><small>5–8주 · 11.02–11.29</small><b>필수 전체 첫 통과</b><p>쓰기 격리·재합류<br>재구축·백업 복원<br>S00–S15 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>동일 RC 안정화</b><p>반복 장애·24h 부하 목표<br>다른 작성자의 문서 재현<br>회귀 수정·산출물 고정</p></div></div><p class="op-boundary"><b>11.29</b> 필수 시나리오 첫 전체 통과 목표　→　<b>12.27</b> v0.1 공개 목표</p><p class="op-caption">실행 커밋·이미지 digest·환경·SQL 이력·판정을 함께 보관합니다. 날짜는 목표이며 통과 사실이 아닙니다.</p>

</OperatorSlide>

<!--
[70초 · 6 · 12주 로드맵]
시즌은 10월 5일부터 12월 27일까지 12주입니다. 1주는 환경과 시나리오를 정하고 단일 DB SQL을 확인합니다. 2주부터 4주는 3멤버 HA와 RW/RO, 실제 VM 실행 경로와 백업·복구 알파가 목표입니다. 현재 Kind와 VM 결과는 이 단계의 일부 근거입니다.

5주부터 8주는 쓰기 격리, 재합류, 재구축과 실제 백업에서 새 클러스터 복원까지 필수 시나리오 전체의 첫 통과를 11월 29일 목표로 잡습니다. 12월은 새로운 필수 기능을 처음 만들기보다 같은 후보에서 핵심 장애를 반복하고, 초기 목표 24시간 부하와 다른 작성자의 문서 재현, 회귀 수정에 사용하려 합니다. 실행 커밋과 이미지 digest, 환경, SQL 이력과 판정을 묶어 남깁니다. 날짜를 지키기 위해 필수 안전 조건을 빼거나 미실행을 통과로 표시하지 않고, 검증 결과로 12월 27일 공개 여부를 판단합니다.
-->

---

<OperatorSlide section="6 · 팀원별 역할" index="08" total="11" source="Governance · Accountability" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">두 명이 공동 개발하고,<br>변경마다 담당자와 리뷰어를 둡니다</h1><div class="op-meta"><b>최영선 @yeongseon</b><b>백경준 @paikend</b><span>공동 메인테이너</span></div><table class="op-comparison"><thead><tr><th>책임</th><th>완료할 작업</th></tr></thead><tbody><tr><td>해당 이슈 담당자</td><td>실패 재현 → 구현·테스트 → 문서·실행 근거</td></tr><tr><td>다른 메인테이너</td><td>실패 경로·변경 내용 리뷰 → 검증 근거 확인</td></tr><tr><td>공동 책임</td><td>설치·HA·복구·공개 기준 검토와 릴리스 판단</td></tr></tbody></table><p class="op-caption">기능별 고정 분담 대신 이슈 단위로 담당하고 상호 리뷰합니다.<br>공유 VM 장애 실험은 한 번에 하나씩, 작성자 외 문서 재현은 별도로 확인합니다.</p>

</OperatorSlide>

<!--
[45초 · 6 · 팀원별 역할]
최영선과 백경준이 공동 메인테이너입니다. 확정되지 않은 개인별 전문 분야나 기능 배정을 만들기보다 실제 작업 책임을 설명하겠습니다. 이슈 담당자가 실패를 재현하고 구현, 테스트와 관련 문서, 실행 근거까지 준비합니다. 다른 메인테이너는 실패 경로와 변경 내용을 리뷰하고 그 근거가 완료 조건을 충족하는지 확인합니다.

클러스터와 HA, 백업·복구, 문서와 공개 준비를 이 방식으로 맡습니다. 공유 VM 장애 실험은 동시에 두 개를 돌리지 않고, 릴리스 단계에서는 작성자가 아닌 사람이 문서만으로 설치와 복구를 재현해야 합니다. 개인별 고정 기능 담당은 확정되면 반영하되, 공동 책임과 변경별 담당·리뷰 원칙을 구분합니다.
-->

---

<OperatorSlide class="op-compact" section="6 · 첫 버전 공개 범위" index="09" total="11" source="ROADMAP · v0.1 acceptance" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1 공개 기준과 산출물</h1><table class="op-comparison op-acceptance"><thead><tr><th>필수 범위</th><th>완료를 판단할 근거</th></tr></thead><tbody><tr><td>비루트·영속 DB<br>3멤버 HA·RW/RO</td><td>실제 SQL·역할·커밋 이력과 데이터 대조</td></tr><tr><td>장애·쓰기 격리<br>재합류·재구축</td><td>Pod/VM/Broker/Operator 장애 후 결과 검증</td></tr><tr><td>백업<br>새 클러스터 복원</td><td>실제 백업 아티팩트와 알려진 데이터셋 일치</td></tr><tr><td>보존·IM 인증<br>중단 정책·관측</td><td>S00–S15 근거 + 설치·운영·복구 문서 재현</td></tr></tbody></table><p class="op-boundary"><b>공개물</b>　이미지·설치 매니페스트·지원 환경표·운영 문서·검증 결과</p><p class="op-caption">CUBRID 11.4.x / amd64 / Kubernetes·CSI 한 구성 · experimental · 호환 업데이트·disk-full 조건부</p>

</OperatorSlide>

<!--
[55초 · 6 · 첫 버전 공개 범위]
v0.1은 기능이 많이 있다는 발표보다 하나의 고정된 환경에서 설치와 장애·복구를 재현할 수 있어야 합니다. 실제 SQL과 역할, 커밋 이력과 데이터를 대조하고, 재합류나 재구축이 정상 데이터를 덮어쓰지 않는지 확인합니다. 실제 백업으로 새 클러스터를 복원해 알려진 데이터셋이 일치해야 합니다. 보존과 IM 인증, 자발적 중단 정책, 정확한 관측과 재현 가능한 문서도 필수입니다.

이미지와 설치 매니페스트, 지원 환경표, 운영 문서와 검증 결과를 같은 후보에 연결해 공개하려 합니다. 기준은 CUBRID 11.4.x와 amd64, Kubernetes와 CSI 한 구성입니다. 현재 VM의 local-path로 CSI 조건을 충족했다고 보지는 않습니다. 첫 버전은 experimental이며 IM API 인증을 DB 인증이나 TLS로 혼동하지 않습니다. 기준 코드의 빈 DBA 암호와 비암호화 통신 제약도 명시해야 합니다.
-->

---

<OperatorSlide section="6 · v0.1 이후의 방향" index="10" total="11" source="Proposal · Beyond v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">v0.1 이후에는<br>운영 경험을 바탕으로 지원을 넓힙니다</h1><div class="op-release"><div><h3>운영화·안정화</h3><ul class="op-list"><li><b>사용자 피드백과 진단 개선</b><small>반복 실패·운영 절차부터 보완</small></li><li><b>도입 요건 검증</b><small>DB 인증·TLS·호환 업데이트</small></li></ul></div><div><h3>지원 환경 확대</h3><ul class="op-list"><li><b>Kubernetes·CSI 추가</b><small>각 조합에서 장애·복구 재검증</small></li><li><b>아키텍처·영역 확장 검토</b><small>arm64·다중 영역은 별도 실험</small></li></ul></div><div><h3>장기 운영 과제</h3><ul class="op-list"><li><b>엔진 버전 전환</b><small>데이터 호환·중단·복귀 절차</small></li><li><b>복제 토폴로지 확장</b><small>비승격 read replica 등 검토</small></li></ul></div></div><p class="op-boundary"><b>진행 기준</b>　v0.1 필수 검증 → 사용자 재현·피드백 → 다음 범위 확정</p><p class="op-caption">후속 방향안입니다. 버전·완료일·운영 지원을 확약하지 않으며 v0.1 필수 범위를 옮기지 않습니다.</p>

</OperatorSlide>

<!--
[40초 · 6 · v0.1 이후의 방향]
v0.1이 프로젝트의 끝은 아닙니다. 먼저 실제 운영 피드백으로 반복 실패와 진단, 운영 절차를 보완하고 DB 인증과 TLS, 호환 업데이트 같은 도입 요건을 검증하려 합니다. 이후 Kubernetes와 CSI 지원 조합을 늘리되 각 조합에서 장애·복구를 다시 확인합니다.

arm64와 다중 영역, 엔진 버전 전환과 비승격 read replica 같은 토폴로지는 별도의 장기 과제입니다. 이 순서는 방향안이며 다음 버전 번호나 완료일을 확약한 것은 아닙니다. v0.1 필수 안전 조건을 후속 버전으로 미루지 않고, 첫 검증과 사용자 피드백으로 다음 범위를 정하겠습니다.
-->

---

<OperatorSlide section="7 · 논의할 내용" index="11" total="11" source="Feedback · Validation partners" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">다음 검증을 구체화할<br>세 가지 의견을 구합니다</h1><ol class="op-questions"><li>최근 장애 한 건에서,<br>무엇을 어떤 순서로 확인하고 복귀를 결정했나요?</li><li>함께 검증할 Kubernetes·CSI 조합과<br>볼륨·장애 실험 제약은 무엇인가요?</li><li>12월에 작성자가 아닌 입장에서<br>설치·복구 문서를 따라 재현해 주실 수 있나요?</li></ol>

</OperatorSlide>

<!--
[30초 · 7 · 논의할 내용]
세 가지 의견을 부탁드립니다. 최근 장애 한 건을 기준으로 어떤 순서로 무엇을 확인해 복귀를 결정했는지 듣고 싶습니다. 함께 고정할 Kubernetes와 CSI, 볼륨과 장애 실험의 제약도 필요합니다. 마지막으로 12월에 작성자가 아닌 입장에서 설치와 복구 문서를 따라 재현해 주실 분을 찾습니다. 이 경험과 환경, 재현 결과로 첫 버전과 그 이후의 우선순위를 구체화하겠습니다. 감사합니다.
-->
