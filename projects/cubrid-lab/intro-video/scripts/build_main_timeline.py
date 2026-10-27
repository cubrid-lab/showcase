#!/usr/bin/env python3
"""Builds timelines/main.json (the 25-shot main cut of VIDEO_DESIGN.md) from the shot list below.

    python3 scripts/build_main_timeline.py [voice/manifest.json]

Narration lengths come from the voice manifest (default: $INTRO_ASSETS/voice/manifest.json).
Footage segment times, camera keys and callouts are in source seconds / shot frames; see the
README "Timeline format". Edit here, not in the JSON.
"""
import json, math, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get('INTRO_ASSETS', '/data/video-intro-assets'), 'voice', 'manifest.json')
man = json.load(open(MANIFEST))
dur = {s['shot']: s['duration_s'] for s in man['shots']}
REPLAY = '실제 세션 재생 · recorded session replay (Claude Code)'
SCRIPT = 'MCP 클라이언트 스크립트 · MCP client script'
shots = []
def shot(id, start_s, len_s, type, props, voice=None, trans=None, sid=None):
    s = {'id': id, 'start': round(start_s*30), 'duration': round(len_s*30), 'type': type, 'props': props}
    v = voice if voice is not None else id
    if v and v in dur:
        s['narration'] = {'src': f'voice/{v}.wav', 'offset': 6, 'durationInFrames': math.ceil(dur[v]*30)}
    if trans: s['transitionIn'] = trans
    shots.append(s)
KEY = {'type': 'keyWipe', 'duration': 14}
TERM_SRC = 'real recording · vhs · CUBRID 11.4 container · 2026-10-26'

