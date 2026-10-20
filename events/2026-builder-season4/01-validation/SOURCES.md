# First-validation presentation — sources

Updated on **2026-10-20 (KST)**. The main deck follows the seven items in the supplied
Builder notice. Detailed source checks stay here and in speaker notes rather
than becoming extra presentation sections.

## Agenda and timing

| Announced item | Slides | Seconds |
|---|---|---|
| 1. Project and team introduction | 1 | 60 |
| 2. Problem and affected users | 2 | 60 |
| 3. Current approaches and existing open-source limitations | 3 | 75 |
| 4. Proposed solution | 4 | 60 |
| 5. Draft architecture, components and information flow | 5–6 | 135 |
| 6. Twelve-week roadmap, team roles and first public release scope | 7–9 | 180 |
| 7. Topics for discussion | 10 | 30 |
| Total | 10 slides | 600 |

Both languages have the same order and time budget. This is a budget for a
ten-minute talk, not a measured rehearsal.

## Inspected technical sources

- Operator main: [`39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb).
- Official Operator: [`fa7b6c2cf26096769c4404a2e2bb683f3872aa1e`](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e).
- Visual basis: the existing [contest source](../../../presentation/slides.md) and [shared styles](../../../presentation/style.css). Only the typography/color/layout vocabulary is reused; Python ecosystem achievements are not Operator evidence.

## Claim map

| Slides | Source | Interpretation |
|---|---|---|
| 1–2, 4 | [Operator README](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md) and [DESIGN](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md) | Database-aware CUBRID/Kubernetes lifecycle coordination; target users remain a hypothesis, not established interview or adoption evidence |
| 3 | [Official README](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/README.md), [storage docs](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/storage-provisioning.en.md), [status controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L68), [Broker checks](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/broker-endpoint-controller.en.md) | Upstream already observes HA roles and provides storage/backup. A port check alone does not establish successful SQL/replica agreement. No deployed stability comparison or absence-of-all-validation claim is made |
| 5–6 | [Architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture), [Broker/service architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture), [ADR-0005](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/adr/0005-failover-split-brain.md) | Integrated DB-container IM; separate Broker tier; separate SQL/control paths. CUBRID owns role transitions. No permanent ordinal-zero master or Operator-selected winner between divergent data sets |
| 7, 9 | [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md) and [season issue 77](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/77) | Oct 05–Dec 27 targets and unchanged required/conditional/future scope. Mandatory release acceptance is not reduced by shortening the presentation |
| 8 | Team record below and [governance](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/docs/governance.md) | Shared maintainer roles are established; fixed feature ownership is not yet confirmed |
| 10 | Project proposal and supplied first-validation notice | Questions for feedback, not settled customer requirements |

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

The deck presents both as co-maintainers with shared design, development and
validation. It does not invent fixed individual feature ownership. Detailed
per-feature assignments are not required to understand this joint working model.

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
