---
title: "CUBRID Kubernetes Operator — Second Validation"
---

<OperatorSlide class="op-session" section="Opening · Project introduction" source="Project and team" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover"><BrandMark name="cubrid-kubernetes-operator" alt="CUBRID Lab Operator icon" :height="84" /><p class="op-kicker">Builder Season 4 · Second validation</p><h1 class="op-title">CUBRID K8s Operator</h1><p class="op-lead">A database server fails and another takes over.<br>When can the app safely write again?</p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik · Co-maintainers</span></div></div>

</OperatorSlide>

<!--
Hello, we’re CUBRID Lab. An application gets a successful write response. Then its database server fails. Will the data be on the new server, and when can the app safely write again? I’ll show how we handle those questions in our failure tests.
-->

---

<OperatorSlide class="op-compact op-session" section="Agenda">

<h1 class="op-title">Agenda</h1>

<div class="op-agenda">
  <div><span>01</span><b>Project introduction</b></div>
  <div><span>02</span><b>First-round feedback</b></div>
  <div><span>03</span><b>Development and design</b></div>
  <div><span>04</span><b>Test results</b></div>
  <div><span>05</span><b>Discussion</b></div>
  <div><span>06</span><b>Final presentation plan</b></div>
</div>

</OperatorSlide>

<!--
I’ll introduce the project and explain what changed after the first review. Then I’ll cover the v0.1 design, the failure scenarios we tested, the open issues and our plan before release.
-->

---

<OperatorSlide class="op-compact op-session" section="01 · Project introduction">

<h1 class="op-title">How the Operator and Instance Manager fit together</h1>

<svg class="op-arch" style="max-height:340px" viewBox="0 0 900 392" role="img" aria-label="The Operator manages the cluster. An Instance Manager in each database Pod reports status and runs database tasks. Applications connect through Services and Brokers. CUBRID elects the primary and replicates. Backups use S3-compatible storage.">
<defs><marker id="op-arch-ink" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#0f1b2d"/></marker><marker id="op-arch-blue" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#1f4e8c"/></marker><marker id="op-arch-mute" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#5b6b82"/></marker></defs>
<rect class="box" x="150" y="0" width="750" height="328" rx="10" style="fill:none;stroke-dasharray:3 4"/><text class="s" x="162" y="16">Kubernetes cluster</text>
<rect class="box" x="0" y="14" width="130" height="50" rx="8"/><text x="65" y="35" text-anchor="middle">DB operator</text><text class="s" x="65" y="53" text-anchor="middle">Submit settings and requests</text>
<path class="ctl" d="M130 39H166" marker-end="url(#op-arch-blue)"/><text class="s b" x="148" y="32" text-anchor="middle">①</text>
<rect class="box" x="170" y="24" width="120" height="62" rx="8"/><text x="230" y="46" text-anchor="middle">Kubernetes API</text><text class="s" x="230" y="63" text-anchor="middle">Cluster settings</text><text class="s" x="230" y="78" text-anchor="middle">Backup requests</text>
<path class="ctl" d="M290 44H336" marker-end="url(#op-arch-blue)"/><text class="s b" x="313" y="37" text-anchor="middle">② Settings</text>
<path class="ctl" d="M338 70H292" marker-end="url(#op-arch-blue)"/><text class="s b" x="315" y="84" text-anchor="middle">④ Status</text>
<rect class="box op" x="340" y="20" width="290" height="96" rx="8"/><text class="b" x="485" y="43" text-anchor="middle">CUBRID Kubernetes Operator</text><text class="s" x="485" y="64" text-anchor="middle">Monitor the cluster</text><text class="s" x="485" y="81" text-anchor="middle">Coordinate write access and recovery</text><text class="s" x="485" y="101" text-anchor="middle">Report progress to operators</text>
<path class="mgmt" d="M630 50H656" marker-end="url(#op-arch-mute)"/>
<rect class="box" x="660" y="24" width="228" height="62" rx="8"/><text x="774" y="46" text-anchor="middle">Monitor operations</text><text class="s" x="774" y="63" text-anchor="middle">Cluster and server metrics</text><text class="s" x="774" y="78" text-anchor="middle">Events and structured logs</text>
<path class="mgmt" d="M400 116V136" marker-end="url(#op-arch-mute)"/><text class="s" x="392" y="131" text-anchor="end">Manage resources</text>
<path class="ctl" d="M600 116V150" marker-end="url(#op-arch-blue)"/><text class="s b" x="610" y="135">③ Check status and request tasks</text>
<rect class="box" x="170" y="138" width="262" height="84" rx="8"/><text x="301" y="159" text-anchor="middle">Kubernetes resources</text><text class="s" x="301" y="177" text-anchor="middle">Database servers and volumes</text><text class="s" x="301" y="194" text-anchor="middle">Service endpoints and network policies</text><text class="s" x="301" y="211" text-anchor="middle">Read and write Brokers</text>
<rect class="box ha" x="450" y="152" width="440" height="152" rx="10"/><text x="464" y="174">Three CUBRID HA members · Primary election and replication</text>
<rect class="box ink" x="462" y="184" width="126" height="108" rx="7"/><text class="b" x="525" y="205" text-anchor="middle">Server 0 · Primary</text><rect class="box im" x="467" y="215" width="116" height="28" rx="5"/><text class="b" x="525" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="525" y="270" text-anchor="middle">CUBRID · Data volume</text>
<rect class="box ink" x="604" y="184" width="126" height="108" rx="7"/><text x="667" y="205" text-anchor="middle">Server 1 · Replica</text><rect class="box im" x="609" y="215" width="116" height="28" rx="5"/><text class="b" x="667" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="667" y="270" text-anchor="middle">CUBRID · Data volume</text>
<rect class="box ink" x="746" y="184" width="126" height="108" rx="7"/><text x="809" y="205" text-anchor="middle">Server 2 · Replica</text><rect class="box im" x="751" y="215" width="116" height="28" rx="5"/><text class="b" x="809" y="234" text-anchor="middle" style="font-size:11px">Instance Manager</text><text class="s" x="809" y="270" text-anchor="middle">CUBRID · Data volume</text>
<path class="sql" d="M525 292V299H809V294" marker-end="url(#op-arch-ink)"/><path class="sql" d="M667 299V294" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="0" y="240" width="130" height="46" rx="8"/><text x="65" y="268" text-anchor="middle">Application</text>
<path class="sql" d="M130 263H166" marker-end="url(#op-arch-ink)"/>
<rect class="box" x="170" y="243" width="128" height="40" rx="8"/><text x="234" y="268" text-anchor="middle">RW / RO Service</text>
<path class="sql" d="M298 263H310" marker-end="url(#op-arch-ink)"/>
<rect class="box ink" x="312" y="235" width="126" height="56" rx="8"/><text x="375" y="257" text-anchor="middle">Broker (RW · RO)</text><text class="s" x="375" y="277" text-anchor="middle">Route application queries</text>
<path class="sql" d="M438 263H458" marker-end="url(#op-arch-ink)"/>
<path class="mgmt" d="M670 304V340" marker-start="url(#op-arch-mute)" marker-end="url(#op-arch-mute)"/><text class="s" x="680" y="326">Upload and restore</text>
<rect class="box store" x="450" y="342" width="440" height="40" rx="8"/><text x="670" y="360" text-anchor="middle">S3-compatible object storage</text><text class="s" x="670" y="376" text-anchor="middle">Backup files and verification data</text>
<path class="sql" d="M0 346H40"/><text class="s" x="48" y="350">Application SQL and replication</text>
<path class="ctl" d="M0 364H40"/><text class="s" x="48" y="368">Operator control and configuration</text>
<path class="mgmt" d="M0 382H40"/><text class="s" x="48" y="386">Resource, backup and monitoring paths</text>
<rect class="box op" x="0" y="93" width="139" height="108" rx="8"/>
<text class="b" x="11" y="117">What we build</text>
<text class="s" x="11" y="142">Operator</text>
<text class="s" x="11" y="161">Instance Manager</text>
<text class="s" x="11" y="184">Shown in blue</text>
</svg>

