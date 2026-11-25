---
title: "CUBRID Kubernetes Operator — 2차 검증"
---

<OperatorSlide section="Opening · 프로젝트 소개" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">빌더 시즌4 · 2차 검증 · 아키텍처 중간 검증</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">장애 뒤 사람 없이 다시 쓸 수 있는 상태로 돌아오는 CUBRID HA Operator</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[20초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 1차 검증에서는 Kubernetes에서 CUBRID HA를 운영하고 장애 뒤 복구까지 확인하는 Operator의 목표와 계획을 말씀드렸습니다. 오늘 2차 검증의 결론부터 말씀드리면, 첫 장애를 넘기는 것은 CUBRID HA도 합니다. 저희 Operator는 그 뒤를 맡습니다. 사람 없이 클러스터를 다시 쓸 수 있고, 다음 장애도 견딜 수 있는 상태로 돌려놓습니다. 그 과정에서 지키는 원칙은 한 문장입니다. master를 확신할 수 없으면 쓰기 경로를 닫고, 닫은 뒤에는 쓰기 성공을 내보내지 않는다. 닫기 전에 생긴 손실은 숨기지 않고 공개합니다. 1차에서 직접 본 위험에서 출발해, 그것을 막는 설계와 VM 랩에서 확인한 증거, 막지 못한 한계, 그리고 그래서 v0.1에서 무엇을 약속하는지 순서대로 말씀드리겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

<OperatorSlide class="op-compact" section="Agenda · 발표 순서" source="발표 구성" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">발표 순서</h1><div class="op-agenda"><div><span>01</span><b>문제</b><p>1차에서 본 가장 큰 위험</p></div><div><span>02</span><b>설계</b><p>쓰기 격리 · 경계 · 명시적 재구축</p></div><div><span>03</span><b>증거와 한계</b><p>공식 operator와 같은 장애 비교 · VM 랩 · Kind · 막지 못한 손실</p></div><div><span>04</span><b>그래서 v0.1</b><p>약속하는 범위 · 판정 방식 · 일정</p></div></div>

</OperatorSlide>

<!--
[15초 · Agenda · 발표 순서]
문제, 설계, 증거와 한계, 그리고 그래서 v0.1의 순서로 말씀드리겠습니다.
-->

---

<OperatorSlide section="01 · 문제">

<ChapterDivider number="01" title="문제" subtitle="1차에서 본 위험에서 출발합니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 문제]
다음 주제를 알리는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-compact" section="01 · 문제" source="1차 검증 발표 · 시험 중 직접 본 위험" source-url="https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation">

<h1 class="op-title">1차에서 본 가장 큰 위험: master가 불확실한데 쓰기가 성공했습니다</h1><div class="op-safety"><div><span>1차 검증에서 직접 본 것</span><h3>master 미확정 상태에서 RW 쓰기 승인</h3><p>Kind에서 master Pod를 삭제하는 시험 중, Operator는 master를 “미확정”으로 표시했지만 읽기-쓰기 경로는 열려 있었고 쓰기가 승인됐습니다.</p><p class="op-mini">상태 표시만으로는 쓰기가 막히지 않음</p></div><div><span>그래서 이번 질문</span><h3>Operator는 어디까지 막을 수 있나</h3><p>장애 중에 애플리케이션이 받은 “쓰기 성공”이 나중에 사라지지 않게 하려면, 무엇을 닫고 무엇을 공개해야 하는지 확인했습니다.</p><p class="op-mini">설계 → VM 랩 증거 → 한계 → v0.1 범위</p></div></div><p class="op-boundary"><b>오늘의 한 문장</b>　확신할 수 없으면 쓰기 경로를 닫고, 닫은 뒤에는 “쓰기 성공”을 내보내지 않습니다</p>

</OperatorSlide>

<!--
[35초 · 01 · 문제]
1차 검증에서 직접 본 가장 큰 위험부터 말씀드리겠습니다. Kind에서 master Pod를 삭제하는 시험 중에 Operator는 master를 미확정으로 표시했지만, 읽기-쓰기 경로는 열려 있었고 쓰기가 승인됐습니다. 상태 표시만으로는 쓰기가 막히지 않는다는 뜻입니다.

그래서 이번 4주 동안의 질문은 하나였습니다. Operator는 어디까지 막을 수 있는가. 애플리케이션이 받은 쓰기 성공이 나중에 사라지지 않게 하려면 무엇을 닫고, 막지 못하는 것은 무엇이며, 그것을 어떻게 공개할지입니다. 오늘 드릴 말씀은 이 한 문장입니다. 확신할 수 없으면 쓰기 경로를 닫고, 닫은 뒤에는 쓰기 성공을 내보내지 않는다. 그리고 닫기 전에 생긴 손실은 숨기지 않고 공개한다.
-->

---

<OperatorSlide section="02 · 설계">

<ChapterDivider number="02" title="설계" subtitle="불확실하면 추정하지 않고, 쓰기를 받지 않습니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 설계]
다음 주제를 알리는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-compact" section="02 · 설계 · 전체 구조" source="전체 아키텍처 · 쓰기 격리 ADR-0005 · 재구축 ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">1차 아키텍처 위에 쓰기 격리와 재구축을 더했습니다</h1><svg class="op-arch" style="max-height:372px" viewBox="0 0 900 384" role="img" aria-label="1차 전체 아키텍처 위에 이번에 더한 것: A 쓰기 격리 판단은 Operator가, B 격리 시 읽기-쓰기 Broker를 0개로 줄여 SQL 경로를 닫고, C 볼륨을 잃은 멤버는 요청에 따라 현재 master의 백업으로 다시 채웁니다.">
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
<path class="ctl" d="M0 364H40"/><text class="s" x="48" y="368">운영 경로 ①–④</text>
<path class="mgmt" d="M0 382H40"/><text class="s" x="48" y="386">생성·관리 · 백업 데이터 · 관측</text>
<rect x="0" y="92" width="140" height="132" rx="8" style="fill:#fff7ed;stroke:#c2410c;stroke-width:1.5"/><text x="10" y="112" style="fill:#c2410c;font-weight:700">이번에 더한 것</text><text class="s" x="10" y="136"><tspan style="fill:#c2410c;font-weight:700">A</tspan> 쓰기 격리 판단</text><text class="s" x="10" y="160"><tspan style="fill:#c2410c;font-weight:700">B</tspan> RW Broker 0개로</text><text class="s" x="22" y="176">SQL 경로 차단</text><text class="s" x="10" y="200"><tspan style="fill:#c2410c;font-weight:700">C</tspan> 명시적 재구축</text><text class="s" x="22" y="216">master 백업 → 복원</text>
<circle cx="352" cy="32" r="9" style="fill:#fff7ed;stroke:#c2410c;stroke-width:1.5"/><text x="352" y="36" text-anchor="middle" style="fill:#c2410c;font-weight:700" font-size="11">A</text>
<rect x="309" y="232" width="132" height="62" rx="9" style="fill:none;stroke:#c2410c;stroke-width:2.5"/><circle cx="440" cy="234" r="9" style="fill:#fff7ed;stroke:#c2410c;stroke-width:1.5"/><text x="440" y="238" text-anchor="middle" style="fill:#c2410c;font-weight:700" font-size="11">B</text>
<circle cx="874" cy="186" r="9" style="fill:#fff7ed;stroke:#c2410c;stroke-width:1.5"/><text x="874" y="190" text-anchor="middle" style="fill:#c2410c;font-weight:700" font-size="11">C</text>
</svg>

</OperatorSlide>

<!--
[40초 · 02 · 설계 · 전체 구조]
1차 때 보여 드린 전체 아키텍처입니다. 구조 자체는 그대로입니다. master 선출과 복제는 CUBRID HA가 하고, Operator는 각 멤버의 Instance Manager에 역할을 묻고 결과를 status에 기록합니다. Operator는 SQL을 중계하지 않습니다.

이번에 더한 것은 주황색 세 가지입니다. A, Operator가 master를 확신할 수 없다고 판단하면 쓰기 격리를 기록합니다. B, 격리 중에는 읽기-쓰기 Broker를 0개로 줄여 애플리케이션의 쓰기 경로를 실제로 닫습니다. C, 볼륨을 잃은 멤버는 사람이 요청하면 현재 master의 백업으로 다시 채웁니다. 다음 장부터 하나씩 보겠습니다.
-->

---

<OperatorSlide class="op-compact" section="02 · 설계 · 쓰기 격리" source="ADR-0005 쓰기 격리" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md">

<h1 class="op-title">불확실한 master로 향하는 쓰기 경로를 닫습니다</h1><WriteIsolationDiagram /><p class="op-caption">자동 해제: 멤버를 확인하지 못해 걸린 격리는 master와 다른 멤버가 안전하다는 것을 10초 이상 간격으로 두 번 확인하면 풀림<br>master가 둘인 경우처럼 사람이 판단해야 하면: 이번 격리에만 쓸 수 있는 일회용 토큰으로 해제</p><p class="op-boundary"><b>확인 기준</b>　Broker Pod 종료 + endpoint 비움 + 기존·새 세션의 쓰기 승인 0건</p>

</OperatorSlide>

<!--
[55초 · 03 · 쓰기 격리]
실선은 클라이언트의 쓰기 경로이고, 파란 점선은 Operator의 관찰과 제어입니다. Operator는 Instance Manager를 통해 멤버 역할을 확인합니다. master를 확신할 수 없으면 격리를 기록하고 읽기-쓰기 Broker Deployment를 0개로 줄입니다. 실제 차단은 Pod 종료와 endpoint 비움, 기존 세션과 새 세션 모두의 쓰기 거절까지 확인합니다.

자동 해제는 아무 격리에나 적용되지 않습니다. 멤버 미확인 격리에 한해 같은 단일 master와 다른 멤버의 안전 근거를 10초 이상 간격으로 두 번 확인해야 합니다. 다중 master 등은 수동 판단이 필요하며, 현재 격리의 멤버 집합에 연결된 일회용 토큰으로 승인합니다.

상세 조건 — ADR-0005 Release: 두 차례 모두 격리에 기록된 같은 master를 확인하고, 다른 승격 가능 멤버는 인증·식별이 일치하는 최신 non-master 응답 또는 승인·감사된 외부 VM 전원 차단 확인과 out-of-service taint가 필요합니다. 멤버 식별이나 근거가 바뀌면 재확인하거나 자동 해제를 금지합니다. 외부 차단 근거에 따른 해제는 PrimaryResolved=True를 뜻하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
-->

---

<OperatorSlide class="op-compact" section="02 · 설계 · 경계" source="시나리오 계약 · S07–S08" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">Operator가 닫을 수 있는 것과 닫을 수 없는 것</h1><div class="op-safety"><div><span>Operator가 약속</span><h3>관리하는 읽기-쓰기 경로는 닫습니다</h3><p>경로를 닫은 뒤에는 새 연결이든 이미 열린 세션이든 쓰기가 승인되면 안 됩니다. 이것은 v0.1에서 반드시 지키는 안전 규칙입니다.</p><p class="op-mini">닫힌 뒤 승인된 쓰기 0건</p></div><div><span>Operator가 약속하지 않음</span><h3>CUBRID 자체 승격과 닫기 전 손실</h3><p>CUBRID HA는 Operator와 무관하게 다른 멤버를 master로 올릴 수 있습니다. 경로를 닫기 전에 승인된 쓰기가 새 master에 없을 수 있고, 이 손실은 숨기지 않고 공개합니다.</p><p class="op-mini">데이터 손실 0 보장 안 함</p></div></div><p class="op-boundary"><b>그래서</b>　안전 규칙은 통과/실패로 판정 · 차단 시간과 데이터 손실은 측정해 공개</p>

</OperatorSlide>

<!--
[40초 · 03 · 쓰기 격리의 경계]
여기서 경계를 분명히 하겠습니다. Operator가 약속하는 것은 자기가 관리하는 읽기-쓰기 경로를 닫는 것입니다. 닫힌 뒤에는 새 연결이든 이미 열려 있던 세션이든 쓰기가 승인되면 안 되고, 이것은 반드시 지킵니다.

반면 CUBRID HA는 Operator와 상관없이 다른 멤버를 master로 올릴 수 있습니다. 경로를 닫기 전에 승인된 쓰기가 새 master에 없을 수 있습니다. 이건 엔진 동작이라 Operator가 막을 수 없어서, 데이터 손실 0을 보장한다고 말하지 않고 측정해서 공개하기로 했습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
-->

---

<OperatorSlide class="op-compact" section="02 · 설계 · 재구축" source="볼륨 교체 재구축 #118" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118">

<h1 class="op-title">볼륨을 잃은 멤버는 명시적인 요청으로 다시 채웁니다</h1><div class="op-timeline"><div><small>① 감지</small><b>빈 볼륨으로 다시 뜬 멤버</b><p>데이터가 없는 멤버는<br>쓰기 격리에 들어감</p></div><div><small>② 요청</small><b>사람이 재구축 요청</b><p>자동으로 덮어쓰지 않음<br>대상 멤버와 볼륨 확인</p></div><div><small>③ 재구축</small><b>현재 master에서 다시 채움</b><p>master 백업을 옮겨 복원한 뒤<br>slave로 다시 합류</p></div><div><small>④ 확인</small><b>확인된 행 대조</b><p>장애 전 승인된 모든 행이<br>재구축한 멤버에 있는지</p></div></div><p class="op-boundary"><b>측정</b>　Kind에서 요청부터 완료까지 40.2초, 모든 행 확인까지 48.9초 · v0.1 제한은 5분</p>

</OperatorSlide>

<!--
[40초 · 04 · 재구축]
두 번째 아키텍처는 볼륨을 잃은 멤버의 재구축입니다. 데이터가 없는 멤버가 다시 뜨면 Operator는 그 멤버를 자동으로 덮어쓰지 않습니다. 쓰기 격리에 넣고, 사람이 대상 멤버와 볼륨을 확인한 뒤 재구축을 요청하게 했습니다.

요청하면 살아 있는 멤버에서 백업으로 채우고 slave로 다시 합류시킵니다. 마지막으로 장애 전에 승인된 모든 행이 재구축한 멤버에 있는지 SQL로 대조합니다. Kind에서는 요청부터 완료까지 40초 정도였고, v0.1 제한은 여유를 두고 5분으로 정했습니다. 남아 있던 데이터로 자동 재합류하는 기능은 v0.2로 미뤘습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118
-->

---

<OperatorSlide section="03 · 증거">

<ChapterDivider number="03" title="증거와 한계" subtitle="막은 것과 막지 못한 것을 모두 보여 드립니다" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 증거와 한계]
다음 주제를 알리는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 증거 · 같은 장애 비교" source="VM 랩 비교 실행 2026-11-25 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">같은 장애를 두 번 연속 냈을 때, 사람 없이 돌아온 쪽</h1><table class="op-comparison"><thead><tr><th>VM 랩 · HA 3대 · 쓰기 중 master Pod 강제 삭제</th><th>CUBRID/cubrid-operator</th><th>이 Operator</th></tr></thead><tbody><tr><td>쓸 수 있는 상태까지</td><td>멤버마다 DB 생성·HA 시작·Broker 시작을 사람이 실행</td><td>수동 단계 없음 · 약 2분</td></tr><tr><td>1번째 삭제</td><td>승인된 쓰기 손실 0 · 끊김 12.4초 · <b>지운 멤버는 사람이 다시 붙임</b></td><td>손실 0 · 끊김 22.0초 · 지운 멤버 자동 복귀</td></tr><tr><td>2번째 삭제</td><td>손실 0 · <b>새 master 선출 안 됨 → 31분간 쓰기 불가</b>, Pod는 모두 Ready</td><td>손실 0 · 끊김 32.8초 · 세 멤버 모두 자동 복귀</td></tr><tr><td>장애 중 상태 표시</td><td>master “알 수 없음”에 머묾</td><td>현재 primary · 격리 여부 · Ready</td></tr></tbody></table><p class="op-boundary"><b>공개할 점</b>　쓰기 끊김은 저희가 더 깁니다(확인될 때까지 닫음) · operator별 2회 실행 · 네트워크 분할은 비교하지 않음</p>

