---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="Opening · Project and team" index="01" total="18" source="Project and team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">CUBRID on Kubernetes, from installation to verified recovery</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div></div>

</OperatorSlide>

<!--
[20s · Opening · Project and team]
Hi, we're Yeongseon Choe and Gyeongjun Paik from CUBRID Lab. We're building an Operator to manage CUBRID, a relational DBMS, on Kubernetes. We want it to cover installation and what happens when something fails and has to recover.

For this season, we're aiming for a v0.1 that we've run through in one setup: install it, cause faults, and check that it recovers. Let me start with the problem we're trying to solve.
-->

---

<OperatorSlide class="op-compact" section="Agenda · Talk outline" index="02" total="18" source="Presentation outline" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Today's outline</h1>
<div class="op-agenda">
  <div><span>01</span><b>Why this matters</b><p>Pod recovery is not DB recovery</p></div>
  <div><span>02</span><b>What we propose</b><p>Existing approaches, Operator, HA and Instance Manager</p></div>
  <div><span>03</span><b>What we have validated</b><p>Evidence, gaps and the test roadmap</p></div>
  <div><span>04</span><b>What we will release</b><p>Co-maintainers, v0.1 boundaries and next steps</p></div>
</div>


</OperatorSlide>

<!--
[15s · Agenda · Talk outline]
I will start with why a restarted Pod does not necessarily mean a recovered database. Then I will compare existing solutions, explain our design, separate what we have verified from what is still unproven, and close with the scope of v0.1. At the end, we'd like to hear about your own operating experience.
-->

---

<OperatorSlide section="1 · The problem" index="03" total="18" source="Problem and users" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title" style="font-size: 2.4rem">A recovered Pod is not a recovered database</h1><p class="op-kicker">EXAMPLE: THE MASTER POD DISAPPEARS AND COMES BACK</p><div class="op-split"><div><p class="op-split-label">K8s monitoring: Pod status only</p><ol class="op-questions op-big"><li>Is the Pod back?</li></ol></div><div><p class="op-split-label">Needs database knowledge</p><ol class="op-questions op-big" start="2" style="counter-reset: discussion 1"><li>Who is master now?</li><li>Can we write and read?</li><li>Is committed data still there?</li></ol></div></div>

</OperatorSlide>

<!--
[35s · 1 · The problem]
Suppose the master Pod disappears and comes back. The Pod is Ready and its volume is attached. That is as far as Kubernetes monitoring goes.

But who is master now, whether we can write and read, and whether the data from before the failure is still there: those need database knowledge. Knowing what to check before calling it recovered is the core of this project.
-->

---

<OperatorSlide section="1 · Target users" index="04" total="18" source="Initial user hypotheses" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#claim-map">

<h1 class="op-title" style="font-size: 2.4rem">Two teams see the same fault differently</h1><div class="op-scene"><div class="op-actor"><div class="op-bubble">The Pod is back.<br>Are we done?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>Kubernetes platform team</b></div><div class="op-incident"><span>⚡</span><b>Same fault</b></div><div class="op-actor op-actor-db"><div class="op-bubble">Who is master now?<br>Is the data safe?</div><svg class="op-person" viewBox="0 0 64 64" aria-hidden="true"><circle cx="32" cy="20" r="12"/><path d="M8 62c0-14 10.7-24 24-24s24 10 24 24z"/></svg><b>CUBRID database team</b></div></div><p class="op-boundary">Our goal is to let both teams confirm “recovered” from the same view.</p>

</OperatorSlide>

<!--
[30s · 1 · Target users]
The first audience we have in mind is the platform engineer who knows Kubernetes resources and the CUBRID operator who knows replication and the data. They may be troubleshooting the same incident but looking at different systems.

We want one operational story that links their observations. We have not yet validated the order of pain points through user interviews, so we are explicitly asking for feedback at this first review. Our goal is to let both teams confirm recovery from the same view.
-->

---

