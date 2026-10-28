# Brand marks used by the decks

These SVG files are byte-identical copies from
[`cubrid-lab/brand`](https://github.com/cubrid-lab/brand) at revision
`4f77a91e1b810b5d17e784b4108e21683b52dfc5`, kept here because the decks run offline. The
permission is decision 6 in the brand repository's
[`BRAND_USAGE.md`](https://github.com/cubrid-lab/brand/blob/4f77a91e1b810b5d17e784b4108e21683b52dfc5/BRAND_USAGE.md)
(decks published by the `cubrid-lab` organization; recorded 2026-10-28).

| File | Source in the brand repository |
| --- | --- |
| `../favicon.svg` | `dist/organization/mark.svg` (organization emblem) |
| `lockup-horizontal.svg` | `dist/organization/lockup-horizontal.svg` |
| `cubrid-kubernetes-operator.svg` | `dist/icons/cubrid-kubernetes-operator.svg` (Operator deck only) |
| `pycubrid.svg` | `dist/icons/pycubrid.svg` (2026 OSS Developer Contest deck only) |
| `sqlalchemy-cubrid.svg` | `dist/icons/sqlalchemy-cubrid.svg` (2026 OSS Developer Contest deck only) |
| `cubrid-cookbook-python.svg` | `dist/icons/cubrid-cookbook-python.svg` (2026 OSS Developer Contest deck only) |
| `cubrid-mcp-server.svg` | `dist/icons/cubrid-mcp-server.svg` (2026 OSS Developer Contest deck only) |

The four Python product icons (`pycubrid.svg`, `sqlalchemy-cubrid.svg`,
`cubrid-cookbook-python.svg`, `cubrid-mcp-server.svg`) are pinned separately at brand revision
`4f77a91e1b810b5d17e784b4108e21683b52dfc5`, which includes the transparent Driver, ORM, Cookbook and MCP details (brand pull
requests 63 and 62). All four are marked `approved` in that revision's `registry/repositories.json`.
They are used only in the 2026 OSS Developer Contest deck.

Rules: show a mark as a whole image (scale, position or fade only; no recolouring, cropping,
reshaping, rasterizing or text inside the mark), use a role icon only for the repository it
represents, and keep the independence notice on the closing slide. Verify the copies with
`cd presentation/public && sha256sum -c brand/SHA256SUMS`. To update, copy the new bytes from a
newer brand revision, regenerate `SHA256SUMS` and change the revision above.