</OperatorSlide>

<!--
[45초 · 03 · 같은 장애 비교]
CUBRID 공식 조직에도 Kubernetes operator가 있습니다. 같은 VM 랩에서 두 operator로 HA 3대를 띄우고, 같은 클라이언트가 쓰는 중에 master Pod를 두 번 연속 강제로 지웠습니다.

첫 번째 장애는 둘 다 넘겼습니다. 승인된 쓰기 손실은 둘 다 0건이었습니다. 첫 장애를 넘기는 것은 CUBRID HA 자체가 하기 때문입니다. 차이는 그다음입니다. 공식 operator에서는 지운 멤버가 저절로 돌아오지 않아 사람이 다시 붙였고, 두 번째 장애에서는 새 master가 뽑히지 않아 31분 동안 쓰기를 못 했습니다. 그동안 Pod는 모두 Ready로 보였습니다. 원인은 멤버마다 노드 목록 순서가 달라진 것이었습니다. 저희 Operator는 두 번 모두 사람 없이 세 멤버로 돌아왔습니다.

대신 쓰기가 끊긴 시간은 저희가 22초와 33초로 더 깁니다. 새 Pod가 확인될 때까지 쓰기를 닫기 때문이고, 그중 절반 정도는 Broker를 다시 띄우는 시간이라 줄일 수 있는 부분으로 보고 있습니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 증거 · VM 랩" source="VM 랩 실행 기록 #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">VM 랩에서 격리 유지와 복구 동작을 확인했습니다</h1><table class="op-comparison op-results-v2"><thead><tr><th>시험</th><th>관찰 결과</th><th>현재 판정</th></tr></thead><tbody><tr><td><b>분할 중 Operator 재시작</b></td><td>같은 격리 유지 · Broker 0개<br>쓰기 승인 없음 · 확인된 행 보존</td><td><b>안전 규칙 통과</b></td></tr><tr><td><b>볼륨 교체 재구축</b></td><td>재구축 후 행 대조</td><td><b>통과</b></td></tr><tr><td><b>새 클러스터 복원</b></td><td>3회 복원 · 세션 끊김 없음</td><td><b>통과</b></td></tr><tr><td><b>VM 전원 손실</b></td><td>역할·접속 복구 시간 분포</td><td>측정 중</td></tr><tr><td><b>해제 후 재분할</b></td><td>옛 토큰이 새 격리를 풀지 못하는지</td><td>실행 전</td></tr></tbody></table><p class="op-boundary"><b>결과의 범위</b>　위 분할 시험의 행 보존은 해당 실행 결과입니다.<br>다른 조건에서 관찰한 데이터 손실은 다음 장에 별도로 공개합니다.</p>

