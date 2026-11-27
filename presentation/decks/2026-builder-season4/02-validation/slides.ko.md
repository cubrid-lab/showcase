---
title: "CUBRID Kubernetes Operator — 2차 검증"
---

<OperatorSlide class="op-session" section="Opening · 프로젝트 소개" source="프로젝트·팀" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">빌더 시즌4 · 2차 검증</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">불확실할 때 쓰기를 멈추고,<br>장애 뒤 복구를 확인합니다.</p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준 · 공동 메인테이너</span></div></div>

</OperatorSlide>

<!--
[30초 · Opening · 프로젝트 소개]
안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저장 성공 응답을 받았는데, 장애 뒤 그 데이터가 없다면 어떨까요? 저희는 Kubernetes에서 CUBRID 운영과 복구를 관리하는 Operator를 만들고 있습니다. 오늘은 쓰기 연결을 막고 복구를 확인한 결과, 그리고 아직 막지 못한 손실을 말씀드리겠습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

<OperatorSlide class="op-session" section="01 · 1차 이후 바뀐 것" source="1차 검증 발표 · 로드맵" source-url="https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation">

<h1 class="op-title">상태 표시에서 실제 차단과 복구로 나아갔습니다</h1><table class="session-table"><thead><tr><th></th><th>1차 (10월 말)</th><th>2차 (지금)</th></tr></thead><tbody><tr><td>쓰기 안전</td><td>불확실한 상태를 표시</td><td><b>쓰기 연결 차단</b> 구현</td></tr><tr><td>데이터 복구</td><td>계획</td><td><b>요청에 따른 복구</b> 구현</td></tr><tr><td>검증</td><td>자동 시험 27개</td><td><b>61개</b> + VM 랩 실제 장애 시험</td></tr></tbody></table><p class="session-takeaway">연결을 닫았는지, 복구 뒤 데이터가 남았는지 확인합니다</p>

</OperatorSlide>

<!--
[25초 · 01 · 1차 이후 바뀐 것]
1차에서는 서버 상태가 불확실하다는 표시까지만 했습니다. 이번에는 쓰기 연결을 실제로 차단하고, 데이터를 잃은 서버를 요청에 따라 복구하도록 구현했습니다. 구현한 기능은 자동 시험과 실제 장애 시험으로 확인했습니다. 먼저 왜 쓰기를 막아야 하는지부터 설명하겠습니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-session" section="01 · 왜 쓰기를 막는가" source="1차 검증 발표 · ADR-0005 쓰기 격리" source-url="https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation">

<h1 class="op-title">불확실하면, 확인될 때까지 쓰기를 막습니다</h1><p class="session-sub">master = 현재 쓰기를 받는 DB 서버 · 다른 서버가 데이터를 복제</p><div class="session-debug session-two"><div><span>위험</span><h3>성공 응답 뒤에도<br>데이터가 없을 수 있습니다</h3><p>복제가 끝나기 전에 장애가 나면<br>새 master에 데이터가 없을 수 있음</p></div><div class="focus"><span>대응 · 쓰기 격리</span><h3>확신할 수 없으면<br>쓰기 연결을 끊습니다</h3><p>연결 실패를 알리고<br>안전 근거를 확인한 뒤 다시 열기</p></div></div><p class="session-takeaway">읽기 전용 Broker와 서비스는 유지 · 차단 전에 성공한 쓰기까지 보호하지는 못함</p>

</OperatorSlide>

<!--
[40초 · 01 · 1차와 2차]
현재 쓰기를 받는 DB 서버를 master라고 부릅니다. 나머지 서버는 그 데이터를 복제합니다. 저장 성공 응답을 받았더라도 복제가 끝나기 전에 장애가 나면, 새 master에는 그 데이터가 없을 수 있습니다.

그래서 누가 쓰기를 받아도 되는지 불확실하면 쓰기 연결을 끊습니다. 이것이 쓰기 격리입니다. 읽기 전용 Broker와 -ro Service는 쓰기 격리의 영향을 받지 않습니다. 다만 차단 전에 이미 성공한 쓰기까지 보호하는 것은 아닙니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
-->

---

<OperatorSlide class="op-session" section="02 · 설계">

<ChapterDivider number="02" title="설계" subtitle="불확실하면 추정하지 않고, 쓰기를 받지 않습니다" />

</OperatorSlide>

<!--
[0초 · 02 · 설계]
다음 주제를 알리는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-session" section="02 · 설계 · 전체 구조" source="전체 아키텍처 · 쓰기 격리 ADR-0005 · 재구축 ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">Operator가 상태를 확인하고 연결을 관리합니다</h1><OperatorSessionArchitecture /><p class="session-takeaway"><b>Broker</b>는 DB 연결 창구 · <b>Instance Manager</b>는 각 DB 서버의 상태를 알려주는 구성 요소</p>

</OperatorSlide>

<!--
[35초 · 02 · 설계 · 전체 구조]
그림 아래가 데이터가 오가는 경로입니다. 애플리케이션은 DB 연결 창구인 Broker를 거쳐 CUBRID에 데이터를 저장합니다. 위쪽의 관리 프로그램 Operator는 각 DB 서버의 Instance Manager에 상태를 묻고, 불확실하면 쓰기용 Broker를 중지합니다.

master 선출과 복제는 CUBRID가 맡고, Operator는 연결 관리와 복구 조정만 합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
-->

---

<OperatorSlide class="op-session" section="02 · 설계 · 쓰기 격리" source="ADR-0005 쓰기 격리" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md">

<h1 class="op-title">연결을 끊고, 확인한 뒤 다시 엽니다</h1><div class="session-flow"><div><span>01 · 관찰</span><h3>서버 상태 불확실</h3><p>응답 없음 · 역할 충돌<br>지운 멤버 확인 전</p></div><i>→</i><div class="focus"><span>02 · 차단</span><h3>쓰기 연결 차단</h3><p>Broker 0개로<br>기존 연결도 종료</p></div><i>→</i><div><span>03 · 검증</span><h3>성공 응답 0건</h3><p>기존 연결<br>새 연결</p></div><i>→</i><div><span>04 · 해제</span><h3>근거 확인</h3><p>자동: 두 번 재확인<br>수동: 이번 격리 전용 토큰</p></div></div><p class="session-takeaway">자동 해제는 멤버 미확인 격리에 한정 · 같은 단일 master와 안전 근거를 10초 이상 간격으로 두 번 확인</p>

