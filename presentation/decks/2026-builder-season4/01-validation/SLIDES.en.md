<OperatorSlide section="1 · Project and team" index="01" total="10" source="Project README · Team profiles" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID<br>Kubernetes Operator</h1><p class="op-lead">An Operator for managing CUBRID deployment,<br>high availability and recovery on Kubernetes.</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik</span></div></div>

</OperatorSlide>

<!--
[60s · 1 · Project and team]
Hello. We are Yeongseon Choe and Gyeongjun Paik from CUBRID Lab. We are developing a Kubernetes Operator for CUBRID deployment, high availability and recovery operations. We participate as the project’s co-maintainers. This first-validation presentation introduces the problem, our proposed approach and the first-release plan, and asks for feedback. The project is experimental.
-->

---

<OperatorSlide section="2 · Problem and target users" index="02" total="10" source="README · DESIGN" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md#why-this-project">

<h1 class="op-title">Problem and target users</h1><div class="op-two"><div class="op-stack"><h3>Target users</h3><ul class="op-list"><li><b>CUBRID database operators</b><small>Check roles, replication and data after a fault</small></li><li><b>Kubernetes platform teams</b><small>Manage Pods, persistent storage and access</small></li></ul></div><div class="op-stack"><h3>Problem</h3><ul class="op-list"><li><b>State is checked in several places</b><small>Pod status alone does not establish the master or replication state</small></li><li><b>Recovery needs separate steps</b><small>Rejoin, data recovery and service recovery need to be checked together</small></li></ul></div></div><p class="op-caption">Initial user hypothesis. We want feedback on actual environments and priorities.</p>

</OperatorSlide>

<!--
[60s · 2 · Problem and target users]
We focus on database operators and platform teams planning to run CUBRID on Kubernetes. After a fault, they need to check not only Pod restart but the current master, replication and whether retained data can be reused. Database operations and Kubernetes resource management involve separate observations and procedures. We want to reduce that repeated coordination work. This is an initial user hypothesis; we are not claiming validated demand or completed user interviews.
-->

---

<OperatorSlide section="3 · Current approaches" index="03" total="10" source="Official Operator · Pinned sources" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">Current approaches and limitations</h1><table class="op-comparison"><thead><tr><th>Approach</th><th>What it already provides</th><th>Additional questions</th></tr></thead><tbody><tr><td>YAML / scripts</td><td>Resource and configuration deployment</td><td>What state returns after a fault?</td></tr><tr><td>Official CUBRID Operator</td><td>HA role observation, storage, scheduled backup</td><td>How should missing observations be interpreted?</td></tr><tr><td>CUBRID native HA</td><td>Replication and role transitions</td><td>How does this meet the Kubernetes lifecycle?</td></tr></tbody></table><p class="op-caption">The official Operator also observes HA roles. Our experiment focuses on state assessment and recovery outcomes after faults.</p>

</OperatorSlide>

<!--
[75s · 3 · Current approaches]
Existing approaches include YAML and scripts, CUBRID native HA, and the official CUBRID Operator. The official Operator already provides HA role observations, storage and scheduled backups as well as deployment. We want to examine incomplete or conflicting observations, real SQL outcomes, replication agreement and reproducible recovery. A listening-port check alone does not establish successful SQL or data agreement. This is the scope of our experiment, not a deployed stability comparison with the official project.
-->

---

<OperatorSlide section="4 · Proposed solution" index="04" total="10" source="DESIGN §2–4" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals">

<h1 class="op-title">Proposed solution</h1><div class="op-path"><div class="op-node project">Intent<small>CubridCluster</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Observe<small>Roles · replication · access</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Reconcile<small>Resources · operation lifecycle</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Report<small>Conditions · Events</small></div></div><p class="op-caption">Observe database state, reconcile Kubernetes resources and operations, and report the result.</p>

</OperatorSlide>

<!--
[60s · 4 · Proposed solution]
The user declares a cluster through CubridCluster. The Operator observes both database and Kubernetes state, coordinates resources and operations, and reports the result. CUBRID retains responsibility for HA role transitions; the Operator connects those results to the resource lifecycle. This is the proposed operating model. Write quarantine, rejoin and complete backup/restore still require real-environment validation and are part of the season plan.
-->

---

<OperatorSlide section="5 · Draft architecture" index="05" total="10" source="DESIGN §7, §9, §10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">Draft architecture</h1><div class="op-stack"><div class="op-path"><div class="op-node ">CubridCluster<small>Kubernetes API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator<small>Observe · reconcile</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Kubernetes resources<small>StatefulSet · Service · PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">DB MEMBERS · CUBRID NATIVE HA</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>Member 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 2 · PVC</small></div></div></div><div class="op-stack"><p class="op-kicker">SEPARATE ACCESS TIER</p><div class="op-node ">Broker tier<small>Redundant RW / RO Brokers</small></div><div class="op-node storage">Object storage<small>Bootstrap · backup · restore</small></div></div></div></div><p class="op-caption">IM is an integrated supervisor in the DB container, not a sidecar. It communicates with the Operator through an authenticated HTTP API.</p>

</OperatorSlide>

<!--
[75s · 5 · Draft architecture]
The main components are the Kubernetes API, Operator, database members, Instance Managers, Brokers and object storage. The Operator manages StatefulSets, Services and PVCs, and uses authenticated Instance Manager APIs for local operations and observations. Each Instance Manager is integrated in its DB container, not a sidecar. CUBRID HA determines roles among the three members. Brokers provide the separate RW/RO access tier. Object storage carries bootstrap copies and backup/restore artifacts.
-->

---

