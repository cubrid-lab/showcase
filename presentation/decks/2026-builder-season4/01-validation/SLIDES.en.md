---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="1 · Project and team" index="01" total="11" source="Project · Team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID Kubernetes<br>Operator</h1><p class="op-lead">Check database state and operations<br>together after Pod recovery.</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div><p class="op-caption">Season goal: v0.1 with reproducible installation, faults and recovery in a bounded environment</p></div>

</OperatorSlide>

<!--
[40s · 1 · Project and team]
Hello. We are Yeongseon Choe and Gyeongjun Paik of CUBRID Lab, developing the CUBRID Kubernetes Operator together. This season, we aim to go beyond running a database in a container and publish a first version that helps verify database state and recovery work after a fault.

One question guides this talk: when a Pod comes back, can the operator resume writes? We will explain how we connect the information and operations needed for that decision, what we have verified, and our proposed direction beyond v0.1.
-->

---

<OperatorSlide section="2 · Problem and target users" index="02" total="11" source="Problem · User hypothesis" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">The Pod is back.<br>Can we resume writes?</h1><div class="op-two"><div class="op-stack"><p class="op-kicker">AN OPERATING SCENARIO</p><ul class="op-list"><li><b>DB member fault → Pod recreated</b><small>Ready alone cannot establish recovery</small></li><li><b>A shared decision</b><small>DB operators: roles · replication · data<br>Platform team: Pods · volumes · Services</small></li></ul></div><div class="op-stack"><p class="op-kicker">THREE CHECKS BEFORE RECOVERY</p><ul class="op-list"><li><b>Role</b><small>Which master currently accepts writes?</small></li><li><b>Data</b><small>Are existing rows and committed writes retained?</small></li><li><b>Access</b><small>Does real SQL behave as intended through RW/RO?</small></li></ul></div></div><p class="op-caption">Initial user hypothesis: DB operators and platform teams running CUBRID on Kubernetes</p>

</OperatorSlide>

<!--
[65s · 2 · Problem and target users]
Imagine a node hosting a database member fails and its Pod is recreated. The platform team can confirm that the Pod is Ready and its volume is attached. The database operator still needs to identify the current master, check replication and existing data, and verify reads and writes through the actual access paths.

An open port, for example, does not prove that every member retains the last committed write. Recovery decisions draw on Kubernetes status, database state and SQL results in separate places. That is the problem we want to address. Our initial users are database operators and platform teams making this decision together. This is a user hypothesis; we have no verified customer incident or interview-based demand evidence. We want feedback on how much this operating problem matters.
-->

---

<OperatorSlide class="op-compact" section="3 · Current approaches and limits" index="03" total="11" source="Pinned upstream · Design" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">Make failure boundaries explicit</h1><table class="op-comparison"><thead><tr><th>Design area</th><th>Observed in official code</th><th>Our design</th></tr></thead><tbody><tr><td>HA observations</td><td>Node data from the first successful CMS response</td><td>Aggregate fresh observations per member<br>Missing or conflicting: primary unresolved</td></tr><tr><td>Long-running work</td><td>Scheduling, Pod exec and backup status</td><td>IM HTTP API · operation IDs persisted on PVC<br>Interruptions remain Failed for review</td></tr><tr><td>Backup metadata</td><td>Target Pod, script and storage settings</td><td>Record target and request ID<br>Validate restore inputs with manifest and checksums</td></tr></tbody></table><p class="op-caption">The official Operator provides HA observations, storage and scheduled backups. This compares pinned implementation models, not stability.</p><p class="op-boundary"><b>SHARED LIMIT</b>　Port/Ready checks are separate from real SQL and data validation.</p>

</OperatorSlide>

<!--
[65s · 3 · Current approaches and limits]
CUBRID native HA and the official CUBRID Operator already exist. Native HA handles replication and role transitions. The official Operator also observes HA roles and provides storage and scheduled backups. Claiming that existing tools lack HA or backup would be inaccurate.

CMS is the CUBRID Manager Server; IM is our Instance Manager. Our separate design experiments with authenticated HTTP APIs and persistent operation IDs for local database work, so requests and results can still be compared after interruption. Failure boundaries matter: if operation records cannot be read, for example, the system must not start another operation on its own. We also distinguish status reports from real SQL and data checks. Both Operators use port-based checks, so our Ready status does not mean SQL has been verified. We have no evidence of superior stability; we publish the design and results to support discussion and improvement.
-->

