---
title: "CUBRID Kubernetes Operator — First Validation"
---

<OperatorSlide section="1 · Project and team" index="01" total="11" source="Project and team" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<div class="op-cover"><p class="op-kicker">BUILDER SEASON 4 · FIRST VALIDATION · 2026.10.31</p><h1 class="op-title">CUBRID Kubernetes<br>Operator</h1><p class="op-lead">From installing CUBRID to recovering it,<br>we want to manage it on Kubernetes.</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div><p class="op-caption">We aim to publish the first version on December 27.</p></div>

</OperatorSlide>

<!--
[40s · 1 · Project and team]
Hi, we're Yeongseon Choe and Gyeongjun Paik from CUBRID Lab. We're building an Operator to manage CUBRID, a relational DBMS, on Kubernetes. We want it to cover installation and what happens when something fails and has to recover.

For this season, we're aiming for a v0.1 that we've run through in one setup: install it, cause faults, and check that it recovers. Let me start with the problem we're trying to solve.
-->

---

<OperatorSlide section="2 · Problem and users" index="02" total="11" source="Problem and users" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#43-database-aware">

<h1 class="op-title">The Pod is back.<br>There is still more to check.</h1><div class="op-two"><div class="op-stack"><p class="op-kicker">WHEN A DB MEMBER FAILS</p><ul class="op-list"><li><b>Check the Pod and volume</b><small>The platform team checks Kubernetes</small></li><li><b>Check inside the database too</b><small>The DB operator checks roles, replication and data</small></li></ul></div><div class="op-stack"><p class="op-kicker">BEFORE CALLING IT RECOVERED</p><ul class="op-list"><li><b>Who is master now?</b><small>Which member accepts writes?</small></li><li><b>Are committed rows still there?</b><small>Can we see both existing and new rows?</small></li><li><b>Do the connections work?</b><small>Can we write through RW and read through RO?</small></li></ul></div></div><p class="op-caption">We are starting with the CUBRID operators and Kubernetes teams who do this work.</p>

</OperatorSlide>

<!--
[65s · 2 · Problem and users]
Suppose a node running the database fails and its Pod comes back. The Pod is Ready and its volume is attached. Does that mean the database is back too?

We still need to check who's master, whether committed rows are there, whether an RW write can be read through RO, and whether RO rejects writes. The platform team looks at Pods and volumes. The database operator looks at roles, replication and data. Recovering the service means checking both sides together. Those are the operators and platform teams we're starting with. We'd also like to hear which checks take the most work in practice.
-->

---

<OperatorSlide class="op-compact" section="3 · How this differs" index="03" total="11" source="Official Operator source" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#comparison-boundaries">

<h1 class="op-title">How our Operator differs</h1><table class="op-comparison"><thead><tr><th>What we compare</th><th>Official Operator</th><th>This project</th></tr></thead><tbody><tr><td>Checking HA status</td><td>Node data from the first successful CMS response</td><td>Compare fresh status from each member<br>No reply or contradictory reports: master unresolved</td></tr><tr><td>Work that takes time</td><td>Run scheduled backups through Pod exec<br>Record backup status</td><td>Request work through IM; save its ID on PVC<br>Record interrupted work as Failed</td></tr><tr><td>Backup settings</td><td>Set the target Pod, script and storage</td><td>Keep the target and request ID<br>Check restore files and checksums</td></tr></tbody></table><p class="op-caption">The official Operator supports HA, storage and scheduled backups too. This table uses the source versions we reviewed.</p><p class="op-boundary">We also run SQL and check the data separately.</p>

</OperatorSlide>

<!--
[65s · 3 · How this differs]
CUBRID already has HA, and there is an official Operator. It checks HA status and manages storage and scheduled backups. We focus on what happens when a response is missing or an operation is interrupted.

This table compares the source versions we reviewed. CMS means CUBRID Manager Server. The official implementation uses node information from the first successful CMS response. We get fresh status from each member and compare it. If a response is missing or the reported roles contradict each other, we don't identify a master. For work such as backups, we send an HTTP request to Instance Manager, or IM, and save the operation ID on the PVC. If IM restarts before the work finishes, that operation stays Failed. It doesn't automatically pick up where it left off.

We haven't compared how the two behave in real faults yet. Both use port checks, so we also run SQL and check the data.
-->

---

<OperatorSlide section="4 · What the Operator does" index="04" total="11" source="October 20 test results" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#recorded-execution-evidence">

