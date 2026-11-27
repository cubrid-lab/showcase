# 발표 스크립트 (2차 검증)

슬라이드 원본: [slides.ko.md](../../../presentation/decks/2026-builder-season4/02-validation/slides.ko.md) · 예상 질문: [EXPECTED_QA.ko.md](EXPECTED_QA.ko.md)

본편 21장, 설명 배정 9분 5초입니다. 10분 중 55초는 전환과 호흡에 배정합니다. 실제 시간은 리허설에서 확인합니다.

## 장별 스크립트

### 1. CUBRID K8s Operator (20초)

> 안녕하세요. CUBRID Lab의 최영선, 백경준입니다. 저장 성공 응답을 받았는데, 장애 뒤 그 데이터가 없다면 어떨까요? 저희는 Kubernetes에서 CUBRID 운영과 복구를 관리하는 Operator를 만들고 있습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator

### 2. 발표 순서 (10초)

> 프로젝트와 1차 피드백을 먼저 소개하겠습니다. 이어서 설계가 어떻게 바뀌었는지와 검증 결과를 보여드리고, 함께 논의할 질문과 최종 발표까지의 계획을 말씀드리겠습니다.

### 3. 장애 뒤 CUBRID가 다시 쓸 수 있는 상태인지 확인합니다 (20초)

> 첫 사용자는 CUBRID 운영자와 Kubernetes 플랫폼 담당자입니다. 예를 들어 장애로 DB 서버가 교체됐을 때 운영자는 쓰기 연결을 다시 열어도 되는지 판단해야 합니다. 저희 Operator는 DB 상태를 확인하고 쓰기 연결과 복구 작업을 조정합니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator

### 4. 장애 중 쓰기 차단과 복원 증거를 우선했습니다 (40초)

> 1차 검토 의견은 쓰기 격리가 실제로 동작하는지 먼저 입증하라는 것이었습니다. 그래서 네트워크 분할 시험에서 차단 뒤 승인된 쓰기가 없는지 확인했습니다. 안전 때문에 쓰기가 얼마나 멈추는지도 별도로 측정했습니다. 복원은 1차 때 세션이 끊겨 판정을 보류한 두 건을 그대로 남겼고, 이후 새 클러스터로 복원한 시험 세 건에서 통과를 관측했습니다. 공개 후보에서는 실패 조건도 포함해 다시 확인합니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 5. 자동화와 지원 범위는 검증할 수 있는 만큼 좁혔습니다 (30초)

> 재합류 과정에서 최신 데이터를 덮어쓰지 않도록, v0.1에서는 운영자가 대상을 확인하고 현재 master의 백업으로 재구축합니다. 기존 데이터를 자동으로 가져오는 방식은 판별 기준과 검증 증거가 더 필요해 미뤘습니다. 공식 Operator와는 동일 장애에서 수동 개입과 복구를 비교했습니다. CSI, 무중단 확장과 복제 지연에 따른 읽기 전환은 이번 검증 밖입니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 6. 상태를 표시하는 설계에서 쓰기를 제어하는 설계로 (40초)

> 처음부터 master 선출과 복제는 CUBRID가 맡았습니다. 달라진 것은 상태가 불확실할 때 Operator가 하는 일입니다. 처음에는 상태를 표시했고, 지금은 쓰기 연결을 닫습니다. 데이터 볼륨을 잃은 서버는 운영자 승인 뒤 현재 master의 백업으로 다시 구성합니다. v0.1에서는 차단 뒤 쓰기 승인이 없고, 잘못된 재구축은 거부되며, 복원 결과를 다른 운영자도 확인할 수 있어야 합니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 7. 불확실하면, 확인될 때까지 쓰기를 막습니다 (30초)

> 현재 쓰기를 받는 DB 서버를 master라고 부릅니다. 나머지 서버는 그 데이터를 복제합니다. 저장 성공 응답을 받았더라도 복제가 끝나기 전에 장애가 나면, 새 master에는 그 데이터가 없을 수 있습니다.

> 그래서 누가 쓰기를 받아도 되는지 불확실하면 쓰기 연결을 끊습니다. 이것이 쓰기 격리입니다. 읽기 전용 Broker와 -ro Service는 쓰기 격리의 영향을 받지 않습니다. 다만 차단 전에 이미 성공한 쓰기까지 보호하는 것은 아닙니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md