</OperatorSlide>

<!--
[40초 · 02 · 설계 · 쓰기 격리]
쓰기 격리는 닫는 것만으로 끝나지 않습니다. master가 불확실하거나 삭제된 멤버를 아직 확인하지 못하면, 쓰기용 Broker를 0개로 줄입니다. 그리고 기존 연결과 새 연결 모두에서 저장 성공 응답이 없는지 확인합니다.

다시 여는 조건도 정했습니다. 멤버 미확인으로 닫은 경우에는 같은 단일 master와 다른 멤버의 안전 근거를 10초 이상 간격으로 두 번 확인해야 자동으로 엽니다. master가 여러 개인 경우 등은 사람이 판단하고, 이번 격리에만 쓸 수 있는 일회용 토큰으로 해제합니다.

상세 조건 — ADR-0005 Release: 두 차례 모두 격리에 기록된 같은 master를 확인하고, 다른 승격 가능 멤버는 인증·식별이 일치하는 최신 non-master 응답 또는 승인·감사된 외부 VM 전원 차단 확인과 out-of-service taint가 필요합니다. 멤버 식별이나 근거가 바뀌면 재확인하거나 자동 해제를 금지합니다. 외부 차단 근거에 따른 해제는 PrimaryResolved=True를 뜻하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
-->

---

<OperatorSlide class="op-session" section="02 · 설계 · 재구축" source="볼륨 교체 재구축 #118" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118">

<h1 class="op-title">데이터를 잃은 서버는 요청에 따라 복구합니다</h1><div class="session-flow"><div><span>01</span><h3>데이터 볼륨 손실</h3><p>쓰기 격리</p></div><i>→</i><div><span>02</span><h3>사람이 복구 요청</h3><p>사람이 대상 확인</p></div><i>→</i><div class="focus"><span>03</span><h3>백업 복원</h3><p>현재 master → 대상</p></div><i>→</i><div><span>04</span><h3>데이터 대조</h3><p>승인된 데이터 확인</p></div></div><div class="session-metrics"><div><strong>40.2초</strong><span>재구축 완료</span></div><div><strong>48.9초</strong><span>행 확인 완료</span></div><p>Kind 측정 · 요청 시점부터<br>v0.1 제한 5분</p></div>

</OperatorSlide>

<!--
[40초 · 02 · 설계 · 재구축]
프로그램이 다시 뜨는 것과 데이터를 되살리는 것은 다릅니다. 이번 시험에서는 Pod가 삭제된 멤버가 자동으로 돌아왔습니다. 반면 데이터 볼륨까지 잃은 경우에는 사람이 대상을 확인하고 복구를 요청해야 합니다.

요청하면 현재 master의 백업으로 데이터를 채우고, 복제하는 서버로 합류시킵니다. 시험에서는 복구 뒤 실제 데이터도 대조했습니다. 컨테이너로 구성한 Kubernetes 시험 환경인 Kind에서 복구는 40.2초, 데이터 확인까지는 48.9초였습니다. v0.1 기준은 5분입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118
-->

---

<OperatorSlide class="op-session" section="03 · 증거 · 시험 방법" source="시나리오 계약 · VM 랩 실행 기록 #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">성공 응답을 받은 데이터가 남았는지 확인합니다</h1><div class="op-clean-three"><div><span>왜</span><h3>응답이 맞았는지</h3><p>상태 표시가 아니라<br>애플리케이션이 받은 “성공”이<br>장애 뒤에도 남는지가 기준</p></div><div><span>어떻게</span><h3>Kind + VM 랩</h3><p>Kind(컨테이너로 띄운 테스트용 K8s)<br>main마다 실제 CUBRID 이미지<br>VM 3대: 전원 차단 · 네트워크 분할<br>Pod 삭제 · Operator 재시작</p></div><div><span>무엇을 확인</span><h3>행 단위 대조</h3><p>클라이언트가 승인된 쓰기를 기록<br>장애 뒤 멤버마다 남았는지 대조<br>닫힌 뒤 승인 0건 · 시간 측정</p></div></div><p class="session-takeaway">실제 전원 차단과 네트워크 정책 적용은 VM 랩에서 별도 시험 · 공유 랩은 점유 Lease로 한 번에 하나</p>

</OperatorSlide>

<!--
[30초 · 03 · 증거 · 시험 방법]
시험에서는 성공 응답을 받은 쓰기를 기록하고, 장애 뒤 각 서버에 그 데이터가 남아 있는지 대조합니다. 연결을 닫은 뒤에는 성공 응답이 없어야 합니다.

