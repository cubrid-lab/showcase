<OperatorSlide section="Introduction" index="01" total="17" source="README · Experimental" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md">

<div class="op-cover"><p class="op-kicker">STP IV · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID operations,<br><span class="accent">through Kubernetes.</span></h1><p class="op-lead">Beyond starting Pods:<br>understand database state and make recovery explainable.</p><div class="op-meta"><b>CUBRID Lab</b><span>CUBRID Kubernetes Operator</span></div></div>

</OperatorSlide>

<!--
[20s · Introduction]
Hello. We are presenting the CUBRID Kubernetes Operator project from CUBRID Lab. Our question starts after deployment: how do we understand database state after a failure, and connect the recovery process to Kubernetes? This is an experimental project, and today we want to validate that direction.
-->

---

<OperatorSlide section="Team and working model" index="02" total="17" source="Governance · Two maintainers" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/governance.md#maintainer-responsibilities">

<h1 class="op-title">Two maintainers.<br><span class="accent">Build together. Review each other.</span></h1><div class="op-two"><div class="op-boundary"><b>CUBRID Lab</b><p class="op-lead">Small changes include<br>implementation, tests and review.</p></div><ul class="op-list"><li><b>Shared responsibility</b><small>Scope, architecture, contribution review and release decisions</small></li><li><b>Authors validate</b><small>The feature author supplies tests and operational evidence</small></li><li><b>A second reviewer</b><small>The other maintainer checks behavior and failure paths</small></li></ul></div>

</OperatorSlide>

<!--
[25s · Team and working model]
The documented team model has two maintainers who share responsibility for scope, architecture and releases. The author brings tests and evidence with a change, and the other maintainer reviews it. Personal names and fixed assignments still need confirmation; this slide describes the established working model rather than inventing ownership.
-->

---

<OperatorSlide section="Problem · Audience" index="03" total="17" source="README · Target-user hypothesis" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md#why-this-project">

<h1 class="op-title">Our first users:<br><span class="accent">CUBRID operators and platform teams.</span></h1><div class="op-two"><ul class="op-list"><li><b>Database operators</b><small>Decide which member roles and data can be trusted after a fault</small></li><li><b>Platform engineers</b><small>Connect Pods, storage and access paths to recovery procedures</small></li></ul><div class="op-boundary"><p class="op-lead">Turn repeated operational judgment<br>into intent, status and reproducible steps.</p></div></div><p class="op-caption">Target-user hypothesis. Real environments and priorities still need user feedback.</p>

</OperatorSlide>

<!--
[35s · Problem · Audience]
Our initial user hypothesis is database operators and platform teams running CUBRID on Kubernetes. One side must interpret roles and data after a failure; the other must coordinate Pods, storage and access. We focus on the point where these responsibilities meet. This is a proposed audience, not a claim that interviews or market adoption have already validated demand.
-->

---

<OperatorSlide section="Problem · State" index="04" total="17" source="DESIGN §4.3 · Database-aware health" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#43-database-aware">

<h1 class="op-title">A running Pod does not<br><span class="accent">establish database safety.</span></h1><div class="op-two"><div class="op-stack"><div class="op-path"><div class="op-node ">Pod 0<small>Ready</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Pod 1<small>Ready</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Pod 2<small>Ready</small></div></div><p class="op-caption">Illustration: readiness observed by Kubernetes</p></div><ul class="op-list"><li><b>Is there exactly one master?</b><small>Pod state and database role are separate observations.</small></li><li><b>Is replication progressing?</b><small>A live process does not prove logs are being applied.</small></li><li><b>Can this member rejoin safely?</b><small>A successful restart alone does not answer that question.</small></li></ul></div>

</OperatorSlide>

<!--
[35s · Problem · State]
Three Ready Pods still leave important questions unanswered. Is there one master? Are logs being applied? Can a returning member safely reuse its data? Kubernetes readiness remains useful, but it is not a complete database-level answer. The project connects that infrastructure observation to CUBRID-specific operational evidence.
-->

---

