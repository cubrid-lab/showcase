---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="Opening · Project and team" index="01" total="15" source="Project and team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">CUBRID on Kubernetes, from installation to verified recovery</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div></div>

</OperatorSlide>

<!--
[20s · Opening · Project and team]
Hi, we're Yeongseon Choe and Gyeongjun Paik from CUBRID Lab. We're building an Operator to manage CUBRID, a relational DBMS, on Kubernetes. We want it to cover installation and what happens when something fails and has to recover.

For this season, we're aiming for a v0.1 that we've run through in one setup: install it, cause faults, and check that it recovers. Let me start with what this Operator is.
-->

---

<OperatorSlide class="op-compact" section="1 · What it is" index="02" total="15" source="Operator README · recorded runs" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/README.md">

<h1 class="op-title">An Operator that runs CUBRID HA clusters on Kubernetes</h1><p class="op-lead">Describe the cluster in YAML. The Operator creates it, watches it, and coordinates backup and restore.</p><table class="op-comparison op-capabilities"><thead><tr><th>What it does</th><th>Where it stands</th></tr></thead><tbody><tr><td>Creates a 3-member HA cluster with RW/RO<small>CubridCluster</small></td><td><span class="op-status done">Verified</span>Install and access on Kind and VMs; data kept after rollout</td></tr><tr><td>Reads each member's role into the status<small>Conflicting answers stay “unresolved”</small></td><td><span class="op-status">Built</span>Blocking RW writes during faults: not yet built or verified</td></tr><tr><td>Backs up and restores into a new cluster<small>CubridBackup · object storage</small></td><td><span class="op-status">First pass</span>5 of 7 VM runs passed; 2 inconclusive</td></tr><tr><td>Rejoins and rebuilds members after faults</td><td><span class="op-status plan">v0.1 goal</span>Rejoin and rebuild tests not yet run</td></tr></tbody></table><p class="op-caption">Experimental and not for production. It does not replace the official CUBRID Operator.</p>

</OperatorSlide>

<!--
[45s · 1 · What it is]
CUBRID Kubernetes Operator is an experimental Operator for deploying and running CUBRID HA clusters on Kubernetes. You describe the cluster you want in YAML. The Operator creates a three-member HA cluster with write and read endpoints, reads each member's role and records it in the status. It also takes backups and restores them into a new cluster.

The right column shows where we stand. We have verified installation and access ourselves, and restoring a backup into a new cluster has passed for the first time. Role tracking is built, but blocking writes during a fault is not yet. Rejoining and rebuilding members after faults is a v0.1 goal. This is not for production, and it is not meant to replace the official Operator.
-->

---

<OperatorSlide section="1 · Why it matters" index="03" total="15" source="Initial user hypotheses" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title" style="font-size: 2.4rem">A recovered Pod is not a recovered database</h1><p class="op-kicker">KUBERNETES BRINGS BACK PODS AND VOLUMES · A DATABASE ALSO NEEDS ROLES, ACCESS AND DATA</p><div class="op-scene"><div class="op-actor"><div class="op-bubble">The Pod is back.<br>Are we done?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>Kubernetes platform team</b></div><div class="op-incident"><span>⚡</span><b>Same fault</b></div><div class="op-actor op-actor-db"><div class="op-bubble">Who is master now?<br>Is the data safe?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>CUBRID database team</b></div></div><p class="op-boundary">Our goal is to let both teams confirm “recovered” from the same view.</p>

</OperatorSlide>

<!--
[40s · 1 · Why it matters]
Why does this matter? When a Pod dies, Kubernetes starts it again and reattaches its volume. But a recovered database service means more than that. You need to know who the master is now, whether you can write and read, and whether the data from before the failure is still there.

So two teams see the same fault differently. The Kubernetes platform team sees the Pod back and thinks it is done; the CUBRID team asks about the master and the data. These two teams are the first users we have in mind. We have not confirmed this through interviews, so we would like to hear about your experience today. Our goal is to let both teams confirm recovery from the same view.
-->

---

