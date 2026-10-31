# 질의응답 준비

문장 수정: 2026-10-27 · 시험 결과 기준: 2026-10-20 (복원 결과만 2026-10-25).
질문이 나오면 참고할 답변입니다. 출처와 정확한 시험 환경은 [SOURCES.md](SOURCES.md)에 모았습니다.

## 1. 누가 쓸 건가요? 수요는 확인했나요?

처음에는 CUBRID DB 운영자와 Kubernetes 플랫폼 팀을 생각하고 있습니다. 장애가 나면
누가 master인지, 데이터가 남아 있는지, 실제로 읽고 쓸 수 있는지를 함께 확인해야 하기
때문입니다. 아직 수요를 검증했다고 할 단계는 아닙니다. 운영자들이 실제로 어떤 확인에
시간을 쓰는지 듣고 우선순위를 잡으려고 합니다.

## 2. 공식 CUBRID Operator가 있는데 왜 따로 만드나요?

공식 Operator도 HA 상태를 보고 스토리지와 예약 백업을 관리합니다. 차이는
구조와 운영 작업 처리 방식에 있습니다. 공식 Operator는 CUBRID DB Pod 안에서
CMS와 Broker를 함께 실행하고, CMS API 및 `pods/exec`로 관리합니다.
저희는 DB Pod 안의 IM API로 관리 작업을 요청하면서 작업 ID와 상태를 PVC에 기록하고,
RW/RO Broker는 별도 Deployment로 분리했습니다.

또한 공식 Operator는 처음 성공한 CMS 응답을 활용하지만, 저희는 각 멤버의 최신 관측값을
종합해 master가 불분명하면 미확정으로 남깁니다. 두 구조 모두 CUBRID 자체 HA를 이용합니다.
현재는 구조적 차이만 확인했으며, 실제 안전성·성능 우위는 아직 입증하지 못했습니다.
CMS 기능을 재사용하거나 공식 Operator에 개선사항을 기여하는 방향도 비교 대상으로 열어두고 있습니다.

출처: [공식 Operator 소스](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e).

## 3. 지금 어디까지 돌아가나요?

발표에서 소개한 버전의 Kind 테스트 27개가 통과했습니다. VM Kubernetes에서도 SQL
접속과 HTTP 연결 제한을 시험했습니다. 기존 demo·HA를 순차 교체한 뒤, 확인한 행과
타임스탬프가 남아 있고 RW로 쓴 행이 RO에서 보이는 것, RO 쓰기가 거부되는 것을 봤습니다.

27개는 테스트 spec 수입니다. 필수 시나리오 S00–S15를 전부 통과했다는 뜻은 아닙니다.