</OperatorSlide>

<!--
[45초 · 05 · VM 랩 결과]
VM 랩에서는 실제로 장애를 냈습니다. 네트워크 분할 중에 Operator를 재시작해도 같은 격리가 유지됐고, Broker는 0개, 분할 동안 쓰기 승인은 없었으며, 끝난 뒤 모든 멤버에 확인된 행이 남아 있었습니다. 볼륨 교체 재구축과 새 클러스터 복원도 VM 랩에서 통과했습니다.

VM 전원 손실은 복구 시간 분포를 측정하는 중입니다. 첫 격리를 해제한 뒤 다시 분할했을 때 옛 토큰으로 새 격리를 풀 수 없는지 보는 시험은 코드 리뷰를 마쳤고, VM 랩 실행은 아직입니다. 랩은 공유 자원이라 한 번에 하나만, 공지하고, 점유 Lease를 잡은 상태에서만 실행합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-compact" section="03 · 증거 · Kind" source="Kind E2E 실행 기록" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1109">

<h1 class="op-title">Kind에서는 전체 테스트를 매번 돌립니다</h1><div class="op-specs-head"><span class="op-evidence-number">55 / 55</span><div><b>Kind E2E 테스트 55개 통과</b><p>1차의 27개에서 늘어났습니다 · 실제 CUBRID 이미지로 한 번 도는 데 약 64분</p></div></div><table class="op-comparison"><thead><tr><th>항목</th><th>결과</th></tr></thead><tbody><tr><td><b>1차의 위험을 다시 시험</b>: 쓰기 중에 master Pod 강제 삭제</td><td>쓰기 격리가 읽기-쓰기 경로를 닫고, 삭제된 멤버의 새 Pod가 확인될 때까지 열지 않음 · 승인된 쓰기가 사라지지 않았는지 대조</td></tr><tr><td>테스트가 DB에 로컬 소켓으로 붙을 때 가끔 세션이 끊김</td><td>11.10–11.20 실패한 실행 58건 중 9건이 이 원인 → TCP 접속으로 바꾼 11.22 이후 같은 원인의 실패 없음</td></tr><tr><td>재구축 중 다른 멤버의 역할 확인이 한 번 늦음</td><td>원인을 바로 보여 주도록 테스트 개선</td></tr></tbody></table><p class="op-boundary"><b>한계</b>　Kind 통과는 VM 랩 검증을 대신하지 않습니다</p>

