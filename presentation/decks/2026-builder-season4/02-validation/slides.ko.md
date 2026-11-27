---
title: "CUBRID Kubernetes Operator — 2차 검증"
---

<OperatorSlide class="op-session" section="Opening · 프로젝트 소개" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">빌더 시즌4 · 2차 검증</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">DB 서버가 장애로 바뀌었습니다.<br>앱은 언제 다시 써도 될까요?</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[20초 · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. DB 서버가 장애로 바뀌었습니다. 앱은 언제 다시 데이터를 써도 될까요? 오늘은 저희가 그 판단을 어떻게 돕고, 실제 장애 시험에서 무엇을 확인했는지 말씀드리겠습니다.
-->

---

<OperatorSlide class="op-compact op-session" section="발표 순서">

<h1 class="op-title">발표 순서</h1>

<div class="op-agenda">
  <div><span>01</span><b>프로젝트 소개</b></div>
  <div><span>02</span><b>1차 피드백 반영</b></div>
  <div><span>03</span><b>개발 현황과 아키텍처</b></div>
  <div><span>04</span><b>검증 결과와 시행착오</b></div>
  <div><span>05</span><b>함께 논의할 질문</b></div>
  <div><span>06</span><b>최종 발표까지의 계획</b></div>
</div>

</OperatorSlide>

<!--
[10초 · 발표 순서]
먼저 프로젝트와 1차 피드백을 소개하고, 바뀐 설계와 시험 결과를 보여드리겠습니다. 마지막으로 함께 논의할 질문과 공개 전 계획을 말씀드리겠습니다.
-->

---

<OperatorSlide class="op-compact op-session" section="01 · 프로젝트 소개">

<h1 class="op-title">Operator와 Instance Manager가 포함된 전체 구조</h1>

<svg class="op-arch" style="max-height:340px" viewBox="0 0 900 392" role="img" aria-label="CUBRID Kubernetes Operator 전체 구조. 개발하는 구성 요소는 클러스터를 관리하는 Operator와 각 DB 서버에서 상태 조회 및 작업을 수행하는 Instance Manager입니다. 앱은 Service와 Broker를 거쳐 CUBRID에 접속합니다. CUBRID가 master 선출과 데이터 복제를 맡으며, 백업과 복원에는 S3 호환 저장소를 사용합니다.">
<defs><marker id="op-arch-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0f1b2d"/></marker><marker id="op-arch-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-arch-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="150" y="0" width="750" height="328" rx="10" style="fill:none;stroke-dasharray:3 4"/><text class="s" x="162" y="16">Kubernetes 클러스터</text>
<rect class="box" x="0" y="14" width="130" height="50" rx="8"/><text x="65" y="35" text-anchor="middle">운영자</text><text class="s" x="65" y="53" text-anchor="middle">클러스터 설정·작업 요청</text>
<path class="ctl" d="M130 39H166" marker-end="url(#op-arch-blue)"/><text class="s b" x="148" y="32" text-anchor="middle">①</text>
<rect class="box" x="170" y="24" width="120" height="62" rx="8"/><text x="230" y="46" text-anchor="middle">Kubernetes API</text><text class="s" x="230" y="63" text-anchor="middle">클러스터 설정</text><text class="s" x="230" y="78" text-anchor="middle">백업 요청</text>
<path class="ctl" d="M290 44H336" marker-end="url(#op-arch-blue)"/><text class="s b" x="313" y="37" text-anchor="middle">② 설정</text>
<path class="ctl" d="M338 70H292" marker-end="url(#op-arch-blue)"/><text class="s b" x="315" y="84" text-anchor="middle">④ 상태</text>
<rect class="box op" x="340" y="20" width="290" height="96" rx="8"/><text class="b" x="485" y="43" text-anchor="middle">CUBRID Kubernetes Operator</text><text class="s" x="485" y="64" text-anchor="middle">클러스터 전체의 상태를 확인</text><text class="s" x="485" y="81" text-anchor="middle">쓰기 연결·복구 절차를 조정</text><text class="s" x="485" y="101" text-anchor="middle">운영자에게 진행 상태를 알림</text>
<path class="mgmt" d="M630 50H656" marker-end="url(#op-arch-mute)"/>
<rect class="box" x="660" y="24" width="228" height="62" rx="8"/><text x="774" y="46" text-anchor="middle">운영 상태 확인</text><text class="s" x="774" y="63" text-anchor="middle">클러스터·서버 지표</text><text class="s" x="774" y="78" text-anchor="middle">이벤트 · 구조화 로그</text>
<path class="mgmt" d="M400 116V136" marker-end="url(#op-arch-mute)"/><text class="s" x="392" y="131" text-anchor="end">생성·관리</text>
<path class="ctl" d="M600 116V150" marker-end="url(#op-arch-blue)"/><text class="s b" x="610" y="135">③ 각 서버의 상태 조회·작업 요청</text>
<rect class="box" x="170" y="138" width="262" height="84" rx="8"/><text x="301" y="159" text-anchor="middle">Kubernetes 리소스</text><text class="s" x="301" y="177" text-anchor="middle">DB 서버와 데이터 디스크</text><text class="s" x="301" y="194" text-anchor="middle">앱이 접속하는 주소와 연결 정책</text><text class="s" x="301" y="211" text-anchor="middle">읽기·쓰기용 Broker</text>
<rect class="box ha" x="450" y="152" width="440" height="152" rx="10"/><text x="464" y="174">CUBRID HA 3대 · master 선출과 데이터 복제</text>
<rect class="box ink" x="462" y="184" width="126" height="108" rx="7"/><text class="b" x="525" y="205" text-anchor="middle">서버 0 · master</text><rect class="box im" x="467" y="215" width="116" height="28" rx="5"/><text class="b" x="525" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="525" y="270" text-anchor="middle">CUBRID · 데이터 디스크</text>
<rect class="box ink" x="604" y="184" width="126" height="108" rx="7"/><text x="667" y="205" text-anchor="middle">서버 1 · 복제본</text><rect class="box im" x="609" y="215" width="116" height="28" rx="5"/><text class="b" x="667" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="667" y="270" text-anchor="middle">CUBRID · 데이터 디스크</text>
<rect class="box ink" x="746" y="184" width="126" height="108" rx="7"/><text x="809" y="205" text-anchor="middle">서버 2 · 복제본</text><rect class="box im" x="751" y="215" width="116" height="28" rx="5"/><text class="b" x="809" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="809" y="270" text-anchor="middle">CUBRID · 데이터 디스크</text>
<path class="sql" d="M525 292V299H809V294" marker-end="url(#op-arch-ink)"/><path class="sql" d="M667 299V294" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="0" y="240" width="130" height="46" rx="8"/><text x="65" y="268" text-anchor="middle">애플리케이션</text>
<path class="sql" d="M130 263H166" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="170" y="243" width="128" height="40" rx="8"/><text x="234" y="268" text-anchor="middle">RW / RO Service</text>
<path class="sql" d="M298 263H310" marker-end="url(#op-arch-ink)"/>
<rect class="box ink" x="312" y="235" width="126" height="56" rx="8"/><text x="375" y="257" text-anchor="middle">Broker (RW · RO)</text><text class="s" x="375" y="277" text-anchor="middle">앱의 읽기·쓰기 요청 전달</text>
<path class="sql" d="M438 263H458" marker-end="url(#op-arch-ink)"/>
<path class="mgmt" d="M670 304V340" marker-start="url(#op-arch-mute)" marker-end="url(#op-arch-mute)"/><text class="s" x="680" y="326">백업 업로드 · 복원</text>
<rect class="box store" x="450" y="342" width="440" height="40" rx="8"/><text x="670" y="360" text-anchor="middle">S3 호환 오브젝트 저장소</text><text class="s" x="670" y="376" text-anchor="middle">백업 파일과 검증 정보 저장</text>
<path class="sql" d="M0 346H40"/><text class="s" x="48" y="350">앱의 SQL 요청 · DB 복제</text>
<path class="ctl" d="M0 364H40"/><text class="s" x="48" y="368">운영자의 설정 · Operator의 제어</text>
<path class="mgmt" d="M0 382H40"/><text class="s" x="48" y="386">생성·관리 · 백업 데이터 · 관측</text>
<rect class="box op" x="0" y="93" width="139" height="108" rx="8"/>
<text class="b" x="11" y="117">우리가 만드는 것</text>
<text class="s" x="11" y="142">Operator</text>
<text class="s" x="11" y="161">Instance Manager</text>
<text class="s" x="11" y="184">파란색 상자로 표시</text>
</svg>

</OperatorSlide>

<!--
[35초 · 프로젝트 소개]
저희가 만드는 두 구성 요소는 파란색 상자에 표시했습니다. Operator는 클러스터 전체를 보고 쓰기 연결과 복구를 조정합니다. Instance Manager는 DB 서버마다 하나씩 있고, 그 서버의 상태를 알려주거나 백업·복원 작업을 실행합니다. DB 운영자와 플랫폼 담당자는 이 두 구성 요소로 장애에 대응합니다. 앱은 아래쪽 Service와 Broker를 거쳐 CUBRID에 연결합니다. CUBRID가 쓰기를 받을 서버를 정하고 데이터를 복제하며, 백업 파일은 오른쪽 아래 저장소에 보관합니다.
-->

---

<OperatorSlide class="op-compact op-session" section="02 · 1차 피드백 반영">

<h1 class="op-title">1차 피드백 반영</h1>

<table class="op-comparison">
<thead><tr><th scope="col">1차 의견</th><th scope="col">바꾼 점</th><th scope="col">공개 전 할 일</th></tr></thead>
<tbody>
<tr><td>상태 표시만으로는 쓰기를 막을 수 없음</td><td>쓰기 연결을 끊고, 차단 뒤 성공 응답이 없는지 확인</td><td>새 연결과 기존 연결을 모두 막는지 재시험</td></tr>
<tr><td>쓰기가 얼마나 오래 막히는지 공개</td><td>같은 장애를 내고 공식 Operator와 쓰기 중단 시간 비교</td><td>분할과 전원 차단에서도 시간과 데이터 손실 범위를 따로 기록</td></tr>
<tr><td>복원 성공을 확인할 수 없으면 통과에서 제외</td><td>1차 2건은 보류. 이후 새 클러스터 복원 3건 통과</td><td>공개 후보에서 다시 복원하고 데이터 대조</td></tr>
</tbody>
</table>
<p class="op-caption">2026년 10월 31일 1차 검증 의견 요약</p>

</OperatorSlide>

<!--
[40초 · 02 · 1차 피드백 반영]
1차 검토 의견은 쓰기 격리가 실제로 동작하는지 먼저 입증하라는 것이었습니다. 그래서 네트워크 분할 시험에서 차단 뒤 승인된 쓰기가 없는지 확인했습니다. 안전 때문에 쓰기가 얼마나 멈추는지도 별도로 측정했습니다. 복원은 1차 때 세션이 끊겨 판정을 보류한 두 건을 그대로 남겼고, 이후 새 클러스터로 복원한 시험 세 건에서 통과를 관측했습니다. 공개 후보에서는 실패 조건도 포함해 다시 확인합니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-compact op-session" section="02 · 1차 피드백 비반영">

<h1 class="op-title">1차 피드백 비반영</h1>

<table class="op-comparison">
<thead><tr><th scope="col">1차 의견</th><th scope="col">v0.1 처리</th><th scope="col">미룬 이유</th></tr></thead>
<tbody>
<tr><td>기존 데이터를 보존하며 서버를 다시 합류시킬 것</td><td>기존 디스크로 자동 합류는 v0.2로 미룸.<br>v0.1은 운영자 승인 후 백업으로 재구축</td><td>이전 데이터가 최신 데이터를 덮어쓰지 않는지 검증 필요</td></tr>
<tr><td>공식 Operator에서 전환할 때의 비용과 협력 방식</td><td>전환 비용과 협력 방식은 추가 검토</td><td>이번 비교에서는 강제 삭제 뒤 복구만 확인</td></tr>
<tr><td>외부 스토리지(CSI), 무중단 확장, 복제 지연에 따른 읽기 전환</td><td>이번 검증에 포함하지 않음</td><td>로컬 디스크를 쓰는 가상 서버 3대에서 장애 복구부터 확인</td></tr>
</tbody>
</table>
<p class="op-caption">2026년 10월 31일 1차 검증 의견 요약</p>

</OperatorSlide>

<!--
[30초 · 02 · 1차 피드백 비반영]
재합류 과정에서 최신 데이터를 덮어쓰지 않도록, v0.1에서는 운영자가 대상을 확인하고 현재 master의 백업으로 재구축합니다. 기존 데이터를 자동으로 가져오는 방식은 판별 기준과 검증 증거가 더 필요해 미뤘습니다. 공식 Operator에서 바꿔 쓰는 데 드는 비용과 협력 방식은 추가로 검토합니다. 외부 스토리지, 무중단 확장, 복제 지연에 따른 읽기 전환도 이번 시험에 포함하지 않았습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-compact op-session" section="03 · 개발 현황과 아키텍처">

<h1 class="op-title">v0.1 구현 범위: 쓰기 차단, 서버 재구축, 백업 복원</h1>

<div class="session-debug">
  <div><span>쓰기 차단과 재개</span><h3>불확실하면 쓰기를 막습니다</h3><p>Operator가 서버 상태를 확인하고<br>쓰기용 Broker를 멈춥니다.</p></div>
  <div><span>볼륨 재구축</span><h3>디스크를 잃은 서버를 복구합니다</h3><p>운영자 승인 후 백업으로 재구축하고<br>복제에 합류시킵니다.</p></div>
  <div><span>백업과 복원</span><h3>새 클러스터에 데이터를 복원합니다</h3><p>Instance Manager가 백업을 실행하고,<br>복원 전에 백업 파일을 검증합니다.</p></div>
</div>
<p class="session-takeaway">1차에서는 상태를 알렸습니다. v0.1에서는 쓰기 연결을 실제로 제어하고, 데이터 복구까지 연결합니다.</p>

</OperatorSlide>

<!--
[40초 · v0.1 구현 범위]
저희가 v0.1에서 끝내려는 일은 세 가지입니다. 첫째, 어느 서버가 쓰기를 받을지 불확실하면 실제로 쓰기 연결을 끊습니다. 둘째, 디스크를 잃은 서버는 운영자가 대상을 승인한 뒤 백업으로 다시 구성합니다. 셋째, 백업을 다른 클러스터에 복원할 수 있게 합니다. 1차 때는 주로 상태를 확인하고 알리는 데 집중했습니다. 지금은 Operator가 연결과 복구를 조정하고 Instance Manager가 각 서버에서 작업을 실행합니다. 다음 그림에서 그 역할을 보여드리겠습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-session" section="03 · 개발 현황과 아키텍처 · 현재 구조" source="전체 아키텍처 · 쓰기 격리 ADR-0005 · 재구축 ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">v0.1 세부 아키텍처: Operator와 Instance Manager</h1>

<svg class="op-arch" viewBox="0 0 900 359" role="img" aria-label="v0.1 제어 구조. Kubernetes API의 클러스터와 백업 요청을 Operator의 두 컨트롤러가 처리합니다. Operator는 쓰기용 Broker의 Deployment를 조정하고 각 DB Pod의 Instance Manager를 인증된 HTTP로 호출합니다. Instance Manager는 CUBRID 상태를 조회하고 백업·복원 준비를 실행하며 볼륨에 작업 기록을 남깁니다. 백업 파일과 검증 정보는 S3 호환 저장소에 보관합니다.">
  <defs>
    <marker id="v01-detail-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--blue)"/></marker>
  </defs>
  <rect class="box" x="0" y="41" width="161" height="102" rx="8"/>
  <text x="80" y="64" text-anchor="middle">Kubernetes API</text>
  <text class="s" x="80" y="89" text-anchor="middle">CubridCluster 설정</text>
  <text class="s" x="80" y="109" text-anchor="middle">CubridBackup 요청</text>
  <text class="s" x="80" y="129" text-anchor="middle">승인된 재구축 요청</text>
  <path class="ctl" d="M162 80H205" marker-end="url(#v01-detail-arrow)"/>
  <path class="ctl" d="M207 106H164" marker-end="url(#v01-detail-arrow)"/>
  <text class="s" x="183" y="122" text-anchor="middle">상태</text>

  <rect class="box op" x="210" y="0" width="323" height="239" rx="9" style="fill:none"/>
  <text class="b" x="224" y="23">Operator</text>
  <rect class="box op" x="225" y="36" width="293" height="82" rx="7"/>
  <text x="237" y="58">CubridCluster 컨트롤러</text>
  <text class="s" x="237" y="79">DB·서비스 리소스와 각 서버의 상태 관리</text>
  <text class="s" x="237" y="101">쓰기 차단·재개와 승인된 재구축 조정</text>
  <rect class="box op" x="225" y="128" width="293" height="60" rx="7"/>
  <text x="237" y="149">CubridBackup 컨트롤러</text>
  <text class="s" x="237" y="173">백업 대상 선택·요청·결과 기록</text>
  <rect class="box im" x="225" y="199" width="293" height="26" rx="6"/>
  <text class="s b" x="237" y="217">Instance Manager 호출 · 토큰 인증 HTTP</text>

  <rect class="box" x="0" y="195" width="180" height="78" rx="8"/>
  <text x="90" y="218" text-anchor="middle">쓰기용 Broker Deployment</text>
  <text class="s" x="90" y="241" text-anchor="middle">차단할 때 0개로 줄임</text>
  <text class="s" x="90" y="259" text-anchor="middle">기존 연결 종료 · 새 연결 차단</text>
  <path class="ctl" d="M210 166H189V227H182" marker-end="url(#v01-detail-arrow)"/>

  <rect class="box ha" x="615" y="0" width="284" height="251" rx="9"/>
  <text class="b" x="631" y="23">각 CUBRID DB Pod</text>
  <rect class="box im" x="631" y="36" width="252" height="128" rx="8"/>
  <text class="b" x="643" y="59">Instance Manager</text>
  <text class="s" x="643" y="81">역할·HA 상태 조회</text>
  <text class="s" x="643" y="104">백업 실행·복원 준비</text>
  <text class="s" x="643" y="127">작업 결과 조회</text>
  <text class="s" x="643" y="150">볼륨에 작업 기록 저장</text>
  <path class="ctl" d="M518 211H575V103H629" marker-end="url(#v01-detail-arrow)"/>
  <rect class="box ink" x="631" y="183" width="252" height="51" rx="7"/>
  <text x="757" y="203" text-anchor="middle">CUBRID와 데이터 볼륨</text>
  <text class="s" x="757" y="222" text-anchor="middle">master 선출·복제는 CUBRID가 수행</text>
  <path class="ctl" d="M757 164V180" marker-end="url(#v01-detail-arrow)"/>

  <rect class="box store" x="615" y="284" width="284" height="58" rx="8"/>
  <text x="757" y="307" text-anchor="middle">S3 호환 백업 저장소</text>
  <text class="s" x="757" y="329" text-anchor="middle">백업 파일·체크섬 저장 및 조회</text>
  <path class="ctl" d="M883 111H896V270H863V282" marker-end="url(#v01-detail-arrow)"/>

  <text class="s b" x="0" y="304">v0.1에서 다시 확인할 작업</text>
  <text x="0" y="331">쓰기 차단·재개, 운영자 승인 후 볼륨 재구축, 새 클러스터 복원</text>
</svg>

</OperatorSlide>

<!--
[35초 · v0.1 세부 아키텍처]
v0.1에서 검증할 관리 경로입니다. 왼쪽 Kubernetes API에서 클러스터 설정과 백업 요청을 받습니다. 가운데 Operator의 클러스터 컨트롤러는 서버 상태를 모아 판단하고, 쓰기를 막아야 하면 쓰기용 Broker를 0개로 줄입니다. 백업 컨트롤러는 대상 서버를 정하고 결과를 기록합니다. 오른쪽 각 DB Pod의 Instance Manager는 인증된 요청을 받아 CUBRID 상태를 읽거나 백업과 복원 준비를 실행합니다. 공개 전에는 이 구조로 쓰기 차단과 재개, 승인 후 디스크 재구축, 새 클러스터 복원을 확인합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/DESIGN.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-session" section="03 · 개발 현황과 아키텍처 · 쓰기 격리" source="ADR-0005 쓰기 격리" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md">

<h1 class="op-title">안전을 확인한 뒤 쓰기 연결을 다시 엽니다</h1>
<div class="session-debug">
  <div><span>01 · 확인</span><h3>서버 상태를 봅니다</h3><p>응답을 받지 못하거나 역할 정보가 서로 다르면 쓰기 연결을 닫습니다.</p></div>
  <div><span>02 · 차단</span><h3>기존 연결도 끊습니다</h3><p>쓰기용 Broker를 멈춰 새 연결과 기존 연결을 함께 막습니다.</p></div>
  <div><span>03 · 재개</span><h3>안전 근거를 확인합니다</h3><p>정해진 조건에서 자동으로 엽니다. 그 밖의 경우 운영자가 판단합니다.</p></div>
</div>
<p class="op-caption">이 차단은 쓰기용 Broker에 적용됩니다. 읽기 전용 Broker는 그대로 둡니다.</p>

</OperatorSlide>

<!--
[25초 · 쓰기 차단과 재개]
서버 상태가 불확실하면 새 연결만 막아서는 부족합니다. 이미 열린 연결도 쓰기용 Broker를 멈춰 끊습니다. 상태를 확인하지 못해 차단한 경우에도 안전 근거를 다시 확인한 뒤에만 자동으로 엽니다. 여러 서버가 자신이 쓰기를 받는다고 보고하는 경우에는 운영자가 판단합니다.

질문 시 참고:
쓰기 격리는 닫는 것만으로 끝나지 않습니다. master가 불확실하거나 삭제된 멤버를 아직 확인하지 못하면, 쓰기용 Broker를 0개로 줄입니다. 그리고 기존 연결과 새 연결 모두에서 저장 성공 응답이 없는지 확인합니다.

다시 여는 조건도 정했습니다. 멤버 미확인으로 닫은 경우에는 같은 단일 master와 다른 멤버의 안전 근거를 10초 이상 간격으로 두 번 확인해야 자동으로 엽니다. master가 여러 개인 경우 등은 사람이 판단하고, 이번 격리에만 쓸 수 있는 일회용 토큰으로 해제합니다.

상세 조건 — ADR-0005 Release: 두 차례 모두 격리에 기록된 같은 master를 확인하고, 다른 승격 가능 멤버는 인증·식별이 일치하는 최신 non-master 응답 또는 승인·감사된 외부 VM 전원 차단 확인과 out-of-service taint가 필요합니다. 멤버 식별이나 근거가 바뀌면 재확인하거나 자동 해제를 금지합니다. 외부 차단 근거에 따른 해제는 PrimaryResolved=True를 뜻하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
-->

---

<OperatorSlide class="op-session" section="03 · 개발 현황과 아키텍처 · 재구축" source="볼륨 교체 재구축 #118" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118">

<h1 class="op-title">디스크를 잃은 서버는 백업으로 복구합니다</h1>
<div class="session-debug session-two">
  <div><span>서버만 중단</span><h3>서버를 다시 띄웁니다</h3><p>디스크가 남은 서버의 자동 복귀를<br>강제 삭제 시험에서 확인했습니다.</p></div>
  <div><span>데이터 디스크도 손실</span><h3>백업으로 데이터를 복구합니다</h3><p>운영자가 대상을 확인하고 요청하면<br>현재 쓰기를 받는 서버의 백업을 복원합니다.</p></div>
</div>
<p class="session-takeaway">재구축 후에는 저장 성공 응답을 받았던 데이터가 남아 있는지 대조합니다.</p>

</OperatorSlide>

<!--
[30초 · 02 · 설계 · 재구축]
프로그램이 다시 뜨는 것과 데이터를 되살리는 것은 다릅니다. 이번 시험에서는 Pod가 삭제된 멤버가 자동으로 돌아왔습니다. 반면 데이터 볼륨까지 잃은 경우에는 사람이 대상을 확인하고 복구를 요청해야 합니다.

요청하면 현재 master의 백업으로 데이터를 채우고, 복제하는 서버로 합류시킵니다. 시험에서는 복구 뒤 실제 데이터도 대조했습니다. 컨테이너로 구성한 Kubernetes 시험 환경인 Kind에서 복구는 40.2초, 데이터 확인까지는 48.9초였습니다. v0.1 기준은 5분입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118
-->

---

<OperatorSlide class="op-session" section="04 · 검증 결과와 시행착오 · 시험 방법" source="시나리오 계약 · VM 랩 실행 기록 #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">장애 전 저장 기록과 복구 후 데이터를 대조했습니다</h1>
<div class="session-debug">
  <div><span>장애 전</span><h3>성공 응답을 기록합니다</h3><p>앱이 쓰기를 요청할 때마다<br>어떤 데이터가 저장됐다고 응답했는지 기록합니다.</p></div>
  <div><span>장애 발생</span><h3>실제로 서버를 멈춥니다</h3><p>전원을 끄거나, 네트워크를 끊거나,<br>쓰기를 받는 서버를 강제로 내립니다.</p></div>
  <div><span>복구 뒤</span><h3>기록과 DB를 대조합니다</h3><p>저장됐다고 응답한 데이터가 있는지,<br>차단 뒤 성공 응답이 있었는지 확인합니다.</p></div>
</div>
<p class="op-caption">컨테이너 자동 시험과 가상 서버 3대에서의 실제 장애 시험을 함께 사용했습니다.</p>

</OperatorSlide>

<!--
[25초 · 03 · 증거 · 시험 방법]
시험에서는 성공 응답을 받은 쓰기를 기록하고, 장애 뒤 각 서버에 그 데이터가 남아 있는지 대조합니다. 연결을 닫은 뒤에는 성공 응답이 없어야 합니다.

Kind에서는 코드 변경마다 자동 시험을 돌립니다. 실제 전원 차단과 네트워크 정책은 VM 세 대의 랩에서 따로 확인합니다. 랩은 공유 자원이라 사용 권한인 Lease를 확보하고 한 번에 하나씩 시험합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="04 · 검증 결과와 시행착오 · 장애 비교" source="VM 랩 비교 실행 2026-11-25 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">두 번째 장애 뒤 Lab Operator만 쓰기를 재개했습니다</h1>
<p class="op-caption">같은 환경에서 두 Operator가 각각 쓰기를 받는 서버를 두 번 강제로 내렸습니다.</p>
<div class="session-debug session-two">
  <div><span>CUBRID Lab Operator</span><h3>쓰기가 다시 됐습니다</h3><p>CUBRID가 새로 쓰기를 받을 서버를 선정했고,<br>DB 서버 3대가 자동으로 복귀했습니다.</p></div>
  <div><span>공식 CUBRID Operator</span><h3>시험을 끝낼 때까지 쓰지 못했습니다</h3><p>두 번째 장애 뒤 새로 쓰기를 받을 서버가 정해지지 않아<br>31분 뒤 시험을 종료할 때까지 쓰기가 재개되지 않았습니다.</p></div>
</div>
<p class="session-takeaway">첫 장애에서는 Lab Operator 쪽 쓰기 중단이 더 길었습니다. Lab 22.0초, 공식 12.4초.</p>

</OperatorSlide>

<!--
[40초 · 같은 장애 비교]
두 Operator를 같은 환경에서 시험했습니다. 두 번째 장애 뒤 Lab Operator에서는 CUBRID가 새로 쓰기를 받을 서버를 정했고 쓰기가 다시 됐습니다. 공식 Operator 쪽은 새 서버가 정해지지 않아 31분 뒤 시험 종료까지 쓰지 못했습니다. 첫 장애는 반대였습니다. Lab Operator의 쓰기 중단이 더 길었습니다. 이 결과는 같은 조건에서 강제 삭제를 두 번 해 본 관찰입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="04 · 검증 결과와 시행착오 · VM 시험 결과" source="VM 랩 실행 기록 #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">차단 뒤 쓰기 성공 0건, 새 클러스터 복원 3회 통과</h1>
<div class="session-debug">
  <div><span>쓰기 차단</span><h3>성공 응답 0건</h3><p>네트워크 장애 중 Operator를 다시 시작해도<br>차단 뒤 성공한 쓰기는 없었습니다.</p></div>
  <div><span>백업 복원</span><h3>3회 통과</h3><p>새 클러스터에 백업을 복원한 시험에서<br>성공을 확인했습니다.</p></div>
  <div><span>전원 차단</span><h3>26~38초</h3><p>전원 차단 표시부터 첫 쓰기 성공 응답까지<br>걸린 시간입니다. 세 차례 측정했습니다.</p></div>
</div>
<p class="op-caption">이 수치는 개별 시험 결과입니다. 공개할 버전으로 같은 조건에서 다시 확인해야 합니다.</p>

</OperatorSlide>

<!--
[25초 · 본문 설명]
VM 랩에서는 네트워크가 끊긴 동안 Operator를 재시작해도 쓰기 차단이 유지되는지 확인했습니다. 볼륨을 교체한 뒤의 복구와 새 클러스터로의 복원도 통과했습니다.

전원 차단은 세 번 측정했고, 차단 표시부터 첫 쓰기까지 26초에서 38초였습니다. 다시 장애를 냈을 때는 이전 격리의 해제 토큰 두 개가 모두 거부됐습니다. 시간은 측정값으로 공개하고, 닫힌 뒤 저장 성공 응답이 없는지는 통과와 실패로 판정합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="04 · 검증 결과와 시행착오 · 현재 문제" source="#1158 · 수정 PR #1159" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158">

<h1 class="op-title">지금 겪는 문제: 데이터 누락, 긴 중단, 복원 판정</h1>

<table class="op-comparison">
<thead><tr><th scope="col">시험에서 겪은 일</th><th scope="col">v0.1에서 확인할 것</th></tr></thead>
<tbody>
<tr><td><b>차단 전 데이터 누락</b><br>복제를 멈춘 전원 차단 시험에서 13건, 네트워크 장애 시험에서 최대 73건이 새 서버에 없었음</td><td>차단 전 데이터 누락을 조건과 함께 기록합니다. 차단이 확인된 뒤에는 성공한 쓰기가 없어야 합니다.</td></tr>
<tr><td><b>쓰기 재개 지연</b><br>강제 삭제 시험 두 차례에서 중지한 Broker를 다시 띄우는 데 약 12~17초</td><td>최종 후보에서 쓰기를 다시 받을 때까지 걸린 시간을 측정하고, 연결을 다시 여는 조건도 확인합니다.</td></tr>
<tr><td><b>복원 판정 보류</b><br>1차에는 세션이 끊겨 복원 2건을 판정하지 못함</td><td>복원 뒤 SQL 조회로 데이터를 대조합니다. 다른 운영자도 문서만 보고 같은 결과를 확인해야 합니다.</td></tr>
</tbody>
</table>
<p class="op-caption">데이터 누락과 중단 수치는 각 시험 조건에서 관찰한 결과입니다. 상세 조건은 22쪽에 있습니다.</p>

</OperatorSlide>

<!--
[45초 · 현재 시행착오]
시험에서 세 가지가 남았습니다. 먼저 이미 성공했다고 응답한 데이터가 새 서버에 없던 경우가 있었습니다. 복제를 일부러 멈춘 전원 차단 시험에서는 13건이 이전 서버에만 남았고, 네트워크 장애 시험에서는 새 서버에 최대 73건이 없었습니다. 이런 차단 전 누락은 조건과 함께 공개합니다. 두 번째로, 쓰기를 다시 열기로 한 뒤에도 Broker가 뜨는 데 12초에서 17초가 걸렸습니다. 마지막으로, 복원은 작업 완료 표시만으로 판단하기 어려웠습니다. 공개 후보에서는 실제 데이터를 대조하고 다른 운영자가 복원에 성공하는지 확인합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/702
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/238
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/127
-->

---

<OperatorSlide class="op-session" section="04 · 검증 결과와 시행착오 · 이후로 미룬 기능" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">v0.1 이후로 미룬 기능과 이유</h1>

<table class="op-comparison">
<thead><tr><th scope="col">미룬 기능</th><th scope="col">v0.1에서 하는 일</th><th scope="col">미룬 이유</th></tr></thead>
<tbody>
<tr><td><b>기존 데이터로 자동 재합류</b><br>v0.2</td><td>운영자가 승인하면 백업으로 재구축</td><td>장애 서버에 남은 데이터가 최신 데이터를 덮어쓰지 않는지 더 검증해야 합니다.</td></tr>
<tr><td><b>기존 디스크 자동 연결</b><br>v0.2</td><td>자동으로 기존 디스크를 가져오지 않음</td><td>새 클러스터가 재사용해도 되는 디스크인지 안전하게 판별해야 합니다.</td></tr>
<tr><td><b>쓰기 연결을 더 빨리 재개</b><br>후속 검토 · 일정 미정</td><td>Broker를 중지하고, 재개까지 걸린 시간을 측정·공개</td><td>더 빠르게 열더라도 기존 연결까지 확실히 끊겼는지 먼저 입증해야 합니다.</td></tr>
</tbody>
</table>
<p class="op-caption">외부 스토리지(CSI)는 이번 검증 환경에 포함하지 않았습니다.</p>

</OperatorSlide>

<!--
[30초 · v0.1 이후로 미룬 기능]
기존 데이터를 그대로 써서 자동으로 재합류시키는 기능과, 새 클러스터에 기존 디스크를 자동으로 연결하는 기능은 v0.2로 미뤘습니다. 기존 데이터의 상태와 소유권을 안전하게 판별해야 하기 때문입니다. 쓰기 연결을 더 빨리 여는 개선은 아직 일정을 정하지 않았습니다. 기존 연결까지 끊는 안전 조건을 유지할 수 있다는 증거가 먼저 필요합니다. v0.1에서는 현재 방식의 중단 시간을 측정해 공개합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/116
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/798
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161
-->

---

<OperatorSlide class="op-compact op-session" section="05 · 함께 논의할 질문">

<h1 class="op-title">쓰기 재개와 복원 완료 기준에 대한 질문</h1>

<ol class="op-questions"><li>복제는 정상처럼 보이는데 서버 한 대에만 연락이 안 된다면, 무엇을 확인한 뒤 쓰기를 다시 열겠습니까?</li><li>백업을 복원한 뒤, 운영자가 성공을 판단하려면 어떤 결과를 최소한 확인할 수 있어야 할까요?</li></ol>

</OperatorSlide>

<!--
[25초 · 05 · 함께 논의할 질문]
검증단과 다른 빌더 분들께 두 가지를 묻고 싶습니다. 상태를 확인할 수 없는 서버가 있어도 쓰기를 재개할 수 있다고 판단하는 근거는 무엇일까요? 그리고 백업의 체크섬이 맞고 작업이 끝났다고 표시됐을 때, 운영자가 복원 성공을 판단하려면 어떤 데이터 검증까지 있어야 할까요?
-->

---

<OperatorSlide class="op-session" section="06 · 최종 발표까지의 계획 · 공개 범위" source="ROADMAP · 시나리오 계약" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">필수 안전 시험을 모두 통과해야 v0.1을 공개합니다</h1>
<div class="session-debug session-two">
  <div><span>반드시 통과</span><h3>차단 뒤 쓰기 성공이 없어야 합니다</h3><p>설치·복제, 장애 대응, 재구축, 백업·복원을 시험합니다. 안전 조건을 위반하거나 근거가 빠지면 공개를 보류합니다.</p></div>
  <div><span>측정해 공개</span><h3>복구 시간과 차단 전 누락을 공개합니다</h3><p>전원 차단·네트워크 장애에서 재개 시간과 차단 전 승인된 쓰기 중 새 서버에 없는 범위를 기록합니다.</p></div>
</div>
<p class="session-takeaway">기존 실패 기록은 남깁니다. 공개 전에는 같은 후보 버전에서 필수 시험을 다시 실행합니다.</p>

</OperatorSlide>

<!--
[30초 · v0.1 공개 조건]
v0.1 공개 전에 설치와 복제, 장애 대응, 재구축과 백업 복원을 검증합니다. 쓰기를 막은 뒤에도 성공 응답이 나오거나 증거가 빠지면 공개를 보류합니다. 얼마나 빨리 다시 쓸 수 있었는지와 차단 전 승인된 데이터가 얼마나 남지 않았는지는 시험 조건과 함께 공개합니다. 과거에 실패했던 시험도 기록에 남깁니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-session" section="06 · 최종 발표까지의 계획 · 일정" source="ROADMAP v0.1 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">12월에 공개 후보를 확정하고 장애 시험을 반복합니다</h1>
<div class="session-debug">
  <div><span>12월 7일</span><h3>공개 후보 확정</h3><p>소스, 이미지, DB 버전과 시험 환경을 고정</p></div>
  <div><span>12월 8~14일</span><h3>실제 장애 반복 시험</h3><p>필수 장애를 다시 내고 24시간 부하 시험</p></div>
  <div><span>12월 15~20일</span><h3>다른 운영자가 재현</h3><p>문서만 보고 설치·장애 복구·백업 복원</p></div>
</div>
<p class="session-takeaway">12월 21~27일 공개 여부를 결정합니다. 필수 증거가 없으면 보류합니다.</p>

</OperatorSlide>

<!--
[25초 · 04 · v0.1 · 일정]
남은 일정입니다. 11월 말부터 판정 도구와 이미지 식별, 랩 통제를 정리하고, 12월 7일에 소스와 이미지, 엔진 버전, 랩을 하나로 고정합니다. 그 후보로 필수 시나리오를 반복하고 24시간 부하 시험을 합니다.

12월 15일부터는 코드를 쓰지 않은 사람이 문서만 보고 설치, 장애 복구, 복원을 재현합니다. 마지막 주에 증거를 보고 공개 여부를 정합니다. 필수 증거가 빠지면 날짜가 와도 공개하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-session" section="06 · 최종 발표까지의 계획 · 마무리">

<div class="op-clean-statement"><h1>쓰기 차단은 확인했고,<br>차단 전 데이터 누락도 발견했습니다</h1></div>
<p class="op-lead">공개 후보에서 같은 결과를 다시 검증하겠습니다.</p>

</OperatorSlide>

<!--
[20초 · 마무리]
이번 시험에서는 불확실한 때 쓰기 연결을 끊을 수 있었습니다. 차단 전에 이미 저장 성공으로 응답했지만 새 서버에 없던 데이터도 확인했습니다. 공개 후보에서 안전 조건을 다시 검증하고, 남은 한계는 시험 조건과 함께 공개하겠습니다.
-->

---

<OperatorSlide class="op-session" section="Q&amp;A · 질의응답" source="Operator 저장소" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><p class="op-caption"><a href="#/20">구성 요소 역할</a> · <a href="#/21">비교 시험 상세</a> · <a href="#/22">한계와 미검증 범위</a> · <a href="#/23">추가 시험 결과</a></p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 프로젝트입니다. CUBRID는 해당 권리자의 상표입니다.</p></div>

</OperatorSlide>

<!--
[Q&A]
감사합니다. 질문 받겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 장애 시 구성 요소의 역할" source="전체 아키텍처 · 쓰기 격리 ADR-0005 · 재구축 ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">장애 시 Operator·Instance Manager·CUBRID의 역할</h1>
<table class="op-comparison">
<thead><tr><th scope="col">구성 요소</th><th scope="col">장애 때 맡는 일</th></tr></thead>
<tbody>
<tr><td>Operator</td><td>서버들의 상태를 비교합니다. 쓰기를 받을 서버가 불확실하면 쓰기용 Broker를 중지하고, 운영자가 요청한 재구축을 조정합니다.</td></tr>
<tr><td>Instance Manager</td><td>각 DB 서버에서 역할을 조회하고, 인증된 요청에 따라 백업·복원 같은 로컬 작업을 실행합니다.</td></tr>
<tr><td>CUBRID HA</td><td>master를 선출하고 데이터를 복제합니다.</td></tr>
<tr><td>Broker</td><td>앱에서 받은 SQL 요청을 CUBRID에 전달합니다.</td></tr>
<tr><td>Kubernetes 리소스</td><td>StatefulSet은 DB 서버를 배치하고, PVC는 데이터 디스크를 연결합니다. Service는 앱이 접속하는 주소를 제공합니다.</td></tr>
</tbody>
</table>

<p class="op-caption text-right"><a href="#/3">전체 구조 보기</a> · <a href="#/19">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
운영자는 쓰기 차단이나 복구가 어디까지 진행됐는지 Operator에서 확인합니다. 각 DB 서버에서 실제 작업을 하는 쪽은 Instance Manager입니다. CUBRID HA는 master를 선출하고 Broker는 애플리케이션 요청을 DB로 전달합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 비교 시험 상세" source="VM 랩 비교 실행 2026-11-25 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">두 Operator의 쓰기 중단 시간 비교</h1>
<svg class="session-chart" style="max-height:240px" viewBox="0 0 860 300" role="img" aria-label="두 번째 master Pod 삭제 뒤 초당 승인된 쓰기 수. 공식 operator는 삭제 직후 0으로 떨어져 측정 끝까지 회복하지 않았고, 이 Operator는 삭제 후 약 43초에 다시 올라왔습니다."><line x1="56" x2="670" y1="260.0" y2="260.0" stroke="var(--line)" stroke-width="1"/><text x="48" y="264.0" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">0</text><line x1="56" x2="670" y1="178.7" y2="178.7" stroke="var(--line)" stroke-width="1"/><text x="48" y="182.7" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">5</text><line x1="56" x2="670" y1="97.3" y2="97.3" stroke="var(--line)" stroke-width="1"/><text x="48" y="101.3" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">10</text><line x1="56" x2="670" y1="16.0" y2="16.0" stroke="var(--line)" stroke-width="1"/><text x="48" y="20.0" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">15</text><text x="56.0" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">-30초</text><text x="117.4" y="280" text-anchor="middle" fill="var(--ink)" style="font-size:12px;font-weight:400">0</text><text x="240.2" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+60초</text><text x="363.0" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+120초</text><text x="485.8" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+180초</text><text x="608.6" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+240초</text><line x1="117.4" x2="117.4" y1="16" y2="260" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 4"/><text x="123.4" y="28" fill="var(--ink)" style="font-size:12px;font-weight:400">master Pod 강제 삭제</text><polyline points="58.0,162.4 62.1,146.1 66.2,178.7 70.3,162.4 74.4,162.4 78.5,154.3 82.6,186.8 86.7,243.7 90.8,235.6 94.9,154.3 99.0,146.1 103.1,146.1 107.2,194.9 111.3,219.3 115.4,219.3 119.4,178.7 123.5,260.0 127.6,260.0 131.7,260.0 135.8,260.0 139.9,260.0 144.0,260.0 148.1,260.0 152.2,260.0 156.3,260.0 160.4,260.0 164.5,260.0 168.6,260.0 172.7,260.0 176.8,260.0 180.8,260.0 184.9,260.0 189.0,260.0 193.1,260.0 197.2,260.0 201.3,260.0 205.4,260.0 209.5,260.0 213.6,260.0 217.7,260.0 221.8,260.0 225.9,260.0 230.0,260.0 234.1,260.0 238.2,260.0 242.2,260.0 246.3,260.0 250.4,260.0 254.5,260.0 258.6,260.0 262.7,260.0 266.8,260.0 270.9,260.0 275.0,260.0 279.1,260.0 283.2,260.0 287.3,260.0 291.4,260.0 295.5,260.0 299.6,260.0 303.6,260.0 307.7,260.0 311.8,260.0 315.9,260.0 320.0,260.0 324.1,260.0 328.2,260.0 332.3,260.0 336.4,260.0 340.5,260.0 344.6,260.0 348.7,260.0 352.8,260.0 356.9,260.0 361.0,260.0 365.0,260.0 369.1,260.0 373.2,260.0 377.3,260.0 381.4,260.0 385.5,260.0 389.6,260.0 393.7,260.0 397.8,260.0 401.9,260.0 406.0,260.0 410.1,260.0 414.2,260.0 418.3,260.0 422.4,260.0 426.4,260.0 430.5,260.0 434.6,260.0 438.7,260.0 442.8,260.0 446.9,260.0 451.0,260.0 455.1,260.0 459.2,260.0 463.3,260.0 467.4,260.0 471.5,260.0 475.6,260.0 479.7,260.0 483.8,260.0 487.8,260.0 491.9,260.0 496.0,260.0 500.1,260.0 504.2,260.0 508.3,260.0 512.4,260.0 516.5,260.0 520.6,260.0 524.7,260.0 528.8,260.0 532.9,260.0 537.0,260.0 541.1,260.0 545.2,260.0 549.2,260.0 553.3,260.0 557.4,260.0 561.5,260.0 565.6,260.0 569.7,260.0 573.8,260.0 577.9,260.0 582.0,260.0 586.1,260.0 590.2,260.0 594.3,260.0 598.4,260.0 602.5,260.0 606.6,260.0 610.6,260.0 614.7,260.0 618.8,260.0 622.9,260.0 627.0,260.0 631.1,260.0 635.2,260.0 639.3,260.0 643.4,260.0 647.5,260.0 651.6,260.0 655.7,260.0 659.8,260.0 663.9,260.0 668.0,260.0" fill="none" stroke="var(--blue)" stroke-width="2" stroke-linejoin="round"/><polyline points="58.0,154.3 62.1,162.4 66.2,146.1 70.3,129.9 74.4,162.4 78.5,154.3 82.6,154.3 86.7,154.3 90.8,154.3 94.9,146.1 99.0,162.4 103.1,138.0 107.2,146.1 111.3,138.0 115.4,154.3 119.4,235.6 123.5,138.0 127.6,97.3 131.7,113.6 135.8,138.0 139.9,260.0 144.0,260.0 148.1,260.0 152.2,260.0 156.3,260.0 160.4,260.0 164.5,260.0 168.6,260.0 172.7,260.0 176.8,260.0 180.8,260.0 184.9,260.0 189.0,260.0 193.1,260.0 197.2,260.0 201.3,260.0 205.4,154.3 209.5,129.9 213.6,146.1 217.7,154.3 221.8,138.0 225.9,146.1 230.0,162.4 234.1,146.1 238.2,138.0 242.2,146.1 246.3,138.0 250.4,146.1 254.5,154.3 258.6,138.0 262.7,154.3 266.8,154.3 270.9,154.3 275.0,154.3 279.1,146.1 283.2,154.3 287.3,162.4 291.4,146.1 295.5,146.1 299.6,154.3 303.6,146.1 307.7,154.3 311.8,146.1 315.9,154.3 320.0,154.3 324.1,146.1 328.2,154.3 332.3,154.3 336.4,146.1 340.5,162.4 344.6,146.1 348.7,162.4 352.8,154.3 356.9,154.3 361.0,146.1 365.0,170.5 369.1,154.3 373.2,154.3 377.3,162.4 381.4,154.3 385.5,154.3 389.6,146.1 393.7,154.3 397.8,162.4 401.9,154.3 406.0,162.4 410.1,170.5 414.2,146.1 418.3,154.3 422.4,154.3 426.4,154.3 430.5,146.1 434.6,154.3 438.7,162.4 442.8,162.4 446.9,138.0 451.0,170.5 455.1,170.5 459.2,154.3 463.3,162.4 467.4,146.1 471.5,138.0 475.6,154.3 479.7,146.1 483.8,146.1 487.8,162.4 491.9,138.0 496.0,170.5 500.1,162.4 504.2,170.5 508.3,162.4 512.4,146.1 516.5,162.4 520.6,162.4 524.7,146.1 528.8,154.3 532.9,154.3 537.0,162.4 541.1,170.5 545.2,138.0 549.2,154.3 553.3,154.3 557.4,162.4 561.5,170.5 565.6,170.5 569.7,146.1 573.8,154.3 577.9,162.4 582.0,154.3 586.1,162.4 590.2,138.0 594.3,154.3 598.4,170.5 602.5,162.4 606.6,170.5 610.6,154.3 614.7,154.3 618.8,162.4 622.9,146.1 627.0,162.4 631.1,162.4 635.2,138.0 639.3,146.1 643.4,162.4 647.5,154.3 651.6,146.1 655.7,146.1 659.8,146.1 663.9,154.3 668.0,154.3" fill="none" stroke="#9a3412" stroke-width="2" stroke-linejoin="round"/><circle cx="668.0" cy="154.3" r="4" fill="#9a3412" stroke="var(--paper)" stroke-width="2"/><text x="680" y="150.3" fill="var(--ink)" style="font-size:13px;font-weight:700">이 Operator</text><text x="680" y="167.3" fill="var(--muted)" style="font-size:12px;font-weight:400">최장 승인 공백 32.8초</text><text x="680" y="184.3" fill="var(--muted)" style="font-size:12px;font-weight:400">삭제 후 +42.5초 재개</text><circle cx="668.0" cy="260.0" r="4" fill="var(--blue)" stroke="var(--paper)" stroke-width="2"/><text x="680" y="242.0" fill="var(--ink)" style="font-size:13px;font-weight:700">cubrid-operator</text><text x="680" y="258.0" fill="var(--muted)" style="font-size:12px;font-weight:400">새 master 없음</text><text x="680" y="274.0" fill="var(--muted)" style="font-size:12px;font-weight:400">31분 뒤 정리까지 미복구</text><text x="56" y="296" fill="var(--muted)" style="font-size:11px;font-weight:400">초당 승인된 쓰기 (2초 평균) · 같은 클라이언트, 트랜잭션당 1행 · 측정 창은 삭제 뒤 약 282초</text><line x1="137.3" x2="137.3" y1="34" y2="260" stroke="var(--muted)" stroke-width="1" stroke-dasharray="2 3"/><text x="143.3" y="48" fill="var(--ink)" style="font-size:12px;font-weight:700">+9.7초 Operator 격리</text><text x="143.3" y="64" fill="var(--muted)" style="font-size:12px;font-weight:400">그 전 +2.5–9.6초: CUBRID가 올린 ha-0가 승인 (손실 0)</text></svg>
<p class="op-caption"><b>32.8초</b>는 쓰기 성공 응답 사이의 최장 공백입니다. <b>42.5초</b>는 Pod 삭제부터 격리 뒤 첫 성공 응답까지의 시간입니다.</p>
<p class="op-caption text-right"><a href="#/19">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 비교 시험 상세]
같은 VM 랩에서 쓰기 중 master Pod를 두 번씩 삭제했습니다. 그래프는 두 번째 시험입니다. 공식 Operator는 새 master가 뽑히지 않아, 31분 뒤 시험을 정리할 때까지 쓰지 못했습니다. 멤버마다 노드 우선순위 목록의 순서가 달라졌기 때문입니다. 저희는 모든 멤버가 같은 목록을 읽어 새 master가 선출됐고, 세 멤버가 자동 복귀했습니다.

