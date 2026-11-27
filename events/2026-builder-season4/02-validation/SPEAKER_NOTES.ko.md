# 발표 스크립트 (2차 검증)

슬라이드 원본: [slides.ko.md](../../../presentation/decks/2026-builder-season4/02-validation/slides.ko.md) · 예상 질문: [EXPECTED_QA.ko.md](EXPECTED_QA.ko.md)

본편 18장, Q&A 1장, 부록 4장입니다. 본편 설명 배정은 8분 50초입니다. 실제 시간은 리허설에서 확인합니다.

## 장별 스크립트

### 1. CUBRID K8s Operator (20초)

> 안녕하세요. CUBRID Lab의 최영선, 백경준입니다. DB 서버가 장애로 바뀌었습니다. 앱은 언제 다시 데이터를 써도 될까요? 오늘은 저희가 그 판단을 어떻게 돕고, 실제 장애 시험에서 무엇을 확인했는지 말씀드리겠습니다.

### 2. 발표 순서 (10초)

> 먼저 프로젝트와 1차 피드백을 소개하고, 바뀐 설계와 시험 결과를 보여드리겠습니다. 마지막으로 함께 논의할 질문과 공개 전 계획을 말씀드리겠습니다.

### 3. Operator와 Instance Manager가 포함된 전체 구조 (35초)

> 저희가 만드는 두 구성 요소는 파란색 상자에 표시했습니다. Operator는 클러스터 전체를 보고 쓰기 연결과 복구를 조정합니다. Instance Manager는 DB 서버마다 하나씩 있고, 그 서버의 상태를 알려주거나 백업·복원 작업을 실행합니다. DB 운영자와 플랫폼 담당자는 이 두 구성 요소로 장애에 대응합니다. 앱은 아래쪽 Service와 Broker를 거쳐 CUBRID에 연결합니다. CUBRID가 쓰기를 받을 서버를 정하고 데이터를 복제하며, 백업 파일은 오른쪽 아래 저장소에 보관합니다.

### 4. 1차 피드백 반영 (40초)

> 1차 검토 의견은 쓰기 격리가 실제로 동작하는지 먼저 입증하라는 것이었습니다. 그래서 네트워크 분할 시험에서 차단 뒤 승인된 쓰기가 없는지 확인했습니다. 안전 때문에 쓰기가 얼마나 멈추는지도 별도로 측정했습니다. 복원은 1차 때 세션이 끊겨 판정을 보류한 두 건을 그대로 남겼고, 이후 새 클러스터로 복원한 시험 세 건에서 통과를 관측했습니다. 공개 후보에서는 실패 조건도 포함해 다시 확인합니다.

근거:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 5. 1차 피드백 비반영 (30초)

> 재합류 과정에서 최신 데이터를 덮어쓰지 않도록, v0.1에서는 운영자가 대상을 확인하고 현재 master의 백업으로 재구축합니다. 기존 데이터를 자동으로 가져오는 방식은 판별 기준과 검증 증거가 더 필요해 미뤘습니다. 공식 Operator에서 바꿔 쓰는 데 드는 비용과 협력 방식은 추가로 검토합니다. 외부 스토리지, 무중단 확장, 복제 지연에 따른 읽기 전환도 이번 시험에 포함하지 않았습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 6. v0.1 구현 범위: 쓰기 차단, 서버 재구축, 백업 복원 (40초)

> 저희가 v0.1에서 끝내려는 일은 세 가지입니다. 첫째, 어느 서버가 쓰기를 받을지 불확실하면 실제로 쓰기 연결을 끊습니다. 둘째, 디스크를 잃은 서버는 운영자가 대상을 승인한 뒤 백업으로 다시 구성합니다. 셋째, 백업을 다른 클러스터에 복원할 수 있게 합니다. 1차 때는 주로 상태를 확인하고 알리는 데 집중했습니다. 지금은 Operator가 연결과 복구를 조정하고 Instance Manager가 각 서버에서 작업을 실행합니다. 다음 그림에서 그 역할을 보여드리겠습니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 7. v0.1 세부 아키텍처: Operator와 Instance Manager (35초)

> v0.1에서 검증할 관리 경로입니다. 왼쪽 Kubernetes API에서 클러스터 설정과 백업 요청을 받습니다. 가운데 Operator의 클러스터 컨트롤러는 서버 상태를 모아 판단하고, 쓰기를 막아야 하면 쓰기용 Broker를 0개로 줄입니다. 백업 컨트롤러는 대상 서버를 정하고 결과를 기록합니다. 오른쪽 각 DB Pod의 Instance Manager는 인증된 요청을 받아 CUBRID 상태를 읽거나 백업과 복원 준비를 실행합니다. 공개 전에는 이 구조로 쓰기 차단과 재개, 승인 후 디스크 재구축, 새 클러스터 복원을 확인합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/DESIGN.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 8. 안전을 확인한 뒤 쓰기 연결을 다시 엽니다 (25초)

