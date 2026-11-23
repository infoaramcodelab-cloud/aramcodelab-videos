"""Shared helpers: environment for Manim (LaTeX, ffmpeg), Kokoro voice, narrated scenes, final audio mix.

Workflow for a video folder X/:
  1. X/script.py defines SEGMENTS = [(key, narration_text), ...]
  2. python lib/narrate.py voice X        -> X/audio/<key>.wav, X/audio/durations.json
  3. manim (in X/) scenes.py Video        -> the scene writes X/audio/cues.json (start time of each segment)
  4. python lib/narrate.py mux X in.mp4 out.mp4  -> mixes the voice at the cue times onto the render

Manim's own add_sound mixing dropped whole segments (gaps of 10-20 s), so the audio is mixed here with ffmpeg.
"""
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.environ['PATH'] = os.pathsep.join([os.path.expanduser('~/Library/TinyTeX/bin/universal-darwin'),
                                      '/opt/homebrew/bin', os.environ.get('PATH', '')])
VOICE = 'am_puck'
SPEED = 1.0
PAUSE = 0.3             # breath after each segment, seconds


def load_script(folder):
    import importlib.util
    sys.path.insert(0, folder)
    spec = importlib.util.spec_from_file_location('script', os.path.join(folder, 'script.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def trim(samples, rate, keep=0.08):
    """Cut the silence Kokoro leaves before and after a clip (up to ~0.8 s), keeping `keep` seconds."""
    import numpy as np
    loud = np.nonzero(np.abs(samples) > 0.01 * np.abs(samples).max())[0]
    if not len(loud):
        return samples
    a = max(0, loud[0] - int(keep * rate))
    b = min(len(samples), loud[-1] + int(keep * rate))
    return samples[a:b]


def make_voice(folder):
    import soundfile as sf
    from kokoro_onnx import Kokoro
    mod = load_script(folder)
    out = os.path.join(folder, 'audio')
    os.makedirs(out, exist_ok=True)
    k = Kokoro(os.path.join(ROOT, 'models', 'kokoro-v1.0.onnx'), os.path.join(ROOT, 'models', 'voices-v1.0.bin'))
    durations, words = {}, 0
    for key, text in mod.SEGMENTS:
        samples, rate = k.create(text, voice=getattr(mod, 'VOICE', VOICE), speed=getattr(mod, 'SPEED', SPEED), lang='en-us')
        samples = trim(samples, rate)
        sf.write(os.path.join(out, key + '.wav'), samples, rate)
        durations[key] = round(len(samples) / rate, 3)
        words += len(text.split())
        print(f'{key}: {durations[key]:6.2f}s  {text[:60]}')
    json.dump(durations, open(os.path.join(out, 'durations.json'), 'w'), indent=1)
    print(f'speech {sum(durations.values()) / 60:.2f} min, {words} words')


def mux(folder, video, out):
    cues = json.load(open(os.path.join(folder, 'audio', 'cues.json')))
    keys = sorted(cues, key=cues.get)
    cmd = ['ffmpeg', '-y', '-loglevel', 'error', '-i', video]
    for k in keys:
        cmd += ['-i', os.path.join(folder, 'audio', k + '.wav')]
    parts = [f'[{i + 1}:a]aresample=48000,adelay={int(cues[k] * 1000)}:all=1[a{i}]' for i, k in enumerate(keys)]
    mix = ''.join(f'[a{i}]' for i in range(len(keys))) + f'amix=inputs={len(keys)}:normalize=0:dropout_transition=0[m]'
    cmd += ['-filter_complex', ';'.join(parts + [mix]), '-map', '0:v', '-map', '[m]',
            '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k', '-ar', '48000', out]
    subprocess.run(cmd, check=True)
    print('wrote', out)


try:
    from manim import Scene

    class Narrated(Scene):
        """`with self.seg('key') as g:` marks where the segment's narration starts and waits until it ends.
        g.left() = seconds of narration still to come (to fit animations to the voice)."""
        folder = None

        def seg(self, key):
            scene = self
            durations = json.load(open(os.path.join(self.folder, 'audio', 'durations.json')))
            if not hasattr(self, '_cues'):
                self._cues = {}

            class _Seg:
                def __enter__(self):
                    self.t0 = scene.renderer.time
                    self.dur = durations[key]
                    scene._cues[key] = round(self.t0, 3)
                    json.dump(scene._cues, open(os.path.join(scene.folder, 'audio', 'cues.json'), 'w'), indent=1)
                    return self

                def left(self):
                    return max(0.0, self.dur - (scene.renderer.time - self.t0))

                def __exit__(self, *exc):
                    rest = self.dur + PAUSE - (scene.renderer.time - self.t0)
                    if rest > 0.02:
                        scene.wait(rest)
            return _Seg()
except ImportError:       # voice generation and mux do not need Manim
    pass


if __name__ == '__main__':
    if sys.argv[1] == 'voice':
        make_voice(os.path.abspath(sys.argv[2]))
    elif sys.argv[1] == 'mux':
        mux(os.path.abspath(sys.argv[2]), sys.argv[3], sys.argv[4])