</OperatorSlide>

<!--
The blue boxes show what we build. The Operator coordinates the cluster and the write path. Each CUBRID server has an Instance Manager that reports its role and runs local operations. Applications use Services and Brokers to reach CUBRID. CUBRID elects the primary and replicates the data.
-->

---

<OperatorSlide class="op-compact op-session" section="02 · First-round feedback addressed">

<h1 class="op-title">First-round feedback addressed</h1>

<table class="op-comparison">
<thead><tr><th scope="col">Feedback</th><th scope="col">What changed</th><th scope="col">Before release</th></tr></thead>
<tbody>
<tr><td>Status alone cannot stop writes</td><td>Close the write path and check for successful writes</td><td>Retest both new and existing connections</td></tr>
<tr><td>Report how long writes are blocked</td><td>Compare write downtime under the same fault</td><td>Record downtime and missing data in partition and power-off tests</td></tr>
<tr><td>Require evidence that restore worked</td><td>Two first-round runs were inconclusive. Three later restores passed.</td><td>Repeat restores on the release candidate and compare data</td></tr>
</tbody>
</table>
<p class="op-caption">First-round feedback summary · October 31, 2026</p>

</OperatorSlide>

<!--
The strongest feedback from round one was to show that writes actually stop. We shut the write path and check whether clients still receive successful responses. We also measure downtime. Two of the first-round restore runs were inconclusive after losing SQL sessions. Three later restores into a new cluster passed. We will repeat those checks on the release candidate.

Sources:
https://github.com/cubrid-lab/showcase/tree/main/events/2026-builder-season4/01-validation
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-compact op-session" section="02 · First-round feedback deferred">

<h1 class="op-title">First-round feedback deferred</h1>

<table class="op-comparison">
<thead><tr><th scope="col">Feedback</th><th scope="col">v0.1 decision</th><th scope="col">Why we deferred it</th></tr></thead>
<tbody>
<tr><td>Rejoin with existing data</td><td>Automatic rejoin moves to v0.2.<br>v0.1 rebuilds from backup after approval.</td><td>Verify that stale data cannot overwrite newer data</td></tr>
<tr><td>Migration costs and collaboration with the official project</td><td>Review migration costs and collaboration separately</td><td>Our comparison covered recovery after forced deletion</td></tr>
<tr><td>External storage (CSI), online scaling and lag-based read routing</td><td>Outside this validation</td><td>We started with recovery on three VMs using local disks</td></tr>
</tbody>
</table>
<p class="op-caption">First-round feedback summary · October 31, 2026</p>

</OperatorSlide>

<!--
We deferred automatic rejoin with an existing disk until we can rule out stale data overwriting newer data. In v0.1 an operator approves the target and we rebuild from backup. The comparison with the official Operator covered forced deletion. Migration costs, collaboration, external storage, online scaling and lag-based read routing need separate work.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-compact op-session" section="03 · Development and architecture">