<OperatorSlide class="op-compact" section="2 · Architecture" index="04" total="15" source="Architecture · Broker design" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID runs HA; the Operator observes</h1><svg class="op-arch" viewBox="0 0 880 352" role="img" aria-label="Operator architecture: an operations path from YAML through the Kubernetes API and the Operator to Kubernetes resources, and an SQL path from the application through RW/RO Services and Brokers to three CUBRID HA members. Each member has an Instance Manager and a PVC and connects to backup storage.">
<defs><marker id="op-arch-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0f1b2d"/></marker><marker id="op-arch-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-arch-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="0" y="8" width="150" height="62" rx="8"/><text x="75" y="29" text-anchor="middle">YAML</text><text class="s" x="75" y="47" text-anchor="middle">CubridCluster</text><text class="s" x="75" y="62" text-anchor="middle">CubridBackup</text>
<rect class="box" x="180" y="8" width="150" height="62" rx="8"/><text x="255" y="44" text-anchor="middle">Kubernetes API</text>
<rect class="box op" x="360" y="8" width="200" height="62" rx="8"/><text class="b" x="460" y="33" text-anchor="middle">Operator</text><text class="s" x="460" y="54" text-anchor="middle">Observes and reconciles</text>
<rect class="box" x="590" y="8" width="290" height="62" rx="8"/><text x="735" y="33" text-anchor="middle">Kubernetes resources</text><text class="s" x="735" y="54" text-anchor="middle">StatefulSet · Broker · Service · PVC</text>
<path class="ctl" d="M150 39H176" marker-end="url(#op-arch-blue)"/><path class="ctl" d="M330 39H356" marker-end="url(#op-arch-blue)"/><path class="ctl" d="M560 39H586" marker-end="url(#op-arch-blue)"/>
<path class="ctl" d="M440 70V108" marker-end="url(#op-arch-blue)"/><text class="s b" x="450" y="94">Work and role reads via Instance Manager</text>
<path class="mgmt" d="M800 70V108" marker-end="url(#op-arch-mute)"/><text class="s" x="790" y="94" text-anchor="end">Creates · manages</text>
<rect class="box ha" x="330" y="112" width="550" height="150" rx="10"/><text x="346" y="136">CUBRID HA elects the master and replicates by itself</text>
<rect class="box ink" x="346" y="148" width="168" height="104" rx="7"/><text x="430" y="171" text-anchor="middle">Member 0</text><rect class="box im" x="358" y="182" width="144" height="30" rx="5"/><text class="b" x="430" y="202" text-anchor="middle" style="font-size:13px">Instance Manager</text><text class="s" x="430" y="238" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="523" y="148" width="168" height="104" rx="7"/><text x="607" y="171" text-anchor="middle">Member 1</text><rect class="box im" x="535" y="182" width="144" height="30" rx="5"/><text class="b" x="607" y="202" text-anchor="middle" style="font-size:13px">Instance Manager</text><text class="s" x="607" y="238" text-anchor="middle">CUBRID · PVC</text>
<rect class="box ink" x="700" y="148" width="168" height="104" rx="7"/><text x="784" y="171" text-anchor="middle">Member 2</text><rect class="box im" x="712" y="182" width="144" height="30" rx="5"/><text class="b" x="784" y="202" text-anchor="middle" style="font-size:13px">Instance Manager</text><text class="s" x="784" y="238" text-anchor="middle">CUBRID · PVC</text>
<rect class="box" x="0" y="112" width="230" height="40" rx="8"/><text x="115" y="137" text-anchor="middle">Application</text>
<path class="sql" d="M115 152V166" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="0" y="168" width="230" height="40" rx="8"/><text x="115" y="193" text-anchor="middle">RW / RO Service</text>
<path class="sql" d="M115 208V220" marker-end="url(#op-arch-ink)"/>
<rect class="box ink" x="0" y="222" width="230" height="52" rx="8"/><text x="115" y="243" text-anchor="middle">Broker (RW · RO)</text><text class="s" x="115" y="263" text-anchor="middle">Separate from DB · RW finds the master</text>
<path class="sql" d="M230 242H326" marker-end="url(#op-arch-ink)"/><text x="278" y="233" text-anchor="middle" style="font-size:13px">SQL</text>
<rect class="box store" x="330" y="296" width="550" height="48" rx="8"/><text x="605" y="317" text-anchor="middle">Backup storage</text><text class="s" x="605" y="335" text-anchor="middle">S3-compatible object storage · initial copy · backup · restore</text>
<path class="mgmt" d="M605 266V292" marker-start="url(#op-arch-mute)" marker-end="url(#op-arch-mute)"/>
<path class="sql" d="M0 306H40"/><text class="s" x="48" y="310">SQL path · the Operator does not relay SQL</text>
<path class="ctl" d="M0 330H40"/><text class="s" x="48" y="334">Operations path · settings, work, status</text>
</svg>