<OperatorSlide section="Existing approaches" index="05" total="17" source="Official Operator · Pinned source audit" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">Existing tools lead to<br><span class="accent">the next operational questions.</span></h1><table class="op-comparison"><thead><tr><th>Approach</th><th>What it already provides</th><th>Our investigation</th></tr></thead><tbody><tr><td>YAML / scripts</td><td>Resource and configuration deployment</td><td>What state returns after a fault?</td></tr><tr><td>Official CUBRID Operator</td><td>HA role observation, storage, scheduled backup</td><td>How should missing observations be interpreted?</td></tr><tr><td>CUBRID native HA</td><td>Replication and role transitions</td><td>How does this meet the Kubernetes lifecycle?</td></tr></tbody></table><p class="op-caption">The official Operator also observes database roles. A listening-port check alone does not establish SQL success or replica agreement.</p>

</OperatorSlide>

<!--
[35s · Existing approaches]
The official CUBRID Operator already exists, including HA role observations, Broker checks, storage and backups. Calling it deployment-only would be inaccurate. We investigate incomplete observations, real SQL outcomes and data agreement after faults. This is a source-based comparison of responsibilities, not a deployed benchmark or a claim that the official project lacks database awareness.
-->

---

<OperatorSlide section="Proposal · Intent and observation" index="06" total="17" source="DESIGN §2–4" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals">

<h1 class="op-title">Declare intent.<br><span class="accent">Continuously observe reality.</span></h1><div class="op-path"><div class="op-node project">Intent<small>CubridCluster</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Observe<small>Roles · replication · access</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Reconcile<small>Resources · operation lifecycle</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Report<small>Conditions · Events</small></div></div><p class="op-caption">Preserve CUBRID HA responsibilities while connecting them to the Kubernetes lifecycle.</p>

</OperatorSlide>

<!--
[25s · Proposal · Intent and observation]
The proposed control plane repeatedly connects intent, observations, reconciliation and status. A user declares the desired cluster; the Operator reads database and Kubernetes state, coordinates resources and operations, and reports what is known or unresolved. It preserves the engine’s HA decisions instead of replacing them.
-->

---

<OperatorSlide section="Proposal · User experience" index="07" total="17" source="DESIGN §2 · API example excerpt" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#2-goals">

<h1 class="op-title">Users describe <span class="accent">operational intent.</span></h1><div class="op-two"><pre class="op-code"><code>apiVersion: database.cubrid.io/v1alpha1
kind: CubridCluster
metadata: {name: app-db}
spec:
  version: &quot;11.4&quot;
  databases: [{name: appdb}]
  highAvailability: {enabled: true}
  topology: {promotableMembers: 3}
  storage:
    data: {size: 100Gi}</code></pre><ul class="op-list"><li><b>Database and version</b><small>appdb · CUBRID 11.4</small></li><li><b>An HA member pool</b><small>Three promotable members; master is decided at runtime</small></li><li><b>Data lifecycle</b><small>Declare persistent storage and retention/recovery policy</small></li></ul></div><p class="op-caption">Illustrative excerpt. Required HA object-storage and Secret configuration is omitted.</p>

</OperatorSlide>

<!--
[40s · Proposal · User experience]
The user describes the database, engine version, HA member pool and storage. The API does not nominate a permanent master: CUBRID decides the runtime role. This is an illustrative excerpt, not a complete runnable installation. HA also needs object storage and Secrets for bootstrap. The control plane is intended to keep observing the cluster after those resources are created.
-->

---

<OperatorSlide section="Architecture · Components" index="08" total="17" source="DESIGN §7, §9, §10" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">How the system fits together</h1><div class="op-stack"><div class="op-path"><div class="op-node ">CubridCluster<small>Kubernetes API</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator<small>Observe · reconcile</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Kubernetes resources<small>StatefulSet · Service · PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">DB MEMBERS · CUBRID NATIVE HA</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>Member 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 2 · PVC</small></div></div></div><div class="op-stack"><p class="op-kicker">SEPARATE ACCESS TIER</p><div class="op-node ">Broker tier<small>Redundant RW / RO Brokers</small></div><div class="op-node storage">Object storage<small>Bootstrap · backup · restore</small></div></div></div></div><p class="op-caption">IM is an integrated supervisor in the DB container, not a sidecar. It communicates with the Operator through an authenticated HTTP API.</p>

