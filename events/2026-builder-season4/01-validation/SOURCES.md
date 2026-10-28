# First-validation presentation — sources

Presentation expanded on **2026-10-22 (KST)** to 18 slides per language and reordered to 15 on **2026-10-28** (#75); execution evidence remains fixed to **2026-10-20**, except the VM-lab backup and new-cluster restore runs of **2026-10-25** (now slides 8–9). The main deck follows the seven items in the supplied
Builder notice. Detailed source checks stay here and in speaker notes rather
than becoming extra presentation sections.

## Agenda and timing

| Announced requirement | Slides | Planned seconds |
|---|---|---|
| 1. Project and team, and what the Operator does today | 1–2 | 65 |
| 2. Problem and initial users | 3 | 40 |
| 5. Architecture, SQL and operations paths, what to check after a master fault | 4–5 | 95 |
| 4. Write safety, recorded evidence and validation gaps | 6, 8–9 | 115 |
| 3. Existing approaches and open-source comparison | 7 | 50 |
| 6. Roadmap, responsibilities, v0.1 and later direction | 10–13 | 125 |
| 7. Discussion topics | 14 | 25 |
| Questions | 15 | 5 |
| **Total** | **15 slides per language** | **520 + 80 seconds buffer** |

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
| 5–6 | [Official README](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/README.md), [status controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L68), [backup controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/backupdb_controller.go#L317) | Upstream already has HA observation, storage and scheduled backup. Comparison is source-level, not field reliability benchmarking |
| 7–9 | [Architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture) and [Broker flows](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture) | CUBRID owns HA promotion. IM is integrated in DB container; Operator never proxies SQL |
| 10 | [Fault-safety ADR](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0005-failover-split-brain.md), [write-quarantine issue](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/113) | Reported unknown master is not automatic RW write isolation; mandatory work remains |
| 11–12 | [Kind, VM and rollout records](#recorded-execution-evidence), [v0.1 gates](#evidence-boundaries-retained-in-the-notes) | Kind 27/27 specs, VM SQL and the first S12 restore passes are not completed S00–S15 fault/restore certification |
| 13, 15 | [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md); the 24-hour load target is from [final integration issue #95](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/95) ("initial target of 24 hours") | Nov 29 full first pass, Dec 27 candidate release are goals, not passed or promised milestones |
| 14 | [CONTRIBUTING](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md) and team record below | Both are co-maintainers; per-issue owner and reviewer, no invented permanent feature assignment |
| 16 | [Post-v0.1 direction](#post-v01-direction) | Unsheduled proposal, not support or release commitment |
| 17 | Builder validation notice | Discussion: incident criteria, the first CSI driver to support, independent runbook review |

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
  three-member HA/RW/RO, Pod/VM/Broker/Operator faults, write quarantine,
  rejoin/rebuild, backup/new-cluster restore, retention/auth/disruption policy,
  truthful observability and reproducible S00–S15 evidence.
- Compatible updates and disk-full testing remain conditional. Engine-version
  migration, non-promotable replicas and broader platform/zone support remain
  outside the initial scope.
- Final speaking rehearsal, PowerPoint desktop review and submission are not
  claimed by a successful browser or export check.

## Comparison boundaries

Slide 6 compares inspected implementation models, not every upstream feature or deployed reliability. Source inspection was repeated against the same two pinned revisions for this content revision.

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
with each capability marked verified, built, or a v0.1 goal: three-member HA
with RW/RO and backup restore are verified by the Kind/VM records above; role
discovery is built (`DESIGN.md` section 11, implementation status), while RW
write blocking during faults is still not built or verified; rejoin and
rebuild are v0.1 goals. Slide 4 replaces the earlier two architecture slides
with one drawing from `DESIGN.md` sections 7 and 10: YAML → Kubernetes API →
Operator → resources; three HA members, each with Instance Manager and PVC;
a separate RW/RO Broker tier behind the RW/RO Services, where RW Brokers find
the master themselves (ADR-0002) and the Operator never relays SQL or picks
the master (ADR-0001); and S3-compatible object storage for initial copy,
backup and restore. Slide 5 walks through a master Pod fault as a *designed*
flow and separates Pod availability (Kubernetes), DB HA state (CUBRID HA
switches, the Operator records it), SQL access (Broker) and data (checked by
E2E tests, not by the Operator). The official Operator comparison is one
slide (7) placed after the proposal; its rows and source boundary are
unchanged. The agenda slide and the old YAML-flow slide are removed. The plan
is 520 seconds with an 80-second buffer.
