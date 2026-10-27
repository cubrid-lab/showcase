# CUBRID Lab introduction video — design and storyboard (콘티)

- Status: design stage, for maintainer review. Production is tracked separately.
- Design issue: [#50](https://github.com/cubrid-lab/showcase/issues/50). Production follow-up: [#51](https://github.com/cubrid-lab/showcase/issues/51).
- Related: [#1](https://github.com/cubrid-lab/showcase/issues/1) is the backup recording of the 2026 OSS Developer Contest talk demo. This video is a separate, reusable project introduction for developers. It does not replace #1.
- Brand revision: [`cubrid-lab/brand@538bad3`](https://github.com/cubrid-lab/brand/tree/538bad3929bb661ee95774119cf3b9b4aebc7f15) (PR #51 merge; Python Yellow keyline aligned with the emblem).
- Style frames: [`style-frames/png/`](style-frames/png/) ([contact sheet](style-frames/png/contact-sheet.png)), sources in [`style-frames/src/`](style-frames/src/).
- Maintainer decisions: 2026-10-25, recorded in #50.

## 1. Concept

**One line:** *CUBRID를, Python으로.* Four open-source projects take a Python developer from `pip install` to an ORM, an AI agent and a running app on CUBRID.

The film works like a product launch, not a screen-recording walkthrough. Every product beat is a real recording, framed in a window mockup, zoomed onto the line that matters and set against kinetic Korean type. Cuts follow a 120 BPM music grid (one bar = 2 s). The brand's “shape = role, color = language” idea is the visual thread: one Python Yellow cube family, four role shapes.

### Audience

1. Python developers who have to work with an existing CUBRID database (public-sector and enterprise systems in Korea).
2. CUBRID users and DBAs evaluating Python, SQLAlchemy or AI-agent access.
3. Visitors of READMEs, the organization website and YouTube who need a two-minute answer to “what is CUBRID Lab?”

### Message hierarchy

1. **Python reaches CUBRID end to end** — driver → ORM → AI agent → runnable examples.
2. **Each layer removes one obstacle** — no C compiler (pycubrid), familiar SQLAlchemy code (sqlalchemy-cubrid), safe read-only AI access (cubrid-mcp-server), copy-and-run templates (cookbook).
3. **Open and verifiable** — MIT licensed, on GitHub and PyPI; what you see is real output.

Benefit lines used on screen: “설치 한 줄.”, “C 컴파일러 없이.”, “PEP 249, 그대로.”, “익숙한 ORM, 그대로.”, “AI가 읽고, 쓰기는 막는다.”, “복사해서, 바로 실행.”

### Out of scope

The TypeScript, Go and Rust drivers/ORMs, the Kubernetes Operator, cubrid-benchmark and this showcase are not featured. Performance numbers are not used (see [Honesty rules](#8-honesty-rules)).

## 2. Structure

Main cut: 16:9, 1920×1080, 30 fps, **2:56** (176 s; hard maximum 3:00). All shot boundaries sit on the 2-second bar grid.

| Segment | Time | Length | Purpose |
|---|---|---|---|
| Hook | 0:00–0:06 | 6 s | Promise in two words, flash of real footage |
| Brand | 0:06–0:20 | 14 s | Four icons assemble; CUBRID Lab, MIT |
| pycubrid | 0:20–0:58 | 38 s | Driver: install, first query, async/TLS/LOB |
| sqlalchemy-cubrid | 0:58–1:36 | 38 s | ORM: engine URL, models, Alembic/reflection |
| cubrid-mcp-server | 1:36–2:20 | 44 s | AI: agent reads; writes are refused by default |
| cubrid-cookbook-python | 2:20–2:42 | 22 s | Examples: FastAPI quickstart, template range |
| Finale + end card | 2:42–2:56 | 14 s | Recap, install commands, links, notices |

Optional derivative: **30-second vertical short** (1080×1920), see [section 4](#4-optional-30-second-short). It also yields the README GIF.

## 3. Storyboard — main cut

Columns: shot, time, visual and motion, on-screen copy, real-footage source, Korean narration (sized for TTS) and English caption. Narration timing is checked by [`narration_budget.py`](narration_budget.py) at 4.5 Korean syllables per second of shot (see [Narration](#61-narration)). “—” means music only.

<!-- storyboard:main -->
| Shot | Time | Visual & motion | On-screen copy | Source (real footage spec) | Narration (KO) | Caption (EN) |
|---|---|---|---|---|---|---|
| H1 | 0:00–0:02 | Black. Isometric 60°/120° grid lines draw outward from center on the downbeat. Grey type slams in, 4-frame overshoot. | CUBRID를, | Motion graphics | CUBRID를, | CUBRID, |
| H2 | 0:02–0:04 | Second line drops in; “Python” in Python Yellow, ochre underline wipes left→right. Style frame H2. | Python으로. | Motion graphics | Python으로. | in Python. |
| H3 | 0:04–0:06 | Four 0.5 s flash cuts on beats (not strobes; no full-frame white): install line, ORM rows, MCP rejection, Swagger UI. | — | Reused takes from P2, S3, C4, K2 | — | — |
| B1 | 0:06–0:12 | A neutral isometric tile settles on each beat; on it the unmodified role icon scales in (driver, ORM, MCP, cookbook). Labels type on. Style frame B1. | 드라이버 · ORM · AI · 예제 | Pinned brand icons (see [Brand marks](#52-brand-marks)) | 드라이버부터 ORM, AI, 그리고 예제까지. | From the driver to the ORM, AI and examples. |
| B2 | 0:12–0:20 | Icons slide up into a row; dark horizontal lockup fades in center; “MIT” chip pops. | Python 개발자를 위한 CUBRID 오픈소스 · MIT | Pinned lockup | CUBRID Lab의 Python 오픈소스, 모두 MIT 라이선스입니다. | Open-source Python tools from CUBRID Lab, all MIT-licensed. |
| P1 | 0:20–0:24 | Chapter card: pycubrid icon lands on its tile, name in 180 px type, role kicker. Style frame P1. | 01 · Driver · DB-API 2.0 / pycubrid | Pinned icon | 첫 번째, pycubrid. | One: pycubrid. |
| P2 | 0:24–0:32 | “설치 한 줄.” kinetic; terminal mockup pushes in; zoom callout on the `Successfully installed` line. | 설치 한 줄. | vhs: fresh venv, `pip install pycubrid` | 설치는 한 줄. C 확장도, 컴파일도 필요 없는 순수 Python 드라이버입니다. | One line to install: a pure-Python driver, no C extensions, no compiling. |
| P3 | 0:32–0:44 | Editor + terminal split. Code types in at 2× speed, run, callout zooms on `(2,)`. Style frame P3. | PEP 249, 그대로. | vhs: README “Your first query” as `first_query.py`, run against a local CUBRID 11.4 container | 연결하고, 커서를 열고, 실행합니다. 익숙한 DB-API 2.0 방식 그대로. | Connect, open a cursor, execute: the familiar DB-API 2.0 way. |
| P4 | 0:44–0:52 | Feature chips stack on beats; behind them the async snippet runs. | asyncio · TLS · LOB | vhs: README “Async” example (`pycubrid.aio.connect`) as a script, real output | asyncio 비동기 연결, TLS 암호화, LOB까지 지원합니다. | asyncio, TLS encryption and LOBs are supported too. |
| P5 | 0:52–0:58 | Button-out: `pip install pycubrid` on a yellow-keyline card; icon recedes. | C 컴파일러 없이. | Motion graphics | C 컴파일러 없이, Python이 도는 곳 어디서나. | No C compiler. Anywhere Python runs. |
| S1 | 0:58–1:02 | Chapter card: ORM icon, name, kicker. | 02 · ORM · SQLAlchemy 2.0–2.1 / sqlalchemy-cubrid | Pinned icon | 두 번째, sqlalchemy-cubrid. | Two: sqlalchemy-cubrid. |
| S2 | 1:02–1:10 | Terminal install, then the engine URL; callout isolates `cubrid+pycubrid://`. | 엔진 URL 하나. | vhs: `pip install "sqlalchemy-cubrid[pycubrid]"`, then `create_engine(...)` line | pycubrid와 함께 설치하고, 엔진 URL 하나로 연결합니다. | Install it with pycubrid and connect with one engine URL. |
| S3 | 1:10–1:24 | Model class types in; highlight sweeps `Mapped[int]`; terminal prints the rows. Style frame S3. | 익숙한 ORM, 그대로. | vhs: ORM script (declarative model, `create_all`, `add_all`, `select`), real output | SQLAlchemy 2.0 스타일 모델로 테이블을 만들고, 저장하고, 조회합니다. | Create tables, then save and query rows with SQLAlchemy 2.0-style models. |
| S4 | 1:24–1:32 | Three chips; behind them `alembic upgrade head` and `inspect(engine).get_table_names()` run. | Alembic · Reflection · Async | vhs: `pip install "sqlalchemy-cubrid[alembic]"`, `alembic upgrade head`, reflection one-liner | Alembic 마이그레이션, 스키마 리플렉션, 비동기 엔진까지. | Alembic migrations, schema reflection and an async engine. |
| S5 | 1:32–1:36 | Music hit; ORM icon flips to the next tile (whole-icon move only). | ORM도, CUBRID로. | Motion graphics | — | — |
| C1 | 1:36–1:40 | Chapter card: MCP icon, name, kicker. | 03 · AI · Model Context Protocol / cubrid-mcp-server | Pinned icon | 세 번째, cubrid-mcp-server. | Three: cubrid-mcp-server. |
| C2 | 1:40–1:50 | “AI가 읽고,” kinetic; agent window: prompt → tool call chip `all_table_names` → answer. | AI가 읽고, | Real agent run (see [Footage](#71-real-footage-specs)): prompt “이 데이터베이스에 어떤 테이블이 있어?” | AI 에이전트가 MCP로 CUBRID에 연결해, 스키마를 살펴봅니다. | An AI agent connects to CUBRID over MCP and explores the schema. |
| C3 | 1:50–2:00 | Second prompt; zoom on the generated `SELECT` inside the `execute_query` call, then the answer table. | 질문 → SELECT | Same run: “카테고리별 상품 수와 평균 가격을 알려줘” | 에이전트가 질문을 SQL로 바꾸면, 서버는 읽기 쿼리만 실행합니다. | The agent turns a question into SQL; the server runs read queries only. |
| C4 | 2:00–2:12 | “쓰기는 막는다.” underline wipe; the agent's `DROP TABLE` attempt returns the rejection; callout `CUBRID_MCP_WRITE=0`. Style frame C4. | AI가 읽고, 쓰기는 막는다. | Same run: “product 테이블을 삭제해줘” → `execute_query` rejected | 기본은 읽기 전용. 쓰기와 DDL 문은 거부되고, 쓰기 도구는 목록에 보이지도 않습니다. | Read-only by default. Writes and DDL are rejected, and the write tool isn't even listed. |
| C5 | 2:12–2:20 | Config card: env table rows animate; `execute_write` appears only when `CUBRID_MCP_WRITE=1` is set for a connection. | 쓰기는 연결별 opt-in | README “Write mode (opt-in)” table rendered as a card (text from README) | 쓰기는 운영자가 연결별로 직접 켤 때만 열립니다. | Writes open only when an operator enables them, per connection. |
| K1 | 2:20–2:24 | Chapter card: cookbook icon, name, kicker. | 04 · Examples / cubrid-cookbook-python | Pinned icon | 네 번째, cubrid-cookbook-python. | Four: cubrid-cookbook-python. |
| K2 | 2:24–2:34 | Terminal `docker compose up` (speed badge “×8”), then browser mockup: Swagger UI, `POST /items` response. | 복사해서, 바로 실행. | vhs + Playwright: `quickstart/5min-fastapi` README steps | Docker로 FastAPI 예제를 띄우고, 브라우저에서 바로 확인합니다. | Start the FastAPI example with Docker and check it in the browser. |
| K3 | 2:34–2:42 | Grid of eight template cards pops on beats (real directory names). Style frame K3. | 복사해서, 바로 실행. | Playwright: repository tree pages for `templates/`, `quickstart/`, `migration/` | Flask, Django, 대시보드, AI 에이전트, Java 마이그레이션 가이드까지. | Flask, Django, dashboards, AI agents and a Java migration guide. |
| F1 | 2:42–2:48 | Four icons return in a row, each with its benefit line; grid pulls back. | 설치 한 줄 · 익숙한 ORM · 읽기 전용 AI · 바로 실행 | Motion graphics | Python으로 CUBRID를, 처음부터 끝까지. | CUBRID from Python, end to end. |
| F2 | 2:48–2:56 | End card holds 8 s: lockup, install commands, URL, MIT, AI-voice and independence notices. Style frame F2. | see [End card](#53-end-card) | Pinned lockup | 지금 GitHub cubrid-lab에서 시작하세요. | Get started at github.com/cubrid-lab. |
<!-- /storyboard:main -->

## 4. Optional 30-second short

Vertical 1080×1920 (a 1080×1080 square crop works from the same layout). Built from main-cut takes; captions are burned in because social players often autoplay muted. Narration is optional; if used, reuse the main-cut lines below.

| Shot | Time | Content | Copy | Narration (optional) |
|---|---|---|---|---|
| V1 | 0:00–0:03 | Hook type, four role words. Style frame V1. | CUBRID를, Python으로. | H1 + H2 lines |
| V2 | 0:03–0:10 | P2 + P3 takes, stacked vertically | 설치 한 줄. PEP 249, 그대로. | 설치는 한 줄. |
| V3 | 0:10–0:17 | S3 take | 익숙한 ORM, 그대로. | — |
| V4 | 0:17–0:25 | C4 take. Style frame V4. | AI가 읽고, 쓰기는 막는다. | 기본은 읽기 전용입니다. |
| V5 | 0:25–0:30 | End card, vertical | github.com/cubrid-lab · MIT | F2 line |

**README GIF:** V2–V4 product footage without narration, 960 px wide, 12 fps, at most 8 s, `ffmpeg` palettegen/paletteuse, target at most 5 MB, alt text describing the real recording. Each repository README already has its own demo GIF; this one is for the showcase/organization pages.

## 5. Visual design system

### 5.1 Tokens

All colors come from [`tokens/colors.json`](https://github.com/cubrid-lab/brand/blob/538bad3929bb661ee95774119cf3b9b4aebc7f15/tokens/colors.json) and [`tokens/organization.json`](https://github.com/cubrid-lab/brand/blob/538bad3929bb661ee95774119cf3b9b4aebc7f15/tokens/organization.json) at the pinned revision. They are CUBRID Lab project tokens, not official CUBRID colors.

| Role | Value | Token |
|---|---|---|
| Canvas | `#0D1117` | `wordmarks.variants.dark.background` (the dark lockup's approved background) |
| Primary text | `#F0F6FC` | `wordmarks.variants.dark.title` |
| Secondary text | `#A8C1E8` | `wordmarks.variants.dark.tagline` |
| Accent / language | `#FFD43B` Python Yellow | `languages.python` |
| Keyline, underline, chip border | `#8C7520` ochre | `treatments.python.keyline` |
| Ink on yellow | `#40350F` | `treatments.python.mark` |
| Grid lines, neutral | `#6B7280` | `languages.neutral` |

The emblem's three face colors (`#006BDA`, `#00A36F`, `#E60039`) appear only inside the unmodified emblem/lockup. Red is not used as a UI color; the read-only rejection is shown with the yellow highlight and the word “rejected”, so meaning never depends on color.

**Typography** (open licenses, no remote dependency in the final render): Pretendard Variable (SIL OFL 1.1, already bundled in [`presentation/public/fonts/`](../../presentation/public/fonts/)) for Korean and Latin display/body; JetBrains Mono (SIL OFL 1.1) for code and terminals, bundled into the render project in production. Display 160–200 px / weight 900, headings 68–104 px / 800, body 34 px / 500, code 25–29 px. Korean lines use `word-break: keep-all`.

**Layout:** title-safe margins 96 px × 54 px; nothing essential in the bottom 150 px of the main cut (caption zone); window mockups with 18 px radius and a 52 px title bar; one idea per frame.

### 5.2 Brand marks

Assets at `cubrid-lab/brand@538bad3`:

| Use | Pinned file |
|---|---|
| Driver | [`dist/icons/pycubrid.svg`](https://raw.githubusercontent.com/cubrid-lab/brand/538bad3929bb661ee95774119cf3b9b4aebc7f15/dist/icons/pycubrid.svg) (complete cube, horizontal grooves) |
| ORM | [`dist/icons/sqlalchemy-cubrid.svg`](https://raw.githubusercontent.com/cubrid-lab/brand/538bad3929bb661ee95774119cf3b9b4aebc7f15/dist/icons/sqlalchemy-cubrid.svg) (complete cube, side-to-side grooves) |
| MCP | [`dist/icons/cubrid-mcp-server.svg`](https://raw.githubusercontent.com/cubrid-lab/brand/538bad3929bb661ee95774119cf3b9b4aebc7f15/dist/icons/cubrid-mcp-server.svg) (router hub) |
| Cookbook | [`dist/icons/cubrid-cookbook-python.svg`](https://raw.githubusercontent.com/cubrid-lab/brand/538bad3929bb661ee95774119cf3b9b4aebc7f15/dist/icons/cubrid-cookbook-python.svg) (pages) |
| Lockup, dark canvas | [`dist/organization/lockup-horizontal-dark.svg`](https://raw.githubusercontent.com/cubrid-lab/brand/538bad3929bb661ee95774119cf3b9b4aebc7f15/dist/organization/lockup-horizontal-dark.svg) (stacked variant for the vertical short) |

The production video reads these by commit-pinned URL through one constant, `BRAND_REVISION` in [`src/brand.ts`](src/brand.ts); moving to a later approved revision is a one-line change and a re-render. The design-stage style frames keep their reviewed pin, `BRAND_COMMIT` (`38b4646`) in [`frames.html`](style-frames/src/frames.html).

**Policy gate (design stage, resolved).** Resolved by decision 5 in [`BRAND_USAGE.md`](https://github.com/cubrid-lab/brand/blob/538bad3929bb661ee95774119cf3b9b4aebc7f15/BRAND_USAGE.md) (cubrid-lab/brand#47, `1d9b374`), which permits CUBRID Lab promotional videos to render, animate and combine approved marks; the production render follows it. The text below is the design-stage record. The brand policy at the design-stage revision `38b4646` ([`BRAND_USAGE.md`](https://github.com/cubrid-lab/brand/blob/38b46469a1e18c7e9f7270f0b3d286ab45c3b376/BRAND_USAGE.md#repository-icon-use), [`ORGANIZATION_MARK_USAGE.md`](https://github.com/cubrid-lab/brand/blob/38b46469a1e18c7e9f7270f0b3d286ab45c3b376/docs/ORGANIZATION_MARK_USAGE.md#wordmark-lockups)) permits each repository's icon only in its own README/docs by pinned URL and lists *rasterizing*, *combining with text*, *modifying* and *using another repository's icon* as not permitted. A video necessarily rasterizes, and this one shows four repositories' icons and the lockup on a showcase/YouTube surface. Therefore:

- The committed style-frame PNGs are rendered with labelled placeholders (`marks=slot`). No brand SVG and no rasterized brand mark is committed here.
- A full-fidelity set rendered with the pinned SVGs (`node render.mjs --marks=pinned --out=<dir>`) is for local review only.
- Production needs a decision recorded in `cubrid-lab/brand` that allows, for this video and its derivatives (YouTube, MP4/WebM, GIF, thumbnail): (1) rasterized display of the unmodified pinned icons and lockup; (2) the four role icons together beside their names; (3) whole-icon transforms only (position, scale, opacity). Once recorded, re-render the PNGs with `--marks=pinned`.

**Cube-grammar motion motif.** The “assembly” is drawn with generic isometric primitives (60°/120° grid lines and a neutral rhombus tile). Each icon then appears whole on its tile. Animating an icon's own faces or grooves would modify it. If the maintainer wants part-level assembly, generate an approved animated asset in the brand repository from its geometry tokens, rather than rebuilding the icon in the video project. (Production: decision 5 allows intermediate frames to show partial cube faces as long as every held frame matches the approved SVG, so the final cut assembles generic faces from the geometry token and then shows the pinned SVG unmodified.)

Never: an official CUBRID logo or wordmark anywhere in the film, a role icon used as the organization mark, or the lockup below its 240 px minimum width (the end card uses it at 900 px).

### 5.3 End card

Lockup (dark); install commands verified in the READMEs: `pip install pycubrid`, `pip install "sqlalchemy-cubrid[pycubrid]"`, `uvx cubrid-mcp-server`; `github.com/cubrid-lab · MIT License`; then, at 24 px or larger:

- 내레이션: AI 생성 음성(TTS) · Narration: AI-generated voice
- CUBRID Lab은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 프로젝트입니다. CUBRID는 해당 권리자의 상표입니다.
- CUBRID Lab is independently maintained and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project.

The independence wording follows [`BRAND_USAGE.md`](https://github.com/cubrid-lab/brand/blob/538bad3929bb661ee95774119cf3b9b4aebc7f15/BRAND_USAGE.md#independence). The same notices go in the YouTube description.

### 5.4 Motion principles

- **Music-led:** 120 BPM; cuts, chip pops and type slams land on beats; chapter cards land on bar 1 of a phrase.
- **Type first, then proof:** each benefit line appears 0.3–0.5 s before the footage that proves it.
- **Real footage is framed, never repainted:** window mockups, push-ins up to 2.5×, callout boxes and highlight sweeps over the recording; typing may be sped up (marked “×N” when more than 2×).
- **Easing:** fast-out/slow-in (cubic-bezier(0.2, 0.8, 0.2, 1)), 8–12 frames for UI, 4-frame overshoot only on hook type.
- **Restraint:** one moving idea at a time; no camera shake, glitch or strobe; `prefers-reduced-motion` is irrelevant for video, so the cut itself stays calm enough to read.

## 6. Audio

### 6.1 Narration

Korean narration by a TTS voice, disclosed as AI-generated (on screen at the end card, in the YouTube description, and by ticking YouTube's altered/synthetic content setting if YouTube Studio asks; a non-cloned synthetic narrator is likely not required to be labelled there, but we disclose anyway — not verified against current YouTube policy).

**Sizing.** Natural Korean read speech runs around 5–6 syllables per second. The script is planned at **4.5 syllables per second of shot length**, which leaves 10–25 % of each shot for music hits and breaths and lets the voice run at a confident, unhurried rate. [`narration_budget.py`](narration_budget.py) applies the pronunciation lexicon (also the TTS lexicon: `pycubrid` → 파이큐브리드, `MCP` → 엠씨피, `DB-API 2.0` → 디비 에이피아이 이 점 영, …), counts syllables per shot and fails if a line is over budget or the cut leaves 2:45–3:00. At the script checkpoint the rate is calibrated against the synthesized audio (measured duration per line, adjusted with the engine's rate control).

```text
$ python3 demo-videos/intro-2026/narration_budget.py
```

**Captions.** Korean track primary, English track secondary (both in the storyboard). Korean: at most 2 lines, about 18 characters per line, at least 1 s per cue, breaks at phrase boundaries. English: at most 2 lines, 42 characters per line. Delivered as `.srt` and `.vtt`; the main cut does not burn captions in (YouTube CC, `<track>` on the website); the short burns Korean in.

### 6.2 TTS engine

**Recommendation: MeloTTS Korean, run locally.** See the evaluation below; the decision is the maintainer's at the script checkpoint.

| Engine | Korean voice | License / YouTube terms | Cost | Reproducibility | Assessment |
|---|---|---|---|---|---|
| **MeloTTS-Korean** (myshell-ai) | One Korean speaker (`KR`), speed parameter | Code MIT ([LICENSE](https://github.com/myshell-ai/MeloTTS/blob/main/LICENSE)); model card MIT, “free for both commercial and non-commercial use” ([model card](https://huggingface.co/myshell-ai/MeloTTS-Korean)) | Free, CPU | Pin repo commit `209145371cff8fc3bd60d7be902ea69cbdb7965a` and model revision; deterministic re-synthesis not verified (see trial) | **Recommended**: permissive, no API key, runs here. Single voice only. |
| Azure AI Speech | Many ko-KR neural/HD voices (e.g. SunHi, InJoon); SSML rate/pitch/breaks | Commercial use expected; output-rights wording not verified; disclosure guidance is advisory | Free tier 0.5 M chars/month | Cloud voice can change or retire | **Fallback 1** if MeloTTS quality is rejected |
| Google Cloud TTS | ko-KR Chirp 3 HD, Neural2, WaveNet; `speaking_rate` | Terms not verified | Pricing not verified | Cloud voice can change | Fallback 2 |
| OpenAI TTS | Korean supported, English-optimized voices | Usage policy requires AI-voice disclosure | — | `gpt-4o-mini-tts`, `tts-1`, `tts-1-hd` shut down 2027-01-06 | Not recommended |
| ElevenLabs / Typecast / Supertone Play | Strong Korean voices | Free plans: non-commercial and/or credit required; paid plans commercial | Subscription | Hosted | Not recommended for a reproducible open pipeline |
| NAVER CLOVA Voice | Korean | API terms: live calls only; saving/editing files not allowed | — | — | Not usable for a rendered video |
| Supertonic 3 | Korean | Weights OpenRAIL-M (use restrictions); repository archived | Free | Weights available | Not recommended |
| Coqui XTTS-v2 / Kokoro / edge-tts | — | CPML (commercial terms unverified) / no Korean / not a licensed API | — | — | Excluded |

Sources: MeloTTS repository and model card above; vendor pages for [Azure voices](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts), [Azure disclosure guidance](https://learn.microsoft.com/en-us/azure/ai-foundry/responsible-ai/speech-service/text-to-speech/concepts-disclosure-guidelines), [Google Chirp 3 HD](https://docs.cloud.google.com/text-to-speech/docs/chirp3-hd), [OpenAI TTS](https://developers.openai.com/api/docs/guides/text-to-speech), [ElevenLabs publishing](https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform.md), [CLOVA Voice policy](https://guide.ncloud-docs.com/docs/en/clovavoice-policy.md), [Supertonic](https://github.com/supertone-inc/supertonic), [Kokoro voices](https://huggingface.co/hexgrad/Kokoro-82M/blob/main/VOICES.md), checked 2026-10-25. Korean naturalness across vendors was not independently assessed; decide by a blind listen of the same three lines.



#### 6.2.1 MeloTTS trial

Not yet run: a local MeloTTS install on the design machine is in progress. Until a trial is recorded here, Korean quality and run-to-run determinism are **not verified**.

### 6.3 Music

**Recommendation: procedurally generated score, owned by the project.** A small script renders a 120 BPM bed (pulse, bass, soft pad, hits on chapter cards, a lift at C4 and a resolve at F2) to WAV with an MIT-licensed synthesis library in headless Chromium (Tone.js `Tone.Offline`) or plain Python/NumPy. Provenance is the script and its seed, committed with the production project; the maintainers dedicate the output under CC0. Nothing can be Content-ID-claimed and the same file is safe on YouTube, the website and in GIF-adjacent MP4s.

Fallback, if the generated score is not good enough: a **YouTube Audio Library** track under the standard (no-attribution) license — YouTube states those tracks are not claimed by Content ID ([help](https://support.google.com/youtube/answer/3376882)) — but its terms for use outside YouTube (website MP4/WebM) are not stated, so use it only on the YouTube upload. Avoid Pixabay (Content ID claims reported) and any NC/ND Creative Commons track. CC BY tracks (e.g. Kevin MacLeod, [incompetech](https://incompetech.com/music/royalty-free/faq.html)) need the credit in the description and end card.

Record per track in `music/PROVENANCE.md`: title, artist or generator script + seed, source URL, license name and URL, download/generation date, track ID/ISRC, where credit is placed, Content ID status at upload, and a saved copy of the license page.

**Mix:** narration −16 LUFS integrated for the master (YouTube normalizes to about −14), music ducked 8–10 dB under narration, true peak ≤ −1 dBTP.

## 7. Production pipeline

**Recommendation: Remotion** (React/TypeScript compositions rendered by headless Chromium to MP4/WebM), pinned to an exact 4.x version.

- The style frames are already HTML/CSS; they port directly into Remotion components with the same tokens and fonts.
- It reuses the repository's Node 24 toolchain and Chromium, renders from the command line (`npx remotion render`) and keeps every timing in code, so the storyboard table becomes a typed shot list and caption files are generated from the same data.
- `<OffthreadVideo>` places the vhs/Playwright recordings; `<Audio>` places narration and music on the bar grid.
- **License:** Remotion is source-available, not OSI open source. Its free license covers individuals, for-profit organizations with up to 3 employees and non-profits ([LICENSE.md](https://github.com/remotion-dev/remotion/blob/main/LICENSE.md)); the maintainer confirms CUBRID Lab qualifies before production. The license does not affect the rendered video.

Alternatives considered: **Motion Canvas** (MIT, strong code animation, but the last release is a 2025 alpha and HTML/CSS cannot be reused); **ffmpeg + Playwright-captured HTML frames** (fully OSS but motion, easing and audio sync become hand-written plumbing). Choose Motion Canvas only if an OSI license is a hard requirement.

**Recording tools:** [vhs](https://github.com/charmbracelet/vhs) tapes for every terminal shot (committed `.tape` files, fixed theme/font/size); Playwright scripts for browser shots (fixed viewport 1600×900, device scale 2); a real MCP agent session recorded in a terminal (vhs or screen capture) with its raw transcript kept.

### 7.1 Real-footage specs

Every take except K2 runs against a fresh local `cubrid/cubrid:11.4` container on the recording machine, with the published PyPI packages (versions recorded in `footage/MANIFEST.md`, not in the script or on screen). K2 records the cookbook quickstart unmodified, so it uses the CUBRID image its `docker-compose.yml` pins (`cubrid/cubrid:11.2` on 2026-10-25, within the cookbook's 11.2/11.4 support matrix); record that image and digest in the manifest instead of overriding it.

| Shot | Command / page / prompt |
|---|---|
| P2 | `python -m venv .venv && . .venv/bin/activate && pip install pycubrid` |
| P3 | README [“Your first query”](https://github.com/cubrid-lab/pycubrid#your-first-query) saved as `first_query.py`; `python first_query.py` → `(2,)` |
| P4 | README [“Async”](https://github.com/cubrid-lab/pycubrid#async) example as a script, run once |
| S2 | `pip install "sqlalchemy-cubrid[pycubrid]"`, then an editor view of `create_engine("cubrid+pycubrid://dba@localhost:33000/testdb")` |
| S3 | ORM script: declarative `Product` model, `create_all`, `add_all`, `select` (the style frame S3 code, run 2026-10-25, printed `1 keyboard` / `2 mouse`) |
| S4 | `pip install "sqlalchemy-cubrid[alembic]"`, `alembic init`, one revision, `alembic upgrade head`; `inspect(engine).get_table_names()` |
| C2–C4 | Seed a small `product` table (name, category, price). Run an MCP client with `uvx cubrid-mcp-server` and `CUBRID_HOST/PORT/USER/PASSWORD/DATABASE` set, write mode unset, preferably a dedicated SELECT-only user per [SECURITY.md](https://github.com/cubrid-lab/cubrid-mcp-server/blob/main/SECURITY.md). Prompts: “이 데이터베이스에 어떤 테이블이 있어?”, “카테고리별 상품 수와 평균 가격을 알려줘”, “product 테이블을 삭제해줘”. Keep the tool-call view visible. If the agent declines to call the tool for the delete prompt, record that honestly and use the scripted client [`demos/mcp_demo.py`](https://github.com/cubrid-lab/cubrid-mcp-server/blob/main/demos/mcp_demo.py) for C4, labelled “MCP client script” on screen. Show the client's name as recorded; do not imply endorsement by its vendor. |
| C5 | Card built from the README [configuration table](https://github.com/cubrid-lab/cubrid-mcp-server#configure) and “Write mode (opt-in)” text |
| K2 | Cookbook [`quickstart/5min-fastapi`](https://github.com/cubrid-lab/cubrid-cookbook-python/tree/main/quickstart/5min-fastapi): `docker compose up -d --build --wait` with the quickstart's own Compose file (its pinned CUBRID image, see above), the README `curl -X POST /items`, then Playwright on `http://localhost:8000/docs` |
| K3 | Playwright on the repository's `templates/`, `quickstart/` and `migration/` tree pages |

## 8. Honesty rules

1. Every product shot is a real recording: terminal via vhs, browser via Playwright, MCP via a real agent run. No mocked output, no edited result text, no composited numbers. Speed-ups are labelled.
2. The style frames use only real text: code from the READMEs or the script run on 2026-10-25, and output from that run (pycubrid `(2,)`, ORM rows, MCP stdio session). Each panel names its source.
3. No package version numbers in narration, on-screen copy or the end card; versions appear only where real footage shows them.
4. **No performance numbers.** If one is ever added, it may come only from [`contests/2026-ossdevcon/metrics/benchmark-2026-10-25/`](../../contests/2026-ossdevcon/metrics/benchmark-2026-10-25/README.md) with its shared-host caveats on screen; the recommendation is to use none.
5. No claims beyond the sources in [section 9](#9-fact-sources). Django appears as a template name, not as “Django ORM support” (the template is a SQLAlchemy bridge).
6. The independence notice and the AI-voice disclosure are on the end card and in the description.

## 9. Fact sources

Checked on 2026-10-25 against `main` of each repository and PyPI.

| Claim in the script | Source |
|---|---|
| pycubrid is a pure-Python DB-API 2.0 (PEP 249) driver, no C extensions, no compilation | [pycubrid README](https://github.com/cubrid-lab/pycubrid#readme) title line and Features |
| `pip install pycubrid`; first query `SELECT 1 + 1` → `(2,)` | pycubrid README “Installation”, “Your first query”; reproduced 2026-10-25 against CUBRID 11.4.6 |
| asyncio (`pycubrid.aio`), TLS (`ssl=True`), LOB (CLOB/BLOB) | pycubrid README Features and FAQ |
| “Anywhere Python runs” | pycubrid README Features: “works everywhere Python runs” |
| sqlalchemy-cubrid is a SQLAlchemy 2.0–2.1 dialect with Alembic support and schema reflection | [sqlalchemy-cubrid README](https://github.com/cubrid-lab/sqlalchemy-cubrid#readme) title, “Why”, Support Status |
| `pip install "sqlalchemy-cubrid[pycubrid]"`, URL `cubrid+pycubrid://`, async `cubrid+aiopycubrid://` | sqlalchemy-cubrid README install section and driver options; ORM script reproduced 2026-10-25 |
| cubrid-mcp-server is read-only by default; whitelist SELECT/SHOW/DESC/DESCRIBE/WITH; `execute_write` registered only with `CUBRID_MCP_WRITE=1`, per connection | [cubrid-mcp-server README](https://github.com/cubrid-lab/cubrid-mcp-server#readme) Features, configuration table, “Write mode (opt-in)”; rejection reproduced 2026-10-25 |
| `uvx cubrid-mcp-server` | cubrid-mcp-server README install section |
| Cookbook FastAPI quickstart with Docker; Flask, Django, Celery, Pandas ETL, Streamlit dashboard, AI agent templates; Java → Python migration | [cubrid-cookbook-python README](https://github.com/cubrid-lab/cubrid-cookbook-python#readme) and its directory tree |
| All four are MIT licensed | Each repository's `LICENSE`; PyPI metadata (`license_expression: MIT`) for the three packages |
| CUBRID Lab independence wording | [brand `BRAND_USAGE.md`](https://github.com/cubrid-lab/brand/blob/538bad3929bb661ee95774119cf3b9b4aebc7f15/BRAND_USAGE.md#independence) |

## 10. Accessibility

- Korean and English caption tracks for every spoken line; on-screen copy repeats the key benefit so the film works muted.
- Text contrast at least 4.5:1 on `#0D1117` (primary text, Python Yellow and the secondary blue all exceed it); code at 25 px or larger at 1080p.
- No flashing: H3's four cuts are 0.5 s apart, with no full-frame luminance flash, below the three-flashes-per-second threshold (WCAG 2.3.1).
- Meaning never by color alone (“rejected” is written, not only highlighted).
- The end-card legal lines hold for 8 s at 24 px or larger.
- A text transcript (Korean, English) is published with the video description.

## 11. Deliverables and naming

Directory for production sources: `demo-videos/intro-2026/` (Remotion project, `.tape` files, Playwright scripts, music generator). Large media are not committed; they are attached to a GitHub Release `intro-video-2026-<yyyy-mm-dd>` (the pattern the presentation exports use) and uploaded to YouTube.

| File | Spec |
|---|---|
| `cubrid-lab-intro-2026_main_1080p.mp4` | H.264 High, 1920×1080, 30 fps, AAC 48 kHz, master for YouTube and backup |
| `cubrid-lab-intro-2026_main_1080p.webm` | VP9 + Opus, for the website `<video>` |
| `cubrid-lab-intro-2026_main.ko.srt` / `.ko.vtt` | Korean captions |
| `cubrid-lab-intro-2026_main.en.srt` / `.en.vtt` | English captions |
| `cubrid-lab-intro-2026_short_1080x1920.mp4` | Optional short, Korean captions burned in |
| `cubrid-lab-intro-2026_readme.gif` | README GIF per section 4 |
| `cubrid-lab-intro-2026_thumbnail.png` | 1280×720, built from style frame H2 with the lockup |
| `transcript.ko.md` / `transcript.en.md` | Text transcript |

YouTube: title “CUBRID Lab — CUBRID를, Python으로 (pycubrid · sqlalchemy-cubrid · cubrid-mcp-server · cookbook)”, description with links, install commands, AI-voice disclosure, music credit if any, independence notice; KO and EN caption tracks uploaded, not auto-generated.

## 12. Review checkpoints

1. **Script** — this storyboard: narration, captions, claims and sources. Plus the TTS decision (listen to the trial lines).
2. **Style frames** — the [contact sheet](style-frames/png/contact-sheet.png) and the brand-mark decision of section 5.2.
3. **Animatic** — Remotion render with placeholder footage, final narration and the music bed, timed to the grid.
4. **Final** — real footage, mix, captions; checked against the honesty rules and the fact table before upload.

## 13. Open decisions for the maintainer

1. Brand-mark use in video (section 5.2) — record the decision in `cubrid-lab/brand`.
2. TTS engine: MeloTTS Korean (local, MIT) or a cloud voice if its quality is not acceptable.
3. Music: generated score (recommended) or a YouTube Audio Library track for the YouTube upload only.
4. Remotion free-license eligibility for CUBRID Lab.
5. Which MCP client is shown in C2–C4.

## Production follow-up

Tracked in [#51](https://github.com/cubrid-lab/showcase/issues/51): blocking decisions, footage, narration and captions, music, motion graphics and edit, review, export and upload.

## Reproducing the style frames

```bash
cd demo-videos/intro-2026/style-frames/src
npm install --no-save --package-lock=false playwright-chromium@1.64.1
npx playwright install chromium
node render.mjs                     # placeholders -> ../png/ (committed)
node render.mjs --marks=pinned --out=/tmp/intro-frames-pinned   # local review only
```