<h1 class="op-title">Set it up in YAML;<br>check DB status and results</h1><div class="op-path"><div class="op-node project">Set up in YAML<small>CubridCluster</small></div><div class="op-arrow">→</div><div class="op-node">Read DB status<small>Roles · replication · access</small></div><div class="op-arrow">→</div><div class="op-node project">Request and track work<small>ID · progress · result</small></div><div class="op-arrow">→</div><div class="op-node">Update status<small>Conditions·Events</small></div></div><div class="op-evidence"><div><p class="op-kicker">WHAT WE HAVE TESTED</p><p>27 Kind test specs passed<br>VMs: existing rows retained; RW/RO SQL checked</p></div><div><p class="op-kicker">WHAT STILL NEEDS WORK</p><p>Block writes during VM faults and partitions<br>Test rejoin, rebuild, backup restore and CSI</p></div></div><p class="op-caption">We want to show database status and work results in Kubernetes.</p>

</OperatorSlide>

<!--
[60s · 4 · What the Operator does]
The user puts the desired configuration in YAML. The Operator reads database status, requests work, and updates progress and results. A long-running backup has an ID so we can look it up again. It also needs to avoid starting another operation blindly if it can't read the existing records.

So far, 27 Kind tests have passed. On VMs, we checked that existing rows were still there, that data written through RW could be read through RO, and that RO rejected writes. Those 27 are test specs; they don't cover every required scenario. We still need VM power-fault and network-partition tests, rejoin, rebuild, real backup restores and CSI testing. The results on this slide were recorded on October 20.
-->

---

<OperatorSlide class="op-compact" section="5 · Architecture" index="05" total="11" source="Architecture" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#7-high-level-architecture">

<h1 class="op-title">What CUBRID, Operator and IM do</h1><div class="op-path"><div class="op-node">Kubernetes API<small>CubridCluster / CubridBackup</small></div><div class="op-arrow">→</div><div class="op-node project">Operator<small>Read status · manage resources</small></div><div class="op-arrow">→</div><div class="op-node">Kubernetes resources<small>StatefulSet·Service·PVC</small></div></div><div class="op-architecture"><div class="op-stack"><p class="op-kicker">CUBRID HA HANDLES REPLICATION AND MASTER CHANGES</p><div class="op-peer-group"><div class="op-node engine">CUBRID + IM<small>Member 0 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 1 · PVC</small></div><div class="op-node engine">CUBRID + IM<small>Member 2 · PVC</small></div></div></div><div class="op-stack"><div class="op-node">Broker<small>RW / RO connections, separate from the DB</small></div><div class="op-node storage">Backup storage<small>S3-compatible · initial copy · backup · restore</small></div></div></div><p class="op-caption">IM takes HTTP requests inside the DB container and records work on PVC.<br>CUBRID decides who becomes master.</p>

</OperatorSlide>

<!--
[70s · 5 · Architecture]
There are four main parts: the Operator, database members with IM, Brokers, and backup storage. The Operator uses the Kubernetes API to manage StatefulSets, Services and PVCs. Each database container runs both CUBRID and IM. IM is a supervisor inside that container, rather than a separate sidecar.

We use IM's authenticated HTTP API to start the database or request local work such as a backup. IM saves operation IDs and status on the PVC. Brokers run separately from the database and accept RW and RO connections. Initial data copies and backup or restore files go through S3-compatible storage.

CUBRID handles replication and decides which member becomes master. Member zero isn't a permanent master. The Operator doesn't promote a member on its own, or pick one of two divergent datasets and overwrite the other.
-->

---

<OperatorSlide class="op-compact" section="5 · SQL and DB operations" index="06" total="11" source="SQL and DB operations" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/DESIGN.md#10-broker-and-service-architecture">

<h1 class="op-title">SQL goes to Broker; DB work goes to IM</h1><div class="op-stack"><p class="op-kicker">WHEN THE APPLICATION RUNS SQL</p><div class="op-path"><div class="op-node">Application</div><div class="op-arrow">→</div><div class="op-node">RW / RO Service</div><div class="op-arrow">→</div><div class="op-node">Broker</div><div class="op-arrow">→</div><div class="op-node engine">CUBRID</div></div><p class="op-kicker">WHEN CHANGING SETTINGS OR REQUESTING DB WORK</p><div class="op-path"><div class="op-node">Kubernetes API</div><div class="op-arrow">→</div><div class="op-node project">Operator</div><div class="op-arrow">→</div><div class="op-node project">IM API<small>Local work · saved records</small></div><div class="op-arrow">→</div><div class="op-node engine">CUBRID / PVC</div></div></div><p class="op-boundary"><b>WHAT TO CHECK AFTER THE MASTER FAILS</b><br>Engine changes roles → query IM → update Operator status → check SQL and data</p><p class="op-caption">Blocking writes during a network partition still needs work.</p>