주황 선은 삭제 직후 잠시 쓰기를 받다가 확인을 위해 닫힌 모습입니다. 쓰기 승인 사이의 최장 공백은 32.8초였고, 격리 뒤 첫 쓰기 승인은 삭제 후 42.5초에 기록됐습니다. 첫 시험의 중단은 저희가 22초로 공식의 12.4초보다 길었습니다. 두 시험 모두 쓰기 손실은 없었지만, 모든 장애에서 복구된다는 뜻은 아닙니다.

질문 시 참고: 초기 구성은 공식 Operator에서 DB 생성·HA 시작·Broker 시작을 멤버마다 수동 실행했고, Lab Operator는 수동 단계 없이 약 2분이었습니다. 두 번째 장애의 원인: 공식 Operator는 Pod 목록이 바뀔 때마다 ha_node_list를 조회 순서대로 다시 써서 ha-0:ha-1:ha-2, ha-1:ha-2:ha-0, ha-2:ha-0:ha-1로 바뀌었고, 손으로 다시 붙인 멤버만 새 순서를 읽었습니다. 이 Operator는 ha_node_list를 스펙만으로 순번대로 만들어 ConfigMap 하나로 모든 멤버에 주므로 Pod 교체나 master 이동에도 바뀌지 않습니다(ADR-0001·ADR-0004). 네트워크 분할은 이 비교에 포함하지 않았습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 한계와 시험 조건" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">데이터 누락·쓰기 중단 사례와 미검증 스토리지</h1><ol class="op-risks"><li><b>복제 지연 후 VM 전원 차단: 승인된 쓰기 13건이 새 master에 없음</b><span>2026-11-19 VM 시험 · 복제 프로세스를 정지한 조건 · 해당 행은 옛 master 디스크에만 남음</span></li><li><b>네트워크 분할에서 승격된 멤버에 승인된 쓰기 최대 73건 없음</b><span>11월 17–18일 VM 분할 5회에서 13–73건 미반영 · 1회는 73건이 없는 멤버가 active master로 전환</span></li><li><b>master Pod 정상 종료 때 쓰기 경로가 28초 닫힘 (Kind)</b><span>불필요한 격리 · 시간과 원인을 공개</span></li><li><b>스토리지는 node-local, CSI 아님</b><span>볼륨이 다른 노드로 따라가는 동작·스냅샷·크기 변경은 검증하지 않음</span></li></ol><p class="op-boundary"><b>원칙</b>　Operator의 제어 범위와 엔진 동작의 한계를 구분하고, 재현 조건과 영향을 공개합니다</p>