</OperatorSlide>

<!--
[35초 · 05 · Kind 결과]
먼저 Kind 결과입니다. 1차 때 27개였던 E2E 테스트가 55개로 늘었고, 실제 CUBRID 이미지로 전부 통과합니다. 한 번 도는 데 64분 정도 걸리는데, 이 시간을 줄이는 것도 지금 과제입니다.

불안정했던 테스트도 원인을 찾아 고쳤습니다. 테스트가 DB에 로컬 소켓으로 붙을 때 세션이 가끔 끊겼는데, 11월 10일부터 20일까지 실패한 실행 58건 중 9건이 이 원인이었고, 11월 22일 TCP 접속으로 바꾼 뒤로는 아직 같은 원인의 실패가 없습니다. 관찰 기간이 짧아서 계속 지켜보고 있습니다. 다만 Kind 통과가 VM 랩 검증을 대신하지는 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1109

1차에서 본 위험도 같은 시험으로 다시 확인합니다. 쓰기가 이어지는 중에 master Pod를 강제로 삭제하면, 이제는 쓰기 격리가 읽기-쓰기 경로를 닫고, 삭제된 멤버의 새 Pod가 확인될 때까지 열지 않습니다. 그 뒤 승인된 쓰기가 사라지지 않았는지 대조합니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 증거 · 검증이 찾은 결함" source="#1158 · 수정 PR #1159" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158">

