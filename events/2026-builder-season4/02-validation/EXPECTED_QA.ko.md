# 질의응답 준비 (2차 검증)

문장 기준: 2026-11-27 · 시험 결과 기준: 2026-11-25 (Operator main `3806d1db`).
질문이 나오면 참고할 답변입니다. 숫자마다 근거 링크를 달았습니다.

## 1. 1차와 2차는 무엇이 다른가요?

1차 때는 계획을 말씀드렸고, 이번에는 만들어서 직접 장애를 내 본 결과입니다.

- **쓰기 안전.** 1차에서는 master를 확신할 수 없을 때 상태에 "미확정"이라고 표시만 했습니다.
  이번에는 쓰기 격리를 구현했습니다. 미확정이면 읽기-쓰기 Broker를 0개로 줄여 쓰기 경로를 닫습니다.
- **복구.** 볼륨을 잃은 멤버를 사람이 요청하면 다시 채우는 명시적 재구축을 구현했습니다.
- **시험.** Kind 테스트가 27개에서 61개로 늘었습니다.
  VM 랩에서는 전원 차단, 네트워크 분할, Operator 재시작까지 실제로 냈습니다.
- **판정.** "30초 안에 복구" 같은 숫자 기준 대신, 안전 규칙은 통과/실패로 판정합니다.
  시간과 손실은 측정해서 공개합니다.

## 2. 쓰기를 막으면 그게 장애 아닌가요?

쓰기용 연결을 차단하고, 안전 근거를 확인한 뒤 다시 엽니다.

- **읽기.** 읽기 전용 Broker와 `-ro` Service는 그대로 둡니다. 장애 중 읽기 성공까지 보장한다는 뜻은 아닙니다.
- **해제.** 멤버를 확인하지 못해 걸린 격리는, 같은 master와 다른 멤버의 안전 근거를 10초 이상 간격으로 두 번 확인하면 자동으로 풀립니다.
  master가 둘인 경우처럼 사람이 판단해야 하는 경우에만 일회용 토큰으로 엽니다.

막는 이유는 두 실패의 성격이 다르기 때문입니다.

- 잘못된 "쓰기 성공"은 애플리케이션이 믿고 지나갑니다. 다른 멤버가 master가 되면 그 쓰기는 사라질 수 있고, 아무도 모릅니다.
- 짧은 "연결 실패"는 애플리케이션이 알고 재시도할 수 있습니다.

그래서 잘못된 성공보다 짧은 실패를 택했고, 막혀 있던 시간은 숨기지 않고 공개합니다.

근거: [ADR-0005](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md)

## 3. 공식 operator보다 쓰기 중단이 왜 더 긴가요?

master Pod를 지운 첫 시험에서 쓰기 중단은 공식 operator가 12.4초, 저희가 22.0초였습니다.
저희는 새 Pod가 확인될 때까지 쓰기 경로를 닫아 두기 때문입니다.

로그로 나눠 보면 이렇습니다.

- **확인 단계: 약 12초.** 격리 시작부터 primary 확정까지입니다. 10초 간격으로 두 번 확인하는 안전 규칙이라 유지합니다.
- **Broker 재기동: 12–17초.** 확정 뒤 Broker Pod를 0개에서 다시 띄우는 시간입니다.

두 번째 단계는 줄일 수 있다고 보고 이슈로 올렸습니다. 다만 Broker를 0개로 줄이는 이유가 이미 열린 세션까지 끊는 데 있습니다.
그래서 그 보장을 지키면서 줄이는 방법을 검토하고 있습니다.

