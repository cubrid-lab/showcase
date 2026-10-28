# AGENTS.md

## Organization-wide writing standard

Follow [cubrid-lab's Issue, PR and commit policy](https://github.com/cubrid-lab/.github/blob/main/docs/ISSUE_PR_COMMIT_STANDARD.md). Issue titles use a type-only prefix such as `feat: ...`, `bug: ...`, or `docs: ...` without a required module scope. Describe a human-readable goal/problem and verifiable acceptance criteria. Triage handles validity, scope, duplicates, priority and size; PR and commit titles retain Conventional Commits/local CI requirements. Avoid internal review codes, personal comments and agent execution logs in issue prose.


## Scope

This repository maintains showcase content and demo assets. Preserve existing
repository-specific build, publishing, security and licensing rules.

## Unified PR Review Workflow

Apply the same review and merge process regardless of whether the change
is human-authored or developed with OpenCode, Codex, Claude Code,
ChatGPT, Copilot or another agent.

1. Keep the change focused; add relevant validation and affected docs.
2. Trust required repository GitHub CI checks at the final PR head as the
   official automated verification. Local runs are encouraged, not an
   additional mandatory merge gate.
3. Review correctness, scope, security, maintainability and publication
   effects. Optional Oracle, Copilot or agent-review output is advisory,
   never required because of which coding tool was used.
4. Resolve or disposition findings. The responsible maintainer checks
   required CI, remaining risks and affected publishing paths and
   decides whether to merge.

Verify referenced artifacts, licenses, privacy-sensitive material, documentation links, and any published outputs before merging.
High-risk workflow permissions, secrets and publishing changes need
independent maintainer scrutiny; existing GitHub branch protections
remain unchanged.

## Issue triage lifecycle

Every new issue in this repository starts with `status: needs triage`.
The issue-opened GitHub Actions workflow applies it to external submissions.
Automation created with `GITHUB_TOKEN` must attach that label when filing,
since its own issue events may not trigger another workflow.

1. Check evidence and impact, unknowns, duplicate/open-PR overlap, repository
   scope, issue type, non-goals, acceptance and dependencies. Close duplicate
   or invalid issues with a reason.
2. Review **all other open issues in this repository**, using pagination,
   before assigning relative priority, considering current risks, work
   already in progress, and blockers rather than creation order.
3. Choose exactly one `priority: critical/high/medium/low` and one existing
   `size: XS/S/M/L/XL` (effort, not importance). Split oversized independent
   implementation tasks, preserving accepted scope and contributor history.
4. Read back GitHub's actual saved issue labels and classification. Only
   remove `status: needs triage` after reviewing type, priority, size,
   evidence, duplicates and backlog position. Keep the status if unresolved.

Do not auto-rank priorities or auto-close triage in CI. This introduces
no new PR merge gate and preserves existing design and release standards.

## Human-readable communication (all agents)

Use this rule for text authored or edited by Codex, Claude Code, OpenCode,
ChatGPT, Copilot, or any other agent. It applies to issues, PRs, reviews,
comments, checklists, status updates, commit summaries, release notes,
documentation, presentations, and other maintainer-facing writing.

- Write for a reader unfamiliar with the underlying script, storyboard,
  automation run, or agent plan. Name the actual project, component,
  action, evidence, and location in ordinary, clear language.
- Never use unexplained internal identifiers as reader-facing labels or
  checklist instructions (for example, `H1, P1, C1, K1, F2` or `A1/B1/R1/R2`).
  Do not substitute `P1`/`P2` for repository priority labels.
- When an internal identifier is necessary for accurate cross-reference,
  **describe the subject first**, then add the identifier in context:
  `pycubrid introduction (0:20; storyboard shot P1)`. Use descriptive
  names and timestamps, section titles, or paths wherever practical.
- Use natural, actionable wording. Prefer `Listen to the full narration and
  verify the pronunciation of each project name` to `Maintainer full listen`.
  Avoid compressed task fragments, unexplained acronyms, and generated
  process/status jargon.
- Keep legitimate technical identifiers unchanged in code, tests, structured
  data, logs, specifications, and exact evidence references. Issue numbers,
  filenames, command names, APIs, error codes, and hashes are not prohibited.
  Do not break machine-readable references to improve prose.
- Before publishing, reread the text as a first-time maintainer. It should
  state what happened or needs to happen, why, and where without requiring a
  separate lookup table. Edit an existing editable comment to correct unclear
  wording rather than adding redundant follow-up comments.

This is a shared writing convention, not a new CI check, reviewer approval,
or merge gate. Keep existing repository-specific technical and safety rules.
