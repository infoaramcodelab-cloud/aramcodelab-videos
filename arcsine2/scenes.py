"""The Arc Sine Law — flagship version (script: SCRIPT.md, narration: script.py).
Render (in this folder): manim -qp --disable_caching scenes.py Video; then lib/narrate.py mux."""
import math
import os
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, '..', 'lib'))

import numpy as np
from manim import *

import data2 as D
from brand import (ACCENT, BORDER2, MUTED, NEXT, SKY, SURFACE, SURFACE2, TEXT, TEXT2, WARN, axes, background,
                   card, header, logo, mono, pill, sans)
from narrate import Narrated

ALICE, BOB, HI = ACCENT, NEXT, WARN


# ---------------------------------------------------------------------- helpers
def tex(s, size=44, color=TEXT):
    return MathTex(s, font_size=size, color=color)


def runs(ax, s, width=3.5, t0=0):
    """The walk split into pieces above / below the axis, coloured by who leads."""
    s = np.asarray(s)
    side = np.where(np.maximum(s[:-1], s[1:]) > 0, 1, -1)
    pieces, start = [], 0
    for i in range(1, len(side) + 1):
        if i == len(side) or side[i] != side[start]:
            pts = [ax.c2p(t0 + j, s[j]) for j in range(start, i + 1)]
            pieces.append(VMobject(stroke_width=width, color=ALICE if side[start] > 0 else BOB)
                          .set_points_as_corners(pts))
            start = i
    return VGroup(*pieces)


def polyline(ax, pts, color=TEXT, width=4):
    return VMobject(stroke_width=width, color=color).set_points_as_corners([ax.c2p(x, y) for x, y in pts])


def lattice(ax, xs, ys, op=0.22):
    return VGroup(*[Dot(ax.c2p(x, y), radius=0.022, color=MUTED, fill_opacity=op) for x in xs for y in ys])


def in_card(w, h, *mobs, shift=ORIGIN):
    c = card(w, h)
    g = VGroup(*mobs)
    g.move_to(c).shift(shift)
    return c, g


def bar_group(ax, xs, hs, width, color=ALICE, top=None, op=0.88):
    out = VGroup()
    for x, h in zip(xs, hs):
        h = min(h, top) if top else h
        h = max(h, 1e-3)
        a, b = max(x - width / 2, ax.x_range[0]), min(x + width / 2, ax.x_range[1])
        out.add(Polygon(ax.c2p(a, 0), ax.c2p(b, 0), ax.c2p(b, h), ax.c2p(a, h),
                        stroke_width=1.2, stroke_color=SURFACE, fill_color=color, fill_opacity=op))
    return out


CODE = '''import random

def lead_fraction(n=1000):
    s, ahead = 0, 0
    for _ in range(n):
        prev = s
        s += random.choice((-1, 1))
        ahead += max(prev, s) > 0
    return ahead / n

fracs = [lead_fraction() for _ in range(10_000)]
print(sum(f > 0.9 or f < 0.1 for f in fracs) / 10_000)'''


def code_lines(src, size=24):
    """Python source -> one MarkupText per line, coloured with pygments tokens in the site palette."""
    from pygments.lexers import PythonLexer
    from pygments.token import Comment, Keyword, Name, Number, Operator, String
    colours = [(Keyword, NEXT), (Name.Builtin, ACCENT), (Name.Function, SKY), (Number, WARN), (String, '#86efac'),
               (Comment, MUTED), (Operator, TEXT2)]
    lex = PythonLexer()
    probe = Text('M' * 20, font='JetBrains Mono', font_size=size)
    cw = probe.width / 20
    lh = Text('Mg', font='JetBrains Mono', font_size=size).height * 1.55
    out = VGroup()
    for i, line in enumerate(src.split('\n')):
        body = line.lstrip(' ')
        indent = len(line) - len(body)
        y = -i * lh
        if not body:
            out.add(Dot(radius=0.001, fill_opacity=0).move_to([0, y, 0]))
            continue
        markup = ''
        for tok, val in lex.get_tokens(body):
            val = val.rstrip('\n')
            if not val:
                continue
            col = next((c for t, c in colours if tok in t), TEXT)
            markup += f'<span foreground="{col}">{escape(val)}</span>'
        m = MarkupText(markup, font='JetBrains Mono', font_size=size)
        m.move_to([indent * cw, y, 0], aligned_edge=LEFT)
        out.add(m)
    return out


