"""Manim scene for the approved A positive test: am I ill? script."""

import sys
from math import pi
from pathlib import Path

from manim import (
    DOWN, DR, LEFT, RIGHT, UP, Arc, Circle, Create, Square,
    FadeIn, FadeOut, FadeTransform, Group, ImageMobject, Indicate, Line, MathTex,
    Rectangle, ReplacementTransform, RoundedRectangle, SurroundingRectangle,
    Transform, TransformFromCopy, VGroup, linear,
)
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))

import data as D
from brand import (
    ACCENT, BORDER2, MUTED, NEXT, SURFACE, TEXT, TEXT2, WARN,
    background, card, header, logo, mono, pill, sans,
)
from code_card import code_lines
from narrate import Narrated

ILL, WELL, POSITIVE = ACCENT, NEXT, WARN


def labelled(value, caption, color=TEXT, width=3.6, height=1.35, size=39):
    reading = VGroup(sans(value, size, color, 'BOLD'), sans(caption, 21, TEXT2))
    reading.arrange(DOWN, buff=0.12)
    if reading.width > width - 0.32:
        reading.scale_to_fit_width(width - 0.32)
    panel = card(width, height)
    return VGroup(panel, reading.move_to(panel))


def status_mark(ill, positive=False, size=0.38):
    shape = Circle(radius=size / 2) if ill else Square(side_length=size).rotate(pi / 4).scale_to_fit_width(size)
    col = ILL if ill else WELL
    shape.set_fill(col, opacity=1).set_stroke(width=0)
    if not positive:
        return VGroup(shape)
    outline = Circle(radius=size * 0.79, color=POSITIVE, stroke_width=2.5)
    plus = mono('+', 19, POSITIVE).move_to(outline.get_right() + RIGHT * 0.17)
    return VGroup(shape, outline, plus)


def status_key(ill, caption, positive=False):
    return VGroup(status_mark(ill, positive), sans(caption, 22, TEXT2)).arrange(RIGHT, buff=0.22)


def dot_grid(reveal):
    """A raster layer keeps the 10,000 real trial positions visible at full resolution."""
    pitch = 12
    side = D.GRID_SIDE * pitch
    canvas = Image.new('RGB', (side, side), SURFACE)
    draw = ImageDraw.Draw(canvas)
    # Put the smaller group together so the viewer can find its positives.
    outcomes = sorted(D.GRID, key=lambda person: not person[0])
    for index, (ill, positive) in enumerate(outcomes):
        row, col = divmod(index, D.GRID_SIDE)
        x, y = col * pitch + pitch // 2, row * pitch + pitch // 2
        color = ILL if ill else WELL
        if reveal and positive:
            draw.ellipse((x - 5, y - 5, x + 5, y + 5), outline=POSITIVE, width=2)
            draw.line((x - 2, y, x + 2, y), fill=color, width=2)
            draw.line((x, y - 2, x, y + 2), fill=color, width=2)
        elif ill:
            draw.ellipse((x - 3, y - 3, x + 3, y + 3), fill=color if not reveal else '#1b5e57')
        else:
            draw.polygon([(x, y - 3), (x + 3, y), (x, y + 3), (x - 3, y)],
                         fill=color if not reveal else '#343658')
    return ImageMobject(canvas).set_height(4.45)


def stack_dots(count, ill):
    marks = VGroup(*(status_mark(ill, size=0.10) for _ in range(count)))
    marks.arrange_in_grid(cols=10, buff=0.055)
    return marks


def sample_rect(prevalence, width, height):
    """Draw a unit-area probability mosaic, with positives rising from the baseline."""
    p = float(prevalence)
    left = Rectangle(width=width * p, height=height).set_fill(ILL, opacity=0.21).set_stroke(width=0)
    right = Rectangle(width=width * (1 - p), height=height).set_fill(WELL, opacity=0.20).set_stroke(width=0)
    cols = VGroup(left, right).arrange(RIGHT, buff=0)
    frame = Rectangle(width=width, height=height, color=BORDER2, stroke_width=2).move_to(cols)
    a = Rectangle(width=left.width, height=height * float(D.SENSITIVITY),
                  stroke_width=0, fill_color=ILL, fill_opacity=1)
    b = Rectangle(width=right.width, height=height * float(D.FALSE_POSITIVE_RATE),
                  stroke_width=0, fill_color=WELL, fill_opacity=1)
    a.move_to(left, aligned_edge=DOWN)
    b.move_to(right, aligned_edge=DOWN)
    return VGroup(cols, frame, a, b)


