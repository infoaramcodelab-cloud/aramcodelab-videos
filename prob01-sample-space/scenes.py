"""Lesson 1: Sample Space and Events."""

import sys
from pathlib import Path
from math import comb

import numpy as np
from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, Arrow, Circle, Create, DashedLine,
    Difference, Dot, Ellipse, FadeIn, FadeOut, Indicate, Intersection, LaggedStart,
    Line, MathTex, Polygon, Rectangle, RoundedRectangle, SurroundingRectangle,
    Transform, Union, VGroup,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))

from brand import ACCENT, BORDER2, SURFACE, MUTED, NEXT, TEXT, TEXT2, WARN, axes, card, mono, pill, sans
from data import (
    ARRANGEMENTS, CODE, COIN_TOSSES, EVENTS, EXACTLY_ONE_TAIL, KEY_IDEAS,
    MAJORITY_HEADS, OUTPUT, TOURNAMENT_ENDLESS, TOURNAMENT_FINITE,
)
from lesson_kit import (
    LessonScene, box, bullet_list, code_cell, end_card,
    inline_text, key_ideas, sample_points, title_card,
)

from prob_visuals import (
    arrangement_grid, cells_for, coin_outcome_cards, collapse_arrangements, dice_matrix, formula_pill,
    tournament_sequences,
)

DANGER = '#f87171'
PALE = '#e8eef3'
SELECTED = '#0f2624'   # tile fill for points in the event
SCHEMES = (
    ('Birthdays', 'people', '365 days'),
    ('Dice', 'dice', '6 faces, or a coin → 2'),
    ('Elevator', 'passengers', 'floors'),
    ('Random digits', 'positions', '10 digits'),
    ('Aces in bridge', '4 aces', '4 players'),
    ('Misprints', 'misprints', 'pages'),
)


def die(value):
    face = RoundedRectangle(
        width=0.96, height=0.96, corner_radius=0.13, color=BORDER2,
        fill_color=PALE, fill_opacity=1, stroke_width=1.5,
    )
    pips = {
        1: [(0, 0)],
        2: [(-1, 1), (1, -1)],
        3: [(-1, 1), (0, 0), (1, -1)],
        4: [(-1, 1), (1, 1), (-1, -1), (1, -1)],
        5: [(-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)],
    }
    return VGroup(face, *(Dot([x * 0.25, y * 0.25, 0], radius=0.065, color='#19212a') for x, y in pips[value]))


def dice_pair(a, b):
    pair = VGroup(die(a), die(b)).arrange(RIGHT, buff=0.11)
    return VGroup(pair, MathTex(f'({a},{b})', font_size=39, color=TEXT2).next_to(pair, DOWN, buff=0.20))


def scheme_icons():
    calendar = VGroup(card(0.48, 0.42), Line(LEFT * 0.19, RIGHT * 0.19, color=ACCENT).shift(UP * 0.07))
    dice = die(5).scale_to_fit_width(0.46)
    lift = VGroup(card(0.48, 0.42), Arrow(DOWN * 0.14, UP * 0.14, buff=0, color=ACCENT,
                                           stroke_width=2, max_tip_length_to_length_ratio=0.34))
    digits = mono('09', 26, ACCENT, 'BOLD')
    aces = VGroup(card(0.36, 0.49).rotate(-0.20), mono('A', 23, ACCENT, 'BOLD'))
    pages = VGroup(card(0.35, 0.41).shift(UP * 0.06 + RIGHT * 0.075), card(0.35, 0.41),
                   Line(LEFT * 0.09, RIGHT * 0.09, color=ACCENT))
    return [VGroup(Rectangle(width=0.63, height=0.55, stroke_width=0), icon) for icon in
            (calendar, dice, lift, digits, aces, pages)]


def coin_face():
    return VGroup(
        Circle(radius=1.18, color=WARN, fill_color='#695020', fill_opacity=0.83, stroke_width=4),
        Circle(radius=0.94, color=WARN, stroke_width=2),
        sans('H', 62, WARN, 'BOLD'),
    )


def playing_card(face='', color=TEXT2):
    tile = RoundedRectangle(width=0.47, height=0.66, corner_radius=0.08,
                            stroke_color=color if face else BORDER2, stroke_width=1.6,
                            fill_color='#243341' if not face else '#18222d', fill_opacity=1)
    glyph = sans(face, 27, color, 'BOLD') if face else Dot(radius=0.037, color=MUTED)
    return VGroup(tile, glyph.move_to(tile))


def person_icon():
    head = Dot(UP * 0.16, radius=0.091, color=MUTED)
    body = RoundedRectangle(width=0.29, height=0.24, corner_radius=0.08,
                            fill_color=MUTED, fill_opacity=1, stroke_width=0).shift(DOWN * 0.075)
    return VGroup(head, body)


def experiment_card(name, icon):
    tile = card(2.43, 2.48)
    label = sans(name, 27, TEXT, 'SEMIBOLD')
    if label.width > tile.width - 0.20:
        label.scale_to_fit_width(tile.width - 0.20)
    label.next_to(tile.get_bottom(), UP, buff=0.32)
    return VGroup(tile, icon.move_to(tile).shift(UP * 0.28), label)


def bridge_hands(ace_counts):
    hands, markers, aces = VGroup(), [], []
    for seat, n_aces in zip('NESW', ace_counts, strict=True):
        backs = VGroup(*(playing_card().shift(RIGHT * index * 0.20)
                         for index in range(13 - n_aces)))
        badges = VGroup(*(playing_card('A', WARN) for _ in range(n_aces)))
        if len(badges):
            badges.arrange(RIGHT, buff=0.13).next_to(backs, RIGHT, buff=0.12)
        aces.extend(badges)
        dealt = VGroup(backs, badges)
        label = VGroup(mono(seat, 41, ACCENT), sans('13 cards', 27, MUTED)).arrange(RIGHT, buff=0.17)
        contents = VGroup(label, dealt).arrange(DOWN, buff=0.21)
        panel = card(4.10, 1.62).move_to(contents)
        markers.append(panel)
        hands.add(VGroup(panel, contents))
    hands.arrange_in_grid(rows=2, cols=2, buff=(0.50, 0.29))
    return hands, markers, aces