> 서버 상태가 불확실하면 새 연결만 막아서는 부족합니다. 이미 열린 연결도 쓰기용 Broker를 멈춰 끊습니다. 상태를 확인하지 못해 차단한 경우에도 안전 근거를 다시 확인한 뒤에만 자동으로 엽니다. 여러 서버가 자신이 쓰기를 받는다고 보고하는 경우에는 운영자가 판단합니다.

질문 시 참고:
쓰기 격리는 닫는 것만으로 끝나지 않습니다. master가 불확실하거나 삭제된 멤버를 아직 확인하지 못하면, 쓰기용 Broker를 0개로 줄입니다. 그리고 기존 연결과 새 연결 모두에서 저장 성공 응답이 없는지 확인합니다.

다시 여는 조건도 정했습니다. 멤버 미확인으로 닫은 경우에는 같은 단일 master와 다른 멤버의 안전 근거를 10초 이상 간격으로 두 번 확인해야 자동으로 엽니다. master가 여러 개인 경우 등은 사람이 판단하고, 이번 격리에만 쓸 수 있는 일회용 토큰으로 해제합니다.

상세 조건 — ADR-0005 Release: 두 차례 모두 격리에 기록된 같은 master를 확인하고, 다른 승격 가능 멤버는 인증·식별이 일치하는 최신 non-master 응답 또는 승인·감사된 외부 VM 전원 차단 확인과 out-of-service taint가 필요합니다. 멤버 식별이나 근거가 바뀌면 재확인하거나 자동 해제를 금지합니다. 외부 차단 근거에 따른 해제는 PrimaryResolved=True를 뜻하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md

### 9. 디스크를 잃은 서버는 백업으로 복구합니다 (30초)

> 프로그램이 다시 뜨는 것과 데이터를 되살리는 것은 다릅니다. 이번 시험에서는 Pod가 삭제된 멤버가 자동으로 돌아왔습니다. 반면 데이터 볼륨까지 잃은 경우에는 사람이 대상을 확인하고 복구를 요청해야 합니다.

> 요청하면 현재 master의 백업으로 데이터를 채우고, 복제하는 서버로 합류시킵니다. 시험에서는 복구 뒤 실제 데이터도 대조했습니다. 컨테이너로 구성한 Kubernetes 시험 환경인 Kind에서 복구는 40.2초, 데이터 확인까지는 48.9초였습니다. v0.1 기준은 5분입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118

### 10. 장애 전 저장 기록과 복구 후 데이터를 대조했습니다 (25초)

> 시험에서는 성공 응답을 받은 쓰기를 기록하고, 장애 뒤 각 서버에 그 데이터가 남아 있는지 대조합니다. 연결을 닫은 뒤에는 성공 응답이 없어야 합니다.

> Kind에서는 코드 변경마다 자동 시험을 돌립니다. 실제 전원 차단과 네트워크 정책은 VM 세 대의 랩에서 따로 확인합니다. 랩은 공유 자원이라 사용 권한인 Lease를 확보하고 한 번에 하나씩 시험합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122

### 11. 두 번째 장애 뒤 Lab Operator만 쓰기를 재개했습니다 (40초)

> 두 Operator를 같은 환경에서 시험했습니다. 두 번째 장애 뒤 Lab Operator에서는 CUBRID가 새로 쓰기를 받을 서버를 정했고 쓰기가 다시 됐습니다. 공식 Operator 쪽은 새 서버가 정해지지 않아 31분 뒤 시험 종료까지 쓰지 못했습니다. 첫 장애는 반대였습니다. Lab Operator의 쓰기 중단이 더 길었습니다. 이 결과는 같은 조건에서 강제 삭제를 두 번 해 본 관찰입니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122

### 12. 차단 뒤 쓰기 성공 0건, 새 클러스터 복원 3회 통과 (25초)

> VM 랩에서는 네트워크가 끊긴 동안 Operator를 재시작해도 쓰기 차단이 유지되는지 확인했습니다. 볼륨을 교체한 뒤의 복구와 새 클러스터로의 복원도 통과했습니다.

> 전원 차단은 세 번 측정했고, 차단 표시부터 첫 쓰기까지 26초에서 38초였습니다. 다시 장애를 냈을 때는 이전 격리의 해제 토큰 두 개가 모두 거부됐습니다. 시간은 측정값으로 공개하고, 닫힌 뒤 저장 성공 응답이 없는지는 통과와 실패로 판정합니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122

### 13. 지금 겪는 문제: 데이터 누락, 긴 중단, 복원 판정 (45초)