<h1 class="op-title">검증이 참조 환경의 결함을 찾아냈습니다</h1><div class="op-timeline"><div><small>① 증상</small><b>잡아 둔 연결이 끊김</b><p>Broker 용량 측정 중<br>CAS가 남았는데도<br>-199 오류</p></div><div><small>② 좁히기</small><b>층별로 나눠 시험</b><p>같은 Pod 안: 정상<br>다른 노드: 끊김<br>정책을 끄면: 정상</p></div><div><small>③ 원인</small><b>생존 확인이 막힘</b><p>CUBRID가 30초쯤 조용한 상대를<br>TCP 7로 확인하는데<br>NetworkPolicy가 조용히 버림</p></div><div><small>④ 수정</small><b>정책에 7번 허용</b><p>멤버 → Broker TCP 7만<br>다른 Pod는 계속 차단<br>랩 회귀 통과 · 리뷰 중</p></div></div><p class="op-boundary"><b>의미</b>　검증 방식이 실제 결함을 잡습니다 · Kind는 정책을 적용하지 않아 놓친 문제를 VM 랩 반복 측정으로 찾았습니다</p>

</OperatorSlide>

<!--
[40초 · 03 · 검증이 찾은 결함]
VM 랩 검증이 실제로 결함을 찾아낸 사례도 하나 말씀드리겠습니다. Broker 용량을 재다가, CAS가 남아 있는데도 잡아 둔 연결이 -199 오류로 끊기는 걸 봤습니다. 층을 나눠 시험해 보니 같은 Pod 안에서는 멀쩡하고, 다른 노드에서 오면 끊기고, NetworkPolicy를 끄면 다시 멀쩡했습니다.

원인은 CUBRID의 생존 확인이었습니다. 30초쯤 조용한 상대를 TCP 7번으로 확인하는데, Broker 정책이 이 포트를 열지 않아 패킷이 조용히 버려지고, 서버는 상대가 죽은 줄 알고 연결을 끊었습니다. 멤버에서 Broker로 가는 7번만 허용하는 수정을 올렸고, 그 정책만으로 VM 랩에서 노드를 건넌 세션 40개와 Broker를 거친 연결 30개가 45초씩 세 번 쉬어도 모두 유지됐습니다. 지금은 리뷰 중입니다. Kind는 정책을 적용하지 않아서 놓쳤던 문제를 실제 환경에서 찾은 것입니다.
-->

