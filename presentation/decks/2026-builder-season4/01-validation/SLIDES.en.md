---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="1 · Project and team" index="01" total="10" source="Project README · Team profiles" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID<br>Kubernetes Operator</h1><p class="op-lead">An Operator for managing CUBRID deployment,<br>high availability and recovery on Kubernetes.</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik</span></div></div>

</OperatorSlide>

<!--
[60s · 1 · Project and team]
Hello. We are Yeongseon Choe and Gyeongjun Paik, co-maintainers of CUBRID Lab's Kubernetes Operator project. We are developing an experimental way to manage CUBRID deployment, high availability and recovery operations on Kubernetes.

Our goal connects the configuration an operator intends with the database state that actually exists. Today we will explain the operational problem, what we want to examine beyond the available approaches, and our proposed architecture and season plan. We will separate observations already recorded from validation still required. For this first review, we want feedback on whether those problems and priorities match real operating needs.
-->

---

<OperatorSlide section="2 · Problem and target users" index="02" total="10" source="README · DESIGN" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md#why-this-project">

<h1 class="op-title">Problem and target users</h1><div class="op-two"><div class="op-stack"><h3>Target users</h3><ul class="op-list"><li><b>CUBRID database operators</b><small>Check roles, replication and data after a fault</small></li><li><b>Kubernetes platform teams</b><small>Manage Pods, persistent storage and access</small></li></ul></div><div class="op-stack"><h3>Problem</h3><ul class="op-list"><li><b>State is checked in several places</b><small>Pod status alone does not establish the master or replication state</small></li><li><b>Recovery needs separate steps</b><small>Rejoin, data recovery and service recovery need to be checked together</small></li></ul></div></div><p class="op-caption">Initial user hypothesis. We want feedback on actual environments and priorities.</p>

</OperatorSlide>

<!--
[60s · 2 · Problem and target users]
Our initial target users are CUBRID database operators and Kubernetes platform teams. Database operators need to identify the current master, understand replication, and assess whether retained data can be reused. Platform teams manage Pods, volumes, Services and access paths. A failure brings these responsibilities together.

A Pod becoming Ready does not by itself show which member accepts writes or whether its data has caught up. When those checks and recovery steps are spread across tools, deciding whether service has recovered becomes harder. We want to reduce repeated coordination and verification. This remains a user hypothesis: we are not presenting completed interviews, validated demand or established adoption as project evidence.
-->

---

<OperatorSlide section="3 · Current approaches" index="03" total="10" source="Official Operator · Pinned sources" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">Current approaches and limitations</h1><table class="op-comparison"><thead><tr><th>Approach</th><th>What it already provides</th><th>Additional questions</th></tr></thead><tbody><tr><td>YAML / scripts</td><td>Resource and configuration deployment</td><td>What state returns after a fault?</td></tr><tr><td>Official CUBRID Operator</td><td>HA role observation, storage, scheduled backup</td><td>How should missing observations be interpreted?</td></tr><tr><td>CUBRID native HA</td><td>Replication and role transitions</td><td>How does this meet the Kubernetes lifecycle?</td></tr></tbody></table><p class="op-caption">The official Operator also observes HA roles. Our experiment focuses on state assessment and recovery outcomes after faults.</p>

</OperatorSlide>

<!--
[75s · 3 · Current approaches]
Available approaches include YAML and scripts, CUBRID native HA, and the official CUBRID Operator. Scripts and manifests deploy resources and configuration. CUBRID HA performs replication and role transitions. The official Operator already provides HA role observations, storage and scheduled backup. We acknowledge those existing capabilities.

Our investigation concerns observations and recovery outcomes after faults. How should the system report a member that could not be observed, or members reporting conflicting roles? Do actual SQL and replication results agree? Can another person reproduce the recovery procedure? A listening port alone cannot establish successful SQL or data agreement. We have not produced a deployed stability comparison with the official project; these are the questions defining our experiment.
-->

---

<OperatorSlide section="4 · Proposed solution" index="04" total="10" source="CI · VM evidence · 2026-10-20" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/301#issuecomment-6281421472">

<h1 class="op-title">Proposed solution</h1><div class="op-path"><div class="op-node project">Intent<small>CubridCluster</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Observe<small>Roles · replication · access</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Reconcile<small>Resources · operation lifecycle</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Report<small>Conditions · Events</small></div></div><p class="op-caption">Observe database state, reconcile Kubernetes resources and operations, and report the result.</p><p class="op-caption"><b>Evidence · 39b1cb6</b>　Kind 27/27 · Real SQL on VMs<br>VM-fault and CSI validation remain pending.</p>