shot('H1', 0, 2, 'hook', {'stage': 1})
shot('H2', 2, 2, 'hook', {'stage': 2})
shot('H3', 4, 2, 'flash', {'each': 15, 'flashes': [
  {'title': 'pip install pycubrid', 'footage': {'src': 'footage/H3-P2.mp4', 'segments': [{'from': 0.5}], 'camera': [{'at': 0, 'zoom': 2.0, 'x': 0.26, 'y': 0.36}]}},
  {'title': 'python orm_demo.py', 'footage': {'src': 'footage/H3-S3.mp4', 'segments': [{'from': 0.5}], 'camera': [{'at': 0, 'zoom': 2.4, 'x': 0.14, 'y': 0.17}]}},
  {'title': 'cubrid-mcp-server · demos/mcp_demo.py', 'footage': {'src': 'footage/C4_script.mp4', 'segments': [{'from': 10.2}], 'camera': [{'at': 0, 'zoom': 1.6, 'x': 0.31, 'y': 0.33}]}},
  {'kind': 'browser', 'url': 'localhost:8000/docs', 'footage': {'src': 'footage/H3-K2.mp4', 'segments': [{'from': 0.5}], 'viewport': {'x': 0, 'y': 0.11, 'w': 1, 'h': 0.89}, 'camera': [{'at': 0, 'zoom': 1.8, 'x': 0.3, 'y': 0.28}]}},
]}, voice='')
shot('B1', 6, 6, 'brandTiles', {'beat': 15})
shot('B2', 12, 8, 'brandLockup', {})
shot('P1', 20, 4, 'chapter', {'repo': 'pycubrid', 'kicker': '01 · Driver · DB-API 2.0', 'name': 'pycubrid', 'tagline': '순수 Python으로 만든 CUBRID 드라이버'}, trans=KEY)
# P2: install, Successfully installed callout
shot('P2', 24, 8, 'proof', {
  'heading': {'kicker': 'pycubrid', 'parts': [{'t': '설치 '}, {'t': '한 줄.', 'accent': True}]},
  'mockup': {'title': 'terminal · fresh venv', 'width': 1728, 'source': TERM_SRC.replace(' · CUBRID 11.4 container', ''),
    'footage': {'src': 'footage/P2.mp4', 'viewport': {'x': 0, 'y': 0, 'w': 1, 'h': 0.56},
      'segments': [{'from': 0, 'to': 9.4, 'rate': 2}, {'from': 9.4, 'to': 12.5}, {'from': 12.4, 'hold': 30}],
      'camera': [{'at': 0, 'zoom': 1.0, 'x': 0.5, 'y': 0.3}, {'at': 140, 'zoom': 1.0, 'x': 0.5, 'y': 0.3}, {'at': 160, 'zoom': 1.7, 'x': 0.27, 'y': 0.33}],
      'callouts': [{'from': 150, 'to': 230, 'x': 0.03, 'y': 0.355, 'w': 0.445, 'h': 0.065, 'label': 'Successfully installed'}]}},
})
# P3: first query, (2,)
shot('P3', 32, 12, 'proof', {
  'heading': {'kicker': 'pycubrid', 'parts': [{'t': 'PEP 249, '}, {'t': '그대로.', 'accent': True}]},
  'mockup': {'title': 'first_query.py · terminal', 'width': 1728, 'source': TERM_SRC + ' · code from the README “Your first query”',
    'footage': {'src': 'footage/P3.mp4', 'viewport': {'x': 0, 'y': 0, 'w': 1, 'h': 0.6},
      'segments': [{'from': 0, 'to': 13.9, 'rate': 2}, {'from': 13.9, 'to': 18.9}, {'from': 18.9, 'hold': 30}],
      'camera': [{'at': 0, 'zoom': 1.0, 'x': 0.5, 'y': 0.3}, {'at': 260, 'zoom': 1.0, 'x': 0.5, 'y': 0.3}, {'at': 282, 'zoom': 2.2, 'x': 0.12, 'y': 0.16}],
      'callouts': [{'from': 285, 'to': 348, 'x': 0.028, 'y': 0.2, 'w': 0.06, 'h': 0.048, 'label': '실제 출력 · real output'}]}},
})
# P4: async + chips
shot('P4', 44, 8, 'proof', {
  'heading': {'kicker': 'pycubrid', 'parts': [{'t': 'asyncio · TLS · LOB'}]},
  'chips': {'items': ['asyncio', 'TLS', 'LOB'], 'at': [15, 30, 45]},
  'mockup': {'title': 'async_query.py · terminal', 'width': 1260, 'source': TERM_SRC + ' · README “Async”',
    'footage': {'src': 'footage/P4.mp4', 'viewport': {'x': 0, 'y': 0.04, 'w': 1, 'h': 0.9},
      'segments': [{'from': 0, 'to': 2.4, 'rate': 2}, {'from': 2.4, 'to': 9.0}, {'from': 9.0, 'hold': 30}],
      'camera': [{'at': 0, 'zoom': 1.25, 'x': 0.36, 'y': 0.4}, {'at': 100, 'zoom': 1.25, 'x': 0.36, 'y': 0.4}, {'at': 130, 'zoom': 1.6, 'x': 0.3, 'y': 0.7}],
      'callouts': [{'from': 40, 'to': 110, 'x': 0.075, 'y': 0.31, 'w': 0.355, 'h': 0.05, 'label': 'pycubrid.aio'},
                   {'from': 132, 'to': 225, 'x': 0.033, 'y': 0.833, 'w': 0.05, 'h': 0.05, 'label': '(2,)'}]}},
})
shot('P5', 52, 6, 'button', {'repo': 'pycubrid', 'command': 'pip install pycubrid', 'heading': {'parts': [{'t': 'C 컴파일러 '}, {'t': '없이.', 'accent': True, 'underline': True}]}})
shot('S1', 58, 4, 'chapter', {'repo': 'sqlalchemy-cubrid', 'kicker': '02 · ORM · SQLAlchemy 2.0–2.1', 'name': 'sqlalchemy-cubrid', 'tagline': 'CUBRID용 SQLAlchemy 방언(dialect)'}, trans=KEY)
# S2: install + engine URL
shot('S2', 62, 8, 'proof', {
  'heading': {'kicker': 'sqlalchemy-cubrid', 'parts': [{'t': '엔진 URL '}, {'t': '하나.', 'accent': True}]},
  'align': 'center',
  'mockup': {'title': 'terminal · pip + python REPL', 'width': 1152, 'source': TERM_SRC,
    'footage': {'src': 'footage/S2.mp4',
      'segments': [{'from': 0.6, 'to': 14.6, 'rate': 5}, {'from': 14.6, 'to': 21.2, 'rate': 2}, {'from': 21.2, 'hold': 60}],
      'camera': [{'at': 0, 'zoom': 1.15, 'x': 0.4, 'y': 0.6}, {'at': 120, 'zoom': 1.3, 'x': 0.45, 'y': 0.75}, {'at': 175, 'zoom': 1.3, 'x': 0.45, 'y': 0.75}, {'at': 196, 'zoom': 1.4, 'x': 0.45, 'y': 0.8}],
      'callouts': [{'from': 184, 'to': 226, 'x': 0.352, 'y': 0.807, 'w': 0.193, 'h': 0.05, 'label': 'cubrid+pycubrid://'}]}},
})
# S3: ORM model, Mapped[int], rows
shot('S3', 70, 14, 'proof', {
  'heading': {'kicker': 'sqlalchemy-cubrid', 'parts': [{'t': '익숙한 ORM, '}, {'t': '그대로.', 'accent': True}]},
  'align': 'center',
  'mockup': {'title': 'orm_demo.py · terminal', 'width': 1152, 'source': TERM_SRC,
    'footage': {'src': 'footage/S3.mp4',
      'segments': [{'from': 0.5, 'to': 27.5, 'rate': 3}, {'from': 27.5, 'to': 31.0}, {'from': 31.0, 'hold': 45}],
      'camera': [{'at': 0, 'zoom': 1.45, 'x': 0.4, 'y': 0.28}, {'at': 150, 'zoom': 1.45, 'x': 0.4, 'y': 0.28}, {'at': 200, 'zoom': 1.35, 'x': 0.42, 'y': 0.62}, {'at': 268, 'zoom': 1.35, 'x': 0.42, 'y': 0.62}, {'at': 285, 'zoom': 2.2, 'x': 0.15, 'y': 0.15}],
      'callouts': [{'from': 110, 'to': 190, 'x': 0.157, 'y': 0.41, 'w': 0.13, 'h': 0.055, 'label': 'Mapped[int]'},
                   {'from': 362, 'to': 412, 'x': 0.026, 'y': 0.148, 'w': 0.13, 'h': 0.105, 'label': '실제 출력 · real rows'}]}},
})
# S4: alembic + reflection
shot('S4', 84, 8, 'proof', {
  'heading': {'kicker': 'sqlalchemy-cubrid', 'parts': [{'t': 'Alembic · Reflection · Async'}]},
  'chips': {'items': ['Alembic', 'Reflection', 'Async'], 'at': [15, 30, 45]},
  'mockup': {'title': 'terminal · alembic', 'width': 1152, 'source': TERM_SRC,
    'footage': {'src': 'footage/S4.mp4',
      'segments': [{'from': 25.5, 'to': 29.0}, {'from': 29.0, 'to': 40.2, 'rate': 4}, {'from': 40.2, 'hold': 60}],
      'camera': [{'at': 0, 'zoom': 1.3, 'x': 0.4, 'y': 0.62}, {'at': 160, 'zoom': 1.3, 'x': 0.4, 'y': 0.7}, {'at': 180, 'zoom': 1.8, 'x': 0.25, 'y': 0.85}],
      'callouts': [{'from': 92, 'to': 150, 'x': 0.03, 'y': 0.6, 'w': 0.86, 'h': 0.19, 'label': 'alembic upgrade head'},
                   {'from': 186, 'to': 226, 'x': 0.03, 'y': 0.832, 'w': 0.385, 'h': 0.052, 'label': 'get_table_names()'}]}},
})
shot('S5', 92, 4, 'hit', {'repo': 'sqlalchemy-cubrid', 'heading': {'parts': [{'t': 'ORM도, '}, {'t': 'CUBRID로.', 'accent': True}]}})
shot('C1', 96, 4, 'chapter', {'repo': 'cubrid-mcp-server', 'kicker': '03 · AI · Model Context Protocol', 'name': 'cubrid-mcp-server', 'tagline': 'AI 에이전트를 위한 CUBRID MCP 서버'}, trans=KEY)
shot('C2', 100, 10, 'proof', {
  'heading': {'kicker': 'cubrid-mcp-server', 'parts': [{'t': 'AI가 '}, {'t': '읽고,', 'accent': True}]},
  'mockup': {'title': 'Claude Code · MCP server: cubrid', 'width': 1728, 'labels': [REPLAY], 'source': 'replay of the recorded stream-json session · cubrid-mcp-server 0.6.0 · CUBRID 11.4 · 2026-10-25',
    'footage': {'src': 'footage/C2.mp4', 'segments': [{'from': 0.4}], 'viewport': {'x': 0, 'y': 0.1, 'w': 1, 'h': 0.62},
      'camera': [{'at': 0, 'zoom': 1.2, 'x': 0.35, 'y': 0.3}, {'at': 200, 'zoom': 1.2, 'x': 0.38, 'y': 0.4}, {'at': 245, 'zoom': 1.1, 'x': 0.4, 'y': 0.42}],
      'callouts': [{'from': 75, 'to': 175, 'x': 0.028, 'y': 0.2, 'w': 0.25, 'h': 0.055, 'label': 'tool call: all_table_names'}]}},
}, sid='C2')
shot('C3', 110, 10, 'proof', {
  'heading': {'kicker': 'cubrid-mcp-server', 'parts': [{'t': '질문 → '}, {'t': 'SELECT', 'accent': True}]},
  'mockup': {'title': 'Claude Code · MCP server: cubrid', 'width': 1728, 'labels': [REPLAY], 'enter': False, 'source': 'replay of the recorded stream-json session · cubrid-mcp-server 0.6.0 · CUBRID 11.4 · 2026-10-25',
    'footage': {'src': 'footage/C3.mp4', 'segments': [{'from': 0.3, 'to': 8.0}, {'from': 8.0, 'hold': 70}], 'viewport': {'x': 0, 'y': 0.1, 'w': 1, 'h': 0.62},
      'camera': [{'at': 0, 'zoom': 1.2, 'x': 0.35, 'y': 0.3}, {'at': 90, 'zoom': 1.2, 'x': 0.35, 'y': 0.3}, {'at': 105, 'zoom': 1.0, 'x': 0.5, 'y': 0.4}, {'at': 180, 'zoom': 1.0, 'x': 0.5, 'y': 0.4}, {'at': 196, 'zoom': 1.3, 'x': 0.33, 'y': 0.6}],
      'callouts': [{'from': 100, 'to': 180, 'x': 0.095, 'y': 0.245, 'w': 0.875, 'h': 0.075, 'label': 'generated SELECT · read query'},
                   {'from': 200, 'to': 296, 'x': 0.05, 'y': 0.51, 'w': 0.55, 'h': 0.2, 'label': 'answer'}]}},
})
C4H = {'kicker': 'cubrid-mcp-server', 'parts': [{'t': 'AI가 읽고, '}, {'t': '쓰기는 막는다.', 'accent': True, 'underline': True}]}
shot('C4', 120, 5, 'proof', {
  'heading': C4H,
  'mockup': {'title': 'Claude Code · MCP server: cubrid', 'width': 1728, 'labels': [REPLAY], 'source': 'replay of the recorded session · prompt “product 테이블을 삭제해줘” · no tool call; the rest of the answer is cut',
    'footage': {'src': 'footage/C4.mp4', 'viewport': {'x': 0, 'y': 0, 'w': 1, 'h': 0.45}, 'mask': {'x': 0, 'y': 0, 'w': 1, 'h': 0.335},
      'segments': [{'from': 0, 'to': 4.85}, {'from': 4.85, 'hold': 10}],
      'camera': [{'at': 0, 'zoom': 1.05, 'x': 0.5, 'y': 0.17}],
      'callouts': [{'from': 104, 'to': 150, 'x': 0.045, 'y': 0.205, 'w': 0.915, 'h': 0.11, 'label': '에이전트가 거절 · the agent declined'}]}},
  'cards': [{'at': 30, 'kicker': 'READ-ONLY BY DEFAULT', 'text': 'CUBRID_MCP_WRITE=0'}],
})
shot('C4b', 125, 7, 'proof', {
  'heading': dict(C4H, still=True),
  'mockup': {'title': 'cubrid-mcp-server · demos/mcp_demo.py', 'width': 1728, 'labels': [SCRIPT], 'enter': False, 'source': 'real recording · vhs · demos/mcp_demo.py from cubrid-mcp-server v0.6.0 · read-only user · 2026-10-25',
    'footage': {'src': 'footage/C4_script.mp4', 'viewport': {'x': 0, 'y': 0, 'w': 1, 'h': 0.45},
      'segments': [{'from': 4.3, 'to': 11.3}],
      'camera': [{'at': 0, 'zoom': 1.05, 'x': 0.5, 'y': 0.22}],
      'callouts': [{'from': 64, 'to': 160, 'x': 0.028, 'y': 0.13, 'w': 0.47, 'h': 0.045, 'label': 'write tool not listed'},
                   {'from': 167, 'to': 210, 'x': 0.028, 'y': 0.355, 'w': 0.89, 'h': 0.055, 'label': 'rejected'}]}},
  'cards': [{'at': -100, 'kicker': 'READ-ONLY BY DEFAULT', 'text': 'CUBRID_MCP_WRITE=0'}],
}, voice='')
shot('C5', 132, 8, 'config', {
  'heading': {'kicker': 'cubrid-mcp-server', 'parts': [{'t': '쓰기는 '}, {'t': '연결별 opt-in', 'accent': True}]},
  'rows': [
    {'name': 'CUBRID_MCP_READONLY', 'def': '1', 'desc': 'Enforce read-only SQL whitelist.'},
    {'name': 'CUBRID_MCP_MAX_ROWS', 'def': '1000', 'desc': 'Max rows returned by execute_query before truncation'},
    {'name': 'CUBRID_MCP_WRITE', 'def': '0', 'desc': 'Opt-in write mode. Honoured per connection (CUBRID_<NAME>_MCP_WRITE). Off by default.', 'highlight': True},
  ],
  'rowAt': [10, 25, 40],
  'tools': ['execute_query', 'all_table_names', 'describe_table', '…'],
  'toolsAt': 55,
  'writeAt': 135,
  'offNote': 'When write mode is off the tool is not registered at all.',
  'writeNote': 'CUBRID_MCP_WRITE=1 registers execute_write (single-statement DML), per connection.',
  'source': 'text: cubrid-mcp-server README v0.6.0 · “Configure” table, “Write mode (opt-in)” · excerpt',
})
shot('K1', 140, 4, 'chapter', {'repo': 'cubrid-cookbook-python', 'kicker': '04 · Examples', 'name': 'cubrid-cookbook-python', 'tagline': '복사해서 바로 실행하는 Python 예제'}, trans=KEY)
KH = {'kicker': 'cubrid-cookbook-python', 'parts': [{'t': '복사해서, '}, {'t': '바로 실행.', 'accent': True}]}
COOK_SRC = 'real recording · cookbook quickstart/5min-fastapi @969c3f9 · its pinned cubrid/cubrid:11.2 · 2026-10-26'
shot('K2', 144, 5.5, 'proof', {
  'heading': KH, 'align': 'center',
  'mockup': {'title': 'terminal · quickstart/5min-fastapi', 'width': 1152, 'clock': True, 'source': COOK_SRC,
    'footage': {'src': 'footage/K2-terminal.mp4',
      'segments': [{'from': 0, 'to': 16.0, 'rate': 8}, {'from': 121.5, 'to': 125.4, 'rate': 2}, {'from': 125.4, 'hold': 60}],
      'camera': [{'at': 0, 'zoom': 1.2, 'x': 0.4, 'y': 0.3}, {'at': 56, 'zoom': 1.2, 'x': 0.4, 'y': 0.3}, {'at': 64, 'zoom': 1.45, 'x': 0.35, 'y': 0.8}],
      'callouts': [{'from': 117, 'to': 160, 'x': 0.035, 'y': 0.828, 'w': 0.41, 'h': 0.048, 'label': 'POST /items → id 1'}]}},
})
shot('K2b', 149.5, 4.5, 'proof', {
  'heading': dict(KH, still=True), 'align': 'center',
  'kind': 'browser',
  'mockup': {'url': 'localhost:8000/docs', 'width': 1728, 'enter': False, 'source': COOK_SRC.replace('real recording', 'real recording · Playwright'),
    'footage': {'src': 'footage/K2.mp4', 'viewport': {'x': 0, 'y': 0.11, 'w': 1, 'h': 0.6},
      'segments': [{'from': 3.4, 'to': 7.4, 'rate': 2.5}, {'from': 7.4, 'to': 9.8, 'rate': 1.5}, {'from': 9.8, 'hold': 60}],
      'camera': [{'at': 0, 'zoom': 1.0, 'x': 0.5, 'y': 0.4}, {'at': 84, 'zoom': 1.0, 'x': 0.5, 'y': 0.4}, {'at': 100, 'zoom': 1.3, 'x': 0.4, 'y': 0.27}],
      'callouts': [{'from': 98, 'to': 140, 'x': 0.03, 'y': 0.19, 'w': 0.94, 'h': 0.155, 'label': 'Swagger UI · 200'}]}},
}, voice='')
shot('K3', 154, 8, 'cards', {
  'heading': dict(KH, still=True),
  'at': 54, 'beat': 8,
  'mockup': {'url': 'github.com/cubrid-lab/cubrid-cookbook-python/tree/main/templates', 'width': 1728, 'enter': False,
    'footage': {'src': 'footage/K3.mp4', 'viewport': {'x': 0, 'y': 0.11, 'w': 1, 'h': 0.6}, 'segments': [{'from': 2.2, 'to': 4.2}, {'from': 4.2, 'hold': 200}],
      'camera': [{'at': 0, 'zoom': 1.2, 'x': 0.45, 'y': 0.4}]}},
  'cards': [
    {'label': 'FastAPI 5분 시작', 'path': 'quickstart/5min-fastapi'},
    {'label': 'Flask', 'path': 'templates/flask'},
    {'label': 'Django 요청 처리', 'path': 'templates/django'},
    {'label': 'Celery 워커', 'path': 'templates/async-worker'},
    {'label': 'Pandas ETL', 'path': 'templates/batch-etl'},
    {'label': 'Streamlit 대시보드', 'path': 'templates/dashboard'},
    {'label': 'AI 에이전트 + MCP', 'path': 'templates/ai-agent'},
    {'label': 'Java → Python', 'path': 'migration/java-to-python'},
  ],
  'note': 'directory names from cubrid-cookbook-python main (git ls-tree, 2026-10-26) · background: the recorded templates/ tree page',
})
shot('F1', 162, 6, 'finale', {
  'beat': 15,
  'items': [
    {'repo': 'pycubrid', 'line': '설치 한 줄'},
    {'repo': 'sqlalchemy-cubrid', 'line': '익숙한 ORM'},
    {'repo': 'cubrid-mcp-server', 'line': '읽기 전용 AI'},
    {'repo': 'cubrid-cookbook-python', 'line': '바로 실행'},
  ],
  'heading': {'parts': [{'t': 'Python', 'accent': True}, {'t': '으로 CUBRID를, 처음부터 끝까지.'}]},
}, trans=KEY)
shot('F2', 168, 8, 'introEndCard', {
  'installs': ['pip install pycubrid', 'pip install "sqlalchemy-cubrid[pycubrid]"', 'uvx cubrid-mcp-server'],
  'url': 'cubrid-lab',
  'notices': [
    '내레이션: AI 생성 음성(TTS) · Narration: AI-generated voice',
    'CUBRID Lab은 CUBRID Corporation 및 공식 CUBRID 프로젝트와 제휴·후원·보증 관계가 없는 독립 프로젝트입니다. CUBRID는 해당 권리자의 상표입니다.',
    'CUBRID Lab is independently maintained and is not affiliated with, sponsored by, or endorsed by CUBRID Corporation or the official CUBRID project.',
  ],
}, trans={'type': 'fade', 'duration': 12})

