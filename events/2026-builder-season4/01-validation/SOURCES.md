# First-validation presentation — sources

Presentation expanded on **2026-10-22 (KST)** to 18 slides per language and reordered to 15 on **2026-10-28** (#75), then given an agenda slide (16) on **2026-10-29**; execution evidence remains fixed to **2026-10-20**, except the VM-lab backup and new-cluster restore runs of **2026-10-25** (now slides 8 and 14). The main deck follows the seven items in the supplied
Builder notice. Detailed source checks stay here and in speaker notes rather
than becoming extra presentation sections.

## Agenda and timing

| Announced requirement | Slides | Planned seconds |
|---|---|---|
| 1. Project and team (cover), agenda and the four project goals | 1–3 | 80 |
| 2. Problem and initial users | 4 | 40 |
| 3. Existing approaches and open-source comparison | 5 | 50 |
| 4. Proposed solution: four checks after a fault, unresolved-master rule, recorded evidence | 6–8 | 120 |
| 5. Architecture draft: full architecture, control loop and data flows, inside the Operator | 9–11 | 125 |
| 6. Roadmap, responsibilities, v0.1 gates and scope, later direction | 12–16 | 165 |
| 7. Discussion topics and questions | 17 | 15 |
| **Total** | **17 slides per language** | **595 + 5 seconds buffer** |

The announced presentation limit is ten minutes plus separate ten-minute Q&A. Times are planning targets, not a rehearsal measurement.
The expanded material deliberately separates hypothetical incident stories, user hypotheses, source comparison, executed evidence and work not yet proven.

## Inspected technical sources

- Operator main: [`39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb).
- Operator main for the 2026-10-25 restore records: [`4ac13fd4d3a37e04007d947568a63ae6e6b49ff6`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/4ac13fd4d3a37e04007d947568a63ae6e6b49ff6) (ROADMAP only; the runs used manager `d6df2ac`).
- Official Operator: [`fa7b6c2cf26096769c4404a2e2bb683f3872aa1e`](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e).
- Visual basis: the existing [contest source](../../../presentation/decks/2026-ossdevcon/slides.md) and [shared styles](../../../presentation/style.css). Only the typography/color/layout vocabulary is reused; Python ecosystem achievements are not Operator evidence.

## Claim map

| Slides | Evidence basis | Claim boundary |
|---|---|---|
| 1, 3–4 | [Operator README](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md), [DESIGN](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md) | Recovery scenario is illustrative, not a customer incident. Initial target users are hypotheses, not proven adoption/interviews |
| 6, 9–11 | [Architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture) and [Broker flows](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture) | CUBRID owns HA promotion. IM is integrated in DB container; Operator never proxies SQL |
| 7 | [Fault-safety ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0005-failover-split-brain.md), [write-quarantine issue](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/113) | Reported unknown master is not automatic RW write isolation; mandatory work remains |
| 5 | [Official pod StatefulSet](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/pkg/manager/statefulset_manager.go#L129-L140), [CMS access](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/cms-access.en.md), [Lab IM ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0003-instance-manager.md), [Lab Broker ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0002-broker-routing.md) | Official: CUBRID DB, CMS and Broker in the same DB Pod; Lab: IM integrated into the DB container and RW/RO Brokers in separate Deployments. Diagram simplifies one repeating DB Pod out of three. These are topology differences, not proven reliability gains. |
| 5 | [Official README](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/README.md), [status controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L68), [backup controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/backupdb_controller.go#L317) | Upstream already has HA observation, storage and scheduled backup. Comparison is source-level, not field reliability benchmarking |
| 8, 14 | [Kind, VM and rollout records](#recorded-execution-evidence), [v0.1 gates](#evidence-boundaries-retained-in-the-notes) | Kind 27/27 specs, VM SQL and the first S12 restore passes are not completed S00–S15 fault/restore certification |
| 12, 15 | [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md); the 24-hour load target is from [final integration issue #95](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/95) ("initial target of 24 hours") | Nov 29 full first pass, Dec 27 candidate release are goals, not passed or promised milestones |
| 13 | [CONTRIBUTING](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md) and team record below | Both are co-maintainers; per-issue owner and reviewer, no invented permanent feature assignment |
| 16 | [Post-v0.1 direction](#post-v01-direction) | Unsheduled proposal, not support or release commitment |
| 17 (speaker note) | Builder validation notice | Discussion: incident criteria, the first CSI driver to support, independent runbook review |

## Recorded execution evidence

The source revision above is the deployed code selection, not a claim that every
mandatory release scenario passed. The observations below were recorded on
2026-10-20; later edits to main do not change their source revision. The last
row, added on 2026-10-26, is the VM-lab restore record of 2026-10-25 as
the pinned ROADMAP above states it.

| Evidence | Exact result and boundary |
|---|---|
| [Kind E2E run 39348551910](https://github.com/cubrid-lab/cubrid-kubernetes-operator/actions/runs/39348551910) | 27/27 specs passed on reviewed head `f12632473de9e91e6b65e44444b4cf622d0caf43`, subsequently merged as `39b1cb6`. Spec count is not the number of S00–S15 scenarios. |
| [Development Images run 39353186855](https://github.com/cubrid-lab/cubrid-kubernetes-operator/actions/runs/39353186855) | Published the selected main commit; manager `sha256:24706be69f034c5f67e3518b1df76b5c9066665ec63550a19875c621a0aaf880`, IM `sha256:49ace1f424586811ae852b0376abb8418ca00080cc4bf425998d8ed3af1fde45`. |
| [VM connection / HTTP record](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281330433) | Fresh LAB00 SQL and bounded HTTP checks passed on Kubernetes `v1.36.5+k3s1`, CUBRID `11.4.6.1963`, four Ready VM nodes and local-path storage. LAB00 is an installed connection lane, not S00 installation or VM power-loss validation. |
| [VM rollout / SQL record](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281421472) | Demo/HA rollout retained seven original DB PVC/PV identities, known rows/timestamps and post-rollout RW/RO behavior. These checks do not guarantee arbitrary dataset recovery. The separate pycubrid upgrade remained held; it is not counted as an updated cluster. |
| [VM-lab restore into a new cluster (scenario S12)](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/4ac13fd4d3a37e04007d947568a63ae6e6b49ff6/ROADMAP.md?plain=1#L159-L194), [#572](https://github.com/cubrid-lab/cubrid-kubernetes-operator/pull/572), [#573](https://github.com/cubrid-lab/cubrid-kubernetes-operator/pull/573) | On 2026-10-25 S12 `exact` restored S11's real backup into a new cluster seven times on the VM lab (manager `d6df2ac`, `local-path`): five passed and two were blocked, not failed, by a `csql` session lost on a restored member after the data checks had held ([#238](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/238), cause unknown). S12 `tampered`, a copy with one changed byte, was refused with a checksum mismatch in both runs that reached it. Interrupted restores (other than the lab-only Operator restart), an Instance Manager restart and the Operator's logs are not covered; this is a first pass, not repeated qualification. |
| [Write quarantine #113](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/113), [unknown HA observation #438](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/438) | Both remain open at this source check. Normal RO write rejection is not partition-time RW quarantine; a later passing Kind run does not identify the earlier unknown-HA cause. |

The timeline's **November 29 first mandatory-scenario pass** and **December 27
v0.1 release** are targets consistent with the pinned ROADMAP stages. December
is reserved for candidate/repeat/soak/regression and runbook checks; no mandatory
safety gate is dropped to meet the dates.

### The 27 Kind E2E specs (slide 10)

Slide 10 lists every spec that passed in [Kind E2E run 39348551910](https://github.com/cubrid-lab/cubrid-kubernetes-operator/actions/runs/39348551910)
("Ran 27 of 27 Specs", head `f126324`), grouped into ten areas. The test text below is
from the run log, shortened where it repeats; the scenario column is the label in
the test itself. A label means the spec checks part of that scenario in Kind. It
does not mean the scenario is complete: S04, S07–S13 and S15 have no Kind spec here, and
S00–S15 completion is still the November target.

| # | Slide group | Spec (from the run log) | Test file at `f126324` | Scenario label |
|---|---|---|---|---|
| 1 | Operator basics | Manager should run successfully | [`e2e_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/e2e_test.go#L130) | — |
| 2 | Operator basics | Manager should ensure the metrics endpoint is serving metrics | [`e2e_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/e2e_test.go#L162) | — |
| 3 | Single database | S00 standalone cluster becomes Ready as a non-root Pod and answers SQL | [`s00_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s00_test.go#L220) | S00 |
| 4 | Single database | S00 standalone cluster keeps the data when the Pod is deleted | [`s00_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s00_test.go#L263) | S00 |
| 5 | Wiring, no database | Fake Instance Manager: reaches every member by its alias Service and resolves the primary | [`e2e_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/e2e_test.go#L371) | — |
| 6 | Wiring, no database | Fake Instance Manager: follows a role change that changes no Kubernetes object | [`e2e_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/e2e_test.go#L402) | — |
| 7 | HA setup | creates the database on one member only | [`ha_bootstrap_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/ha_bootstrap_test.go#L356) | — |
| 8 | HA setup | seeds the other members, which join as slaves | [`ha_bootstrap_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/ha_bootstrap_test.go#L371) | — |
| 9 | HA setup | replicates a row written on the master to both slaves | [`ha_bootstrap_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/ha_bootstrap_test.go#L403) | — |
| 10 | HA setup | serves SQL through the read-write and the read-only Service | [`ha_bootstrap_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/ha_bootstrap_test.go#L422) | — |
| 11 | HA setup | holds what a recorded workload was told, on both Services | [`ha_bootstrap_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/ha_bootstrap_test.go#L459) | — |
| 12 | HA setup | reports the cluster Ready with the master as primary | [`ha_bootstrap_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/ha_bootstrap_test.go#L519) | — |
| 13 | HA behavior | has one master and two slaves, and accepts writes only through the read-write Service | [`s01_s02_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s01_s02_test.go#L313) | S01 |
| 14 | HA behavior | replicates rows, schema changes and rollbacks, also to a replaced slave | [`s01_s02_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s01_s02_test.go#L357) | S02 |
| 15 | Master Pod deleted | graceful: one member is master again after the master Pod is deleted, and no acknowledged write is lost | [`s03_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s03_test.go#L378) | S03 |
| 16 | Master Pod deleted | abrupt: same check after an abrupt delete | [`s03_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s03_test.go#L378) | S03 |
| 17 | Master Pod deleted | abrupt-first-member: same check when the first member is the master | [`s03_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s03_test.go#L378) | S03 |
| 18 | Broker failure | broker-process: clients recover from a Broker failure, and it causes no database failover | [`s05_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s05_test.go#L166) | S05 |
| 19 | Broker failure | one-broker-pod: same check after one Broker Pod is deleted | [`s05_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s05_test.go#L166) | S05 |
| 20 | Broker failure | all-rw-brokers: same check with every RW Broker down | [`s05_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s05_test.go#L166) | S05 |
| 21 | Operator failure | restart: SQL is not interrupted and no member is restarted when the Operator Pod is killed | [`s06_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s06_test.go#L157) | S06 |
| 22 | Operator failure | absent-during-failover: CUBRID fails over without the Operator, which reports the new master when it returns | [`s06_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s06_test.go#L163) | S06 |
| 23 | Replication faults | reports a slave that looks healthy and applies nothing, and no longer after its Pod is replaced | [`replication_stall_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/replication_stall_test.go#L50) | — |
| 24 | Replication faults | restarts the container of a member whose CUBRID processes were stopped | [`replication_stall_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/replication_stall_test.go#L291) | — |
| 25 | Instance Manager auth | the Instance Manager refuses a caller without the token, and the token is not shown anywhere | [`s14_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s14_test.go#L114) | S14 |
| 26 | Instance Manager auth | token-rotation: the operator reaches every member through a token rotation, and the old token is refused once every member was replaced | [`s14_token_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s14_token_test.go#L327) | S14 |
| 27 | Instance Manager auth | token-migration: a token Secret without a rotation time is moved to a new token without a member refusing the operator | [`s14_token_test.go`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f12632473de9e91e6b65e44444b4cf622d0caf43/test/e2e/s14_token_test.go#L333) | S14 |

## Team and role record

On 2026-10-15 the repository collaborator metadata identifies `yeongseon` and
`paikend` as the two repository administrators. Their public profiles identify
[Yeongseon Choe](https://github.com/yeongseon) and
[Paik Gyeongjun (Kent)](https://github.com/paikend). The existing contest cover
records the Korean names **최영선 · 백경준**. These identities were checked rather
than inferred from commit authorship alone.

The deck presents both as co-maintainers. It makes the per-change owner/reviewer contract concrete from [CONTRIBUTING](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow): the assigned implementer supplies reproduction, implementation, tests, documentation and execution evidence; the other maintainer reviews it. Fixed individual feature ownership is unconfirmed and is not invented. Shared-lab experiments are serialized, and non-author reproduction remains release acceptance.

## Evidence boundaries retained in the notes

- The project is experimental, not production-ready.
- The exact Kind and VM results above are existing recorded executions, not
  new database runs performed while editing the presentation. Neither proves
  zone or broad-platform behavior.
- ROADMAP records RW writes continuing while primary/routing Conditions were
  unresolved. SQL quarantine enforcement remains open; recovery design is
  not evidence that integrated rejoin/rebuild has passed. The 2026-10-25
  new-cluster restore runs are a first pass, not repeated qualification.
- IM bearer authentication is separate from database authentication/TLS. The
  pinned README records no traffic encryption and empty DBA passwords; the
  slides do not claim production security.
- Required first-release work still includes authenticated non-root lifecycle,
  3-node CUBRID HA/RW/RO, Pod/VM/Broker/Operator faults, write quarantine,
  rejoin/rebuild, backup/new-cluster restore, retention/auth/disruption policy,
  truthful observability and reproducible S00–S15 evidence.
- Compatible updates and disk-full testing remain conditional. Engine-version
  migration, non-promotable replicas and broader platform/zone support remain
  outside the initial scope.
- Final speaking rehearsal, PowerPoint desktop review and submission are not
  claimed by a successful browser or export check.

## Comparison boundaries

Slide 5 compares inspected implementation models, not every upstream feature or deployed reliability. Source inspection was repeated against the same two pinned revisions for this content revision.

| Claim | Primary source and boundary |
|---|---|
| Official HA status uses the first successful CMS response's node view | [status controller, lines 63–110](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L63-L110). The project already supports HA observation. |
| Our primary decision aggregates expected-member observations and leaves missing/conflicting evidence unresolved | [resolution inputs](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/haresolve.go#L36-L105), [decision](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/haresolve.go#L189-L235). This does not itself stop SQL writes. |
| Official backup uses scheduling, Pod exec and persisted per-Pod status | [execution/status](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/backupdb_controller.go#L317-L345), [API](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/api/v1/backupdb_types.go#L23-L54). Do not say it has no backup persistence or recovery support. |
| The official Operator has no restore workflow | The [source tree](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e) at `fa7b6c2` (still the head of `develop` on 2026-10-28) has BackupDB types, controller, webhook and `backupdb.sh` only: no restore CR, controller, script or document. Slide 6 says "no restore feature found in the source", not that recovery from its backups is impossible. |
| Our IM has a PVC-durable operation protocol; interrupted operations become Failed on restart | [opstore](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/instancemanager/opstore.go#L57-L120). Durable identity is not automatic resumption or guaranteed completion. |
| Our backup target/request identity is recorded; restore verifies manifest objects and targets a new cluster | [dispatch](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/cubridbackup_controller.go#L199-L207), [size/SHA-256 checks](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/instancemanager/restore.go#L347-L421), [restore ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0008-restore-semantics.md#L47-L79). New-cluster restore first passed on the VM lab on 2026-10-25 (see above); repeated and interrupted restores remain a required verification gate. |
| Port/Ready observations and SQL validation differ in both projects | [official endpoint check](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/broker_endpoint_controller.go#L97-L111), [our TCP readiness](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/broker.go#L208-L216). Recorded VM SQL is separate evidence, not our readiness mechanism. |

Both projects observe periodically. Polling is not presented as a differentiator. The hypothetical recovery scenario is an explanation of a decision, not a newly discovered customer incident. No RTO/RPO reduction, adoption, comparative stability, most-caught-up-backup selection or universal recovery guarantee is claimed.

## Post-v0.1 direction

Slide 16 is a **direction proposal prompted by presentation feedback**, not an approved new release plan. The first version remains the required, bounded recovery qualification described by the pinned ROADMAP; no mandatory safety condition is moved to a later version.

1. Learn from independent installations and incident reproduction; improve failure diagnosis and operating procedures. Qualify DB authentication/TLS and compatible updates as adoption needs. These are not claimed supported today; IM authentication is distinct. Compatible updates remain conditional in v0.1 until their gates pass.
2. Expand Kubernetes/CSI coverage only with per-configuration recovery evidence. Consider arm64 and multi-zone tests separately; do not generalize single-lab results.
3. Investigate engine-version migration and additional replication topologies after the recovery foundation is established. These are explicitly future scope in the pinned ROADMAP.

Dates, version numbers, implementation order and supported-production status are not promised. The next bounded release scope follows v0.1 acceptance, maintainer decisions, available validation environments and actual user feedback.

## Spoken-copy revision

The 2026-10-21 wording revision keeps the same eleven slides,600-second budget, source revisions and execution evidence. Titles, captions and notes use concrete actors/actions instead of repeating abstract labels and disclaimers. Relevant limits remain beside the Kind/VM results, write-quarantine work, release/security scope and future plan. No interviews, personal incidents, fixed individual assignments, measurements or future dates were added.

The 2026-10-26 revision (slide numbers as they were before the 2026-10-27 revision) keeps the 18 slides, the 580-second plan and the
2026-10-20 Kind and VM rows. It adds the 2026-10-25 restore record to slide 12,
rewords the restore gate on slide 13 and the restore sentences in the notes of
slides 8, 12 and 13, and shortens the notes of slide 17 to its 20 seconds. The
slide 17 body is unchanged.

The 2026-10-27 revision follows a slide-by-slide review. It keeps the seven
announced items and the evidence above, and changes how they are shown:
slides 3 and 4 are merged into one (what Kubernetes monitoring shows and what
needs database knowledge); slide 4 shows the two teams as two people with
their own questions; slide 5 states why another Operator when an official one
exists, and slide 6 details the differences; repeated sentences, unexplained
abbreviations and internal scenario IDs are removed from the slides; every
title fits one line; slide 18 is a closing questions slide. Slide 5 says
recovery is *tested* with SQL and data, since both Operators use port checks
at runtime. The plan is 550 seconds with a 50-second buffer.

The 2026-10-28 restructure (#75) changes the order and the opening, not the
evidence. Slide 2 now says what the Operator is and does before any incident,
with each capability marked verified, built, or a v0.1 goal: 3-node CUBRID HA
with RW/RO and backup restore are verified by the Kind/VM records above; role
discovery is built (`DESIGN.md` section 11, implementation status), while RW
write blocking during faults is still not built or verified; rejoin and
rebuild are v0.1 goals; the backup restore chip says *partly verified*, since
the 2026-10-25 runs are not a repeated qualification. Slide 4 replaces the earlier two architecture slides
with one drawing from `DESIGN.md` sections 7 and 10: YAML → Kubernetes API →
Operator → resources; three CUBRID HA nodes (the Operator's per-node "members"), each with Instance Manager and PVC;
a separate RW/RO Broker tier behind the RW/RO Services, where RW Brokers find
the master themselves (ADR-0002), and the Operator never relays SQL and
does not pick the master during failover (ADR-0001, ADR-0005; on a restore it
bootstraps the first member as master, ADR-0008); and S3-compatible object storage for initial copy,
backup and restore. Slide 5 walks through a master Pod fault as a *designed*
flow and separates Pod availability (Kubernetes), DB HA state (CUBRID HA
switches, the Operator records it), SQL access (Broker) and data (checked by
E2E tests, not by the Operator). The official Operator comparison is one
slide (7) placed after the proposal. The claim map above uses the new
slide numbers; its rows and source boundary are
unchanged. The agenda slide and the old YAML-flow slide are removed. The plan
is 520 seconds with an 80-second buffer.

On 2026-10-29 the deck gained an agenda slide (2) whose five parts match the
section label at the top right of every slide. Slide 3 now states the four
project goals instead of a status table. Slide 8 compares the two Operators in
one table and links the official repository and its pinned source. Headlines
fit on one line, and wording was smoothed. Evidence, numbers and source
revisions are unchanged. The plan is 535 seconds with a 65-second buffer.

Later on 2026-10-29 the separate feedback slide was removed at the maintainer's
request. The Q&A slide (now 15) keeps the discussion topics in its speaker
note: what people check first after a fault and which CSI driver v0.1 should
support first. The plan returns to 520 seconds with an 80-second buffer.

The slides were then reordered to follow the six announced items in order:
project and team, problem, existing approaches, proposed solution, architecture
draft, and roadmap with the first version. The official Operator comparison moves
up to slide 5. The fault-check, safety and evidence slides (6–8) form the
proposed solution. The architecture draft keeps the component diagram (9) and
adds slide 10, which shows the control loop (desired state, reconcilers,
Instance Manager observation, status and Conditions) and the SQL, backup and
status data flows from DESIGN.md sections 7, 9, 15–16 and 18–19 as a designed
flow, not as verified behaviour. The plan is 560 seconds with a 40-second buffer.

Slide 9 then became one full architecture picture: the user and Kubernetes
API, the Operator with its reconcilers, observability output, the Kubernetes
resources it creates (StatefulSet, PVC, Secret, headless and per-member alias
Services, NetworkPolicy, Broker Deployment), the three CUBRID HA nodes with
their Instance Managers and roles, the application SQL path through RW/RO
Services and Brokers, and S3-compatible storage for initial copies and
backups. Its numbered operations arrows (1-4) match the control loop on
slide 10. The content follows DESIGN.md sections 7, 9, 10, 14-16, 18 and 19.

Slide 11 shows the inside of the Operator as the code stands at
[`986b775`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/986b77521a1a2fa2a9da5a3ccce4e5a0c0b2fdd7)
(2026-10-29). Two controllers run in one controller-runtime manager
(`cmd/main.go`). `CubridClusterReconciler` watches CubridCluster and owns
StatefulSets, Deployments, Services, ConfigMaps, Secrets and NetworkPolicies.
It reconciles them in order: headless and member Services, the Instance Manager
token Secret, HA configuration, NetworkPolicies, the StatefulSet. Then status
covers HA bootstrap, role reads and the master decision, restore bootstrap, the
update guard and rolling replacement, and the Broker tier
(`internal/controller/cubridcluster_controller.go`). `CubridBackupReconciler`
picks a target, starts a backup with an idempotency key, polls the operation and
records the result (`cubridbackup_controller.go`). Both call each Pod's Instance
Manager over HTTP with a bearer token (`roleprober.go`, `imclient.go`). The
Instance Manager endpoints are listed from `internal/instancemanager/server.go`.
Slides 9 and 10 now say "two controllers" instead of the design document's six
named reconcilers. The plan is 595 seconds with a 5-second buffer.

On 2026-10-31 the recorded-results slide (10) shows the 27 Kind E2E specs in ten groups (listed in
[The 27 Kind E2E specs](#the-27-kind-e2e-specs-slide-10)), so the audience can see
what "27 / 27" covers. The VM rollout and VM restore results move to one line each
below the list. Numbers, run IDs and boundaries are unchanged; the slide count
stays at 17 and its speaking time stays at 40 seconds.