### 8. Operator가 상태를 확인하고 연결을 관리합니다 (30초)

> 그림 아래가 데이터가 오가는 경로입니다. 애플리케이션은 DB 연결 창구인 Broker를 거쳐 CUBRID에 데이터를 저장합니다. 위쪽의 관리 프로그램 Operator는 각 DB 서버의 Instance Manager에 상태를 묻고, 불확실하면 쓰기용 Broker를 중지합니다.

> master 선출과 복제는 CUBRID가 맡고, Operator는 연결 관리와 복구 조정만 합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md

### 9. 연결을 끊고, 확인한 뒤 다시 엽니다 (30초)

> 쓰기 격리는 닫는 것만으로 끝나지 않습니다. master가 불확실하거나 삭제된 멤버를 아직 확인하지 못하면, 쓰기용 Broker를 0개로 줄입니다. 그리고 기존 연결과 새 연결 모두에서 저장 성공 응답이 없는지 확인합니다.

> 다시 여는 조건도 정했습니다. 멤버 미확인으로 닫은 경우에는 같은 단일 master와 다른 멤버의 안전 근거를 10초 이상 간격으로 두 번 확인해야 자동으로 엽니다. master가 여러 개인 경우 등은 사람이 판단하고, 이번 격리에만 쓸 수 있는 일회용 토큰으로 해제합니다.

> 상세 조건 — ADR-0005 Release: 두 차례 모두 격리에 기록된 같은 master를 확인하고, 다른 승격 가능 멤버는 인증·식별이 일치하는 최신 non-master 응답 또는 승인·감사된 외부 VM 전원 차단 확인과 out-of-service taint가 필요합니다. 멤버 식별이나 근거가 바뀌면 재확인하거나 자동 해제를 금지합니다. 외부 차단 근거에 따른 해제는 PrimaryResolved=True를 뜻하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md

### 10. 데이터를 잃은 서버는 요청에 따라 복구합니다 (30초)

> 프로그램이 다시 뜨는 것과 데이터를 되살리는 것은 다릅니다. 이번 시험에서는 Pod가 삭제된 멤버가 자동으로 돌아왔습니다. 반면 데이터 볼륨까지 잃은 경우에는 사람이 대상을 확인하고 복구를 요청해야 합니다.

> 요청하면 현재 master의 백업으로 데이터를 채우고, 복제하는 서버로 합류시킵니다. 시험에서는 복구 뒤 실제 데이터도 대조했습니다. 컨테이너로 구성한 Kubernetes 시험 환경인 Kind에서 복구는 40.2초, 데이터 확인까지는 48.9초였습니다. v0.1 기준은 5분입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118

### 11. 성공 응답을 받은 데이터가 남았는지 확인합니다 (25초)

> 시험에서는 성공 응답을 받은 쓰기를 기록하고, 장애 뒤 각 서버에 그 데이터가 남아 있는지 대조합니다. 연결을 닫은 뒤에는 성공 응답이 없어야 합니다.

> Kind에서는 코드 변경마다 자동 시험을 돌립니다. 실제 전원 차단과 네트워크 정책은 VM 세 대의 랩에서 따로 확인합니다. 랩은 공유 자원이라 사용 권한인 Lease를 확보하고 한 번에 하나씩 시험합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122

### 12. 두 번째 장애에서 결과가 달라졌습니다 (45초)

> 같은 VM 랩에서 쓰기 중 master Pod를 두 번씩 삭제했습니다. 그래프는 두 번째 시험입니다. 공식 Operator는 새 master가 뽑히지 않아, 31분 뒤 시험을 정리할 때까지 쓰지 못했습니다. 멤버마다 노드 우선순위 목록의 순서가 달라졌기 때문입니다. 저희는 모든 멤버가 같은 목록을 읽어 새 master가 선출됐고, 세 멤버가 자동 복귀했습니다.