---

<OperatorSlide section="4 · Proposed solution" index="04" total="11" source="Design · Recorded evidence" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Connect intent, observations<br>and operation results</h1><div class="op-path"><div class="op-node project">Declare intent<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">Observe DB<small>Roles · replication · access</small></div><div class="op-arrow">→</div><div class="op-node project">Manage work<small>Operation ID · progress · result</small></div><div class="op-arrow">→</div><div class="op-node">Report status<small>Conditions·Events</small></div></div><div class="op-evidence"><div><p class="op-kicker">IMPLEMENTED AND OBSERVED</p><p>Kind: 27/27 specs passed<br>VMs: known rows retained · RW/RO SQL checked</p></div><div><p class="op-kicker">EVIDENCE STILL REQUIRED</p><p>Write quarantine under VM faults and partitions<br>Rejoin · rebuild · backup restore · CSI</p></div></div><p class="op-caption">Intended value: shared state and operation records, plus reproducible SQL evidence, for recovery decisions</p>

</OperatorSlide>

<!--
[60s · 4 · Proposed solution]
Users declare their desired configuration through CubridCluster. The Operator observes database state and coordinates Kubernetes resources and local operations. Long-running work is tracked through operation IDs, progress and results, rather than command execution alone. Interrupted operations can remain Failed. A persistent record does not guarantee success or automatic resumption of every operation.

The Kind run linked to code reference 39b1cb6 passed 27 specs. On real Kubernetes VMs, standalone and HA checks preserved known data, committed new writes through RW, read through RO and rejected RO writes. These observations do not complete every mandatory scenario, partition behavior, VM-fault testing or CSI qualification. Our intended value is a shared state and operation record, plus separately recorded SQL and data evidence, on which operators can base a recovery decision.
-->

---

<OperatorSlide class="op-compact" section="5 · Draft architecture" index="05" total="11" source="DESIGN · ADR 0003 / 0005" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">Separate HA decisions,<br>resource control and DB work</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>Observations · resources · operations</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes resources<small>StatefulSet·Service·PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID NATIVE HA · REPLICATION AND ROLE TRANSITIONS</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>Member 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 2 · PVC</small></div></div></div><div class="op-stack"><div class="op-node">Broker tier<small>Separate RW / RO access tier</small></div><div class="op-node storage">Object storage<small>Initial copy · backup · restore</small></div></div></div><p class="op-caption">IM: supervisor in the DB container · authenticated HTTP API · operation records on PVC<br>The Operator never promotes a master or chooses a winner between divergent datasets.</p>

</OperatorSlide>

<!--
[70s · 5 · Draft architecture]
The platform combines Kubernetes, CUBRID native HA and S3-compatible object storage. The Operator reads configuration from the API and manages StatefulSets, Services and PVCs. Each database container contains both CUBRID and an Instance Manager. IM is an integrated supervisor, not a separate sidecar, and exposes local operations and their status through an authenticated HTTP API.

The responsibilities are distinct. The engine decides replication and role transitions; the Operator connects them to the Kubernetes lifecycle. IM handles local work and tracks it through operation IDs and PVC records. A separate Broker tier provides RW and RO access. Object storage carries initial copies and backup or restore artifacts. Member zero is not a permanent master. When observations are incomplete, the Operator does not promote a member or choose a winner between divergent datasets.
-->

---

<OperatorSlide class="op-compact" section="5 · Data and control flow" index="06" total="11" source="DESIGN · Fault contract" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">Separate SQL from operational control</h1><div class="op-stack"><p class="op-kicker">DATA · APPLICATION SQL</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">CONTROL · OPERATIONAL INTENT AND MEMBER WORK</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">IM API<small>Local work · operation records</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / PVC</div></div></div><p class="op-boundary"><b>FLOW TO VALIDATE AFTER A MASTER FAULT</b><br>Engine role transition → IM observation → Operator status → SQL/data comparison</p><p class="op-caption">Unresolved status does not block writes. Partition write quarantine requires validation.</p>

</OperatorSlide>