<p class="op-caption text-right"><a href="#/19">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
공개할 한계입니다. 복제 프로세스를 정지한 뒤 VM 전원을 차단한 시험에서 승인된 쓰기 13건이 새 master에 없었습니다. 해당 행은 옛 master 디스크에만 남았습니다. 원인에 대한 가설과 관측 결과는 구분합니다. 네트워크 분할에서는 경로를 닫기 전에 승인된 쓰기가 승격된 멤버에 최대 73건 없었습니다. master Pod를 정상 종료할 때 쓰기 경로가 28초 닫히는 문제도 있습니다.

그리고 저희 랩은 node-local 스토리지라 CSI 동작은 검증하지 않았습니다. 이 숫자는 각각의 시험 조건에서 관찰한 결과입니다. 앞서 소개한 격리 유지 시험과 구분해야 합니다. 승격된 멤버의 미반영과 전체 멤버에서의 최종 손실도 같은 뜻으로 쓰지 않습니다. 제어 가능한 범위와 엔진 동작의 한계를 구분해 공개하겠습니다.

관측 근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035 및 https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md (section 8의 2026-11-17–18 VM 기록).

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 추가 시험 결과">

<h1 class="op-title">디스크 교체 복구와 이전 해제 토큰 거부 시험</h1>
<table class="op-comparison">
<thead><tr><th scope="col">시험</th><th scope="col">확인한 결과</th></tr></thead>
<tbody>
<tr><td>데이터 디스크를 교체한 서버 재구축</td><td>복구 뒤 저장 성공으로 응답했던 데이터가 남았는지 대조했습니다.</td></tr>
<tr><td>격리를 해제한 뒤 다시 네트워크를 분할</td><td>이전 해제 토큰 두 개를 모두 거부했습니다. 쓰기 연결을 닫은 뒤 성공 응답이 없었습니다.</td></tr>
<tr><td>한동안 쓰지 않은 DB 연결이 끊김</td><td>네트워크 규칙에서 연결 확인 신호를 허용한 뒤 같은 조건에서 연결이 유지됐습니다.</td></tr>
</tbody>
</table>

<p class="op-caption text-right"><a href="#/19">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 추가 시험 결과]
재구축 후 데이터 대조와 반복 장애에서 과거 해제 토큰 재사용 거부를 관찰했습니다. 자세한 조건은 VM 랩 실행 기록에 있습니다.

연결 끊김을 해결한 사례:
VM 랩에서는 연결을 유지하지 못하는 결함도 찾았습니다. 같은 Pod 안에서는 괜찮았지만 다른 노드에서 연결하면 끊겼고, 네트워크 정책을 끄면 문제가 사라졌습니다.

원인은 서버가 상대의 생존을 확인하는 TCP 7번 패킷을 정책이 막는 것이었습니다. 필요한 경로만 허용한 뒤, 노드를 건넌 세션 40개와 Broker를 거친 연결 30개가 세 차례 대기 후에도 유지됐습니다. Kind에는 이 정책이 없어 놓쳤습니다. 실제 환경 시험을 함께 하는 이유입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->