근거: [#1161](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161),
[비교 실행](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122)

## 4. 공식 operator와의 비교는 공정한가요?

같은 조건으로 시험했습니다.

- 같은 VM 랩, 같은 HA 3멤버 구성이었습니다.
- 같은 클라이언트가 트랜잭션마다 한 행씩 썼습니다.
- 같은 장애를 냈습니다: 쓰기 중 master Pod 강제 삭제, 두 번 연속.

한계도 있습니다.

- **수동 단계.** 공식 operator는 문서상 DB 생성·HA 시작·Broker 시작을 사용자가 하게 되어 있어서, 그 단계는 제가 손으로 했습니다.
- **재합류.** 첫 삭제 뒤 지워진 멤버도 자동으로 돌아오지 않아 손으로 다시 붙였습니다.
- **두 번째 장애의 원인.** 공식 operator가 Pod 목록이 바뀔 때마다 `ha_node_list` 순서를 바꿔 쓰는 바람에, 멤버들이 서로 다른 우선순위 목록을 갖게 됐습니다. 그 결과 새 master가 뽑히지 않았고, 31분 뒤 시험을 정리할 때까지 쓰기가 막혀 있었습니다.
- **저희가 괜찮았던 이유.** 저희 Operator는 `ha_node_list`를 클러스터 스펙만으로 StatefulSet 순번대로 만들고, ConfigMap 하나로 모든 멤버에 줍니다. Pod가 교체되거나 master가 옮겨도 순서가 바뀌지 않아, 남은 멤버들이 같은 우선순위로 새 master를 뽑았습니다(ADR-0001·ADR-0004, `internal/controller/haconfig.go`). 삭제된 멤버도 사람 손 없이 같은 설정으로 돌아옵니다.
- **범위.** operator마다 두 번씩 실행했고, 네트워크 분할은 비교하지 않았습니다.

승인된 쓰기 손실은 두 operator 모두 0건이었습니다.
공식 operator의 0건은 동기 복제 설정(`sync:sync:sync`) 덕분일 가능성이 큽니다.

근거: [비교 실행 결과](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122),
[공식 operator](https://github.com/CUBRID/cubrid-operator)

## 5. "최대 73건 손실"은 무엇이고, Operator 책임인가요?

네트워크 분할 중에 CUBRID HA가 스스로 다른 멤버를 master로 올린 경우입니다.
11월 17–18일 VM 분할 5회에서 새 master에 13–73건이 없었습니다.

- **언제 생긴 손실인가.** Operator가 쓰기 경로를 닫기 전에 옛 master가 승인한 쓰기입니다.
- **Operator가 할 수 있는 일.** 승격은 Operator가 아니라 CUBRID가 결정합니다.
  Operator가 지키는 것은 "닫은 뒤에는 쓰기 승인 0건"입니다. 닫기 전 손실은 엔진 동작의 한계로 공개합니다.

11월 25일 같은 조건의 재실행에서는 손실이 없었습니다. 그래서 재현 조건을 계속 추적하고 있습니다.

근거: [#702](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/702),
[#115](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/115)

## 6. 데이터 손실 0을 보장하나요?

아닙니다. 보장하는 것과 보장하지 않는 것을 나눕니다.

- **보장합니다.** 쓰기 경로를 닫은 뒤에는 새 연결이든 이미 열린 세션이든 쓰기 승인이 0건이어야 합니다.
  이것은 v0.1에서 반드시 통과해야 하는 안전 규칙입니다.
- **보장하지 않습니다.** 닫기 전에 승인된 쓰기가 새 master에 없을 수 있습니다.
  이것은 측정해서 조건과 함께 공개합니다. 복제 지연 뒤 VM 전원 차단에서 13건, 분할에서 최대 73건이 그 예입니다.

## 7. Patroni나 CloudNativePG처럼 Operator가 master를 정하면 되지 않나요?

PostgreSQL 쪽은 Operator나 Patroni가 합의 저장소를 써서 leader를 직접 정합니다.
CUBRID HA는 엔진이 heartbeat로 master를 스스로 선출합니다.
그래서 저희 Operator는 master를 고르지 않습니다. 할 수 있는 일은 둘입니다.

- 누가 master인지 확인합니다.
- 확신할 수 없으면 쓰기 경로를 닫습니다.

엔진의 선출을 바꾸는 것은 v0.1 범위 밖이고, Operator 쪽에서 가능한 한계는 따로 정리하고 있습니다.

근거: [ADR-0005](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md),
[#994](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/994)

## 8. 검증이 찾은 결함은 왜 Kind에서 안 잡혔나요?

Kind의 기본 네트워크(kindnet)는 NetworkPolicy를 적용하지 않습니다.

- **원인.** CUBRID는 30초쯤 조용한 상대를 TCP 7번으로 생존 확인합니다.
  VM 랩은 정책을 실제로 적용해서, 그 패킷이 버려지고 연결이 끊겼습니다.
- **수정.** 멤버에서 Broker로 가는 7번만 허용했습니다.
- **확인.** 머지한 빌드로 랩 회귀를 통과했습니다. 멤버끼리는 이 확인이 오가지 않는다는 것도 캡처로 확인하고 이슈를 닫았습니다.

Kind만으로는 부족하고 실제 정책을 적용하는 환경이 필요하다는 근거이기도 합니다.

근거: [#1158](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158),
[#1159](https://github.com/cubrid-lab/cubrid-kubernetes-operator/pull/1159)

## 9. 클라우드 스토리지(CSI)에서도 되나요?

아직 검증하지 않았습니다. 지금 검증 범위는 node-local 스토리지입니다.
볼륨이 다른 노드로 따라가는 동작, 스냅샷, 크기 변경은 검증하지 않았고, 이 범위를 그대로 공개합니다.

## 10. v0.1은 언제, 어떤 조건으로 나오나요?

목표는 12월 27일이지만, 필수 증거가 모두 모여야 하는 조건부입니다.

| 날짜 | 단계 |
|---|---|
| 11월 29일 | 복구·안전성 Go/No-Go 체크포인트 |
| 12월 7일 | 후보 동결: 소스·이미지·엔진·랩을 하나로 고정 |
| 12월 8–14일 | 필수 시나리오 반복과 24시간 soak |
| 12월 15–20일 | 작성자가 아닌 메인테이너가 문서만 보고 설치·복구·복원 재현 |
| 12월 21–27일 | 공개 판단. 필수 증거가 빠지면 공개하지 않습니다 |

근거: [CONTRIBUTING · v0.1 일정](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/CONTRIBUTING.md)

## 11. 장애 중 시간은 얼마나 걸리나요?

조건마다 측정값으로 공개합니다.

| 조건 | 측정값 |
|---|---|
| VM 전원 차단 | 차단 표시 뒤 첫 쓰기까지 26–38초 (3회) |
| master Pod 강제 삭제 (VM 랩 비교) | 쓰기 승인 사이의 최대 공백 22.0초, 32.8초. 두 번째 삭제 후 격리 뒤 첫 쓰기 승인은 +42.5초 |
| master Pod 정상 종료 | 쓰기 경로가 28초 닫힘 (불필요한 격리, 원인 공개) |
| 볼륨 재구축 (Kind) | 요청부터 완료 40.2초, 행 확인 48.9초 (v0.1 제한 5분) |

근거: [#1003](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1003),
[#938](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/938)

## 12. 누가 쓸 건가요? 수요는 확인했나요?

CUBRID를 Kubernetes에서 운영하려는 DB 운영자와 플랫폼 팀을 생각합니다.
장애 때 "지금 누가 master인지, 써도 되는지, 데이터가 남았는지"를 사람이 일일이 확인하지 않게 하는 것이 목표입니다.
수요를 검증했다고 할 단계는 아닙니다. v0.1 공개 뒤 사용자 피드백으로 다음 우선순위를 정합니다.

## 13. 28초 중단은 롤링 업데이트 때마다 반복되나요?

측정하지 않았고, 아래는 코드에서 확인한 내용입니다.

- **slave 교체.** Operator의 롤링 업데이트는 slave만 한 번에 하나씩 자동으로 교체합니다.
- **master 교체.** master만 남으면 `MasterUpdatePending`으로 멈추고, master Pod는 자동으로 지우지 않습니다.
  계획된 switchover는 아직 없어서, master를 교체하려면 사람이 master Pod를 정상 종료해야 합니다.
- **결론.** 그 경로는 28초 중단이 기록된 경우(#938, Kind)와 같은 경로라, 같은 중단이 생길 것으로 예상합니다.
  slave 교체만으로 격리가 걸리는지는 측정하지 않았습니다. 그래서 "업데이트 때도 같은 중단"이라고 발표에서 단정하지 않습니다.

근거: [`rollingplan.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/internal/controller/rollingplan.go),
[ADR-0009](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0009-update-vs-upgrade.md),
[ADR-0012](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0012-voluntary-disruption.md),
[#938](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/938)

## 14. 부록 21쪽 그래프에서 삭제 직후 주황 선이 튀는 구간의 쓰기는 누가 승인했나요?

CUBRID가 새로 올린 master(`ha-0`)가 승인했고, 그 쓰기는 하나도 사라지지 않았습니다.
11월 25일 두 번째 삭제(지운 Pod는 그 전 master `ha-1`) 기록입니다. 시각은 삭제 시점 기준입니다.

| 시각 | 일어난 일 |
|---|---|
| +0.9초 이전 | 쓰기 3건 승인. 지운 `ha-1`의 프로세스가 아직 멈추기 전입니다 |
| +0.9 – 2.3초 | 연결 오류 5건 (`CAS did not answer`). 옛 master로 가던 연결이 끊겼습니다 |
| +2.5 – 9.6초 | 쓰기 68건 승인. +2.4초 관측에서 master는 `ha-0` 하나뿐이었고, 읽기-쓰기 Broker도 아직 열려 있었습니다 |
| +9.7초 | 기존 연결이 끊깁니다. 이후 Broker가 0개라 접속 실패입니다 |

- **누가 받았나.** 새 master는 CUBRID가 스스로 올렸습니다. Operator는 지워진 멤버의 새 Pod를 아직 확인하지 못해 격리를 걸었고, 그게 +9.7초입니다.
  그래서 튀는 구간은 "CUBRID 승격 뒤, Operator가 길을 닫기 전" 구간입니다. #1161은 격리 해제 뒤 Broker를 다시 띄우는 시간을 줄이는 제안입니다.
- **사라졌나.** 시험이 끝난 뒤 새 연결로 읽은 최종 master(`ha-0`)에 이 구간의 승인된 쓰기가 모두 있었습니다. 손실은 0건입니다.
- **한계.** 클라이언트는 행마다 어느 서버가 받았는지 기록하지 않았습니다. 그래서 +0.9초 이전 3건이 옛 master에서 승인됐다는 것은 시각으로 추정한 것입니다.
  그래프의 2초 평균값이 평소보다 높은 것은 끊긴 연결을 다시 열면서 대기 중이던 요청이 몰린 결과로 보이지만, 따로 측정하지는 않았습니다.

근거: [비교 실행](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122),
[#1161](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161)

## 16. 표에 요약한 것 외에 1차에서 어떤 의견이 있었나요?

- **자동 재조정과 운영자 개입.** v0.1에서 보여줄 대표 사례는 쓰기 격리, 근거 확인 후 해제, 운영자 승인 후 볼륨 재구축입니다. 반복 실패 알림과 재시도 기준은 이 발표에서 운영 검증을 완료했다고 설명하지 않습니다.
- **인증과 운영 범위.** Instance Manager 토큰 교체는 공개 후보의 인증 검증 항목입니다. DB 인증, TLS와 버전 업그레이드를 동일한 검증으로 간주하지 않습니다. 공개 시 지원 범위와 미검증 조건을 문서에 명시합니다.
- **다른 Operator와의 비교.** 이번 비교는 공식 CUBRID Operator와 같은 강제 삭제를 실행한 관측입니다. PostgreSQL 계열의 격리 방식은 후속 비교 후보이며, 제안에 나온 차단 시간과 저장소 동작은 이번 시험에서 확인하지 않았습니다.
- **복원 증거.** 1차의 판정 보류 건은 성공 수에 넣지 않습니다. 공개 후보에서는 새 클러스터 복원과 데이터 대조, 변조·누락된 백업 거부를 함께 확인합니다. 규제 충족 여부는 이번 발표의 검증 범위 밖입니다.

근거: [공개 후보 검증](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126), [로드맵](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md)

## 17. 첫 버전 이후 어떤 기능을 검토하나요?

기존 데이터로 자동 재합류하는 기능, 기존 볼륨을 새 클러스터에서 이어받는 기능, 아카이브 로그 공간 관리, DB 상태 관측과 쓰기 차단 판단을 분리하는 설계를 검토합니다. 시험 결과와 도입 피드백을 보고 우선순위를 정합니다.

근거: [Operator 로드맵](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md)