</OperatorSlide>

<!--
[55s · Architecture · Components]
The cluster resource enters through the Kubernetes API. The Operator coordinates resources and member operations. Each CUBRID member has persistent storage and an integrated Instance Manager in the same DB container. That authenticated HTTP API provides local operations and observations. Brokers form a separate, redundant RW/RO access tier. Object storage carries bootstrap copies and backup/restore artifacts. These are three members, not a master fixed to ordinal zero; roles are determined at runtime.
-->

---

<OperatorSlide section="Architecture · Two paths" index="09" total="17" source="DESIGN §9–10 · ADR-0002" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL goes through Brokers.<br><span class="accent">Control goes through Instance Managers.</span></h1><div class="op-stack"><p class="op-kicker">DATA PATH · APPLICATION SQL</p><div class="op-path"><div class="op-node ">Application</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">RW / RO Service</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Broker</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>SQL execution</small></div></div><p class="op-kicker">CONTROL PATH · INTENT AND OPERATIONS</p><div class="op-path"><div class="op-node ">CubridCluster</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Operator</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Instance Manager<small>Authenticated HTTP</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node engine">CUBRID<small>Local operations · status</small></div></div></div><p class="op-caption">Role and operation observations feed Conditions, Events and metrics. Data traffic and control information follow separate paths.</p>

</OperatorSlide>

<!--
[40s · Architecture · Two paths]
There are two distinct paths. Application SQL goes through stable RW/RO Services and Brokers to CUBRID. Operational intent and commands go through Kubernetes, the Operator and authenticated Instance Managers. Observations return as Conditions, Events and metrics. This keeps the existing engine and Broker responsibilities clear instead of putting the Operator in the application SQL path.
-->

---

<OperatorSlide section="Safety · Authority boundary" index="10" total="17" source="ADR-0005 · ROADMAP evidence boundary" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/adr/0005-failover-split-brain.md">

<h1 class="op-title"><span class="accent">CUBRID decides promotion.</span></h1><div class="op-two"><ul class="op-list"><li><b>CUBRID native HA</b><small>Replication and role transitions</small></li><li><b>Operator</b><small>Observe, assess state, reconcile Kubernetes resources</small></li></ul><div class="op-stack"><div class="op-node ">One master, complete observations<small>Identify the observed primary</small></div><div class="op-node project">Missing or conflicting observations<small>Remain unresolved; report ambiguity</small></div></div></div><p class="op-caption">No permanent ordinal-zero master. The Operator never promotes from incomplete evidence or chooses between divergent data sets. SQL quarantine enforcement is a separate gate.</p>

</OperatorSlide>

<!--
[45s · Safety · Authority boundary]
This boundary is central. CUBRID owns replication and role transitions. The Operator interprets observations and coordinates Kubernetes resources. If a member is unknown or multiple masters are seen, it must not invent a winner or promote a node from incomplete evidence. Ordinal zero is not permanently the master. These are authority constraints; they do not by themselves prove that SQL write quarantine is enforced.
-->

---

<OperatorSlide section="Recovery · Lifecycle" index="11" total="17" source="ADR-0006, 0008 · ROADMAP" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#v01-scope">

<h1 class="op-title">Recovery extends <span class="accent">beyond restarting.</span></h1><div class="op-stack"><div class="op-path"><div class="op-node ">Retained PVC<small>Existing data</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Verify role, logs and data</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Rejoin<small>After verification</small></div></div><div class="op-path"><div class="op-node ">Lost PVC<small>No retained data</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Explicit rebuild</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Restore member</div></div><div class="op-path"><div class="op-node ">Backup artifact</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">New-cluster bootstrap</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Verify dataset</div></div></div><p class="op-caption">Design and first-release requirements. Integrated rejoin, rebuild and backup/restore validation remain open.</p>