---

<OperatorSlide class="op-compact" section="03 · 증거 · 공개할 한계" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">숨기지 않고 공개할 한계</h1><ol class="op-risks"><li><b>복제 지연 후 VM 전원 차단: 승인된 쓰기 13건이 새 master에 없음</b><span>2026-11-19 VM 시험 · 복제 프로세스를 정지한 조건 · 해당 행은 옛 master 디스크에만 남음</span></li><li><b>네트워크 분할에서 승격된 멤버에 승인된 쓰기 최대 73건 없음</b><span>11월 17–18일 VM 분할 5회에서 13–73건 미반영 · 1회는 73건이 없는 멤버가 active master로 전환</span></li><li><b>master Pod 정상 종료 때 쓰기 경로가 28초 닫힘</b><span>불필요한 격리 · 시간과 원인을 공개</span></li><li><b>스토리지는 node-local, CSI 아님</b><span>볼륨이 다른 노드로 따라가는 동작·스냅샷·크기 변경은 검증하지 않음</span></li></ol><p class="op-boundary"><b>원칙</b>　Operator의 제어 범위와 엔진 동작의 한계를 구분하고, 재현 조건과 영향을 공개합니다</p>

</OperatorSlide>

<!--
[45초 · 05 · 공개할 한계]
공개할 한계입니다. 복제 프로세스를 정지한 뒤 VM 전원을 차단한 시험에서 승인된 쓰기 13건이 새 master에 없었습니다. 해당 행은 옛 master 디스크에만 남았습니다. 원인에 대한 가설과 관측 결과는 구분합니다. 네트워크 분할에서는 경로를 닫기 전에 승인된 쓰기가 승격된 멤버에 최대 73건 없었습니다. master Pod를 정상 종료할 때 쓰기 경로가 28초 닫히는 문제도 있습니다.

그리고 저희 랩은 node-local 스토리지라 CSI 동작은 검증하지 않았습니다. 이 숫자는 각각의 시험 조건에서 관찰한 결과입니다. 앞 장의 격리 유지 시험과 혼동하지 않도록 구분합니다. 승격된 멤버의 미반영과 전체 멤버에서의 최종 손실도 같은 뜻으로 쓰지 않습니다. 제어 가능한 범위와 엔진 동작의 한계를 구분해 공개하겠습니다.

관측 근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035 및 https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md (section 8의 2026-11-17–18 VM 기록).

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide section="04 · v0.1">

<ChapterDivider number="04" title="그래서 v0.1" subtitle="증거에서 나온 약속과 일정" />

</OperatorSlide>

<!--
[0초 · 챕터 전환 · 그래서 v0.1]
다음 주제를 알리는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-compact" section="04 · v0.1 · 범위" source="ROADMAP · 시나리오 계약" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">안전 규칙은 필수, 시간과 손실은 측정 공개</h1><table class="op-comparison op-acceptance"><thead><tr><th>구분</th><th>약속하는 범위</th><th>공개 조건</th></tr></thead><tbody><tr><td><b>반드시 통과</b></td><td>설치·복제 / 장애 대응<br>볼륨 재구축·백업·복원 / 운영 안전</td><td>필수 항목의 실패·막힘·미실행이 없어야 함</td></tr><tr><td><b>측정해서 공개</b></td><td>VM 전원 손실 · 네트워크 분할·반복 장애<br>master Pod 정상 종료</td><td>안전 규칙은 통과 필수<br>시간·손실은 측정값 공개</td></tr><tr><td><b>v0.2로 미룸</b></td><td>남아 있던 데이터로 자동 재합류<br>재생성한 클러스터의 옛 볼륨 자동 채택</td><td>이번 공개 범위에서 제외</td></tr></tbody></table><p class="op-boundary"><b>검증 환경</b>　CUBRID 11.4.x · amd64 · k3s 워커 3대 (각 2 vCPU·8 GiB)<br>node-local 스토리지 · CSI 동작은 검증 범위 밖</p>

</OperatorSlide>

<!--
[35초 · 02 · v0.1 범위]
v0.1의 약속은 세 가지입니다. 설치·복제, 장애 대응, 재구축·복원과 운영 안전은 반드시 통과해야 합니다. VM 전원 손실과 분할, 정상 종료는 시간과 손실을 측정해 공개하되, 안전 규칙은 똑같이 통과해야 합니다. 자동 재합류와 옛 볼륨 자동 채택은 v0.2로 미룹니다. 검증 환경은 CUBRID 11.4와 amd64, node-local 스토리지를 쓰는 3-VM 랩으로 한정합니다.

상세 시나리오: 필수 S00–S02, S03 abrupt, S05–S06, S10–S15, 상태·이벤트·메트릭. 측정 S04, S07–S08, S03 graceful. 이월 S09 및 옛 볼륨 자동 채택.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
-->

---

