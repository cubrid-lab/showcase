#!/usr/bin/env python3
"""Builds timelines/demo-cut.json (the demo-focused cut) and its captions from the shot list below.

    python3 scripts/build_demo_timeline.py [voice-demo/manifest.json]

Narration text: scripts/demo_cut_lines.json (synthesize with scripts/synth_demo_voice.py).
Narration lengths come from the voice manifest (default: $INTRO_ASSETS/voice-demo/manifest.json);
every shot is at least as long as its narration needs (0.2 s offset + duration <= shot length - 0.3 s).
Footage times are source seconds; camera keys and callouts are given in source seconds too and
converted to the window's local frames. Footage plays at 1x except the long waits marked below.
Edit here, not in the JSON.
"""
import json, math, os, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = os.environ.get('INTRO_ASSETS', '/data/video-intro-assets')
MANIFEST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ASSETS, 'voice-demo', 'manifest.json')
man = json.load(open(MANIFEST))
dur = {s['shot']: s['duration_s'] for s in man['shots']}
lines = {l['shot']: l for l in json.load(open(ROOT / 'scripts' / 'demo_cut_lines.json'))}
FPS = 30
WINDOW_AT = 8      # frames before the footage window appears
NARR_AT = 6        # narration offset (0.2 s)
TAIL = 30          # frames the last picture stays after the footage ends

REPLAY = '실제 세션 재생 · recorded session replay (Claude Code)'
SCRIPT = 'MCP 클라이언트 스크립트 · MCP client script'
TERM_SRC = 'real recording · vhs · CUBRID 11.4 container · 2026-10-26'
COOK_SRC = 'real recording · cookbook quickstart/5min-fastapi @969c3f9 · its pinned cubrid/cubrid:11.2 · 2026-10-26'

shots = []
cursor = 0


def place(segs):
    """(start frame, frame count) of each segment, back to back."""
    out, t = [], 0
    for s in segs:
        n = s['hold'] if 'hold' in s else round((s['to'] - s['from']) * FPS / s.get('rate', 1))
        out.append((t, n))
        t += n
    return out


def lf(segs, t):
    """Local frame at which source time t is shown (first segment containing it)."""
    for s, (st, n) in zip(segs, place(segs)):
        if 'to' in s and s['from'] - 1e-6 <= t <= s['to'] + 1e-6:
            return round(st + (t - s['from']) * FPS / s.get('rate', 1))
    raise ValueError(f'time {t} not in any segment')


def footage(src, segs, need, cams=None, calls=None, viewport=None, mask=None):
    """Footage props. segs: [{from,to,rate?}], cams: one (zoom, x, y) or (start, end) pair of them per
    segment, calls: [(t0, t1, x, y, w, h, label)] in source seconds. `need` = frames the shot must last."""
    base = sum(n for _, n in place(segs))
    total = max(base + TAIL, need - WINDOW_AT)
    last = segs[-1]['to']
    segs = segs + [{'from': round(last - 0.05, 3), 'hold': total - base}]
    f = {'src': src, 'segments': segs}
    if viewport: f['viewport'] = viewport
    if mask: f['mask'] = mask
    keys = []
    for i, ((st, n), c) in enumerate(zip(place(segs[:-1]), cams or [])):
        a, b = (c, c) if not isinstance(c[0], tuple) else c
        keys.append({'at': st, 'zoom': a[0], 'x': a[1], 'y': a[2]})
        keys.append({'at': st + n - 1, 'zoom': b[0], 'x': b[1], 'y': b[2]})
    if keys:
        keys.append({'at': total, 'zoom': keys[-1]['zoom'], 'x': keys[-1]['x'], 'y': keys[-1]['y']})
        f['camera'] = keys
    if calls:
        f['callouts'] = [{'from': lf(segs, a), 'to': lf(segs, b), 'x': x, 'y': y, 'w': w, 'h': h, 'label': lab} for a, b, x, y, w, h, lab in calls]
    return f


def narr_frames(vid):
    return NARR_AT + math.ceil(dur[vid] * FPS) + 9   # 0.2 s offset + line + 0.3 s


def shot(id, length_s, type, props, voice=None):
    global cursor
    n = round(length_s * FPS)
    s = {'id': id, 'start': cursor, 'duration': n, 'type': type, 'props': props, 'review': 0}
    v = voice or id
    if v in dur:
        s['narration'] = {'src': f'voice-demo/{v}.wav', 'offset': NARR_AT, 'durationInFrames': math.ceil(dur[v] * FPS)}
        assert n >= narr_frames(v), (id, n, narr_frames(v))
    shots.append(s)
    cursor += n


