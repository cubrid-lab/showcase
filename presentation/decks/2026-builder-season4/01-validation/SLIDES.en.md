# 1. Project and team

- **CUBRID Kubernetes Operator**
- [Draft] One sentence about the target user and operational task
- [Confirm] Team name · members · relevant experience · roles

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 60 seconds</div>

<!--
- Project: CUBRID Kubernetes Operator
- `[Draft]` One sentence describing the user and operational task it helps with
- `[Confirm]` Team name, member names, relevant experience, and project roles
- Repository: https://github.com/cubrid-lab/cubrid-kubernetes-operator
-->

---

# 2. Problem and affected users

- [Draft] Initial target user and a specific operational situation
- [Draft] Recurring work or incident response to address this season
- [Confirm] Real examples · interviews · observed cost and frequency

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 90 seconds</div>

<!--
- `[Draft]` The initial target user and a specific operational situation
- `[Draft]` The recurring work, incident response, or operational uncertainty to address this season
- `[Confirm]` Interviews or real examples, observed costs and frequency, and sources
- Separate untested hypotheses from confirmed user needs
-->

---

# 3. Current approaches and limitations

- [Draft] Existing manual procedures · scripts · deployment tools
- [Confirm] Open-source alternatives and versions, with sources
- [Draft] What each approach solves and what work remains

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 90 seconds</div>

<!--
- `[Draft]` Manual procedures, scripts, and deployment tools the target user currently uses
- `[Confirm]` Existing open-source alternatives and versions, with official documentation or reproduction results
- `[Draft]` What each approach covers and what work remains for this use case
- Avoid unverified claims of uniqueness, absence of alternatives, or full automation
-->

---

# 4. Proposed solution

- [Draft] Describe desired state → observe status → make changes
- [Draft] Before and after for one use case, with a success criterion
- [Confirm] Separate proposed, implemented, and verified behavior
- [Confirm] CUBRID and Operator responsibilities during failures

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 90 seconds</div>

<!--
- `[Draft]` How users describe the desired state and observe operational status
- `[Draft]` Before and after for one core use case, with a success criterion
- `[Confirm]` Distinguish the proposal, implemented features, and verified behavior
- `[Confirm]` Explain CUBRID and Operator responsibilities during failures using the ADRs
-->

---

# 5. Draft architecture

- [Confirm] Integration platforms · main components · versions
- [Draft] Request → Kubernetes resources → control components → CUBRID
- [Draft] Diagram database data paths and control/status flows
- [Confirm] Safety boundaries for incomplete observations and failures

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 120 seconds</div>

<!--
- `[Confirm]` Integration platforms and versions, supported by DESIGN.md and ADRs
- `[Draft]` User request → Kubernetes resources → control components → CUBRID integration
- `[Draft]` Diagram the main components and the observation, decision, and change flow
- `[Draft]` Separate the application's database data path from control and status information
- `[Confirm]` Behavior and safety boundaries when observations are incomplete or components fail
- Evidence: `[commit / document path / verification date]`
-->

---

# 6. 12-week plan and first public release

- [Confirm] Season dates and first public release scope

| Period | Verifiable goal | Owner | Evidence |
|---|---|---|---|
| Weeks 1–3 | [Draft] | [Confirm] | [Draft] |
| Weeks 4–6 | [Draft] | [Confirm] | [Draft] |
| Weeks 7–9 | [Draft] | [Confirm] | [Draft] |
| Weeks 10–12 | [Draft] | [Confirm] | [Draft] |

*Writing scaffold, pending agreement · confirm completion criteria and exclusions*

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 90 seconds</div>

<!--
Start and end dates: `[Confirm]`. The four periods below are a writing scaffold,
not an agreed schedule.

| Period | Verifiable goal | Team member | Completion evidence |
|---|---|---|---|
| Weeks 1–3 | [Draft] | [Confirm] | [Draft] |
| Weeks 4–6 | [Draft] | [Confirm] | [Draft] |
| Weeks 7–9 | [Draft] | [Confirm] | [Draft] |
| Weeks 10–12 | [Draft] | [Confirm] | [Draft] |

- `[Confirm]` Features, supported environments, documentation, and tests in the first public release at season end
- `[Confirm]` Release completion criteria and exclusions
- Use the Operator ROADMAP.md for overall delivery and validation status;
  this table records the presentation's season-specific plan
-->

---

# 7. Discussion and feedback

- [Draft] A user or problem hypothesis to validate
- [Draft] A question about release scope or architecture
- [Draft] Help needed with user feedback, test environments, or operations

<div class="absolute bottom-8 right-12 text-sm opacity-60">Draft · 60 seconds</div>

<!--
- `[Draft]` One user or problem hypothesis to validate
- `[Draft]` One release-scope or architecture decision needing advice
- `[Draft]` Help needed with user feedback, test environments, or operational experience
- Prepare supporting evidence and unresolved questions separately for Q&A
-->