</OperatorSlide>

<!--
[60s · 5 · SQL and DB operations]
Application SQL takes the upper path: an RW or RO Service, then a Broker, then CUBRID. The Operator doesn't relay SQL. The lower path is for reading settings or requesting database work. The Operator calls the IM API and puts the result in its status.

After a master fails, we first look at CUBRID's role transition. We query each member through IM, check that Operator status changes correctly, and run SQL to see whether the data agrees. One important piece still needs work: blocking writes. In Kind, RW write requests returned success responses while the master was unresolved. Reporting an unclear status didn't stop those requests. We need to implement write blocking during a network partition and test it through real connections.
-->

---

<OperatorSlide section="6 · 12-week plan" index="07" total="11" source="Schedule" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#stp-iv-delivery-stages">

<h1 class="op-title">November: first full pass<br>December: repeat the tests</h1><div class="op-timeline"><div><small>Week 1 · Oct 05–11</small><b>Choose the setup</b><p>Set environment and scenarios<br>Check standalone SQL</p></div><div><small>Weeks 2–4 · Oct 12–Nov 01</small><b>HA and the test setup</b><p>Three members · RW/RO<br>Run on VMs<br>Try backup and recovery</p></div><div><small>Weeks 5–8 · Nov 02–29</small><b>Test faults and recovery</b><p>Block writes · rejoin<br>Rebuild · restore backups<br>Aim for first S00–S15 pass</p></div><div><small>Weeks 9–12 · Nov 30–Dec 27</small><b>Repeat on the same RC</b><p>Repeat faults<br>24h load target<br>Someone else tries the docs<br>Fix issues · release files</p></div></div><p class="op-boundary"><b>11.29</b> Aim: first pass of every required scenario　→　<b>12.27</b> v0.1 publication target</p><p class="op-caption">Keep the tested commit, image, setup and SQL results together.</p>

</OperatorSlide>

<!--
[70s · 6 · 12-week plan]
We've planned twelve weeks, from October 5 to December 27. The first week is for choosing the environment and scenarios and checking SQL on a standalone database. Weeks two through four cover three-member HA, RW/RO, running on VMs, and initial backup and recovery tests. The Kind and VM results we just showed come from that stage.

By the end of November, specifically November 29, we want every required scenario to have passed once. That includes blocking writes, rejoining, rebuilding, and restoring a new cluster from a backup. In December, we want to repeat fault tests on the same release candidate, try a 24-hour load test, and have someone else follow the documentation. We'll fix what those tests find, aiming to publish on December 27. We'll keep the commit, image, environment and SQL results together. The test results will determine whether we're ready to publish.
-->

---

<OperatorSlide section="6 · How we work together" index="08" total="11" source="Team" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/CONTRIBUTING.md#development-workflow">

<h1 class="op-title">We build and review together</h1><div class="op-meta"><b>Yeongseon Choe @yeongseon</b><b>Gyeongjun Paik @paikend</b><span>Co-maintainers</span></div><table class="op-comparison"><thead><tr><th>Who</th><th>What they do</th></tr></thead><tbody><tr><td>The issue owner</td><td>Reproduce the problem; write code, tests, docs and experiment records</td></tr><tr><td>The other person</td><td>Review the code and check the results</td></tr><tr><td>Together</td><td>Test installation, HA and recovery; decide whether to release</td></tr></tbody></table><p class="op-caption">Each issue has an owner. We run one fault test at a time on the shared VMs.<br>Before release, someone else tries installation and recovery using only the docs.</p>

</OperatorSlide>

<!--
[45s · 6 · How we work together]
The two of us develop this together. We assign an owner to each issue. That person takes it from reproducing the problem through code, tests, documentation and experiment records. The other person reviews the change and checks the results.

We use the same approach for HA, backup and recovery, and installation docs. VM fault tests share one environment, so we run them one at a time. Before release, we'll also check that the other maintainer can complete installation and recovery from the docs alone.
-->

---

<OperatorSlide class="op-compact" section="6 · What goes into v0.1" index="09" total="11" source="v0.1 scope" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/39b1cb6ca7b6a52cf933b778c546cd9d6c6979bb/ROADMAP.md#v01-scope">