<OperatorSlide class="op-compact" section="04 · v0.1 · 판정 방식" source="릴리스 후보 검증 #126" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126">

<h1 class="op-title">과거 결과는 보존하고, 새 판정은 따로 남깁니다</h1><div class="op-safety"><div><span>원래 결과</span><h3>실패 기록을 통과로 바꾸지 않습니다</h3><p>기존 시간 기준을 넘긴 기록도 그대로 보존합니다. 새 범위로 판정하는 이유를 함께 남깁니다.</p></div><div><span>v0.1 판정</span><h3>안전 규칙 위반은 그대로 실패입니다</h3><p>측정 항목은 시간·손실을 공개합니다. 필수 항목은 정한 기준을 통과해야 합니다.</p><p class="op-mini">예: 볼륨 교체 재구축은 5분 이내</p></div></div><p class="op-boundary"><b>공통 원칙</b>　필수 증거가 빠지면 통과가 아니라 막힘입니다</p>

</OperatorSlide>

<!--
[20초 · 02 · 판정 방식]
범위를 바꿔도 과거 실패 기록은 그대로 보존합니다. v0.1 판정은 별도로 남기고, 안전 규칙 위반은 여전히 실패입니다. 측정 항목의 시간과 손실은 공개하지만, 필수 항목인 볼륨 교체 재구축은 5분 기준을 통과해야 합니다. 필수 증거가 없으면 막힘입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide section="04 · v0.1 · 일정" source="ROADMAP v0.1 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">12월 7일 후보 동결, 반복 검증과 독립 재현</h1><div class="op-timeline"><div><small>11.30–12.06</small><b>후보 준비</b><p>판정 도구 정렬<br>이미지·소스 식별<br>랩 통제 점검</p></div><div><small>12.07</small><b>후보 동결</b><p>소스·이미지·엔진·랩을<br>하나로 고정</p></div><div><small>12.08–12.14</small><b>반복 검증</b><p>필수 시나리오 반복<br>24시간 부하 시험</p></div><div><small>12.15–12.20</small><b>독립 재현</b><p>작성자가 아닌 사람이<br>문서만 보고 설치·복구·복원</p></div></div><p class="op-boundary"><b>12.21–12.27</b> 증거를 보고 공개 여부 결정　·　작성자와 최종 검증자는 다른 사람 · 필수 증거가 빠지면 공개하지 않음</p>

</OperatorSlide>

<!--
[40초 · 06 · 릴리스 일정]
남은 일정입니다. 11월 말부터 판정 도구와 이미지 식별, 랩 통제를 정리하고, 12월 7일에 소스와 이미지, 엔진 버전, 랩을 하나로 고정합니다. 그 후보로 필수 시나리오를 반복하고 24시간 부하 시험을 합니다.

12월 15일부터는 코드를 쓰지 않은 사람이 문서만 보고 설치, 장애 복구, 복원을 재현합니다. 마지막 주에 증거를 보고 공개 여부를 정합니다. 작성자와 최종 검증자는 다른 사람입니다. 날짜에 맞추려고 억지로 공개하지 않고, 필수 증거가 빠지면 공개하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide section="마무리">

<h1 class="op-title">상태 표시에서 실제 쓰기 차단과 재구축으로</h1><div class="op-release"><div><p class="op-kicker">구현·시험</p><h3>쓰기 격리</h3><p>master가 불확실할 때<br>관리하는 쓰기 경로 차단</p></div><div><p class="op-kicker">구현·시험</p><h3>명시적 재구축</h3><p>볼륨을 잃은 멤버를<br>요청에 따라 복구·대조</p></div><div><p class="op-kicker">남은 공개 조건</p><h3>안전성 검증·독립 재현</h3><p>고정한 후보의 필수 증거와<br>작성자 외 검증자의 재현</p></div></div><p class="op-boundary"><b>한 문장으로</b>　장애 뒤 사람 없이 다시 쓸 수 있는 상태로 돌아옵니다.<br>확신할 수 없는 동안은 쓰기를 닫고, 닫혀 있던 시간과 손실은 공개합니다.</p>

</OperatorSlide>

<!--
[20초 · 마무리]
이번 검증에서는 미확정 상태 표시에서 실제 쓰기 경로 차단으로 나아갔고, 볼륨을 잃은 멤버의 명시적 재구축을 구현하고 시험했습니다. 남은 안전성 검증과 독립 재현을 릴리스 조건으로 삼겠습니다. 다시 한 문장으로 정리하면, 확신할 수 없으면 쓰기 경로를 닫고 닫은 뒤에는 쓰기 성공을 내보내지 않습니다. 닫기 전의 손실과 닫혀 있던 시간은 조건과 함께 공개하겠습니다.
-->

---

<OperatorSlide section="Q&A" source="Operator 저장소" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><div class="op-meta"><b>github.com/cubrid-lab/cubrid-kubernetes-operator</b></div></div>

</OperatorSlide>

<!--
[Q&A]
감사합니다. 질문 받겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