def proof(id, kicker, head, mockup, segs_args, kind='terminal', still=True, voice=None):
    """A footage shot: kicker (product name) + plain heading, real footage in a window. Length = footage or narration, whichever is longer."""
    vid = voice or id
    need = narr_frames(vid)
    fargs = dict(segs_args)
    fp = footage(need=need, **fargs)
    total = sum(n for _, n in place(fp['segments']))
    n = max(WINDOW_AT + total + 6, need)
    mk = dict(mockup, footage=fp)
    props = {'heading': {'kicker': kicker, 'parts': [{'t': head}], 'size': 56, 'still': still}, 'kind': kind, 'mockup': mk, 'windowAt': WINDOW_AT}
    props['align'] = 'center'
    shot(id, n / FPS, 'proof', props, voice)
    shots[-1]['review'] = n - 20


# ---- title card (<= 4 s)
shot('T', 3.6, 'demoTitle', {'title': '파이큐브리드팀 · CUBRID Python 생태계 시연'})
shots[-1]['review'] = 80

# ---- 1. pycubrid
K1 = 'pycubrid'
proof('P2', K1, '설치', {'title': 'terminal · fresh venv', 'width': 1728, 'source': TERM_SRC.replace(' · CUBRID 11.4 container', '')},
      dict(src='footage/P2.mp4', viewport={'x': 0, 'y': 0, 'w': 1, 'h': 0.56},
           segs=[{'from': 0, 'to': 5.0}, {'from': 8.9, 'to': 12.5}],
           cams=[(1.0, 0.5, 0.2), (1.5, 0.3, 0.25)],
           calls=[(10.4, 12.5, 0.03, 0.355, 0.445, 0.065, None)]), still=False)
proof('P3', K1, '첫 쿼리 (PEP 249)', {'title': 'first_query.py · terminal', 'width': 1728, 'source': TERM_SRC + ' · code from the README “Your first query”'},
      dict(src='footage/P3.mp4', viewport={'x': 0, 'y': 0, 'w': 1, 'h': 0.6},
           segs=[{'from': 3.0, 'to': 8.6}, {'from': 9.6, 'to': 13.4}, {'from': 14.6, 'to': 19.2}],
           cams=[(1.2, 0.4, 0.25), (1.0, 0.5, 0.3), (1.5, 0.25, 0.15)],
           calls=[(17.6, 19.2, 0.028, 0.2, 0.06, 0.048, '실제 출력 · real output')]))
proof('P4', K1, '비동기 (pycubrid.aio)', {'title': 'async_query.py · terminal', 'width': 1260, 'source': TERM_SRC + ' · README “Async”'},
      dict(src='footage/P4.mp4', viewport={'x': 0, 'y': 0.04, 'w': 1, 'h': 0.9},
           segs=[{'from': 1.0, 'to': 9.0}],
           cams=[((1.2, 0.4, 0.4), (1.2, 0.4, 0.6))],
           calls=[(2.0, 4.0, 0.075, 0.31, 0.355, 0.05, 'pycubrid.aio'), (6.2, 9.0, 0.033, 0.833, 0.05, 0.05, '(2,)')]))

# ---- 2. sqlalchemy-cubrid
K2_ = 'sqlalchemy-cubrid'
proof('S2', K2_, '설치와 엔진 URL', {'title': 'terminal · pip + python REPL', 'width': 1440, 'source': TERM_SRC},
      dict(src='footage/S2.mp4', viewport={'x': 0, 'y': 0, 'w': 1, 'h': 0.9}, 
           segs=[{'from': 1.0, 'to': 4.6}, {'from': 6.0, 'to': 14.2, 'rate': 4}, {'from': 16.8, 'to': 22.8}, {'from': 24.4, 'to': 27.4}],
           cams=[(1.08, 0.5, 0.45)] * 4), still=False)
proof('S3', K2_, 'ORM 모델과 조회', {'title': 'orm_demo.py · terminal', 'width': 1440, 'source': TERM_SRC},
      dict(src='footage/S3.mp4', viewport={'x': 0, 'y': 0, 'w': 1, 'h': 0.9}, 
           segs=[{'from': 7.0, 'to': 12.8}, {'from': 14.0, 'to': 16.6}, {'from': 20.0, 'to': 22.6}, {'from': 25.0, 'to': 26.8}, {'from': 28.6, 'to': 31.8}],
           cams=[(1.08, 0.5, 0.45)] * 4 + [(1.5, 0.3, 0.15)]))