def tournament_tree():
    """Show two starting winners and expand the first a–c–b continuation."""
    locations = {
        'a vs b': (0, 1.62), 'a': (-2.98, 0.69), 'b': (2.98, 0.69),
        'aa': (-5.0, -0.24), 'ac': (-1.52, -0.24),
        'bc': (1.52, -0.24), 'bb': (5.0, -0.24),
        'acc': (-2.98, -1.22), 'acb': (-0.10, -1.22),
        'bca': (2.11, -1.22), 'bcc': (4.2, -1.22),
        'acbb': (-1.15, -2.17), 'acba…': (0.97, -2.17),
    }
    finished = {'aa', 'bb', 'acc', 'bcc', 'acbb'}
    nodes = {
        name: VGroup(card(1.40 if len(name) > 3 else 0.91, 0.54).set_stroke(
            ACCENT if name in finished else BORDER2, width=2),
            mono(name, 26, ACCENT if name in finished else TEXT2)).move_to([x, y, 0])
        for name, (x, y) in locations.items()
    }
    edges = [('a vs b', 'a'), ('a vs b', 'b'), ('a', 'aa'), ('a', 'ac'), ('b', 'bc'), ('b', 'bb'),
             ('ac', 'acc'), ('ac', 'acb'), ('bc', 'bca'), ('bc', 'bcc'),
             ('acb', 'acbb'), ('acb', 'acba…')]
    lines = VGroup(*(Line(nodes[src].get_bottom(), nodes[dest].get_top(), color=MUTED, stroke_width=1.7)
                     for src, dest in edges))
    tree = VGroup(lines, VGroup(*nodes.values()))
    title = sans('First game: a plays b while c waits', 40, TEXT, 'BOLD').next_to(tree, UP, buff=0.31)
    label = pill('Two consecutive wins end the tournament', ACCENT, 27).next_to(tree, DOWN, buff=0.30)
    return VGroup(title, tree, label)


class EventDiagram(VGroup):
    """Two event boundaries and a fixed set of sample points."""

    def __init__(self, *, distinct=False, first_only=False, nested=False):
        self.universe = card(7.4, 4.55)
        self.a = Circle(radius=1.48, color=ACCENT, fill_opacity=0.12, stroke_width=3)
        self.b = Circle(radius=1.48, color=NEXT, fill_opacity=0.12, stroke_width=3)
        if nested:
            self.a.scale(0.51).shift(LEFT * 0.31)
            self.b.scale(1.22)
        else:
            self.a.shift(LEFT * (1.79 if distinct else 0.88))
            self.b.shift(RIGHT * (1.79 if distinct else 0.88))
        self.locations = [(x, y) for y in (-1.61, -0.84, -0.12, 0.62, 1.50)
                          for x in (-3.18, -2.45, -1.66, -0.9, -0.1, 0.72, 1.49, 2.36, 3.11)]
        ac, bc = self.a.get_center(), self.b.get_center()
        self.memberships = [(np.hypot(x - ac[0], y - ac[1]) < self.a.width / 2,
                             np.hypot(x - bc[0], y - bc[1]) < self.b.width / 2)
                            for x, y in self.locations]
        self.dots = VGroup(*(Dot([x, y, 0], radius=0.065, color=MUTED) for x, y in self.locations))
        a_label = MathTex('A', font_size=41, color=ACCENT).next_to(self.a.get_top(), UP, buff=0.13)
        b_label = MathTex('B', font_size=41, color=NEXT).next_to(self.b.get_top(), UP, buff=0.13)
        omega = MathTex(r'\Omega', font_size=40, color=TEXT2).move_to([3.21, 1.86, 0])
        regions = VGroup(self.a, a_label) if first_only else VGroup(self.a, self.b, a_label, b_label)
        super().__init__(self.universe, regions, self.dots, omega)

    def colors(self, predicate, shade):
        colors = []
        for (in_a, in_b), dot in zip(self.memberships, self.dots, strict=True):
            selected = predicate(in_a, in_b)
            colors.append((dot, shade if selected else MUTED))
        return colors

    def choose(self, scene, predicate, shade=ACCENT, *, outline=False):
        animation = []
        for dot, color in self.colors(predicate, shade):
            filled = 0 if outline and color == shade else 1
            width = 2.5 if color == shade else 0
            animation.append(dot.animate.set_fill(color, filled).set_stroke(color, width=width))
        scene.play(*animation, run_time=0.65)

    def shading(self, operation, color=WARN):
        boundary = Rectangle(width=self.universe.width, height=self.universe.height).move_to(self.universe)
        a, b = self.a.copy(), self.b.copy()
        outside_a, outside_b = Difference(boundary, a), Difference(boundary, b)
        regions = {
            'outside_union': lambda: Difference(boundary, Union(a, b)),
            'both_outside': lambda: Intersection(outside_a, outside_b),
            'outside_intersection': lambda: Difference(boundary, Intersection(a, b)),
            'either_outside': lambda: Union(outside_a, outside_b),
            'a_minus_ab': lambda: Difference(a, Intersection(a, b)),
            'a_and_outside_b': lambda: Intersection(a, outside_b),
            'union': lambda: Union(a, b),
            'a': lambda: a,
            'b_minus_ab': lambda: Difference(b, Intersection(a, b)),
        }
        return regions[operation]().set_fill(color, opacity=0.23).set_stroke(width=0)

    def shade(self, operation):
        color = WARN if operation in ('outside_union', 'both_outside', 'outside_intersection', 'either_outside') else ACCENT
        regions = (
            VGroup(self.shading('a', ACCENT), self.shading('b_minus_ab', NEXT))
            if operation == 'disjoint_union' else VGroup(self.shading(operation, color))
        )
        self.remove(self.universe)
        self.add_to_back(regions)
        self.add_to_back(self.universe)
        predicates = {
            'outside_union': lambda a, b: not (a or b),
            'both_outside': lambda a, b: not a and not b,
            'outside_intersection': lambda a, b: not (a and b),
            'either_outside': lambda a, b: not a or not b,
            'a_minus_ab': lambda a, b: a and not (a and b),
            'a_and_outside_b': lambda a, b: a and not b,
            'union': lambda a, b: a or b,
            'disjoint_union': lambda a, b: a or (b and not a),
        }
        for dot, shade in self.colors(predicates[operation], color):
            dot.set_fill(shade, opacity=0 if shade == WARN else 1)
            dot.set_stroke(shade, width=2.5 if shade == WARN else 0)
        return regions