<h1 class="op-title">v0.1 scope: block writes, rebuild servers, restore backups</h1>

<div class="session-debug">
  <div><span>Block and resume writes</span><h3>Block writes when the primary is uncertain</h3><p>The Operator checks database roles<br>and stops the write Brokers.</p></div>
  <div><span>Rebuild after volume loss</span><h3>Rebuild the affected server</h3><p>After human approval, restore from backup<br>and rejoin as a replica.</p></div>
  <div><span>Backup and restore</span><h3>Restore into a new cluster</h3><p>The Instance Manager runs the backup<br>and verifies the files before restore.</p></div>
</div>
<p class="session-takeaway">In round one, we reported status. In v0.1, we control write access and coordinate data recovery.</p>

</OperatorSlide>

<!--
v0.1 adds three behaviors. First, block application writes when we cannot verify the primary and reopen the connection when it is safe. Second, rebuild a member from backup after a human approves the target. Third, restore a backup into a new cluster. We test single-member rebuild and whole-cluster restore separately.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-session" section="03 · Development and architecture · Current design" source="Architecture · Write quarantine ADR-0005 · Rebuild ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">v0.1 internals: Operator and Instance Manager</h1>

<svg class="op-arch" viewBox="0 0 900 359" role="img" aria-label="Two Operator controllers handle Kubernetes cluster and backup requests. The Operator scales the write Broker Deployment and calls the Instance Manager in each database Pod over token-authenticated HTTP. The Instance Manager checks CUBRID status, runs backups, prepares restores and keeps operation records on the volume. Backup artifacts use S3-compatible storage.">
  <defs>
    <marker id="v01-detail-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0L10 5L0 10z" fill="var(--blue)"/></marker>
  </defs>
  <rect class="box" x="0" y="41" width="161" height="102" rx="8"/>
  <text x="80" y="64" text-anchor="middle">Kubernetes API</text>
  <text class="s" x="80" y="89" text-anchor="middle">CubridCluster configuration</text>
  <text class="s" x="80" y="109" text-anchor="middle">CubridBackup request</text>
  <text class="s" x="80" y="129" text-anchor="middle">Approved rebuild request</text>
  <path class="ctl" d="M162 80H205" marker-end="url(#v01-detail-arrow)"/>
  <path class="ctl" d="M207 106H164" marker-end="url(#v01-detail-arrow)"/>
  <text class="s" x="183" y="122" text-anchor="middle">Status</text>

  <rect class="box op" x="210" y="0" width="323" height="239" rx="9" style="fill:none"/>
  <text class="b" x="224" y="23">Operator</text>
  <rect class="box op" x="225" y="36" width="293" height="82" rx="7"/>
  <text x="237" y="58">CubridCluster controller</text>
  <text class="s" x="237" y="79">Manage resources and server state</text>
  <text class="s" x="237" y="101">Control writes and coordinate rebuilds</text>
  <rect class="box op" x="225" y="128" width="293" height="60" rx="7"/>
  <text x="237" y="149">CubridBackup controller</text>
  <text class="s" x="237" y="173">Select a target, request backup and record results</text>
  <rect class="box im" x="225" y="199" width="293" height="26" rx="6"/>
  <text class="s b" x="237" y="217">Instance Manager client · Token-based HTTP</text>

  <rect class="box" x="0" y="195" width="180" height="78" rx="8"/>
  <text x="90" y="218" text-anchor="middle">Write Broker Deployment</text>
  <text class="s" x="90" y="241" text-anchor="middle">Scale to zero during quarantine</text>
  <text class="s" x="90" y="259" text-anchor="middle">End sessions and block new connections</text>
  <path class="ctl" d="M210 166H189V227H182" marker-end="url(#v01-detail-arrow)"/>

  <rect class="box ha" x="615" y="0" width="284" height="251" rx="9"/>
  <text class="b" x="631" y="23">Each CUBRID DB Pod</text>
  <rect class="box im" x="631" y="36" width="252" height="128" rx="8"/>
  <text class="b" x="643" y="59">Instance Manager</text>
  <text class="s" x="643" y="81">Read server role and HA status</text>
  <text class="s" x="643" y="104">Run backup and prepare restore</text>
  <text class="s" x="643" y="127">Check operation results</text>
  <text class="s" x="643" y="150">Persist operation records on disk</text>
  <path class="ctl" d="M518 211H575V103H629" marker-end="url(#v01-detail-arrow)"/>
  <rect class="box ink" x="631" y="183" width="252" height="51" rx="7"/>
  <text x="757" y="203" text-anchor="middle">CUBRID and data volume</text>
  <text class="s" x="757" y="222" text-anchor="middle">CUBRID elects the primary and replicates</text>
  <path class="ctl" d="M757 164V180" marker-end="url(#v01-detail-arrow)"/>

  <rect class="box store" x="615" y="284" width="284" height="58" rx="8"/>
  <text x="757" y="307" text-anchor="middle">S3-compatible backup storage</text>
  <text class="s" x="757" y="329" text-anchor="middle">Store and retrieve backups and checksums</text>
  <path class="ctl" d="M883 111H896V270H863V282" marker-end="url(#v01-detail-arrow)"/>

  <text class="s b" x="0" y="304">Retest on the v0.1 candidate</text>
  <text x="0" y="331">Write quarantine and release, approved volume rebuild, and new-cluster restore</text>
</svg>

</OperatorSlide>