tl = {
  'meta': {'title': 'CUBRID Lab introduction video 2026 — main cut (VIDEO_DESIGN.md, 25 shots, 2:56)', 'fps': 30, 'width': 1920, 'height': 1080, 'draft': False,
           'note': 'Shot ids follow the storyboard; C4b and K2b are the second halves of C4 and K2.'},
  'music': {'src': 'music/bed.wav', 'volume': 1, 'duckedVolume': 0.398, 'rampFrames': 6, 'fadeInFrames': 1, 'fadeOutFrames': 1},
  'shots': shots,
}
# sanity: contiguous
REVIEW = dict(H1=40, H2=40, H3=37, B1=150, B2=150, P1=90, P2=200, P3=320, P4=180, P5=150, S1=90, S2=215, S3=385, S4=210,
              S5=100, C1=90, C2=120, C3=150, C4=135, C4b=195, C5=200, K1=90, K2=145, K2b=110, K3=200, F1=160, F2=200)
for s in shots:
    s['review'] = REVIEW[s['id']]
t = 0
for s in shots:
    assert s['start'] == t, (s['id'], s['start'], t)
    t += s['duration']
assert t == 5280, t
(ROOT / 'timelines' / 'main.json').write_text(json.dumps(tl, ensure_ascii=False, indent=1) + '\n')
print('ok', len(shots), t)