Kind에서는 코드 변경마다 자동 시험을 돌립니다. 실제 전원 차단과 네트워크 정책은 VM 세 대의 랩에서 따로 확인합니다. 랩은 공유 자원이라 사용 권한인 Lease를 확보하고 한 번에 하나씩 시험합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="03 · 증거 · 같은 장애 비교" source="VM 랩 비교 실행 2026-11-25 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">두 번째 장애에서 결과가 달라졌습니다</h1><p class="session-sub">11월 25일 VM 랩 · HA 3멤버 · operator별 master Pod 강제 삭제 2회 중 두 번째</p><svg class="session-chart" style="max-height:215px" viewBox="0 0 860 300" role="img" aria-label="두 번째 master Pod 삭제 뒤 초당 승인된 쓰기 수. 공식 operator는 삭제 직후 0으로 떨어져 측정 끝까지 회복하지 않았고, 이 Operator는 삭제 후 약 43초에 다시 올라왔습니다."><line x1="56" x2="670" y1="260.0" y2="260.0" stroke="var(--line)" stroke-width="1"/><text x="48" y="264.0" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">0</text><line x1="56" x2="670" y1="178.7" y2="178.7" stroke="var(--line)" stroke-width="1"/><text x="48" y="182.7" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">5</text><line x1="56" x2="670" y1="97.3" y2="97.3" stroke="var(--line)" stroke-width="1"/><text x="48" y="101.3" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">10</text><line x1="56" x2="670" y1="16.0" y2="16.0" stroke="var(--line)" stroke-width="1"/><text x="48" y="20.0" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">15</text><text x="56.0" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">-30초</text><text x="117.4" y="280" text-anchor="middle" fill="var(--ink)" style="font-size:12px;font-weight:400">0</text><text x="240.2" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+60초</text><text x="363.0" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+120초</text><text x="485.8" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+180초</text><text x="608.6" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+240초</text><line x1="117.4" x2="117.4" y1="16" y2="260" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 4"/><text x="123.4" y="28" fill="var(--ink)" style="font-size:12px;font-weight:400">master Pod 강제 삭제</text><polyline points="58.0,162.4 62.1,146.1 66.2,178.7 70.3,162.4 74.4,162.4 78.5,154.3 82.6,186.8 86.7,243.7 90.8,235.6 94.9,154.3 99.0,146.1 103.1,146.1 107.2,194.9 111.3,219.3 115.4,219.3 119.4,178.7 123.5,260.0 127.6,260.0 131.7,260.0 135.8,260.0 139.9,260.0 144.0,260.0 148.1,260.0 152.2,260.0 156.3,260.0 160.4,260.0 164.5,260.0 168.6,260.0 172.7,260.0 176.8,260.0 180.8,260.0 184.9,260.0 189.0,260.0 193.1,260.0 197.2,260.0 201.3,260.0 205.4,260.0 209.5,260.0 213.6,260.0 217.7,260.0 221.8,260.0 225.9,260.0 230.0,260.0 234.1,260.0 238.2,260.0 242.2,260.0 246.3,260.0 250.4,260.0 254.5,260.0 258.6,260.0 262.7,260.0 266.8,260.0 270.9,260.0 275.0,260.0 279.1,260.0 283.2,260.0 287.3,260.0 291.4,260.0 295.5,260.0 299.6,260.0 303.6,260.0 307.7,260.0 311.8,260.0 315.9,260.0 320.0,260.0 324.1,260.0 328.2,260.0 332.3,260.0 336.4,260.0 340.5,260.0 344.6,260.0 348.7,260.0 352.8,260.0 356.9,260.0 361.0,260.0 365.0,260.0 369.1,260.0 373.2,260.0 377.3,260.0 381.4,260.0 385.5,260.0 389.6,260.0 393.7,260.0 397.8,260.0 401.9,260.0 406.0,260.0 410.1,260.0 414.2,260.0 418.3,260.0 422.4,260.0 426.4,260.0 430.5,260.0 434.6,260.0 438.7,260.0 442.8,260.0 446.9,260.0 451.0,260.0 455.1,260.0 459.2,260.0 463.3,260.0 467.4,260.0 471.5,260.0 475.6,260.0 479.7,260.0 483.8,260.0 487.8,260.0 491.9,260.0 496.0,260.0 500.1,260.0 504.2,260.0 508.3,260.0 512.4,260.0 516.5,260.0 520.6,260.0 524.7,260.0 528.8,260.0 532.9,260.0 537.0,260.0 541.1,260.0 545.2,260.0 549.2,260.0 553.3,260.0 557.4,260.0 561.5,260.0 565.6,260.0 569.7,260.0 573.8,260.0 577.9,260.0 582.0,260.0 586.1,260.0 590.2,260.0 594.3,260.0 598.4,260.0 602.5,260.0 606.6,260.0 610.6,260.0 614.7,260.0 618.8,260.0 622.9,260.0 627.0,260.0 631.1,260.0 635.2,260.0 639.3,260.0 643.4,260.0 647.5,260.0 651.6,260.0 655.7,260.0 659.8,260.0 663.9,260.0 668.0,260.0" fill="none" stroke="var(--blue)" stroke-width="2" stroke-linejoin="round"/><polyline points="58.0,154.3 62.1,162.4 66.2,146.1 70.3,129.9 74.4,162.4 78.5,154.3 82.6,154.3 86.7,154.3 90.8,154.3 94.9,146.1 99.0,162.4 103.1,138.0 107.2,146.1 111.3,138.0 115.4,154.3 119.4,235.6 123.5,138.0 127.6,97.3 131.7,113.6 135.8,138.0 139.9,260.0 144.0,260.0 148.1,260.0 152.2,260.0 156.3,260.0 160.4,260.0 164.5,260.0 168.6,260.0 172.7,260.0 176.8,260.0 180.8,260.0 184.9,260.0 189.0,260.0 193.1,260.0 197.2,260.0 201.3,260.0 205.4,154.3 209.5,129.9 213.6,146.1 217.7,154.3 221.8,138.0 225.9,146.1 230.0,162.4 234.1,146.1 238.2,138.0 242.2,146.1 246.3,138.0 250.4,146.1 254.5,154.3 258.6,138.0 262.7,154.3 266.8,154.3 270.9,154.3 275.0,154.3 279.1,146.1 283.2,154.3 287.3,162.4 291.4,146.1 295.5,146.1 299.6,154.3 303.6,146.1 307.7,154.3 311.8,146.1 315.9,154.3 320.0,154.3 324.1,146.1 328.2,154.3 332.3,154.3 336.4,146.1 340.5,162.4 344.6,146.1 348.7,162.4 352.8,154.3 356.9,154.3 361.0,146.1 365.0,170.5 369.1,154.3 373.2,154.3 377.3,162.4 381.4,154.3 385.5,154.3 389.6,146.1 393.7,154.3 397.8,162.4 401.9,154.3 406.0,162.4 410.1,170.5 414.2,146.1 418.3,154.3 422.4,154.3 426.4,154.3 430.5,146.1 434.6,154.3 438.7,162.4 442.8,162.4 446.9,138.0 451.0,170.5 455.1,170.5 459.2,154.3 463.3,162.4 467.4,146.1 471.5,138.0 475.6,154.3 479.7,146.1 483.8,146.1 487.8,162.4 491.9,138.0 496.0,170.5 500.1,162.4 504.2,170.5 508.3,162.4 512.4,146.1 516.5,162.4 520.6,162.4 524.7,146.1 528.8,154.3 532.9,154.3 537.0,162.4 541.1,170.5 545.2,138.0 549.2,154.3 553.3,154.3 557.4,162.4 561.5,170.5 565.6,170.5 569.7,146.1 573.8,154.3 577.9,162.4 582.0,154.3 586.1,162.4 590.2,138.0 594.3,154.3 598.4,170.5 602.5,162.4 606.6,170.5 610.6,154.3 614.7,154.3 618.8,162.4 622.9,146.1 627.0,162.4 631.1,162.4 635.2,138.0 639.3,146.1 643.4,162.4 647.5,154.3 651.6,146.1 655.7,146.1 659.8,146.1 663.9,154.3 668.0,154.3" fill="none" stroke="#9a3412" stroke-width="2" stroke-linejoin="round"/><circle cx="668.0" cy="154.3" r="4" fill="#9a3412" stroke="var(--paper)" stroke-width="2"/><text x="680" y="150.3" fill="var(--ink)" style="font-size:13px;font-weight:700">이 Operator</text><text x="680" y="167.3" fill="var(--muted)" style="font-size:12px;font-weight:400">최장 승인 공백 32.8초</text><text x="680" y="184.3" fill="var(--muted)" style="font-size:12px;font-weight:400">삭제 후 +42.5초 재개</text><circle cx="668.0" cy="260.0" r="4" fill="var(--blue)" stroke="var(--paper)" stroke-width="2"/><text x="680" y="242.0" fill="var(--ink)" style="font-size:13px;font-weight:700">cubrid-operator</text><text x="680" y="258.0" fill="var(--muted)" style="font-size:12px;font-weight:400">새 master 없음</text><text x="680" y="274.0" fill="var(--muted)" style="font-size:12px;font-weight:400">31분 뒤 정리까지 미복구</text><text x="56" y="296" fill="var(--muted)" style="font-size:11px;font-weight:400">초당 승인된 쓰기 (2초 평균) · 같은 클라이언트, 트랜잭션당 1행 · 측정 창은 삭제 뒤 약 282초</text><line x1="137.3" x2="137.3" y1="34" y2="260" stroke="var(--muted)" stroke-width="1" stroke-dasharray="2 3"/><text x="143.3" y="48" fill="var(--ink)" style="font-size:12px;font-weight:700">+9.7초 Operator 격리</text><text x="143.3" y="64" fill="var(--muted)" style="font-size:12px;font-weight:400">그 전 +2.5–9.6초: CUBRID가 올린 ha-0가 승인 (손실 0)</text></svg><table class="op-comparison session-why"><tbody><tr><td><b>왜 갈렸나</b></td><td><b>cubrid-operator</b><br>Pod 목록이 바뀔 때마다 멤버별 <code>ha_node_list</code> 순서를 다시 씀 → 남은 두 멤버의 우선순위가 달라 둘 다 standby</td><td><b>이 Operator</b><br>스펙에서 순번대로 만든 한 목록을 모든 멤버가 공유 → Pod가 바뀌어도 순서 불변, CUBRID가 새 master 선출</td></tr></tbody></table><p class="session-takeaway">첫 삭제의 쓰기 중단: 우리 22.0초 · 공식 12.4초 / 두 시험 모두 쓰기 손실 0건</p>