<!--
Cluster and backup requests enter through the Kubernetes API. The cluster controller compares server state and stops write Brokers when necessary. The backup controller chooses a member, requests the backup and records the result. An Instance Manager in each database Pod handles authenticated requests. CUBRID still handles primary election and replication.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/DESIGN.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-compact op-session" section="03 · Development and architecture · Required scenarios" source="v0.1 scenario contract" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">Scenarios that must pass for v0.1</h1>

<table class="op-comparison">
<thead><tr><th scope="col">Test case</th><th scope="col">Scenario</th><th scope="col">Pass criteria</th></tr></thead>
<tbody>
<tr><td>Installation and normal operation</td><td>S00~S02</td><td>Install, run SQL reads and writes, and check three-member HA and replication</td></tr>
<tr><td>Forced server shutdown</td><td>S03 abrupt</td><td>Recover the write path and check data, including loss of the first DB member</td></tr>
<tr><td>Broker failure and Operator restart</td><td>S05~S06</td><td>Restore application access and verify status after the Operator restarts</td></tr>
<tr><td>Data volume loss</td><td>S10</td><td>Rebuild after operator approval and compare recovered data</td></tr>
<tr><td>Backup and new-cluster restore</td><td>S11~S12</td><td>Verify data after restore. Reject corrupt backups and incorrect targets.</td></tr>
<tr><td>Cluster operations and security</td><td>S13~S15</td><td>Check disk retention and deletion, tokens and disruption limits during drain</td></tr>
</tbody>
</table>
<p class="op-caption">Run every required test on the same release candidate. Cross-check status, events and metrics against real behavior.</p>

</OperatorSlide>

<!--
These are the scenarios the release candidate must pass. We start with installation, SQL and replication. Then we test recovery from abrupt server loss, Broker failure and Operator restart. We check the data after an approved rebuild or restore and make sure the system rejects bad backups and incorrect targets. Authentication and safe node drain are also required.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126#issuecomment-7096254639
-->

---

<OperatorSlide class="op-compact op-session" section="03 · Development and architecture · Measurements" source="v0.1 scenario contract" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">Scenarios for recovery time and missing data</h1>

<table class="op-comparison">
<thead><tr><th scope="col">Test case</th><th scope="col">Scenario</th><th scope="col">What we record</th></tr></thead>
<tbody>
<tr><td>Graceful primary shutdown</td><td>S03 graceful</td><td>Write downtime and whether writes were blocked unnecessarily</td></tr>
<tr><td>Power loss on a DB server VM</td><td>S04</td><td>Time until writes resume and data missing from the new primary</td></tr>
<tr><td>Network partition between DB servers</td><td>S07</td><td>Confirmed write block and recovery, plus missing pre-block writes</td></tr>
</tbody>
</table>
<p class="op-caption"><b>Repeated faults (S08)</b> are covered by repeated S04 and S07 runs. <b>Automatic rejoin with existing data (S09)</b> moves to v0.2.</p>
<p class="op-boundary">Hold the release if writes succeed after the block is verified or required measurements are missing.</p>

</OperatorSlide>

<!--
We also run graceful primary shutdown, a VM power cut and a network partition. We publish recovery time and any missing data with the test conditions. Repeated-fault coverage comes from rerunning S04 and S07. Successful writes after verified closure, before a valid release, block the release. Automatic rejoin with retained data is deferred to v0.2.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/118
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126#issuecomment-7096254639
-->

---

<OperatorSlide class="op-compact op-session" section="04 · Validation results and open issues · Method" source="Scenario contract · VM lab record #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">We checked the data after each fault</h1>
<div class="session-debug">
  <div><span>Before the fault</span><h3>Record successful writes</h3><p>For each write the app sends,<br>record which data the DB says it saved.</p></div>
  <div><span>During the fault</span><h3>Trigger a real failure</h3><p>Cut power, partition the network,<br>or force-delete the primary Pod.</p></div>
  <div><span>After recovery</span><h3>Compare the log and the DB</h3><p>Check which acknowledged rows remain<br>and whether any writes succeeded after the block.</p></div>
</div>
<p class="op-caption">We ran container-based automated tests and real faults in a three-VM lab.</p>

</OperatorSlide>

<!--
The client logs each successful write before and during a fault. After recovery, we compare that log against the data on each server. When write access is blocked, we check both existing and new connections. We use automated container tests and a dedicated three-VM lab for real faults.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-compact op-session" section="04 · Validation results and open issues · Comparison" source="VM lab comparison · Nov 25, 2026 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">Only the Lab Operator recovered from the second fault</h1>
<p class="op-caption">We force-deleted the primary Pod twice for each Operator in the same lab.</p>
<div class="session-debug session-two">
  <div><span>CUBRID Lab Operator</span><h3>Writes resumed</h3><p>CUBRID elected a new primary,<br>and all three DB servers returned automatically.</p></div>
  <div><span>Official CUBRID Operator</span><h3>Writes did not resume during the test</h3><p>After the second failure, no new primary was elected.<br>Writes were still down when we ended the test 31 minutes later.</p></div>
</div>
<p class="session-takeaway">The Lab Operator took longer on the first failure: 22.0 seconds versus 12.4 seconds.</p>

</OperatorSlide>