<h1 class="op-title">What goes into v0.1</h1><table class="op-comparison op-acceptance"><thead><tr><th>What is included</th><th>How we will check it</th></tr></thead><tbody><tr><td>Non-root · persistent DB<br>Three-member HA · RW/RO</td><td>Run SQL; check roles, commits and data</td></tr><tr><td>Faults · block writes<br>Rejoin · rebuild</td><td>Check state and data after Pod/VM/Broker/Operator faults</td></tr><tr><td>Backup<br>Restore to a new cluster</td><td>Build a new cluster from a backup and compare data</td></tr><tr><td>Retention · IM auth<br>Disruption · status · metrics</td><td>Run S00–S15; follow installation, operations and recovery docs</td></tr></tbody></table><p class="op-boundary"><b>ALSO PUBLISH</b> Images · install manifests · supported setups · operations docs · test results</p><p class="op-caption">CUBRID 11.4.x / amd64 / one Kubernetes/CSI setup · experimental · compatible updates and disk-full conditional</p>

</OperatorSlide>

<!--
[55s · 6 · What goes into v0.1]
For v0.1, we'll choose one environment and test everything from installation to recovery. We'll run SQL through three-member HA and RW/RO, then check roles and data after faults. Rejoining or rebuilding must not overwrite good data. When we restore a new cluster from a backup, we'll compare it with a dataset prepared in advance. We also need to check retention, IM authentication, node-disruption policy, status and metrics.

We want to publish the images, install manifests, supported-environment table, operations docs and test results together. The starting setup is CUBRID 11.4.x, amd64, and one Kubernetes/CSI combination. Our current VMs use local-path, so CSI still needs its own tests. This first version is experimental. The IM API has authentication, but the DBA password is currently empty and traffic is unencrypted. Compatible updates and disk-full tests are conditional too.
-->

---

<OperatorSlide section="6 · After v0.1" index="10" total="11" source="After v0.1" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md#post-v01-direction">

<h1 class="op-title">After v0.1</h1><div class="op-release"><div><h3>First, fix what people run into</h3><ul class="op-list"><li><b>Improve logs and diagnostics</b><small>Work on recurring issues and recovery steps</small></li><li><b>Features needed for actual use</b><small>DB authentication · TLS · compatible updates</small></li></ul></div><div><h3>Then, try more setups</h3><ul class="op-list"><li><b>More Kubernetes/CSI combinations</b><small>Test faults and recovery in each</small></li><li><b>arm64 · multiple availability zones</b><small>Check support separately</small></li></ul></div><div><h3>Work that will take longer</h3><ul class="op-list"><li><b>Changing CUBRID versions</b><small>Data compatibility, downtime and how to roll back</small></li><li><b>More replication setups</b><small>For example, read replicas that cannot become master</small></li></ul></div></div><p class="op-boundary">We will test v0.1 first, then decide what matters most from the problems people find.</p><p class="op-caption">The next version and date are not set. We will finish the required v0.1 work first.</p>

</OperatorSlide>

<!--
[40s · 6 · After v0.1]
Once the first version is out, we'd like to fix the rough edges people find. Can they find the cause in the logs and follow the recovery steps? We also need to test features needed for actual use, such as database authentication, TLS and compatible updates.

Then we'd add Kubernetes and CSI combinations one at a time, testing faults and recovery in each. arm64 and setups across availability zones need separate work. Changing CUBRID versions and adding read replicas that cannot become master are longer-term jobs too. We haven't set a next version or date. First we'll finish the required v0.1 work, then use feedback from people who've tried it to decide what comes next.
-->

---

<OperatorSlide section="7 · Questions for you" index="11" total="11" source="Feedback and help" source-url="https://github.com/cubrid-lab/showcase/blob/main/events/2026-builder-season4/01-validation/SOURCES.md">

<h1 class="op-title">Questions for you</h1><ol class="op-questions"><li>Think of a recent incident:<br>what did you check before calling it recovered?</li><li>Which Kubernetes/CSI setup could we test together,<br>and what should we watch out for in storage and fault tests?</li><li>Could you try the installation and recovery docs in December<br>and tell us where you get stuck?</li></ol>

</OperatorSlide>

<!--
[30s · 7 · Questions for you]
Finally, we'd like to hear about your operating experience. After a recent incident, what did you check first, and what convinced you that the service had recovered? Which Kubernetes and CSI combination should we test, and what should we watch out for with storage or fault tests?

In December, we'd like someone else to try our installation and recovery docs. Knowing where you get stuck, or which explanations are missing, would help us. Thank you.
-->
