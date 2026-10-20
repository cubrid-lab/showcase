---
title: "CUBRID Kubernetes Operator — 1차 검증"
---

<OperatorSlide section="1 · 프로젝트·팀 소개" index="01" total="10" source="Project README · Team profiles" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID<br>Kubernetes Operator</h1><p class="op-lead">CUBRID의 배포·HA·복구 운영을<br>Kubernetes에서 관리하는 Operator를 개발합니다.</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div></div>

</OperatorSlide>

<!--
[60초 · 1 · 프로젝트·팀 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저희는 CUBRID Kubernetes Operator를 함께 개발하는 공동 메인테이너입니다. 이 프로젝트는 CUBRID 클러스터의 배포와 HA, 장애 이후 복구 운영을 Kubernetes에서 관리하기 위한 실험입니다.

데이터베이스를 컨테이너로 실행하는 것에서 시작해, 운영자가 원하는 구성과 실제 DB 상태를 연결하는 것이 목표입니다. 오늘은 어떤 운영 문제를 풀려는지, 기존 방식에서 무엇을 더 확인하려는지, 제안하는 구조와 시즌 계획을 순서대로 설명하겠습니다. 현재 확인한 결과와 앞으로 충족해야 할 검증 조건도 구분해 말씀드리겠습니다. 이번 발표를 통해 실제 운영 현장에 맞는 문제를 잡았는지 의견을 듣고 싶습니다.
-->

---

<OperatorSlide section="2 · 문제와 대상" index="02" total="10" source="README · DESIGN" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md#why-this-project">

<h1 class="op-title">해결하려는 문제와 대상</h1><div class="op-two"><div class="op-stack"><h3>대상</h3><ul class="op-list"><li><b>CUBRID DB 운영자</b><small>장애 이후 역할·복제·데이터 상태를 확인</small></li><li><b>Kubernetes 플랫폼 팀</b><small>Pod·스토리지·접속 경로를 관리</small></li></ul></div><div class="op-stack"><h3>문제</h3><ul class="op-list"><li><b>운영 상태를 여러 곳에서 확인</b><small>Pod 상태만으로 현재 master나 복제 상태를 알기 어려움</small></li><li><b>복구 절차를 별도로 수행</b><small>멤버 재합류·데이터 복원과 서비스 복귀를 함께 확인해야 함</small></li></ul></div></div><p class="op-caption">초기 대상 사용자 가설입니다. 실제 운영 환경과 우선 과제는 피드백으로 확인하려 합니다.</p>

</OperatorSlide>

<!--
[60초 · 2 · 문제와 대상]
초기 대상은 Kubernetes에서 CUBRID를 운영하려는 DB 운영자와 플랫폼 팀입니다. DB 운영자는 현재 master와 복제 상태, 기존 데이터를 다시 사용할 수 있는지 확인해야 합니다. 플랫폼 팀은 Pod와 볼륨, Service와 접속 경로를 관리합니다. 장애가 나면 이 두 관점이 만납니다.

예를 들어 Pod가 다시 Ready가 되었더라도, 어떤 멤버가 쓰기를 받고 있는지와 데이터가 따라왔는지는 추가로 확인해야 합니다. 상태 조회와 복구 절차가 여러 곳으로 나뉘어 있으면 서비스 복귀 판단도 복잡해집니다. 저희는 이때 반복되는 확인과 조정 작업을 줄이려 합니다. 다만 이 대상과 우선순위는 아직 사용자 가설입니다. 이미 수요가 검증되었거나 도입 사례가 확보되었다고 설명하는 것은 아닙니다.
-->

---

<OperatorSlide section="3 · 현재 방식과 한계" index="03" total="10" source="Official Operator · Pinned sources" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">현재 해결 방식과 기존 OSS의 한계</h1><table class="op-comparison"><thead><tr><th>현재 방식</th><th>이미 제공하는 것</th><th>추가로 확인할 내용</th></tr></thead><tbody><tr><td>YAML·스크립트</td><td>리소스와 설정 배포</td><td>장애 뒤 어떤 상태로 복귀하는가?</td></tr><tr><td>공식 CUBRID Operator</td><td>HA 역할 관찰·스토리지·예약 백업</td><td>관찰 누락·불일치를 어떻게 판단하는가?</td></tr><tr><td>CUBRID native HA</td><td>복제와 역할 전환</td><td>Kubernetes 수명주기와 어떻게 연결하는가?</td></tr></tbody></table><p class="op-caption">공식 Operator도 HA 역할을 관찰합니다. 이 프로젝트는 장애 이후의 상태 판단과 복구 결과를 추가로 검증하려는 실험입니다.</p>

</OperatorSlide>

<!--
[75초 · 3 · 현재 방식과 한계]
현재 사용할 수 있는 방식에는 YAML과 스크립트, CUBRID native HA, 공식 CUBRID Operator가 있습니다. YAML과 스크립트는 자원과 설정을 배포하고, CUBRID HA는 복제와 역할 전환을 수행합니다. 공식 Operator 역시 HA 역할 관찰, 스토리지와 예약 백업을 제공합니다. 이 세 가지가 현재 운영을 구성하는 출발점입니다.

저희 프로젝트에서 확인하려는 항목은 장애 이후의 관찰과 복구 결과입니다. 어떤 멤버의 관찰이 빠졌거나 서로 다른 역할을 보고할 때 상태를 어떻게 표시할지, SQL 접속과 복제 결과가 실제로 일치하는지, 복구 절차를 다시 재현할 수 있는지가 관심사입니다. 포트가 열린다는 결과만으로 SQL 성공이나 데이터 일치를 입증할 수는 없습니다. 아직 공식 프로젝트와 배포 안정성을 비교한 결과는 없으며, 여기서는 저희의 검증 범위를 설명하고 있습니다.
-->

---

<OperatorSlide section="4 · 제안하는 해결 방법" index="04" total="10" source="CI · VM evidence · 2026-10-20" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281421472">

<h1 class="op-title">제안하는 해결 방법</h1><div class="op-path"><div class="op-node project">운영 의도<small>CubridCluster</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">관찰<small>역할 · 복제 · 접속</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">조정<small>리소스 · 작업 수명주기</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">상태 보고<small>Conditions · Events</small></div></div><p class="op-caption">DB 상태를 관찰해 Kubernetes 자원과 운영 작업을 조정하고, 결과를 상태로 제공합니다.</p><p class="op-caption"><b>현재 근거 · 39b1cb6</b>　Kind 27/27 · VM 실제 SQL 확인<br>VM 장애·CSI 검증은 남아 있습니다.</p>

</OperatorSlide>

<!--
[60초 · 4 · 제안하는 해결 방법]
제안하는 흐름은 운영 의도를 선언하고, 현재 상태를 관찰하고, 자원과 작업을 조정한 뒤 결과를 보고하는 것입니다. 사용자는 CubridCluster로 구성을 지정하고, Operator는 DB와 Kubernetes 상태를 함께 확인합니다. HA 역할 전환은 CUBRID가 결정합니다.

현재 근거도 짧게 말씀드리겠습니다. 코드 기준은 39b1cb6이며 Kind 실행에서 27개 테스트가 모두 통과했습니다. VM에서는 단일 DB의 SQL과 기존 행 보존을 확인했습니다. HA에서는 기존 행과 시각 보존, RW 커밋과 RO 읽기·쓰기 거부를 확인했습니다. 단일 DB 멤버에서는 HTTP 연결 제한도 확인했습니다. 환경은 네 VM 노드의 k3s 1.36.5+k3s1과 CUBRID 11.4.6.1963, CSI가 아닌 local-path 스토리지입니다. 이 결과는 필수 S00부터 S15 전체나 VM 장애, CSI 검증의 완료를 뜻하지 않습니다.
-->

---

<OperatorSlide section="5 · 아키텍처 초안" index="05" total="10" source="DESIGN §7, §9, §10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">아키텍처 초안</h1><div class="op-stack"><div class="op-path"><div class="op-node ">CubridCluster<small>Kubernetes API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator<small>관찰 · 리소스 조정</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Kubernetes 자원<small>StatefulSet · Service · PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">DB 멤버 · CUBRID native HA</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>멤버 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 2 · PVC</small></div></div></div><div class="op-stack"><p class="op-kicker">분리된 접속 계층</p><div class="op-node ">Broker tier<small>중복 RW / RO Broker</small></div><div class="op-node storage">Object storage<small>bootstrap · backup · restore</small></div></div></div></div><p class="op-caption">IM은 DB 컨테이너의 통합 supervisor입니다. 별도 sidecar가 아니며, Operator와 인증된 HTTP API로 통신합니다.</p>

</OperatorSlide>

<!--
[75초 · 5 · 아키텍처 초안]
구성 요소를 보면 Kubernetes API와 Operator, DB 멤버, Instance Manager, 분리된 Broker 계층, 오브젝트 스토리지가 있습니다. Operator는 StatefulSet과 Service, PVC 같은 자원을 관리하고, 각 DB 멤버의 로컬 작업과 상태는 Instance Manager를 통해 다룹니다.

여기서 Instance Manager는 별도 sidecar가 아닙니다. CUBRID와 같은 DB 컨테이너 안에서 실행되는 supervisor이며, Operator와는 IM API의 Bearer 토큰으로 통신합니다. 세 멤버 중 누가 master가 되는지는 CUBRID HA가 정합니다. 멤버 0을 영구 master로 정하지도 않습니다. Broker는 DB 멤버와 분리된 계층에서 RW와 RO 접속을 제공합니다. 오브젝트 스토리지는 초기 멤버 복사와 백업·복원 아티팩트의 경로입니다. 이 구조 위에서 각 운영 결과를 실제 시나리오로 확인하는 것이 개발 과제입니다.
-->

---

<OperatorSlide section="5 · 데이터 처리 흐름" index="06" total="10" source="DESIGN §9–10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">데이터와 제어 흐름</h1><div class="op-stack"><p class="op-kicker">데이터 경로 · 애플리케이션의 SQL</p><div class="op-path"><div class="op-node ">Application</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">RW / RO Service</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Broker</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>SQL 실행</small></div></div><p class="op-kicker">제어 경로 · 의도와 작업</p><div class="op-path"><div class="op-node ">CubridCluster</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Instance Manager<small>인증된 HTTP API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>로컬 작업 · 상태</small></div></div></div><p class="op-caption">역할·작업 관찰은 Operator의 Conditions·Events·Metrics로 이어집니다. 데이터 경로와 제어 경로를 분리합니다.</p>

</OperatorSlide>

<!--
[60초 · 5 · 데이터 처리 흐름]
위쪽은 애플리케이션의 데이터 경로입니다. SQL은 RW 또는 RO Service를 거쳐 Broker와 CUBRID로 전달됩니다. 아래쪽은 제어 경로입니다. 원하는 구성과 운영 요청은 CubridCluster에서 Operator, Instance Manager로 이어집니다. 역할과 작업의 관찰은 Conditions, Events, Metrics로 돌아옵니다.

Operator가 SQL 요청을 중계하지 않도록 두 경로를 분리했습니다. CUBRID가 역할을 전환하고, Operator는 멤버를 직접 master로 승격하지 않습니다. 관찰이 불완전하면 primary를 확정하지 않고, 갈라진 데이터 중 하나를 정답으로 고르지도 않습니다. 또 상태에 불명확하다고 표시된 것과 실제 SQL 쓰기가 차단된 것은 별개입니다. 필요한 쓰기 격리는 실제 접속을 통해 검증해야 하며, 시즌의 필수 복구 범위에 포함됩니다.
-->

---

<OperatorSlide section="6 · 12주 로드맵" index="07" total="10" source="ROADMAP · STP IV" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">12주 로드맵</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>범위와 기준</b><p>시나리오·환경 확정<br>단일 DB 실제 SQL</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA alpha</b><p>3멤버 HA·RW/RO<br>백업·복구 알파</p></div><div><small>5–8주 · 11.02–11.29</small><b>복구 검증</b><p>쓰기 격리·재합류·재구축<br>11.29 필수 전체 첫 통과 목표</p></div><div><small>9–12주 · 11.30–12.27</small><b>RC·릴리스 준비</b><p>12월 RC·반복 검증<br>12.27 v0.1 공개 목표</p></div></div><p class="op-caption">2026.10.05–12.27 · 단계별 목표입니다. 실제 완료 여부는 검증 결과로 확인합니다.</p>

</OperatorSlide>

<!--
[75초 · 6 · 12주 로드맵]
시즌은 10월 5일부터 12월 27일까지 12주입니다. 첫 주에는 범위와 시나리오, 환경을 정리하고 단일 DB의 실제 SQL을 확인합니다. 2주부터 4주는 세 멤버 HA와 RW/RO 접근, 대표 장애와 백업·복구 알파를 목표로 합니다. 현재 결과도 이 단계의 일부 근거로 다룹니다.

5주부터 8주에는 쓰기 격리와 재합류, 재구축을 포함한 필수 시나리오 전체의 첫 통과를 11월 29일 목표로 잡았습니다. 12월에는 RC, 즉 릴리스 후보를 기준으로 핵심 장애를 반복하고 회귀 수정과 운영 문서 재현을 진행할 계획입니다. 12월 27일 v0.1 공개가 목표입니다. 모두 목표 날짜이며 통과 사실을 미리 선언한 것은 아닙니다. 필수 조건을 충족하지 못하면 범위를 줄여 완료로 발표하지 않고, 남은 조건과 공개 상태를 그대로 설명하겠습니다.
-->

---

<OperatorSlide section="6 · 팀원별 역할" index="08" total="10" source="Team profiles · Project governance" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#team-and-role-record">

<h1 class="op-title">팀 구성과 역할</h1><div class="op-two"><table class="op-comparison"><thead><tr><th>팀원</th><th>현재 역할</th></tr></thead><tbody><tr><td>최영선<br><small>@yeongseon</small></td><td>공동 메인테이너</td></tr><tr><td>백경준<br><small>@paikend</small></td><td>공동 메인테이너</td></tr></tbody></table><div class="op-stack"><h3>이번 시즌 작업</h3><ul class="op-list"><li><b>클러스터·HA 연동</b><small>상태 관찰과 Kubernetes 자원 관리</small></li><li><b>백업·복구</b><small>장애와 복구 시나리오 확인</small></li><li><b>문서·공개 준비</b><small>설치·운영 문서와 검증 결과 정리</small></li></ul></div></div><p class="op-caption">설계·구현·검증을 공동으로 맡고, 변경과 결과를 함께 검토합니다.</p>

</OperatorSlide>

<!--
[45초 · 6 · 팀원별 역할]
최영선과 백경준, 두 사람이 공동 메인테이너로 설계와 구현, 검증을 함께 맡습니다. 시즌 작업은 클러스터와 HA 연동, 백업·복구, 문서와 공개 준비의 세 영역으로 정리했습니다.

상태를 관찰하는 코드와 실제 DB의 결과를 연결하고, 그 결과를 다른 사람이 재현할 수 있는 자료로 만드는 일까지 함께 책임집니다. 두 사람 모두 시나리오와 구현, 검토와 문서를 연결하는 역할입니다. 공동 역할 안에서 개별 작업과 검토는 변경 단위로 조율합니다. 시즌의 목표는 구현, 실제 DB 관찰, 다른 사람이 따라 할 수 있는 운영 자료를 함께 남기는 것입니다.
-->

---

<OperatorSlide section="6 · 첫 버전 공개 범위" index="09" total="10" source="ROADMAP · v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">시즌 종료 시 공개할 첫 버전</h1><div class="op-release"><div><h3>기본 운영</h3><ul class="op-list"><li><b>클러스터 수명주기</b><small>IM API 인증·비루트 실행 · 영속 스토리지</small></li><li><b>3멤버 HA와 접근</b><small>역할 관찰 · RW/RO 접속</small></li></ul></div><div><h3>장애·데이터 복구</h3><ul class="op-list"><li><b>장애와 쓰기 격리</b><small>Pod·VM·Broker·Operator 장애</small></li><li><b>재합류·재구축·복원</b><small>백업과 새 클러스터 복원</small></li></ul></div><div><h3>운영·배포 자료</h3><ul class="op-list"><li><b>보존·보안·관측</b><small>IM API 인증 · 중단 정책 · 상태·이벤트·지표</small></li><li><b>재현 가능한 문서와 증거</b><small>설치·운영 안내 · 필수 시나리오 검증</small></li></ul></div></div><p class="op-caption">초기 대상: CUBRID 11.4.x / amd64 + 하나의 Kubernetes·CSI 구성. 호환 업데이트·disk-full은 조건부이며, 엔진 버전 이동·광범위 환경 지원은 초기 범위 밖입니다.</p>

</OperatorSlide>

<!--
[60초 · 6 · 첫 버전 공개 범위]
첫 공개 버전의 목표는 하나의 고정된 CUBRID 11.4.x, amd64, Kubernetes와 CSI 구성에서 필수 운영 범위를 검증하는 것입니다. 세 멤버 HA와 RW/RO뿐 아니라 Pod·VM·Broker·Operator 장애, 쓰기 격리, 재합류와 재구축, 백업에서 새 클러스터로의 복원까지 포함합니다. 보존 정책과 IM API 인증, 자발적 중단 정책과 정확한 관측 정보, 설치·운영 문서와 재현 증거도 필요합니다.

현재 VM의 local-path 결과로 CSI 조건을 충족했다고 보지는 않습니다. 호환 업데이트와 disk-full은 조건부이고, 엔진 버전 이동과 넓은 환경 지원은 초기 범위 밖입니다. 여기서 인증은 IM API 인증을 뜻합니다. 현재 실험 버전은 DBA 암호가 비어 있고 전송 암호화가 없어, DB 인증이나 TLS까지 갖춘 운영 지원을 주장하지 않습니다. 필수 검증과 지원 경계가 확인된 뒤 공개 범위를 판단할 계획입니다.
-->

---

<OperatorSlide section="7 · 논의할 내용" index="10" total="10" source="Project proposal" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md">

<h1 class="op-title">함께 논의하고 싶은 내용</h1><ol class="op-questions"><li>장애 후 가장 번거로운 확인·복구 작업은 무엇인가요?</li><li>기준 환경으로 함께 고정할 Kubernetes·CSI 조합은 무엇인가요?</li><li>설치·장애·복구 절차를 재현할 검증 파트너로 참여할 수 있나요?</li></ol>

</OperatorSlide>

<!--
[30초 · 7 · 논의할 내용]
오늘은 세 가지 의견을 부탁드립니다. 장애 뒤에 실제로 가장 번거로운 확인이나 복구 작업은 무엇인지, 첫 기준 환경으로 함께 고정할 Kubernetes와 CSI 조합은 무엇인지 궁금합니다. 또 설치와 장애·복구 절차를 재현할 검증 파트너로 참여할 수 있는지도 듣고 싶습니다. 실제 수요와 검증 협력 가능성을 확인하기 위한 질문입니다. 감사합니다.
-->
