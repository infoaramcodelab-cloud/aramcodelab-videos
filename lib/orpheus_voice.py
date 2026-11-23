"""Narration with Orpheus 3B (MLX, local) for a lesson folder X/.

Needs Apple Silicon and `pip install mlx-audio soundfile` (the 4-bit weights, ~1.8 GB, download on first run):
    python lib/orpheus_voice.py X [key ...]

Writes X/audio/<key>.wav and X/audio/durations.json in the same format as `narrate.py voice`,
so scenes, cues and `narrate.py mux` work unchanged. With keys given, only those segments are
regenerated (durations.json is updated in place).

Orpheus drifts on long inputs, so each segment is generated sentence by sentence and glued with
short pauses. Every sentence is checked (speaking rate, long silences, clipping) and regenerated
with another seed when it looks wrong. Levels are matched across the whole lesson.
"""
import json
import os
import re
import sys
from pathlib import Path

os.environ['HF_HUB_DISABLE_IMPLICIT_TOKEN'] = '1'

import numpy as np
import soundfile as sf

MODEL = 'mlx-community/orpheus-3b-0.1-ft-4bit'
GAP = 0.28            # pause between sentences, s
TARGET_RMS = -21.0    # dBFS of speech
MAX_SILENCE = 0.75    # longest allowed quiet span inside a sentence, s
SEED = int(os.environ.get("ORPHEUS_SEED", 420))   # change to get a different take
WPS = (1.6, 3.6)      # plausible words per second


def sentences(text):
    parts = re.split(r'(?<=[.?!])\s+(?=[A-Z"\'(])', text.strip())
    out = []
    for p in parts:       # very short pieces sound clipped on their own: glue to the previous one
        if out and len(p.split()) <= 2:
            out[-1] += ' ' + p
        else:
            out.append(p)
    return out


def trim(x, rate, keep=0.06):
    loud = np.flatnonzero(np.abs(x) > 0.02 * np.abs(x).max())
    if not len(loud):
        return x
    return x[max(0, loud[0] - int(keep * rate)):loud[-1] + int(keep * rate)]


def longest_silence(x, rate):
    win = int(0.02 * rate)
    n = len(x) // win
    if n == 0:
        return 0.0
    frames = x[:n * win].reshape(n, win)
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-9)
    quiet = db < db.max() - 38
    best = run = 0
    for q in quiet:
        run = run + 1 if q else 0
        best = max(best, run)
    return best * 0.02


def problems(x, rate, text):
    dur = len(x) / rate
    words = len(text.split())
    out = []
    if not (WPS[0] <= words / dur <= WPS[1]):
        out.append(f'rate {words / dur:.2f} w/s')
    s = longest_silence(x, rate)
    if s > MAX_SILENCE:
        out.append(f'silence {s:.2f}s')
    return out


def main():
    folder = Path(sys.argv[1]).resolve()
    only = set(sys.argv[2:])
    sys.path.insert(0, str(folder))
    import importlib.util
    spec = importlib.util.spec_from_file_location('script', folder / 'script.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    voice = getattr(mod, 'VOICE', 'tara')
    out = folder / 'audio'
    out.mkdir(exist_ok=True)
    dur_path = out / 'durations.json'
    durations = json.load(open(dur_path)) if only and dur_path.exists() else {}

    import mlx.core as mx
    mx.set_cache_limit(128 * 1024 ** 2)
    from mlx_audio.tts.utils import load_model
    model = load_model(MODEL)

    def say(text, seed):
        mx.random.seed(seed)
        pieces = list(model.generate(text, voice=voice, temperature=0.60, top_p=0.90,
                                     repetition_penalty=1.15, max_tokens=3500, verbose=False))
        return np.concatenate([np.asarray(p.audio).reshape(-1) for p in pieces]).astype(np.float32), pieces[0].sample_rate

    log = []
    for key, text in mod.SEGMENTS:
        if only and key not in only:
            continue
        clips, rate = [], 24000
        for i, sent in enumerate(sentences(text)):
            best = None
            for attempt in range(4):
                x, rate = say(sent, SEED + 97 * attempt + i)
                x = trim(x, rate)
                bad = problems(x, rate, sent)
                if best is None or len(bad) < len(best[1]):
                    best = (x, bad)
                if not bad:
                    break
                print(f'  retry {key}[{i}] ({", ".join(bad)})', flush=True)
            if best[1]:
                log.append(f'{key}[{i}]: {", ".join(best[1])}: {sent}')
            if clips:
                clips.append(np.zeros(int(GAP * rate), np.float32))
            clips.append(best[0])
        wave = np.concatenate(clips)
        rms = np.sqrt((wave ** 2).mean())
        gain = 10 ** (TARGET_RMS / 20) / rms
        gain = min(gain, 0.97 / np.abs(wave).max())
        sf.write(out / f'{key}.wav', wave * gain, rate, subtype='PCM_16')
        durations[key] = round(len(wave) / rate, 3)
        print(f'{key}: {durations[key]:6.2f}s  {text[:60]}', flush=True)
        json.dump(durations, open(dur_path, 'w'), indent=1)
    print(f'speech {sum(durations.values()) / 60:.2f} min')
    if log:
        print('STILL FLAGGED:\n' + '\n'.join(log))


if __name__ == '__main__':
    main()