</OperatorSlide>

<!--
[60s · 4 · Proposed solution]
The proposed flow is to declare intent, observe current state, reconcile resources and operations, then report the outcome. CubridCluster holds the desired configuration. CUBRID remains responsible for HA role transitions.

The current code reference is 39b1cb6. One Kind run passed 27 of 27 tests. On VMs, standalone SQL and retained-row checks passed. HA checks preserved existing rows and timestamps, committed through RW, read through RO and rejected RO writes. Bounded HTTP connection checks passed on the standalone member. The environment has four VM nodes, k3s 1.36.5+k3s1, CUBRID 11.4.6.1963 and local-path storage, which is not CSI. These are recorded observations, not completion of every S00–S15 requirement, VM-fault testing or CSI qualification.
-->

---

<OperatorSlide section="5 · Draft architecture" index="05" total="10" source="DESIGN §7, §9, §10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">Draft architecture</h1><div class="op-stack"><div class="op-path"><div class="op-node ">CubridCluster<small>Kubernetes API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator<small>Observe · reconcile</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Kubernetes resources<small>StatefulSet · Service · PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">DB MEMBERS · CUBRID NATIVE HA</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>Member 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 2 · PVC</small></div></div></div><div class="op-stack"><p class="op-kicker">SEPARATE ACCESS TIER</p><div class="op-node ">Broker tier<small>Redundant RW / RO Brokers</small></div><div class="op-node storage">Object storage<small>Bootstrap · backup · restore</small></div></div></div></div><p class="op-caption">IM is an integrated supervisor in the DB container, not a sidecar. It communicates with the Operator through an authenticated HTTP API.</p>

</OperatorSlide>

<!--
[75s · 5 · Draft architecture]
The architecture contains the Kubernetes API, Operator, database members, Instance Managers, a separate Broker tier and object storage. The Operator manages StatefulSets, Services and PVCs. Each Instance Manager handles local operations and exposes observations for its database member.

The Instance Manager is a supervisor integrated into the same DB container as CUBRID, not a sidecar. Its API uses a bearer token for Operator access. CUBRID HA decides which member becomes master; ordinal zero is not a permanent master. Brokers provide redundant RW and RO access in a separate tier. Object storage carries initial member copies and backup or restore artifacts. Validating the operational results of these paths remains part of the project work.
-->

---

<OperatorSlide section="5 · Data and control flow" index="06" total="10" source="DESIGN §9–10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">Data and control flow</h1><div class="op-stack"><p class="op-kicker">DATA PATH · APPLICATION SQL</p><div class="op-path"><div class="op-node ">Application</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">RW / RO Service</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Broker</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>SQL execution</small></div></div><p class="op-kicker">CONTROL PATH · INTENT AND OPERATIONS</p><div class="op-path"><div class="op-node ">CubridCluster</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Instance Manager<small>Authenticated HTTP</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>Local operations · status</small></div></div></div><p class="op-caption">Role and operation observations feed Conditions, Events and metrics. Data traffic and control information follow separate paths.</p>

</OperatorSlide>

<!--
[60s · 5 · Data and control flow]
The upper path carries application data: SQL passes through an RW or RO Service and a Broker to CUBRID. The lower path carries control: desired configuration and operations pass from CubridCluster to the Operator and Instance Managers. Observations return as Conditions, Events and metrics.

The Operator does not relay application SQL and never promotes a member. CUBRID performs role transitions. Incomplete observations cannot establish a primary, and the Operator never chooses a winner between divergent datasets. Reporting an unresolved state also does not establish that SQL writes were blocked. Enforced write quarantine needs actual connection-level validation and remains within the required recovery scope.
-->

---

<OperatorSlide section="6 · 12-week roadmap" index="07" total="10" source="ROADMAP · STP IV" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">12-week roadmap</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Scope and contracts</b><p>Scenarios and environment<br>Standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA alpha</b><p>Three members, RW/RO<br>Backup/restore alpha</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Recovery validation</b><p>Quarantine, rejoin, rebuild<br>Nov 29 target: first pass of all mandatory scenarios</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>RC and release preparation</b><p>December RC and repeated runs<br>Dec 27: v0.1 publication target</p></div></div><p class="op-caption">Oct 05–Dec 27, 2026. These are stage targets; completion depends on validation results.</p>

</OperatorSlide>

<!--
[75s · 6 · 12-week roadmap]
The season lasts twelve weeks, October 5 through December 27. Week one establishes scope, scenarios and the environment, including real standalone SQL. Weeks two through four target three-member HA, RW/RO access, representative failures and backup or restore alpha. Current observations contribute only part of that evidence.

