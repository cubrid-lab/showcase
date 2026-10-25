---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="Opening · Project and team" index="01" total="18" source="Project and team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID Kubernetes<br>Operator</h1><p class="op-lead">We are connecting CUBRID operations to Kubernetes,<br>from installation through recovery verification.</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div><p class="op-caption">We aim to publish the first version on December 27.</p></div>

</OperatorSlide>

<!--
[20s · Opening · Project and team]
Hi, we're Yeongseon Choe and Gyeongjun Paik from CUBRID Lab. We're building an Operator to manage CUBRID, a relational DBMS, on Kubernetes. We want it to cover installation and what happens when something fails and has to recover.

For this season, we're aiming for a v0.1 that we've run through in one setup: install it, cause faults, and check that it recovers. Let me start with the problem we're trying to solve.
-->

---

<OperatorSlide class="op-compact" section="Agenda · Talk outline" index="02" total="18" source="Presentation outline" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Four things we want<br>to discuss today</h1>
<div class="op-agenda">
  <div><span>01</span><b>Why this matters</b><p>Pod recovery is not DB recovery</p></div>
  <div><span>02</span><b>What we propose</b><p>Existing approaches, Operator, HA and IM</p></div>
  <div><span>03</span><b>What we have validated</b><p>Evidence, gaps and the test roadmap</p></div>
  <div><span>04</span><b>What we will release</b><p>Co-maintainers, v0.1 boundaries and next steps</p></div>
</div>
<p class="op-boundary">We will finish with three questions for operators and potential collaborators.</p>

</OperatorSlide>

<!--
[15s · Agenda · Talk outline]
I will start with why a restarted Pod does not necessarily mean a recovered database. Then I will compare existing solutions, explain our design, separate what we have verified from what is still unproven, and close with the scope of v0.1 and three questions.
-->

---

<OperatorSlide section="1 · The problem" index="03" total="18" source="Problem and users" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">A recovered Pod is not<br>a recovered database.</h1><div class="op-two"><div class="op-stack"><p class="op-kicker">WHEN A DB MEMBER FAILS</p><ul class="op-list"><li><b>Check the Pod and volume</b><small>The platform team checks Kubernetes</small></li><li><b>Check inside the database too</b><small>The DB operator checks roles, replication and data</small></li></ul></div><div class="op-stack"><p class="op-kicker">BEFORE CALLING IT RECOVERED</p><ul class="op-list"><li><b>Who is master now?</b><small>Which member accepts writes?</small></li><li><b>Are committed rows still there?</b><small>Can we see both existing and new rows?</small></li><li><b>Do the connections work?</b><small>Can we write through RW and read through RO?</small></li></ul></div></div><p class="op-caption">We are starting with the CUBRID operators and Kubernetes teams who do this work.</p>

</OperatorSlide>

<!--
[35s · 1 · The problem]
Suppose a node running the database fails and its Pod comes back. The Pod is Ready and its volume is attached. Does that mean the database is back too?

We still need to check who's master, whether committed rows are there, whether an RW write can be read through RO, and whether RO rejects writes. The platform team looks at Pods and volumes. The database operator looks at roles, replication and data. Recovering the service means checking both sides together. Those are the operators and platform teams we're starting with. We'd also like to hear which checks take the most work in practice.
-->

---

<OperatorSlide section="1 · Failure scenario" index="04" total="18" source="Database recovery definition" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">After a fault, operators need<br>four different answers</h1>
<p class="op-kicker">EXAMPLE: WHAT IF THE MASTER POD DISAPPEARS?</p>
<div class="op-steps">
  <div><span>01</span><b>Is the Pod back?</b><small>Scheduling and PVC attachment</small></div>
  <div><span>02</span><b>Who is the master?</b><small>Consistent role reports across members</small></div>
  <div><span>03</span><b>Can clients read and write?</b><small>Actual SQL through RW and RO</small></div>
  <div><span>04</span><b>Is committed data intact?</b><small>Compare known and newly written rows</small></div>
