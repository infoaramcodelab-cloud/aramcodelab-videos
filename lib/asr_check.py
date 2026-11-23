"""Compare every narration clip with its script text using offline Whisper (base).

    python lib/asr_check.py X [key ...]        (pip install openai-whisper)

Prints the word error rate per clip and the differing words for clips above 12 %.
Whisper itself mishears names and symbols ("A B", "Aram Code Lab"), so read the diffs by eye.
"""
import difflib
import os
import re
import runpy
import sys

import whisper

NUM = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four', '5': 'five', '6': 'six',
       '7': 'seven', '8': 'eight', '9': 'nine', '10': 'ten'}


def words(s):
    s = s.lower().replace('-', ' ')
    s = re.sub(r"[^a-z0-9' ]", ' ', s)
    return [NUM.get(w, w) for w in s.split()]


def main():
    folder = os.path.abspath(sys.argv[1])
    only = set(sys.argv[2:])
    segs = runpy.run_path(os.path.join(folder, 'script.py'))['SEGMENTS']
    model = whisper.load_model('base')
    bad = []
    for key, text in segs:
        if only and key not in only:
            continue
        heard = model.transcribe(os.path.join(folder, 'audio', key + '.wav'), language='en',
                                 fp16=False, initial_prompt='Probability, sample space, events, Aram Code Lab.')['text']
        a, b = words(text), words(heard)
        sm = difflib.SequenceMatcher(a=a, b=b)
        err = sum(max(i2 - i1, j2 - j1) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != 'equal')
        wer = err / max(1, len(a))
        print(f'{key:22s} WER {wer:5.1%}', flush=True)
        if wer > 0.12:
            bad.append(key)
            for op, i1, i2, j1, j2 in sm.get_opcodes():
                if op != 'equal':
                    print(f'      script: {" ".join(a[i1:i2])!r:40s} heard: {" ".join(b[j1:j2])!r}')
    print('CHECK BY EAR:', ' '.join(bad))


if __name__ == '__main__':
    main()
