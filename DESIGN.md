# Design

## Source of truth

- Status: Active
- Last refreshed: 2026-10-15
- Primary product surfaces: HTML presentations, matching PDF/PPTX exports, presentation index.
- Evidence reviewed: `presentation/slides.md`, `presentation/style.css`, `presentation/components/`, the published contest deck, the Builder first-validation notice, and the Operator README/DESIGN/ROADMAP/ADRs pinned in the event's `SOURCES.md`.
- Existing evidence: the contest uses white backgrounds, bundled Pretendard, blue emphasis, chapter transitions, diagrams, screenshots, and speaker notes. Design decision: extend that language to the Operator talk rather than shipping a bullet outline.

## Brand

- Personality: clear, technical, careful, human.
- Trust signals: actual repository evidence, explicit safety boundaries, source footers, honest experimental status.
- Avoid: invented metrics, fake terminals, unsupported competitor claims, pending brand symbols, decorative dashboard cards, and empty writing prompts.

## Product goals

- Deliver a substantive ten-minute Korean first-validation talk and a content-equivalent English deck.
- Make all seven requested topics understandable without a live demo.
- Publish the HTML decks and derive PDF/PPTX from the same sources.
- Non-goals: a production-readiness claim, a database demo, or a pixel copy of the contest narrative.
- Success: a viewer can explain the problem, architecture, authority boundary, first-release target and feedback request after the talk.

## Personas and jobs

- Audience: Builder validation reviewers and technical peers.
- Proposed project users: DB operators and platform engineers preparing to run CUBRID on Kubernetes. This is a target-user hypothesis, not interview evidence.
- Jobs: understand the proposal, challenge its assumptions, and assess the season's scope and validation plan.
- Context: projector presentation, ten-minute talk plus ten-minute Q&A; browser review on desktop or mobile.

## Information architecture

- Presentation index → event/program → presentation round → language-specific HTML deck.
- Source and evidence remain accessible from the event brief.
- Talk hierarchy: opening/team → operating problem → current approaches → declarative proposal → architecture/safety → evidence → season plan/roles/release → discussion/closing.

## Design principles

- One claim or question per slide; the headline should carry its meaning.
- Show relationships with diagrams and timelines instead of dense bullet lists.
- Separate intended design, documented Kind observations and unvalidated release gates.
- Reuse the contest's typography/tokens/layout vocabulary with an explicit Operator class. Preserve the existing contest rendering.
- Use more slides with fewer ideas, while keeping the total speaker budget at 600 seconds.

## Visual language

- Color: white `#ffffff`, ink `#0f1b2d`, CUBRID blue `#1f4e8c`, muted `#5b6b82`, line `#d8dee8`. Red only for an actual unresolved safety condition.
- Typography: bundled Pretendard; large two-line headings; readable short supporting sentences; no remote font dependency.
- Layout: 16:9 canvas, consistent small section/source/page chrome, ample whitespace, purposeful two-column compositions.
- Shape: thin diagram borders; modest radii; no decorative shadows or card walls.
- Motion: restrained transitions; all content must be understandable in static exports.
- Imagery: code-native architecture/control/data diagrams; no invented team photos or synthetic evidence screenshots.

## Components

- Reuse existing shared style tokens and utilities; retain the contest's class support.
- `OperatorSlide.vue`: section label, content slot, source and page footer.
- Operator-only layouts/diagrams live in `operator.css` under `.operator-deck`.
- Deck sources own narrative and translated text. Components own reusable layout, not project claims.

## Accessibility

- Headings and diagram labels remain readable at presentation size.
- Text/lines identify states; color is never the only signal.
- Use actual text in diagrams and semantic headings; language attributes match each deck.
- Preserve keyboard slide navigation and visible focus on links.
- Avoid essential animations; respect reduced motion where custom motion exists.

## Responsive behavior

- Slidev scales the fixed 16:9 presentation canvas; do not reflow slide meaning on mobile.
- The index remains responsive; deck typography must remain legible when expanded full screen.
- No information depends on hover.

## Interaction states

- Loading: assets resolve within the deployed deck base path.
- Empty: do not publish writing prompts as a completed presentation.
- Error: unknown evidence stays unknown; a source link is available for technical claims.
- Success: opening a presentation link immediately displays the deck.
- Disabled: no dead download buttons or nonexistent round links.
- Offline: local fonts and generated assets; no CDN resource required by the slides.

## Content voice

- Korean talk: natural spoken sentences. English: equivalent claims and diagrams, not literal cramped translation.
- Keep CUBRID's master/slave terminology when discussing engine roles, and distinguish it from Kubernetes readiness.
- Acknowledge the existing official Operator and its actual role/health capabilities.
- Target dates are targets; Kind evidence is not VM, zone or production validation.
- Mandatory release safety gates cannot be reduced to fit the calendar.

## Implementation constraints

- Existing Slidev 53 and theme; no new dependencies.
- Share existing CSS through an explicit class alias; scope new styles to Operator slides.
- Keep source paths, HTML routes, and export commands stable.
- Verify both languages, source timing, source links, all slide bounds, PDF/PPTX and deployed HTML.
- Compare representative screenshots against the existing contest language, and verify the contest's rendering remains unchanged.

## Open questions

- [ ] Confirm personal team names and per-member assignments; use the documented two-maintainer collaboration model until confirmed.
- [ ] Confirm official external program display name; current notice says Builder Season 4 and the project roadmap says STP IV.
- [ ] A pinned reference lab's final platform/storage inventory and release evidence remain project work, not presentation assumptions.
