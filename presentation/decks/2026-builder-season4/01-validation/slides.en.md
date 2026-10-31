---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="Opening · Project and team" source="Project and team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">Running CUBRID HA on Kubernetes and confirming recovery after a fault</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div></div>

</OperatorSlide>

<!--
[20s · Opening · Project and team]
Hi, we're Yeongseon Choe and Gyeongjun Paik from CUBRID Lab. We're building an Operator to manage CUBRID, a relational DBMS, on Kubernetes. Today we have built deployment and status checking for a 3-node CUBRID HA cluster, and recovery validation is still in progress. We want the Operator to cover not just installation but also confirming recovery after a failure.

For this season, we're aiming to publish a v0.1 that we have run through in one setup: install it, cause faults, and check that it recovers. Let me start with what this Operator is.
-->

---

<OperatorSlide class="op-compact" section="Agenda · Talk outline" source="Presentation outline" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/README.md">

<h1 class="op-title">Today's outline</h1><div class="op-agenda"><div><span>01</span><b>Project and team</b><p>Project goals · co-maintainers</p></div><div><span>02</span><b>The problem</b><p>Pod recovery is not DB recovery · who has it</p></div><div><span>03</span><b>Limits of today's approach</b><p>vs the official CUBRID Operator</p></div><div><span>04</span><b>Our approach</b><p>Four checks · safety principle · recorded results</p></div><div><span>05</span><b>Architecture draft</b><p>Platforms · components · data flows</p></div><div><span>06</span><b>Roadmap and first version</b><p>12-week plan · team roles · v0.1 scope · after v0.1</p></div></div>

</OperatorSlide>

<!--
[15s · Agenda · Talk outline]
We follow the six items in the notice: the project and team, the problem, the limits of today's approach, our approach, the architecture draft, and the 12-week roadmap with the first version's scope.
-->

---

<OperatorSlide section="01 · Problem and goal">

<ChapterDivider number="01" title="The problem and the goal" subtitle="A restarted Pod does not prove database recovery" />

</OperatorSlide>

<!--
[0s · Chapter transition · Problem and goal]
Visual transition only. Move on without additional narration.
-->

---

<OperatorSlide class="op-compact" section="01 · Project and team" source="Operator README · recorded runs" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md">

<h1 class="op-title">An Operator to run CUBRID HA safely on Kubernetes</h1><p class="op-lead">The goal goes beyond automated install: confirm that the database really recovered after a fault.</p><div class="op-goals"><div><span>01</span><b>Declarative setup</b><p>One YAML file sets up a 3-node CUBRID HA cluster with RW/RO access</p></div><div><span>02</span><b>Database-aware status</b><p>Checks each node's HA role and leaves the master “unresolved” when unsure</p></div><div><span>03</span><b>Tracked backup and restore</b><p>Records each job by ID and checks files and checksums before a restore</p></div><div><span>04</span><b>Recovery checked with SQL</b><p>Judges recovery by real writes, reads and data, not by Pod status</p></div></div><p class="op-caption">Experimental and not for production · Does not replace the official CUBRID Operator · Progress on slide 10</p>

</OperatorSlide>

<!--
[40s · 01 · Project and team]
CUBRID Kubernetes Operator is an experimental Operator whose goal is to run CUBRID HA clusters safely on Kubernetes. It should not stop at automating the install: we want an operations flow that confirms the database really recovered after a fault.

There are four goals. First, one YAML file sets up a 3-node CUBRID HA cluster with write and read endpoints; these nodes are CUBRID HA database nodes, not Kubernetes worker nodes. Second, it checks each node's HA role and, when it is not sure, leaves the master unresolved instead of guessing. Third, backups and restores are tracked by job ID, and files and checksums are checked before a restore. Fourth, recovery is judged by real SQL and data, not by Pod status. I will show how far we have verified this later, with results.
-->

---

<OperatorSlide section="02 · Problem and users" source="Initial user hypotheses" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">A recovered Pod is not a recovered database</h1><p class="op-kicker">RESTARTING A POD AND ATTACHING ITS VOLUME DOES NOT SHOW THE DATABASE HAS RECOVERED</p><div class="op-scene"><div class="op-actor"><div class="op-bubble">The Pod is back.<br>Are we done?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>Kubernetes platform team</b></div><div class="op-incident"><span>⚡</span><b>Same fault</b></div><div class="op-actor op-actor-db"><div class="op-bubble">Who is master now?<br>Is the data safe?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>CUBRID database team</b></div></div><p class="op-boundary">Our goal is to let both teams confirm “recovered” from the same view.</p>

