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

Supertonic 3 (`Supertone/supertonic-3`, voice style `M5`, 16 steps, speed 1.05, `lang=ko`;
Python package `supertonic` 1.3.1, MIT; model weights OpenRAIL) run locally on CPU; 23 lines,
each placed at its shot start + 0.2 s (`narration.offset` = 6 frames), post-processed with the
same trim, pad and two-pass loudnorm (-16 LUFS / -1.5 dBTP) as before. Every line fits its
storyboard shot (`voice/manifest.json`: `fits: true`). Chosen on 2026-10-28 because MeloTTS read
“큐브리드” close to “퓨브리드”; in a faster-whisper large-v3 check on ten names-heavy lines
the M5 voice scored 0.91 against 0.81 for MeloTTS. Lines B2 and F2 were rewritten to name the
파이큐브리드팀 instead of CUBRID Lab. The MeloTTS take of 2026-10-27 is kept outside git as
`voice-melotts-2026-10-27/`.
Disclosed on the end card: “내레이션: AI 생성 음성(Supertonic TTS) · Narration: AI-generated voice (Supertonic)”.

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
f572359103624695fc9ce1c00ff5fa0783b8ef17d7a70b633e451961bc828ad3  voice/B1.wav
b9d6928eeaba3a5de010b21c9350ad4cf9638cc3a29f6264159e3b04ce1dc63d  voice/B2.wav
58f168f3d27dd7d9f90719ffabab964852c0b83ff17ef81d28a61300d142f28a  voice/C1.wav
7e3c5ffa2aacbf9e4c1cd8a18e4f30d9379baecc3b5de0f1d612ebc2f04e7687  voice/C2.wav
b71c4ef1321af15d1c8bc36de07cad3ec4baf362299318e3d939b54a8c5c0857  voice/C3.wav
629b80af7e719bc1e55a3e77892456ec40328680c9f753ba1e13bbd41cca8eb0  voice/C4.wav
5ed36795066ad9da88c343b24090976c88b8a7bf323905c2bf3f2609fce339f2  voice/C5.wav
edd70b3048cd146ba9440403905e4817e208c1444f442282b01a430fecc56c08  voice/F1.wav
3a0a7f381888c2c9f7c0621902e2924dc01214e8abe8221b2d09ff3bbee85fe8  voice/F2.wav
aff59aaf916df1abd7ef19609dd713692ffffabe6fe70e8b17412e52fff2e906  voice/H1.wav
81eb79242a3a3cf9491c0cf21629e3930d3a1b4530dbd7c53000005ffddb8cc0  voice/H2.wav
d9f4bb05a91fb1787bf01f58761c9d645eba8e5994481dabbd708a9632a1c833  voice/K1.wav
ec9d6e6f05531884d5838e8137ccaaf4479e8790870e704c00681e14a788e95a  voice/K2.wav
bfa5d3cda58e167301476e3a31234203f62daff40f9d5a7bf33c8d8110785355  voice/K3.wav
8cef1543a70244ad4891f9c97b73b7698a93a28b1027e259ee62082ff886f393  voice/P1.wav
686993a9ba1b013cd4a7671ccb775a44a055e72938373c0d41a33918a8d120f8  voice/P2.wav
f9b8b29c9c3c497dd73a76b721151d5c2a93f1dc92b4c452dec4222a51a5896e  voice/P3.wav
419a75ebd1a4db70c73f2fe11b3d485b776efb68fc2b11daf3c90f782231087a  voice/P4.wav
2d704b6762ac73b7b9a10e7aff2f74e71820f7e662dc4be20df64236c80d1272  voice/P5.wav
af843a5b88986a022d4095e59287995cd363b6bb9cc3933f378f1a4e7dbe61b6  voice/S1.wav
62ff95af805cc1c2ce3092f4a1ebee45ec13d263da45923850d6a5db999516e6  voice/S2.wav
99c6678dd57d4b3d4f5ea4233a8af4ac45d7202f35d8b53bbd7aff7d8fc149f7  voice/S3.wav
991ef311a91cb7544d8d0ca9b1b624cdeb26b3afbb6a87dc8916a81f1449c58f  voice/S4.wav
387761485fdde05d6ad743e5474df605b27752cd256230276cdcb088833f9cd1  music/bed.wav
db5bfd9c1a60354067ae51e58009b717750c0ddd531bb8861e30fcef6c0af918  music/stems/bass.wav
4fa5f246203db962816883252627d7560833c25efa450cf00b1c55c1dd28b70f  music/stems/drums.wav
451477f3356f33360acb8cc7925546d5cf91114aff8661219085de644c3e13c6  music/stems/fx.wav
8bc6d0fcddd7a40e527891496e0d75137de8df04fc9859d0ccff2bb8f5fb79cf  music/stems/keys.wav
401ebf25abfc1afdb9928f3fc1291ea79c086808dd43852a72cad0f257d558f7  music/stems/pads.wav
```
