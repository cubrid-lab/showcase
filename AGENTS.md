# AGENTS.md

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