</OperatorSlide>

<!--
[40s · Recovery · Lifecycle]
Recovery has several paths. A member with retained data needs verification before rejoining. A member that lost its PVC needs an explicit rebuild. Backup restore is a new-cluster bootstrap workflow. These distinctions are in the design and first-release requirements. We are not claiming that every integrated recovery path has already been validated in a real environment.
-->

---

<OperatorSlide class="op-compact" section="Progress · Evidence" index="12" total="17" source="ROADMAP · Snapshot 2026-10-15" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#implementation-and-validation-inventory">

<h1 class="op-title">Separate observed evidence<br><span class="accent">from remaining validation.</span></h1><div class="op-evidence"><div><h3>Documented Kind CI scenarios</h3><ul class="op-list"><li><b>S00 · Standalone DB</b><small>Real SQL and data retained after Pod replacement</small></li><li><b>S01–S03 · HA and master Pod faults</b><small>Three-member replication, RW/RO and transaction checks</small></li><li><b>S05 · S06 · S14</b><small>Broker/Operator faults, auth, network and token rotation</small></li></ul></div><div><h3>Remaining release evidence</h3><ul class="op-list"><li><b>Quarantine, rejoin, rebuild</b><small>Actual SQL behavior, including existing connections</small></li><li><b>Backup and new-cluster restore</b><small>Artifacts and dataset verification</small></li><li><b>VM faults and reference environment</b><small>Evidence beyond Kind</small></li></ul></div></div><p class="op-boundary"><b>Write quarantine is currently reported.</b> Enforced SQL blocking is not established.</p>

</OperatorSlide>

<!--
[35s · Progress · Evidence]
The roadmap records real CUBRID scenarios in Kind for standalone persistence, HA, master Pod and Broker faults, Operator interruption, and authentication. It also records writes continuing while routing and primary Conditions were unresolved. We must distinguish reporting quarantine from enforcing it. VM failure evidence, integrated rejoin/rebuild, and complete backup/restore validation remain release work. These are documented observations, not experiments rerun for this talk.
-->

---

<OperatorSlide section="12-week roadmap" index="13" total="17" source="ROADMAP · STP IV delivery stages" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">Twelve weeks.<br><span class="accent">Verifiable outcomes at each stage.</span></h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Scope and contracts</b><p>Scenarios and environment<br>Standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA alpha</b><p>Three members, RW/RO<br>Backup/restore alpha</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Recovery validation</b><p>Write quarantine<br>Rejoin and rebuild</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Release preparation</b><p>Repeated faults and fixes<br>Runbooks and evidence</p></div></div><p class="op-caption">Oct 05–Dec 27, 2026. Delivery targets, not completion claims. Calendar pressure does not waive required safety gates.</p>

</OperatorSlide>

<!--
[40s · 12-week roadmap]
The season runs from October 5 to December 27. Week 1 settles scope, scenario contracts and the environment. Weeks 2 to 4 target HA, access paths and backup/restore alpha. Weeks 5 to 8 focus on quarantine, rejoin and rebuild validation. The last four weeks repeat failures, fix regressions and prepare reproducible documentation and release evidence. These are delivery targets, not a claim that elapsed stages automatically passed.
-->

---

<OperatorSlide section="Responsibilities and collaboration" index="14" total="17" source="ROADMAP · Two-maintainer start order" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#two-maintainer-start-order">

<h1 class="op-title">Authors validate their work.<br><span class="accent">Maintainers review each other.</span></h1><div class="op-stack"><div class="op-path"><div class="op-node ">Runtime work<small>Feature author</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Implement + test</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Other maintainer reviews</div></div><div class="op-path"><div class="op-node ">Validation work<small>Scenario author</small></div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node project">Fault injection + evidence</div><div class="op-arrow" aria-hidden="true">→</div><div class="op-node ">Independent result review</div></div></div><p class="op-boundary"><b>Assign owners per issue.</b> One active issue per person; one full VM-lab run at a time.</p>

