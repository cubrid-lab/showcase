# Contributing

**Title policy:** Use type-only issue titles (`feat:`, `bug:`, `docs:`) without module scopes. Keep Conventional Commits for PRs/commits and verifiable acceptance criteria for issues; triage and PR CI have separate responsibilities. See [organization guidance](https://github.com/cubrid-lab/.github/blob/main/docs/ISSUE_PR_COMMIT_STANDARD.md).

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
