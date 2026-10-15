# First-validation talk — evidence and editorial boundaries

Prepared on **2026-10-15**. This is a presentation evidence snapshot, not a
release/support certification. Re-check the project roadmap before presenting.

## Inspected sources

- Operator main: [`f981f818029eb8c9e2fdf845edd80828b7bbb016`](https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/f981f818029eb8c9e2fdf845edd80828b7bbb016).
- The local substantive source revision was `28d42fa26b9dfe532f2c43b99de34576a3d1d6ed`; the remote revision above adds README branding. The remote ROADMAP content was checked and is the basis for validation wording.
- Official CUBRID Operator: [`fa7b6c2cf26096769c4404a2e2bb683f3872aa1e`](https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e).
- Visual reference: the existing [contest web source](../../../presentation/slides.md) and [shared styles](../../../presentation/style.css). The Operator talk borrows their claim-first white/Pretendard/blue vocabulary, not Python ecosystem results.

## Claim map

| Slides | Claim / evidence | Source | Boundary |
|---|---|---|---|
| 1, 3–4, 6 | Database-aware operations connect Kubernetes lifecycle and native CUBRID HA | [README](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md), [DESIGN](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md) | Target users are a hypothesis; no customer/interview numbers were established |
| 2, 14 | Two-maintainer governance, author-owned implementation/tests, cross-review, one issue per person and serialized full-lab runs | [Governance](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/governance.md), [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#two-maintainer-start-order) | Personal names and fixed individual assignments remain unconfirmed |
| 5 | Official Operator already supplies HA role observations, storage and scheduled backups | [Official README](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/README.md), [storage documentation](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/storage-provisioning.en.md) | This experimental project is neither a replacement claim nor an upstream stability benchmark |
| 5 | Official status controller uses CMS `ha_status`; Broker endpoint checks use port and Pod/container observations | [Status controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/internal/controller/cubriddb_controller_status.go#L68), [Broker endpoint controller](https://github.com/CUBRID/cubrid-operator/blob/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e/docs/broker-endpoint-controller.en.md) | A listening-port check alone does not prove SQL success or replica agreement. This does not establish that upstream has no other validation |
| 7 | Declarative database, version, HA topology and storage fields | [Design example](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals), [API types](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/api/v1alpha1/cubridcluster_types.go) | Shortened illustrative YAML; HA object storage/Secrets and other prerequisites are omitted. The slide is not an install/runbook |
| 8–9 | DB-integrated Instance Manager, separate Broker tier, SQL path separate from control path | [DESIGN sections 7, 9, 10](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#7-high-level-architecture) | IM is a supervisor in the DB container, not a sidecar; SQL does not pass through the Operator |
| 10 | CUBRID owns role transitions; incomplete/ambiguous observations never authorize an Operator-selected winner | [ADR-0005](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/adr/0005-failover-split-brain.md) | An authority boundary does not prove that SQL write quarantine is enforced |
| 11–12 | Retained-data rejoin, explicit rebuild and new-cluster restore are distinct requirements; Kind evidence and gaps remain separate | [ROADMAP inventory](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#implementation-and-validation-inventory) | The roadmap records continued RW writes during unresolved Conditions: quarantine is reported, not enforced. No fresh database/Kind/VM experiment was run for this talk |
| 13, 15 | Oct 05–Dec 27 season stages and required/conditional/future v0.1 boundaries | [ROADMAP](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#stp-iv-delivery-stages), [issue 77](https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/77) | Dates are targets; mandatory safety gates are not waived. The pinned lab/platform/storage support inventory is not yet established |
| 16–17 | Discussion questions and experimental project direction | [README](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md), [scenario contract](https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/testing/scenario-contract.md) | Requests for feedback, not validated customer requirements |

## Required-topic and timing map

| Notice requirement | Slides | Seconds |
|---|---|---|
| Project and team introduction | 1–2 | 45 |
| Problem and affected users | 3–4 | 70 |
| Current approaches and open-source limitations | 5 | 35 |
| Proposed solution | 6–7 | 65 |
| Architecture, components and information flow | 8–11 | 180 |
| Progress, roadmap, roles and first-release scope | 12–15 | 145 |
| Discussion and closing | 16–17 | 60 |
| Total | 17 slides | 600 |

Korean and English sources have identical slide order and timing. Speaker
notes contain the spoken narrative and evidence caveats. The ten-minute
budget is a target; no live speaking rehearsal is claimed.

## Remaining submission details

The technical narrative is a substantive working draft. Actual team-member
names and named responsibilities remain unconfirmed; slides 2 and 14 describe
the documented collaboration model instead. These personal details are still
required before the team treats the deck as a final submission. No interview,
full-lab validation, rehearsal or support certification is implied.