<OperatorSlide section="1 · Existing approaches" index="05" total="18" source="Official implementation comparison" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">Why build another CUBRID Operator?</h1><div class="op-split"><div><p class="op-split-label">What the official Operator does</p><ul class="op-list"><li><b>HA status</b></li><li><b>Storage</b></li><li><b>Scheduled backups</b></li></ul></div><div><p class="op-split-label">What we add</p><ul class="op-list"><li><b>Do not trust a single member</b><small>Missing or conflicting answers stay “unresolved”</small></li><li><b>Keep a record of interrupted work</b><small>Backup and restore requests tracked by ID</small></li><li><b>Test recovery with SQL and data</b><small>Real writes and reads, beyond Pod status</small></li></ul></div></div><p class="op-boundary">Our goal is to help operators judge recovery correctly, so a failure does not spread.</p>

</OperatorSlide>

<!--
[30s · 1 · Existing approaches]
CUBRID already has an official Operator. It provides HA status, storage and scheduled backups. So why are we building another one?

We add three things. When members do not answer or disagree, we do not guess the master; we leave it unresolved. Long operations such as backups keep a record of the request and the result, even when they are interrupted. And we check recovery with real SQL and data, not Pod status. Whether that difference matters in real failures is something our tests have to show.
-->

---

<OperatorSlide class="op-compact" section="1 · Comparison" index="06" total="18" source="Official Operator source" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">What exactly do we do differently?</h1><table class="op-comparison"><thead><tr><th></th><th>Official Operator (today)</th><th>What we change</th></tr></thead><tbody><tr><td><b>Finding the master</b></td><td>Uses the node list from<br>the first member that answers</td><td>Compares fresh answers from every member<br>Missing or conflicting: marked “unresolved”</td></tr><tr><td><b>Tracking backup work</b></td><td>Runs scheduled backups as a command in the Pod<br>Records backup status</td><td>Sends the request to Instance Manager; keeps its ID on the volume<br>Work cut off by a restart stays “Failed”</td></tr><tr><td><b>Restore</b></td><td>Sets the target Pod, script and storage</td><td>Checks the file list and checksums first<br>Always restores into a new cluster</td></tr><tr><td><b>Recovery check</b></td><td>Port checks</td><td>Same port checks<br>Tests also run real SQL writes, reads and data checks</td></tr></tbody></table><p class="op-caption">Compared from the source versions we reviewed. We have not yet tested which behaves better in real failures.</p>

</OperatorSlide>

<!--
[40s · 1 · Comparison]
Here is the difference from slide 5 in more detail. We built this table by reading both projects' source code.

The official Operator takes the master from the first member that answers. We compare fresh answers from every member and leave the master unresolved when answers are missing or conflict. Operations such as backups go through Instance Manager, and their IDs stay on the volume, so interrupted work is recorded as failed. Before a restore we check the file list and checksums. Both projects use port checks at runtime, so our tests check SQL and data separately. We have not yet compared how the two behave in real failures.
-->

---

<OperatorSlide section="2 · Proposed approach" index="07" total="18" source="Design document" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">Write YAML; the Operator connects the rest</h1><div class="op-path"><div class="op-node project">Set up in YAML<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">Read DB status<small>Roles · replication · access</small></div><div class="op-arrow">→</div><div class="op-node project">Request and track work<small>ID · progress · result</small></div><div class="op-arrow">→</div><div class="op-node">Update status<small>Conditions·Events</small></div></div>

</OperatorSlide>

<!--
[35s · 2 · Proposed approach]
The user puts the desired configuration in YAML. The Operator reads database status, requests work, and updates progress and results. A long-running backup has an ID so we can look it up again. It also needs to avoid starting another operation blindly if it can't read the existing records.
-->

---