</OperatorSlide>

<!--
[50s · 2 · Architecture]
Here is the whole picture. The blue dashed line at the top is the operations path. You apply YAML to the Kubernetes API, and the Operator creates the StatefulSet, Brokers, Services and volumes. It asks the Instance Manager inside each member to do work such as starting the database or taking a backup, and it reads each member's role into the status.

The solid line on the left is the application's SQL path: an RW or RO Service, then a Broker that runs separately from the database, then CUBRID. The RW Broker finds the master by itself, so the Operator never relays SQL. CUBRID HA elects the master and replicates; the Operator does not pick the master during failover. Initial data copies and backup files go through the object storage at the bottom.
-->

---

<OperatorSlide class="op-compact" section="2 · Example failure" index="05" total="15" source="What to check after a fault" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#12-failover-and-split-brain-model">

<h1 class="op-title">When the master Pod goes away, check four things</h1><p class="op-kicker">EXAMPLE: THE MASTER POD DISAPPEARS AND COMES BACK · DESIGNED FLOW</p><table class="op-comparison op-checks"><thead><tr><th>What to check</th><th>Who answers</th><th>What we look at</th></tr></thead><tbody><tr><td>① Pod availability</td><td>Kubernetes</td><td>Is the Pod Ready again? Is the volume attached?</td></tr><tr><td>② DB HA state</td><td>CUBRID HA switches<br>Operator records it</td><td>Compare every member's role<br>Missing or conflicting: “unresolved”</td></tr><tr><td>③ SQL access</td><td>Broker</td><td>Does the RW Broker reach the new master?<br>Do RW writes and RO reads work?</td></tr><tr><td>④ Data</td><td>E2E tests</td><td>Are rows committed before the fault still there?<br>The Operator does not check this itself</td></tr></tbody></table><p class="op-boundary"><b>Kubernetes monitoring stops at ①</b>　Checking ② to ④ as one flow is the core of this project.</p>

</OperatorSlide>

<!--
[45s · 2 · Example failure]
Now suppose the master Pod in this setup disappears and comes back. There are four things to check. First, Kubernetes tells you whether the Pod is Ready again and its volume is attached. Ordinary Kubernetes monitoring stops there.

Second, CUBRID HA switches the master, and the Operator reads every member's role and compares them. If answers are missing or conflict, it does not guess; it leaves the master unresolved. Third, we check that the RW Broker reaches the new master and that writes and reads work. Fourth, whether the data committed before the fault is still there is checked by our E2E tests today. The Operator does not verify data by itself.
-->

---

<OperatorSlide section="2 · Failure-safety principle" index="06" total="15" source="Write-quarantine evidence" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Unknown master: safety before success</h1>
<div class="op-safety">
 <div><span>WHAT WE CAN REPORT</span><h3>Keep master unresolved</h3><p>Missing or conflicting member observations must not be converted into an assumed master.</p><p class="op-mini">Status: uncertainty is visible</p></div>
 <div><span>WHAT v0.1 MUST PROVE</span><h3>Enforce RW write quarantine</h3><p>When writes must be blocked, confirm that real client SQL cannot succeed through Broker.</p><p class="op-mini">Status: not yet implemented or verified</p></div>
</div>
<p class="op-boundary"><b>IMPORTANT</b>　Marking a condition “unknown” does not itself stop SQL writes.</p>

</OperatorSlide>

