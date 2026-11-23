"""AramCodeLab visual style for videos, taken from the site (myapp/static/css/style.css, dark theme):
near-black background with a soft teal glow, Inter / JetBrains Mono, rounded bordered cards, teal accent."""
import os

import manimpango
import numpy as np
from manim import (DOWN, LEFT, RIGHT, UP, UL, Axes, ImageMobject, RoundedRectangle, Text, VGroup, config)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

BG = '#090a0c'
SURFACE = '#111418'
SURFACE2 = '#161a1f'
BORDER = '#22272e'
BORDER2 = '#30363f'
AXIS = '#5b6370'
TEXT = '#f3f4f6'
TEXT2 = '#c9ced6'
MUTED = '#8b939e'
ACCENT = '#2dd4bf'          # teal
NEXT = '#818cf8'            # indigo
WARN = '#fbbf24'            # amber
SKY = '#7dd3fc'

for f in sorted(os.listdir(os.path.join(ROOT, 'fonts'))):
    if f.endswith('.ttf'):
        manimpango.register_font(os.path.join(ROOT, 'fonts', f))

config.background_color = BG


def background():
    """Full-frame image: --bg with the teal glow the site has at the top of every page."""
    path = os.path.join(ROOT, 'fonts', '..', 'lib', 'bg.png')
    if not os.path.exists(path):
        from PIL import Image
        w, h = 1920, 1080
        y, x = np.mgrid[0:h, 0:w]
        g = 0.16 * np.exp(-(((x - w * 0.5) / (w * 0.42)) ** 2 + ((y + h * 0.15) / (h * 0.42)) ** 2))
        base, teal = np.array([9, 10, 12.0]), np.array([45, 212, 191.0])
        img = base * (1 - g[..., None]) + teal * g[..., None]
        Image.fromarray(np.clip(img, 0, 255).astype('uint8')).save(path)
    im = ImageMobject(path)
    im.height = config.frame_height
    return im


def sans(text, size=30, color=TEXT, weight='NORMAL', **kw):
    return Text(text, font='Inter', font_size=size, color=color, weight=weight, **kw)


def mono(text, size=20, color=MUTED, weight='NORMAL', **kw):
    return Text(text, font='JetBrains Mono', font_size=size, color=color, weight=weight, **kw)


def header(num, eyebrow, title):
    """Section header in the style of the site's cards: '01 · EYEBROW' in mono, then a bold title."""
    e = mono(f'{num}  ·  {eyebrow.upper()}', 20, ACCENT)
    t = sans(title, 40, TEXT, 'BOLD')
    g = VGroup(e, t).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    return g.to_corner(UL, buff=0.55)


def card(w, h):
    return RoundedRectangle(width=w, height=h, corner_radius=0.18, fill_color=SURFACE, fill_opacity=0.92,
                            stroke_color=BORDER2, stroke_width=1.5)


def pill(text, color=TEXT2, size=22):
    t = sans(text, size, color, 'MEDIUM')
    r = RoundedRectangle(width=t.width + 0.5, height=t.height + 0.32, corner_radius=0.2, fill_color=SURFACE2,
                         fill_opacity=1, stroke_color=BORDER2, stroke_width=1.5)
    return VGroup(r, t.move_to(r))


def logo(size=22):
    """'AramCodeLab' with 'Code' in the accent colour, as in the site header."""
    a = sans('Aram', size, TEXT, 'BOLD')
    c = sans('Code', size, ACCENT, 'BOLD')
    b = sans('Lab', size, TEXT, 'BOLD')
    return VGroup(a, c, b).arrange(RIGHT, buff=0.02, aligned_edge=DOWN)


def axes(xr, yr, w, h, xt=(), yt=(), fmt=lambda v: f'{v:g}', size=18):
    """Axes with Inter tick labels (Manim's default numbers are in the TeX font)."""
    ax = Axes(x_range=xr, y_range=yr, x_length=w, y_length=h, tips=False,
              axis_config={'color': AXIS, 'stroke_width': 2, 'tick_size': 0.05})
    labs = VGroup()
    for v in xt:
        labs.add(sans(fmt(v), size, MUTED).next_to(ax.c2p(v, yr[0]), DOWN, buff=0.16))
    for v in yt:
        labs.add(sans(fmt(v), size, MUTED).next_to(ax.c2p(xr[0], v), LEFT, buff=0.16))
    return ax, labs
