# Screenshots used by the 2026 OSS Developer Contest deck

Screenshots of live pages, shown on the contest deck
([`decks/2026-ossdevcon/slides.md`](../../decks/2026-ossdevcon/slides.md)).
They are evidence of what the pages looked like on the capture date, not
generated output; there is no script that recreates them. The pycubrid,
sqlalchemy-cubrid and cubrid-mcp-server documentation captures of 2026-10-28
were removed on 2026-11-01 when the slides moved to one screenshot each; they
remain in the git history.

| File | Page | Captured | Size |
|---|---|---|---|
| `docs-cookbook.jpg` | <https://cubrid-lab.github.io/cubrid-cookbook-python/>, first screen at a 760×500 window so the text stays legible on the slide | 2026-11-01 | 1600×1053 |
| `mcp-session.jpg` | Last frame of the intro video's MCP shot C3: a replay of a recorded Claude Code session against cubrid-mcp-server 0.6.0 (question → `execute_query` → answer), cropped to the left 64 % and top 74 % | recorded 2026-10-25 (see `projects/cubrid-lab/intro-video/PROVENANCE.md`) | 1400×904 |
| `merged-prs.jpg` | pycubrid's merged pull requests on GitHub, each with its CI status | 2026-10-15 (`fa3d89f`) | 1600×804 |

To update one, capture the same page at the same size, replace the file, and
change its row here. Keep the old capture date in the commit message when a
slide's claim depends on it.