By November 29, our target is a first pass of every mandatory scenario, including write quarantine, rejoin and rebuild. December is for a release candidate, repeated core faults, regression fixes and independently reproduced operational guidance. December 27 is the v0.1 publication target. These dates are goals, not declarations of completion. Missing mandatory evidence will remain visible; we will not reduce required scope merely to label the calendar milestone complete.
-->

---

<OperatorSlide section="6 · Team roles" index="08" total="10" source="Team profiles · Project governance" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#team-and-role-record">

<h1 class="op-title">Team roles</h1><div class="op-two"><table class="op-comparison"><thead><tr><th>Member</th><th>Current role</th></tr></thead><tbody><tr><td>Yeongseon Choe<br><small>@yeongseon</small></td><td>Co-maintainer</td></tr><tr><td>Gyeongjun Paik<br><small>@paikend</small></td><td>Co-maintainer</td></tr></tbody></table><div class="op-stack"><h3>Season work areas</h3><ul class="op-list"><li><b>Cluster and HA integration</b><small>State observations and Kubernetes resources</small></li><li><b>Backup and recovery</b><small>Failure and recovery scenarios</small></li><li><b>Documentation and publication</b><small>Installation, operations and validation results</small></li></ul></div></div><p class="op-caption">Shared design, implementation and validation, with joint review of changes and results.</p>

</OperatorSlide>

<!--
[45s · 6 · Team roles]
Yeongseon Choe and Gyeongjun Paik share the co-maintainer role across design, implementation and validation. Our season work has three areas: cluster and HA integration, backup and recovery, and documentation and publication.

We share responsibility for connecting code decisions to actual database results and making those results reproducible. Both maintainers work across scenario definition, implementation, review and documentation. We coordinate individual tasks and review around each change, keeping the season’s technical work connected to evidence others can inspect. These are the outcomes we aim to deliver together.
-->

---

<OperatorSlide section="6 · First public release scope" index="09" total="10" source="ROADMAP · v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">First public release scope</h1><div class="op-release"><div><h3>Cluster operations</h3><ul class="op-list"><li><b>Cluster lifecycle</b><small>Authenticated IM API, non-root runtime and persistent storage</small></li><li><b>Three-member HA and access</b><small>Role observations and RW/RO access</small></li></ul></div><div><h3>Failure and data recovery</h3><ul class="op-list"><li><b>Faults and write quarantine</b><small>Pod, VM, Broker and Operator faults</small></li><li><b>Rejoin, rebuild and restore</b><small>Backup and new-cluster restore</small></li></ul></div><div><h3>Operational material</h3><ul class="op-list"><li><b>Retention, security and observability</b><small>IM API auth, disruption policy, status, Events and metrics</small></li><li><b>Reproducible docs and evidence</b><small>Installation/operations guidance and required scenarios</small></li></ul></div></div><p class="op-caption">Initial target: CUBRID 11.4.x / amd64 and one Kubernetes/CSI setup. Compatible updates and disk-full tests are conditional; engine migration and broad environment support are outside the initial scope.</p>

</OperatorSlide>

<!--
[60s · 6 · First public release scope]
The first public release targets one pinned CUBRID 11.4.x, amd64, Kubernetes and CSI configuration. Required scope includes HA and RW/RO access, Pod, VM, Broker and Operator faults, write quarantine, rejoin, rebuild, backup and restore into a new cluster. Retention, IM API authentication, voluntary-disruption policy, accurate observations, operational guidance and reproducible evidence also matter.

Current local-path observations do not satisfy CSI qualification. Compatible updates and disk-full testing remain conditional; engine migration and broad platform support remain outside this first scope. Authentication here means the IM API token. The experimental version uses an empty DBA password and has no traffic encryption; it does not establish database authentication or TLS support. Publication depends on evidence for required behavior and clear support boundaries.
-->

---

<OperatorSlide section="7 · Discussion" index="10" total="10" source="Project proposal" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md">

<h1 class="op-title">Discussion</h1><ol class="op-questions"><li>Which post-fault checks or recovery steps cost your team the most work?</li><li>Which Kubernetes and CSI setup should be our first reference environment?</li><li>Who can help reproduce installation, fault and recovery scenarios?</li></ol>

</OperatorSlide>

<!--
[30s · 7 · Discussion]
We would like feedback on three concrete questions. Which post-fault checks or recovery steps create the most work for your team? Which Kubernetes and CSI combination should become our first reference environment? Who can help reproduce installation, fault and recovery scenarios? These are requests to understand real needs and find validation partners, not evidence of adoption. Thank you.
-->
