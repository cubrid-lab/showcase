# CUBRID Lab Presentation Standard

## Purpose

Use one unobtrusive frame across future HTML, PDF, and PPTX presentations, while keeping the story and diagrams free to vary. The four corners do not need four pieces of content.

## Corner responsibilities

| Position | Default | Rules |
| --- | --- | --- |
| Top-left | Current section / chapter | Concise, human-readable. Do not use an unexplained internal code. |
| Top-right | Short deck / project identity | Fixed per deck; secondary to the main claim. Avoid repeating a long title. |
| Bottom-left | **Intentionally empty** | No persistent citation, logo, event, date, badge, navigation or other label. |
| Bottom-right | Automatically calculated page number | Current / total; never type per-slide counts into content. |

**Evidence is still required when making verifiable claims.** Put citations and links next to the claim, in a table footnote within the content area, in speaker notes, or in a linked source document. Do not relocate them to a persistent bottom-left footer.

## Slide variants

- **Cover:** prioritize title, team and project identification; any or all persistent corner metadata may be omitted.
- **Content:** standard three-corner frame; the content area is free for diagrams, comparisons, code and metrics.
- **Chapter divider:** a chapter number, short human-readable title and one line explaining the next idea, without an agenda repeated as bullets.
- **Q&A / evidence backup:** preserve source links near evidence and provide explicit return navigation; neither should occupy the reserved bottom-left corner.

## Chapter transitions

- Use `ChapterDivider.vue` rather than reimplementing markup in every slide.
- Insert at major narrative boundaries, not after each minor topic. Typically 3–4 chapters for a 10–12 minute talk.
- A divider must not introduce unsupported claims or displace a required topic.
- A divider can be visually advanced without extra spoken script; if the talk has a strict time cap, the rehearsal must include the extra slide changes. Do not claim that zero seconds of narration proves zero elapsed time.
- For bilingual decks, chapter count, sequence, numbers and relative positions must match.
- After insertion, update all hardcoded navigation, citations, index labels, speaker notes, page-count documentation and export validation. Preserve earlier release notes and their historical page counts.

## Visual geometry

- 16:9, consistent safe margins and stable header/page-number alignment.
- Header and page chrome must remain legible but clearly smaller than the content headline.
- Korean uses `word-break: keep-all` and wraps at natural phrase boundaries.
- Never shrink a dense slide until unreadable just to make the layout pass; split the content instead.
- Ensure that horizontal comparisons, code labels and long URLs do not collide with fixed corner metadata.
- Preserve keyboard navigation, links and static PDF/PPTX comprehension.

## Review checklist

1. Count slides and confirm navigation/return links resolve to the intended pages.
2. Confirm bottom-left remains unoccupied by persistent chrome.
3. Confirm each divider is a meaningful change in the story, not decoration.
4. Check speaker notes and planned talk duration, including transition clicks.
5. Check Korean and English parity where applicable.
6. Export and inspect HTML, PDF and PPTX. In particular, inspect all divider slides and the densest technical slides for overflow.
7. Keep old release assets and their counts labeled as historical; never describe a newly edited deck as a previously released artifact.

## Current implementations

- OSSDevCon: `presentation/decks/2026-ossdevcon/slides.md`, with auto page numbering in `presentation/slide-bottom.vue`.
- Builder Season 4: `presentation/components/OperatorSlide.vue` and bilingual decks in `presentation/decks/2026-builder-season4/01-validation/`.
- Shared chapter presentation: `presentation/components/ChapterDivider.vue`.