<!--
[35s · 2 · Failure-safety principle]
This is a risk we want to state plainly. Our implementation can leave master unresolved when member observations are missing or contradictory. But an unresolved Kubernetes condition is not an enforcement mechanism for SQL traffic.

In an earlier Kind test, RW writes succeeded during an unresolved-master state. Therefore, write quarantine and partition tests are mandatory release gates, not optional improvements after v0.1.
-->

---

<OperatorSlide class="op-compact" section="2 · Compared with existing" index="07" total="15" source="Official Operator source" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">An official Operator exists. What is different?</h1><p class="op-kicker">THE OFFICIAL CUBRID OPERATOR ALSO PROVIDES HA STATUS · STORAGE · SCHEDULED BACKUPS</p><table class="op-comparison"><thead><tr><th></th><th>Official Operator (today)</th><th>What we change</th></tr></thead><tbody><tr><td><b>Finding the master</b></td><td>Uses the node list from<br>the first member that answers</td><td>Compares fresh answers from every member<br>Missing or conflicting: marked “unresolved”</td></tr><tr><td><b>Tracking backup work</b></td><td>Runs scheduled backups as a command in the Pod<br>Records backup status</td><td>Sends the request to Instance Manager; keeps its ID on the volume<br>Work cut off by a restart stays “Failed”</td></tr><tr><td><b>Restore</b></td><td>No restore feature found in the source<br>(backups only)</td><td>Checks the file list and checksums first<br>Always restores into a new cluster</td></tr><tr><td><b>Recovery check</b></td><td>Port checks</td><td>Same port checks<br>Tests also run real SQL writes, reads and data checks</td></tr></tbody></table><p class="op-caption">Compared from the source versions we reviewed. We have not yet tested which behaves better in real failures.</p>

</OperatorSlide>

<!--
[50s · 2 · Compared with existing]
CUBRID already has an official Operator, and it provides HA status, storage and scheduled backups. So what is different? We built this table by reading both projects' source code.

The official Operator takes the master from the first member that answers. We compare fresh answers from every member and leave the master unresolved when answers are missing or conflict. Operations such as backups go through Instance Manager, and their IDs stay on the volume, so interrupted work is recorded as failed. We did not find a restore feature in the official Operator's source; before a restore we check the file list and checksums. Both projects use port checks at runtime, so our tests check SQL and data separately. We have not yet compared how the two behave in real failures.
-->

---