> 주황 선은 삭제 직후 잠시 쓰기를 받다가 확인을 위해 닫힌 모습입니다. 쓰기 승인 사이의 최장 공백은 32.8초였고, 격리 뒤 첫 쓰기 승인은 삭제 후 42.5초에 기록됐습니다. 첫 시험의 중단은 저희가 22초로 공식의 12.4초보다 길었습니다. 두 시험 모두 쓰기 손실은 없었지만, 모든 장애에서 복구된다는 뜻은 아닙니다.

질문 시 참고: 초기 구성은 공식 Operator에서 DB 생성·HA 시작·Broker 시작을 멤버마다 수동 실행했고, Lab Operator는 수동 단계 없이 약 2분이었습니다. 두 번째 장애의 원인: 공식 Operator는 Pod 목록이 바뀔 때마다 ha_node_list를 조회 순서대로 다시 써서 ha-0:ha-1:ha-2, ha-1:ha-2:ha-0, ha-2:ha-0:ha-1로 바뀌었고, 손으로 다시 붙인 멤버만 새 순서를 읽었습니다. 이 Operator는 ha_node_list를 스펙만으로 순번대로 만들어 ConfigMap 하나로 모든 멤버에 주므로 Pod 교체나 master 이동에도 바뀌지 않습니다(ADR-0001·ADR-0004). 네트워크 분할은 이 비교에 포함하지 않았습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122

### 13. VM 랩에서 확인한 동작과 측정값입니다 (25초)

> VM 랩에서는 네트워크가 끊긴 동안 Operator를 재시작해도 쓰기 차단이 유지되는지 확인했습니다. 볼륨을 교체한 뒤의 복구와 새 클러스터로의 복원도 통과했습니다.

> 전원 차단은 세 번 측정했고, 차단 표시부터 첫 쓰기까지 26초에서 38초였습니다. 다시 장애를 냈을 때는 이전 격리의 해제 토큰 두 개가 모두 거부됐습니다. 시간은 측정값으로 공개하고, 닫힌 뒤 저장 성공 응답이 없는지는 통과와 실패로 판정합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122

### 14. 실제 환경에서 발견한 연결 끊김을 고쳤습니다 (25초)

> VM 랩에서는 연결을 유지하지 못하는 결함도 찾았습니다. 같은 Pod 안에서는 괜찮았지만 다른 노드에서 연결하면 끊겼고, 네트워크 정책을 끄면 문제가 사라졌습니다.

> 원인은 서버가 상대의 생존을 확인하는 TCP 7번 패킷을 정책이 막는 것이었습니다. 필요한 경로만 허용한 뒤, 노드를 건넌 세션 40개와 Broker를 거친 연결 30개가 세 차례 대기 후에도 유지됐습니다. Kind에는 이 정책이 없어 놓쳤습니다. 실제 환경 시험을 함께 하는 이유입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158

### 15. 차단 전에 성공한 쓰기는 새 master에 없을 수 있습니다 (30초)

> 막지 못한 사례도 있습니다. 복제를 멈춘 뒤 VM 전원을 차단하자, 성공 응답을 받은 데이터 13건이 새 master에 없었습니다. 옛 master 디스크에는 남아 있었습니다. 네트워크 분할 시험에서는 새 master에 최대 73건이 없었습니다. 모두 쓰기 경로를 닫기 전에 승인된 데이터입니다.

> 반대로 정상 종료 때 불필요하게 쓰기가 28초 막힌 Kind 기록도 있습니다. 두 문제 모두 시험 조건과 함께 공개합니다.

관측 근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035 및 https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md (section 8의 2026-11-17–18 VM 기록).

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md

### 16. 어떤 증거가 있어야 다시 쓰기를 열 수 있을까요? (25초)

> 검증단과 다른 빌더 분들께 두 가지를 묻고 싶습니다. 상태를 확인할 수 없는 서버가 있어도 쓰기를 재개할 수 있다고 판단하는 근거는 무엇일까요? 그리고 백업의 체크섬이 맞고 작업이 끝났다고 표시됐을 때, 운영자가 복원 성공을 판단하려면 어떤 데이터 검증까지 있어야 할까요?

### 17. v0.1의 약속은 세 가지로 나눕니다 (25초)

> v0.1 공개 조건은 세 가지로 나눴습니다. 설치와 복구 같은 필수 기능은 모두 통과해야 합니다. 전원 차단이나 네트워크 분할에서는 시간과 손실을 측정해 공개하고, 닫힌 뒤 쓰기를 받지 않는 안전 규칙은 반드시 지켜야 합니다.