출처: [Kind 실행](https://github.com/cubrid-lab/cubrid-kubernetes-operator/actions/runs/39348551910),
[VM 결과](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281421472).

## 4. VM에 장애가 나도 괜찮나요? 바로 운영에 쓸 수 있나요?

그렇게 말씀드리기는 아직 이릅니다. VM에서 SQL이 되는 것까지 확인했지만 전원을 끄거나
네트워크를 갈라보는 시험은 더 해야 합니다. 현재 VM은 local-path를 사용하므로 CSI도
별도로 확인해야 합니다. 전체 필수 시나리오와 장시간 부하 시험도 남아 있습니다.

현재는 experimental입니다. 기존 pycubrid 클러스터도 데이터가 보이는 상태를 확인하는
중이라 이미지 갱신을 보류했습니다.

## 5. Operator가 master를 정하나요? split-brain은 어떻게 다루나요?

master 전환은 CUBRID HA가 합니다. Operator는 그 결과를 보고 Kubernetes 리소스와 작업을
관리합니다. 멤버 0을 항상 master로 두지 않고, 응답이 없거나 역할 정보가 모순되면 master를
확정하지 않습니다. 갈라진 데이터 중 하나를 골라 덮어쓰지도 않습니다.

다만 상태를 불명확하다고 표시하는 것과 쓰기를 막는 것은 다른 일입니다. 네트워크가
갈라졌을 때 새 연결과 기존 연결에서 쓰기가 어떻게 되는지 확인하고, 차단과 해제 정책을
구현·시험해야 합니다. 정상 RO 접속에서 쓰기가 거부됐다는 결과만으로는 부족합니다.

출처: [ADR-0005](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0005-failover-split-brain.md),
[쓰기 격리 #113](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/113).

## 6. 데이터 손실이나 복구 시간을 보장하나요?

지금은 RPO나 RTO를 보장할 수 없습니다. 데이터가 남아 있었다는 결과도 시험에서 확인한
행에 대한 것입니다. 실제 장애를 내고, 성공 응답을 받은 쓰기가 데이터에 남아 있는지
비교해야 합니다. 실패한 요청과 결과를 알 수 없는 요청도 따로 기록해야 합니다.

HA 초기 복사나 백업 업로드 시험과 실제 CubridBackup으로 새 클러스터를 복원하는
전체 시험도 구분합니다. 10월 25일 VM에서 새 클러스터 복원을 일곱 번 시험했고
다섯 번 통과했습니다. 두 번은 데이터 확인까지 마친 뒤 복원된 노드의 세션이 끊겨
판정을 보류했고, 원인은 아직 모릅니다. 초기 시험 결과일 뿐이라 반복과 중단 상황까지
확인해야 복구가 됐다고 말할 수 있습니다.

## 7. 인증이나 암호화는 어디까지 되나요?

IM API에는 bearer 인증이 있습니다. DB 접속 인증이나 TLS와는 별개입니다. 발표 기준
코드에서는 DBA 암호가 비어 있고 통신도 암호화되지 않습니다. NetworkPolicy 역시 실제
네트워크 플러그인이 강제하는지 확인해야 합니다.

지원하는 환경과 이런 제약은 첫 버전의 문서에 함께 적으려고 합니다.

출처: [네트워크·보안 안내](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md#network-access).

## 8. 12월 27일에는 무엇을 공개하나요? 늦어지면요?

CUBRID 11.4.x/amd64, Kubernetes와 CSI 한 구성에서 설치·HA·RW/RO·장애 복구를 시험한
v0.1이 목표입니다. 쓰기 격리와 재합류, 재구축, 백업에서 새 클러스터로 복원하는 것도
필수입니다. 이미지와 설치 파일, 운영·복구 문서, 시험 결과를 같이 공개하려고 합니다.

11월 29일까지 필수 시나리오를 한 번씩은 전부 통과시키고, 12월에는 같은 RC로 장애를
반복하며 24시간 부하와 다른 사람의 문서 재현을 해보려 합니다. 12월 27일은 목표 날짜입니다.
필수 안전 조건이 남아 있으면 그 상태를 그대로 알리고, 공개 여부는 시험 결과로 판단하겠습니다.

출처: [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md).

## 9. 두 사람은 어떻게 나눠서 일하나요?

최영선과 백경준이 함께 개발합니다. 이슈마다 담당자를 정하고, 맡은 사람이 문제 재현부터
코드·테스트·문서·실험 기록까지 준비합니다. 다른 한 사람은 코드와 결과를 리뷰합니다.
공유 VM 장애 시험은 한 번에 하나씩 합니다. 릴리스 전에는 작성자가 아닌 사람이 문서만
보고 설치와 복구를 끝낼 수 있는지도 확인하겠습니다.

## 10. 이번 자리에서 어떤 도움을 받고 싶나요?

최근 장애에서 무엇을 먼저 확인했는지, 어떤 결과를 보고 복구됐다고 판단했는지 듣고
싶습니다. 첫 시험 환경으로 쓸 Kubernetes와 CSI 조합, 스토리지나 장애 시험에서 주의할
점도 필요합니다. 12월에는 설치·복구 문서를 따라 해보고 막히는 곳을 알려주실 분을 찾습니다.

## 11. v0.1을 내고 나면 무엇을 하나요?

우선 써보면서 불편한 곳을 고치려고 합니다. 로그로 원인을 찾을 수 있는지, 복구 절차를
따라갈 수 있는지부터 보고 DB 인증과 TLS, 호환 업데이트도 검증해야 합니다. 그다음에는
Kubernetes·CSI 조합을 늘리되 각 환경에서 장애와 복구를 다시 시험하겠습니다.

arm64와 여러 가용영역, CUBRID 버전 변경, master로 승격되지 않는 읽기 복제본도 길게 보고
있습니다. 후속 버전과 일정은 아직 정하지 않았습니다. v0.1의 필수 작업을 끝내고 실제로
써본 분들의 의견을 받아 다음 순서를 정하려고 합니다.

## 12. 16개 장애·복구 시나리오는 무엇이고, 실제로 어떤 문제가 발견됐나요?

v0.1 필수 검증 시나리오 S00–S15는 설치와 정상 복제, Master Pod 및 VM 장애,
Broker/Operator 장애, 네트워크 분할·복제 지연, 재합류·PVC 재구축, 백업·복원,
데이터 보존·인증·노드 점검을 포함합니다. CUBRID 공식 매뉴얼·CTP와
CloudNativePG·Percona·Crunchy의 시험 구성을 검토하되, 장애 주입 성공 확인과
실제 SQL·커밋 이력·각 멤버 데이터 비교를 우리 프로젝트의 검증 계약으로 정의했습니다.

실제 Kind 시험에서는 Master 상태가 미확정인데 RW 쓰기 성공 응답이 나왔습니다.
별도의 CUBRID 엔진 수동 POC에서는 네트워크 분할 중 두 Master가 서로 다른 데이터를
가진 것을 관찰했습니다. 일부 실험에서는 Slave가 존재해도 복제 적용이 중단되는
문제가 확인됐습니다. 이 근거의 시험 수준을 구분해야 하며, 전체 S00–S15를 통과한 것은 아닙니다.

출처: [시나리오 계약](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md),
[외부 참고·출처 기록](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/upstream-scenarios.md),
[ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md),
[엔진 POC](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/poc/RESULTS.md).