<OperatorSlide section="5 · Data and control flow" index="06" total="10" source="DESIGN §9–10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">Data and control flow</h1><div class="op-stack"><p class="op-kicker">DATA PATH · APPLICATION SQL</p><div class="op-path"><div class="op-node ">Application</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">RW / RO Service</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Broker</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>SQL execution</small></div></div><p class="op-kicker">CONTROL PATH · INTENT AND OPERATIONS</p><div class="op-path"><div class="op-node ">CubridCluster</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Instance Manager<small>Authenticated HTTP</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>Local operations · status</small></div></div></div><p class="op-caption">Role and operation observations feed Conditions, Events and metrics. Data traffic and control information follow separate paths.</p>

</OperatorSlide>

<!--
[60s · 5 · Data and control flow]
Application SQL goes through RW/RO Services and Brokers to CUBRID. Configuration and control requests go from CubridCluster to the Operator and Instance Managers. Observations feed status, Events and metrics. These are separate data and control paths. The design does not put the Operator in the SQL path or let it promote a member from incomplete observations or choose between divergent datasets.
-->

---

<OperatorSlide section="6 · 12-week roadmap" index="07" total="10" source="ROADMAP · STP IV" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">12-week roadmap</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Scope and contracts</b><p>Scenarios and environment<br>Standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA alpha</b><p>Three members, RW/RO<br>Backup/restore alpha</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Recovery validation</b><p>Write quarantine<br>Rejoin and rebuild</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Release preparation</b><p>Repeated faults and fixes<br>Runbooks and evidence</p></div></div><p class="op-caption">Oct 05–Dec 27, 2026. These are stage targets; completion depends on validation results.</p>

</OperatorSlide>

<!--
[75s · 6 · 12-week roadmap]
The season runs for twelve weeks, October 5 to December 27. Week one settles scope, scenarios and the environment. Weeks two to four target three-member HA, RW/RO access and backup/restore alpha. Weeks five to eight validate quarantine, rejoin and rebuild. The final four weeks cover repeated validation, regression fixes, installation and operational documentation, and release evidence. These are stage targets. Elapsed dates do not establish completion; actual validation does.
-->

---

<OperatorSlide section="6 · Team roles" index="08" total="10" source="Team profiles · Project governance" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#team-and-role-record">

<h1 class="op-title">Team roles</h1><div class="op-two"><table class="op-comparison"><thead><tr><th>Member</th><th>Current role</th></tr></thead><tbody><tr><td>Yeongseon Choe<br><small>@yeongseon</small></td><td>Co-maintainer</td></tr><tr><td>Gyeongjun Paik<br><small>@paikend</small></td><td>Co-maintainer</td></tr></tbody></table><div class="op-stack"><h3>Season work areas</h3><ul class="op-list"><li><b>Cluster and HA integration</b><small>State observations and Kubernetes resources</small></li><li><b>Backup and recovery</b><small>Failure and recovery scenarios</small></li><li><b>Documentation and publication</b><small>Installation, operations and validation results</small></li></ul></div></div><p class="op-caption">Shared design, development and validation. Fixed feature-to-person assignments are not yet confirmed.</p>

</OperatorSlide>

<!--
[45s · 6 · Team roles]
The team is Yeongseon Choe and Gyeongjun Paik, the project’s co-maintainers. The season’s work areas are cluster and HA integration, backup and recovery, and documentation/publication. The established model is shared design, development and validation. Specific feature ownership for each person is still being organized.
-->

---

<OperatorSlide section="6 · First public release scope" index="09" total="10" source="ROADMAP · v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#v01-scope">

<h1 class="op-title">First public release scope</h1><div class="op-release"><div><h3>Cluster operations</h3><ul class="op-list"><li><b>Cluster lifecycle</b><small>Authenticated non-root runtime and persistent storage</small></li><li><b>Three-member HA and access</b><small>Role observations and RW/RO access</small></li></ul></div><div><h3>Failure and data recovery</h3><ul class="op-list"><li><b>Faults and write quarantine</b><small>Pod, VM, Broker and Operator faults</small></li><li><b>Rejoin, rebuild and restore</b><small>Backup and new-cluster restore</small></li></ul></div><div><h3>Operational material</h3><ul class="op-list"><li><b>Retention, security and observability</b><small>Auth, disruption policy, status, Events and metrics</small></li><li><b>Reproducible docs and evidence</b><small>Installation/operations guidance and required scenarios</small></li></ul></div></div><p class="op-caption">Initial target: CUBRID 11.4.x / amd64 and one Kubernetes/CSI setup. Compatible updates and disk-full tests are conditional; engine migration and broad environment support are outside the initial scope.</p>

</OperatorSlide>

<!--
[60s · 6 · First public release scope]
The first-release target is cluster operations and HA, access, failure/data recovery, and reproducible installation and operational guidance for one pinned environment. It includes enforced write quarantine, rejoin and rebuild, backup and new-cluster restore, retention, authentication, disruption policy and truthful observability, supported by required scenario evidence. Compatible updates and disk-full testing are conditional. Engine migration and broad environment support are outside the initial scope. These are targets, not claims of completed support.
-->

---

<OperatorSlide section="7 · Discussion" index="10" total="10" source="Project proposal" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md">

<h1 class="op-title">Discussion</h1><ol class="op-questions"><li>Are the target users and problem definition appropriate?</li><li>Which operational capabilities should we prioritize for the first version?</li><li>Who can help validate it in an actual operating environment?</li></ol>

</OperatorSlide>

<!--
[30s · 7 · Discussion]
For this first validation, we would like feedback on the target users and problem definition, the priorities for the first version, and opportunities to validate it in a real operating environment. We also welcome help reproducing the operational documentation. Thank you.
-->
