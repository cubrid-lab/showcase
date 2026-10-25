# First-validation presentation — sources

Presentation expanded on **2026-10-22 (KST)** to 18 slides per language; execution evidence remains fixed to **2026-10-20**. The main deck follows the seven items in the supplied
Builder notice. Detailed source checks stay here and in speaker notes rather
than becoming extra presentation sections.

## Agenda and timing

| Announced requirement | Slides | Planned seconds |
|---|---|---|
| 1. Project and team | 1 | 20 |
| Agenda | 2 | 15 |
| 2. Problem, recovery scenario and initial users | 3–5 | 100 |
| 3. Existing approaches and open-source comparison | 6–7 | 70 |
| 4. Proposal, recorded evidence and validation gaps | 8, 12–13 | 115 |
| 5. Components, data/control flow and write safety | 9–11 | 110 |
| 6. Roadmap, responsibilities, v0.1 and later direction | 14–17 | 125 |
| 7. Discussion topics | 18 | 25 |
| **Total** | **18 slides per language** | **580 + 20 seconds transition buffer** |

The announced presentation limit is ten minutes plus separate ten-minute Q&A. Times are planning targets, not a rehearsal measurement.
The expanded material deliberately separates hypothetical incident stories, user hypotheses, source comparison, executed evidence and work not yet proven.

## Inspected technical sources