> 기존 데이터를 그대로 활용하는 자동 재합류와 옛 볼륨 자동 채택은 다음 버전으로 미룹니다. 이번 검증은 CUBRID 11.4, amd64, 서버별 로컬 디스크를 쓰는 VM 세 대로 한정합니다. 다른 노드로 볼륨을 옮기는 CSI 동작은 검증하지 않았습니다.

질문 시 참고 — 상세 시나리오: 필수 S00–S02, S03 abrupt, S05–S06, S10–S15, 상태·이벤트·메트릭. 측정 S04, S07–S08, S03 graceful. 이월 S09 및 옛 볼륨 자동 채택.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md

### 18. 기준이 바뀌어도, 과거 결과는 남깁니다 (15초)

> 범위를 바꿔도 과거 실패 기록은 그대로 보존합니다. v0.1 판정은 별도로 남기고, 안전 규칙 위반은 여전히 실패입니다. 측정 항목의 시간과 손실은 공개하지만, 필수 항목인 볼륨 교체 재구축은 5분 기준을 통과해야 합니다. 필수 증거가 없으면 막힘입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 19. 후보를 고정하고, 같은 조건에서 검증합니다 (25초)

> 남은 일정입니다. 11월 말부터 판정 도구와 이미지 식별, 랩 통제를 정리하고, 12월 7일에 소스와 이미지, 엔진 버전, 랩을 하나로 고정합니다. 그 후보로 필수 시나리오를 반복하고 24시간 부하 시험을 합니다.

> 12월 15일부터는 코드를 쓰지 않은 사람이 문서만 보고 설치, 장애 복구, 복원을 재현합니다. 마지막 주에 증거를 보고 공개 여부를 정합니다. 필수 증거가 빠지면 날짜가 와도 공개하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md

### 20. v0.1 이후에는 미룬 기능부터 검토합니다 (10초)

> v0.1 이후에는 미뤄 둔 것부터 봅니다. 남아 있던 데이터로 자동 재합류, 옛 볼륨 이어받기, 아카이브 로그 공간 제한, 그리고 HA 관측과 격리 판단을 나누는 설계입니다. 우선순위는 v0.1 결과와 사용자 피드백을 보고 정하겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md

### 21. 표시에서 차단으로. 복구 뒤 데이터 대조까지. (15초)

> 이번에는 상태 표시에서 실제 쓰기 차단으로 나아갔고, 복구 뒤 데이터가 남았는지도 확인했습니다. 차단 전의 손실과 불필요한 중단은 여전히 남아 있습니다. 이 한계를 공개하고, 남은 안전성 시험과 다른 사람의 독립 재현을 통과한 뒤 릴리스를 결정하겠습니다.

### 22. Q&A (0초)

> 감사합니다. 질문 받겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator

## 숫자 한눈에

| 숫자 | 뜻 | 장 |
|---|---|---|
| 61 / 61 | Kind 자동 시험 통과 (1차 27개) | 예상 질문 1번 |
| 22.0초 · 32.8초 | 우리 쓰기 승인 사이의 최대 공백 (첫·두 번째 master 삭제) | 12 |
| +42.5초 | 두 번째 master 삭제 시점부터 격리 뒤 첫 쓰기 승인까지 | 12 |
| 12.4초 · 31분 | 공식 operator 쓰기 중단 (첫 삭제 · 두 번째 삭제 뒤 master 미선출, 31분 뒤 시험 정리까지 미복구) | 12 |
| 26–38초 | VM 전원 차단 표시 뒤 첫 쓰기 (3회) | 13 |
| 40.2초 · 48.9초 | Kind 재구축 완료 · 행 확인 (기준 5분) | 10 |
| 13건 | 복제 정지 후 전원 차단에서 새 master에 없는 승인된 쓰기 | 15 |
| 최대 73건 | 분할에서 승격 멤버에 없는 승인된 쓰기 (5회 중 13–73) | 15 |
| 28초 | master Pod 정상 종료 때 불필요한 격리 (Kind) | 15 |
| 12/7 · 12/27 | 후보 동결 · 공개 판단 마감 | 19 |