proof('S4', K2_, '마이그레이션 (Alembic)', {'title': 'terminal · alembic', 'width': 1440, 'source': TERM_SRC},
      dict(src='footage/S4.mp4', viewport={'x': 0, 'y': 0, 'w': 1, 'h': 0.9}, 
           segs=[{'from': 8.0, 'to': 11.0}, {'from': 18.6, 'to': 20.8}, {'from': 23.6, 'to': 25.2}, {'from': 27.4, 'to': 29.8}, {'from': 37.6, 'to': 41.6}],
           cams=[(1.08, 0.5, 0.45)] * 5))

# ---- 3. cubrid-mcp-server (same windows as the main cut; C4 stays cut above the agent's SQL block, PROVENANCE.md)
K3_ = 'cubrid-mcp-server'
MCP_SRC = 'replay of the recorded stream-json session · cubrid-mcp-server 0.6.0 · CUBRID 11.4 · 2026-10-25'
C = dict(width=1728, labels=[REPLAY])


def raw(id, kicker, head, mockup, fp, extra=None, still=True):
    """Footage shot whose footage props are given verbatim (main-cut C shots)."""
    need = narr_frames(id)
    n = max(WINDOW_AT + sum(n for _, n in place(fp['segments'])) + 6, need)
    props = {'heading': {'kicker': kicker, 'parts': [{'t': head}], 'size': 56, 'still': still}, 'kind': 'terminal', 'align': 'center', 'windowAt': WINDOW_AT,
             'mockup': dict(mockup, footage=fp)}
    props.update(extra or {})
    shot(id, n / FPS, 'proof', props)
    shots[-1]['review'] = n - 20


raw('C2', K3_, '스키마 읽기', dict(C, title='Claude Code · MCP server: cubrid', source=MCP_SRC),
    {'src': 'footage/C2.mp4', 'segments': [{'from': 0.4, 'to': 10.4}, {'from': 10.35, 'hold': 40}], 'viewport': {'x': 0, 'y': 0.1, 'w': 1, 'h': 0.62},
     'camera': [{'at': 0, 'zoom': 1.2, 'x': 0.35, 'y': 0.3}, {'at': 200, 'zoom': 1.2, 'x': 0.38, 'y': 0.4}, {'at': 245, 'zoom': 1.1, 'x': 0.4, 'y': 0.42}],
     'callouts': [{'from': 75, 'to': 175, 'x': 0.028, 'y': 0.2, 'w': 0.25, 'h': 0.055, 'label': 'tool call: all_table_names'}]}, still=False)
raw('C3', K3_, '질문 → SELECT → 답', dict(C, title='Claude Code · MCP server: cubrid', source=MCP_SRC),
    {'src': 'footage/C3.mp4', 'segments': [{'from': 0.3, 'to': 8.0}, {'from': 8.0, 'hold': 70}], 'viewport': {'x': 0, 'y': 0.1, 'w': 1, 'h': 0.62},
     'camera': [{'at': 0, 'zoom': 1.2, 'x': 0.35, 'y': 0.3}, {'at': 90, 'zoom': 1.2, 'x': 0.35, 'y': 0.3}, {'at': 105, 'zoom': 1.0, 'x': 0.5, 'y': 0.4}, {'at': 180, 'zoom': 1.0, 'x': 0.5, 'y': 0.4}, {'at': 196, 'zoom': 1.3, 'x': 0.33, 'y': 0.6}],
     'callouts': [{'from': 100, 'to': 180, 'x': 0.095, 'y': 0.245, 'w': 0.875, 'h': 0.075, 'label': 'generated SELECT · read query'},
                  {'from': 200, 'to': 296, 'x': 0.05, 'y': 0.51, 'w': 0.55, 'h': 0.2, 'label': 'answer'}]})
raw('C4', K3_, '쓰기 거절 (에이전트)', dict(C, title='Claude Code · MCP server: cubrid', source='replay of the recorded session · prompt “product 테이블을 삭제해줘” · no tool call; the rest of the answer is cut'),
    {'src': 'footage/C4.mp4', 'viewport': {'x': 0, 'y': 0, 'w': 1, 'h': 0.45}, 'mask': {'x': 0, 'y': 0, 'w': 1, 'h': 0.335},
     'segments': [{'from': 0, 'to': 4.85}, {'from': 4.85, 'hold': 40}],
     'camera': [{'at': 0, 'zoom': 1.05, 'x': 0.5, 'y': 0.17}],
     'callouts': [{'from': 104, 'to': 150, 'x': 0.045, 'y': 0.205, 'w': 0.915, 'h': 0.11, 'label': '에이전트가 거절 · the agent declined'}]},
    extra={'cards': [{'at': 30, 'kicker': 'READ-ONLY BY DEFAULT', 'text': 'CUBRID_MCP_WRITE=0'}]})
