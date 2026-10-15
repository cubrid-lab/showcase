<OperatorSlide section="1 · 프로젝트·팀 소개" index="01" total="10" source="Project README · Team profiles" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">빌더 시즌4 · 1차 검증 · 2026.10.31</p><h1 class="op-title">CUBRID<br>Kubernetes Operator</h1><p class="op-lead">CUBRID의 배포·HA·복구 운영을<br>Kubernetes에서 관리하는 Operator를 개발합니다.</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div></div>

</OperatorSlide>

<!--
[60초 · 1 · 프로젝트·팀 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. CUBRID Kubernetes Operator는 Kubernetes에서 CUBRID 클러스터의 배포와 HA, 복구 운영을 관리하기 위한 프로젝트입니다. 두 사람이 공동 메인테이너로 참여하고 있습니다. 이번 1차 검증에서는 어떤 운영 문제를 풀려는지, 어떤 방식으로 접근하는지, 시즌 동안 어디까지 공개할 계획인지 말씀드리고 의견을 구하려 합니다. 현재는 실험 단계입니다.
-->

---

<OperatorSlide section="2 · 문제와 대상" index="02" total="10" source="README · DESIGN" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md#why-this-project">

<h1 class="op-title">해결하려는 문제와 대상</h1><div class="op-two"><div class="op-stack"><h3>대상</h3><ul class="op-list"><li><b>CUBRID DB 운영자</b><small>장애 이후 역할·복제·데이터 상태를 확인</small></li><li><b>Kubernetes 플랫폼 팀</b><small>Pod·스토리지·접속 경로를 관리</small></li></ul></div><div class="op-stack"><h3>문제</h3><ul class="op-list"><li><b>운영 상태를 여러 곳에서 확인</b><small>Pod 상태만으로 현재 master나 복제 상태를 알기 어려움</small></li><li><b>복구 절차를 별도로 수행</b><small>멤버 재합류·데이터 복원과 서비스 복귀를 함께 확인해야 함</small></li></ul></div></div><p class="op-caption">초기 대상 사용자 가설입니다. 실제 운영 환경과 우선 과제는 피드백으로 확인하려 합니다.</p>

</OperatorSlide>

<!--
[60초 · 2 · 문제와 대상]
대상은 Kubernetes에서 CUBRID를 운영하려는 DB 운영자와 플랫폼 팀입니다. 장애가 나면 Pod가 다시 떴는지뿐 아니라 현재 master, 복제 진행 상태, 기존 데이터의 재사용 가능 여부를 확인해야 합니다. DB 운영과 Kubernetes 자원 관리가 분리되어 있어 이 과정을 여러 도구와 절차로 확인하게 됩니다. 이 반복 작업을 줄이는 것이 문제 정의입니다. 아직 인터뷰로 검증된 수요라고 말하는 단계는 아니며, 이번 검증에서 대상과 우선 과제가 적절한지 확인하고 싶습니다.
-->

---

<OperatorSlide section="3 · 현재 방식과 한계" index="03" total="10" source="Official Operator · Pinned sources" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">현재 해결 방식과 기존 OSS의 한계</h1><table class="op-comparison"><thead><tr><th>현재 방식</th><th>이미 제공하는 것</th><th>추가로 확인할 내용</th></tr></thead><tbody><tr><td>YAML·스크립트</td><td>리소스와 설정 배포</td><td>장애 뒤 어떤 상태로 복귀하는가?</td></tr><tr><td>공식 CUBRID Operator</td><td>HA 역할 관찰·스토리지·예약 백업</td><td>관찰 누락·불일치를 어떻게 판단하는가?</td></tr><tr><td>CUBRID native HA</td><td>복제와 역할 전환</td><td>Kubernetes 수명주기와 어떻게 연결하는가?</td></tr></tbody></table><p class="op-caption">공식 Operator도 HA 역할을 관찰합니다. 이 프로젝트는 장애 이후의 상태 판단과 복구 결과를 추가로 검증하려는 실험입니다.</p>

</OperatorSlide>

<!--
[75초 · 3 · 현재 방식과 한계]
현재는 YAML과 스크립트, CUBRID native HA, 공식 CUBRID Operator를 사용할 수 있습니다. 공식 Operator는 배포뿐 아니라 HA 역할 관찰, 스토리지와 예약 백업도 제공합니다. 저희가 더 확인하려는 것은 장애 이후 관찰이 누락되거나 서로 다를 때의 판단, 실제 SQL 접속과 복제 결과, 복구 과정의 재현입니다. 예를 들어 포트가 열려 있다는 검사만으로 SQL 성공과 데이터 일치를 입증할 수는 없습니다. 공식 제품의 안정성을 비교한 결과를 제시하는 것이 아니라, 이 프로젝트에서 검증할 운영 문제의 범위를 설명하는 것입니다.
-->

---

<OperatorSlide section="4 · 제안하는 해결 방법" index="04" total="10" source="DESIGN §2–4" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals">

<h1 class="op-title">제안하는 해결 방법</h1><div class="op-path"><div class="op-node project">운영 의도<small>CubridCluster</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">관찰<small>역할 · 복제 · 접속</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">조정<small>리소스 · 작업 수명주기</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">상태 보고<small>Conditions · Events</small></div></div><p class="op-caption">DB 상태를 관찰해 Kubernetes 자원과 운영 작업을 조정하고, 결과를 상태로 제공합니다.</p>

</OperatorSlide>

<!--
[60초 · 4 · 제안하는 해결 방법]
사용자가 CubridCluster로 원하는 구성을 선언하면 Operator가 DB와 Kubernetes의 현재 상태를 함께 관찰하도록 합니다. 관찰한 내용을 바탕으로 자원과 운영 작업을 조정하고 상태를 보고하는 방식입니다. HA 역할 전환은 CUBRID가 맡고, Operator는 그 결과와 주변 자원을 연결합니다. 모든 복구 동작이 완성된 것은 아닙니다. 특히 쓰기 격리와 재합류, 백업·복구는 실제 환경 검증이 남아 있으며 시즌 계획에서 다룹니다.
-->

---

<OperatorSlide section="5 · 아키텍처 초안" index="05" total="10" source="DESIGN §7, §9, §10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">아키텍처 초안</h1><div class="op-stack"><div class="op-path"><div class="op-node ">CubridCluster<small>Kubernetes API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator<small>관찰 · 리소스 조정</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Kubernetes 자원<small>StatefulSet · Service · PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">DB 멤버 · CUBRID native HA</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>멤버 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>멤버 2 · PVC</small></div></div></div><div class="op-stack"><p class="op-kicker">분리된 접속 계층</p><div class="op-node ">Broker tier<small>중복 RW / RO Broker</small></div><div class="op-node storage">Object storage<small>bootstrap · backup · restore</small></div></div></div></div><p class="op-caption">IM은 DB 컨테이너의 통합 supervisor입니다. 별도 sidecar가 아니며, Operator와 인증된 HTTP API로 통신합니다.</p>

</OperatorSlide>

<!--
[75초 · 5 · 아키텍처 초안]
주요 구성 요소는 Kubernetes API, Operator, DB 멤버, Instance Manager, Broker, 오브젝트 스토리지입니다. Operator는 StatefulSet과 Service, PVC를 관리하고 각 멤버의 Instance Manager를 통해 로컬 작업과 상태를 관찰합니다. Instance Manager는 별도 sidecar가 아니라 DB 컨테이너 안의 supervisor입니다. 세 DB 멤버의 역할은 CUBRID HA가 결정합니다. Broker는 분리된 접속 계층으로 RW와 RO 접근을 제공합니다. 오브젝트 스토리지는 초기 멤버 복제와 백업·복구 아티팩트를 다루는 데 사용합니다.
-->

---

<OperatorSlide section="5 · 데이터 처리 흐름" index="06" total="10" source="DESIGN §9–10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">데이터와 제어 흐름</h1><div class="op-stack"><p class="op-kicker">데이터 경로 · 애플리케이션의 SQL</p><div class="op-path"><div class="op-node ">Application</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">RW / RO Service</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Broker</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>SQL 실행</small></div></div><p class="op-kicker">제어 경로 · 의도와 작업</p><div class="op-path"><div class="op-node ">CubridCluster</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Instance Manager<small>인증된 HTTP API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>로컬 작업 · 상태</small></div></div></div><p class="op-caption">역할·작업 관찰은 Operator의 Conditions·Events·Metrics로 이어집니다. 데이터 경로와 제어 경로를 분리합니다.</p>

</OperatorSlide>

<!--
[60초 · 5 · 데이터 처리 흐름]
애플리케이션의 SQL은 RW 또는 RO Service를 거쳐 Broker와 CUBRID로 흐릅니다. 반면 운영 설정과 제어 요청은 CubridCluster에서 Operator, Instance Manager로 이어집니다. Instance Manager의 역할과 작업 관찰은 Operator의 상태, 이벤트, 지표로 돌아옵니다. 이 두 경로를 분리해 DB 접속이 Operator를 통과하도록 만들지 않습니다. 불완전한 관찰만으로 Operator가 master를 승격하거나 갈라진 데이터 중 하나를 선택하지 않는 것이 설계 원칙입니다.
-->

---

<OperatorSlide section="6 · 12주 로드맵" index="07" total="10" source="ROADMAP · STP IV" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">12주 로드맵</h1><div class="op-timeline"><div><small>1주 · 10.05–10.11</small><b>범위와 기준</b><p>시나리오·환경 확정<br>단일 DB 실제 SQL</p></div><div><small>2–4주 · 10.12–11.01</small><b>HA alpha</b><p>3멤버 HA·RW/RO<br>백업·복구 알파</p></div><div><small>5–8주 · 11.02–11.29</small><b>복구 검증</b><p>쓰기 격리<br>재합류·재구축</p></div><div><small>9–12주 · 11.30–12.27</small><b>릴리스 준비</b><p>반복 실험·회귀 수정<br>재현 문서·증거</p></div></div><p class="op-caption">2026.10.05–12.27 · 단계별 목표입니다. 실제 완료 여부는 검증 결과로 확인합니다.</p>

</OperatorSlide>

<!--
[75초 · 6 · 12주 로드맵]
시즌은 10월 5일부터 12월 27일까지 12주입니다. 첫 주에는 범위와 시나리오, 환경을 정리합니다. 2주부터 4주는 3멤버 HA와 RW/RO 접근, 백업·복구 알파를 목표로 합니다. 5주부터 8주는 쓰기 격리와 재합류, 재구축 등 복구 시나리오를 확인합니다. 마지막 네 주에는 반복 검증과 회귀 수정, 설치·운영 문서와 공개 버전의 증거를 준비합니다. 날짜가 지났다는 이유로 완료로 보는 것은 아니며, 실제 결과를 기준으로 진행 상태를 구분합니다.
-->

---

<OperatorSlide section="6 · 팀원별 역할" index="08" total="10" source="Team profiles · Project governance" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#team-and-role-record">

<h1 class="op-title">팀 구성과 역할</h1><div class="op-two"><table class="op-comparison"><thead><tr><th>팀원</th><th>현재 역할</th></tr></thead><tbody><tr><td>최영선<br><small>@yeongseon</small></td><td>공동 메인테이너</td></tr><tr><td>백경준<br><small>@paikend</small></td><td>공동 메인테이너</td></tr></tbody></table><div class="op-stack"><h3>이번 시즌 작업</h3><ul class="op-list"><li><b>클러스터·HA 연동</b><small>상태 관찰과 Kubernetes 자원 관리</small></li><li><b>백업·복구</b><small>장애와 복구 시나리오 확인</small></li><li><b>문서·공개 준비</b><small>설치·운영 문서와 검증 결과 정리</small></li></ul></div></div><p class="op-caption">설계·개발·검증에 공동 참여합니다. 기능별 개인 담당 배정은 확정 전입니다.</p>

</OperatorSlide>

<!--
[45초 · 6 · 팀원별 역할]
팀원은 최영선과 백경준 두 명이며, 현재 공동 메인테이너로 참여하고 있습니다. 이번 시즌 작업은 클러스터와 HA 연동, 백업·복구, 문서와 공개 준비로 정리했습니다. 현재 확인된 역할은 설계와 개발, 검증을 함께 맡는 구조입니다. 구체적인 개인별 기능 분담은 아직 정리 중입니다.
-->

---

<OperatorSlide section="6 · 첫 버전 공개 범위" index="09" total="10" source="ROADMAP · v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#v01-scope">

<h1 class="op-title">시즌 종료 시 공개할 첫 버전</h1><div class="op-release"><div><h3>기본 운영</h3><ul class="op-list"><li><b>클러스터 수명주기</b><small>인증된 비루트 실행 · 영속 스토리지</small></li><li><b>3멤버 HA와 접근</b><small>역할 관찰 · RW/RO 접속</small></li></ul></div><div><h3>장애·데이터 복구</h3><ul class="op-list"><li><b>장애와 쓰기 격리</b><small>Pod·VM·Broker·Operator 장애</small></li><li><b>재합류·재구축·복원</b><small>백업과 새 클러스터 복원</small></li></ul></div><div><h3>운영·배포 자료</h3><ul class="op-list"><li><b>보존·보안·관측</b><small>인증 · 중단 정책 · 상태·이벤트·지표</small></li><li><b>재현 가능한 문서와 증거</b><small>설치·운영 안내 · 필수 시나리오 검증</small></li></ul></div></div><p class="op-caption">초기 대상: CUBRID 11.4.x / amd64 + 하나의 Kubernetes·CSI 구성. 호환 업데이트·disk-full은 조건부이며, 엔진 버전 이동·광범위 환경 지원은 초기 범위 밖입니다.</p>

</OperatorSlide>

<!--
[60초 · 6 · 첫 버전 공개 범위]
첫 버전의 목표는 하나의 고정된 환경에서 기본 운영과 HA, 접속, 장애·데이터 복구, 설치·운영 문서를 함께 공개하는 것입니다. 여기에는 실제 쓰기 격리, 재합류와 재구축, 백업에서 새 클러스터로의 복원도 포함됩니다. 보존과 인증, 자발적 중단 정책, 상태와 지표, 필수 시나리오의 재현 증거도 필요합니다. 호환 업데이트와 디스크 가득 참은 조건부이며, 엔진 버전 이동이나 넓은 환경 지원은 초기 범위 밖입니다. 이 내용은 목표 범위이며 필수 검증을 마치기 전 지원 완료로 발표하지 않습니다.
-->

---

<OperatorSlide section="7 · 논의할 내용" index="10" total="10" source="Project proposal" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md">

<h1 class="op-title">함께 논의하고 싶은 내용</h1><ol class="op-questions"><li>대상 사용자와 문제 정의가 적절한가요?</li><li>첫 버전에서 우선할 운영 기능은 무엇인가요?</li><li>실제 사용 환경에서 검증에 참여할 수 있나요?</li></ol>

</OperatorSlide>

<!--
[30초 · 7 · 논의할 내용]
이번 1차 검증에서는 대상과 문제를 제대로 잡았는지, 첫 버전에서 어떤 운영 기능의 우선순위를 높여야 하는지 의견을 듣고 싶습니다. 또 실제 사용 환경에서 테스트와 운영 문서 재현에 참여할 분이 계신지도 논의하고 싶습니다. 감사합니다.
-->
