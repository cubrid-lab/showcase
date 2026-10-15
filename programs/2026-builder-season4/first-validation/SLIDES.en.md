# CUBRID Kubernetes Operator — First Validation Outline

Status: outline only. Fill in `[Draft]` and `[Confirm]` before producing PPTX.
See the [presentation brief](README.md) for delivery requirements and
[SLIDES.ko.md](SLIDES.ko.md) for the matching Korean outline.

Talk: 10 minutes (600 seconds). Q&A: 10 minutes. The proposed timing below
covers all seven required topics. No separate demo slot is allocated.

| Slide | Required topic | Time |
|---|---|---|
| 1 | Project and team introduction | 60 seconds |
| 2 | Problem and affected users | 90 seconds |
| 3 | Current approaches and limitations of existing open source | 90 seconds |
| 4 | Proposed solution | 90 seconds |
| 5 | Draft architecture | 120 seconds |
| 6 | 12-week roadmap, team roles, and first public release scope | 90 seconds |
| 7 | Topics for discussion and feedback | 60 seconds |
| Total | | 600 seconds |

## 1. Project and team introduction — 60 seconds

- Project: CUBRID Kubernetes Operator
- `[Draft]` One sentence describing the user and operational task it helps with
- `[Confirm]` Team name, member names, relevant experience, and project roles
- Repository: https://github.com/cubrid-lab/cubrid-kubernetes-operator

## 2. Problem and affected users — 90 seconds

- `[Draft]` The initial target user and a specific operational situation
- `[Draft]` The recurring work, incident response, or operational uncertainty to address this season
- `[Confirm]` Interviews or real examples, observed costs and frequency, and sources
- Separate untested hypotheses from confirmed user needs

## 3. Current approaches and limitations of existing open source — 90 seconds

- `[Draft]` Manual procedures, scripts, and deployment tools the target user currently uses
- `[Confirm]` Existing open-source alternatives and versions, with official documentation or reproduction results
- `[Draft]` What each approach covers and what work remains for this use case
- Avoid unverified claims of uniqueness, absence of alternatives, or full automation

## 4. Proposed solution — 90 seconds

- `[Draft]` How users describe the desired state and observe operational status
- `[Draft]` Before and after for one core use case, with a success criterion
- `[Confirm]` Distinguish the proposal, implemented features, and verified behavior
- `[Confirm]` Explain CUBRID and Operator responsibilities during failures using the ADRs

## 5. Draft architecture — 120 seconds

- `[Confirm]` Integration platforms and versions, supported by DESIGN.md and ADRs
- `[Draft]` User request → Kubernetes resources → control components → CUBRID integration
- `[Draft]` Diagram the main components and the observation, decision, and change flow
- `[Draft]` Separate the application's database data path from control and status information
- `[Confirm]` Behavior and safety boundaries when observations are incomplete or components fail
- Evidence: `[commit / document path / verification date]`

## 6. 12-week roadmap, team roles, and first public release scope — 90 seconds

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

## 7. Topics for discussion and feedback — 60 seconds

- `[Draft]` One user or problem hypothesis to validate
- `[Draft]` One release-scope or architecture decision needing advice
- `[Draft]` Help needed with user feedback, test environments, or operational experience
- Prepare supporting evidence and unresolved questions separately for Q&A