- Operator main: [`39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb).
- Official Operator: [`fa7b6c2cf26096769c4404a2e2bb683f3872aa1e`](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e).
- Visual basis: the existing [contest source](../../../presentation/slides.md) and [shared styles](../../../presentation/style.css). Only the typography/color/layout vocabulary is reused; Python ecosystem achievements are not Operator evidence.

## Claim map

| Slides | Evidence basis | Claim boundary |
|---|---|---|
| 1, 3–5 | [Operator README](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md), [DESIGN](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md) | Recovery scenario is illustrative, not a customer incident. Initial target users are hypotheses, not proven adoption/interviews |
| 6–7 | [Official README](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/README.md), [status controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L68), [backup controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/backupdb_controller.go#L317) | Upstream already has HA observation, storage and scheduled backup. Comparison is source-level, not field reliability benchmarking |
| 8–10 | [Architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture) and [Broker flows](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture) | CUBRID owns HA promotion. IM is integrated in DB container; Operator never proxies SQL |
| 11 | [Fault-safety ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0005-failover-split-brain.md), [write-quarantine issue](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/113) | Reported unknown master is not automatic RW write isolation; mandatory work remains |
| 12–13 | [Kind, VM and rollout records](#recorded-execution-evidence), [v0.1 gates](#evidence-boundaries-retained-in-the-notes) | Kind 27/27 specs and VM SQL are not completed S00–S15 fault/restore certification |
| 14, 16 | [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md) | Nov 29 full first pass, Dec 27 candidate release are goals, not passed or promised milestones |
| 15 | [CONTRIBUTING](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md) and team record below | Both are co-maintainers; per-issue owner and reviewer, no invented permanent feature assignment |
| 17 | [Post-v0.1 direction](#post-v01-direction) | Unsheduled proposal, not support or release commitment |
| 18 | Builder validation notice | Discussion: incident criteria, reference CSI stack, independent runbook review |

## Recorded execution evidence

The source revision above is the deployed code selection, not a claim that every
mandatory release scenario passed. The observations below were recorded on
2026-10-20; later edits to main do not change their source revision.

| Evidence | Exact result and boundary |
|---|---|
| [Kind E2E run 39348551910](https://github.com/cubrid-lab/cubrid-kubernetes-operator/actions/runs/39348551910) | 27/27 specs passed on reviewed head `f12632473de9e91e6b65e44444b4cf622d0caf43`, subsequently merged as `39b1cb6`. Spec count is not the number of S00–S15 scenarios. |
| [Development Images run 39353186855](https://github.com/cubrid-lab/cubrid-kubernetes-operator/actions/runs/39353186855) | Published the selected main commit; manager `sha256:24706be69f034c5f67e3518b1df76b5c9066665ec63550a19875c621a0aaf880`, IM `sha256:49ace1f424586811ae852b0376abb8418ca00080cc4bf425998d8ed3af1fde45`. |
| [VM connection / HTTP record](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281330433) | Fresh LAB00 SQL and bounded HTTP checks passed on Kubernetes `v1.36.5+k3s1`, CUBRID `11.4.6.1963`, four Ready VM nodes and local-path storage. LAB00 is an installed connection lane, not S00 installation or VM power-loss validation. |
| [VM rollout / SQL record](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281421472) | Demo/HA rollout retained seven original DB PVC/PV identities, known rows/timestamps and post-rollout RW/RO behavior. These checks do not guarantee arbitrary dataset recovery. The separate pycubrid upgrade remained held; it is not counted as an updated cluster. |
| [Write quarantine #113](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/113), [unknown HA observation #438](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/438) | Both remain open at this source check. Normal RO write rejection is not partition-time RW quarantine; a later passing Kind run does not identify the earlier unknown-HA cause. |

The timeline's **November 29 first mandatory-scenario pass** and **December 27
v0.1 release** are targets consistent with the pinned ROADMAP stages. December
is reserved for candidate/repeat/soak/regression and runbook checks; no mandatory
safety gate is dropped to meet the dates.

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
  not evidence that integrated rejoin/rebuild/backup/restore has passed.
- IM bearer authentication is separate from database authentication/TLS. The
  pinned README records no traffic encryption and empty DBA passwords; the
  slides do not claim production security.
- Required first-release work still includes authenticated non-root lifecycle,
  three-member HA/RW/RO, Pod/VM/Broker/Operator faults, write quarantine,
  rejoin/rebuild, backup/new-cluster restore, retention/auth/disruption policy,
  truthful observability and reproducible S00–S15 evidence.
- Compatible updates and disk-full testing remain conditional. Engine-version
  migration, non-promotable replicas and broader platform/zone support remain
  outside the initial scope.
- Final speaking rehearsal, PowerPoint desktop review and submission are not
  claimed by a successful browser or export check.

## Comparison boundaries

Slide 7 compares inspected implementation models, not every upstream feature or deployed reliability. Source inspection was repeated against the same two pinned revisions for this content revision.

| Claim | Primary source and boundary |
|---|---|
| Official HA status uses the first successful CMS response's node view | [status controller, lines 63–110](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L63-L110). The project already supports HA observation. |
| Our primary decision aggregates expected-member observations and leaves missing/conflicting evidence unresolved | [resolution inputs](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/haresolve.go#L36-L105), [decision](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/haresolve.go#L189-L235). This does not itself stop SQL writes. |
| Official backup uses scheduling, Pod exec and persisted per-Pod status | [execution/status](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/backupdb_controller.go#L317-L345), [API](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/api/v1/backupdb_types.go#L23-L54). Do not say it has no backup persistence or recovery support. |
| Our IM has a PVC-durable operation protocol; interrupted operations become Failed on restart | [opstore](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/instancemanager/opstore.go#L57-L120). Durable identity is not automatic resumption or guaranteed completion. |
| Our backup target/request identity is recorded; restore verifies manifest objects and targets a new cluster | [dispatch](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/cubridbackup_controller.go#L199-L207), [size/SHA-256 checks](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/instancemanager/restore.go#L347-L421), [restore ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0008-restore-semantics.md#L47-L79). Integrated new-cluster restore remains a required verification gate. |
| Port/Ready observations and SQL validation differ in both projects | [official endpoint check](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/broker_endpoint_controller.go#L97-L111), [our TCP readiness](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/internal/controller/broker.go#L208-L216). Recorded VM SQL is separate evidence, not our readiness mechanism. |

Both projects observe periodically. Polling is not presented as a differentiator. The hypothetical recovery scenario is an explanation of a decision, not a newly discovered customer incident. No RTO/RPO reduction, adoption, comparative stability, most-caught-up-backup selection or universal recovery guarantee is claimed.

## Post-v0.1 direction

Slide 17 is a **direction proposal prompted by presentation feedback**, not an approved new release plan. The first version remains the required, bounded recovery qualification described by the pinned ROADMAP; no mandatory safety condition is moved to a later version.

1. Learn from independent installations and incident reproduction; improve failure diagnosis and operating procedures. Qualify DB authentication/TLS and compatible updates as adoption needs. These are not claimed supported today; IM authentication is distinct. Compatible updates remain conditional in v0.1 until their gates pass.
2. Expand Kubernetes/CSI coverage only with per-configuration recovery evidence. Consider arm64 and multi-zone tests separately; do not generalize single-lab results.
3. Investigate engine-version migration and additional replication topologies after the recovery foundation is established. These are explicitly future scope in the pinned ROADMAP.

Dates, version numbers, implementation order and supported-production status are not promised. The next bounded release scope follows v0.1 acceptance, maintainer decisions, available validation environments and actual user feedback.

## Spoken-copy revision

The 2026-10-21 wording revision keeps the same eleven slides,600-second budget, source revisions and execution evidence. Titles, captions and notes use concrete actors/actions instead of repeating abstract labels and disclaimers. Relevant limits remain beside the Kind/VM results, write-quarantine work, release/security scope and future plan. No interviews, personal incidents, fixed individual assignments, measurements or future dates were added.