</div>
<p class="op-boundary"><b>THE POINT</b>　Kubernetes can answer #1. The remaining questions require database-aware checks.</p>
<p class="op-caption">This is an illustrative scenario, not evidence of a real customer incident.</p>

</OperatorSlide>

<!--
[35s · 1 · Failure scenario]
Imagine the master Pod disappears while applications are running. Kubernetes can restart and reattach its volume, but that is only the first checkpoint. A database operator still needs to establish the effective master role, run actual client SQL, and verify committed rows are preserved.

We use this scenario to avoid equating a healthy Pod with proven database recovery. The goal is to make the additional checks observable and repeatable.
-->

---

<OperatorSlide section="1 · Target users" index="05" total="18" source="Initial user hypotheses" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title">Two teams see the same fault<br>through different signals</h1>
<div class="op-personas">
 <div><span>PLATFORM ENGINEER</span><h3>Kubernetes platform team</h3><p>Checks Pods, nodes, volumes and scheduling after a failure.</p><strong>Question: what happens after the Pod returns?</strong></div>
 <div><span>DB OPERATOR</span><h3>CUBRID database team</h3><p>Checks HA roles, replication, client SQL and actual database records.</p><strong>Question: is the database safe to resume?</strong></div>
</div>
<div class="op-bridge"><b>THE LINK WE WANT</b><span>Platform state ↔ database state ↔ operation results</span></div>
<p class="op-caption">These are initial user hypotheses. We want to validate the real priorities with practitioners.</p>

</OperatorSlide>

<!--
[30s · 1 · Target users]
The first audience we have in mind is the platform engineer who knows Kubernetes resources and the CUBRID operator who knows replication and the data. They may be troubleshooting the same incident but looking at different systems.

We want one operational story that links their observations. We have not yet validated the order of pain points through user interviews, so we are explicitly asking for feedback at this first review.
-->

---

<OperatorSlide section="1 · Existing approaches" index="06" total="18" source="Official implementation comparison" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">Existing tools already<br>solve important parts</h1>
<div class="op-alternatives">
  <div><span>01 · KUBERNETES</span><h3>StatefulSet</h3><p>Keeps Pod and persistent-volume resources aligned with declared configuration.</p></div>
  <div><span>02 · CUBRID</span><h3>Built-in HA</h3><p>Owns replication and master-role transitions in the database engine.</p></div>
  <div><span>03 · OPEN SOURCE</span><h3>Official CUBRID Operator</h3><p>Already supports HA status, storage and scheduled backup capabilities.</p></div>
</div>
<p class="op-boundary"><b>OUR QUESTION</b>　How should we handle uncertain database state and interrupted operations?</p>

</OperatorSlide>

<!--
[30s · 1 · Existing approaches]
We should not present the upstream project as if it does nothing. Kubernetes already manages Pod and storage lifecycles. CUBRID already owns HA. The official CUBRID Operator also provides meaningful HA, storage and scheduled backup functionality.

Our proposed focus is the decision boundary when role observations disagree, and the traceability of long-running local database work. Whether that design performs better under faults still has to be demonstrated.
-->

---

<OperatorSlide class="op-compact" section="1 · Comparison" index="07" total="18" source="Official Operator source" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">The difference is how we<br>handle uncertainty</h1><table class="op-comparison"><thead><tr><th>What we compare</th><th>Official Operator</th><th>This project</th></tr></thead><tbody><tr><td>Checking HA status</td><td>Node data from the first successful CMS response</td><td>Compare fresh status from each member<br>No reply or contradictory reports: master unresolved</td></tr><tr><td>Work that takes time</td><td>Run scheduled backups through Pod exec<br>Record backup status</td><td>Request work through IM; save its ID on PVC<br>Record interrupted work as Failed</td></tr><tr><td>Backup settings</td><td>Set the target Pod, script and storage</td><td>Keep the target and request ID<br>Check restore files and checksums</td></tr></tbody></table><p class="op-caption">The official Operator supports HA, storage and scheduled backups too. This table uses the source versions we reviewed.</p><p class="op-boundary">If evidence is missing, we do not guess a master. SQL and data are checked separately.</p>

</OperatorSlide>