</OperatorSlide>

<!--
[40s · 02 · Problem and users]
Why does this matter? When a Pod dies, Kubernetes can start it again and reattach its volume. But a restarted Pod and an attached volume do not show that the database has recovered. You need to know who the master is now, whether you can write and read, and whether the data from before the failure is still there.

So two teams see the same fault differently. The Kubernetes platform team sees the Pod back and thinks it is done; the CUBRID team asks about the master and the data. These two teams are the first users we have in mind. We have not confirmed this through interviews, so we would like to hear about your experience today. Our goal is to let both teams confirm recovery from the same view.
-->

---

<OperatorSlide class="op-compact" section="03 · Existing approach" source="Official Operator source" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">How is it different from the official Operator?</h1><p class="op-kicker">COMPARED WITH: <a href="https://github.com/CUBRID/cubrid-operator" target="_blank">github.com/CUBRID/cubrid-operator</a></p><table class="op-comparison"><thead><tr><th></th><th>Official CUBRID Operator</th><th>CUBRID Kubernetes Operator (this project)</th></tr></thead><tbody><tr><td><b>In common</b></td><td>HA status · storage · scheduled backups</td><td>HA status · storage · backups</td></tr><tr><td><b>Finding the master</b></td><td>Uses the node info in the first successful answer</td><td>Compares fresh answers from every node · conflicts stay “unresolved”</td></tr><tr><td><b>Backup records</b></td><td>Runs a command in the Pod · records status</td><td>Asks Instance Manager · keeps the job ID on the volume</td></tr><tr><td><b>Restore</b></td><td>No restore feature found in the source</td><td>Checks file list and checksums, restores into a new cluster</td></tr><tr><td><b>Recovery check</b></td><td>Port checks</td><td>Port checks + SQL writes, reads and data in tests</td></tr></tbody></table><p class="op-caption">Compared with <a href="https://github.com/CUBRID/cubrid-operator/tree/fa7b6c2cf26096769c4404a2e2bb683f3872aa1e" target="_blank">official source fa7b6c2</a> · We have not yet tested which behaves better in real failures.</p>

</OperatorSlide>

<!--
[45s · 03 · Existing approach]
CUBRID already has an official Operator, and it provides HA status, storage and scheduled backups. So what is different? We built this table by reading both projects' source code.

In the source, the official Operator uses the node information from the first successful response for HA status. We compare fresh answers from every node and leave the master unresolved when answers are missing or conflict. Operations such as backups go through Instance Manager, and their IDs stay on the volume, so interrupted work is recorded as failed. We did not find a restore feature in the official Operator's source; before a restore we check the file list and checksums. In the source, both projects use port checks at runtime, so our tests check SQL and data separately. We have not yet compared how the two behave in real failures.
-->

---

<OperatorSlide section="02 · Approach and architecture">

<ChapterDivider number="02" title="Approach and architecture" subtitle="What the Operator observes, and what it can safely change" />

</OperatorSlide>

<!--
[0s · Chapter transition · Approach and architecture]
Visual transition only. Move on without additional narration.
-->

---

<OperatorSlide class="op-compact" section="04 · Our approach" source="What to check after a fault" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#12-failover-and-split-brain-model">

<h1 class="op-title">When the master Pod goes away, check four things</h1><p class="op-kicker">EXAMPLE: THE MASTER POD DISAPPEARS AND COMES BACK · DESIGNED FLOW</p><table class="op-comparison op-checks"><thead><tr><th>What to check</th><th>Who answers</th><th>What we look at</th></tr></thead><tbody><tr><td>① Pod availability</td><td>Kubernetes</td><td>Is the Pod Ready again? Is the volume attached?</td></tr><tr><td>② DB HA state</td><td>CUBRID HA switches<br>Operator records it</td><td>Compare every node's role<br>Missing or conflicting: “unresolved”</td></tr><tr><td>③ SQL access</td><td>Broker</td><td>Does the RW Broker reach the new master?<br>Do RW writes and RO reads work?</td></tr><tr><td>④ Data</td><td>E2E tests</td><td>Are rows committed before the fault still there?<br>The Operator does not check this itself</td></tr></tbody></table><p class="op-boundary"><b>KEY POINT</b>　We go past Pod status (①) and check HA roles, SQL access and data (② to ④) as one flow.</p>

</OperatorSlide>