<!--
We forced the primary Pod down twice with each Operator in the same lab. After the second fault, writes resumed with the Lab Operator. On the official Operator, no new primary was elected and writes were still unavailable at cleanup 31 minutes later. After the first fault, the Lab Operator took longer: 22 seconds versus 12.4. These results apply to the tests shown here.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-session" section="04 · Validation results and open issues · VM lab" source="VM lab record #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">No writes succeeded after the block and three restores passed</h1>
<div class="session-debug">
  <div><span>Write quarantine</span><h3>0 successful writes</h3><p>We restarted the Operator during a partition.<br>No writes succeeded after the block.</p></div>
  <div><span>Backup restore</span><h3>3 successful runs</h3><p>We verified the restored data<br>in a new cluster.</p></div>
  <div><span>Power loss</span><h3>26–38 seconds</h3><p>From the recorded power-off marker to<br>the first successful write across three runs.</p></div>
</div>
<p class="op-caption">These are individual lab results. We will repeat the tests on the release candidate.</p>

</OperatorSlide>

<!--
Restarting the Operator during a partition preserved the write block and no writes succeeded after it. Three restores into a new cluster passed. In three separate power-off runs, the first successful write came 26 to 38 seconds after the recorded power-off marker. These tests still need to be repeated on the release candidate.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-compact op-session" section="04 · Validation results and open issues · Open issues" source="#1158 · Fix PR #1159" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158">

<h1 class="op-title">Missing data, delayed writes and restore evidence</h1>

<table class="op-comparison">
<thead><tr><th scope="col">What happened in testing</th><th scope="col">What we check for v0.1</th></tr></thead>
<tbody>
<tr><td><b>Missing data</b><br>13 rows after power loss;<br>up to 73 after a partition</td><td>Report missing pre-block writes with test conditions. No writes may succeed after the block is verified.</td></tr>
<tr><td><b>Delayed write recovery</b><br>Brokers took about 12–17 seconds to return</td><td>Measure time to the first successful write. Verify the conditions for reopening the write path.</td></tr>
<tr><td><b>Inconclusive restore results</b><br>Two first-round runs lost their SQL sessions</td><td>Compare restored data through SQL. Ask a second operator to reproduce the results from the documentation.</td></tr>
</tbody>
</table>
<p class="op-caption">These are individual test results. See slide 22 for the conditions.</p>

</OperatorSlide>

<!--
We found three open issues. In a test with replication paused, 13 acknowledged rows were absent from the new primary and stayed on the old disk. In separate partition tests, up to 73 were missing from the new primary. In the forced-deletion comparison, Brokers needed around 12 to 17 seconds to come back after release. Finally, a completed restore operation needs a SQL data check and independent reproduction.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/702
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/238
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/127
-->

---

<OperatorSlide class="op-session" section="04 · Validation results and open issues · Deferred work" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">Work deferred beyond v0.1</h1>

<table class="op-comparison">
<thead><tr><th scope="col">Deferred feature</th><th scope="col">v0.1 approach</th><th scope="col">Why we deferred it</th></tr></thead>
<tbody>
<tr><td><b>Automatic rejoin with retained data</b><br>v0.2</td><td>Rebuild from backup after operator approval</td><td>Verify that a returning server cannot overwrite newer data with older data.</td></tr>
<tr><td><b>Automatic adoption of existing volumes</b><br>v0.2</td><td>Do not automatically reuse old volumes</td><td>Verify that a volume is safe for the new cluster to reuse.</td></tr>
<tr><td><b>Faster reopening of write connections</b><br>Follow-up · No schedule</td><td>Stop write Brokers and publish time to recovery</td><td>Prove that existing sessions still end when recovery is faster.</td></tr>
</tbody>
</table>
<p class="op-caption">Our test environment did not cover external storage through CSI.</p>

</OperatorSlide>

<!--
We moved automatic rejoin with existing data and automatic volume adoption to v0.2. We need better evidence that a returning member or disk is safe to reuse. Faster write reopening is a separate follow-up without a schedule. Any faster design must still end existing write sessions.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/116
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/798
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1161
-->

---

<OperatorSlide class="op-compact op-session" section="05 · Questions for discussion">

<h1 class="op-title">When is it safe to resume writes and declare restore complete?</h1>

<ol class="op-questions"><li>If replication looks healthy but one server is unreachable, what evidence would you require before reopening writes?</li><li>After restoring a backup, what minimum evidence would you need to call the restore successful?</li></ol>

</OperatorSlide>

<!--
Two questions for the reviewers and other builders. If one server is unreachable while replication appears healthy, what evidence would you need before reopening writes? After restoring a backup, what data would you check before calling the restore successful?
-->

---

<OperatorSlide class="op-session" section="06 · Final presentation plan · Release scope" source="Roadmap · Scenario contract" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/testing/scenario-contract.md">

<h1 class="op-title">v0.1 ships only after the required safety tests pass</h1>
<div class="session-debug session-two">
  <div><span>Must pass</span><h3>No writes succeed after a verified block</h3><p>Test installation, replication, fault recovery, rebuild, backup and restore. Hold the release if a safety check fails or evidence is missing.</p></div>
  <div><span>Measure and publish</span><h3>Report recovery time and missing pre-block writes</h3><p>For power loss and network partitions, record when writes resume and which pre-block writes are missing from the new primary.</p></div>
</div>
<p class="session-takeaway">Keep earlier failures in the record. Before release, rerun the required tests on the same candidate.</p>

</OperatorSlide>

<!--
The release candidate must pass the required tests, from installation and replication through recovery and restore. A successful write after a verified block or missing required evidence means we hold the release. We publish recovery time and missing pre-block data with the test conditions and retain earlier failed results.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/126
-->

---