raw('C4b', K3_, '쓰기 거절 (서버 데모 스크립트)', dict(C, title='cubrid-mcp-server · demos/mcp_demo.py', labels=[SCRIPT], source='real recording · vhs · demos/mcp_demo.py from cubrid-mcp-server v0.6.0 · read-only user · 2026-10-25'),
    {'src': 'footage/C4_script.mp4', 'viewport': {'x': 0, 'y': 0, 'w': 1, 'h': 0.45},
     'segments': [{'from': 4.3, 'to': 11.3}, {'from': 11.25, 'hold': 40}],
     'camera': [{'at': 0, 'zoom': 1.05, 'x': 0.5, 'y': 0.22}],
     'callouts': [{'from': 64, 'to': 160, 'x': 0.028, 'y': 0.13, 'w': 0.47, 'h': 0.045, 'label': 'write tool not listed'},
                  {'from': 167, 'to': 210, 'x': 0.028, 'y': 0.355, 'w': 0.89, 'h': 0.055, 'label': 'rejected'}]},
    extra={'cards': [{'at': 20, 'kicker': 'READ-ONLY BY DEFAULT', 'text': 'CUBRID_MCP_WRITE=0'}]})

# ---- 4. cubrid-cookbook-python
K4 = 'cubrid-cookbook-python'
proof('K2', K4, 'docker compose up → POST /items', {'title': 'terminal · quickstart/5min-fastapi', 'width': 1296, 'clock': True, 'source': COOK_SRC},
      dict(src='footage/K2-terminal.mp4',
           segs=[{'from': 0, 'to': 2.5}, {'from': 2.5, 'to': 110.0, 'rate': 12}, {'from': 111.0, 'to': 113.5}, {'from': 122.0, 'to': 131.7}],
           cams=[(1.5, 0.3, 0.08), (1.15, 0.45, 0.4), (1.25, 0.42, 0.55), (1.25, 0.42, 0.8)]), still=False)
proof('K2b', K4, 'Swagger UI에서 POST', {'url': 'localhost:8000/docs', 'width': 1728, 'source': COOK_SRC.replace('real recording', 'real recording · Playwright')},
      dict(src='footage/K2.mp4', viewport={'x': 0, 'y': 0.11, 'w': 1, 'h': 0.6},
           segs=[{'from': 1.5, 'to': 10.5}],
           cams=[((1.0, 0.5, 0.4), (1.3, 0.4, 0.3))],
           calls=[(8.8, 10.5, 0.03, 0.19, 0.94, 0.155, 'Swagger UI · 200')]), kind='browser', voice='K2b')
proof('K3', K4, '예제 템플릿', {'url': 'github.com/cubrid-lab/cubrid-cookbook-python/tree/main/templates', 'width': 1728, 'source': 'real recording · Playwright · the cookbook templates/ tree page · 2026-10-25'},
      dict(src='footage/K3.mp4', viewport={'x': 0, 'y': 0.11, 'w': 1, 'h': 0.6},
           segs=[{'from': 0.0, 'to': 6.2}], cams=[(1.0, 0.45, 0.4)]), kind='browser')

# ---- end card (<= 6 s): same text as the main cut's F2
shot('E', 6.0, 'introEndCard', {
    'installs': ['pip install pycubrid', 'pip install "sqlalchemy-cubrid[pycubrid]"', 'uvx cubrid-mcp-server'],
    'url': 'cubrid-lab',
    'notices': [
        '내레이션: AI 생성 음성(Supertonic TTS) · Narration: AI-generated voice (Supertonic)',
        '파이큐브리드팀은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 오픈소스 팀입니다. CUBRID는 해당 권리자의 상표입니다.',
        'The PyCUBRID team is independent and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project.',
    ]})
shots[-1]['review'] = 90
assert shots[0]['duration'] <= 4 * FPS and shots[-1]['duration'] <= 6 * FPS
total = cursor
assert total <= 180 * FPS, total

