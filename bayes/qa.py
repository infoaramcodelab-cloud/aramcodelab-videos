"""Review rendered narration endpoints and flag any unexpected audio gap.

Run from the project root: .venv/bin/python bayes/qa.py PATH_TO_MUXED_VIDEO
Optional --youtube writes timestamps for the supplied render.
"""

import argparse
import io
import json
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from script import SEGMENTS


HERE = Path(__file__).resolve().parent
CHAPTERS = {
    'cold1': 'A positive result, a fifty-fifty chance',
    'puzzle1': 'The puzzle: guess the false alarms',
    'experiment1': 'The experiment: 10,000 people',
    'count1': 'Why: count the positives',
    'area1': 'Bayes’ rule from the picture',
    'code1': 'Code Lab: check it in Python',
    'meaning1': 'What it means: the base rate',
    'challenge1': 'Challenge: a rarer condition',
}
# These pauses hold an image the viewer needs time to read or reason about.
PAUSES = {
    'cold2': 'title',
    'puzzle2': 'pause and think',
    'experiment2': 'inspect the trial tally',
    'count3': 'compare denominators',
    'area3': 'read the equation',
    'code2': 'read the code and output',
    'meaning3': 'read the note',
    'challenge1': 'try the challenge',
    'challenge2': 'end card',
}


def inspect_frames(video, cues, durations):
    directory = HERE / 'media' / 'qa' / video.stem
    directory.mkdir(parents=True, exist_ok=True)
    width, height, caption = 528, 297, 30
    font = ImageFont.load_default(size=16)
    for offset in range(0, len(SEGMENTS), 5):
        sheet = Image.new('RGB', (3 * width, 2 * (height + caption)), '#111418')
        draw = ImageDraw.Draw(sheet)
        for index, (key, _) in enumerate(SEGMENTS[offset:offset + 5]):
            timestamp = cues[key] + durations[key] - 0.045
            frame = subprocess.check_output([
                'ffmpeg', '-hide_banner', '-loglevel', 'error', '-ss', f'{timestamp:.3f}',
                '-i', str(video), '-frames:v', '1', '-vf', f'scale={width}:{height}',
                '-f', 'image2pipe', '-vcodec', 'png', '-',
            ])
            column, row = index % 3, index // 3
            x, y = width * column, (height + caption) * row
            with Image.open(io.BytesIO(frame)) as image:
                sheet.paste(image, (x, y))
            label = f'{offset + index + 1:02d}  {key}   {timestamp:.2f}s'
            draw.text((x + 10, y + height + 4), label, font=font, fill='#f3f4f6')
        path = directory / f'contact-{offset // 5 + 1}.png'
        sheet.save(path)
        print(path)


def check_audio(video, cues, durations):
    length_arg = subprocess.check_output([
        'ffprobe', '-v', 'error', '-show_entries', 'format=duration',
        '-of', 'default=noprint_wrappers=1:nokey=1', str(video),
    ], text=True).strip()
    video_length = float(length_arg)
    # The shared mux ends the audio track with the last speech clip; pad for
    # analysis so the detector also accounts for a silent end card.
    result = subprocess.run([
        'ffmpeg', '-hide_banner', '-nostats', '-i', str(video), '-vn',
        '-af', f'apad,atrim=duration={length_arg},silencedetect=noise=-40dB:d=1.2',
        '-f', 'null', '-',
    ], capture_output=True, text=True, check=True)
    pattern = r'silence_end: ([\d.]+)\s+\| silence_duration: ([\d.]+)'
    keys = [key for key, _ in SEGMENTS]
    pauses = {}
    for index, key in enumerate(keys):
        if key in PAUSES:
            tail = cues[key] + durations[key]
            resume = cues[keys[index + 1]] if index + 1 < len(keys) else video_length
            pauses[key] = tail, resume
    unexpected = []
    for end, length in re.findall(pattern, result.stderr):
        end, length = float(end), float(length)
        start = end - length
        key = next((key for key, (low, high) in pauses.items()
                    if low - 0.28 <= start <= end <= high + 0.28), None)
        label = PAUSES[key] if key else 'UNEXPECTED'
        print(f'{start:7.3f}–{end:7.3f}  {length:5.3f}s  {label}')
        if key is None:
            unexpected.append((start, end))
    if unexpected:
        raise SystemExit(f'{len(unexpected)} unexpected silence(s) over 1.2 seconds')
    print('Audio check passed')


def write_youtube(cues):
    chapters = []
    for key, title in CHAPTERS.items():
        minutes, seconds = divmod(int(cues[key]), 60)
        chapters.append(f'{minutes}:{seconds:02d} {title}')
    (HERE / 'youtube.txt').write_text(
        'TITLE\nA Positive Test: Am I Ill? | Bayes’ Rule\n\n'
        'DESCRIPTION\n'
        'A hypothetical test catches 99% of people with a condition. Why can a positive '
        'result still mean a 50% chance of having it? We test a simulated crowd, count '
        'two kinds of positive results, turn the picture into Bayes’ rule, and check it '
        'with ten lines of Python. The example is about mathematics, not diagnosis.\n\n'
        'Chapters\n' + '\n'.join(chapters) +
        '\n\nRead the worked example and find the challenge answer on Aram Code Lab:\n'
        'https://aramcodelab.pythonanywhere.com/articles/positive-test-am-i-ill/\n\n'
        'Challenge: The test stays the same, but the condition affects 0.1% of the tested '
        'group. Among people with a positive result, how many actually have the condition?\n\n'
        'Animations made with Manim in the AramCodeLab style. '
        'Narration is AI-generated (synthetic voice).\n\n'
        'TAGS\nBayes rule, conditional probability, base rate, false positives, '
        'sensitivity, Python simulation, Manim, math visualization\n',
        encoding='utf-8',
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--youtube', action='store_true')
    args = parser.parse_args()
    cues = json.loads((HERE / 'audio' / 'cues.json').read_text())
    durations = json.loads((HERE / 'audio' / 'durations.json').read_text())
    keys = [key for key, _ in SEGMENTS]
    if list(cues) != keys or list(durations) != keys:
        raise SystemExit('Render cues and audio durations must match every narration segment')
    inspect_frames(args.video, cues, durations)
    check_audio(args.video, cues, durations)
    if args.youtube:
        write_youtube(cues)


if __name__ == '__main__':
    main()
