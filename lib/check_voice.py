"""Scan a lesson's narration clips for generation glitches.

    python lib/check_voice.py X

For every segment of X/script.py: speaking rate (words per second), the longest quiet span
inside the clip, and clipping. Prints the flagged keys on the last line, ready to pass to
`lib/orpheus_voice.py X <keys>`.
"""
import os
import runpy
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from orpheus_voice import MAX_SILENCE, WPS, longest_silence  # noqa: E402


def main():
    folder = os.path.abspath(sys.argv[1])
    segs = runpy.run_path(os.path.join(folder, 'script.py'))['SEGMENTS']
    flagged = []
    for key, text in segs:
        x, rate = sf.read(os.path.join(folder, 'audio', key + '.wav'), dtype='float32')
        dur = len(x) / rate
        wps = len(text.split()) / dur
        sil = longest_silence(x, rate)
        clip = np.mean(np.abs(x) > 0.985)
        bad = []
        if not (WPS[0] <= wps <= WPS[1]):
            bad.append(f'rate {wps:.2f}')
        if sil > MAX_SILENCE:
            bad.append(f'silence {sil:.2f}s')
        if clip > 1e-4:
            bad.append('clipping')
        mark = '  <-- ' + ', '.join(bad) if bad else ''
        print(f'{key:22s} {dur:6.2f}s {wps:4.2f} w/s  max quiet {sil:4.2f}s{mark}')
        if bad:
            flagged.append(key)
    print('FLAGGED:', ' '.join(flagged))


if __name__ == '__main__':
    main()