<!--
[60s · 5 · Data and control flow]
In the upper data path, application SQL travels through an RW or RO Service and a Broker to CUBRID. The Operator does not relay SQL. In the lower control path, operational intent and requests reach IM through the Operator. Role and operation observations return as Conditions, Events and metrics. Backup and restore artifacts move between database operations and object storage.

Returning to our fault example, we must observe the engine's role transition through IM, check that Operator status converges, and compare actual SQL and data with that result. Displaying Unknown does not block writes. A recorded Kind run continued RW writes while roles were unresolved. Testing writes on both new and existing connections during partitions, and implementing and validating quarantine, remain mandatory work for the first version.
-->

---

<OperatorSlide section="6 · 12-week roadmap" index="07" total="11" source="ROADMAP · Delivery gates" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">A 12-week plan measured<br>by evidence at each stage</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Pin the baseline</b><p>Environment and scenarios<br>Standalone SQL evidence</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA alpha</b><p>Three members · RW/RO<br>Real-VM execution path<br>Backup/recovery alpha</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>First full required pass</b><p>Write quarantine · rejoin<br>Rebuild · backup restore<br>S00–S15 target</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Stabilize the same RC</b><p>Repeated faults · 24h load target<br>Docs reproduced by another person<br>Fix regressions · pin artifacts</p></div></div><p class="op-boundary"><b>11.29</b> Target: first full mandatory pass　→　<b>12.27</b> v0.1 publication target</p><p class="op-caption">Retain commit, image digests, environment, SQL history and verdict together. Dates are targets, not passes.</p>

</OperatorSlide>

<!--
[70s · 6 · 12-week roadmap]
The season runs for twelve weeks, October 5 through December 27. Week one fixes the environment and scenarios and checks standalone SQL. Weeks two through four target three-member HA, RW/RO, a real-VM execution path, and backup and recovery alpha. Current Kind and VM results provide part of that evidence.

Weeks five through eight target the first complete pass of all mandatory scenarios by November 29: write quarantine, rejoin, rebuild, and restoring a new cluster from a real backup. December is intended for repeated core faults on the same candidate, an initial 24-hour load target, documentation reproduced by someone other than the author, and regression fixes. We retain the commit, image digests, environment, SQL history and verdict together. We will not drop mandatory safety conditions or mark unexecuted cases as passed to meet a date. Validation will determine whether publication is possible on December 27.
-->

---

<OperatorSlide section="6 · Team responsibilities" index="08" total="11" source="Governance · Accountability" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">Two co-maintainers;<br>an owner and reviewer per change</h1><div class="op-meta"><b>Yeongseon Choe @yeongseon</b><b>Gyeongjun Paik @paikend</b><span>Co-maintainers</span></div><table class="op-comparison"><thead><tr><th>Responsibility</th><th>Work to complete</th></tr></thead><tbody><tr><td>Issue owner</td><td>Reproduce failure → implement/test → docs/evidence</td></tr><tr><td>Other maintainer</td><td>Review failure paths and changes → check evidence</td></tr><tr><td>Shared accountability</td><td>Review installation, HA, recovery and release criteria</td></tr></tbody></table><p class="op-caption">Ownership is per issue, with mutual review, rather than fixed feature assignments.<br>One shared-VM fault experiment at a time; independently reproduce the documentation.</p>

</OperatorSlide>

<!--
[45s · 6 · Team responsibilities]
Yeongseon Choe and Gyeongjun Paik are co-maintainers. We describe actual responsibilities without inventing unconfirmed individual specialties or permanent feature assignments. Each issue owner reproduces the failure, implements and tests the change, and prepares documentation and execution evidence. The other maintainer reviews failure paths and the change, then checks the evidence against completion criteria.

We use this approach for cluster and HA work, backup and recovery, documentation and release preparation. Shared VM fault experiments run one at a time. For release validation, someone other than the author must reproduce installation and recovery from the documentation alone. We can add fixed individual ownership once confirmed; shared accountability and an owner and reviewer for each change remain distinct.
-->

---

