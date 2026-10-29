import json, sys
from pathlib import Path
sys.path.insert(0, '/data/video-intro-assets/voice-melotts-2026-10-27')
import synth
from supertonic import TTS
LINES = json.load(open(sys.argv[1]))
OUT = Path('/data/video-intro-assets/voice-demo'); RAW = OUT / 'raw'; RAW.mkdir(exist_ok=True)
tts = TTS(model='supertonic-3'); style = tts.get_voice_style('M5')
shots = []
for s in LINES:
    wav, _ = tts.synthesize(s['tts_input'], style, total_steps=16, speed=1.05, lang='ko')
    raw = RAW / f"{s['shot']}.wav"; tts.save_audio(wav, str(raw))
    dst = OUT / f"{s['shot']}.wav"; synth.postprocess(raw, dst, 60)
    d = round(synth.duration(dst), 3)
    shots.append({'shot': s['shot'], 'tts_input': s['tts_input'], 'display_text': s['display_text'], 'duration_s': d, 'speed': 1.05})
    print(s['shot'], d, flush=True)
man = {'engine': 'supertonic', 'model': 'Supertone/supertonic-3', 'speaker': 'M5', 'steps': 16, 'device': 'cpu (onnxruntime)',
       'sample_rate': 48000, 'loudness': {'I': -16.0, 'TP': -1.5}, 'caption_offset_s': 0.2,
       'fit_rule': '0.2 s caption/voice offset + duration_s <= shot_length_s - 0.3', 'shots': shots}
(OUT / 'manifest.json').write_text(json.dumps(man, ensure_ascii=False, indent=1) + '\n')