<OperatorSlide class="op-compact" section="2 · Architecture" index="08" total="18" source="Architecture" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">CUBRID runs HA; the Operator observes</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>Read status · manage resources</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes resources<small>StatefulSet·Service·volume</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID HA HANDLES REPLICATION AND MASTER CHANGES</p><div class="op-peer-group"><div class="op-node engine">CUBRID + Instance Manager<small>Member 0 · volume</small></div><div class="op-node engine">CUBRID + Instance Manager<small>Member 1 · volume</small></div><div class="op-node engine">CUBRID + Instance Manager<small>Member 2 · volume</small></div></div></div><div class="op-stack"><div class="op-node">Broker<small>RW / RO connections, separate from the DB</small></div><div class="op-node storage">Backup storage<small>Object storage · initial copy · backup · restore</small></div></div></div>

</OperatorSlide>

<!--
[40s · 2 · Architecture]
There are four main parts: the Operator, the database members, Brokers and backup storage. The Operator uses the Kubernetes API to manage StatefulSets, Services and volumes. Each database container runs CUBRID together with Instance Manager, and work such as starting the database or taking a backup is requested from Instance Manager.

Brokers run separately and accept RW and RO connections. Initial data copies and backup files go through object storage. CUBRID handles replication and master changes; the Operator never changes the master itself.
-->

---

<OperatorSlide class="op-compact" section="2 · Data and control flow" index="09" total="18" source="SQL and DB operations" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">Separate the SQL path from the control path</h1><div class="op-stack"><p class="op-kicker">WHEN THE APPLICATION RUNS SQL</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">WHEN CHANGING SETTINGS OR REQUESTING DB WORK</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">Instance Manager<small>DB work · saved records</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / volume</div></div></div><p class="op-boundary"><b>AFTER A MASTER FAILS</b>　CUBRID changes roles → query each member → Operator status → SQL and data</p>

</OperatorSlide>

<!--
[35s · 2 · Data and control flow]
Application SQL takes the upper path: an RW or RO Service, then a Broker, then CUBRID. The Operator doesn't relay SQL. The lower path is for changing settings or requesting database work: the Operator calls Instance Manager and puts the result in its status.

After a master fails, we first look at CUBRID's role change, query each member to check that the Operator's status follows, and finally check SQL and data.
-->

---

<OperatorSlide section="2 · Failure-safety principle" index="10" total="18" source="Write-quarantine evidence" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Unknown master: safety before success</h1>
<div class="op-safety">
 <div><span>WHAT WE CAN REPORT</span><h3>Keep master unresolved</h3><p>Missing or conflicting member observations must not be converted into an assumed master.</p><p class="op-mini">Status: uncertainty is visible</p></div>
 <div><span>WHAT v0.1 MUST PROVE</span><h3>Enforce RW write quarantine</h3><p>When writes must be blocked, confirm that real client SQL cannot succeed through Broker.</p><p class="op-mini">Status: still required and unproven</p></div>
</div>
<p class="op-boundary"><b>IMPORTANT</b>　Marking a condition “unknown” does not itself stop SQL writes.</p>

</OperatorSlide>

<!--
[35s · 2 · Failure-safety principle]
This is a risk we want to state plainly. Our implementation can leave master unresolved when member observations are missing or contradictory. But an unresolved Kubernetes condition is not an enforcement mechanism for SQL traffic.

In an earlier Kind test, RW writes succeeded during an unresolved-master state. Therefore, write quarantine and partition tests are mandatory release gates, not optional improvements after v0.1.
-->

---

<OperatorSlide section="3 · Recorded evidence" index="11" total="18" source="Recorded executions · Oct 20–25" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

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

<OperatorSlide section="3 · Next validation" index="12" total="18" source="v0.1 validation gates" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#evidence-boundaries-retained-in-the-notes">

