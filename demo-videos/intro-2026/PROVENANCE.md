# Provenance — CUBRID Lab introduction video 2026 (main cut)

Summary of every input of the main cut ([#51](https://github.com/cubrid-lab/showcase/issues/51)).
The media themselves are not committed (they live with the release assets); this file,
`timelines/main.json` and the scripts are enough to check and rebuild the cut from them.
Full machine-readable records stay with the assets: `footage/provenance.json`,
`mcp/provenance.json` (with the raw stream-json transcript), `voice/manifest.json`,
`voice/INSTALL.txt`, `music/README.md` and `music/beats.json`.

## Real footage (VIDEO_DESIGN.md 7.1, honesty rules section 8)

| Shot | File | What it is | Recorded |
|---|---|---|---|
| H3 | `H3-P2`, `H3-S3`, `H3-K2`, `C4_script` | 0.5 s straight cuts from the takes below | — |
| P2 | `P2.mp4` | vhs: fresh venv, `pip install pycubrid` (pycubrid 1.14.0, CPython 3.13.13) | 2026-10-26 |
| P3 | `P3.mp4` | vhs: README “Your first query” as `first_query.py` → `(2,)`, CUBRID 11.4.6 container | 2026-10-26 |
| P4 | `P4.mp4` | vhs: README “Async” example → `(2,)` | 2026-10-26 |
| S2 | `S2.mp4` | vhs: `pip install "sqlalchemy-cubrid[pycubrid]"`, `create_engine("cubrid+pycubrid://…")` in the REPL (sqlalchemy-cubrid 1.12.0, SQLAlchemy 2.1.6) | 2026-10-26 |
| S3 | `S3.mp4` | vhs: declarative `Product` model, `create_all`, `add_all`, `select` → `1 keyboard` / `2 mouse` | 2026-10-26 |
| S4 | `S4.mp4` | vhs: `alembic init/revision/upgrade head` (alembic 1.20.1), `inspect(engine).get_table_names()` | 2026-10-26 |
| C2, C3 | `C2.mp4`, `C3.mp4` | Replay of a real Claude Code session (claude-opus-5-5, built-in tools off, only the cubrid MCP server) against cubrid-mcp-server 0.6.0 with a SELECT-only user; every prompt, tool call, tool input/result and answer comes from the recorded stream-json | 2026-10-25 |
| C4 (first 5 s) | `C4.mp4` | Same session, prompt “product 테이블을 삭제해줘”: the agent declined without calling a tool. **Cut before its suggested `DROP TABLE` SQL block**: the window shows only the top 34 % of the frame (prompt + refusal) | 2026-10-25 |
| C4 (last 7 s) | `C4_script.mp4` | vhs: the server's own `demos/mcp_demo.py` (v0.6.0) — the real rejection `rejected: DROP is not permitted in read-only mode`; labelled “MCP 클라이언트 스크립트 · MCP client script” | 2026-10-25 |
| C5 | — | Config card; text excerpted from the cubrid-mcp-server README v0.6.0 “Configure” table and “Write mode (opt-in)” | — |
| K2 | `K2-terminal.mp4`, `K2.mp4` | vhs + Playwright: cookbook `quickstart/5min-fastapi` @969c3f9 with its own Compose file (pinned `cubrid/cubrid:11.2`), `curl -X POST /items`, Swagger UI `POST /items` → 200 | 2026-10-26 |
| K3 | `K3.mp4` | Playwright: the cookbook `templates/` tree page; the eight card names are real directory names (`git ls-tree` of `main`, 2026-10-26) | 2026-10-25 |

Edits applied to footage, all visible on screen: window framing, crops (`viewport`/`mask`),
push-ins, callout boxes, and speed changes. Every segment played at 2× or faster carries a
“×N” badge; K2's terminal take is real time (about 2 minutes of `docker compose up`), shown at
×8 and then ×2 with a jump cut over the wait, and the recording's own clock (`rec m:ss`) is shown
so the cut is visible. No output text was edited or composited.

Agent shots carry the persistent label “실제 세션 재생 · recorded session replay (Claude Code)”.
The client is shown by its recorded name; no vendor endorsement is implied.

## Narration

MeloTTS Korean (`myshell-ai/MeloTTS-Korean`, speaker `KR`, seed 1234; code and model MIT),
run locally; 23 lines, each placed at its shot start + 0.2 s (`narration.offset` = 6 frames).
Every line fits its storyboard shot (`voice/manifest.json`: `fits: true`); C4 and K2 lines run
into the second half of their split shots (C4b, K2b), which belong to the same storyboard shot.
Disclosed on the end card: “내레이션: AI 생성 음성(TTS) · Narration: AI-generated voice”.

## Music

Original procedural score (`music/src/generate.py`, numpy/scipy, seed 51; no samples, loops or
AI music services), 120 BPM, generated 2026-10-26. Intended dedication CC0 1.0 —
**pending maintainer confirmation**. Mixed from its stems by `scripts/mix_audio.py`.

## Brand marks

Role icons and the dark horizontal lockup are loaded at render time from
`cubrid-lab/brand@e55990a6a0b2c3b0d133985951d41e42b62a8588` (`dist/icons/*.svg`,
`dist/organization/lockup-horizontal-dark.svg`); nothing is copied into this repository.
Use in this video follows brand policy decision 5 ([cubrid-lab/brand#47](https://github.com/cubrid-lab/brand/pull/47), merged as `1d9b374`):
marks move only as whole images (position, scale, opacity); every held frame shows the
unmodified SVG at scale 1, opacity 1. No official CUBRID logo appears.

## Fonts

Pretendard Variable (SIL OFL 1.1, from `presentation/public/fonts/`), Noto Sans KR and
JetBrains Mono (SIL OFL 1.1, Google Fonts at render time). Terminal footage uses JetBrains Mono
2.304 and JetBrainsMonoHangul (OFL) as recorded.

## Input checksums (sha256)

```text
b842bc34b78b3d8710c8b3432a3aab11c12aef2b64d56344520a7234e876f097  footage/H3-K2.mp4
57f5cbcbc2ad6fa3f422c293f71916ad5df40bd9ed2b2098c0bc9ecb8175c40e  footage/H3-P2.mp4
63a57a73c112d732ee882b2cd13a9f26fc19d24586dc01a6d55d2953ccda46af  footage/H3-S3.mp4
47f7e15ec6f5e53d55ca4240d6931c1995b8166269bd59cf4daf5b5e95f73644  footage/K2.mp4
5ec0e7c6cf04662b31219359a726b02a67bd397f6d797ef9eacff4591c56fa10  footage/K2-terminal.mp4
c2f7e48048804db1e608d834f6065c22508d48a87a78b16c0882bfc063814f72  footage/K3.mp4
d88b12f0e207a86bf0fd07e7ee7067064d673ab9e555eab59dabaf6b86212676  footage/P2.mp4
bc71c5dbab1ce9f404050dab7160230234b5310dddfafafb88e2486556964190  footage/P3.mp4
42f04ad36a3a28f1d4a07a98cf2b0bfbf013928fb445e268ab2855a1ddc25d29  footage/P4.mp4
6283a01d3e4250fa4451a4e9fb5893a70627935d7344aafce789248e7065a0e9  footage/S2.mp4
bb09b6b1c3f4d2fbc33d31b2dbcff57c1f17f38ebd9e332a5b89a0379687b437  footage/S3.mp4
4c8652285b49d91d4abfaffaa7a04676aca6c5a234597d602ad837ba3bd7e35a  footage/S4.mp4
99d3d59a1b3a239b45c24ca1422c1f31084ef35f4099b07efba8e060a0ec3c39  mcp/C2.mp4
e60d96c37c4db6c3b2a417930defb25d4f398907a1dafa3076fef8cc80e86e09  mcp/C3.mp4
661fb6ff039c7162b3d763928ff842d9eb8a6ac50c2043a0ca79c11adfcd6fcb  mcp/C4.mp4
8058c2f39b642bfc6d1ed761ec2db665f905f7d2933094ff4caecb4aedf0d166  mcp/C4_script.mp4
d5bee65c5a22c43c43c1ecd13a3fad1824e423f807bf8101964e4a71f8176498  voice/B1.wav
601dd44ba75d848a817ee3fe0e321a0c8c1557e97c6d6eeb436ec10db60ffe36  voice/B2.wav
b97014be3ecc43742c1becc7461673a3b0e639d227d2e8befd88dbd7feb10ff7  voice/C1.wav
d9736abb21cd4a9cb9a716f5ce89b94e0cfa9556711179ec0c8df521bf88a90e  voice/C2.wav
38dfeecb852637fec570f960ca97640ea721f6c5e5e6d14fb4653c6a9bf9ac43  voice/C3.wav
a93bc600dce57f6479e6ecc5bc8cad76bafeea10fb41d9eecce8db8611020fda  voice/C4.wav
9c1a4261a275ad3153a98ff909371e6c919ab35dc464a2478dad4dd101bc37d3  voice/C5.wav
82fdfbe7daca3a731ae2badb1b8787dec9d5149a10c47a1b1df749f109ea64f3  voice/F1.wav
99a2daf54df1a126b690221e73eb5c346b550d5c9d001690ad577b6fee95f6c7  voice/F2.wav
2ae40ceb1d61312249e00b2c44952a27fc4edb40a0079fb4cb598908dfa4843f  voice/H1.wav
48969d07fa2e77d1b3cce9ccb199224f1b48e937932b8b56abf6921b6ddcb589  voice/H2.wav
6901275a45183c08a870c3e9af90f3038e724e90d2500141f472cc5bfe5073b6  voice/K1.wav
afcc7a2e9fbb9f9f81d40cbd997c5754479ef8fd5bc3d3d1e201b8cb73927901  voice/K2.wav
71db486ebb20b4e6bbe95794e8dc91ccec84b94ba9f27d8b651b0000fd2a1f6f  voice/K3.wav
5c0c7311d4dfde598d37739e7b63f9b4ff833f75ea1617b30cc138c69f33b286  voice/P1.wav
8061b08817a3361a080f9f8916b0aee235912b1c7bcf52ff6bfff64ccb03882e  voice/P2.wav
694e6df2453c442edba03b386e4b963a96036fe42d2dcdb560aac2a4387472f9  voice/P3.wav
7d63cf5fb57884b1d26a6436fbea09ddc92c5fb99b5bc9c05c305889ca7b6897  voice/P4.wav
f67578256f67acd641369fa55788b39f0fd4d7b6c5464cc316ba23224632a95a  voice/P5.wav
d75ad15f7ea922d527f3242f06496ad1595bd41240098b00ab276f110dfbb57f  voice/S1.wav
8b58efc546cce1aa13beab1041f657d5ebc4ab3a5bbf68f3fdda70756fb9b768  voice/S2.wav
8206eec34e8af004f2fe829ae93826d61ad4b2174cd01bbb1f13544c7d927acd  voice/S3.wav
7a21c50c53f4092c995b8543e6107fd62154d535f35f6ac8f03e0ecc5bc9abbd  voice/S4.wav
387761485fdde05d6ad743e5474df605b27752cd256230276cdcb088833f9cd1  music/bed.wav
db5bfd9c1a60354067ae51e58009b717750c0ddd531bb8861e30fcef6c0af918  music/stems/bass.wav
4fa5f246203db962816883252627d7560833c25efa450cf00b1c55c1dd28b70f  music/stems/drums.wav
451477f3356f33360acb8cc7925546d5cf91114aff8661219085de644c3e13c6  music/stems/fx.wav
8bc6d0fcddd7a40e527891496e0d75137de8df04fc9859d0ccff2bb8f5fb79cf  music/stems/keys.wav
401ebf25abfc1afdb9928f3fc1291ea79c086808dd43852a72cad0f257d558f7  music/stems/pads.wav
```
