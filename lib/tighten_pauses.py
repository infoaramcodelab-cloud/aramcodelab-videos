"""Shorten unnaturally long pauses inside narration clips and update durations.json.

    python lib/tighten_pauses.py X [max_pause=0.9] [keep=0.7]

Any quiet span longer than max_pause seconds (40 dB below the clip's loudest 20 ms frame)
is cut down to `keep` seconds, taking the middle out so the breath edges stay. Run it after
generating the voice and before rendering, because scene timing reads durations.json.
"""
import json
import os
import runpy
import sys

import numpy as np
import soundfile as sf


def tighten(x, rate, max_pause, keep):
    win = int(0.02 * rate)
    n = len(x) // win
    db = 20 * np.log10(np.sqrt((x[:n * win].reshape(n, win) ** 2).mean(1)) + 1e-9)
    quiet = db < db.max() - 40
    cuts, i = [], 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            if (j - i) * 0.02 > max_pause:
                a, b = i * win, j * win
                half = int(keep * rate / 2)
                cuts.append((a + half, b - half))
            i = j
        else:
            i += 1
    if not cuts:
        return x, 0.0
    parts, last = [], 0
    fade = int(0.01 * rate)
    for a, b in cuts:
        seg = x[last:a].copy()
        if len(seg) > fade:
            seg[-fade:] *= np.linspace(1, 0, fade)
        parts.append(seg)
        last = b
    parts.append(x[last:])
    y = np.concatenate(parts)
    return y, (len(x) - len(y)) / rate


def main():
    folder = os.path.abspath(sys.argv[1])
    max_pause = float(sys.argv[2]) if len(sys.argv) > 2 else 0.9
    keep = float(sys.argv[3]) if len(sys.argv) > 3 else 0.7
    keys = [k for k, _ in runpy.run_path(os.path.join(folder, 'script.py'))['SEGMENTS']]
    dpath = os.path.join(folder, 'audio', 'durations.json')
    durations = json.load(open(dpath))
    total = 0.0
    for key in keys:
        path = os.path.join(folder, 'audio', key + '.wav')
        x, rate = sf.read(path, dtype='float32')
        y, saved = tighten(x, rate, max_pause, keep)
        if saved:
            sf.write(path, y, rate, subtype='PCM_16')
            print(f'{key:22s} -{saved:4.2f}s')
            total += saved
        durations[key] = round(len(y) / rate, 3)
    json.dump(durations, open(dpath, 'w'), indent=1)
    print(f'saved {total:.1f}s; speech now {sum(durations.values()) / 60:.2f} min')


if __name__ == '__main__':
    main()