<!--
[45s · 04 · Our approach]
Our approach is to split what must be checked after a fault into four parts and check them as one flow. Suppose the running master Pod disappears and comes back. First, Kubernetes tells you whether the Pod is Ready again and its volume is attached. But Pod status alone cannot tell you the HA roles, SQL access or data.

Second, CUBRID HA switches the master, and the Operator reads every node's role and compares them. If answers are missing or conflict, it does not guess; it leaves the master unresolved. Third, we check that the RW Broker reaches the new master and that writes and reads work. Fourth, whether the data committed before the fault is still there is checked by our E2E tests today. The Operator does not verify data by itself.
-->

---

<OperatorSlide section="04 · Safety principle" source="Write-quarantine evidence" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">If the master is uncertain, the Operator does not guess</h1>
<div class="op-safety">
 <div><span>WHAT WE CAN REPORT</span><h3>Keep master unresolved</h3><p>Missing or conflicting node observations must not be converted into an assumed master.</p><p class="op-mini">Status: shown as unresolved</p></div>
 <div><span>WHAT v0.1 MUST PROVE</span><h3>Block real SQL writes while unresolved</h3><p>When writes must be blocked, confirm that real client SQL writes cannot succeed through the Broker.</p><p class="op-mini">Status: to be implemented and verified</p></div>
</div>
<p class="op-boundary"><b>IMPORTANT</b>　Marking the master “unresolved” does not itself stop SQL writes.</p>

</OperatorSlide>

<!--
[35s · 04 · Safety principle]
This is a risk we want to state plainly. Our implementation can leave the master unresolved when node observations are missing or contradictory. But an unresolved Kubernetes condition is not an enforcement mechanism for SQL traffic.

In an earlier Kind test, RW writes succeeded during an unresolved-master state. Therefore, write quarantine and partition tests are mandatory release gates, not optional improvements after v0.1.
-->

---