</OperatorSlide>

<!--
[55초 · 본문 설명]
같은 VM 랩에서 쓰기 중 master Pod를 두 번씩 삭제했습니다. 그래프는 두 번째 시험입니다. 공식 Operator는 새 master가 뽑히지 않아, 31분 뒤 시험을 정리할 때까지 쓰지 못했습니다. 멤버마다 노드 우선순위 목록의 순서가 달라졌기 때문입니다. 저희는 모든 멤버가 같은 목록을 읽어 새 master가 선출됐고, 세 멤버가 자동 복귀했습니다.

주황 선은 삭제 직후 잠시 쓰기를 받다가 확인을 위해 닫힌 모습입니다. 쓰기 승인 사이의 최장 공백은 32.8초였고, 격리 뒤 첫 쓰기 승인은 삭제 후 42.5초에 기록됐습니다. 첫 시험의 중단은 저희가 22초로 공식의 12.4초보다 길었습니다. 두 시험 모두 쓰기 손실은 없었지만, 모든 장애에서 복구된다는 뜻은 아닙니다.

질문 시 참고: 초기 구성은 공식 Operator에서 DB 생성·HA 시작·Broker 시작을 멤버마다 수동 실행했고, Lab Operator는 수동 단계 없이 약 2분이었습니다. 두 번째 장애의 원인: 공식 Operator는 Pod 목록이 바뀔 때마다 ha_node_list를 조회 순서대로 다시 써서 ha-0:ha-1:ha-2, ha-1:ha-2:ha-0, ha-2:ha-0:ha-1로 바뀌었고, 손으로 다시 붙인 멤버만 새 순서를 읽었습니다. 이 Operator는 ha_node_list를 스펙만으로 순번대로 만들어 ConfigMap 하나로 모든 멤버에 주므로 Pod 교체나 master 이동에도 바뀌지 않습니다(ADR-0001·ADR-0004). 네트워크 분할은 이 비교에 포함하지 않았습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="03 · 증거 · VM 시험 현황" source="VM 랩 실행 기록 #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">VM 랩에서 확인한 동작과 측정값입니다</h1><table class="session-table session-status"><thead><tr><th>VM 랩 시험</th><th>확인한 동작</th><th>상태</th></tr></thead><tbody><tr><td>분할 중 Operator 재시작</td><td>격리 유지 · 쓰기 승인 없음</td><td><b>안전 규칙 통과</b></td></tr><tr><td>볼륨 교체 재구축</td><td>재구축 뒤 행 대조</td><td><b>통과</b></td></tr><tr><td>새 클러스터 복원</td><td>3회 복원 · 세션 끊김 없음</td><td><b>통과</b></td></tr><tr><td>VM 전원 손실</td><td>전원 차단 표시 뒤 첫 쓰기까지 26–38초 (3회) · 복제 정지 조건에서는 13건 유실 (13장)</td><td><b>측정 공개</b></td></tr><tr><td>해제 후 재분할</td><td>옛 토큰 2개 모두 거부 · 닫힌 뒤 쓰기 승인 없음</td><td><b>안전 규칙 통과</b></td></tr></tbody></table><p class="session-takeaway">각 행은 해당 실행의 결과 · 승인했지만 사라진 쓰기는 13장에 모음</p>