</OperatorSlide>

<!--
[30s · Responsibilities and collaboration]
Ownership is assigned per issue rather than splitting implementation and tests between people. The author owns both, while the other maintainer reviews failure paths and expectations. Runtime, validation infrastructure and the shared lab are work streams, not three permanent people. Each maintainer normally has one active issue; full three-VM runs are serialized. Named permanent assignments remain subject to team confirmation.
-->

---

<OperatorSlide section="First public release scope" index="15" total="17" source="ROADMAP · Required / Conditional / Future" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/ROADMAP.md#v01-scope">

<h1 class="op-title">Define the <span class="accent">first release boundary.</span></h1><div class="op-release"><div><h3>Required evidence</h3><ul class="op-list"><li><b>Lifecycle, HA and RW/RO</b><small>Faults, quarantine, rejoin and rebuild</small></li><li><b>Backup and new-cluster restore</b><small>Retention, auth and disruption policy</small></li><li><b>Truthful observability</b><small>Reproducible S00–S15 and release evidence</small></li></ul></div><div><h3>Conditional</h3><ul class="op-list"><li><b>Compatible image/config updates</b><small>After required recovery gates</small></li><li><b>Disk-full testing</b><small>With enforced limits and recovery evidence</small></li></ul></div><div><h3>Outside initial scope</h3><ul class="op-list"><li><b>Engine-version migration</b><small>Non-promotable replicas</small></li><li><b>Broad environment support</b><small>Multi-zone or multi-platform guarantees</small></li></ul></div></div><p class="op-caption">Initial reference target: CUBRID 11.4.x / amd64 plus one Kubernetes/CSI configuration. Missing required evidence means v0.1 is not complete.</p>

</OperatorSlide>

<!--
[40s · First public release scope]
The first release is defined by its evidence boundary. Required work includes lifecycle, HA and access, fault recovery and quarantine, rejoin and rebuild, backup and new-cluster restore, retention, authentication and truthful observability. Compatible updates and disk-full testing have additional gates. Engine migration and broad platform support are outside the initial scope. We target one pinned environment, and will not declare v0.1 complete without the required evidence.
-->

---

<OperatorSlide section="Questions for discussion" index="16" total="17" source="README · ROADMAP · Scenario contracts" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/docs/testing/scenario-contract.md">

<h1 class="op-title">Three questions<br><span class="accent">we want to validate together.</span></h1><ol class="op-questions"><li>Which recurring CUBRID operational task should we reduce first?</li><li>Are the write-quarantine and recovery acceptance criteria sufficient?</li><li>Who can help reproduce the reference environment and runbooks?</li></ol><p class="op-caption">We want feedback on user priorities, failure criteria and independent reproduction.</p>

</OperatorSlide>

<!--
[35s · Questions for discussion]
We would like feedback on three questions. Which recurring operational task should come first? Do the quarantine and recovery criteria cover what operators need, including existing connections? And can someone independently reproduce the chosen environment and runbooks? These answers will help refine the sequence and acceptance criteria for the season, without weakening the mandatory safety requirements.
-->

---

<OperatorSlide section="Closing" index="17" total="17" source="Project · Experimental" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/f981f818029eb8c9e2fdf845edd80828b7bbb016/README.md">

<div class="op-cover"><p class="op-kicker">CUBRID KUBERNETES OPERATOR</p><h1 class="op-title">From deploying a database<br><span class="accent">to explaining its state.</span></h1><p class="op-lead">Observe state, separate responsibilities,<br>and verify recovery with real SQL and evidence.</p><div class="op-meta"><b>Experimental project</b><a href="https://github.com/cubrid-lab/cubrid-kubernetes-operator">github.com/cubrid-lab/cubrid-kubernetes-operator</a></div></div>

</OperatorSlide>

<!--
[25s · Closing]
Our goal is to move from deploying a database to explaining its operational state and recovery. We want to preserve what CUBRID HA does and validate the decisions and procedures where it meets Kubernetes. The project is experimental. We welcome review of the public design and scenario contracts. Thank you.
-->