def age_plane():
    ax, ticks = axes((0, 80, 20), (0, 80, 20), 6.3, 4.4, xt=(20, 40, 60, 80), yt=(20, 40, 60, 80), size=26)
    point = ax.c2p
    lines = VGroup(
        DashedLine(point(40, 0), point(40, 80), color=ACCENT, stroke_width=2),
        DashedLine(point(0, 0), point(80, 80), color=NEXT, stroke_width=2),
        DashedLine(point(0, 40), point(80, 40), color=WARN, stroke_width=2),
    )
    regions = VGroup(
        Polygon(point(40, 0), point(80, 0), point(80, 80), point(40, 80), color=ACCENT, stroke_width=0, fill_opacity=0.19),
        Polygon(point(0, 0), point(80, 0), point(80, 80), color=NEXT, stroke_width=0, fill_opacity=0.19),
        Polygon(point(0, 40), point(80, 40), point(80, 80), point(0, 80), color=WARN, stroke_width=0, fill_opacity=0.12),
        Polygon(point(40, 0), point(80, 0), point(80, 80), point(40, 40), color=ACCENT, stroke_width=0, fill_opacity=0.52),
        Polygon(point(40, 0), point(80, 0), point(80, 80), point(0, 80), point(0, 40), point(40, 40),
                color=ACCENT, stroke_width=0, fill_opacity=0.28),
    )
    labels = VGroup(
        inline_text(r'Husband’s age $x$', 32).next_to(ax.x_axis, DOWN, buff=0.52),
        inline_text(r'Wife’s age $y$', 32).next_to(ax.y_axis, UP, buff=0.22).align_to(ax, LEFT),
    )
    legend = VGroup(
        inline_text(r'$A = \{x > 40\}$', 43, ACCENT),
        inline_text(r'$B = \{x > y\}$', 43, NEXT),
        inline_text(r'$C = \{y > 40\}$', 43, WARN),
        inline_text(r'$AB$ · overlap', 43, ACCENT),
        inline_text(r'$A\cup C$ · union', 43, ACCENT),
    ).arrange(DOWN, aligned_edge=LEFT, buff=0.34)
    chart = VGroup(regions, lines, ax, ticks, labels)
    legend.next_to(chart, RIGHT, buff=0.75)
    return VGroup(chart, legend), regions, lines, legend