</OperatorSlide>

<!--
[35초 · 본문 설명]
VM 랩에서는 네트워크가 끊긴 동안 Operator를 재시작해도 쓰기 차단이 유지되는지 확인했습니다. 볼륨을 교체한 뒤의 복구와 새 클러스터로의 복원도 통과했습니다.

전원 차단은 세 번 측정했고, 차단 표시부터 첫 쓰기까지 26초에서 38초였습니다. 다시 장애를 냈을 때는 이전 격리의 해제 토큰 두 개가 모두 거부됐습니다. 시간은 측정값으로 공개하고, 닫힌 뒤 저장 성공 응답이 없는지는 통과와 실패로 판정합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="03 · 증거 · Kind" source="Kind E2E 실행 기록" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1109">

<h1 class="op-title">자동 시험 61개로 같은 위험을 반복 확인합니다</h1><div class="op-clean-hero"><strong>61 / 61</strong><p>자동 시험 통과 (Kind E2E)</p></div><p class="op-clean-caption">master 삭제 → 쓰기 차단 → 복귀 확인 → 데이터 대조<br>실제 노드·네트워크 정책은 VM 랩에서 별도 검증</p>

</OperatorSlide>

<!--
[20초 · 03 · 증거 · Kind]
자동 시험은 1차의 27개에서 61개로 늘었고, 확인한 빌드에서는 모두 통과했습니다. 하지만 시험 통과가 모든 장애에서 데이터 손실이 없다는 뜻은 아닙니다. 실제 환경에서 찾은 결함과 남은 한계를 이어서 보여 드리겠습니다.

질문 시 참고: 전체 실행 약 63분 (main 3806d1db, 11월 25일). 11월 10–20일 실패 실행 58건 중 9건이 로컬 소켓 세션 끊김이었으며, 11월 22일 TCP 전환 후 기존 기록상 같은 원인 재발은 없었습니다. 짧은 관찰 기간의 결과입니다. 재구축 중 역할 확인 지연은 원인을 드러내도록 테스트를 개선했습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1109
-->

---

<OperatorSlide class="op-session" section="03 · 증거 · 검증이 찾은 결함" source="#1158 · 수정 PR #1159" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158">

<h1 class="op-title">VM 랩이 찾아낸 결함: 생존 확인 패킷 차단</h1><div class="session-debug"><div><span>관찰</span><h3>같은 Pod 정상<br>다른 노드 끊김</h3><p>Broker 용량을 재다가<br>잡아 둔 연결이 끊김</p></div><div class="focus"><span>원인</span><h3>멤버 → Broker</h3><p>TCP 7 생존 확인을<br>NetworkPolicy가 차단</p></div><div><span>수정·회귀</span><h3>필요한 경로만 허용</h3><p>머지한 빌드로 랩 회귀 통과<br>멤버끼리는 불필요 확인 · 종료</p></div></div><p class="session-takeaway">Kind 회귀 시험과 실제 네트워크 정책을 적용한 VM 시험을 함께 운영</p>

</OperatorSlide>

<!--
[40초 · 03 · 증거 · 검증이 찾은 결함]
VM 랩에서는 연결을 유지하지 못하는 결함도 찾았습니다. 같은 Pod 안에서는 괜찮았지만 다른 노드에서 연결하면 끊겼고, 네트워크 정책을 끄면 문제가 사라졌습니다.

원인은 서버가 상대의 생존을 확인하는 TCP 7번 패킷을 정책이 막는 것이었습니다. 필요한 경로만 허용한 뒤, 노드를 건넌 세션 40개와 Broker를 거친 연결 30개가 세 차례 대기 후에도 유지됐습니다. Kind에는 이 정책이 없어 놓쳤습니다. 실제 환경 시험을 함께 하는 이유입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158
-->

---

<OperatorSlide class="op-session" section="03 · 증거 · 한계" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">차단 전에 성공한 쓰기는 새 master에 없을 수 있습니다</h1><div class="session-limits"><div><strong>13건</strong><h3>승인했지만 새 master에 없는 쓰기</h3><p>복제 정지 후 VM 전원 차단<br>옛 master 디스크에는 남음</p></div><div><strong>최대 73건</strong><h3>승인했지만 승격 멤버에 없는 쓰기</h3><p>VM 분할 5회에서 13–73건<br>격리 전 승인된 쓰기</p></div><div><strong>28초</strong><h3>불필요한 쓰기 중단</h3><p>master Pod 정상 종료 때 (Kind)<br>격리가 발생한 기록</p></div></div><p class="session-takeaway">차단 전 데이터 보존과 쓰기 중단 시간은 남은 과제</p>

</OperatorSlide>

<!--
[35초 · 본문 설명]
막지 못한 사례도 있습니다. 복제를 멈춘 뒤 VM 전원을 차단하자, 성공 응답을 받은 데이터 13건이 새 master에 없었습니다. 옛 master 디스크에는 남아 있었습니다. 네트워크 분할 시험에서는 새 master에 최대 73건이 없었습니다. 모두 쓰기 경로를 닫기 전에 승인된 데이터입니다.

반대로 정상 종료 때 불필요하게 쓰기가 28초 막힌 Kind 기록도 있습니다. 두 문제 모두 시험 조건과 함께 공개합니다.