<h1 class="op-title">Next, we will test the moments that can go wrong</h1>
<div class="op-gates">
  <div><span>01 · SAFE WRITES</span><b>Unknown master / network partition</b><p>Does client SQL stop when writes must not be accepted?</p></div>
  <div><span>02 · RECOVERY</span><b>Rejoin and rebuild</b><p>Can a failed member return without overwriting correct data?</p></div>
  <div><span>03 · RESTORE</span><b>Repeated and interrupted restores</b><p>Does the data still match after many runs, or a restart in the middle of a restore?</p></div>
  <div><span>04 · REPRODUCE</span><b>Storage and independent runbooks</b><p>Can another maintainer repeat the result on one defined stack?</p></div>
</div>
<p class="op-boundary">All four must pass before we publish v0.1.</p>

</OperatorSlide>

<!--
[40s · 3 · Next validation]
The next work targets fault conditions. Write quarantine must be enforced during uncertain HA states. Rejoining or rebuilding must not damage valid data. As I mentioned, restoring a backup into a new cluster has passed for the first time. Next we need to find why the sessions dropped and repeat it under more conditions.

We also need an explicit Kubernetes and CSI environment and independent runbook reproduction. Those are acceptance gates for the initial release, not evidence we already have.
-->

---

<OperatorSlide section="3 · Twelve-week roadmap" index="13" total="18" source="Schedule" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">November: one full pass. December: repeat.</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Choose the setup</b><p>Set environment and scenarios<br>Check standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA and the test setup</b><p>Three members · RW/RO<br>Run on VMs<br>Try backup and recovery</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Test faults and recovery</b><p>Block writes · rejoin<br>Rebuild · restore backups<br>Aim for a first full pass</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Repeat on one candidate</b><p>Repeat faults<br>24h load target<br>Someone else tries the docs<br>Fix issues · release files</p></div></div><p class="op-boundary"><b>11.29</b> Aim: first pass of every required scenario　→　<b>12.27</b> v0.1 publication target</p>

</OperatorSlide>

<!--
[40s · 3 · Twelve-week roadmap]
We've planned twelve weeks, from October 5 to December 27. The first week is for choosing the environment and scenarios and checking SQL on a standalone database. Weeks two through four cover three-member HA, RW/RO, running on VMs, and initial backup and recovery tests. The Kind and VM results we just showed come from that stage.

By the end of November, specifically November 29, we want every required scenario to have passed once. That includes blocking writes, rejoining, rebuilding, and restoring a new cluster from a backup. In December, we want to repeat fault tests on the same release candidate, try a 24-hour load test, and have someone else follow the documentation. We'll fix what those tests find, aiming to publish on December 27. The test results will determine whether we're ready to publish.
-->

---

<OperatorSlide section="3 · Collaboration" index="14" total="18" source="Team" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">Two maintainers, independent checks</h1><div class="op-meta"><b>Yeongseon Choe @yeongseon</b><b>Gyeongjun Paik @paikend</b><span>Co-maintainers</span></div><table class="op-comparison"><thead><tr><th>Who</th><th>What they do</th></tr></thead><tbody><tr><td>The issue owner</td><td>Reproduce the problem; write code, tests, docs and experiment records</td></tr><tr><td>The other person</td><td>Review the code and check the results</td></tr><tr><td>Together</td><td>Test installation, HA and recovery; decide whether to release</td></tr></tbody></table><p class="op-boundary">The author is never the final reviewer; we decide on a release together.</p>

</OperatorSlide>

<!--
[25s · 3 · Collaboration]
The two of us develop this together. We assign an owner to each issue. That person takes it from reproducing the problem through code, tests, documentation and experiment records. The other person reviews the change and checks the results.

We use the same approach for HA, backup and recovery, and installation docs. VM fault tests share one environment, so we run them one at a time. Before release, we'll also check that the other maintainer can complete installation and recovery from the docs alone.
-->

---