<OperatorSlide class="op-session" section="06 · Final presentation plan · Schedule" source="v0.1 roadmap" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">Freeze the candidate and repeat fault tests in December</h1>
<div class="session-debug">
  <div><span>December 7</span><h3>Freeze the candidate</h3><p>Pin the source, images, DB version and lab environment</p></div>
  <div><span>December 8–14</span><h3>Repeat fault tests</h3><p>Repeat required failures and run a 24-hour load test</p></div>
  <div><span>December 15–20</span><h3>Independent reproduction</h3><p>A second operator follows the docs to install, recover and restore</p></div>
</div>
<p class="session-takeaway">Dec 21–27: Decide whether to release. Hold the release if required evidence is missing.</p>

</OperatorSlide>

<!--
We plan to freeze the candidate on December 7. From December 8 to 14, we repeat the required faults and run a 24-hour load test. From December 15 to 20, another operator follows the documentation to install, recover and restore. The release decision is scheduled for December 21 to 27, subject to the evidence.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-session" section="06 · Final presentation plan · Summary">

<div class="op-clean-statement"><h1>We verified the write block<br>and found missing pre-block writes</h1></div>
<p class="op-lead">We will rerun the safety checks on the release candidate.</p>

</OperatorSlide>

<!--
We were able to verify that application writes stopped after the block. We also found acknowledged data missing from the new primary when the writes happened before the block. We will repeat the safety checks on the release candidate and publish the results with the test conditions.
-->

---

<OperatorSlide class="op-session" section="Q&amp;A" source="Operator repository" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator">

<div class="op-cover op-closing"><h1 class="op-title">Q&amp;A</h1><p class="op-lead">Thank you</p><p class="op-caption"><a href="#/20">Component roles</a> · <a href="#/21">Comparison details</a> · <a href="#/22">Limits and untested areas</a> · <a href="#/23">Additional results</a></p><div class="op-meta"><b>CUBRID Lab</b><span>Yeongseon Choe · Gyeongjun Paik</span></div><BrandMark name="lockup-horizontal" alt="CUBRID Lab" :height="40" /><p class="op-notice">CUBRID Lab is independent and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project. CUBRID is a trademark of its respective owner.</p></div>

</OperatorSlide>

<!--
Thank you. I’m happy to take questions. The appendix has component responsibilities, the comparison graph, test limits and additional results.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

<OperatorSlide class="op-compact op-session" section="Appendix · Component roles during a fault" source="Architecture · Write quarantine ADR-0005 · Rebuild ADR-0006" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md">

<h1 class="op-title">What the Operator, Instance Manager and CUBRID do</h1>
<table class="op-comparison">
<thead><tr><th scope="col">Component</th><th scope="col">Role during a fault</th></tr></thead>
<tbody>
<tr><td>Operator</td><td>Compares server states. Stops write Brokers when the primary is uncertain and coordinates an approved rebuild.</td></tr>
<tr><td>Instance Manager</td><td>Reads the role of each DB server and runs authenticated requests for local operations such as backup and restore.</td></tr>
<tr><td>CUBRID HA</td><td>Elects the primary and replicates data.</td></tr>
<tr><td>Broker</td><td>Forwards application SQL to CUBRID.</td></tr>
<tr><td>Kubernetes resources</td><td>StatefulSet deploys DB servers. PVC attaches data storage. Services provide application endpoints.</td></tr>
</tbody>
</table>

<p class="op-caption text-right"><a href="#/3">View the full architecture</a> · <a href="#/19">← Back to Q&amp;A</a></p>

</OperatorSlide>

<!--
The Operator compares state and coordinates write access and recovery. The Instance Manager reports local state and carries out authenticated operations on its database server. CUBRID elects a primary and replicates data. The Broker handles application SQL.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0006-node-join-rebuild.md
-->

---

<OperatorSlide class="op-compact op-session" section="Appendix · Comparison details" source="VM lab comparison · Nov 25, 2026 · #122" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122">