관측 근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035 및 https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md (section 8의 2026-11-17–18 VM 기록).

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-session" section="04 · v0.1">

<ChapterDivider number="04" title="그래서 v0.1" subtitle="증거에서 나온 약속과 일정" />

</OperatorSlide>

<!--
[0초 · 04 · v0.1]
다음 주제를 알리는 전환 페이지입니다. 별도 설명 없이 다음 장으로 진행합니다.
-->

---

<OperatorSlide class="op-session" section="04 · v0.1 · 범위" source="ROADMAP · 시나리오 계약" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">v0.1의 약속은 세 가지로 나눕니다</h1><table class="session-table"><thead><tr><th>구분</th><th>범위</th><th>공개 조건</th></tr></thead><tbody><tr><td><b>반드시 통과</b></td><td>설치·복제 · 장애 대응<br>재구축·백업·복원 · 운영 안전</td><td>필수 항목 실패·막힘·미실행 없음</td></tr><tr><td><b>측정해 공개</b></td><td>전원 손실 · 분할·반복 장애<br>master Pod 정상 종료 (switchover 전까지 master 교체 시)</td><td>안전 규칙 통과<br>시간·손실 측정 공개</td></tr><tr><td>v0.2로 이월</td><td>기존 데이터 자동 재합류<br>옛 볼륨 자동 채택</td><td>이번 공개 범위 밖</td></tr></tbody></table><p class="session-takeaway">CUBRID 11.4.x · amd64 · 3-VM 랩 · node-local 스토리지</p>

</OperatorSlide>

<!--
[40초 · 04 · v0.1 · 범위]
v0.1 공개 조건은 세 가지로 나눴습니다. 설치와 복구 같은 필수 기능은 모두 통과해야 합니다. 전원 차단이나 네트워크 분할에서는 시간과 손실을 측정해 공개하고, 닫힌 뒤 쓰기를 받지 않는 안전 규칙은 반드시 지켜야 합니다.

기존 데이터를 그대로 활용하는 자동 재합류와 옛 볼륨 자동 채택은 다음 버전으로 미룹니다. 이번 검증은 CUBRID 11.4, amd64, 서버별 로컬 디스크를 쓰는 VM 세 대로 한정합니다. 다른 노드로 볼륨을 옮기는 CSI 동작은 검증하지 않았습니다.

질문 시 참고 — 상세 시나리오: 필수 S00–S02, S03 abrupt, S05–S06, S10–S15, 상태·이벤트·메트릭. 측정 S04, S07–S08, S03 graceful. 이월 S09 및 옛 볼륨 자동 채택.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
-->

---

<OperatorSlide class="op-session" section="04 · v0.1 · 판정" source="릴리스 후보 검증 #126" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126">

<h1 class="op-title">기준이 바뀌어도, 과거 결과는 남깁니다</h1><div class="session-debug"><div><span>원래 결과</span><h3>실패 기록 보존</h3><p>기존 시간 기준을 넘긴 기록도 유지<br>예: 전원 손실 30초 기준 실패 2회</p></div><div class="focus"><span>v0.1 판정</span><h3>범위별로 별도 판정</h3><p>안전 규칙 위반은 실패<br>측정 항목은 시간·손실 공개</p></div><div><span>공개 결정</span><h3>필수 증거 확인</h3><p>누락은 통과가 아닌 막힘<br>재구축은 5분 기준 적용</p></div></div>

</OperatorSlide>

<!--
[20초 · 본문 설명]
범위를 바꿔도 과거 실패 기록은 그대로 보존합니다. v0.1 판정은 별도로 남기고, 안전 규칙 위반은 여전히 실패입니다. 측정 항목의 시간과 손실은 공개하지만, 필수 항목인 볼륨 교체 재구축은 5분 기준을 통과해야 합니다. 필수 증거가 없으면 막힘입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-session" section="04 · v0.1 · 일정" source="ROADMAP v0.1 일정" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">후보를 고정하고, 같은 조건에서 검증합니다</h1><div class="session-roadmap"><div><span>11.30–12.06</span><h3>후보 준비</h3><p>판정 도구 정렬<br>이미지·소스 식별</p></div><div class="focus"><span>12.07</span><h3>후보 동결</h3><p>소스·이미지·엔진<br>랩 환경 고정</p></div><div><span>12.08–12.14</span><h3>반복 검증</h3><p>필수 시나리오<br>24시간 부하 시험</p></div><div><span>12.15–12.20</span><h3>독립 재현</h3><p>문서만 보고<br>설치·복구·복원</p></div></div><p class="session-decision"><b>12.21–12.27 · 공개 판단</b><span>필수 증거가 빠지면 보류</span></p>

</OperatorSlide>

<!--
[35초 · 04 · v0.1 · 일정]
남은 일정입니다. 11월 말부터 판정 도구와 이미지 식별, 랩 통제를 정리하고, 12월 7일에 소스와 이미지, 엔진 버전, 랩을 하나로 고정합니다. 그 후보로 필수 시나리오를 반복하고 24시간 부하 시험을 합니다.

12월 15일부터는 코드를 쓰지 않은 사람이 문서만 보고 설치, 장애 복구, 복원을 재현합니다. 마지막 주에 증거를 보고 공개 여부를 정합니다. 필수 증거가 빠지면 날짜가 와도 공개하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-session" section="04 · v0.1 · 팀" source="팀 역할" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md">

<h1 class="op-title">작성자와 최종 검증자를 나눕니다</h1><div class="session-debug session-two"><div><span>구현 · 실행</span><h3>만들고 기록</h3><p>Operator 구현 · 장애 시나리오<br>판정 도구 · VM 랩 실행 기록</p></div><div class="focus"><span>리뷰 · 독립 재현</span><h3>다른 사람이 확인</h3><p>코드·결과 교차 검증<br>문서만 보고 설치·복구 재현</p></div></div><p class="session-takeaway">공유 랩 장애 시험은 한 번에 하나 · 공개 여부는 공동 결정</p>

</OperatorSlide>