<OperatorSlide class="op-compact" section="4 · v0.1 scope" index="15" total="18" source="v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">What goes into v0.1</h1><table class="op-comparison op-acceptance"><thead><tr><th>What is included</th><th>How we will check it</th></tr></thead><tbody><tr><td>Non-root · persistent DB<br>Three-member HA · RW/RO</td><td>Run SQL; check roles, commits and data</td></tr><tr><td>Faults · block writes<br>Rejoin · rebuild</td><td>Check state and data after Pod/VM/Broker/Operator faults</td></tr><tr><td>Backup<br>Restore to a new cluster</td><td>Build a new cluster from a backup and compare data</td></tr><tr><td>Retention · Instance Manager auth<br>Node maintenance · status · metrics</td><td>Run the required scenarios; follow installation, operations and recovery docs</td></tr></tbody></table><p class="op-boundary"><b>ALSO PUBLISH</b> Images · install manifests · supported setups · operations docs · test results</p><p class="op-caption">Supported: CUBRID 11.4.x · amd64 · one Kubernetes and storage setup · experimental</p>

</OperatorSlide>

<!--
[40s · 4 · v0.1 scope]
For v0.1, we'll choose one environment and test everything from installation to recovery. We'll run SQL through three-member HA and RW/RO, then check roles and data after faults. Rejoining or rebuilding must not overwrite good data. When we restore a new cluster from a backup, we'll compare it with a dataset prepared in advance. We also need to check retention, Instance Manager authentication, node-disruption policy, status and metrics.

We want to publish the images, install manifests, supported-environment table, operations docs and test results together. The starting setup is CUBRID 11.4.x, amd64, and one Kubernetes/CSI combination. Our current VMs use local-path, so CSI still needs its own tests. This first version is experimental. Instance Manager has authentication, but the DBA password is currently empty and traffic is unencrypted. Compatible updates and disk-full tests are conditional too.
-->

---

<OperatorSlide section="4 · After v0.1" index="16" total="18" source="After v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">After v0.1</h1><div class="op-release"><div><h3>First, fix what people run into</h3><ul class="op-list"><li><b>Improve logs and diagnostics</b><small>Work on recurring issues and recovery steps</small></li><li><b>Features needed for actual use</b><small>DB authentication · TLS · compatible updates</small></li></ul></div><div><h3>Then, try more setups</h3><ul class="op-list"><li><b>More Kubernetes/CSI combinations</b><small>Test faults and recovery in each</small></li><li><b>arm64 · multiple availability zones</b><small>Check support separately</small></li></ul></div><div><h3>Work that will take longer</h3><ul class="op-list"><li><b>Changing CUBRID versions</b><small>Data compatibility, downtime and how to roll back</small></li><li><b>More replication setups</b><small>For example, read replicas that cannot become master</small></li></ul></div></div><p class="op-boundary">We will test v0.1 first, then decide what matters most from the problems people find.</p>

</OperatorSlide>

<!--
[20s · 4 · After v0.1]
Once the first version is out, we'll fix what people run into first: logs, recovery steps, database authentication and TLS.

Then we'll add Kubernetes and CSI combinations one at a time, testing faults and recovery in each. We haven't set a next version or date.
-->

---

<OperatorSlide section="Closing · Discussion" index="17" total="18" source="Feedback and help" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Three things we would like to ask</h1><ol class="op-questions op-big"><li>Recently, what did you check before calling it recovered?</li><li>Which Kubernetes CSI driver would you want supported first?</li><li>Could you try our install and recovery docs in December?</li></ol>

</OperatorSlide>

<!--
[25s · Closing · Discussion]
Finally, three things we'd like to ask. In a recent incident, what did you check before calling it recovered? Which Kubernetes CSI driver would you want v0.1 to support first, and what should we watch out for when testing faults on it?

And could you try our installation and recovery docs in December and tell us where you get stuck?
-->

---

<OperatorSlide section="Q&amp;A" index="18" total="18" source="Expected questions" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/EXPECTED_QA.ko.md">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">Thank you</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik</span></div></div>

</OperatorSlide>

<!--
[5s · Q&A]
Thank you. We are happy to take your questions.
-->