<!--
[40s · 1 · Comparison]
CUBRID already has HA, and there is an official Operator. It checks HA status and manages storage and scheduled backups. We focus on what happens when a response is missing or an operation is interrupted.

This table compares the source versions we reviewed. CMS means CUBRID Manager Server. The official implementation uses node information from the first successful CMS response. We get fresh status from each member and compare it. If a response is missing or the reported roles contradict each other, we don't identify a master. For work such as backups, we send an HTTP request to Instance Manager, or IM, and save the operation ID on the PVC. If IM restarts before the work finishes, that operation stays Failed. It doesn't automatically pick up where it left off.

We haven't compared how the two behave in real faults yet. Both use port checks, so we also run SQL and check the data.
-->

---

<OperatorSlide section="2 · Proposed approach" index="08" total="18" source="October 20 test results" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Set it up in YAML;<br>check DB status and results</h1><div class="op-path"><div class="op-node project">Set up in YAML<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">Read DB status<small>Roles · replication · access</small></div><div class="op-arrow">→</div><div class="op-node project">Request and track work<small>ID · progress · result</small></div><div class="op-arrow">→</div><div class="op-node">Update status<small>Conditions·Events</small></div></div><div class="op-principles"><div><b>Do not invent a master</b><small>CUBRID owns HA transitions</small></div><div><b>Keep operation records</b><small>IDs and results survive in PVC</small></div><div><b>Expose uncertainty</b><small>State and SQL are checked separately</small></div></div><p class="op-caption">We want to show database status and work results in Kubernetes.</p>

</OperatorSlide>

<!--
[35s · 2 · Proposed approach]
The user puts the desired configuration in YAML. The Operator reads database status, requests work, and updates progress and results. A long-running backup has an ID so we can look it up again. It also needs to avoid starting another operation blindly if it can't read the existing records.

So far, 27 Kind tests have passed. On VMs, we checked that existing rows were still there, that data written through RW could be read through RO, and that RO rejected writes. Those 27 are test specs; they don't cover every required scenario. We still need VM power-fault and network-partition tests, rejoin, rebuild, real backup restores and CSI testing. The results on this slide were recorded on October 20.
-->

---

<OperatorSlide class="op-compact" section="2 · Architecture" index="09" total="18" source="Architecture" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID handles HA.<br>Operator observes and coordinates.</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>Read status · manage resources</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes resources<small>StatefulSet·Service·PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID HA HANDLES REPLICATION AND MASTER CHANGES</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>Member 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 2 · PVC</small></div></div></div><div class="op-stack"><div class="op-node">Broker<small>RW / RO connections, separate from the DB</small></div><div class="op-node storage">Backup storage<small>S3-compatible · initial copy · backup · restore</small></div></div></div><p class="op-caption">IM takes HTTP requests inside the DB container and records work on PVC.<br>CUBRID decides who becomes master.</p>

</OperatorSlide>

<!--
[40s · 2 · Architecture]
There are four main parts: the Operator, database members with IM, Brokers, and backup storage. The Operator uses the Kubernetes API to manage StatefulSets, Services and PVCs. Each database container runs both CUBRID and IM. IM is a supervisor inside that container, rather than a separate sidecar.

We use IM's authenticated HTTP API to start the database or request local work such as a backup. IM saves operation IDs and status on the PVC. Brokers run separately from the database and accept RW and RO connections. Initial data copies and backup or restore files go through S3-compatible storage.

CUBRID handles replication and decides which member becomes master. Member zero isn't a permanent master. The Operator doesn't promote a member on its own, or pick one of two divergent datasets and overwrite the other.
-->

---

<OperatorSlide class="op-compact" section="2 · Data and control flow" index="10" total="18" source="SQL and DB operations" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">Separate the SQL path<br>from the control path</h1><div class="op-stack"><p class="op-kicker">WHEN THE APPLICATION RUNS SQL</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">WHEN CHANGING SETTINGS OR REQUESTING DB WORK</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">IM API<small>Local work · saved records</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / PVC</div></div></div><p class="op-boundary"><b>WHAT TO CHECK AFTER THE MASTER FAILS</b><br>Engine changes roles → query IM → update Operator status → check SQL and data</p><p class="op-caption">Blocking writes during a network partition still needs work.</p>

