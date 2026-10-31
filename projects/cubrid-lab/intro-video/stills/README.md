# Review stills of the main cut

Four frames of the introduction video's main cut, kept as the review record of
the real product footage. They were exported during production
([#53](https://github.com/cubrid-lab/showcase/pull/53), 2026-10-26) and are
1280×720 JPEGs. The video itself is not committed; it is attached to releases.

| File | Shot (storyboard id) | What it shows |
|---|---|---|
| `main-P3.jpg` | pycubrid, shot P3 | `python first_query.py` printing `(2,)`: the README's first query, recorded with vhs in a CUBRID 11.4 container |
| `main-S3.jpg` | sqlalchemy-cubrid, shot S3 | `python orm_demo.py` printing two ORM rows, recorded with vhs in a CUBRID 11.4 container |
| `main-C4b.jpg` | cubrid-mcp-server, second half of shot C4 | a read-only MCP client session (v0.6.0) refusing `DROP TABLE` |
| `main-K2b.jpg` | cubrid-cookbook-python, second half of shot K2 | the FastAPI quickstart answering 200 in Swagger UI, recorded with Playwright |

Shot ids are those of [`timelines/main.json`](../timelines/main.json) and
[VIDEO_DESIGN.md](../VIDEO_DESIGN.md).

## Regenerating

Render the same shots straight from the source (PNG, written to the ignored
`out/` folder):

```bash
node scripts/review-stills.mjs Main out/review 0.5 P3 S3 C4b K2b
```

Frames from a rendered file: `node scripts/extract-stills.mjs <video> <dir> [seconds ...]`.

## What does not belong here

Placeholder or draft stills (for example `npm run stills:demo`, which reads the
placeholder pipeline demo) go to `out/` and are not committed. The four
placeholder stills that used to be here were removed on 2026-10-31 (#105).
Replace a file here only when the main cut is re-rendered and its review frames
are approved.