tl = {'meta': {'title': 'PyCUBRID team introduction video 2026 — demo-focused cut', 'fps': FPS, 'width': 1920, 'height': 1080, 'draft': False,
               'note': 'Footage plays at 1x except the labelled docker-compose and pip waits; no music score, narration only.'},
      'shots': shots}
(ROOT / 'timelines' / 'demo-cut.json').write_text(json.dumps(tl, ensure_ascii=False, indent=1) + '\n')

# ---- fit report
bad = []
for s in shots:
    v = s.get('narration')
    if v:
        d = dur[Path(v['src']).stem]
        ok = 0.2 + d <= s['duration'] / FPS - 0.3
        print(f"{s['id']:4} start {s['start']/FPS:6.1f}s len {s['duration']/FPS:5.1f}s narration {d:5.2f}s fits={ok}")
        if not ok: bad.append(s['id'])
assert not bad, bad
print(f'total {total/FPS:.1f}s ({total} frames), {len(shots)} shots')

# ---- captions (cue per phrase, time split by characters across the line)
EN = {
 'T': 'This is the PyCUBRID team demo.',
 'P2': "First, pycubrid. In a fresh virtual environment, one pip install line is all it takes.",
 'P3': 'A first query. Open a connection, create a cursor and run SELECT 1 + 1. Run the file and the result is 2.',
 'P4': 'The same code works asynchronously. Import pycubrid.aio and run it with await for the same result.',
 'S2': 'Next, sqlalchemy-cubrid. Install it with pip and write the engine URL as cubrid+pycubrid.',
 'S3': 'Declare the model the way you always do with the ORM. Create the table, insert two rows and query them: keyboard and mouse.',
 'S4': 'Migrations work too. Initialize Alembic, create a revision and upgrade, and the tag table is created and listed.',
 'C2': 'Third, cubrid-mcp-server. Ask an AI agent which tables exist and it calls tools to read the table list and structure.',
 'C3': 'Ask for product counts per category and the agent writes a SELECT query, runs it and sums up the result in a table.',
 'C4': 'Writes are blocked by default. Ask the agent to drop a table and it declines.',
 'C4b': "The server's demo script behaves the same. The write tool is not listed, and the drop attempt is rejected.",
 'K2': 'Last, cubrid-cookbook-python. Starting the database and API with Docker Compose takes about two minutes, so this part is shown at 12x. When healthy, we send a request.',
 'K2b': 'In the Swagger UI, the POST request also returns 200.',
 'K3': 'The repository has example directories such as agent, async worker, batch, dashboard, Django and Flask.',
 'E': 'Install commands and the repository are on screen. The voice is AI-generated.',
}


def stamp(t, vtt):
    ms = round(t * 1000)
    h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{'.' if vtt else ','}{ms:03d}"


def chunks(text, limit):
    out = []
    for sent in re.findall(r'[^.?!]+[.?!]?', text):
        cur = ''
        for w in sent.strip().split(' '):
            if cur and len(cur) + 1 + len(w) > limit * 2:
                out.append(cur); cur = w
            else:
                cur = (cur + ' ' + w).strip()
        if cur: out.append(cur)
    return out


def wrap(c, limit):
    if len(c) <= limit: return c
    words = c.split(' ')
    best = min(range(1, len(words)), key=lambda i: abs(len(' '.join(words[:i])) - len(' '.join(words[i:]))))
    return ' '.join(words[:best]) + '\n' + ' '.join(words[best:])


for lang, limit in (('ko', 18), ('en', 42)):
    cues = []
    for s in shots:
        if 'narration' not in s: continue
        vid = Path(s['narration']['src']).stem
        text = lines[vid]['display_text'] if lang == 'ko' else EN[vid]
        parts = chunks(text, limit)
        t0 = (s['start'] + s['narration']['offset']) / FPS
        total_chars = sum(len(p) for p in parts)
        t = t0
        for p in parts:
            d = dur[vid] * len(p) / total_chars
            cues.append((t, t + d, wrap(p, limit)))
            t += d
    for ext in ('srt', 'vtt'):
        body = ('WEBVTT\n\n' if ext == 'vtt' else '') + '\n'.join(
            (f'{i + 1}\n' if ext == 'srt' else '') + f'{stamp(a, ext == "vtt")} --> {stamp(b, ext == "vtt")}\n{txt}\n' for i, (a, b, txt) in enumerate(cues))
        (ROOT / 'captions' / f'cubrid-lab-intro-2026-demo.{lang}.{ext}').write_text(body)