</OperatorSlide>

<!--
[35s · 2 · Data and control flow]
Application SQL takes the upper path: an RW or RO Service, then a Broker, then CUBRID. The Operator doesn't relay SQL. The lower path is for reading settings or requesting database work. The Operator calls the IM API and puts the result in its status.

After a master fails, we first look at CUBRID's role transition. We query each member through IM, check that Operator status changes correctly, and run SQL to see whether the data agrees. One important piece still needs work: blocking writes. In Kind, RW write requests returned success responses while the master was unresolved. Reporting an unclear status didn't stop those requests. We need to implement write blocking during a network partition and test it through real connections.
-->

---

<OperatorSlide section="2 · Failure-safety principle" index="11" total="18" source="Write-quarantine evidence" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">When master is unknown,<br>safety matters more than optimism</h1>
<div class="op-safety">
 <div><span>WHAT WE CAN REPORT</span><h3>Keep master unresolved</h3><p>Missing or conflicting member observations must not be converted into an assumed master.</p><p class="op-mini">Status: uncertainty is visible</p></div>
 <div><span>WHAT v0.1 MUST PROVE</span><h3>Enforce RW write quarantine</h3><p>When writes must be blocked, confirm that real client SQL cannot succeed through Broker.</p><p class="op-mini">Status: still required and unproven</p></div>
</div>
<p class="op-boundary"><b>IMPORTANT</b>　Marking a condition “unknown” does not itself stop SQL writes.</p>
<p class="op-caption">A Kind observation returned successful RW writes while master could not be resolved. Isolation remains required work.</p>

</OperatorSlide>

<!--
[35s · 2 · Failure-safety principle]
This is a risk we want to state plainly. Our implementation can leave master unresolved when member observations are missing or contradictory. But an unresolved Kubernetes condition is not an enforcement mechanism for SQL traffic.

In an earlier Kind test, RW writes succeeded during an unresolved-master state. Therefore, write quarantine and partition tests are mandatory release gates, not optional improvements after v0.1.
-->

---

<OperatorSlide section="3 · Recorded evidence" index="12" total="18" source="Recorded executions · Oct 20" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Here is what we have<br>actually verified so far</h1>
<div class="op-evidence-list">
  <div><span class="op-evidence-number">27 / 27</span><div><b>Kind end-to-end test specs passed</b><p>Recorded October 20, 2026. Specs are not the S00–S15 release scenarios.</p></div></div>
  <div><span class="op-evidence-number">LAB00</span><div><b>VM connection and SQL checks</b><p>k3s and CUBRID 11.4.6. Not a VM power-loss test.</p></div></div>
  <div><span class="op-evidence-number">RW / RO</span><div><b>Post-rollout data and SQL checks</b><p>Known PVC identities and rows retained; read/write routing and RO rejection checked.</p></div></div>
</div>
<p class="op-boundary"><b>SCOPE OF EVIDENCE</b>　Passing these paths does not prove the whole recovery lifecycle works.</p>

</OperatorSlide>

<!--
[40s · 3 · Recorded evidence]
We are separating actual observations from targets. First, all 27 Kind E2E specs in the cited run passed on October 20. This is not the same as passing all mandatory scenarios S00 through S15.

Second, a k3s VM environment passed initial connectivity and SQL checks. Third, a controlled rollout preserved known storage identities and data, with RW and RO SQL behavior checked. These are useful results but not a guarantee of recovery after arbitrary faults.
-->

---

<OperatorSlide section="3 · Next validation" index="13" total="18" source="v0.1 validation gates" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">Next, we will test<br>the moments that can go wrong</h1>
<div class="op-gates">
  <div><span>01 · SAFE WRITES</span><b>Unknown master / network partition</b><p>Does client SQL stop when writes must not be accepted?</p></div>
  <div><span>02 · RECOVERY</span><b>Rejoin and rebuild</b><p>Can a failed member return without overwriting correct data?</p></div>
  <div><span>03 · RESTORE</span><b>Backup into a new cluster</b><p>Are manifests, checksums and restored rows correct?</p></div>
  <div><span>04 · REPRODUCE</span><b>CSI and independent runbooks</b><p>Can another maintainer repeat the result on one defined stack?</p></div>