<OperatorSlide class="op-compact" section="6 · v0.1 release scope" index="09" total="11" source="ROADMAP · v0.1 acceptance" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">v0.1 acceptance and deliverables</h1><table class="op-comparison op-acceptance"><thead><tr><th>Required scope</th><th>Completion evidence</th></tr></thead><tbody><tr><td>Non-root · persistent DB<br>3-member HA · RW/RO</td><td>Compare real SQL, roles, commits and data</td></tr><tr><td>Faults · write quarantine<br>Rejoin · rebuild</td><td>Verify outcomes after Pod/VM/Broker/Operator faults</td></tr><tr><td>Backup<br>Restore to new cluster</td><td>Restore real backups; match known data</td></tr><tr><td>Retention · IM auth<br>Disruption · observability</td><td>S00–S15 evidence + reproducible install/operate/recover docs</td></tr></tbody></table><p class="op-boundary"><b>PUBLIC ARTIFACTS</b>　Images · install manifests · environment matrix · operations docs · results</p><p class="op-caption">CUBRID 11.4.x / amd64 / one K8s/CSI setup · experimental · compatible updates/disk-full conditional</p>

</OperatorSlide>

<!--
[55s · 6 · v0.1 release scope]
v0.1 must make installation, faults and recovery reproducible in one pinned environment. We compare real SQL, roles, commit history and data, and verify that rejoin or rebuild does not overwrite valid data. A new cluster restored from a real backup must match a known dataset. Retention, IM authentication, voluntary-disruption policy, accurate observations and reproducible documentation are also required.

We plan to publish images, installation manifests, a supported-environment table, operations guidance and validation results tied to the same candidate. The baseline is CUBRID 11.4.x, amd64 and one Kubernetes/CSI configuration. Current local-path VM observations do not satisfy CSI qualification. The first version is experimental. IM API authentication must not be confused with database authentication or TLS. The pinned code's empty DBA password and unencrypted traffic must also be documented.
-->

---

<OperatorSlide section="6 · Beyond v0.1" index="10" total="11" source="Proposal · Beyond v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">Beyond v0.1:<br>broaden support through experience</h1><div class="op-release"><div><h3>Operations and stability</h3><ul class="op-list"><li><b>User feedback and diagnostics</b><small>Improve recurring failures and procedures</small></li><li><b>Validate adoption requirements</b><small>DB authentication · TLS · compatible updates</small></li></ul></div><div><h3>Broader environments</h3><ul class="op-list"><li><b>More Kubernetes/CSI setups</b><small>Revalidate faults and recovery per setup</small></li><li><b>Explore architectures and zones</b><small>Separate arm64 and multi-zone experiments</small></li></ul></div><div><h3>Long-term operations</h3><ul class="op-list"><li><b>Engine-version migration</b><small>Data compatibility · disruption · recovery</small></li><li><b>Replication topologies</b><small>Explore non-promotable read replicas</small></li></ul></div></div><p class="op-boundary"><b>DECISION GATES</b>　v0.1 required validation → user reproduction/feedback → decide next scope</p><p class="op-caption">Proposed directions only. No version, date or operational-support commitment; v0.1 requirements stay in scope.</p>

</OperatorSlide>

<!--
[40s · 6 · Beyond v0.1]
v0.1 is not the end of the project. We propose using operating feedback to improve recurring failures, diagnostics and procedures, and to validate adoption needs such as database authentication, TLS and compatible updates. Additional Kubernetes and CSI configurations would each need fresh fault and recovery validation.

arm64, multiple zones, engine-version migration and topologies such as non-promotable read replicas are separate long-term topics. This is a proposed direction, with no next-version number or completion-date commitment. Mandatory v0.1 safety conditions stay in v0.1. Initial validation and user feedback will guide the next scope.
-->

---

<OperatorSlide section="7 · Discussion" index="11" total="11" source="Feedback · Validation partners" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Three questions to shape<br>the next validation</h1><ol class="op-questions"><li>For one recent incident,<br>what did you check, in what order, before restoring service?</li><li>Which Kubernetes/CSI setup can we validate together,<br>and what limits apply to volume and fault experiments?</li><li>In December, could you independently<br>reproduce installation and recovery from the docs?</li></ol>

</OperatorSlide>

<!--
[30s · 7 · Discussion]
We would welcome feedback on three questions. For one recent incident, what did you check, in what order, before deciding to restore service? We also need a Kubernetes/CSI combination to pin together, along with constraints on volume and fault experiments. Finally, we are looking for someone other than the authors to reproduce installation and recovery from the documentation in December. Your operating experience, environment and reproduction results will help shape the first version and the direction beyond it. Thank you.
-->