class Video(Narrated):
    folder = HERE

    def setup(self):
        self.add(background())
        self.mark = logo(20).set_opacity(0.8).to_corner(DR, buff=0.3).set_z_index(10)
        self.add(self.mark)
        self.fixed = set(self.mobjects)

    def hold(self, t):
        if t > 0.03:
            self.wait(t)

    def clear_all(self, t=0.45):
        out = [m for m in self.mobjects if m not in self.fixed]
        if out:
            self.play(*[FadeOut(m) for m in out], run_time=t)

    def construct(self):
        self.cold_open()
        self.puzzle()
        self.experiment()
        self.reflection()
        self.telescope()
        self.last_tie()
        self.bars_to_curve()
        self.code_lab()
        self.meaning()
        self.challenge()

    # ================================================================== 1. cold open
    def grid_cells(self):
        cells, lop = VGroup(), []
        for s, f in zip(D.GRID, D.GRID_FRAC):
            m = max(abs(s.min()), abs(s.max()), 5)
            ax = Axes(x_range=[0, D.N, D.N], y_range=[-m, m, m], x_length=2.6, y_length=1.35, tips=False,
                      axis_config={'color': BORDER2, 'stroke_width': 1.5, 'include_ticks': False})
            pieces = runs(ax, s, 2.4)
            pct = sans(f'Alice {round(100 * f)}%', 20, ALICE if f >= 0.5 else BOB, 'SEMIBOLD').next_to(ax, UP, buff=0.12)
            inner = VGroup(ax, pieces, pct)
            box = card(inner.width + 0.4, inner.height + 0.35).move_to(inner)
            cells.add(VGroup(box, ax, pieces, pct))
            lop.append(max(f, 1 - f) >= 0.8)
        cells.arrange_in_grid(2, 4, buff=(0.3, 0.3)).move_to(UP * 0.35)
        return cells, lop

    def cold_open(self):
        cells, lop = self.grid_cells()
        with self.seg('c1') as g:
            self.play(LaggedStart(*[FadeIn(VGroup(c[0], c[1], c[3])) for c in cells], lag_ratio=0.12),
                      LaggedStart(*[Create(c[2]) for c in cells], lag_ratio=0.12), run_time=max(3, g.left() - 0.2))
        with self.seg('c2'):
            note = pill(f'{D.GRID_LOPSIDED} of 8: one player ahead ≥ 80% of the time', HI, 26).next_to(cells, DOWN, buff=0.45)
            self.play(*[c[0].animate.set_stroke(HI, width=3) for c, l in zip(cells, lop) if l], FadeIn(note, shift=UP * 0.15), run_time=1)
        bi = int(np.argmin(D.GRID_FRAC))
        others = VGroup(*[c for i, c in enumerate(cells) if i != bi])
        with self.seg('c3'):
            lab = pill(f'Bob ahead for all {D.N} tosses', BOB, 26).next_to(cells, DOWN, buff=0.45)
            self.play(others.animate.set_opacity(0.2), cells[bi][0].animate.set_stroke(BOB, width=4),
                      FadeOut(note), FadeIn(lab, shift=UP * 0.15), run_time=1)
        with self.seg('c4') as g:
            self.hold(g.left() - 2.3)
            self.play(FadeOut(VGroup(cells, lab)), run_time=0.5)
            eb = mono('PROBABILITY  ·  RANDOM WALKS', 22, ACCENT)
            title = sans('The Arc Sine Law', 80, TEXT, 'BOLD')
            sub = sans('why fair games are so unfair', 34, MUTED)
            t = VGroup(eb, title, sub).arrange(DOWN, buff=0.35)
            self.play(FadeIn(eb, shift=DOWN * 0.15), Write(title), FadeIn(sub, shift=UP * 0.15), run_time=1.5)
        self.wait(1.6)
        self.play(FadeOut(t), run_time=0.5)

    # ================================================================== 2. the puzzle
    def puzzle(self):
        h = header('01', 'the puzzle', 'A fair coin, two players')
        with self.seg('p1') as g:
            a = [Dot(color=ALICE, radius=0.13), sans('Alice', 38, ALICE, 'BOLD'), sans('heads  →  +1 point', 34, TEXT2)]
            b = [Dot(color=BOB, radius=0.13), sans('Bob', 38, BOB, 'BOLD'), sans('tails  →  +1 point', 34, TEXT2)]
            rows = VGroup(*a, *b).arrange_in_grid(2, 3, buff=(0.35, 0.5), col_alignments='cll')
            c = card(rows.width + 1.2, rows.height + 1).move_to(rows)
            coin = VGroup(Circle(radius=0.62, fill_color=SURFACE2, fill_opacity=1, stroke_color=HI, stroke_width=4),
                          sans('H', 40, HI, 'BOLD'))
            grp = VGroup(VGroup(c, rows), coin).arrange(RIGHT, buff=1.2).move_to(DOWN * 0.3)
            self.play(FadeIn(h), FadeIn(c), FadeIn(rows[:3], shift=RIGHT * 0.3), run_time=0.8)
            self.play(FadeIn(rows[3:], shift=RIGHT * 0.3), FadeIn(coin), run_time=0.6)
            for face, col in (('T', BOB), ('H', ALICE), ('T', BOB)):
                if g.left() < 1.2:
                    break
                self.play(coin.animate.stretch(0.05, 0), run_time=0.18)
                new = sans(face, 40, col, 'BOLD').move_to(coin[1]).stretch(0.05, 0)
                coin[1].become(new)
                coin[0].set_stroke(col)
                self.play(coin.animate.stretch(20, 0), run_time=0.18)
                self.wait(0.25)
        s = D.PUZZLE
        m = int(max(abs(s.min()), abs(s.max()))) + 1
        ax, labs = axes([0, 60, 10], [-m, m, 2], 11.6, 4.0, xt=range(0, 61, 10), yt=(-m, 0, m))
        cd, _ = in_card(12.6, 5.0, ax, labs, shift=RIGHT * 0.2 + UP * 0.1)
        VGroup(cd, ax, labs).move_to(DOWN * 0.5)
        pieces = runs(ax, s, 4)
        with self.seg('p2') as g:
            self.play(FadeOut(VGroup(c, rows, coin)), FadeIn(cd), Create(ax), FadeIn(labs), run_time=0.8)
            lens = [len(p.get_anchors()) / 2 for p in pieces]
            total = max(3.0, g.left() - 2.2)
            self.play(Succession(*[Create(p, rate_func=linear, run_time=total * l / sum(lens)) for p, l in zip(pieces, lens)]))
            up = sans('Alice ahead', 26, ALICE, 'SEMIBOLD').move_to(ax.c2p(20, m * 0.75))
            down = sans('Bob ahead', 26, BOB, 'SEMIBOLD').move_to(ax.c2p(55, -m * 0.75))
            self.play(FadeIn(up), run_time=0.5)
            self.play(FadeIn(down), run_time=0.5)
        game = VGroup(cd, ax, labs, pieces, up, down)
        with self.seg('p3') as g:
            self.play(game.animate.scale(0.42).to_corner(UR, buff=0.5).shift(DOWN * 0.15), run_time=0.8)
            opts = VGroup()
            shapes = [lambda x: 0.85 * math.exp(-((x - 0.5) / 0.17) ** 2) + 0.05, lambda x: 0.45,
                      lambda x: min(0.95, 0.09 / math.sqrt(max(x * (1 - x), 1e-4)))]
            names = ['a hill', 'flat', 'a valley']
            for k, (f, nm) in enumerate(zip(shapes, names)):
                a2 = Axes(x_range=[0, 1, 1], y_range=[0, 1, 1], x_length=2.8, y_length=1.5, tips=False,
                          axis_config={'color': BORDER2, 'stroke_width': 1.5, 'include_ticks': False})
                cv = a2.plot(f, x_range=[0.005, 0.995, 0.005], color=TEXT, stroke_width=3.5)
                letter = mono('ABC'[k], 26, HI, 'SEMIBOLD')
                cap = sans(nm, 24, TEXT2)
                top = VGroup(letter, cap).arrange(RIGHT, buff=0.25)
                body = VGroup(top, VGroup(a2, cv)).arrange(DOWN, buff=0.3)
                box = card(body.width + 0.6, body.height + 0.5).move_to(body)
                opts.add(VGroup(box, body))
            opts.arrange(RIGHT, buff=0.45).move_to(DOWN * 1.2)
            self.hold(g.left() - 4.6)
            for o in opts:
                self.play(FadeIn(o, shift=UP * 0.2), run_time=0.6)
                self.wait(0.5)
        with self.seg('p4'):
            tr = ValueTracker(0.001)
            ring_bg = Circle(radius=0.42, stroke_color=BORDER2, stroke_width=6).next_to(opts, UP, buff=0.4)
            ring = always_redraw(lambda: Arc(radius=0.42, start_angle=PI / 2, angle=-TAU * tr.get_value(),
                                             stroke_color=HI, stroke_width=6).move_arc_center_to(ring_bg.get_center()))
            think = mono('PAUSE AND THINK', 20, HI).next_to(ring_bg, LEFT, buff=0.35)
            self.add(ring_bg, ring)
            self.play(FadeIn(think), run_time=0.3)
            self.play(tr.animate.set_value(1), run_time=3.2, rate_func=linear)
            self.remove(ring)
            self.play(FadeOut(VGroup(ring_bg, think)), run_time=0.3)
        with self.seg('p5'):
            guess = pill("most people's guess", HI, 24).next_to(opts[0], DOWN, buff=0.25)
            self.play(opts[0][0].animate.set_stroke(HI, width=3), FadeIn(guess, shift=UP * 0.1), run_time=0.8)
        self.clear_all()

    # ================================================================== 3. the experiment
    def experiment(self):
        h = header('02', 'the experiment', "Let's play")
        ax, labs = axes([0, 1, 0.05], [0, 1, 1], 10.2, 3.6, xt=(0, 0.25, 0.5, 0.75, 1))
        ax.y_axis.set_opacity(0)
        cap = sans('fraction of time Alice leads', 22, MUTED).next_to(ax.x_axis, DOWN, buff=0.55)
        hc, _ = in_card(11.4, 4.75, ax, labs, cap, shift=UP * 0.1)
        VGroup(hc, ax, labs, cap).move_to(DOWN * 1.25)
        # small card with the current game
        gax = Axes(x_range=[0, D.N, D.N], y_range=[-60, 60, 60], x_length=3.6, y_length=1.0, tips=False,
                   axis_config={'color': BORDER2, 'stroke_width': 1.5, 'include_ticks': False})
        gc = card(4.2, 1.45)
        gc.to_edge(UP, buff=0.5).to_edge(RIGHT, buff=0.6)
        gax.move_to(gc)
        counter = pill('0 games', TEXT2, 24).next_to(gc, LEFT, buff=0.3)
        bins = 20
        xs = [(i + 0.5) / bins for i in range(bins)]

        def hist(nm):
            c = np.histogram(D.FRACS[:nm], bins=bins, range=(0, 1))[0]
            return c

        def bars_for(c):
            mx = max(c.max(), 1)
            return bar_group(ax, xs, c / mx * 0.92, 1 / bins)

        counts = np.zeros(bins, dtype=int)
        bars = bars_for(counts)
        with self.seg('e1') as g:
            self.play(FadeIn(h), FadeIn(hc), Create(ax), FadeIn(labs), FadeIn(cap), FadeIn(gc), FadeIn(gax), FadeIn(counter), run_time=1)
            self.add(bars)
            self.hold(min(1.5, g.left() - 9))
            for i in range(10):
                s = D._S[i]
                m = max(abs(int(s.min())), abs(int(s.max())), 10)
                gpath = runs(gax, s[::4] * (60 / m), 2.2)
                for p in gpath:   # x positions were made for every 4th step
                    p.stretch_about_point(4, 0, gax.c2p(0, 0))
                self.play(Create(gpath), run_time=0.28, rate_func=linear)
                f = D.FRACS[i]
                b = min(int(f * bins), bins - 1)
                dot = Dot(gax.get_center(), radius=0.09, color=HI)
                counts[b] += 1
                new = bars_for(counts)
                self.play(dot.animate.move_to(new[b].get_top() + UP * 0.08), run_time=0.26, rate_func=rush_into)
                self.remove(dot)
                self.remove(gpath)
                bars.become(new)
                counter.become(pill(f'{i + 1} game' + ('s' if i else ''), TEXT2, 24).move_to(counter, aligned_edge=RIGHT))
                self.wait(0.05)
        with self.seg('e2') as g:
            self.play(FadeOut(VGroup(gc, gax)), run_time=0.5)
            self.wait(0.2)
            for nm, label in ((100, '100 games'), (10000, '10,000 games')):
                self.play(Transform(bars, bars_for(hist(nm))),
                          Transform(counter, pill(label, TEXT2, 24).move_to(counter, aligned_edge=RIGHT)), run_time=0.8)
                self.wait(0.35)
        with self.seg('e3') as g:
            hill = DashedVMobject(ax.plot(lambda x: 0.62 * math.exp(-((x - 0.5) / 0.17) ** 2) + 0.02, x_range=[0, 1],
                                          color=MUTED, stroke_width=3), num_dashes=45)
            hl = sans('the hill we expected', 22, MUTED).move_to(ax.c2p(0.5, 0.78))
            self.play(Create(hill), FadeIn(hl), run_time=1)
            self.hold(min(1.5, g.left() - 4))
            self.play(FadeOut(hill), FadeOut(hl), run_time=0.5)
            ends = VGroup(bars[0], bars[-1])
            self.play(ends.animate.set_fill(HI), run_time=0.5)
            self.play(Indicate(ends, color=HI, scale_factor=1.04), run_time=max(0.8, min(1.5, g.left() - 0.3)))
        with self.seg('e4'):
            mid = VGroup(*bars[8:12])
            self.play(ends.animate.set_fill(ALICE), mid.animate.set_fill(HI), run_time=0.6)
            t1 = pill(f'between 40% and 60%:  ≈ {round(100 * D.TH_40_60)}%', HI, 26).move_to(ax.c2p(0.5, 0.75))
            self.play(FadeIn(t1, shift=UP * 0.1), run_time=0.6)
        with self.seg('e5'):
            ext = VGroup(*bars[:2], *bars[-2:])
            self.play(mid.animate.set_fill(ALICE), ext.animate.set_fill(HI), FadeOut(t1), run_time=0.6)
            t2 = pill(f'someone ahead > 90% of the time:  ≈ {round(100 * D.TH_OVER_90)}%', HI, 26).move_to(ax.c2p(0.5, 0.75))
            self.play(FadeIn(t2, shift=UP * 0.1), run_time=0.6)
        with self.seg('e6'):
            self.clear_all(0.4)
            q = sans('Why?', 72, TEXT, 'BOLD')
            q2 = sans('one beautiful trick', 34, ACCENT)
            VGroup(q, q2).arrange(DOWN, buff=0.35)
            self.play(Write(q), run_time=0.6)
            self.play(FadeIn(q2, shift=UP * 0.15), run_time=0.6)
        self.clear_all()

    # ================================================================== 4a. reflection
    def reflection(self):
        h = header('03', 'why', 'The reflection trick')
        ax, labs = axes([0, 13, 1], [-4, 5, 1], 10.8, 4.3, xt=(), yt=(0,))
        ax.x_axis.set_stroke(TEXT2, width=2.5)
        lat = lattice(ax, range(0, 14), range(-4, 6))
        cd, _ = in_card(12.2, 5.2, ax, labs, lat, shift=RIGHT * 0.15)
        VGroup(cd, ax, labs, lat).move_to(DOWN * 0.55)
        pts = list(enumerate(D.REFL))
        k = D.REFL.index(0)
        pre = polyline(ax, pts[:k + 1], ALICE, 4.5)
        post = polyline(ax, pts[k:], ALICE, 4.5)
        A = Dot(ax.c2p(0, 2), radius=0.09, color=TEXT)
        B = Dot(ax.c2p(13, D.REFL[-1]), radius=0.09, color=TEXT)
        T = Dot(ax.c2p(k, 0), radius=0.11, color=HI)
        la = tex('A', 36).next_to(A, LEFT, buff=0.3)
        lb = tex('B', 36).next_to(B, RIGHT, buff=0.15)
        lt = sans('first touch', 22, HI).next_to(T, UP, buff=0.4)
        with self.seg('r1') as g:
            self.play(FadeIn(h), FadeIn(cd), Create(ax), FadeIn(labs), FadeIn(lat), run_time=0.8)
            self.play(FadeIn(A), FadeIn(la), run_time=0.3)
            self.play(Create(pre), run_time=1.0, rate_func=linear)
            self.play(Create(post), run_time=1.6, rate_func=linear)
            self.play(FadeIn(B), FadeIn(lb), run_time=0.3)
            self.play(GrowFromCenter(T), FadeIn(lt), run_time=0.5)
        y0 = ax.c2p(0, 0)[1]
        mirror = lambda p: np.array([p[0], 2 * y0 - p[1], p[2]])
        ref = pre.copy().set_color(BOB)
        A2 = Dot(ax.c2p(0, -2), radius=0.09, color=BOB)
        la2 = tex("A'", 36, BOB).next_to(A2, LEFT, buff=0.3)
        with self.seg('r2') as g:
            self.play(pre.animate.set_stroke(opacity=0.3), run_time=0.4)
            self.add(ref)
            self.play(ref.animate.apply_function(mirror), run_time=1.6)
            self.play(FadeIn(A2), FadeIn(la2), run_time=0.4)
            self.play(Indicate(VGroup(ref, post), color=BOB, scale_factor=1.0), run_time=1)
        with self.seg('r3') as g:
            back = ref.copy()
            self.play(ref.animate.apply_function(mirror).set_color(ALICE), run_time=1.3)
            self.play(ref.animate.apply_function(mirror).set_color(BOB), run_time=1.3)
            rule = VGroup(sans('touching paths from A', 26, ALICE, 'SEMIBOLD'), sans('↔', 30, HI, 'BOLD'),
                          sans("all paths from A′", 26, BOB, 'SEMIBOLD')).arrange(RIGHT, buff=0.35)
            box = RoundedRectangle(width=rule.width + 0.7, height=rule.height + 0.4, corner_radius=0.2,
                                   fill_color=SURFACE2, fill_opacity=1, stroke_color=HI, stroke_width=2)
            rr = VGroup(box, rule.move_to(box)).next_to(cd, DOWN, buff=0.2)
            if rr.get_bottom()[1] < -3.85:
                rr.move_to(cd.get_bottom() + UP * 0.45)
            self.hold(g.left() - 4)
            self.play(FadeIn(rr, shift=UP * 0.15), run_time=0.7)
            name = pill('the reflection principle', HI, 24).to_edge(UP, buff=0.6).to_edge(RIGHT, buff=0.55)
            self.play(FadeIn(name), run_time=0.5)
        self.clear_all()

    # ================================================================== 4b. telescope
    def telescope(self):
        h = header('03', 'why', 'Games that never return to zero')
        with self.seg('r4') as g:
            l0 = tex(r'\#\{\text{paths with } S_1 > 0,\ \dots,\ S_{2n} > 0\}', 42)
            l1 = tex(r'= \sum_{r = 2, 4, \dots} \Big[\, N(r - 1) - N(r + 1) \,\Big]', 44)
            note = tex(r'N(j) = \#\{\text{paths of } 2n - 1 \text{ steps from } 0 \text{ to } j\}', 32, MUTED)
            col = VGroup(l0, l1, note).arrange(DOWN, buff=0.45)
            c, _ = in_card(col.width + 1.2, col.height + 1.0, col)
            VGroup(c, col).move_to(DOWN * 0.3)
            self.play(FadeIn(h), FadeIn(c), Write(l0), run_time=1.6)
            self.hold(g.left() - 5.5)
            self.play(Write(l1), run_time=1.6)
            self.play(FadeIn(note), run_time=0.6)
        with self.seg('r5') as g:
            parts = [r'=', r'\big[N(1)', r'-\,N(3)\big]', r'+', r'\big[N(3)', r'-\,N(5)\big]', r'+', r'\big[N(5)',
                     r'-\,N(7)\big]', r'+ \cdots']
            row = MathTex(*parts, font_size=40, color=TEXT)
            if row.width > 11.6:
                row.scale(11.6 / row.width)
            row.move_to(l1)
            wide = card(max(c.width, row.width + 0.9), c.height + 0.5).move_to(c).shift(DOWN * 0.25)
            self.play(FadeOut(note), ReplacementTransform(l1, row), Transform(c, wide), run_time=1)
            pairs = [(2, 4), (5, 7), (8, 9)]
            for a, b in pairs:
                sa = Line(row[a].get_corner(DL), row[a].get_corner(UR), color=HI, stroke_width=4)
                sb = Line(row[b].get_corner(DL), row[b].get_corner(UR), color=HI, stroke_width=4)
                self.play(Create(sa), Create(sb), row[a].animate.set_opacity(0.35), row[b].animate.set_opacity(0.35), run_time=0.6)
            res = tex(r'= N(1) = \binom{2n-1}{n}', 46, HI).next_to(row, DOWN, buff=0.45)
            self.play(Write(res), run_time=1)
        with self.seg('r6') as g:
            self.play(*[FadeOut(m) for m in self.mobjects if m not in self.fixed and m is not h], run_time=0.5)
            f1 = tex(r'P(S_1 > 0, \dots, S_{2n} > 0) = \binom{2n-1}{n} 2^{-2n} = \tfrac12\, u_{2n}', 40)
            f2 = tex(r'P(\text{no return to } 0 \text{ in } 2n \text{ tosses}) = u_{2n}', 48, HI)
            f3 = tex(r'u_{2n} = P(S_{2n} = 0) = \binom{2n}{n} 2^{-2n}', 40, TEXT2)
            col = VGroup(f1, f2, f3).arrange(DOWN, buff=0.55)
            c, _ = in_card(col.width + 1.2, col.height + 1.0, col)
            VGroup(c, col).move_to(DOWN * 0.3)
            box = SurroundingRectangle(f2, color=HI, buff=0.2, corner_radius=0.12, stroke_width=2.5)
            self.play(FadeIn(c), Write(f1), run_time=1.5)
            self.play(Write(f2), Create(box), run_time=1.5)
            self.hold(g.left() - 3.5)
            self.play(Write(f3), run_time=1.2)
        with self.seg('r7') as g:
            self.play(FadeOut(VGroup(c, f1, f2, f3, box)), run_time=0.6)
            ax, labs = axes([0, 50, 10], [0, 0.6, 0.1], 9.4, 3.8, xt=(10, 20, 30, 40, 50), yt=(0.1, 0.3, 0.5))
            c2, _ = in_card(11, 4.9, ax, labs, shift=RIGHT * 0.2 + UP * 0.15)
            VGroup(c2, ax, labs).move_to(DOWN * 0.75)
            xl = tex('m', 34, MUTED).next_to(ax.x_axis, RIGHT, buff=0.15)
            dots = VGroup(*[Dot(ax.c2p(m, D.u(2 * m)), radius=0.055, color=ALICE) for m in range(1, 51)])
            curve = ax.plot(lambda m: 1 / math.sqrt(math.pi * m), x_range=[0.9, 50], color=HI, stroke_width=3.5)
            f = tex(r'u_{2m} \approx \frac{1}{\sqrt{\pi m}}', 50, HI).move_to(ax.c2p(32, 0.42))
            self.play(FadeIn(c2), Create(ax), FadeIn(labs), FadeIn(xl), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.04), run_time=1.6)
            self.play(Create(curve), Write(f), run_time=1.4)
            p = pill(f'after {D.N} tosses:  u ≈ {D.u(D.N):.3f}', HI, 26).move_to(ax.c2p(32, 0.24))
            self.hold(g.left() - 4.5)
            self.play(FadeIn(p, shift=UP * 0.1), run_time=0.6)
        self.clear_all()

    # ================================================================== 5. the last tie
    def last_tie(self):
        h = header('04', 'when was the score last level?', 'The last tie')
        s = D.LAST
        n2, T = len(s) - 1, D.LAST_TIE
        m = int(max(abs(s.min()), abs(s.max()))) + 1
        ax, labs = axes([0, n2, 2], [-m, m, 1], 11.4, 3.7, xt=(0, T, n2), yt=(0,),
                        fmt=lambda v: {0: '0', T: '2k', n2: '2n'}.get(v, f'{v:g}'))
        lat = lattice(ax, range(0, n2 + 1, 2), range(-m, m + 1, 2), 0.15)
        cd, _ = in_card(12.6, 5.3, ax, labs, lat, shift=RIGHT * 0.15 + UP * 0.55)
        VGroup(cd, ax, labs, lat).move_to(DOWN * 0.55)
        before = runs(ax, s[:T + 1], 4)
        after = runs(ax, s[T:], 4, t0=T)
        zeros = VGroup(*[Dot(ax.c2p(i, 0), radius=0.06, color=HI) for i, v in enumerate(s) if v == 0 and i < T])
        flag = Dot(ax.c2p(T, 0), radius=0.12, color=HI)
        fl = sans('last tie', 24, HI, 'SEMIBOLD').next_to(flag, UP, buff=0.25)
        with self.seg('l1') as g:
            self.play(FadeIn(h), FadeIn(cd), Create(ax), FadeIn(labs), FadeIn(lat), run_time=0.8)
            self.play(Create(before), run_time=1.3, rate_func=linear)
            self.play(Create(after), run_time=1.3, rate_func=linear)
            self.play(FadeIn(zeros), run_time=0.4)
            self.play(GrowFromCenter(flag), FadeIn(fl), run_time=0.6)
        yb = ax.c2p(0, -m)[1] - 0.5
        br1 = BraceBetweenPoints([ax.c2p(0, 0)[0], yb, 0], [ax.c2p(T, 0)[0], yb, 0], DOWN, color=SKY)
        br2 = BraceBetweenPoints([ax.c2p(T, 0)[0], yb, 0], [ax.c2p(n2, 0)[0], yb, 0], DOWN, color=HI)
        t1 = tex(r'0 \to 0:\ \ u_{2k}', 36, SKY).next_to(br1, DOWN, buff=0.12)
        t2 = tex(r'\text{never returns}:\ \ u_{2n-2k}', 36, HI).next_to(br2, DOWN, buff=0.12)
        with self.seg('l2') as g:
            self.play(after.animate.set_stroke(opacity=0.3), run_time=0.5)
            self.hold(g.left() - 3.2)
            self.play(GrowFromCenter(br1), FadeIn(t1), before.animate.set_stroke(width=5.5), run_time=0.9)
        with self.seg('l3') as g:
            self.play(after.animate.set_stroke(opacity=1, width=5.5), before.animate.set_stroke(opacity=0.35), run_time=0.5)
            self.hold(g.left() - 2.6)
            self.play(GrowFromCenter(br2), FadeIn(t2), run_time=0.9)
        with self.seg('l4') as g:
            law = tex(r'P(\text{last tie at } 2k) = u_{2k}\cdot u_{2n-2k}', 46, TEXT)
            law.to_edge(UP, buff=0.55).to_edge(RIGHT, buff=0.55)
            self.play(before.animate.set_stroke(opacity=1), TransformFromCopy(VGroup(t1, t2), law), run_time=1.4)
            self.hold(g.left() - 6.5)
            self.play(FadeOut(VGroup(cd, ax, labs, lat, before, after, zeros, flag, fl, br1, br2, t1, t2)), run_time=0.5)
            ax2, labs2 = axes([-1, 21, 1], [0, 0.2, 0.05], 9.4, 3.9, xt=range(0, 21, 2), yt=(0.05, 0.1, 0.15))
            ax2.x_axis.ticks.set_opacity(0)
            c2, _ = in_card(11, 5.0, ax2, labs2, shift=RIGHT * 0.2 + UP * 0.15)
            VGroup(c2, ax2, labs2).move_to(DOWN * 0.7)
            cap = sans('2n = 20 tosses', 22, MUTED).next_to(c2, DOWN, buff=0.12).align_to(c2, LEFT)
            bars = VGroup(*[Polygon(ax2.c2p(2 * kk - 0.7, 0), ax2.c2p(2 * kk + 0.7, 0), ax2.c2p(2 * kk + 0.7, p), ax2.c2p(2 * kk - 0.7, p),
                                    stroke_width=0, fill_color=ALICE, fill_opacity=0.9) for kk, p in enumerate(D.EXACT)])
            self.play(FadeIn(c2), Create(ax2), FadeIn(labs2), FadeIn(cap), run_time=0.6)
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), run_time=max(1.2, g.left() - 0.2))
        with self.seg('l5'):
            ends = VGroup(bars[0], bars[-1])
            el = sans('very early', 22, HI).next_to(bars[0], UP, buff=0.12)
            ll = sans('very late', 22, HI).next_to(bars[-1], UP, buff=0.12)
            self.play(ends.animate.set_fill(HI), FadeIn(el), FadeIn(ll), run_time=0.8)
        with self.seg('l6') as g:
            sur = VGroup(sans('time Alice spends in the lead', 28, ALICE, 'SEMIBOLD'),
                         sans('has the same distribution', 28, TEXT))
            sur.arrange(DOWN, buff=0.15)
            bx = RoundedRectangle(width=sur.width + 0.8, height=sur.height + 0.5, corner_radius=0.18, fill_color=SURFACE2,
                                  fill_opacity=0.97, stroke_color=ALICE, stroke_width=2.5)
            sg = VGroup(bx, sur.move_to(bx)).move_to(ax2.c2p(10, 0.13))
            self.wait(1.2)
            self.play(FadeIn(sg, scale=0.95), run_time=0.8)
            proof = pill('full proof on Aram Code Lab', TEXT2, 22).next_to(sg, DOWN, buff=0.2)
            self.hold(g.left() - 3)
            self.play(FadeIn(proof, shift=UP * 0.1), run_time=0.5)
        self.clear_all()

    # ================================================================== 6. bars to a curve
    def bars_to_curve(self):
        h = header('05', 'from bars to a curve', 'Let the game grow')
        ax, labs = axes([0, 1, 0.1], [0, 3.5, 1], 9.4, 3.8, xt=(0, 0.25, 0.5, 0.75, 1), yt=(1, 2, 3))
        c, _ = in_card(11, 4.9, ax, labs, shift=RIGHT * 0.15 + UP * 0.15)
        VGroup(c, ax, labs).move_to(DOWN * 0.75)
        xl = tex(r'x = k / n', 34, MUTED).next_to(ax.x_axis, DOWN, buff=0.5).align_to(ax, RIGHT)
        est = tex(r'u_{2m} \approx \frac{1}{\sqrt{\pi m}}', 38, TEXT2).to_edge(UP, buff=0.55).to_edge(RIGHT, buff=0.6)

        def bars(n):
            hs = D.bars(n)
            return bar_group(ax, [k / n for k in range(n + 1)], hs, 1 / n, top=3.45, op=0.85)

        label = pill('2n = 20', TEXT2, 24).next_to(c, DOWN, buff=0.12).align_to(c, LEFT)
        with self.seg('b1') as g:
            b = bars(10)
            self.play(FadeIn(h), FadeIn(c), Create(ax), FadeIn(labs), FadeIn(est), run_time=0.8)
            self.play(LaggedStart(*[GrowFromEdge(x, DOWN) for x in b], lag_ratio=0.05), FadeIn(label), FadeIn(xl), run_time=1)
            self.hold(g.left() - 4)
            for n in (25, 50, 100):
                self.play(Transform(b, bars(n)), Transform(label, pill(f'2n = {2 * n}', TEXT2, 24).move_to(label, aligned_edge=LEFT)), run_time=0.9)
        with self.seg('b2') as g:
            self.play(Transform(b, bars(200)), Transform(label, pill('2n = 400', TEXT2, 24).move_to(label, aligned_edge=LEFT)), run_time=0.9)
            curve = ax.plot(lambda x: 1 / (math.pi * math.sqrt(x * (1 - x))), x_range=[0.0085, 0.9915, 0.002], color=HI, stroke_width=4.5)
            dens = tex(r'\frac{1}{\pi\sqrt{x(1-x)}}', 50, HI).move_to(ax.c2p(0.5, 2.55))
            self.play(Create(curve), run_time=1.5)
            self.play(Write(dens), run_time=1.0)
        with self.seg('b3') as g:
            self.play(b.animate.set_fill(opacity=0.18), FadeOut(dens), run_time=0.5)
            xv = ValueTracker(0.01)
            area = always_redraw(lambda: ax.get_area(curve, x_range=[0.0085, max(0.0086, xv.get_value())], color=HI, opacity=0.35))
            mark = always_redraw(lambda: DashedLine(ax.c2p(xv.get_value(), 0), ax.c2p(xv.get_value(), 3.4), color=HI, stroke_width=2))
            xlab = always_redraw(lambda: tex('x', 34, HI).next_to(ax.c2p(xv.get_value(), 0), DOWN, buff=0.12))
            self.add(area, mark, xlab)
            self.play(xv.animate.set_value(0.3), run_time=2.2)
            law = tex(r'\int_0^x \frac{dt}{\pi\sqrt{t(1-t)}} = \frac{2}{\pi}\arcsin\sqrt{x}', 46, TEXT)
            bx = RoundedRectangle(width=law.width + 0.7, height=law.height + 0.5, corner_radius=0.18, fill_color=SURFACE2,
                                  fill_opacity=0.97, stroke_color=HI, stroke_width=2.5)
            lg = VGroup(bx, law.move_to(bx)).move_to(ax.c2p(0.58, 2.45))
            self.play(FadeIn(bx), Write(law), run_time=1.6)
            self.play(xv.animate.set_value(0.7), run_time=max(1, g.left() - 2.2))
            name = pill('the arc sine law', HI, 26).next_to(lg, DOWN, buff=0.2)
            self.play(FadeIn(name, shift=UP * 0.1), run_time=0.6)
        self.clear_all()

    # ================================================================== 7. code lab
    def code_lab(self):
        h = header('06', 'code lab', 'Try it yourself')
        lines = code_lines(CODE, 24)
        if lines.width > 7.6:
            lines.scale(7.6 / lines.width)
        cc = card(lines.width + 0.8, lines.height + 1.2)
        bar = mono('lead_fraction.py', 18, MUTED)
        lines.move_to(cc).shift(DOWN * 0.2)
        bar.next_to(cc.get_corner(UL), DR, buff=0.25)
        dots3 = VGroup(*[Dot(radius=0.06, color=col) for col in ('#ff5f57', '#febc2e', '#28c840')]).arrange(RIGHT, buff=0.12)
        dots3.next_to(cc.get_corner(UR), DL, buff=0.28)
        code = VGroup(cc, lines, bar, dots3).to_edge(LEFT, buff=0.55).shift(DOWN * 0.45)
        with self.seg('k1') as g:
            self.play(FadeIn(h), FadeIn(cc), FadeIn(bar), FadeIn(dots3), run_time=0.6)
            self.play(LaggedStart(*[AddTextLetterByLetter(l) if isinstance(l, MarkupText) else Wait(0.05) for l in lines],
                                  lag_ratio=0.9), run_time=max(2.5, g.left() - 0.1))
        with self.seg('k2') as g:
            def hl(i0, i1):
                top, bot = lines[i0].get_top()[1], lines[i1].get_bottom()[1]
                return RoundedRectangle(width=cc.width - 0.3, height=top - bot + 0.18, corner_radius=0.08, fill_color=ACCENT,
                                        fill_opacity=0.12, stroke_width=0).move_to([cc.get_center()[0], (top + bot) / 2, 0])
            r1 = hl(2, 8)
            self.play(FadeIn(r1), run_time=0.5)
            r2 = hl(7, 7).set_fill(HI, opacity=0.18)
            self.play(Transform(r1, r2), run_time=0.6)
            self.hold(g.left() - 2.6)
            self.play(Transform(r1, hl(10, 11)), run_time=0.6)
        with self.seg('k3') as g:
            run = pill('▶  Run', ACCENT, 26).next_to(cc, DOWN, buff=0.25).align_to(cc, LEFT)
            out = VGroup(mono('>>>', 22, MUTED), mono('0.4169', 26, HI, 'SEMIBOLD')).arrange(RIGHT, buff=0.25).next_to(run, RIGHT, buff=0.4)
            self.play(FadeIn(run), FadeOut(r1), run_time=0.4)
            self.play(Indicate(run, color=ACCENT, scale_factor=1.08), run_time=0.5)
            self.play(FadeIn(out, shift=RIGHT * 0.15), run_time=0.5)
            ax, labs = axes([0, 1, 0.05], [0, 3.2, 1], 3.6, 2.4, xt=(0, 0.5, 1), size=16)
            ax.y_axis.set_opacity(0)
            hc, _ = in_card(4.2, 3.3, ax, labs, shift=UP * 0.1)
            VGroup(hc, ax, labs).next_to(cc, RIGHT, buff=0.3).align_to(cc, UP)
            hb = bar_group(ax, [(i + 0.5) / 20 for i in range(20)], D.HIST, 0.05)
            self.play(FadeIn(hc), Create(ax), FadeIn(labs), LaggedStart(*[GrowFromEdge(b, DOWN) for b in hb], lag_ratio=0.04), run_time=1.4)
            site = VGroup(sans('run it in your browser on', 24, TEXT2), logo(26)).arrange(DOWN, buff=0.15).next_to(hc, DOWN, buff=0.35)
            self.hold(g.left() - 1.6)
            self.play(FadeIn(site, shift=UP * 0.1), run_time=0.6)
        self.clear_all()

    # ================================================================== 8. what it means
    def meaning(self):
        h = header('07', 'what it means', 'Long leads are normal')
        s = D.SEASON
        m = int(math.ceil(max(abs(s.min()), abs(s.max())) / 5) * 5)
        ax, labs = axes([0, 160, 20], [-m, m, 5], 11.4, 3.8, xt=range(0, 161, 40), yt=(-m, 0, m))
        cd, _ = in_card(12.6, 4.9, ax, labs, shift=RIGHT * 0.15 + UP * 0.15)
        VGroup(cd, ax, labs).move_to(DOWN * 0.6)
        cap = sans('two equally good teams: wins of team A − wins of team B, game by game', 22, MUTED).next_to(cd, DOWN, buff=0.14).align_to(cd, LEFT)
        with self.seg('m1') as g:
            self.play(FadeIn(h), FadeIn(cd), Create(ax), FadeIn(labs), FadeIn(cap), run_time=0.8)
            self.play(Create(runs(ax, s, 4)), run_time=max(2.5, g.left() - 2.2), rate_func=linear)
            p = pill(f'team A ahead {round(100 * D.lead_fraction(s))}% of the season', ALICE, 26).to_edge(UP, buff=0.6).to_edge(RIGHT, buff=0.55)
            self.play(FadeIn(p, shift=UP * 0.1), run_time=0.6)
        with self.seg('m2'):
            self.clear_all(0.4)
            a = sans('The coin has no memory.', 54, TEXT2, 'BOLD')
            b = sans('The score does.', 54, ACCENT, 'BOLD')
            VGroup(a, b).arrange(DOWN, buff=0.35)
            self.play(FadeIn(a, shift=UP * 0.15), run_time=0.7)
            self.play(FadeIn(b, shift=UP * 0.15), run_time=0.7)
        self.wait(0.2)
        self.clear_all()

    # ================================================================== 9. challenge
    def challenge(self):
        h = header('08', 'challenge', 'Counting votes')
        v = D.BALLOT
        chips = VGroup(*[RoundedRectangle(width=0.32, height=0.32, corner_radius=0.06, stroke_width=0,
                                          fill_color=ALICE if x > 0 else BOB, fill_opacity=0.95) for x in v])
        chips.arrange_in_grid(5, 20, buff=0.08)
        key = VGroup(VGroup(Square(0.26, fill_color=ALICE, fill_opacity=1, stroke_width=0), sans('A: 60 votes', 24, ALICE, 'SEMIBOLD')).arrange(RIGHT, buff=0.15),
                     VGroup(Square(0.26, fill_color=BOB, fill_opacity=1, stroke_width=0), sans('B: 40 votes', 24, BOB, 'SEMIBOLD')).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.6)
        top = VGroup(key, chips).arrange(DOWN, buff=0.3)
        cs = np.concatenate([[0], np.cumsum(v)])
        ax, labs = axes([0, 100, 10], [-5, 25, 5], 8.6, 2.2, xt=(0, 50, 100), yt=(0, 20), size=16)
        path = runs(ax, cs, 3.5)
        bottom = VGroup(ax, labs, path)
        body = VGroup(top, bottom).arrange(DOWN, buff=0.35)
        if body.height > 4.9:
            body.scale(4.9 / body.height)
        c, _ = in_card(body.width + 1, body.height + 0.7, body)
        VGroup(c, body).move_to(DOWN * 0.65)
        q = tex(r'P\big(\text{A strictly ahead during the whole count}\big) = \ ?', 40, HI)
        with self.seg('z1') as g:
            self.play(FadeIn(h), FadeIn(c), FadeIn(key), run_time=0.6)
            self.play(LaggedStart(*[FadeIn(x, scale=0.6) for x in chips], lag_ratio=0.03), run_time=min(4, max(2, g.left() - 8)))
            self.play(Create(ax), FadeIn(labs), run_time=0.5)
            self.play(Create(path), run_time=2.5, rate_func=linear)
            self.hold(g.left() - 2.4)
            qb = RoundedRectangle(width=q.width + 0.7, height=q.height + 0.45, corner_radius=0.18, fill_color=SURFACE2,
                                  fill_opacity=0.97, stroke_color=HI, stroke_width=2.5)
            qg = VGroup(qb, q.move_to(qb)).move_to(c.get_center())
            veil = RoundedRectangle(width=c.width, height=c.height, corner_radius=0.18, fill_color=SURFACE, fill_opacity=0.72,
                                    stroke_width=0).move_to(c)
            self.play(FadeIn(veil), FadeIn(qg, scale=0.95), run_time=0.8)
        with self.seg('z2') as g:
            self.clear_all(0.4)
            eb = mono('PROBABILITY  ·  RANDOM WALKS', 22, ACCENT)
            title = sans('The Arc Sine Law', 64, TEXT, 'BOLD')
            law = tex(r'P\big(\text{Alice leads} \le x\big) \approx \frac{2}{\pi}\arcsin\sqrt{x}', 46, HI)
            site = VGroup(sans('Answer · full proof · exercises · code', 28, TEXT2), logo(32)).arrange(DOWN, buff=0.3)
            VGroup(eb, title, law, site).arrange(DOWN, buff=0.45)
            self.play(FadeIn(eb), Write(title), FadeIn(law), run_time=1.2)
            self.play(FadeIn(site, shift=UP * 0.15), run_time=0.7)
        self.wait(2.5)