<h1 class="op-title">Write downtime in the two Operator tests</h1>
<svg class="session-chart" style="max-height:240px" viewBox="0 0 860 300" role="img" aria-label="Acknowledged writes per second after the second primary Pod deletion. The official Operator did not recover before the test ended. The Lab Operator resumed writes about 43 seconds after deletion."><line x1="56" x2="670" y1="260.0" y2="260.0" stroke="var(--line)" stroke-width="1"/><text x="48" y="264.0" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">0</text><line x1="56" x2="670" y1="178.7" y2="178.7" stroke="var(--line)" stroke-width="1"/><text x="48" y="182.7" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">5</text><line x1="56" x2="670" y1="97.3" y2="97.3" stroke="var(--line)" stroke-width="1"/><text x="48" y="101.3" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">10</text><line x1="56" x2="670" y1="16.0" y2="16.0" stroke="var(--line)" stroke-width="1"/><text x="48" y="20.0" text-anchor="end" fill="var(--muted)" style="font-size:12px;font-weight:400">15</text><text x="56.0" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">-30 s</text><text x="117.4" y="280" text-anchor="middle" fill="var(--ink)" style="font-size:12px;font-weight:400">0</text><text x="240.2" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+60 s</text><text x="363.0" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+120 s</text><text x="485.8" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+180 s</text><text x="608.6" y="280" text-anchor="middle" fill="var(--muted)" style="font-size:12px;font-weight:400">+240 s</text><line x1="117.4" x2="117.4" y1="16" y2="260" stroke="var(--ink)" stroke-width="1.5" stroke-dasharray="4 4"/><text x="123.4" y="28" fill="var(--ink)" style="font-size:12px;font-weight:400">Primary Pod force-deleted</text><polyline points="58.0,162.4 62.1,146.1 66.2,178.7 70.3,162.4 74.4,162.4 78.5,154.3 82.6,186.8 86.7,243.7 90.8,235.6 94.9,154.3 99.0,146.1 103.1,146.1 107.2,194.9 111.3,219.3 115.4,219.3 119.4,178.7 123.5,260.0 127.6,260.0 131.7,260.0 135.8,260.0 139.9,260.0 144.0,260.0 148.1,260.0 152.2,260.0 156.3,260.0 160.4,260.0 164.5,260.0 168.6,260.0 172.7,260.0 176.8,260.0 180.8,260.0 184.9,260.0 189.0,260.0 193.1,260.0 197.2,260.0 201.3,260.0 205.4,260.0 209.5,260.0 213.6,260.0 217.7,260.0 221.8,260.0 225.9,260.0 230.0,260.0 234.1,260.0 238.2,260.0 242.2,260.0 246.3,260.0 250.4,260.0 254.5,260.0 258.6,260.0 262.7,260.0 266.8,260.0 270.9,260.0 275.0,260.0 279.1,260.0 283.2,260.0 287.3,260.0 291.4,260.0 295.5,260.0 299.6,260.0 303.6,260.0 307.7,260.0 311.8,260.0 315.9,260.0 320.0,260.0 324.1,260.0 328.2,260.0 332.3,260.0 336.4,260.0 340.5,260.0 344.6,260.0 348.7,260.0 352.8,260.0 356.9,260.0 361.0,260.0 365.0,260.0 369.1,260.0 373.2,260.0 377.3,260.0 381.4,260.0 385.5,260.0 389.6,260.0 393.7,260.0 397.8,260.0 401.9,260.0 406.0,260.0 410.1,260.0 414.2,260.0 418.3,260.0 422.4,260.0 426.4,260.0 430.5,260.0 434.6,260.0 438.7,260.0 442.8,260.0 446.9,260.0 451.0,260.0 455.1,260.0 459.2,260.0 463.3,260.0 467.4,260.0 471.5,260.0 475.6,260.0 479.7,260.0 483.8,260.0 487.8,260.0 491.9,260.0 496.0,260.0 500.1,260.0 504.2,260.0 508.3,260.0 512.4,260.0 516.5,260.0 520.6,260.0 524.7,260.0 528.8,260.0 532.9,260.0 537.0,260.0 541.1,260.0 545.2,260.0 549.2,260.0 553.3,260.0 557.4,260.0 561.5,260.0 565.6,260.0 569.7,260.0 573.8,260.0 577.9,260.0 582.0,260.0 586.1,260.0 590.2,260.0 594.3,260.0 598.4,260.0 602.5,260.0 606.6,260.0 610.6,260.0 614.7,260.0 618.8,260.0 622.9,260.0 627.0,260.0 631.1,260.0 635.2,260.0 639.3,260.0 643.4,260.0 647.5,260.0 651.6,260.0 655.7,260.0 659.8,260.0 663.9,260.0 668.0,260.0" fill="none" stroke="var(--blue)" stroke-width="2" stroke-linejoin="round"/><polyline points="58.0,154.3 62.1,162.4 66.2,146.1 70.3,129.9 74.4,162.4 78.5,154.3 82.6,154.3 86.7,154.3 90.8,154.3 94.9,146.1 99.0,162.4 103.1,138.0 107.2,146.1 111.3,138.0 115.4,154.3 119.4,235.6 123.5,138.0 127.6,97.3 131.7,113.6 135.8,138.0 139.9,260.0 144.0,260.0 148.1,260.0 152.2,260.0 156.3,260.0 160.4,260.0 164.5,260.0 168.6,260.0 172.7,260.0 176.8,260.0 180.8,260.0 184.9,260.0 189.0,260.0 193.1,260.0 197.2,260.0 201.3,260.0 205.4,154.3 209.5,129.9 213.6,146.1 217.7,154.3 221.8,138.0 225.9,146.1 230.0,162.4 234.1,146.1 238.2,138.0 242.2,146.1 246.3,138.0 250.4,146.1 254.5,154.3 258.6,138.0 262.7,154.3 266.8,154.3 270.9,154.3 275.0,154.3 279.1,146.1 283.2,154.3 287.3,162.4 291.4,146.1 295.5,146.1 299.6,154.3 303.6,146.1 307.7,154.3 311.8,146.1 315.9,154.3 320.0,154.3 324.1,146.1 328.2,154.3 332.3,154.3 336.4,146.1 340.5,162.4 344.6,146.1 348.7,162.4 352.8,154.3 356.9,154.3 361.0,146.1 365.0,170.5 369.1,154.3 373.2,154.3 377.3,162.4 381.4,154.3 385.5,154.3 389.6,146.1 393.7,154.3 397.8,162.4 401.9,154.3 406.0,162.4 410.1,170.5 414.2,146.1 418.3,154.3 422.4,154.3 426.4,154.3 430.5,146.1 434.6,154.3 438.7,162.4 442.8,162.4 446.9,138.0 451.0,170.5 455.1,170.5 459.2,154.3 463.3,162.4 467.4,146.1 471.5,138.0 475.6,154.3 479.7,146.1 483.8,146.1 487.8,162.4 491.9,138.0 496.0,170.5 500.1,162.4 504.2,170.5 508.3,162.4 512.4,146.1 516.5,162.4 520.6,162.4 524.7,146.1 528.8,154.3 532.9,154.3 537.0,162.4 541.1,170.5 545.2,138.0 549.2,154.3 553.3,154.3 557.4,162.4 561.5,170.5 565.6,170.5 569.7,146.1 573.8,154.3 577.9,162.4 582.0,154.3 586.1,162.4 590.2,138.0 594.3,154.3 598.4,170.5 602.5,162.4 606.6,170.5 610.6,154.3 614.7,154.3 618.8,162.4 622.9,146.1 627.0,162.4 631.1,162.4 635.2,138.0 639.3,146.1 643.4,162.4 647.5,154.3 651.6,146.1 655.7,146.1 659.8,146.1 663.9,154.3 668.0,154.3" fill="none" stroke="#9a3412" stroke-width="2" stroke-linejoin="round"/><circle cx="668.0" cy="154.3" r="4" fill="#9a3412" stroke="var(--paper)" stroke-width="2"/><text x="680" y="150.3" fill="var(--ink)" style="font-size:13px;font-weight:700">Lab Operator</text><text x="680" y="167.3" fill="var(--muted)" style="font-size:12px;font-weight:400">Longest gap: 32.8 s</text><text x="680" y="184.3" fill="var(--muted)" style="font-size:12px;font-weight:400">Resumed at +42.5 s</text><circle cx="668.0" cy="260.0" r="4" fill="var(--blue)" stroke="var(--paper)" stroke-width="2"/><text x="680" y="242.0" fill="var(--ink)" style="font-size:13px;font-weight:700">cubrid-operator</text><text x="680" y="258.0" fill="var(--muted)" style="font-size:12px;font-weight:400">No new primary</text><text x="680" y="274.0" fill="var(--muted)" style="font-size:12px;font-weight:400">Still down at 31 min</text><text x="56" y="296" fill="var(--muted)" style="font-size:11px;font-weight:400">Acknowledged writes/s (2 s average) · Same client, one row per transaction · 282 s shown after deletion</text><line x1="137.3" x2="137.3" y1="34" y2="260" stroke="var(--muted)" stroke-width="1" stroke-dasharray="2 3"/><text x="143.3" y="48" fill="var(--ink)" style="font-size:12px;font-weight:700">+9.7 s: write quarantine</text><text x="143.3" y="64" fill="var(--muted)" style="font-size:12px;font-weight:400">+2.5–9.6 s: promoted ha-0 accepted writes; 0 missing</text></svg>
<p class="op-caption"><b>32.8 seconds</b> was the longest gap between successful write responses. <b>42.5 seconds</b> ran from deletion to the first successful write after quarantine.</p>
<p class="op-caption text-right"><a href="#/19">← Back to Q&amp;A</a></p>