<!--
[10초 · 본문 설명]
팀 원칙은 1차 때와 같습니다. 작성자와 최종 검증자를 다르게 하고, 공유 랩 시험은 한 번에 하나씩, 공개 여부는 함께 결정합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md
-->

---

<OperatorSlide class="op-session" section="04 · v0.1 이후" source="ROADMAP · v0.2 후보" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">v0.1 이후에는 미룬 기능부터 검토합니다</h1><div class="session-next"><div><span>복구 자동화</span><h3>자동 재합류</h3><p>기존 데이터로 안전하게 합류</p></div><div><span>데이터 수명주기</span><h3>옛 볼륨 채택</h3><p>재생성한 클러스터에서 이어받기</p></div><div><span>운영 안정성</span><h3>아카이브 로그 한도</h3><p>멤버 볼륨의 로그 공간 제한</p></div><div><span>설계 개선</span><h3>관찰과 정책 분리</h3><p>HA 관측과 격리 판단 분리</p></div></div><p class="session-takeaway">우선순위는 v0.1 검증 결과와 사용자 피드백으로 결정</p>

</OperatorSlide>

<!--
[20초 · 본문 설명]
v0.1 이후에는 미뤄 둔 것부터 봅니다. 남아 있던 데이터로 자동 재합류, 옛 볼륨 이어받기, 아카이브 로그 공간 제한, 그리고 HA 관측과 격리 판단을 나누는 설계입니다. 우선순위는 v0.1 결과와 사용자 피드백을 보고 정하겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-session" section="마무리">

<p class="op-kicker">이번 검증의 성과</p><div class="op-clean-statement"><h1>표시에서 차단으로.<br>복구 뒤 데이터 대조까지.</h1></div><p class="op-clean-caption">쓰기 격리 · 명시적 재구축 · 반복 장애 후 멤버 복귀 검증</p>

</OperatorSlide>

<!--
[20초 · 마무리]
이번에는 상태 표시에서 실제 쓰기 차단으로 나아갔고, 복구 뒤 데이터가 남았는지도 확인했습니다. 차단 전의 손실과 불필요한 중단은 여전히 남아 있습니다. 이 한계를 공개하고, 남은 안전성 시험과 다른 사람의 독립 재현을 통과한 뒤 릴리스를 결정하겠습니다.

-->

---

<OperatorSlide class="op-session" section="Q&amp;A · 질의응답" source="Operator 저장소" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">감사합니다</p><p class="op-caption"><a href="#/22">상세 구조</a> · <a href="#/23">시험 비교</a> · <a href="#/24">관측 조건</a></p><div class="op-meta"><b>CUBRID Lab</b><span>최영선 · 백경준</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 프로젝트입니다. CUBRID는 해당 권리자의 상표입니다.</p></div>

</OperatorSlide>

<!--
[Q&A]
감사합니다. 질문 받겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 전체 아키텍처" source="전체 아키텍처 · 쓰기 격리 ADR-0005 · 재구축 ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">1차 아키텍처 위에 쓰기 격리와 재구축을 더했습니다</h1><svg class="op-arch" style="max-height:325px" viewBox="0 0 900 392" role="img" aria-label="1차 전체 아키텍처 위에 이번에 더한 것: A 쓰기 격리 판단은 Operator가, B 격리 시 읽기-쓰기 Broker를 0개로 줄여 SQL 경로를 닫고, C 볼륨을 잃은 멤버는 요청에 따라 현재 master의 백업으로 다시 채웁니다.">
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
<rect x="0" y="92" width="140" height="132" rx="8" style="fill:var(--blue-soft);stroke:var(--blue);stroke-width:1.5"/><text x="10" y="112" style="fill:var(--blue);font-weight:700">이번에 더한 것</text><text class="s" x="10" y="136"><tspan style="fill:var(--blue);font-weight:700">A</tspan> 쓰기 격리 판단</text><text class="s" x="10" y="160"><tspan style="fill:var(--blue);font-weight:700">B</tspan> RW Broker 0개로</text><text class="s" x="22" y="176">SQL 경로 차단</text><text class="s" x="10" y="200"><tspan style="fill:var(--blue);font-weight:700">C</tspan> 명시적 재구축</text><text class="s" x="22" y="216">master 백업 → 복원</text>
<circle cx="352" cy="32" r="9" style="fill:var(--blue-soft);stroke:var(--blue);stroke-width:1.5"/><text x="352" y="36" text-anchor="middle" style="fill:var(--blue);font-weight:700" font-size="11">A</text>
<rect x="309" y="232" width="132" height="62" rx="9" style="fill:none;stroke:var(--blue);stroke-width:2.5"/><circle cx="440" cy="234" r="9" style="fill:var(--blue-soft);stroke:var(--blue);stroke-width:1.5"/><text x="440" y="238" text-anchor="middle" style="fill:var(--blue);font-weight:700" font-size="11">B</text>
<circle cx="874" cy="186" r="9" style="fill:var(--blue-soft);stroke:var(--blue);stroke-width:1.5"/><text x="874" y="190" text-anchor="middle" style="fill:var(--blue);font-weight:700" font-size="11">C</text>
</svg>

<p class="op-caption text-right"><a href="#/21">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
1차 때 보여 드린 전체 아키텍처입니다. 구조 자체는 그대로입니다. master 선출과 복제는 CUBRID HA가 하고, Operator는 각 멤버의 Instance Manager에 역할을 묻고 결과를 status에 기록합니다. Operator는 SQL을 중계하지 않습니다.