<OperatorSlide class="op-compact" section="부록 · 1차 이후 바뀐 것" source="ROADMAP 2026-11-21 결정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">1차에는 계획, 지금은 측정한 결과로 말합니다</h1><table class="op-comparison"><thead><tr><th></th><th>1차 검증 (10월 말)</th><th>2차 검증 (지금)</th></tr></thead><tbody><tr><td><b>쓰기 안전</b></td><td>master 미확정이면 “미확정”으로 표시만</td><td>쓰기 격리 구현 · 읽기-쓰기 Broker를 0으로 줄여 쓰기 경로를 닫음</td></tr><tr><td><b>장애 시험</b></td><td>Kind 중심, VM 장애는 아직</td><td>VM 랩에서 전원 차단·네트워크 분할·Operator 재시작까지 실행</td></tr><tr><td><b>판정</b></td><td>“30초 안에 복구” 같은 숫자 기준</td><td>안전 규칙은 통과/실패, 시간은 측정해서 공개</td></tr><tr><td><b>범위</b></td><td>필수 시나리오 16개 전부</td><td>11월 21일 범위 결정 · 일부는 측정 공개, 자동 재합류는 v0.2</td></tr></tbody></table><p class="op-boundary"><b>바뀐 이유</b>　VM 랩에서 CUBRID 자체 동작의 한계를 직접 확인했기 때문입니다.</p>

</OperatorSlide>

<!--
[40초 · 01 · 1차 이후 바뀐 것]
1차 때와 비교하면 네 가지가 바뀌었습니다. 1차에는 master가 불확실하면 상태에 미확정이라고 표시만 했습니다. 지금은 쓰기 격리를 구현해서, 실제로 읽기-쓰기 Broker를 0개로 줄여 쓰기 경로를 닫습니다. 장애 시험도 Kind에서 VM 랩으로 옮겨 전원 차단, 네트워크 분할, Operator 재시작까지 실행했습니다.

그리고 판정 방식과 범위를 바꿨습니다. VM 랩에서 장애를 내 보니, CUBRID 엔진 자체 동작 때문에 Operator가 보장할 수 없는 부분이 분명히 보였습니다. 그래서 11월 21일에 v0.1이 약속하는 범위를 좁히기로 결정했습니다. 다음 장에서 자세히 말씀드리겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide section="부록 · 팀 역할" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md">

<h1 class="op-title">만든 사람과 검증하는 사람을 나눕니다</h1><div class="op-people"><div><p class="op-kicker">구현 · 시나리오 실행</p><b>만들고 기록합니다</b><p>Operator 구현, 장애 시나리오, 판정 도구, VM 랩 실행 기록을 맡습니다.</p></div><div><p class="op-kicker">리뷰 · 랩 · 독립 재현</p><b>교차 검증합니다</b><p>코드와 실행 결과를 교차 검증하고, VM 랩 인프라를 운영하며, 공개 전 문서만 보고 재현합니다.</p></div></div><p class="op-boundary"><b>원칙</b>　작성자와 최종 검증자는 다른 사람입니다 · 공유 랩 장애 시험은 한 번에 하나씩 · 공개 여부는 함께 결정</p>

<p class="op-caption"><a href="#/21">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
팀 역할은 1차 때 말씀드린 원칙을 그대로 지키고 있습니다. 구현과 시나리오 실행, 그리고 리뷰와 랩 운영, 독립 재현을 나눴습니다. 작성자와 최종 검증자를 다르게 하고, 공유 랩 시험은 한 번에 하나씩, 공개 여부는 함께 결정합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md
-->

---

<OperatorSlide class="op-compact" section="부록 · v0.1 이후" source="ROADMAP · v0.2 후보" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">v0.1 이후에는 미룬 것부터 다시 봅니다</h1><div class="op-goals"><div><span>01</span><b>자동 재합류</b><p>남아 있던 데이터로 멤버가 안전하게 다시 합류 (S09)</p></div><div><span>02</span><b>옛 볼륨 채택</b><p>클러스터를 다시 만들 때 기존 볼륨을 안전하게 이어받기</p></div><div><span>03</span><b>아카이브 로그 한도</b><p>멤버 볼륨 안에서 아카이브 로그가 차지할 공간 제한</p></div><div><span>04</span><b>관찰과 격리 정책 분리</b><p>HA 상태 수집과 쓰기 격리 판단을 나눠 다시 설계</p></div></div><p class="op-caption">로드맵에서 v0.1 이후로 미룬 항목입니다 · 우선순위는 v0.1 결과와 사용자 피드백을 보고 정합니다</p>

<p class="op-caption"><a href="#/21">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
v0.1 이후에는 로드맵에서 미뤄 둔 것부터 다시 봅니다. 남아 있던 데이터로 자동 재합류, 클러스터를 다시 만들 때 옛 볼륨을 이어받는 것, 멤버 볼륨 안에서 아카이브 로그 공간을 제한하는 것, 그리고 HA 상태 수집과 쓰기 격리 판단을 나누는 설계입니다. 우선순위는 v0.1 결과와 사용자 피드백을 보고 정하겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->