> 시험에서 세 가지가 남았습니다. 먼저 이미 성공했다고 응답한 데이터가 새 서버에 없던 경우가 있었습니다. 복제를 일부러 멈춘 전원 차단 시험에서는 13건이 이전 서버에만 남았고, 네트워크 장애 시험에서는 새 서버에 최대 73건이 없었습니다. 이런 차단 전 누락은 조건과 함께 공개합니다. 두 번째로, 쓰기를 다시 열기로 한 뒤에도 Broker가 뜨는 데 12초에서 17초가 걸렸습니다. 마지막으로, 복원은 작업 완료 표시만으로 판단하기 어려웠습니다. 공개 후보에서는 실제 데이터를 대조하고 다른 운영자가 복원에 성공하는지 확인합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/702
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/238
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/127

### 14. v0.1 이후로 미룬 기능과 이유 (30초)

> 기존 데이터를 그대로 써서 자동으로 재합류시키는 기능과, 새 클러스터에 기존 디스크를 자동으로 연결하는 기능은 v0.2로 미뤘습니다. 기존 데이터의 상태와 소유권을 안전하게 판별해야 하기 때문입니다. 쓰기 연결을 더 빨리 여는 개선은 아직 일정을 정하지 않았습니다. 기존 연결까지 끊는 안전 조건을 유지할 수 있다는 증거가 먼저 필요합니다. v0.1에서는 현재 방식의 중단 시간을 측정해 공개합니다.

근거:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/116
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/798
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161

### 15. 쓰기 재개와 복원 완료 기준에 대한 질문 (25초)

> 검증단과 다른 빌더 분들께 두 가지를 묻고 싶습니다. 상태를 확인할 수 없는 서버가 있어도 쓰기를 재개할 수 있다고 판단하는 근거는 무엇일까요? 그리고 백업의 체크섬이 맞고 작업이 끝났다고 표시됐을 때, 운영자가 복원 성공을 판단하려면 어떤 데이터 검증까지 있어야 할까요?

### 16. 필수 안전 시험을 모두 통과해야 v0.1을 공개합니다 (30초)

> v0.1 공개 전에 설치와 복제, 장애 대응, 재구축과 백업 복원을 검증합니다. 쓰기를 막은 뒤에도 성공 응답이 나오거나 증거가 빠지면 공개를 보류합니다. 얼마나 빨리 다시 쓸 수 있었는지와 차단 전 승인된 데이터가 얼마나 남지 않았는지는 시험 조건과 함께 공개합니다. 과거에 실패했던 시험도 기록에 남깁니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126

### 17. 12월에 공개 후보를 확정하고 장애 시험을 반복합니다 (25초)

> 남은 일정입니다. 11월 말부터 판정 도구와 이미지 식별, 랩 통제를 정리하고, 12월 7일에 소스와 이미지, 엔진 버전, 랩을 하나로 고정합니다. 그 후보로 필수 시나리오를 반복하고 24시간 부하 시험을 합니다.

> 12월 15일부터는 코드를 쓰지 않은 사람이 문서만 보고 설치, 장애 복구, 복원을 재현합니다. 마지막 주에 증거를 보고 공개 여부를 정합니다. 필수 증거가 빠지면 날짜가 와도 공개하지 않습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md

### 18. 쓰기 차단은 확인했고, 차단 전 데이터 누락도 발견했습니다 (20초)

> 이번 시험에서는 불확실한 때 쓰기 연결을 끊을 수 있었습니다. 차단 전에 이미 저장 성공으로 응답했지만 새 서버에 없던 데이터도 확인했습니다. 공개 후보에서 안전 조건을 다시 검증하고, 남은 한계는 시험 조건과 함께 공개하겠습니다.

### 19. Q&A (0초)

> 감사합니다. 질문 받겠습니다.

근거: https://github.com/cubrid-lab/cubrid-kubernetes-operator

## 숫자 한눈에

| 숫자 | 뜻 | 장 |
|---|---|---|
| 61 / 61 | Kind 자동 시험 통과 (1차 27개) | 예상 질문 1번 |
| 22.0초 · 32.8초 | 우리 쓰기 승인 사이의 최대 공백 (첫·두 번째 master 삭제) | 21 |
| +42.5초 | 두 번째 master 삭제 시점부터 격리 뒤 첫 쓰기 승인까지 | 21 |
| 12.4초 · 31분 | 공식 operator 쓰기 중단 (첫 삭제 · 두 번째 삭제 뒤 master 미선출, 31분 뒤 시험 정리까지 미복구) | 21 |
| 26–38초 | VM 전원 차단 표시 뒤 첫 쓰기 (3회) | 12 |
| 40.2초 · 48.9초 | Kind 재구축 완료 · 행 확인 (기준 5분) | 9 |
| 13건 | 복제 정지 후 전원 차단에서 새 master에 없는 승인된 쓰기 | 22 |
| 최대 73건 | 분할에서 승격 멤버에 없는 승인된 쓰기 (5회 중 13–73) | 22 |
| 28초 | master Pod 정상 종료 때 불필요한 격리 (Kind) | 22 |
| 12/7 · 12/27 | 후보 동결 · 공개 판단 마감 | 17 |