파란색으로 표시한 A, B, C가 이번에 추가한 동작입니다. A, Operator가 master를 확신할 수 없다고 판단하면 쓰기 격리를 기록합니다. B, 격리 중에는 읽기-쓰기 Broker를 0개로 줄여 애플리케이션의 쓰기 경로를 실제로 닫습니다. C, 볼륨을 잃은 멤버는 사람이 요청하면 현재 master의 백업으로 다시 채웁니다. 다음 장부터 하나씩 보겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 비교 시험 상세" source="VM 랩 비교 실행 2026-11-25 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">두 번의 master 삭제 뒤, 세 멤버가 자동 복귀했습니다</h1><p class="op-caption">2026-11-25 VM 랩 · HA 3멤버 · 쓰기 중 master Pod 강제 삭제를 operator별 2회</p><table class="op-comparison op-repeat-comparison"><thead><tr><th>관찰 항목</th><th>CUBRID/cubrid-operator</th><th>CUBRID Lab Operator</th></tr></thead><tbody><tr><td><b>첫 삭제 뒤</b></td><td>쓰기 중단 12.4초<br>삭제한 멤버는 수동 재합류</td><td>쓰기 중단 22.0초<br>삭제한 멤버 자동 복귀</td></tr><tr><td><b>두 번째 삭제 뒤</b></td><td>새 master 미선출 · Pod는 Ready<br>31분 뒤 정리할 때까지 쓰기 불가</td><td>최장 승인 공백 32.8초<br>격리 이후 재개 +42.5초<br>세 멤버 모두 자동 복귀</td></tr><tr><td><b>두 번째 장애의 원인</b></td><td>Pod 목록이 바뀔 때마다 <code>ha_node_list</code> 순서를 다시 씀<br>멤버마다 우선순위가 달라 남은 둘 다 standby</td><td>스펙에서 만든 한 목록을 모든 멤버가 공유<br>Pod 교체·master 이동에도 순서 불변</td></tr><tr><td><b>승인된 쓰기 손실</b></td><td>두 시험 모두 0건</td><td>두 시험 모두 0건</td></tr></tbody></table>

<p class="op-caption text-right"><a href="#/21">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
같은 VM 랩에서 두 Operator로 HA 3멤버를 구성하고, 쓰기 중에 master Pod를 두 번씩 삭제했습니다. 첫 장애에서는 둘 다 쓰기가 다시 가능해졌고, 승인된 쓰기 손실도 없었습니다. 다만 공식 Operator는 삭제한 멤버를 사람이 다시 붙여야 했고, 저희는 자동으로 복귀했습니다.
두 번째 장애에서 차이가 더 드러났습니다. 공식 Operator는 새 master가 선출되지 않아 31분 뒤 시험을 정리할 때까지 쓰지 못했습니다. 멤버마다 ha_node_list 순서가 달라졌기 때문이고, 저희는 모든 멤버가 같은 목록을 읽습니다. 저희의 최장 쓰기 승인 공백은 32.8초였고, 격리 뒤 첫 쓰기 승인은 삭제 후 42.5초에 기록됐습니다. 세 멤버도 자동 복귀했습니다. 첫 장애의 중단 시간은 저희가 더 길었습니다. 이번 성과는 두 번의 시험에서 멤버 복귀까지 자동으로 이어졌다는 것이며, 모든 장애의 자동 복구를 입증한 것은 아닙니다.

질문 시 참고: 초기 구성은 공식 Operator에서 DB 생성·HA 시작·Broker 시작을 멤버마다 수동 실행했고, Lab Operator는 수동 단계 없이 약 2분이었습니다. 두 번째 장애의 원인: 공식 Operator는 Pod 목록이 바뀔 때마다 ha_node_list를 조회 순서대로 다시 써서 ha-0:ha-1:ha-2, ha-1:ha-2:ha-0, ha-2:ha-0:ha-1로 바뀌었고, 손으로 다시 붙인 멤버만 새 순서를 읽었습니다. 이 Operator는 ha_node_list를 스펙만으로 순번대로 만들어 ConfigMap 하나로 모든 멤버에 주므로 Pod 교체나 master 이동에도 바뀌지 않습니다(ADR-0001·ADR-0004). 네트워크 분할은 이 비교에 포함하지 않았습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-compact op-session" section="부록 · 한계와 시험 조건" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">숨기지 않고 공개할 한계</h1><ol class="op-risks"><li><b>복제 지연 후 VM 전원 차단: 승인된 쓰기 13건이 새 master에 없음</b><span>2026-11-19 VM 시험 · 복제 프로세스를 정지한 조건 · 해당 행은 옛 master 디스크에만 남음</span></li><li><b>네트워크 분할에서 승격된 멤버에 승인된 쓰기 최대 73건 없음</b><span>11월 17–18일 VM 분할 5회에서 13–73건 미반영 · 1회는 73건이 없는 멤버가 active master로 전환</span></li><li><b>master Pod 정상 종료 때 쓰기 경로가 28초 닫힘 (Kind)</b><span>불필요한 격리 · 시간과 원인을 공개</span></li><li><b>스토리지는 node-local, CSI 아님</b><span>볼륨이 다른 노드로 따라가는 동작·스냅샷·크기 변경은 검증하지 않음</span></li></ol><p class="op-boundary"><b>원칙</b>　Operator의 제어 범위와 엔진 동작의 한계를 구분하고, 재현 조건과 영향을 공개합니다</p>

<p class="op-caption text-right"><a href="#/21">← Q&amp;A로 돌아가기</a></p>

</OperatorSlide>

<!--
[부록 · 질문 시 설명]
공개할 한계입니다. 복제 프로세스를 정지한 뒤 VM 전원을 차단한 시험에서 승인된 쓰기 13건이 새 master에 없었습니다. 해당 행은 옛 master 디스크에만 남았습니다. 원인에 대한 가설과 관측 결과는 구분합니다. 네트워크 분할에서는 경로를 닫기 전에 승인된 쓰기가 승격된 멤버에 최대 73건 없었습니다. master Pod를 정상 종료할 때 쓰기 경로가 28초 닫히는 문제도 있습니다.

그리고 저희 랩은 node-local 스토리지라 CSI 동작은 검증하지 않았습니다. 이 숫자는 각각의 시험 조건에서 관찰한 결과입니다. 앞서 소개한 격리 유지 시험과 구분해야 합니다. 승격된 멤버의 미반영과 전체 멤버에서의 최종 손실도 같은 뜻으로 쓰지 않습니다. 제어 가능한 범위와 엔진 동작의 한계를 구분해 공개하겠습니다.

관측 근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035 및 https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md (section 8의 2026-11-17–18 VM 기록).

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->
