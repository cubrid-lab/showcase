# First-validation presentation — sources

Prepared on **2026-10-15**. The main deck follows the seven items in the supplied
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

- Operator main: [`f981f818029eb8c9e2fdf845edd80828b7bbb016`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/f981f818029eb8c9e2fdf845edd80828b7bbb016).
- Official Operator: [`fa7b6c2cf26096769c4404a2e2bb683f3872aa1e`](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e).
- Visual basis: the existing [contest source](../../../presentation/slides.md) and [shared styles](../../../presentation/style.css). Only the typography/color/layout vocabulary is reused; Python ecosystem achievements are not Operator evidence.

## Claim map

| Slides | Source | Interpretation |
|---|---|---|
| 1–2, 4 | [Operator README](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md) and [DESIGN](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md) | Database-aware CUBRID/Kubernetes lifecycle coordination; target users remain a hypothesis, not established interview or adoption evidence |
| 3 | [Official README](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/README.md), [storage docs](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/storage-provisioning.en.md), [status controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L68), [Broker checks](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/broker-endpoint-controller.en.md) | Upstream already observes HA roles and provides storage/backup. A port check alone does not establish successful SQL/replica agreement. No deployed stability comparison or absence-of-all-validation claim is made |
| 5–6 | [Architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#7-high-level-architecture), [Broker/service architecture](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#10-broker-and-service-architecture), [ADR-0005](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/adr/0005-failover-split-brain.md) | Integrated DB-container IM; separate Broker tier; separate SQL/control paths. CUBRID owns role transitions. No permanent ordinal-zero master or Operator-selected winner between divergent data sets |
| 7, 9 | [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md) and [season issue 77](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/77) | Oct 05–Dec 27 targets and unchanged required/conditional/future scope. Mandatory release acceptance is not reduced by shortening the presentation |
| 8 | Team record below and [governance](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/governance.md) | Shared maintainer roles are established; fixed feature ownership is not yet confirmed |
| 10 | Project proposal and supplied first-validation notice | Questions for feedback, not settled customer requirements |

## Team and role record

On 2026-10-15 the repository collaborator metadata identifies `yeongseon` and
`paikend` as the two repository administrators. Their public profiles identify
[Yeongseon Choe](https://github.com/yeongseon) and
[Paik Gyeongjun (Kent)](https://github.com/paikend). The existing contest cover
records the Korean names **최영선 · 백경준**. These identities were checked rather
than inferred from commit authorship alone.

The deck labels both as co-maintainers and describes shared design,
development and validation. It does not invent a fixed personal specialization
or feature assignment. That assignment remains a final preparation detail.

## Evidence boundaries retained in the notes

- The project is experimental, not production-ready.
- The recorded Kind scenarios are not fresh tests performed for this talk,
  and are not proof of VM, zone or broad-platform behavior.
- ROADMAP records RW writes continuing while primary/routing Conditions were
  unresolved. SQL quarantine enforcement remains open; recovery design is
  not evidence that integrated rejoin/rebuild/backup/restore has passed.
- Required first-release work still includes authenticated non-root lifecycle,
  three-member HA/RW/RO, Pod/VM/Broker/Operator faults, write quarantine,
  rejoin/rebuild, backup/new-cluster restore, retention/auth/disruption policy,
  truthful observability and reproducible S00–S15 evidence.
- Compatible updates and disk-full testing remain conditional. Engine-version
  migration, non-promotable replicas and broader platform/zone support remain
  outside the initial scope.
- Final speaking rehearsal, PowerPoint desktop review and submission are not
  claimed by a successful browser or export check.
