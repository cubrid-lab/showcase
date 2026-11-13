# Contributing

**Title policy:** Use type-only issue titles (`feat:`, `bug:`, `docs:`) without module scopes. Keep Conventional Commits for PRs/commits and verifiable acceptance criteria for issues; triage and PR CI have separate responsibilities. See [AGENTS.md](AGENTS.md).

Use a focused pull request with a clear purpose, changed files, validation
evidence and any required documentation updates. Human contributors and
all AI-assisted implementations follow the same review criteria.

Required GitHub CI checks on the final head are authoritative.
Local validation is encouraged but does not create a separate merge
requirement. Oracle, Copilot and agent-review are optional advisory
reviewers; their outputs are not approval or evidence of passing tests.
The responsible maintainer examines correctness, security, affected
published assets and CI status before merging. Validate referenced artifacts,
licenses, privacy-sensitive content and documentation links; report which
published outputs were actually checked.
Do not weaken existing workflow, release, credential or publishing
security requirements.

## Showcase issue and agent handoff

Work in one **showcase-specific** issue/PR with clear evidence of what content,
links or presentation assets change. Review the latest `main`, active content
PRs and the historical source/provenance before editing an existing exhibit.
Do not replace another contributor's media or rewrite archival event material
to satisfy unrelated agent instructions.

New issues begin with `status: needs triage`. Maintainers check validity,
duplicates, local ownership, scope and relative priority against all open
issues, then confirm one `priority: critical/high/medium/low` and one
`size: XS/S/M/L/XL`. Clear the intake status only after checking actual
saved labels. Human contributors can propose unclaimed changes without an AI
review requirement; maintainer-operated autonomous agents need authorization
and verified assignment before taking reserved work.

The existing `.github/workflows/pages.yml` builds and publishes **HTML
presentations** from `presentation/` using Node 24, `npm ci` and
`npm run build:site`; it runs on qualifying pushes to `main` or manually,
not as proof that a docs-only PR has been deployed. Run the matching
presentation build from its directory when applicable and state what was
actually validated. Review rights, credit, privacy and public links before
publishing; a media-generation model or AI reviewer cannot approve rights.
Historic contest dates and demonstration artifacts are context, not delivery
gates for ordinary repository development.


## Issue handoff and development progress

Use the issue and PR's actual state as evidence. Classification, authorization,
implementation, review and completion are **different decisions**:

1. **Intake / triage:** A newly filed issue starts with `status: needs triage`.
   Check evidence or reproduction, duplicate open/closed issues and overlapping
   PRs, repository scope, type, priority, size, dependencies, and verifiable
   acceptance criteria. A maintainer removes the intake label only after
   confirming the saved GitHub metadata. Do not infer priority, size, or triage
   completion automatically from the title or an AI suggestion.
2. **Ready:** Triage completion alone does not authorize development. Mark work
   Ready only when the intended outcome and non-goals are bounded, blockers
   have been resolved, and any repository-specific product, architecture,
   safety or compatibility decisions have been accepted. Unresolved research
   remains investigation; blocked work records its dependency and next action.
3. **In Progress:** Before maintainer-directed or autonomous implementation,
   identify the actual implementer in the GitHub Assignee field, check whether
   another open PR already owns the change, and link the implementation PR to
   its issue. Human-led outside contributors may propose a change on an
   unclaimed issue without prior assignment or an AI-tool-specific approval;
   coordinate with existing assignees and follow the local contribution rules.
4. **In Review:** A PR is in review only when its scoped change and verification
   evidence are available. Check the required CI on the final PR head, test
   coverage appropriate to the risk, unresolved review findings and any
   repository-specific independent review or live-system validation. A bot
   review or passing CI cannot replace an outstanding product/safety decision.
5. **Done:** Record the actual disposition: a merged and validated change,
   a completed investigation with evidence, or an explained duplicate/not-
   planned closure. Use an issue-closing PR keyword only if merging actually
   satisfies its acceptance criteria. A merged PR is not proof that any
   deferred integration, fault, security or release verification has passed.

**Tracking:** Where a GitHub Project is in use, track `Todo`, `Ready`,
`In Progress`, `In Review` and `Done` in its Status field; record
`Blocked` and the unblock condition when applicable. Without a Project,
record the next action in the issue, maintain the Assignee and linked PR, and
avoid creating duplicate status-label taxonomies. Priority means impact,
size means estimated effort, and neither is a work-in-progress indicator.
This guidance does not add an automatic merge gate or supersede this
repository's existing design, testing, security, or release requirements.