</div>
<p class="op-caption">Record fault outcomes with commits, images, environment, SQL evidence and S00–S15 scenario IDs.</p>

</OperatorSlide>

<!--
[40s · 3 · Next validation]
The next work targets fault conditions. Write quarantine must be enforced during uncertain HA states. Rejoining or rebuilding must not damage valid data. Backup needs to be tested by restoring into a new cluster, not merely by checking that archive files exist.

We also need an explicit Kubernetes and CSI environment and independent runbook reproduction. Those are acceptance gates for the initial release, not evidence we already have.
-->

---

<OperatorSlide section="3 · Twelve-week roadmap" index="14" total="18" source="Schedule" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">One complete pass in November.<br>Repeat the same tests in December.</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Choose the setup</b><p>Set environment and scenarios<br>Check standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA and the test setup</b><p>Three members · RW/RO<br>Run on VMs<br>Try backup and recovery</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Test faults and recovery</b><p>Block writes · rejoin<br>Rebuild · restore backups<br>Aim for first S00–S15 pass</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Repeat on the same RC</b><p>Repeat faults<br>24h load target<br>Someone else tries the docs<br>Fix issues · release files</p></div></div><p class="op-boundary"><b>11.29</b> Aim: first pass of every required scenario　→　<b>12.27</b> v0.1 publication target</p><p class="op-caption">Keep the tested commit, image, setup and SQL results together.</p>

</OperatorSlide>

<!--
[40s · 3 · Twelve-week roadmap]
We've planned twelve weeks, from October 5 to December 27. The first week is for choosing the environment and scenarios and checking SQL on a standalone database. Weeks two through four cover three-member HA, RW/RO, running on VMs, and initial backup and recovery tests. The Kind and VM results we just showed come from that stage.

By the end of November, specifically November 29, we want every required scenario to have passed once. That includes blocking writes, rejoining, rebuilding, and restoring a new cluster from a backup. In December, we want to repeat fault tests on the same release candidate, try a 24-hour load test, and have someone else follow the documentation. We'll fix what those tests find, aiming to publish on December 27. We'll keep the commit, image, environment and SQL results together. The test results will determine whether we're ready to publish.
-->

---

<OperatorSlide section="3 · Collaboration" index="15" total="18" source="Team" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">Two maintainers,<br>independent checks</h1><div class="op-meta"><b>Yeongseon Choe @yeongseon</b><b>Gyeongjun Paik @paikend</b><span>Co-maintainers</span></div><table class="op-comparison"><thead><tr><th>Who</th><th>What they do</th></tr></thead><tbody><tr><td>The issue owner</td><td>Reproduce the problem; write code, tests, docs and experiment records</td></tr><tr><td>The other person</td><td>Review the code and check the results</td></tr><tr><td>Together</td><td>Test installation, HA and recovery; decide whether to release</td></tr></tbody></table><p class="op-caption">Each issue has an owner. We run one fault test at a time on the shared VMs.<br>Before release, someone else tries installation and recovery using only the docs.</p>

</OperatorSlide>

<!--
[25s · 3 · Collaboration]
The two of us develop this together. We assign an owner to each issue. That person takes it from reproducing the problem through code, tests, documentation and experiment records. The other person reviews the change and checks the results.

We use the same approach for HA, backup and recovery, and installation docs. VM fault tests share one environment, so we run them one at a time. Before release, we'll also check that the other maintainer can complete installation and recovery from the docs alone.
-->

---