</OperatorSlide>

<!--
The 32.8 seconds measure the longest interval between successful writes. The 42.5 seconds start when we delete the Pod and end at the first successful write after quarantine. There were a few successful writes immediately after deletion and before the block.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->

---

<OperatorSlide class="op-compact op-session" section="Appendix · Limits and test conditions" source="#1035 · #702 · #938" source-url="https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md">

<h1 class="op-title">Missing data, write downtime and untested storage</h1><ol class="op-risks"><li><b>13 acknowledged writes missing from the new primary after VM power loss</b><span>Nov 19, 2026 · Replication was deliberately stopped · Rows remained on the old primary’s disk</span></li><li><b>Up to 73 acknowledged writes missing from the new primary after a partition</b><span>Nov 17–18 · Five VM partition runs had 13–73 missing rows. In one run, the member missing 73 rows became active primary.</span></li><li><b>A graceful primary shutdown blocked the write path for 28 seconds (Kind)</b><span>The write block was unnecessary. Report the duration and cause.</span></li><li><b>Tested on node-local storage</b><span>CSI volume portability, snapshots and resizing remain untested</span></li></ol><p class="op-boundary"><b>How we report the result</b>　We distinguish Operator behavior from CUBRID engine limits and report the conditions and impact.</p>

<p class="op-caption text-right"><a href="#/19">← Back to Q&amp;A</a></p>

</OperatorSlide>

<!--
The 13 and 73 refer to different tests. The 13 rows remained on the old primary’s disk after power loss with replication stopped. The maximum of 73 was observed after a network partition. The 28 seconds are a separate case of unnecessary write blocking during graceful shutdown. CSI behavior was outside our test environment.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1035
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/docs/adr/0005-failover-split-brain.md
https://github.com/cubrid-lab/cubrid-kubernetes-operator/blob/main/ROADMAP.md
-->

---

<OperatorSlide class="op-compact op-session" section="Appendix · Additional test results">

<h1 class="op-title">Volume replacement and rejection of old release tokens</h1>
<table class="op-comparison">
<thead><tr><th scope="col">Test</th><th scope="col">Result</th></tr></thead>
<tbody>
<tr><td>Rebuild a server after replacing its data volume</td><td>We compared recovered data with the client’s successful-write log.</td></tr>
<tr><td>Partition the network again after releasing quarantine</td><td>Both old release tokens were rejected. No writes succeeded after the path closed.</td></tr>
<tr><td>Idle database connections dropped</td><td>After allowing the connection probe in the network policy, sessions stayed open under the same conditions.</td></tr>
</tbody>
</table>

<p class="op-caption text-right"><a href="#/19">← Back to Q&amp;A</a></p>

</OperatorSlide>

<!--
After a disk replacement, we compared the rebuilt server’s data against the client’s successful-write history. In a second network partition, the Operator rejected two old release tokens and no writes succeeded after blocking. We also fixed the idle-connection problem in network policy and retested it.

Sources:
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/1158
https://github.com/cubrid-lab/cubrid-kubernetes-operator/issues/122
-->