<OperatorSlide section="04 · Recorded results" source="Recorded executions · Oct 20–25" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">What we have verified so far</h1>
<div class="op-evidence-list">
  <div><span class="op-evidence-number">27 / 27</span><div><b>Kind E2E test items passed</b><p>Recorded October 20, 2026. This counts test items, not completed required recovery scenarios.</p></div></div>
  <div><span class="op-evidence-number">RW / RO</span><div><b>VM connection and post-rollout data checks</b><p>k3s and CUBRID 11.4.6. Known volumes and rows retained; RW/RO routing and RO rejection checked. Not a VM power-loss test.</p></div></div>
  <div><span class="op-evidence-number">5 / 7</span><div><b>VM runs restoring a backup into a new cluster: 5 passed</b><p>Recorded October 25, 2026. The other 2 were blocked by a dropped session, cause under investigation (#238). A tampered backup was refused.</p></div></div>
</div>
<p class="op-boundary">The working paths are confirmed; full fault and restore testing comes next.</p>

</OperatorSlide>

<!--
[40s · 04 · Recorded results]
We are separating actual observations from targets. First, all 27 of 27 Kind E2E test items in the cited run passed on October 20. That counts test items; it is not the same as passing all mandatory scenarios S00 through S15.

Second, on k3s VMs we checked connectivity and SQL, and a controlled rollout kept known storage and rows, with RW and RO behavior checked. Third, the roadmap set an early backup-restore test for weeks 2 to 4, and on October 25 we ran it seven times on the VMs, restoring a backup into a new cluster. Five runs passed. Two were blocked when a database session dropped after the data checks had passed, and we're still looking for the cause. When we tampered with a backup file, the restore was refused. None of this guarantees recovery after arbitrary faults.
-->

---

<OperatorSlide class="op-compact" section="05 · Full architecture" source="Architecture · Broker design" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID runs HA; the Operator watches and operates</h1><svg class="op-arch" style="max-height:372px" viewBox="0 0 900 384" role="img" aria-label="Full architecture: a user applies YAML to the Kubernetes API; the Operator reads the spec, creates Kubernetes resources, asks each node Instance Manager for its role and records the result in status. Application SQL goes through RW/RO Services and Brokers to the three CUBRID HA nodes; backups go to S3-compatible storage.">
<defs><marker id="op-arch-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0f1b2d"/></marker><marker id="op-arch-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-arch-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="150" y="0" width="750" height="328" rx="10" style="fill:none;stroke-dasharray:3 4"/><text class="s" x="162" y="16">Kubernetes cluster</text>
<rect class="box" x="0" y="14" width="130" height="50" rx="8"/><text x="65" y="35" text-anchor="middle">User</text><text class="s" x="65" y="53" text-anchor="middle">kubectl · apply YAML</text>
<path class="ctl" d="M130 39H166" marker-end="url(#op-arch-blue)"/><text class="s b" x="148" y="32" text-anchor="middle">①</text>
<rect class="box" x="170" y="24" width="120" height="62" rx="8"/><text x="230" y="46" text-anchor="middle">Kubernetes API</text><text class="s" x="230" y="63" text-anchor="middle">CubridCluster</text><text class="s" x="230" y="78" text-anchor="middle">CubridBackup</text>
<path class="ctl" d="M290 44H336" marker-end="url(#op-arch-blue)"/><text class="s b" x="313" y="37" text-anchor="middle">② spec</text>
<path class="ctl" d="M338 70H292" marker-end="url(#op-arch-blue)"/><text class="s b" x="315" y="84" text-anchor="middle">④ status</text>
<rect class="box op" x="340" y="20" width="290" height="96" rx="8"/><text class="b" x="485" y="43" text-anchor="middle">CUBRID Kubernetes Operator</text><text class="s" x="485" y="64" text-anchor="middle">CubridCluster · CubridBackup controllers</text><text class="s" x="485" y="81" text-anchor="middle">HA · Services · storage · backup · updates</text><text class="s" x="485" y="101" text-anchor="middle">→ one state machine</text>
<path class="mgmt" d="M630 50H656" marker-end="url(#op-arch-mute)"/>
<rect class="box" x="660" y="24" width="228" height="62" rx="8"/><text x="774" y="46" text-anchor="middle">Observability</text><text class="s" x="774" y="63" text-anchor="middle">cubrid_cluster_* · cubrid_instance_*</text><text class="s" x="774" y="78" text-anchor="middle">Events · JSON logs</text>
<path class="mgmt" d="M400 116V136" marker-end="url(#op-arch-mute)"/><text class="s" x="392" y="131" text-anchor="end">creates · manages</text>
<path class="ctl" d="M600 116V150" marker-end="url(#op-arch-blue)"/><text class="s b" x="610" y="135">③ role reads · work requests (token auth)</text>
<rect class="box" x="170" y="138" width="262" height="84" rx="8"/><text x="301" y="159" text-anchor="middle">Kubernetes resources</text><text class="s" x="301" y="177" text-anchor="middle">StatefulSet · PVC · Secret</text><text class="s" x="301" y="194" text-anchor="middle">Services: headless · per-member alias</text><text class="s" x="301" y="211" text-anchor="middle">NetworkPolicy · Broker Deployment</text>
<rect class="box ha" x="450" y="152" width="440" height="152" rx="10"/><text x="464" y="174">CUBRID HA, 3 nodes — CUBRID elects and replicates</text>
<rect class="box ink" x="462" y="184" width="126" height="108" rx="7"/><text class="b" x="525" y="205" text-anchor="middle">node 0 · master</text><rect class="box im" x="467" y="215" width="116" height="28" rx="5"/><text class="b" x="525" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="525" y="270" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="604" y="184" width="126" height="108" rx="7"/><text x="667" y="205" text-anchor="middle">node 1 · slave</text><rect class="box im" x="609" y="215" width="116" height="28" rx="5"/><text class="b" x="667" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="667" y="270" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="746" y="184" width="126" height="108" rx="7"/><text x="809" y="205" text-anchor="middle">node 2 · slave</text><rect class="box im" x="751" y="215" width="116" height="28" rx="5"/><text class="b" x="809" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="809" y="270" text-anchor="middle">CUBRID · PVC</text>
<path class="sql" d="M588 262H602" marker-end="url(#op-arch-ink)"/><path class="sql" d="M730 262H744" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="0" y="240" width="130" height="46" rx="8"/><text x="65" y="268" text-anchor="middle">Application</text>
<path class="sql" d="M130 263H166" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="170" y="243" width="128" height="40" rx="8"/><text x="234" y="268" text-anchor="middle">RW / RO Service</text>
<path class="sql" d="M298 263H310" marker-end="url(#op-arch-ink)"/>
<rect class="box ink" x="312" y="235" width="126" height="56" rx="8"/><text x="375" y="257" text-anchor="middle">Broker (RW · RO)</text><text class="s" x="375" y="277" text-anchor="middle">RW finds the master</text>
<path class="sql" d="M438 263H458" marker-end="url(#op-arch-ink)"/>
<path class="mgmt" d="M670 304V340" marker-start="url(#op-arch-mute)" marker-end="url(#op-arch-mute)"/><text class="s" x="680" y="326">backup upload · restore</text>
<rect class="box store" x="450" y="342" width="440" height="40" rx="8"/><text x="670" y="360" text-anchor="middle">S3-compatible object storage</text><text class="s" x="670" y="376" text-anchor="middle">initial copy · backup files · file list and checksums</text>
<path class="sql" d="M0 346H40"/><text class="s" x="48" y="350">SQL path · replication (the Operator relays no SQL)</text>
<path class="ctl" d="M0 364H40"/><text class="s" x="48" y="368">operations path ①–④ (control loop on slide 12)</text>
<path class="mgmt" d="M0 382H40"/><text class="s" x="48" y="386">creates · manages · backup data · observability</text>
</svg>

</OperatorSlide>

<!--
[45s · 05 · Full architecture]
Now the architecture draft, on one page. A user applies YAML to the Kubernetes API. The Operator reads the spec and creates the StatefulSet, volumes, Secrets, Services, Brokers and NetworkPolicies. Inside the Operator, two controllers handle HA, Services, storage, backup and updates as one state machine; the next slide shows them. They ask each node's Instance Manager for its role and send work requests with token authentication, then record the result in the CubridCluster status. Metrics, Events and logs come from here too.

The solid line at the bottom is the application's SQL path: from the RW or RO Service through a Broker, which runs separately from the database, to CUBRID. The Operator relays no SQL, and CUBRID HA elects the master and replicates by itself. Initial copies and backup files go through the S3-compatible storage at the bottom right.
-->

---

<OperatorSlide class="op-compact" section="05 · Control and data flow" source="Architecture · observability · security design" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">The Operator observes, records and reconciles again</h1><p class="op-kicker">THE ①–④ CONTROL LOOP FROM SLIDE 11 AND THE DATA FLOWS · DESIGNED FLOW</p><div class="op-timeline"><div><small>① Desired state</small><b>Declared in YAML</b><p>CubridCluster · CubridBackup<br>spec</p></div><div><small>② Reconcile</small><b>Two controllers</b><p>CubridCluster · CubridBackup<br>HA · Services · storage · backup · updates<br>in one state machine</p></div><div><small>③ Observe</small><b>Instance Manager</b><p>Reads each node's HA role<br>Token auth · no pods/exec</p></div><div><small>④ Record</small><b>status · Conditions</b><p>currentPrimary<br>“unresolved” on conflict<br>Events · metrics · logs<br>→ back to ②</p></div></div><table class="op-comparison"><thead><tr><th>Data</th><th>How it flows</th></tr></thead><tbody><tr><td><b>SQL</b></td><td>App → RW/RO Service → Broker → CUBRID · CUBRID HA replicates and switches</td></tr><tr><td><b>Backup · restore</b></td><td>Instance Manager → S3-compatible storage → checksums checked → new CubridCluster</td></tr><tr><td><b>Status</b></td><td>Instance Manager → Operator → CubridCluster status · cubrid_* metrics</td></tr></tbody></table>

</OperatorSlide>

<!--
[40s · 05 · Control and data flow]
Seen as a sequence, the architecture has four steps. You declare the desired state in YAML. The Operator's two controllers handle HA, Services, storage, backup and updates as one state machine rather than separate subsystems. They ask each node's Instance Manager for its role and record the result in status and Conditions. If node answers conflict, the master is left unresolved instead of guessed, and the loop runs again.

Data takes three paths. SQL goes through the Broker to CUBRID and never through the Operator. Backups are uploaded by the Instance Manager to S3-compatible storage, and a restore checks the file list and checksums before building a new cluster. Status is collected by the Operator and shown in status and metrics. This is the designed flow; what we have actually verified is what the results slide showed.
-->

---

<OperatorSlide class="op-compact" section="05 · Inside the Operator" source="Operator source 986b775" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/tree/986b77521a1a2fa2a9da5a3ccce4e5a0c0b2fdd7/internal/controller">

<h1 class="op-title">Inside the Operator and the Instance Manager</h1><svg class="op-arch" style="max-height:384px" viewBox="0 0 900 388" role="img" aria-label="Inside the Operator: a controller-runtime manager in the Operator Pod runs the CubridCluster and CubridBackup controllers. The cluster controller reconciles Services, Secrets, ConfigMaps, NetworkPolicies and the StatefulSet in order, then handles HA status, restore, updates and Brokers, and records status. Both controllers call each DB Pod Instance Manager over HTTP with a bearer token; the Instance Manager works with CUBRID and S3-compatible storage.">
<defs><marker id="op-in-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-in-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="0" y="0" width="150" height="74" rx="8"/><text x="75" y="24" text-anchor="middle">Kubernetes API</text><text class="s" x="75" y="44" text-anchor="middle">CubridCluster</text><text class="s" x="75" y="62" text-anchor="middle">CubridBackup</text>
<path class="ctl" d="M150 28H180" marker-end="url(#op-in-blue)"/><path class="ctl" d="M180 52H152" marker-end="url(#op-in-blue)"/><text class="s b" x="0" y="92">watch: CRs + owned objects</text><text class="s b" x="0" y="110">write: status · Events</text>
<rect class="box" x="0" y="140" width="150" height="104" rx="8"/><text x="75" y="162" text-anchor="middle">Owned objects</text><text class="s" x="75" y="184" text-anchor="middle">StatefulSet · Deployment</text><text class="s" x="75" y="202" text-anchor="middle">Service · ConfigMap</text><text class="s" x="75" y="220" text-anchor="middle">Secret · NetworkPolicy</text>
<path class="mgmt" d="M182 192H154" marker-end="url(#op-in-mute)"/>
<rect class="box" x="0" y="262" width="150" height="66" rx="8"/><text x="75" y="284" text-anchor="middle">Observability</text><text class="s" x="75" y="303" text-anchor="middle">cubrid_* metrics</text><text class="s" x="75" y="320" text-anchor="middle">Events · JSON logs</text>
<path class="mgmt" d="M182 296H154" marker-end="url(#op-in-mute)"/>
<rect class="box op" x="170" y="0" width="460" height="388" rx="10" style="fill:none"/><text class="b" x="184" y="20">Operator Pod</text><text class="s" x="184" y="36">controller-runtime manager · leader election · metrics · health probe</text>
<rect class="box op" x="182" y="46" width="436" height="214" rx="8"/><text x="196" y="66">CubridClusterReconciler <tspan class="s" style="font-weight:400;fill:#5b6b82">(in order)</tspan></text><text class="s" x="196" y="88">1. Services: headless · per-member alias</text><text class="s" x="196" y="110">2. Instance Manager token Secret · HA config ConfigMap</text><text class="s" x="196" y="132">3. NetworkPolicies · StatefulSet</text><text class="s" x="196" y="154">4. HA bootstrap → per-member role reads → master decision</text><text class="s" x="196" y="176">5. restore from backup · engine version guard · slaves-first rollout</text><text class="s" x="196" y="198">6. Broker tier and Broker Conditions</text><text class="s" x="196" y="220">7. status · Conditions · Events · metrics</text>
<rect class="box op" x="182" y="268" width="436" height="56" rx="8"/><text x="196" y="288">CubridBackupReconciler</text><text class="s" x="196" y="310">pick target (role reads) → backup (idempotency key) → poll → record</text>
<rect class="box im" x="182" y="332" width="436" height="48" rx="8"/><text class="b" x="196" y="351">Instance Manager client</text><text class="s" x="196" y="370">role reads · backup and restore requests · HTTP + bearer token from a Secret</text>
<path class="ctl" d="M618 356H644V120H668" marker-end="url(#op-in-blue)"/>
<rect class="box ha" x="660" y="0" width="240" height="306" rx="10"/><text x="672" y="20">DB Pod (each HA node)</text>
<rect class="box im" x="672" y="30" width="216" height="198" rx="8"/><text class="b" x="684" y="52">Instance Manager</text><text class="s" x="684" y="74">GET /v1/role · /v1/ha/status</text><text class="s" x="684" y="93">GET /v1/ha/convergence</text><text class="s" x="684" y="112">POST /v1/ha/bootstrap · /v1/backup</text><text class="s" x="684" y="131">POST /v1/restore/prepare</text><text class="s" x="684" y="150">GET /v1/operations</text><text class="s" x="684" y="169">POST /v1/shutdown</text><text class="s" x="684" y="188">operation records · volume lock</text><text class="s" x="684" y="207">upload and verify · watchdog</text>
<path class="mgmt" d="M780 228V238" marker-end="url(#op-in-mute)"/>
<rect class="box ink" x="672" y="240" width="216" height="54" rx="8"/><text x="780" y="262" text-anchor="middle">CUBRID</text><text class="s" x="780" y="282" text-anchor="middle">DB server · HA · data volume</text>
<path class="mgmt" d="M780 306V334" marker-start="url(#op-in-mute)" marker-end="url(#op-in-mute)"/><text class="s" x="790" y="324">upload · restore prep</text>
<rect class="box store" x="660" y="336" width="240" height="48" rx="8"/><text x="780" y="356" text-anchor="middle">S3-compatible storage</text><text class="s" x="780" y="374" text-anchor="middle">backup files · file list and checksums</text>
</svg>

</OperatorSlide>

<!--
[35s · 05 · Inside the Operator]
A closer look inside the Operator, as the code stands today. In the Operator Pod, a controller-runtime manager runs two controllers. The CubridCluster controller works in the same order every time: Services, the token Secret and HA configuration, NetworkPolicies and the StatefulSet; then HA bootstrap and per-member role reads to decide the master; then restore, rolling updates and Brokers; and finally status, Conditions, Events and metrics. The CubridBackup controller picks a target member, requests the backup and records the result.

Both controllers call each DB Pod's Instance Manager over HTTP with a token from a Secret. The Instance Manager handles role reads, HA bootstrap, backup, restore preparation and shutdown, and keeps an operation record on the volume so an interrupted job can be found again.
-->

---

<OperatorSlide section="03 · Validation and next steps">

<ChapterDivider number="03" title="Validation and next steps" subtitle="Test recovery and safety before expanding features" />

</OperatorSlide>

<!--
[0s · Chapter transition · Validation and next steps]
Visual transition only. Move on without additional narration.
-->

---

<OperatorSlide section="06 · Twelve-week plan" source="Schedule" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">Targets: one full pass in November, repeats in December</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Choose the setup</b><p>Set environment and scenarios<br>Check standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA and the test setup</b><p>3-node HA · RW/RO<br>Run on VMs<br>Try backup and recovery</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Test faults and recovery</b><p>Block writes · rejoin<br>Rebuild · restore backups<br>Aim for a first full pass</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Repeat on one candidate</b><p>Repeat faults<br>24h load target<br>Someone else tries the docs<br>Fix issues · release files</p></div></div><p class="op-boundary"><b>11.29</b> Aim: first pass of every required scenario　→　<b>12.27</b> v0.1 publication target</p>

</OperatorSlide>

<!--
[40s · 06 · Twelve-week plan]
We've planned twelve weeks, from October 5 to December 27. The first week is for choosing the environment and scenarios and checking SQL on a standalone database. Weeks two through four cover 3-node HA, RW/RO, running on VMs, and initial backup and recovery tests. The Kind and VM results we just showed come from that stage.

By the end of November, specifically November 29, we want every required scenario to have passed once. That includes blocking writes, rejoining, rebuilding, and restoring a new cluster from a backup. In December, we want to repeat fault tests on the same release candidate, try a 24-hour load test, and have someone else follow the documentation. We'll fix what those tests find, aiming to publish on December 27. The test results will determine whether we're ready to publish.
-->

---

<OperatorSlide section="06 · Team roles" source="Team" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">Two maintainers who check each other</h1><div class="op-meta"><b>Yeongseon Choe @yeongseon</b><b>Gyeongjun Paik @paikend</b><span>Co-maintainers</span></div><table class="op-comparison"><thead><tr><th>Who</th><th>What they do</th></tr></thead><tbody><tr><td>The issue owner</td><td>Reproduce the problem; write code, tests, docs and experiment records</td></tr><tr><td>The other person</td><td>Review the code and check the results</td></tr><tr><td>Together</td><td>Test installation, HA and recovery; decide whether to release</td></tr></tbody></table><p class="op-boundary">The author is never the final reviewer; we decide on a release together.</p>

</OperatorSlide>

<!--
[25s · 06 · Team roles]
The two of us develop this together. We assign an owner to each issue. That person takes it from reproducing the problem through code, tests, documentation and experiment records. The other person reviews the change and checks the results.

We use the same approach for HA, backup and recovery, and installation docs. VM fault tests share one environment, so we run them one at a time. Before release, we'll also check that the other maintainer can complete installation and recovery from the docs alone.
-->

---

<OperatorSlide section="06 · v0.1 required tests" source="v0.1 validation gates" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">Before v0.1, we check it stays safe during faults</h1>
<div class="op-gates">
  <div><span>01 · BLOCK WRITES</span><b>When the master is uncertain or the network splits</b><p>Do real SQL writes stop when writes must not be accepted?</p></div>
  <div><span>02 · REJOIN AND REBUILD</span><b>When a failed node rejoins or is rebuilt</b><p>Can a failed node return without overwriting healthy nodes or committed data?</p></div>
  <div><span>03 · REPEATED RESTORE</span><b>When restores repeat or are interrupted</b><p>Does the data still match after many runs, or a restart in the middle of a restore?</p></div>
  <div><span>04 · REPRODUCE</span><b>When someone else follows the docs</b><p>Can another maintainer repeat the result on one defined stack?</p></div>
</div>
<p class="op-boundary">These four, along with every other required scenario, must pass before we publish v0.1.</p>

</OperatorSlide>

<!--
[40s · 06 · v0.1 required tests]
The next work targets fault conditions. Write quarantine must be enforced during uncertain HA states. A failed node that rejoins or is rebuilt must not damage valid data. As I mentioned, restoring a backup into a new cluster passed in 5 of 7 early VM runs. Next we need to find why the sessions dropped and repeat it under more conditions.

We also need an explicit Kubernetes and CSI environment and independent runbook reproduction. Those are acceptance gates for the initial release, not evidence we already have.
-->

---

<OperatorSlide class="op-compact" section="06 · v0.1 scope" source="v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">What goes into v0.1</h1><table class="op-comparison op-acceptance"><thead><tr><th>What is included</th><th>How we will check it</th></tr></thead><tbody><tr><td>Non-root · persistent DB<br>3-node HA · RW/RO</td><td>Run SQL; check roles, commits and data</td></tr><tr><td>Faults · block writes<br>Rejoin · rebuild</td><td>Check state and data after Pod/VM/Broker/Operator faults</td></tr><tr><td>Backup<br>Restore to a new cluster</td><td>Build a new cluster from a backup and compare data</td></tr><tr><td>Retention · Instance Manager auth<br>Kubernetes node maintenance · status · metrics</td><td>Run the required scenarios; follow installation, operations and recovery docs</td></tr></tbody></table><p class="op-boundary"><b>ALSO PUBLISH</b> Images · install manifests · supported setups · operations docs · test results</p><p class="op-caption">Supported: CUBRID 11.4.x · amd64 · one Kubernetes and storage setup · experimental · DB password and TLS after v0.1</p>

</OperatorSlide>

<!--
[40s · 06 · v0.1 scope]
For v0.1, we aim to choose one environment and test everything from installation to recovery. We'll run SQL through 3-node HA and RW/RO, then check roles and data after faults. Rejoining or rebuilding must not overwrite good data. When we restore a new cluster from a backup, we'll compare it with a dataset prepared in advance. We also need to check retention, Instance Manager authentication, Kubernetes node-disruption policy, status and metrics.

We want to publish the images, install manifests, supported-environment table, operations docs and test results together. The starting setup is CUBRID 11.4.x, amd64, and one Kubernetes/CSI combination. Our current VMs use local-path, so CSI still needs its own tests. This first version is experimental. Instance Manager has authentication, but the DBA password is currently empty and traffic is unencrypted. Compatible updates and disk-full tests are conditional too.
-->

---

<OperatorSlide section="06 · After v0.1" source="After v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">After v0.1</h1><div class="op-release"><div><h3>First, fix what people run into while using it</h3><ul class="op-list"><li><b>Improve logs and diagnostics</b><small>Work on recurring issues and recovery steps</small></li><li><b>Features needed for actual use</b><small>DB authentication · TLS · compatible updates</small></li></ul></div><div><h3>Then, try more setups</h3><ul class="op-list"><li><b>More Kubernetes/CSI combinations</b><small>Test faults and recovery in each</small></li><li><b>arm64 · multiple availability zones</b><small>Check support separately</small></li></ul></div><div><h3>Work that will take longer · not scheduled</h3><ul class="op-list"><li><b>Changing CUBRID versions</b><small>Data compatibility, downtime and how to roll back</small></li><li><b>More replication setups</b><small>For example, non-promotable replicas</small></li></ul></div></div><p class="op-boundary">We will test v0.1 first, then decide what matters most from the problems people find.</p>

</OperatorSlide>

<!--
[20s · 06 · After v0.1]
Once the first version is out, we'll fix what people run into first: logs, recovery steps, database authentication and TLS.

Then we'll add Kubernetes and CSI combinations one at a time, testing faults and recovery in each. We haven't set a next version or date.
-->

---

<OperatorSlide section="Q&amp;A" source="Expected questions" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">Thank you</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab is independently maintained and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project.</p></div>

</OperatorSlide>

<!--
[15s · Q&A]
Thank you. We are happy to take your questions. We would also like to hear what you check first after a fault, and which Kubernetes CSI driver v0.1 should support first.
-->