<OperatorSlide section="3 · Recorded evidence" index="08" total="15" source="Recorded executions · Oct 20–25" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Here is what we have actually verified so far</h1>
<div class="op-evidence-list">
  <div><span class="op-evidence-number">27 / 27</span><div><b>Kind end-to-end test specs passed</b><p>Recorded October 20, 2026. Specs are not the required release scenarios.</p></div></div>
  <div><span class="op-evidence-number">RW / RO</span><div><b>VM connection and post-rollout data checks</b><p>k3s and CUBRID 11.4.6. Known volumes and rows retained; RW/RO routing and RO rejection checked. Not a VM power-loss test.</p></div></div>
  <div><span class="op-evidence-number">5 / 7</span><div><b>Backup restores into a new cluster passed on VMs</b><p>Recorded October 25, 2026. The other 2 were blocked by a dropped session, cause under investigation (#238). A tampered backup was refused.</p></div></div>
</div>
<p class="op-boundary">The working paths are confirmed; full fault and restore testing comes next.</p>

</OperatorSlide>

<!--
[40s · 3 · Recorded evidence]
We are separating actual observations from targets. First, all 27 Kind E2E specs in the cited run passed on October 20. This is not the same as passing all mandatory scenarios S00 through S15.

Second, on k3s VMs we checked connectivity and SQL, and a controlled rollout kept known storage and rows, with RW and RO behavior checked. Third, the roadmap set an early backup-restore test for weeks 2 to 4, and on October 25 we ran it seven times on the VMs, restoring a backup into a new cluster. Five runs passed. Two were blocked when a database session dropped after the data checks had passed, and we're still looking for the cause. When we tampered with a backup file, the restore was refused. None of this guarantees recovery after arbitrary faults.
-->

---

<OperatorSlide section="3 · Next validation" index="09" total="15" source="v0.1 validation gates" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">Next, we will test the moments that can go wrong</h1>
<div class="op-gates">
  <div><span>01 · SAFE WRITES</span><b>Unknown master / network partition</b><p>Does client SQL stop when writes must not be accepted?</p></div>
  <div><span>02 · RECOVERY</span><b>Rejoin and rebuild</b><p>Can a failed member return without overwriting correct data?</p></div>
  <div><span>03 · RESTORE</span><b>Repeated and interrupted restores</b><p>Does the data still match after many runs, or a restart in the middle of a restore?</p></div>
  <div><span>04 · REPRODUCE</span><b>Storage and independent runbooks</b><p>Can another maintainer repeat the result on one defined stack?</p></div>
</div>
<p class="op-boundary">These four, along with every other required scenario, must pass before we publish v0.1.</p>

</OperatorSlide>

<!--
[40s · 3 · Next validation]
The next work targets fault conditions. Write quarantine must be enforced during uncertain HA states. Rejoining or rebuilding must not damage valid data. As I mentioned, restoring a backup into a new cluster has passed for the first time. Next we need to find why the sessions dropped and repeat it under more conditions.

We also need an explicit Kubernetes and CSI environment and independent runbook reproduction. Those are acceptance gates for the initial release, not evidence we already have.
-->

---

<OperatorSlide section="3 · Twelve-week roadmap" index="10" total="15" source="Schedule" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">November: one full pass. December: repeat.</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Choose the setup</b><p>Set environment and scenarios<br>Check standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA and the test setup</b><p>Three members · RW/RO<br>Run on VMs<br>Try backup and recovery</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Test faults and recovery</b><p>Block writes · rejoin<br>Rebuild · restore backups<br>Aim for a first full pass</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Repeat on one candidate</b><p>Repeat faults<br>24h load target<br>Someone else tries the docs<br>Fix issues · release files</p></div></div><p class="op-boundary"><b>11.29</b> Aim: first pass of every required scenario　→　<b>12.27</b> v0.1 publication target</p>

</OperatorSlide>

<!--
[40s · 3 · Twelve-week roadmap]
We've planned twelve weeks, from October 5 to December 27. The first week is for choosing the environment and scenarios and checking SQL on a standalone database. Weeks two through four cover three-member HA, RW/RO, running on VMs, and initial backup and recovery tests. The Kind and VM results we just showed come from that stage.

By the end of November, specifically November 29, we want every required scenario to have passed once. That includes blocking writes, rejoining, rebuilding, and restoring a new cluster from a backup. In December, we want to repeat fault tests on the same release candidate, try a 24-hour load test, and have someone else follow the documentation. We'll fix what those tests find, aiming to publish on December 27. The test results will determine whether we're ready to publish.
-->

---

<OperatorSlide section="3 · Collaboration" index="11" total="15" source="Team" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">Two maintainers, independent checks</h1><div class="op-meta"><b>Yeongseon Choe @yeongseon</b><b>Gyeongjun Paik @paikend</b><span>Co-maintainers</span></div><table class="op-comparison"><thead><tr><th>Who</th><th>What they do</th></tr></thead><tbody><tr><td>The issue owner</td><td>Reproduce the problem; write code, tests, docs and experiment records</td></tr><tr><td>The other person</td><td>Review the code and check the results</td></tr><tr><td>Together</td><td>Test installation, HA and recovery; decide whether to release</td></tr></tbody></table><p class="op-boundary">The author is never the final reviewer; we decide on a release together.</p>

</OperatorSlide>

<!--
[25s · 3 · Collaboration]
The two of us develop this together. We assign an owner to each issue. That person takes it from reproducing the problem through code, tests, documentation and experiment records. The other person reviews the change and checks the results.

We use the same approach for HA, backup and recovery, and installation docs. VM fault tests share one environment, so we run them one at a time. Before release, we'll also check that the other maintainer can complete installation and recovery from the docs alone.
-->

---

<OperatorSlide class="op-compact" section="4 · v0.1 scope" index="12" total="15" source="v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">What goes into v0.1</h1><table class="op-comparison op-acceptance"><thead><tr><th>What is included</th><th>How we will check it</th></tr></thead><tbody><tr><td>Non-root · persistent DB<br>Three-member HA · RW/RO</td><td>Run SQL; check roles, commits and data</td></tr><tr><td>Faults · block writes<br>Rejoin · rebuild</td><td>Check state and data after Pod/VM/Broker/Operator faults</td></tr><tr><td>Backup<br>Restore to a new cluster</td><td>Build a new cluster from a backup and compare data</td></tr><tr><td>Retention · Instance Manager auth<br>Node maintenance · status · metrics</td><td>Run the required scenarios; follow installation, operations and recovery docs</td></tr></tbody></table><p class="op-boundary"><b>ALSO PUBLISH</b> Images · install manifests · supported setups · operations docs · test results</p><p class="op-caption">Supported: CUBRID 11.4.x · amd64 · one Kubernetes and storage setup · experimental · DB password and TLS after v0.1</p>

</OperatorSlide>

<!--
[40s · 4 · v0.1 scope]
For v0.1, we'll choose one environment and test everything from installation to recovery. We'll run SQL through three-member HA and RW/RO, then check roles and data after faults. Rejoining or rebuilding must not overwrite good data. When we restore a new cluster from a backup, we'll compare it with a dataset prepared in advance. We also need to check retention, Instance Manager authentication, node-disruption policy, status and metrics.

We want to publish the images, install manifests, supported-environment table, operations docs and test results together. The starting setup is CUBRID 11.4.x, amd64, and one Kubernetes/CSI combination. Our current VMs use local-path, so CSI still needs its own tests. This first version is experimental. Instance Manager has authentication, but the DBA password is currently empty and traffic is unencrypted. Compatible updates and disk-full tests are conditional too.
-->

---

<OperatorSlide section="4 · After v0.1" index="13" total="15" source="After v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">After v0.1</h1><div class="op-release"><div><h3>First, fix what people run into</h3><ul class="op-list"><li><b>Improve logs and diagnostics</b><small>Work on recurring issues and recovery steps</small></li><li><b>Features needed for actual use</b><small>DB authentication · TLS · compatible updates</small></li></ul></div><div><h3>Then, try more setups</h3><ul class="op-list"><li><b>More Kubernetes/CSI combinations</b><small>Test faults and recovery in each</small></li><li><b>arm64 · multiple availability zones</b><small>Check support separately</small></li></ul></div><div><h3>Work that will take longer</h3><ul class="op-list"><li><b>Changing CUBRID versions</b><small>Data compatibility, downtime and how to roll back</small></li><li><b>More replication setups</b><small>For example, read replicas that cannot become master</small></li></ul></div></div><p class="op-boundary">We will test v0.1 first, then decide what matters most from the problems people find.</p>

</OperatorSlide>

<!--
[20s · 4 · After v0.1]
Once the first version is out, we'll fix what people run into first: logs, recovery steps, database authentication and TLS.

Then we'll add Kubernetes and CSI combinations one at a time, testing faults and recovery in each. We haven't set a next version or date.
-->

---

<OperatorSlide section="Closing · Discussion" index="14" total="15" source="Feedback and help" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Three things we would like to ask</h1><ol class="op-questions op-big"><li>Recently, what did you check before calling it recovered?</li><li>Which Kubernetes CSI driver would you want supported first?</li><li>Could you try our install and recovery docs in December?</li></ol>

</OperatorSlide>

<!--
[25s · Closing · Discussion]
Finally, three things we'd like to ask. In a recent incident, what did you check before calling it recovered? Which Kubernetes CSI driver would you want v0.1 to support first, and what should we watch out for when testing faults on it?

And could you try our installation and recovery docs in December and tell us where you get stuck?
-->

---

<OperatorSlide section="Q&amp;A" index="15" total="15" source="Expected questions" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">Thank you</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab is independently maintained and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project.</p></div>

</OperatorSlide>

<!--
[5s · Q&A]
Thank you. We are happy to take your questions.
-->