class Video(Narrated):
    folder = str(HERE)

    def setup(self):
        self.add(background())
        self.mark = logo(22).set_opacity(0.83).to_corner(DR, buff=0.32).set_z_index(20)
        self.add(self.mark)
        self.heading = None
        self.body = None

    def title(self, number, eyebrow, title):
        new = header(number, eyebrow, title)
        if self.heading is None:
            self.play(FadeIn(new, shift=RIGHT * 0.12), run_time=0.55)
        else:
            self.play(ReplacementTransform(self.heading, new), run_time=0.55)
        self.heading = new

    def transition(self, new, duration=0.8):
        if self.body is None:
            self.play(FadeIn(new, shift=UP * 0.12), run_time=duration)
        elif isinstance(self.body, VGroup) and isinstance(new, VGroup):
            self.play(FadeTransform(self.body, new), run_time=duration)
        else:
            # Cairo cannot restore a mixed vector/raster Group from FadeTransform.
            self.play(FadeOut(self.body, shift=UP * 0.10),
                      FadeIn(new, shift=UP * 0.10), run_time=duration)
        self.body = new

    def at(self, segment, seconds):
        """Schedule a reveal a fixed number of seconds after the current cue."""
        rest = seconds - (self.renderer.time - segment.t0)
        if rest > 0.03:
            self.wait(rest)

    def construct(self):
        self.cold_open()
        self.puzzle()
        self.experiment()
        self.natural_frequencies()
        self.formula()
        self.code_lab()
        self.meaning()
        self.challenge()

    def cold_open(self):
        result = labelled('POSITIVE', 'Test result', POSITIVE, width=5.25, height=1.72, size=51)
        result.move_to(UP * 0.72)
        with self.seg('cold1') as g:
            self.transition(result)
            self.at(g, 10)
            tiles = VGroup(
                labelled('+', 'Has the condition', ILL, width=3.65),
                labelled('+', 'Does not have it', WELL, width=3.65),
            ).arrange(RIGHT, buff=0.28).move_to(DOWN * 0.95)
            for tile, ill in zip(tiles, (True, False), strict=True):
                tile[0].set_stroke(POSITIVE, width=2)
                caption = tile[1][1]
                tile[1] = VGroup(status_mark(ill, True), caption)
                tile[1].arrange(DOWN, buff=0.14).move_to(tile[0])
            answer = pill(f'{float(D.EXACT.posterior):.0%}', POSITIVE, 38).move_to(UP * 0.9)
            self.play(FadeTransform(result, answer), FadeIn(tiles, shift=UP * 0.2), run_time=0.95)
            self.body = VGroup(tiles, answer)

        with self.seg('cold2') as g:
            self.at(g, 6.4)
            subtitle = mono('PROBABILITY  ·  CONDITIONAL CHANCE', 22, ACCENT)
            heading = sans('A positive test: am I ill?', 65, TEXT, 'BOLD')
            symbols = VGroup(status_mark(True, True), status_mark(False, True)).arrange(RIGHT, buff=0.65)
            title = VGroup(subtitle, heading, symbols).arrange(DOWN, buff=0.36)
            self.transition(title, 1.15)
        self.wait(2)

    def puzzle(self):
        with self.seg('puzzle1') as g:
            self.title('01', 'the puzzle', 'The rules of the test')
            conditions = VGroup(
                labelled(f'{float(D.BASE_RATE):.0%}', 'Have the condition', ILL),
                labelled(f'{float(D.SENSITIVITY):.0%}', 'Positive with it', ILL),
                labelled(f'{float(D.FALSE_POSITIVE_RATE):.0%}', 'Positive without it', WELL),
            ).arrange(RIGHT, buff=0.28).move_to(UP * 0.65)
            tray = pill('+  Positive results', POSITIVE, 25).move_to(DOWN * 0.92)
            self.transition(conditions[0])
            self.at(g, 6.8)
            self.play(FadeIn(conditions[1], shift=UP * 0.12), run_time=0.55)
            self.at(g, 10.3)
            self.play(FadeIn(conditions[2], shift=UP * 0.12), run_time=0.55)
            self.at(g, 12.8)
            self.play(TransformFromCopy(conditions[2][1][0], tray), run_time=0.65)
            self.body = Group(conditions, tray)

        with self.seg('puzzle2') as g:
            self.title('01', 'make a guess', f'False alarms per {D.PEOPLE:,}?')
            options = VGroup(*(pill(f'About {value:,}', TEXT2, 25) for value in D.GUESS_OPTIONS))
            options.arrange(RIGHT, buff=0.44).move_to(DOWN * 1.76)
            self.at(g, 6.2)
            for option in options:
                self.play(FadeIn(option, shift=UP * 0.14), run_time=0.4)
                self.wait(0.48)
            self.body = Group(conditions, tray, options)
        prompt = mono('PAUSE AND THINK', 20, POSITIVE).move_to(DOWN * 2.67 + RIGHT * 0.25)
        ring = Arc(radius=0.16, start_angle=0.0, angle=2 * pi,
                   color=POSITIVE, stroke_width=3).next_to(prompt, direction=LEFT, buff=0.24)
        self.play(FadeIn(prompt), Create(ring, rate_func=linear), run_time=D.GUESS_SECONDS)
        self.body = Group(self.body, prompt, ring)

    def experiment(self):
        with self.seg('experiment1') as g:
            self.title('02', 'the experiment', f'One simulated group · {D.PEOPLE:,} people')
            grid = dot_grid(False).move_to(RIGHT * -3.08 + DOWN * 0.15)
            boundary = card(4.72, 4.72).move_to(grid)
            legend = VGroup(
                status_key(True, 'Has the condition'),
                status_key(False, 'Does not have it'),
                pill('+  Positive test', POSITIVE, 22),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(RIGHT * 2.62 + UP * 0.15)
            self.transition(Group(boundary, grid, legend))
            self.at(g, 8.6)
            lit = dot_grid(True).move_to(grid)
            self.play(FadeTransform(grid, lit), Indicate(legend[-1], color=POSITIVE), run_time=1.05)
            grid = lit
            self.body = Group(boundary, grid, legend)

        with self.seg('experiment2') as g:
            count = D.GRID_COUNTS
            true = labelled(f'{count.true_positive:,}', 'True positives', ILL, width=4.0)
            false = labelled(f'{count.false_positive:,}', 'False positives', WELL, width=4.0)
            tally = VGroup(true, false).arrange(DOWN, buff=0.20).move_to(RIGHT * 2.73 + UP * 0.33)
            for panel in tally:
                panel[0].set_stroke(POSITIVE, width=1.8)
            self.play(FadeTransform(legend, true), run_time=0.68)
            self.at(g, 4)
            self.play(TransformFromCopy(true, false), run_time=0.75)
            self.at(g, 7.15)
            result = pill(
                f'{count.true_positive} / {count.positives}  ≈  {float(count.posterior):.1%}',
                POSITIVE, 27,
            ).next_to(tally, DOWN, buff=0.33)
            self.play(FadeIn(result, shift=UP * 0.14), run_time=0.72)
            self.body = Group(boundary, grid, tally, result)
            self.simulation = boundary, grid, true, false, result
        self.wait(4)

    def natural_frequencies(self):
        count = D.EXACT
        left_x, right_x = -3.04, 3.04
        with self.seg('count1') as g:
            self.title('03', 'count the positives', f'Expected counts · {D.PEOPLE:,} people')
            left = labelled(f'{count.ill:,}', 'Have the condition', ILL, width=5.25)
            right = labelled(f'{count.healthy:,}', 'Do not have it', WELL, width=5.25)
            groups = VGroup(left.move_to([left_x, 1.01, 0]), right.move_to([right_x, 1.01, 0]))
            boundary, grid, true, false, result = self.simulation
            self.play(FadeOut(Group(boundary, grid), shift=RIGHT * 0.18),
                      FadeOut(result, shift=DOWN * 0.12),
                      ReplacementTransform(true, left), ReplacementTransform(false, right),
                      run_time=0.92)
            left_dots = stack_dots(count.true_positive, True)
            right_dots = stack_dots(count.false_positive, False)
            left_dots.move_to([left_x - 1.28, -0.77, 0])
            right_dots.move_to([right_x - 1.28, -0.77, 0])
            l = labelled(f'{count.true_positive:,}', 'True positives', ILL, width=2.7)
            r = labelled(f'{count.false_positive:,}', 'False positives', WELL, width=2.7)
            l.move_to([left_x + 0.98, -0.77, 0])
            r.move_to([right_x + 0.98, -0.77, 0])
            for panel in (l, r):
                panel[0].set_stroke(POSITIVE, width=2)
            self.at(g, 5.1)
            self.play(FadeIn(left_dots), TransformFromCopy(left[1][0], l), run_time=0.75)
            self.at(g, 12.3)
            self.play(FadeIn(right_dots), TransformFromCopy(right[1][0], r), run_time=0.75)
            self.body = Group(groups, left_dots, right_dots, l, r)

        with self.seg('count2') as g:
            tray_title = mono(f'{count.positives}  POSITIVE RESULTS', 24, POSITIVE)
            fraction = sans(f'{count.true_positive} / {count.positives} = {float(count.posterior):.0%}',
                            43, POSITIVE, 'BOLD')
            mini = VGroup(l.copy(), r.copy()).arrange(RIGHT, buff=0.43)
            tray = VGroup(tray_title, mini, fraction).arrange(DOWN, buff=0.34).move_to(DOWN * 0.2)
            self.play(
                FadeOut(Group(groups, left_dots, right_dots), shift=UP * 0.1),
                ReplacementTransform(l, mini[0]), ReplacementTransform(r, mini[1]),
                FadeIn(tray_title), run_time=0.95,
            )
            self.at(g, 7.05)
            self.play(FadeIn(fraction, shift=UP * 0.12), run_time=0.65)
            self.body = tray

        with self.seg('count3') as g:
            lhs = labelled(f'{count.true_positive} / {count.ill}', 'Positive among those with it', ILL,
                           width=5.16, height=1.74, size=43)
            rhs = labelled(f'{count.true_positive} / {count.positives}', 'Have it among the positives',
                           POSITIVE, width=5.16, height=1.74, size=43)
            comparison = VGroup(lhs, rhs).arrange(RIGHT, buff=0.49).move_to(DOWN * 0.08)
            rhs.set_opacity(0.32)
            self.transition(comparison)
            focus = SurroundingRectangle(lhs[0], color=ILL, buff=0.06, corner_radius=0.19)
            self.play(Create(focus), run_time=0.66)
            self.at(g, 8.75)
            self.play(Transform(focus, SurroundingRectangle(rhs[0], color=POSITIVE, buff=0.06,
                                                           corner_radius=0.19)),
                      lhs.animate.set_opacity(0.58), rhs.animate.set_opacity(1), run_time=0.78)
            self.body = Group(comparison, focus)
        self.wait(5)

    def formula(self):
        with self.seg('area1') as g:
            self.title('04', 'from the picture to the formula', 'Width × height gives probability')
            mosaic = sample_rect(D.BASE_RATE, 7.0, 3.0).move_to([-2.3, -0.26, 0])
            width_labels = VGroup(
                status_key(True, f'{float(D.BASE_RATE):.0%} have it'),
                status_key(False, f'{float(1 - D.BASE_RATE):.0%} do not'),
            ).arrange(RIGHT, buff=0.52).next_to(mosaic, UP, buff=0.23)
            heights = VGroup(
                labelled(f'{float(D.SENSITIVITY):.0%}', 'Positive with it', ILL, width=3.6),
                labelled(f'{float(D.FALSE_POSITIVE_RATE):.0%}', 'Positive without it', WELL, width=3.6),
            ).arrange(DOWN, buff=0.25).move_to([3.68, -0.26, 0])
            self.transition(Group(mosaic, width_labels))
            self.at(g, 5.5)
            self.play(FadeIn(heights, shift=RIGHT * 0.12), run_time=0.75)
            self.body = Group(mosaic, width_labels, heights)

        with self.seg('area2') as g:
            true_area = pill(f'{float(D.EXACT.true_positive / D.PEOPLE):.2%} of the whole crowd', ILL, 23)
            false_area = pill(f'{float(D.EXACT.false_positive / D.PEOPLE):.2%} of the whole crowd', WELL, 23)
            areas = VGroup(true_area, false_area).arrange(DOWN, buff=0.32).move_to(heights)
            eq_note = mono('EQUAL POSITIVE AREAS', 20, POSITIVE).move_to([3.68, -1.77, 0])
            self.play(TransformFromCopy(heights[0], true_area), FadeOut(heights[0]),
                      Indicate(mosaic[2], color=POSITIVE, scale_factor=1), run_time=0.72)
            self.at(g, 3.5)
            self.play(TransformFromCopy(heights[1], false_area), FadeOut(heights[1]),
                      Indicate(mosaic[3], color=POSITIVE, scale_factor=1), run_time=0.72)
            self.at(g, 6.45)
            self.play(FadeIn(eq_note), run_time=0.5)
            self.body = Group(mosaic, width_labels, areas, eq_note)

        with self.seg('area3') as g:
            mosaic_target = mosaic.copy().scale(0.70).move_to([-3.59, -0.54, 0])
            teal = MathTex(r'P(D)P(+\mid D)', color=ILL, font_size=34)
            indigo = MathTex(r'P(\bar D)P(+\mid\bar D)', color=WELL, font_size=34)
            terms = VGroup(teal, indigo).arrange(DOWN, buff=0.24).move_to([-3.55, 1.16, 0])
            self.play(Transform(mosaic, mosaic_target), FadeOut(width_labels), FadeOut(eq_note),
                      ReplacementTransform(areas[0], teal), ReplacementTransform(areas[1], indigo),
                      run_time=0.95)
            card_surface = card(7.0, 3.38).move_to([2.59, -0.31, 0])
            label = MathTex(r'P(D\mid+)', color=TEXT, font_size=42)
            num = teal.copy().scale(0.95)
            den = VGroup(teal.copy().scale(0.95), MathTex('+', font_size=34),
                         indigo.copy().scale(0.95)).arrange(RIGHT, buff=0.15)
            rule = Line([-den.width / 2 - 0.15, 0, 0],
                        [den.width / 2 + 0.15, 0, 0], color=TEXT2, stroke_width=2)
            stack = VGroup(num, rule, den).arrange(DOWN, buff=0.15)
            expression = VGroup(label, MathTex('=', font_size=38), stack)
            expression.arrange(RIGHT, buff=0.18).move_to([2.59, 0.20, 0])
            if expression.width > 6.5:
                expression.scale_to_fit_width(6.5)
            expression.set_z_index(2)
            self.at(g, 6.1)
            self.play(FadeIn(card_surface), FadeIn(label), FadeIn(expression[1]), Create(rule),
                      TransformFromCopy(teal, num), run_time=0.90)
            self.at(g, 9.7)
            self.play(TransformFromCopy(teal, den[0]), FadeIn(den[1]),
                      TransformFromCopy(indigo, den[2]), run_time=0.85)
            simplified = MathTex(
                rf'\frac{{{D.EXACT.true_positive / D.PEOPLE:.4f}}}'
                rf'{{{D.EXACT.true_positive / D.PEOPLE:.4f}+{D.EXACT.false_positive / D.PEOPLE:.4f}}}'
                rf'=\frac{{1}}{{2}}',
                font_size=38, color=POSITIVE,
            ).move_to([2.59, -1.10, 0]).set_z_index(2)
            name = pill('Bayes’ rule', POSITIVE, 23).move_to([2.59, -2.48, 0])
            self.at(g, 12.1)
            self.play(FadeIn(simplified, shift=UP * 0.12), run_time=0.72)
            self.at(g, 14.0)
            self.play(FadeIn(name), run_time=0.57)
            self.body = Group(mosaic, terms, card_surface, expression, simplified, name)
        self.wait(7.5)

    def code_lab(self):
        with self.seg('code1') as g:
            self.title('05', 'code lab', 'Run the same experiment in Python')
            lines = code_lines(D.CODE)
            if lines.width > 7.52:
                lines.scale_to_fit_width(7.52)
            panel = card(8.10, 5.00).move_to([-2.07, -0.28, 0])
            name = mono('positive_test.py', 19, MUTED).move_to([-4.76, 1.80, 0])
            lines.move_to([-2.07, -0.46, 0])
            self.transition(Group(panel, name, lines))
            expected = labelled(f'{float(D.EXACT.posterior):.0%}', 'Exact probability', POSITIVE,
                                width=3.74, height=1.41).move_to([4.09, 0.92, 0])
            self.play(TransformFromCopy(lines[-1], expected), run_time=0.65)

            def highlight(index):
                band = RoundedRectangle(width=7.79, height=0.34, corner_radius=0.07,
                                        stroke_width=0, fill_color=ACCENT, fill_opacity=0.19)
                return band.move_to([panel.get_center()[0], lines[index].get_center()[1], 0]).set_z_index(-1)

            # Keep the highlight in front of the card and the code in front of the highlight.
            lines.set_z_index(2)
            h = highlight(4).set_z_index(1)
            self.at(g, 4.4)
            self.play(FadeIn(h), run_time=0.43)
            self.at(g, 7.65)
            self.play(Transform(h, highlight(6).set_z_index(1)), run_time=0.52)
            self.at(g, 12.0)
            self.play(Transform(h, highlight(8).set_z_index(1)), run_time=0.52)
            self.body = Group(panel, name, lines, expected, h)

        with self.seg('code2') as g:
            result = labelled(f'{float(D.CODE_COUNTS.posterior):.1%}', 'Simulated result', ILL,
                              width=3.74, height=1.41).move_to([4.09, -0.69, 0])
            button = pill('▶  Run', ACCENT, 24).move_to([4.09, -2.01, 0])
            self.play(FadeOut(h), FadeIn(button), run_time=0.55)
            self.at(g, 5.45)
            self.play(Indicate(button, color=ACCENT, scale_factor=1.07), run_time=0.5)
            self.play(FadeIn(result, shift=UP * 0.12), run_time=0.66)
            self.at(g, 13.2)
            self.play(Indicate(expected[1][0], color=POSITIVE, scale_factor=1.11), run_time=0.68)
            self.body = Group(panel, name, lines, expected, result, button)
        self.wait(6)

    def meaning(self):
        with self.seg('meaning1') as g:
            self.title('06', 'what it means', 'A flagged transaction')
            flags = sample_rect(D.BASE_RATE, 8.85, 2.27).move_to(DOWN * 0.18)
            labels = VGroup(status_key(True, 'Fraud'), status_key(False, 'Legitimate'))
            labels.arrange(RIGHT, buff=0.76).next_to(flags, UP, buff=0.26)
            note = pill('+  Flagged', POSITIVE, 24).next_to(flags, DOWN, buff=0.34)
            self.transition(Group(flags, labels, note))
            self.at(g, 7.0)
            self.play(Indicate(note, color=POSITIVE, scale_factor=1.08), run_time=0.7)

        with self.seg('meaning2') as g:
            base = mono('BASE RATE  ·  SHARE BEFORE THE RESULT', 22, ACCENT)
            base.move_to(UP * 2.18)
            self.play(FadeIn(base), run_time=0.6)
            illustrative = sample_rect(D.BASE_RATE * 6, 8.85, 2.27).move_to(flags)
            self.at(g, 6.7)
            self.play(Transform(flags, illustrative), run_time=1.45)
            self.at(g, 10.7)
            self.play(Transform(flags, sample_rect(D.BASE_RATE, 8.85, 2.27).move_to(flags)),
                      run_time=1.45)
            self.body = Group(flags, labels, note, base)

        with self.seg('meaning3'):
            boundary = sans('Mathematics, not diagnosis.', 32, TEXT2).move_to(DOWN * 2.64)
            self.play(FadeIn(boundary), run_time=0.5)
            self.body = Group(self.body, boundary)
        self.wait(4)

    def challenge(self):
        with self.seg('challenge1') as g:
            self.title('07', 'challenge', 'Same test. A rarer condition.')
            pct = labelled(f'{float(D.BASE_RATE):.0%}', 'Have the condition', ILL)
            tp = labelled(f'{float(D.SENSITIVITY):.0%}', 'Positive with it', ILL)
            fp = labelled(f'{float(D.FALSE_POSITIVE_RATE):.0%}', 'Positive without it', WELL)
            top = VGroup(pct, tp, fp).arrange(RIGHT, buff=0.29).move_to(UP * 0.74)
            self.transition(top)
            self.at(g, 3.55)
            self.play(Transform(pct, labelled(f'{float(D.RARE_RATE):.1%}',
                                              'Have the condition', ILL).move_to(pct)),
                      run_time=0.7)
            prompt = pill('Of those who test positive, what fraction have it?', POSITIVE, 28)
            prompt.move_to(DOWN * 1.05)
            self.at(g, 6.85)
            self.play(FadeIn(prompt, shift=UP * 0.12), run_time=0.65)
            self.body = Group(top, prompt)
        self.wait(5)

        with self.seg('challenge2') as g:
            self.at(g, 6.5)
            end = VGroup(
                logo(58), sans('A positive test: am I ill?', 45, TEXT, 'BOLD'),
                pill('Answer  ·  Worked example  ·  Python', POSITIVE, 25),
            ).arrange(DOWN, buff=0.44).move_to(DOWN * 0.15)
            self.play(FadeOut(self.heading, shift=UP * 0.09), run_time=0.42)
            self.transition(end, 0.95)
        self.wait(3.2)