class Video(LessonScene):
    folder = HERE
    number = '1.1'
    section_title = 'Sample Space and Events'

    def construct(self):
        self.introduce()
        self.define_points()
        self.arrange_balls()
        self.compare_models()
        self.count_smokers()
        self.three_coins()
        self.couple_ages()
        self.bridge()
        self.combine_events()
        self.show_complement_rules()
        self.finish_lesson()

    def introduce(self):
        with self.seg('welcome'):
            self.show(title_card(self.number, self.section_title, self.lesson_k))
        with self.seg('site'):
            self.show(VGroup(
                sans('Aram Code Lab', 62, TEXT, 'BOLD'),
                bullet_list(['Full text and proofs', 'Problems with solutions', 'Runnable Python code']),
            ).arrange(DOWN, buff=0.54))
        with self.seg('question'):
            lines = VGroup(sans('What are we computing', 58, TEXT, 'BOLD'),
                           sans('probabilities of?', 58, ACCENT, 'BOLD')).arrange(DOWN, buff=0.24)
            self.show(lines)

        with self.seg('model_intro') as g:
            tiles = VGroup(*(experiment_card(name, icon) for name, icon in (
                ('Coin toss', coin_face().scale(0.38)),
                ('Dice', die(5).scale(0.88)),
                ('Cards', playing_card('A', NEXT).scale(1.15)),
                ('Random sample', person_icon().scale(1.7)),
                ('Phone calls', sans('☎', 60, ACCENT)),
            ))).arrange(RIGHT, buff=0.16)
            self.place(tiles)
            self.play(LaggedStart(*(FadeIn(tile) for tile in tiles), lag_ratio=0.24),
                      run_time=min(7.5, g.left() * 0.53))
            self.remove(*tiles)
            self.add(tiles)
        with self.seg('coin'):
            coin = coin_face()
            heading = sans('What counts as an outcome?', 48, TEXT, 'BOLD').next_to(coin, UP, buff=0.48)
            self.show(VGroup(heading, coin), run_time=0.5)
            edge = Ellipse(width=0.16, height=2.36, color=WARN, fill_color='#695020', fill_opacity=1).move_to(coin)
            center = coin.get_center()
            for angle in (22, -15, 8, 0):
                tilt = edge.copy().rotate(angle * np.pi / 180).move_to(center)
                self.play(Transform(coin, tilt), run_time=0.18)
            mark = sans('×', 90, DANGER, 'BOLD').next_to(coin, RIGHT, buff=0.35)
            self.play(FadeIn(mark), run_time=0.25)
            self.wait(0.45)
            self.play(FadeOut(mark), run_time=0.20)
            letters = VGroup(*(VGroup(card(2.24, 2.56), sans(symbol, 90, color, 'BOLD'))
                               for symbol, color in [('H', ACCENT), ('T', NEXT)])).arrange(RIGHT, buff=0.55)
            self.show(letters)
        with self.seg('age') as g:
            ruler = Line(LEFT * 4.7, RIGHT * 4.7, color=TEXT2, stroke_width=3)
            ticks = VGroup(*(Line(ORIGIN, DOWN * (0.38 if i % 5 == 0 else 0.17), color=MUTED)
                             .move_to(ruler.point_from_proportion(i / 20), aligned_edge=UP) for i in range(21)))
            labels = VGroup(*(mono(str(32 + i), 35, TEXT2).next_to(ticks[i * 5], DOWN, buff=0.18) for i in range(5)))
            needle = Arrow(UP * 0.78, ORIGIN, buff=0, color=ACCENT).next_to(ruler.point_from_proportion(0.570425), UP, buff=0.02)
            age = mono('34.2817…', 72, ACCENT).next_to(needle, UP, buff=0.22)
            self.show(VGroup(ruler, ticks, labels, needle, age))
            self.wait(g.left() * 0.38)
            target = ticks[10].get_top()
            self.play(needle.animate.next_to(target, UP, buff=0.02),
                      Transform(age, mono('34', 72, ACCENT).move_to(age).set_x(target[0])), run_time=0.55)

    def define_points(self):
        with self.seg('dice_intro'):
            self.show(sans('Simple and compound events', 56, TEXT, 'BOLD'))
        with self.seg('dice_sum') as g:
            tossed = VGroup(die(2).rotate(0.24), die(4).rotate(-0.31)).arrange(RIGHT, buff=0.65).scale(1.65)
            self.show(tossed, run_time=0.45)
            for turn in (0.75, -0.45, 0.17):
                self.play(tossed[0].animate.rotate(turn), tossed[1].animate.rotate(-turn), run_time=0.21)
            pairs = VGroup(*(dice_pair(n, 6 - n) for n in range(1, 6))).arrange(RIGHT, buff=0.45)
            cards = VGroup(*(SurroundingRectangle(pair, color=ACCENT, buff=0.13, corner_radius=0.13)
                             for pair in pairs))
            heading = pill('The sum is six', ACCENT, 39).next_to(pairs, UP, buff=0.45)
            display = VGroup(cards, pairs, heading)
            self.place(display)
            self.play(FadeIn(heading), LaggedStart(*(
                FadeIn(VGroup(tile, pair)) for tile, pair in zip(cards, pairs, strict=True)
            ), lag_ratio=0.28), run_time=min(7.2, g.left() * 0.48))
            self.remove(*cards, *pairs, heading)
            self.add(display)
        with self.seg('dice_odd') as g:
            matrix, intersection = dice_matrix()
            self.show(matrix, run_time=0.65)
            self.wait(min(2.9, g.left() * 0.24))
            self.play(Indicate(intersection, color=TEXT, scale_factor=1.12), run_time=1.15)
        with self.seg('definition') as g:
            definition = box('definition', 'Definition 1.1', [
                'The indecomposable outcomes are called sample points.',
                'Every possible outcome is represented by exactly one point.',
                r'The set of all points is the sample space, written $\Omega$.',
                'And an event is simply a set of sample points.',
            ])
            self.show(definition, step_time=min(1.45, g.left() / (len(definition.lines) + 2)))
        with self.seg('geometry') as g:
            dot = Dot(radius=0.15, color=ACCENT)
            line = Line(LEFT * 1.15, RIGHT * 1.15, color=ACCENT, stroke_width=4)
            primitive = VGroup(
                VGroup(dot, sans('Point', 36)).arrange(DOWN, buff=0.34),
                VGroup(line, sans('Line', 36)).arrange(DOWN, buff=0.34),
                VGroup(MathTex(r'\Omega', font_size=76, color=ACCENT),
                       sans('Sample space', 36)).arrange(DOWN, buff=0.29),
            ).arrange(RIGHT, buff=1.16, aligned_edge=DOWN)
            heading = sans('Primitive notions', 48, TEXT, 'BOLD').next_to(primitive, UP, buff=0.5)
            self.show(VGroup(heading, primitive))
            self.wait(g.left() * 0.64)
            self.show(inline_text(r'Define $\Omega$ before assigning probabilities.', 47))

    def arrange_balls(self):
        grid = arrangement_grid(ARRANGEMENTS)
        status = pill('27 distinct arrangements', ACCENT, 38)
        display = VGroup(grid, status).arrange(DOWN, buff=0.38)
        with self.seg('cells') as g:
            boxes, balls = cells_for(ARRANGEMENTS[22])
            formula = formula_pill(r'Each ball has 3 choices: $3\cdot3\cdot3=27$', 38).next_to(boxes, DOWN, buff=0.55)
            balls.shift(UP * 1.20)
            intro = VGroup(boxes, balls, formula)
            self.place(intro)
            self.play(FadeIn(boxes), FadeIn(balls), run_time=0.65)
            for ball in balls:
                self.wait(g.left() * 0.14)
                self.play(ball.animate.shift(DOWN * 1.20), run_time=0.65)
            self.play(FadeIn(formula), run_time=0.55)
            self.remove(boxes, balls, formula)
            self.add(intro)
        with self.seg('grid') as g:
            self.place(display)
            for tile in grid:
                tile.save_state().set_opacity(0)
            self.play(FadeIn(display), run_time=0.5)
            self.play(LaggedStart(*(tile.animate.restore() for tile in grid), lag_ratio=0.07), run_time=2.25)
            groups = (
                (range(1, 4), 'All three in one cell'),
                (range(4, 22), 'Two together, one elsewhere'),
                (range(22, 28), 'One ball in each cell'),
            )
            for labels, caption in groups:
                self.highlight(grid, status, labels, caption)
                self.wait(g.left() * 0.33)
        with self.seg('event_crowded'):
            self.highlight(grid, status, EVENTS['crowded'], 'Some cell has at least two balls')
        with self.seg('event_first'):
            self.highlight(grid, status, EVENTS['first'], 'The first cell is not empty')
        with self.seg('event_full'):
            self.highlight(grid, status, EVENTS['full'], 'Every cell is occupied')
        with self.seg('event_first_empty'):
            self.highlight(grid, status, EVENTS['first_empty'], 'First cell empty and some cell has two balls')
        with self.seg('event_empty'):
            self.highlight(grid, status, EVENTS['impossible'], r'Every cell has two balls · impossible event $\varnothing$')

    def highlight(self, grid, status, event, wording):
        selected = set(event)
        target = formula_pill(f'{wording}   {len(selected)}', 31).move_to(status)
        animations = []
        for index, tile in enumerate(grid, 1):
            on = index in selected
            frame = tile[0][0]
            animations.append(tile[-1].animate.set_color(ACCENT if on else MUTED).set_opacity(1 if on else 0.45))
            animations.append(frame.animate.set_stroke(ACCENT if on else BORDER2, width=3.2 if on else 1.4)
                              .set_fill(SELECTED if on else SURFACE, opacity=1))
            animations.append(tile[1].animate.set_opacity(1 if on else 0.28))
        self.play(Transform(status, target), *animations, run_time=0.65)

    def compare_models(self):
        with self.seg('formula') as g:
            formula = formula_pill(r'$r$ balls $\longrightarrow$ $n$ cells: $n^r$ points', 45)
            examples = VGroup(
                inline_text(r'4 balls in 3 cells: $3^4 = 81$', 40),
                inline_text(r'10 balls in 10 cells: $10^{10}$', 40),
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.33)
            block = VGroup(formula, examples).arrange(DOWN, buff=0.61)
            self.place(block)
            self.play(FadeIn(formula), run_time=0.6)
            self.wait(g.left() * 0.44)
            for example in examples:
                self.play(FadeIn(example), run_time=0.65)
                self.wait(g.left() * 0.43)
            self.remove(formula, *examples)
            self.add(block)
        with self.seg('schemes') as g:
            rows = [rf'{title}: {items} $\longrightarrow$ {bins}' for title, items, bins in SCHEMES]
            examples = bullet_list(rows, icons=scheme_icons(), size=37)
            self.show(examples, step_time=min(3.6, g.left() / 8))
        with self.seg('scheme_caution'):
            self.show(VGroup(
                sans('Same structure', 53, ACCENT, 'BOLD'),
                sans('Probabilities can differ.', 45, TEXT),
            ).arrange(DOWN, buff=0.43))

        with self.seg('collapse') as g:
            collapse_arrangements(self, ARRANGEMENTS, g)
        with self.seg('model_choice'):
            pass

    def count_smokers(self):
        with self.seg('smokers') as g:
            people = VGroup(*(person_icon() for _ in range(100))).arrange_in_grid(
                rows=5, cols=20, buff=(0.18, 0.23),
            )
            title = sans('Survey 100 people', 47, TEXT, 'BOLD').next_to(people, UP, buff=0.35)
            self.show(VGroup(title, people), run_time=0.7)
            self.wait(g.left() * 0.20)
            smokers = (person for i, person in enumerate(people) if (i * 37) % 100 < 54)
            self.play(*(person.animate.set_color(ACCENT) for person in smokers), run_time=1.0)
            self.wait(g.left() * 0.57)
            axis = Line(LEFT * 5.6, RIGHT * 5.6, color=TEXT2, stroke_width=2.4)
            points = VGroup(*(Dot(axis.point_from_proportion(i / 100), radius=0.042, color=MUTED)
                              for i in range(101)))
            ticks = VGroup(*(mono(str(i), 27, TEXT2).next_to(points[i], DOWN, buff=0.20)
                             for i in (0, 25, 50, 75, 100)))
            count = pill('101 possible counts', ACCENT, 34).next_to(axis, UP, buff=0.56)
            self.show(VGroup(axis, points, ticks, count))
        with self.seg('majority'):
            event = inline_text(r'Majority are smokers: $\{51,\ldots,100\}$', 42, ACCENT).move_to(count)
            self.play(Transform(count, event), *(point.animate.set_color(ACCENT) for point in points[51:]),
                      run_time=0.68)
        with self.seg('quadruples') as g:
            equation = MathTex(r'(M_s,F_s,M_n,F_n)', font_size=64, color=ACCENT)
            fields = VGroup(*(inline_text(label, 33) for label in (
                r'$M_s$ · male smokers', r'$F_s$ · female smokers',
                r'$M_n$ · male non-smokers', r'$F_n$ · female non-smokers',
            ))).arrange_in_grid(rows=2, cols=2, buff=(0.65, 0.30), col_alignments='ll')
            total = MathTex(r'M_s+F_s+M_n+F_n=100', font_size=46, color=TEXT)
            count = pill(f'{comb(103, 3):,} points', ACCENT, 46)
            note = sans('Counted in Lesson 2.2', 28, MUTED)
            block = VGroup(equation, fields, total, count, note).arrange(DOWN, buff=0.35)
            self.place(block)
            self.play(FadeIn(equation), FadeIn(fields), run_time=0.7)
            self.wait(g.left() * 0.30)
            self.play(FadeIn(total), run_time=0.55)
            self.wait(g.left() * 0.25)
            self.play(FadeIn(count), FadeIn(note), run_time=0.7)
            self.remove(*block)
            self.add(block)

    def three_coins(self):
        with self.seg('three_coins'):
            tiles = coin_outcome_cards(COIN_TOSSES)
            more_heads = pill('Two or more heads', ACCENT, 36)
            one_tail = pill('Exactly one tail', NEXT, 36)
            legend = VGroup(more_heads, one_tail).arrange(RIGHT, buff=0.34).next_to(tiles, DOWN, buff=0.50)
            self.place(VGroup(tiles, legend))
            self.play(FadeIn(tiles), run_time=0.65)
        with self.seg('heads_event'):
            teal = VGroup(*(SurroundingRectangle(tile, color=ACCENT, buff=0.05, corner_radius=0.17)
                            for outcome, tile in zip(COIN_TOSSES, tiles, strict=True) if outcome in MAJORITY_HEADS))
            self.play(FadeIn(more_heads), Create(teal), run_time=0.62)
        with self.seg('tail_event'):
            indigo = VGroup(*(RoundedRectangle(width=tile.width - 0.27, height=tile.height - 0.22,
                                                corner_radius=0.13, color=NEXT, stroke_width=2.8).move_to(tile)
                              for outcome, tile in zip(COIN_TOSSES, tiles, strict=True) if outcome in EXACTLY_ONE_TAIL))
            self.play(FadeIn(one_tail), Create(indigo), run_time=0.62)
            self.remove(tiles, more_heads, one_tail, teal, indigo)
            self.body = VGroup(tiles, legend, teal, indigo)
            self.add(self.body)

    def couple_ages(self):
        with self.seg('axes'):
            chart, regions, boundaries, legend = age_plane()
            self.place(chart)
            for item in (*regions, *boundaries, *legend):
                item.save_state().set_opacity(0)
            self.play(FadeIn(chart), run_time=0.6)
        for index, cue in enumerate(('age_a', 'age_b', 'age_c')):
            with self.seg(cue):
                self.play(regions[index].animate.restore(), boundaries[index].animate.restore(),
                          legend[index].animate.restore(), run_time=0.75)
        with self.seg('age_ab') as g:
            self.play(regions[3].animate.restore(), legend[3].animate.restore(),
                      regions[2].animate.set_fill(opacity=0.04), run_time=0.75)
            self.wait(g.left() * 0.59)
            self.play(regions[3].animate.set_fill(opacity=0),
                      regions[1].animate.set_fill(opacity=0), regions[2].animate.set_fill(opacity=0),
                      regions[4].animate.restore(), legend[4].animate.restore(), run_time=0.65)

    def bridge(self):
        with self.seg('bridge') as g:
            hands, panels, aces = bridge_hands((2, 1, 1, 0))
            headline = sans('52 cards · four players', 46, TEXT, 'BOLD').next_to(hands, UP, buff=0.38)
            footer = inline_text(r'$N_1$ · North has at least one ace', 36, ACCENT).next_to(hands, DOWN, buff=0.34)
            block = VGroup(headline, hands, footer)
            self.place(block)
            self.play(FadeIn(headline), LaggedStart(*(FadeIn(hand) for hand in hands), lag_ratio=0.36),
                      run_time=2.8)
            self.wait(g.left() * 0.52)
            self.play(FadeIn(footer), panels[0].animate.set_stroke(ACCENT, width=2.8),
                      *(Indicate(ace, color=WARN, scale_factor=1.16) for ace in aces), run_time=1.15)
            self.remove(headline, *hands, footer)
            self.add(block)
        with self.seg('bridge_union'):
            target = inline_text(r'$N_1\cup E_1\cup S_1\cup W_1 = \Omega$', 43, ACCENT).move_to(footer)
            self.play(Transform(footer, target), *(panel.animate.set_stroke(ACCENT, width=2.8) for panel in panels[:3]),
                      run_time=0.68)
        with self.seg('bridge_all'):
            hands, panels, _ = bridge_hands((1, 1, 1, 1))
            for panel in panels:
                panel.set_stroke(ACCENT, width=2.8)
            formula = inline_text(r'$N_1E_1S_1W_1$ · one ace per player', 39, ACCENT)
            self.show(VGroup(hands, formula).arrange(DOWN, buff=0.45))

    def event_view(self, diagram, label, predicate, *, color=ACCENT, outline=False):
        caption = inline_text(label, 42, color).next_to(diagram, DOWN, buff=0.38)
        self.show(VGroup(diagram, caption), run_time=0.52)
        diagram.choose(self, predicate, color, outline=outline)
        return caption

    def combine_events(self):
        with self.seg('events_equal') as g:
            self.event_view(EventDiagram(first_only=True),
                            r'$A=B$ if they contain exactly the same points', lambda a, b: a)
            self.wait(g.left() * 0.48)
            self.show(box('definition', 'Definitions 1.2–1.4', [
                r'$\varnothing$ · impossible event',
                r"$A'$ · complement",
                r'$AB=A\cap B$ · intersection',
                r'$A\cup B$ · union',
                r'$AB=\varnothing$ · mutually exclusive events',
            ]), run_time=0.38, step_time=0.29)
        with self.seg('empty'):
            empty = EventDiagram(first_only=True)
            empty[1].set_opacity(0)
            self.event_view(empty, r'$\varnothing$ · no points', lambda a, b: False)
        with self.seg('complement') as g:
            caption = self.event_view(EventDiagram(first_only=True), r"$A'$ · all points outside $A$",
                                      lambda a, b: not a, color=WARN, outline=True)
            self.wait(g.left() * 0.64)
            self.play(Transform(caption, inline_text(r"$\Omega'=\varnothing$", 46, WARN).move_to(caption)),
                      run_time=0.6)
        operations = (
            ('intersection', r'$AB=A\cap B$ · both events occur', lambda a, b: a and b),
            ('union', r'$A\cup B$ · at least one occurs', lambda a, b: a or b),
            ('exclusive', r'$AB=\varnothing$ · mutually exclusive', lambda a, b: a or b),
        )
        for cue, label, predicate in operations:
            with self.seg(cue):
                self.event_view(EventDiagram(distinct=cue == 'exclusive'), label, predicate)
        with self.seg('implies') as g:
            self.show(box('definition', 'Definition 1.5', [
                r'$A\subset B$ · $A$ implies $B$.',
                r"$B-A=BA'$ · $B$ happens but $A$ does not.",
            ]), step_time=0.5)
            self.wait(g.left() * 0.38)
            self.event_view(EventDiagram(nested=True), r'$A\subset B$ · every point of $A$ also belongs to $B$',
                            lambda a, b: a)
        with self.seg('coin_implies'):
            tiles = coin_outcome_cards(COIN_TOSSES)
            teal = VGroup(*(SurroundingRectangle(tile, color=ACCENT, buff=0.06, corner_radius=0.16)
                            for outcome, tile in zip(COIN_TOSSES, tiles, strict=True) if outcome in MAJORITY_HEADS))
            indigo = VGroup(*(RoundedRectangle(width=tile.width - 0.27, height=tile.height - 0.22,
                                                corner_radius=0.13, color=NEXT, stroke_width=2.8).move_to(tile)
                              for outcome, tile in zip(COIN_TOSSES, tiles, strict=True) if outcome in EXACTLY_ONE_TAIL))
            caption = inline_text(r'Exactly one tail $\implies$ two or more heads', 40).next_to(tiles, DOWN, buff=0.45)
            self.show(VGroup(tiles, teal, indigo, caption))
        with self.seg('difference'):
            self.event_view(EventDiagram(nested=True), r"$B-A=BA'$ · in $B$, outside $A$", lambda a, b: b and not a)
        with self.seg('omega_difference'):
            self.event_view(EventDiagram(first_only=True), r"$A'=\Omega-A$", lambda a, b: not a,
                            color=WARN, outline=True)
        with self.seg('exclusive_implies'):
            self.event_view(EventDiagram(distinct=True), r"$AB=\varnothing\ \Longrightarrow\ A\subset B'$",
                            lambda a, b: not b, color=WARN, outline=True)
        with self.seg('a_not_both'):
            self.event_view(EventDiagram(), r"$A-AB=AB'$ · $A$, but not both", lambda a, b: a and not b)

    def show_complement_rules(self):
        with self.seg('identity_one') as g:
            self.show(box('property', 'Property 1.1', [
                r"$(A\cup B)'=A'B'$",
                r"$(AB)'=A'\cup B'$",
                r"$A-AB=AB'$",
                r"$A\cup B=A\cup(B-AB)$",
            ]), step_time=0.40)
            self.wait(g.left() * 0.30)
            self.same_shading('outside_union', 'both_outside', r"(A\cup B)'", r"A'B'")
        with self.seg('identity_two'):
            self.same_shading('outside_intersection', 'either_outside', r"(AB)'", r"A'\cup B'")
        with self.seg('identity_three'):
            self.same_shading('a_minus_ab', 'a_and_outside_b', r'A-AB', r"AB'")
        with self.seg('identity_four'):
            self.same_shading('union', 'disjoint_union', r'A\cup B', r'A\cup(B-AB)', slide=True)
        with self.seg('identity_proof') as g:
            self.same_shading('outside_union', 'both_outside', r"(A\cup B)'", r"A'B'")
            self.wait(g.left() * 0.46)
            self.show(box('property', 'Check one point at a time', [
                r"$x\in(A\cup B)'$",
                r'$\Longleftrightarrow$ $x$ lies outside both $A$ and $B$',
                r"$\Longleftrightarrow$ $x\in A'B'$",
            ]), step_time=0.48)
        with self.seg('trap') as g:
            self.same_shading('outside_union', 'either_outside', r"(A\cup B)'", r"A'\cup B'", equal=False)
            self.wait(g.left() * 0.48)
            self.same_shading('outside_intersection', 'both_outside', r"(AB)'", r"A'B'", equal=False)

    def same_shading(self, left, right, left_formula, right_formula, *, equal=True, slide=False):
        diagrams = []
        for operation, formula in ((left, left_formula), (right, right_formula)):
            figure = EventDiagram()
            tinted = figure.shade(operation)
            figure.scale_to_fit_width(5.18)
            caption = MathTex(formula, font_size=49, color=TEXT2).next_to(figure, DOWN, buff=0.38)
            diagrams.append(VGroup(figure, caption))
        symbol = MathTex('=' if equal else r'\neq', font_size=62, color=TEXT if equal else WARN)
        row = VGroup(diagrams[0], symbol, diagrams[1]).arrange(RIGHT, buff=0.48)
        block = row if equal else VGroup(pill('Careful', WARN, 34), row).arrange(DOWN, buff=0.30)
        if slide:
            self.place(block)
            tinted[1].shift(RIGHT * 0.62)
            self.play(FadeIn(block), run_time=0.62)
            self.play(tinted[1].animate.shift(LEFT * 0.62), run_time=1.25)
        else:
            self.show(block, run_time=0.62)

    def finish_lesson(self):
        with self.seg('discrete_row') as g:
            sequence = sample_points(('H', 'TH', 'TTH', 'TTTH', '…'), cols=5)
            names = VGroup()
            for name, point in zip((r'E_1', r'E_2', r'E_3', r'E_4', r'\cdots'), sequence, strict=True):
                names.add(MathTex(name, font_size=48, color=ACCENT).next_to(point, UP, buff=0.30))
            numbered = VGroup(sequence, names)
            zero = VGroup(MathTex('E_0', font_size=46, color=WARN), sans('?', 39, WARN, 'BOLD'),
                          sans('No heads', 28, WARN)).arrange(DOWN, buff=0.15)
            zero.next_to(numbered, LEFT, buff=0.55)
            row = VGroup(zero, numbered)
            heading = sans('Toss a coin until the first head', 46, TEXT, 'BOLD').next_to(row, UP, buff=0.66)
            display = VGroup(row, heading)
            self.place(display)
            self.play(FadeIn(heading), run_time=0.6)
            self.wait(g.left() * 0.32)
            outcomes = [VGroup(point, name) for point, name in zip(sequence, names, strict=True)]
            self.play(LaggedStart(*(FadeIn(outcome) for outcome in outcomes), lag_ratio=0.36), run_time=3.2)
            self.wait(g.left() * 0.31)
            self.play(FadeIn(zero), run_time=0.65)
            self.remove(*outcomes, heading, zero)
            self.add(display)
        with self.seg('discrete_definition'):
            self.show(box('definition', 'Definition 1.6', [
                'A sample space is discrete if it has finitely many points',
                r'or its points can be arranged in a sequence $E_1, E_2, \dots$',
            ]), step_time=0.85)
        self.play_tournament()
        with self.seg('code') as g:
            self.show(code_cell(CODE, OUTPUT), step_time=min(1.90, g.left() / 12))
        with self.seg('code_check'):
            pass
        with self.seg('recall'):
            ideas = key_ideas(KEY_IDEAS, pause=5)
            self.place(ideas)
            ideas.start_recall(self)
        ideas.countdown(self)
        with self.seg('ideas') as g:
            ideas.reveal_items(self, step_time=g.left() * 0.22)
            self.remove(*ideas.submobjects)
            self.add(ideas)
        with self.seg('end'):
            self.show(end_card('Probabilities in discrete sample spaces'))

    def play_tournament(self):
        with self.seg('tournament') as g:
            players = VGroup(*(VGroup(card(2.30, 1.50), mono(letter, 66, color))
                               for letter, color in zip('abc', (ACCENT, NEXT, WARN), strict=True)))
            players.arrange(RIGHT, buff=0.37)
            caption = sans('a plays b · c waits', 48, TEXT, 'SEMIBOLD').next_to(players, DOWN, buff=0.52)
            self.show(VGroup(players, caption))
            self.wait(g.left() * 0.48)
            tree = tournament_tree()
            self.place(tree)
            self.play(FadeIn(tree[0]), FadeIn(tree[2]), Create(tree[1][0]),
                      LaggedStart(*(FadeIn(node) for node in tree[1][1]), lag_ratio=0.14), run_time=2.45)
            self.remove(*tree[1][1], tree[1][0], tree[0], tree[2])
            self.add(tree)
        with self.seg('tournament_outcomes') as g:
            heading = sans('Finite outcomes', 50, TEXT, 'BOLD')
            columns = []
            for player, outcomes in zip('ab', TOURNAMENT_FINITE, strict=True):
                rows = VGroup(*(mono(outcome, 40, TEXT2) for outcome in (*outcomes, '…')))
                rows.arrange(DOWN, buff=0.14)
                label = sans(f'Starting with {player}', 30, ACCENT, 'SEMIBOLD').next_to(rows, UP, buff=0.22)
                contents = VGroup(label, rows)
                columns.append(VGroup(card(3.5, contents.height + 0.42).move_to(contents), contents))
            row = VGroup(*columns).arrange(RIGHT, buff=0.42)
            self.show(VGroup(heading, row).arrange(DOWN, buff=0.31))
            for side, index in ((0, 0), (0, 1), (0, 2), (1, 0)):
                self.wait(g.left() * 0.16)
                self.play(Indicate(columns[side][1][1][index], color=ACCENT, scale_factor=1.13), run_time=0.67)
        with self.seg('tournament_endless'):
            title = sans('Two endless outcomes', 50, TEXT, 'BOLD')
            rows = tournament_sequences(TOURNAMENT_ENDLESS)
            self.show(VGroup(title, rows).arrange(DOWN, buff=0.55), run_time=0.55)
        with self.seg('tournament_list') as g:
            ordered = (*TOURNAMENT_ENDLESS, 'aa', 'bb', 'acc', 'bcc', 'acbb', 'bcaa')
            title = sans('Every outcome gets a number', 46, TEXT, 'BOLD')
            numbered = VGroup(*(mono(f'{number:>2}  {name}', 37, NEXT if number <= 2 else TEXT2)
                                for number, name in enumerate(ordered, 1)))
            numbered.arrange_in_grid(rows=4, cols=2, buff=(0.64, 0.20), col_alignments='ll')
            heading = VGroup(title, numbered, mono('…', 40, MUTED)).arrange(DOWN, buff=0.38)
            self.place(heading)
            self.play(FadeIn(title),
                      LaggedStart(*(FadeIn(item) for item in numbered), lag_ratio=0.24),
                      run_time=min(5, g.left() * 0.46))
            self.play(FadeIn(heading[-1]), run_time=0.40)
            self.remove(title, *numbered, heading[-1])
            self.add(heading)
        with self.seg('discrete_caution') as g:
            chart, regions, boundaries, legend = age_plane()
            chart[0].remove(regions)
            chart[0].remove(boundaries)
            chart.remove(legend)
            title = sans('Ages form a region of the plane', 41, TEXT, 'BOLD').next_to(chart, UP, buff=0.26)
            self.show(VGroup(chart, title))
            self.wait(g.left() * 0.50)
            self.show(VGroup(
                inline_text(r'Discrete sample spaces: add probabilities of points.', 38),
                inline_text(r'Continuous models: use integrals.', 38),
            ).arrange(DOWN, buff=0.42))