<OperatorSlide class="op-compact" section="4 · v0.1 scope" index="16" total="18" source="v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">What goes into v0.1</h1><table class="op-comparison op-acceptance"><thead><tr><th>What is included</th><th>How we will check it</th></tr></thead><tbody><tr><td>Non-root · persistent DB<br>Three-member HA · RW/RO</td><td>Run SQL; check roles, commits and data</td></tr><tr><td>Faults · block writes<br>Rejoin · rebuild</td><td>Check state and data after Pod/VM/Broker/Operator faults</td></tr><tr><td>Backup<br>Restore to a new cluster</td><td>Build a new cluster from a backup and compare data</td></tr><tr><td>Retention · IM auth<br>Disruption · status · metrics</td><td>Run S00–S15; follow installation, operations and recovery docs</td></tr></tbody></table><p class="op-boundary"><b>ALSO PUBLISH</b> Images · install manifests · supported setups · operations docs · test results</p><p class="op-caption">CUBRID 11.4.x / amd64 / one Kubernetes/CSI setup · experimental · compatible updates and disk-full conditional</p>

</OperatorSlide>

<!--
[40s · 4 · v0.1 scope]
For v0.1, we'll choose one environment and test everything from installation to recovery. We'll run SQL through three-member HA and RW/RO, then check roles and data after faults. Rejoining or rebuilding must not overwrite good data. When we restore a new cluster from a backup, we'll compare it with a dataset prepared in advance. We also need to check retention, IM authentication, node-disruption policy, status and metrics.

We want to publish the images, install manifests, supported-environment table, operations docs and test results together. The starting setup is CUBRID 11.4.x, amd64, and one Kubernetes/CSI combination. Our current VMs use local-path, so CSI still needs its own tests. This first version is experimental. The IM API has authentication, but the DBA password is currently empty and traffic is unencrypted. Compatible updates and disk-full tests are conditional too.
-->

---

<OperatorSlide section="4 · After v0.1" index="17" total="18" source="After v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">After v0.1</h1><div class="op-release"><div><h3>First, fix what people run into</h3><ul class="op-list"><li><b>Improve logs and diagnostics</b><small>Work on recurring issues and recovery steps</small></li><li><b>Features needed for actual use</b><small>DB authentication · TLS · compatible updates</small></li></ul></div><div><h3>Then, try more setups</h3><ul class="op-list"><li><b>More Kubernetes/CSI combinations</b><small>Test faults and recovery in each</small></li><li><b>arm64 · multiple availability zones</b><small>Check support separately</small></li></ul></div><div><h3>Work that will take longer</h3><ul class="op-list"><li><b>Changing CUBRID versions</b><small>Data compatibility, downtime and how to roll back</small></li><li><b>More replication setups</b><small>For example, read replicas that cannot become master</small></li></ul></div></div><p class="op-boundary">We will test v0.1 first, then decide what matters most from the problems people find.</p><p class="op-caption">The next version and date are not set. We will finish the required v0.1 work first.</p>

</OperatorSlide>

<!--
[20s · 4 · After v0.1]
Once the first version is out, we'd like to fix the rough edges people find. Can they find the cause in the logs and follow the recovery steps? We also need to test features needed for actual use, such as database authentication, TLS and compatible updates.

Then we'd add Kubernetes and CSI combinations one at a time, testing faults and recovery in each. arm64 and setups across availability zones need separate work. Changing CUBRID versions and adding read replicas that cannot become master are longer-term jobs too. We haven't set a next version or date. First we'll finish the required v0.1 work, then use feedback from people who've tried it to decide what comes next.
-->

---

<OperatorSlide section="Closing · Discussion" index="18" total="18" source="Feedback and help" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Questions for you</h1><ol class="op-questions"><li>Think of a recent incident:<br>what did you check before calling it recovered?</li><li>Which Kubernetes/CSI setup could we test together,<br>and what should we watch out for in storage and fault tests?</li><li>Could you try the installation and recovery docs in December<br>and tell us where you get stuck?</li></ol>

</OperatorSlide>

<!--
[25s · Closing · Discussion]
Finally, we'd like to hear about your operating experience. After a recent incident, what did you check first, and what convinced you that the service had recovered? Which Kubernetes and CSI combination should we test, and what should we watch out for with storage or fault tests?

In December, we'd like someone else to try our installation and recovery docs. Knowing where you get stuck, or which explanations are missing, would help us. Thank you.
-->
