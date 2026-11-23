"""Lesson 2: Probabilities in Discrete Sample Spaces."""

import sys
from math import log10, sqrt
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Circle, Ellipse, Create, DashedLine, Dot, FadeIn, FadeOut,
    LaggedStart, Line, MathTex, Rectangle, RoundedRectangle, SurroundingRectangle,
    Transform, TransformFromCopy, VGroup, VMobject,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))

from brand import ACCENT, BORDER2, MUTED, NEXT, SURFACE, TEXT, TEXT2, WARN, axes, card, mono, pill, sans
from data import (
    ARRANGEMENTS, BE, BOOLE_BOUND, CODE, COIN_A, COIN_B, COIN_TOSSES, COIN_WEIGHTS,
    COINS_TWO, CONFIGURATIONS, BOTH_ODD, DICE, DICE_WEIGHTS, EXACT_SIX, FREQUENCY_BAND,
    GROUP_HEADS, GROUP_HISTOGRAM, GROUP_SIZE, IN_BAND, KEY_IDEAS, MASS_EVENT, MB,
    MB_LABELS, ONE_SIX, OUTPUT, POINT_MASSES, PREFIX, RUNNING_HEADS, SIMULATED_OCCUPIED,
    SUM_COUNTS, SUM_SIX, THROWS, TOURNAMENT_ENDLESS, TOURNAMENT_FINITE, WEIGHT_COUNTS, WEIGHTS,
)
from lesson_kit import (
    LessonScene, box, bullet_list, code_cell, derivation, end_card, inline_text, key_ideas, title_card,
)
from prob_visuals import (
    arrangement, arrangement_grid, coin_outcome_cards, collapse_arrangements, dice_matrix, formula_pill,
    tournament_sequences,
)


EVENT_TITLES = {
    'crowded': 'Some cell has at least two balls',
    'occupied': 'Every cell is occupied',
    'first': 'The first cell is not empty',
    'together': 'All three in one cell',
}


def fraction(numerator, denominator=None):
    if denominator is None:
        numerator, denominator = numerator.numerator, numerator.denominator
    return rf'\tfrac{{{numerator}}}{{{denominator}}}'


def equation(text, size=47, color=TEXT):
    return MathTex(text, font_size=size, color=color)


def exact_box(kind, title, lines):
    """The title of the fundamental convention."""
    result = box(kind, title, lines)
    if title == 'Fundamental convention':
        heading = sans(title, 44, ACCENT, 'BOLD')
        result.heading.become(heading.move_to(result.heading).align_to(result.heading, LEFT))
    return result


def stack_content(*parts, gap=0.42):
    return VGroup(*parts).arrange(DOWN, buff=gap)


def labeled_card(visual, label, width=3.55, height=2.55):
    panel = card(width, height)
    words = sans(label, 33, TEXT, 'SEMIBOLD').next_to(visual, DOWN, buff=0.36)
    contents = VGroup(visual, words).move_to(panel)
    return VGroup(panel, contents)


def fair_coin_face(color=ACCENT):
    disc = Circle(radius=0.69, color=color, fill_opacity=0.12, stroke_width=3)
    return VGroup(disc, mono('H', 47, color, 'BOLD').move_to(disc))


def weighted_grid():
    grid = arrangement_grid(ARRANGEMENTS)
    for tile in grid:
        tile.add(equation(fraction(1, len(ARRANGEMENTS)), 23, TEXT2).next_to(tile[-1], DOWN, buff=0.08))
    grid.arrange_in_grid(rows=3, cols=9, buff=(0.22, 0.15))
    return grid


def comparison_card(*, decimals=True):
    """Compare the same three outcomes under both models."""
    header = VGroup(sans('Event', 31, TEXT, 'BOLD'), sans('MB', 35, ACCENT, 'BOLD'),
                    sans('BE', 35, NEXT, 'BOLD'))
    rows = VGroup(header)
    for key in ('occupied', 'together', 'crowded'):
        left = fraction(MB[key])
        if decimals:
            left += rf'\approx {float(MB[key]):.2f}'
        rows.add(VGroup(sans(EVENT_TITLES[key], 30, TEXT2), equation(left, 42, ACCENT),
                        equation(fraction(BE[key]), 42, NEXT)))
    contents = VGroup(*(cell for row in rows for cell in row)).arrange_in_grid(
        rows=4, cols=3, buff=(0.60, 0.38), col_alignments='lcc',
    )
    panel = card(contents.width + 0.72, contents.height + 0.55).move_to(contents)
    return VGroup(panel, contents)


def weight_table():
    counts = [3, 2, 1]
    headings = []
    for weight, maximum in zip(WEIGHTS, counts, strict=True):
        cells = next(cells for cells in CONFIGURATIONS if max(cells) == maximum)
        cells = tuple(sorted(cells, reverse=True))
        tile = arrangement(tuple('*' * count for count in cells))
        count = WEIGHT_COUNTS[weight]
        headings.append(stack_content(tile, sans(f'{count} configuration' + ('s' if count != 1 else ''),
                                                 26, MUTED), gap=.16))
    mb_row = [
        equation(fraction(weight, len(ARRANGEMENTS)) +
                 ('' if weight == 1 else '=' + fraction(WEIGHTS[weight])), 37, ACCENT)
        for weight in WEIGHTS
    ]
    be_row = [equation(fraction(1, len(CONFIGURATIONS)), 38, NEXT) for _ in WEIGHTS]
    named_be = [sans('Bose–Einstein', 31, NEXT, 'BOLD'), *be_row]
    cells = [
        sans('Configuration', 29, TEXT, 'BOLD'), *headings,
        sans(f'From {len(ARRANGEMENTS)} arrangements', 28, ACCENT), *mb_row,
        *named_be,
    ]
    contents = VGroup(*cells).arrange_in_grid(rows=3, cols=4, buff=(0.52, 0.34), col_alignments='lccc')
    panel = card(contents.width + 0.75, contents.height + 0.52).move_to(contents)
    return VGroup(panel, contents), VGroup(*named_be)


def frequency_plot():
    ax, ticks = axes((0, 4, 1), (0, 1, 0.25), 10.8, 3.65, yt=(0, .25, .5, .75, 1), size=26)
    for power in range(5):
        ticks.add(mono(f'{10**power:,}', 27, TEXT2).next_to(ax.c2p(power, 0), DOWN, buff=0.14))
    x_label = sans('Number of tosses (log scale)', 28, MUTED).next_to(ticks, DOWN, buff=0.26)
    y_label = sans('Fraction of heads', 32, TEXT, 'SEMIBOLD').next_to(ax, UP, buff=0.27).align_to(ax, LEFT)
    expected = DashedLine(ax.c2p(0, .5), ax.c2p(4, .5), color=WARN, stroke_width=2.4)
    # Subsample in log space for the drawing; all headline counts are exact.
    sample_steps = sorted(set(np.geomspace(1, THROWS, 1300).astype(int)) | set(PREFIX))
    positions = [ax.c2p(log10(n), RUNNING_HEADS[n - 1] / n) for n in sample_steps]
    line = VMobject(color=ACCENT, stroke_width=3.1).set_points_as_corners(positions)
    labels = VGroup(*(pill(f'{heads:,}/{n:,}', ACCENT, 30) for n, heads in PREFIX.items())).arrange(RIGHT, buff=0.28)
    labels.next_to(x_label, DOWN, buff=0.24)
    points = VGroup(*(Dot(ax.c2p(log10(n), heads / n), radius=.07, color=ACCENT) for n, heads in PREFIX.items()))
    base = VGroup(ax, ticks, expected, x_label, y_label)
    return VGroup(base, line, points, labels), base, line, points, labels


def group_plot():
    lo, hi = min(GROUP_HEADS), max(GROUP_HEADS)
    max_row = max(GROUP_HISTOGRAM.values())
    ax, ticks = axes((lo - 1, hi + 1, 1), (0, max_row + 1, 2), 11.8, 3.25,
                    xt=(lo, *FREQUENCY_BAND, hi), yt=tuple(range(2, max_row + 1, 2)), size=25)
    band_min, band_max = FREQUENCY_BAND
    a, b = ax.c2p(band_min - .48, 0), ax.c2p(band_max + .48, max_row + .65)
    band = Rectangle(width=b[0]-a[0], height=b[1]-a[1], fill_color=ACCENT, fill_opacity=.13,
                     stroke_width=0).move_to((a+b)/2)
    points = VGroup(*(Dot(ax.c2p(heads, height), radius=.070,
                          color=ACCENT if band_min <= heads <= band_max else TEXT2)
                      for heads, count in sorted(GROUP_HISTOGRAM.items())
                      for height in range(1, count + 1)))
    label = sans(f'Heads per group of {GROUP_SIZE}', 31, TEXT2).next_to(ticks, DOWN, buff=0.29)
    count = pill(f'{IN_BAND} of {len(GROUP_HEADS)} groups in {band_min}–{band_max}', ACCENT, 33)
    count.next_to(label, DOWN, buff=0.34)
    return VGroup(band, ax, ticks, points, label, count)


def mass_points():
    points = VGroup()
    for i, mass in enumerate(POINT_MASSES, 1):
        dot = Dot(radius=.58 * sqrt(float(mass / max(POINT_MASSES))), color=MUTED)
        label = equation(f'E_{i}', 37, TEXT2)
        probability = equation(fraction(mass), 39, ACCENT)
        anchor = Rectangle(width=1.43, height=2.18, stroke_width=0)
        label.next_to(anchor.get_top(), DOWN, buff=.08)
        dot.move_to(anchor)
        probability.next_to(anchor.get_bottom(), UP, buff=.07)
        points.add(VGroup(anchor, dot, label, probability))
    return points.arrange(RIGHT, buff=.22)


class UnionDots(VGroup):
    """Disjoint or overlapping event outlines over the same sample space."""

    def __init__(self, *, separated=False, many=False):
        self.universe = card(8.7, 4.72)
        radius = 1.46
        distance = 1.72 if separated else 1.03
        centers = [-distance * RIGHT, distance * RIGHT]
        colors = [ACCENT, NEXT]
        if many:
            centers.append(DOWN * .63 + RIGHT * .12)
            colors.append(WARN)
        self.regions = VGroup()
        for i, (center, color) in enumerate(zip(centers, colors, strict=True), 1):
            outline = Circle(radius=radius, color=color, fill_opacity=.10, stroke_width=3).move_to(center)
            label = equation(f'A_{i}', 36, color).next_to(outline.get_top(), UP, buff=.22)
            if i == 3:
                label.next_to(outline.get_bottom(), UP, buff=.07)
            self.regions.add(VGroup(outline, label))

        self.locations = [np.array([x, y, 0]) for y in (-1.63, -.84, -.05, .72, 1.56)
                          for x in (-3.57, -2.70, -1.74, -.83, 0, .83, 1.74, 2.70, 3.57)]
        self.membership = [tuple(np.linalg.norm(point - center) < radius for center in centers) for point in self.locations]
        self.dots = VGroup(*(Dot(point, radius=.067, color=MUTED) for point in self.locations))
        omega = equation(r'\Omega', 36, TEXT2).move_to([3.87, 1.94, 0])
        super().__init__(self.universe, self.regions, self.dots, omega)

    def highlight(self, scene, column, color):
        changes = []
        for dot, flags in zip(self.dots, self.membership, strict=True):
            if flags[column]:
                animation = dot.animate.set_color(color)
                if column == 1 and flags[0]:
                    animation.set_stroke(ACCENT, width=2.2)
                changes.append(animation)
        scene.play(*changes, run_time=.60)

    def overlap_badges(self):
        return VGroup(*(pill('×2', WARN, 23).scale(.66).next_to(dot, RIGHT, buff=.065)
                        for dot, (a, b) in zip(self.dots, self.membership, strict=True) if a and b))


def coin_probabilities(outcomes):
    tiles = coin_outcome_cards(outcomes)
    for tile in tiles:
        tile[1].shift(UP * .23)
        label = equation(fraction(1, len(outcomes)), 31, ACCENT).move_to(tile[0]).shift(DOWN * .29)
        tile.add(label)
    return tiles


def sums_chart():
    columns = VGroup()
    for total, count in SUM_COUNTS.items():
        matching = [(a, b) for a, b in DICE if a + b == total]
        color = ACCENT if total == 7 else TEXT2
        pairs = VGroup(*(VGroup(card(.93, .55), equation(f'({a},{b})', 22, color)) for a, b in matching))
        pairs.arrange(DOWN, buff=.11)
        floor = mono(str(total), 37, color)
        pairs.next_to(floor, UP, buff=.24)
        label = equation(fraction(count, len(DICE)), 31, color).next_to(floor, DOWN, buff=.18)
        if total not in (min(SUM_COUNTS), 7, max(SUM_COUNTS)):
            label.set_opacity(0)
        columns.add(VGroup(floor, label, pairs))
    columns.arrange(RIGHT, buff=.20, aligned_edge=DOWN)
    return columns


def simulation_bars():
    rows = VGroup()
    for label, result, exact, color in zip(('Maxwell–Boltzmann', 'Bose–Einstein'), SIMULATED_OCCUPIED,
                                           (MB['occupied'], BE['occupied']), (ACCENT, NEXT), strict=True):
        title = sans(label, 38, color, 'BOLD')
        track = Rectangle(width=8.3, height=.40, fill_color=SURFACE, fill_opacity=1,
                          stroke_color=BORDER2, stroke_width=1)
        fill = Rectangle(width=8.3 * float(result), height=.40, fill_color=color,
                         fill_opacity=.84, stroke_width=0).move_to(track, aligned_edge=LEFT)
        value = inline_text(rf'${float(result):.3f}$ · exact ${fraction(exact)}$', 36, color)
        bar = VGroup(track, fill)
        bar.next_to(title, DOWN, buff=.17).align_to(title, LEFT)
        value.next_to(bar, DOWN, buff=.15).align_to(track, LEFT)
        rows.add(VGroup(title, bar, value))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=.53)
    heading = sans('Every cell occupied', 47, TEXT, 'BOLD')
    return stack_content(heading, rows, gap=.55)


class Video(LessonScene):
    folder = str(HERE)
    lesson_k = 2
    number = '1.2'
    section_title = 'Probabilities in Discrete Sample Spaces'

    def construct(self):
        self.welcome()
        self.models_in_practice()
        self.distinguishable()
        self.indistinguishable()
        self.frequencies()
        self.rules()
        self.event_probability()
        self.unions()
        self.dice_union()
        self.boole()
        self.equally_likely()
        self.dice_sums()
        self.code_lab()
        self.finish_lesson()

    def beat(self, cue, share):
        self.wait(max(.08, share * cue.left()))

    def welcome(self):
        with self.seg('welcome'):
            self.show(title_card(self.number, self.section_title, self.lesson_k))
        with self.seg('recap'):
            grid = arrangement_grid(ARRANGEMENTS).scale(.76)
            self.show(stack_content(grid, pill(f'Ω: {len(ARRANGEMENTS)} points', ACCENT, 35)))

    def models_in_practice(self):
        with self.seg('like_lengths') as cue:
            ruler = Rectangle(width=2.4, height=.55, color=ACCENT, fill_opacity=.15)
            ticks = VGroup(*(Line(ruler.get_left() + RIGHT * (i * .22 + .22) + UP * .27,
                                  ruler.get_left() + RIGHT * (i * .22 + .22) + UP * (.07 if i % 2 else -.04),
                                  color=ACCENT, stroke_width=2) for i in range(10)))
            weight = RoundedRectangle(width=1.32, height=1.04, corner_radius=.24,
                                      color=NEXT, fill_opacity=.15)
            weight.add(Circle(radius=.24, color=NEXT, stroke_width=3).next_to(weight, UP, buff=0))
            cards = VGroup(labeled_card(VGroup(ruler, ticks), 'Length'),
                           labeled_card(weight, 'Mass'),
                           labeled_card(fair_coin_face(), 'Probability')).arrange(RIGHT, buff=.31)
            self.place(cards)
            for tile in cards:
                self.play(FadeIn(tile), run_time=.60)
                self.beat(cue, .20)
            self.remove(*cards)
            self.add(cards)

        with self.seg('fair_coin') as cue:
            values = VGroup(*(equation(rf'\mathrm{{{side}}}:\ {fraction(COIN_WEIGHTS[0])}', 54, color)
                              for side, color in zip('HT', (ACCENT, NEXT), strict=True))).arrange(RIGHT, buff=.66)
            self.show(stack_content(fair_coin_face(), values))
            self.beat(cue, .35)
            tiles = coin_probabilities(COIN_TOSSES)
            self.show(stack_content(tiles, formula_pill(r'$2^n$ outcomes, each $1/2^n$', 36)))

        with self.seg('model_use') as cue:
            coin = fair_coin_face(WARN)
            deck = VGroup()
            for index, label in enumerate(('7', '9', 'J', 'Q', 'A')):
                face = card(.80, 1.15).rotate((index-2)*.07).shift(RIGHT*index*.34)
                corner = face.get_corner(UP + LEFT) + RIGHT*.18 + DOWN*.36
                deck.add(VGroup(face, mono(label, 26, WARN if index >= 2 else TEXT2, 'BOLD')
                                .move_to(corner).rotate((index-2)*.07)))
            row = VGroup(labeled_card(coin, 'A real coin'),
                         labeled_card(deck, 'A shuffled deck')).arrange(RIGHT, buff=.40)
            caption = sans('Departures from the model tell us something', 34, TEXT2)
            self.place(stack_content(row, caption))
            self.play(FadeIn(row), run_time=.65)
            self.beat(cue, .54)
            self.play(FadeIn(caption), run_time=.60)
            self.remove(row, caption)
            self.add(self.body)

    def distinguishable(self):
        with self.seg('mb_intro') as cue:
            self.show(box('example', 'Example 1.9 · distinguishable balls', [
                f'Each of the ${len(ARRANGEMENTS)}$ arrangements has the same probability.',
            ]))
            self.beat(cue, .37)
            self.show(stack_content(weighted_grid(), pill('Maxwell–Boltzmann', ACCENT, 34)))

        with self.seg('mb_events') as cue:
            grid = weighted_grid()
            first = sans(EVENT_TITLES['crowded'], 34, TEXT, 'SEMIBOLD')
            tally = equation(fraction(len(MB_LABELS['crowded']), len(ARRANGEMENTS)) + '=' +
                             fraction(MB['crowded']), 38, ACCENT)
            caption = stack_content(first, tally, gap=.13)
            self.show(stack_content(grid, caption, gap=.35))
            for key in ('crowded', 'occupied', 'first'):
                labels = MB_LABELS[key]
                unsimplified = fraction(len(labels), len(ARRANGEMENTS))
                reduced = fraction(MB[key])
                heading = sans(EVENT_TITLES[key], 34, TEXT, 'SEMIBOLD').move_to(first)
                value = equation(unsimplified if unsimplified == reduced else
                                 unsimplified + '=' + reduced, 38, ACCENT).move_to(tally)
                changes = [tile[0][0].animate.set_stroke(ACCENT if index in labels else BORDER2)
                           .set_fill(ACCENT if index in labels else SURFACE, opacity=.20 if index in labels else 1)
                           for index, tile in zip(ARRANGEMENTS, grid, strict=True)]
                self.play(*changes, Transform(first, heading), Transform(tally, value), run_time=.66)
                self.beat(cue, .31)

    def indistinguishable(self):
        with self.seg('be_collapse') as cue:
            collapse_arrangements(self, ARRANGEMENTS, cue, pace=.72)
        with self.seg('be_weights') as cue:
            self.show(box('example', 'Example 1.10 · indistinguishable balls', [
                f'Keep the probabilities from the ${len(ARRANGEMENTS)}$ arrangements.',
            ]))
            self.beat(cue, .12)
            table, second_row = weight_table()
            products = '+'.join(rf'{count}\cdot{fraction(WEIGHTS[weight])}'
                                for weight, count in WEIGHT_COUNTS.items())
            common = max((WEIGHTS[w] * n).denominator for w, n in WEIGHT_COUNTS.items())
            contributions = '+'.join(fraction(int(WEIGHTS[w] * n * common), common)
                                     for w, n in WEIGHT_COUNTS.items())
            formula = derivation([products + '=' + contributions + '=1'])
            block = stack_content(table, formula)
            self.place(block)
            second_row.set_opacity(0)
            self.play(FadeIn(table), run_time=.8)
            self.beat(cue, .62)
            formula.reveal(self, run_time=.8)
            self.remove(table, *formula.submobjects)
            self.add(block)

        with self.seg('be_equal') as cue:
            table, second_row = weight_table()
            caption = pill('Bose–Einstein', NEXT, 35)
            block = stack_content(table, caption)
            self.place(block)
            second_row.set_opacity(0)
            self.play(FadeIn(table), run_time=.55)
            self.beat(cue, .33)
            self.play(second_row.animate.set_opacity(1).shift(UP*.10), FadeIn(caption), run_time=.8)
            self.remove(table, *second_row, second_row, caption)
            self.add(block)
        with self.seg('be_compare'):
            self.show(comparison_card())
        with self.seg('be_lesson'):
            heading = stack_content(sans('The sample space does not decide', 54, TEXT, 'BOLD'),
                                    sans('the probabilities.', 55, ACCENT, 'BOLD'), gap=.14)
            note = sans('Which model fits is a question of experience, not of logic.', 33, TEXT2)
            self.show(stack_content(heading, note, gap=.51))

    def frequencies(self):
        with self.seg('frequency_idea'):
            self.show(stack_content(bullet_list(['Repeat the experiment many times'], size=40),
                                    formula_pill(r'$\dfrac{\text{trials in which }A\text{ occurs}}{\text{all trials}}'
                                                 r'\ \approx\ \mathbf{P}\{A\}$', 42)))
        with self.seg('frequency_run') as cue:
            block, base, line, points, labels = frequency_plot()
            self.place(block)
            self.play(FadeIn(base), Create(line), run_time=1.45)
            for dot, label in zip(points, labels, strict=True):
                self.beat(cue, .18)
                self.play(FadeIn(dot), FadeIn(label), run_time=.52)
            self.remove(base, line, *points, *labels)
            self.add(block)
        with self.seg('frequency_groups'):
            self.show(group_plot())

    def rules(self):
        with self.seg('convention') as cue:
            self.show(mass_points())
            self.beat(cue, .45)
            self.show(exact_box('definition', 'Fundamental convention', [
                r'$\mathbf{P}\{E_i\} \ge 0$',
                r'$\mathbf{P}\{E_1\}+\mathbf{P}\{E_2\}+\dots = 1 \qquad (1.1)$',
            ]))
        with self.seg('zero_points'):
            rows = tuple('  '.join(outcomes[:3]) + '  …' for outcomes in TOURNAMENT_FINITE)
            finite = labeled_card(tournament_sequences(rows, 34, TEXT2, .35),
                                  'Finite outcomes', width=5.60, height=2.95)
            sequences = tournament_sequences(TOURNAMENT_ENDLESS, 36, NEXT, .35)
            labels = VGroup(*(equation(r'P=0', 35, ACCENT).next_to(text, RIGHT, buff=.27)
                              for text in sequences))
            examples = VGroup(sequences, labels)
            endless = labeled_card(examples, 'Endless outcomes', width=5.25, height=2.95)
            self.show(stack_content(sans('The tournament', 47, TEXT, 'BOLD'),
                                    VGroup(finite, endless).arrange(RIGHT, buff=.35)))

    def event_probability(self):
        with self.seg('event_sum') as cue:
            points = mass_points()
            selected = VGroup(*(points[index] for index in MASS_EVENT))
            outline = SurroundingRectangle(selected, color=ACCENT, buff=.12, corner_radius=.20)
            heading = equation('A', 45, ACCENT).next_to(outline, UP, buff=.14)
            mass = sum(POINT_MASSES[index] for index in MASS_EVENT)
            bar = VGroup(*(Rectangle(width=9 * float(POINT_MASSES[index]), height=.45, color=ACCENT,
                                      fill_opacity=.34 + i * .18) for i, index in enumerate(MASS_EVENT)))
            bar.arrange(RIGHT, buff=.02).next_to(points, DOWN, buff=.32)
            total = equation(r'\mathbf{P}\{A\}=' + fraction(mass), 42, ACCENT).next_to(bar, DOWN, buff=.20)
            block = VGroup(points, outline, heading, bar, total)
            self.place(block)
            self.play(FadeIn(points), FadeIn(outline), FadeIn(heading), run_time=.65)
            for point in selected:
                point[1].set_color(ACCENT)
            self.beat(cue, .22)
            self.play(*(TransformFromCopy(point[1], part) for point, part in zip(selected, bar, strict=True)),
                      FadeIn(total), run_time=.8)
            self.remove(points, outline, heading, *bar, total)
            self.add(block)
            self.beat(cue, .36)
            self.show(box('definition', 'Definition 1.7', [
                r'$\mathbf{P}\{A\}=\sum_{E_i\in A}\mathbf{P}\{E_i\}$',
            ]))
        with self.seg('consequences') as cue:
            self.show(derivation([
                r'\mathbf{P}\{\Omega\}=1',
                r'\mathbf{P}\{\varnothing\}=0',
                r'0\le\mathbf{P}\{A\}\le1 \qquad (1.2)',
            ]), step_time=min(3.4, cue.left()*.23))

    def unions(self):
        with self.seg('union_question'):
            self.show(UnionDots())
        with self.seg('union_overcount') as cue:
            dots = UnionDots()
            inequality = equation(r'\mathbf{P}\{A_1\cup A_2\}\le\mathbf{P}\{A_1\}+\mathbf{P}\{A_2\}\qquad(1.3)', 42)
            self.place(stack_content(dots, inequality, gap=.29))
            self.play(FadeIn(dots), run_time=.57)
            self.beat(cue, .12)
            dots.highlight(self, 0, ACCENT)
            self.beat(cue, .15)
            dots.highlight(self, 1, NEXT)
            badges = dots.overlap_badges()
            self.play(FadeIn(badges), run_time=.65)
            self.beat(cue, .38)
            self.play(FadeIn(inequality), run_time=.66)

        with self.seg('union_theorem') as cue:
            self.beat(cue, .11)
            self.play(FadeOut(badges), run_time=.62)
            self.remove(dots, inequality)
            self.add(self.body)
            self.beat(cue, .18)
            self.show(box('theorem', 'Theorem 1.1', [
                r'$\mathbf{P}\{A_1\cup A_2\} = \mathbf{P}\{A_1\} + \mathbf{P}\{A_2\} - \mathbf{P}\{A_1A_2\}\quad(1.4)$',
            ]))

        with self.seg('union_coins') as cue:
            example = box('example', 'Example 1.11', ['At least one head in two tosses'])
            tiles = coin_probabilities(COINS_TWO)
            legend = VGroup(pill('Heads on the first toss', ACCENT, 29),
                            pill('Heads on the second toss', NEXT, 29)).arrange(RIGHT, buff=.24)
            result = derivation(['+'.join(fraction(p) for p in COIN_WEIGHTS[:2]) + '-' +
                                 fraction(COIN_WEIGHTS[2]) + '=' + fraction(COIN_WEIGHTS[3])])
            block = stack_content(example, tiles, legend, result, gap=.28)
            self.place(block)
            self.play(FadeIn(example), FadeIn(tiles), run_time=.72)
            self.beat(cue, .24)
            outlines = VGroup()
            for event, color, pad, label in zip((COIN_A, COIN_B), (ACCENT, NEXT), (.04, .105), legend, strict=True):
                group = VGroup(*(SurroundingRectangle(tile, color=color, buff=pad, corner_radius=.16,
                                                      stroke_width=3)
                                 for key, tile in zip(COINS_TWO, tiles, strict=True) if key in event))
                self.play(FadeIn(group), FadeIn(label), run_time=.68)
                outlines.add(group)
                self.beat(cue, .23)
            result.reveal(self, run_time=.65)
            self.remove(example, tiles, *legend, *outlines, *result.submobjects)
            self.body.add(outlines)
            self.add(self.body)

    def dice_union(self):
        with self.seg('dice_union') as cue:
            matrix, _ = dice_matrix()
            intersection = [outcome for pair, outcome in zip(DICE, matrix[1], strict=True)
                            if pair in SUM_SIX & BOTH_ODD]
            example = box('example', 'Example', ['Sum six or both faces odd'])
            a, b, overlap, union = (fraction(int(p * len(DICE)), len(DICE)) for p in DICE_WEIGHTS)
            result = derivation([f'{a}+{b}-{overlap}={union}'])
            block = VGroup(matrix, stack_content(example.scale(.68), result, gap=.42)).arrange(RIGHT, buff=.45)
            self.place(block)
            self.play(FadeIn(matrix), FadeIn(example), run_time=.80)
            self.beat(cue, .37)
            pulse = VGroup(*(SurroundingRectangle(dot, color=WARN, buff=.04, stroke_width=2) for dot in intersection))
            self.play(FadeIn(pulse), run_time=.61)
            self.beat(cue, .22)
            self.play(FadeOut(pulse), run_time=.57)
            result.reveal(self, run_time=.75)
            self.remove(matrix, example, *result.submobjects)
            self.add(block)

    def boole(self):
        with self.seg('exclusive_add') as cue:
            dots = UnionDots()
            eq = equation(r'A_1A_2=\varnothing\Rightarrow\mathbf{P}\{A_1\cup A_2\}'
                          r'=\mathbf{P}\{A_1\}+\mathbf{P}\{A_2\}\qquad(1.5)', 41)
            block = stack_content(dots, eq, gap=.35)
            self.place(block)
            self.play(FadeIn(dots), run_time=.55)
            self.beat(cue, .26)
            target = UnionDots(separated=True).match_width(dots).move_to(dots)
            self.play(Transform(dots, target), FadeIn(eq), run_time=.93)
            self.remove(dots, eq)
            self.add(block)

        with self.seg('boole'):
            theorem = box('property', "Property 1.2 · Boole's inequality", [
                r'$\mathbf{P}\{A_1\cup A_2\cup\dots\}\le\mathbf{P}\{A_1\}+\mathbf{P}\{A_2\}+\dots\quad(1.6)$',
                'For mutually exclusive events',
                r'$\mathbf{P}\{A_1\cup A_2\cup\dots\}='
                r'\mathbf{P}\{A_1\}+\mathbf{P}\{A_2\}+\dots\quad(1.7)$',
            ])
            self.show(stack_content(UnionDots(many=True).scale(.68), theorem, gap=.22))

        with self.seg('boole_dice') as cue:
            six = VGroup(card(1.45, 1.45),
                         VGroup(*(Dot([x, y, 0], radius=.074, color=ACCENT)
                                  for x in (-.34, .34) for y in (-.39, 0, .39))))
            faces = VGroup(*(stack_content(six.copy(), equation(fraction(ONE_SIX), 40, ACCENT), gap=.19)
                             for _ in range(3))).arrange(RIGHT, buff=.48)
            estimates = VGroup(
                stack_content(sans('Upper bound', 34, ACCENT), equation('+'.join([fraction(ONE_SIX)] * 3) +
                              '=' + fraction(BOOLE_BOUND), 43), gap=.18),
                stack_content(sans('Exact probability', 34, NEXT), equation(rf'1-\left({fraction(1-ONE_SIX)}\right)^3'
                              rf'={fraction(EXACT_SIX)}\approx {float(EXACT_SIX):.2f}', 43), gap=.18),
            ).arrange(RIGHT, buff=.76)
            block = stack_content(faces, estimates, gap=.55)
            self.place(block)
            self.play(FadeIn(faces), run_time=.65)
            for estimate in estimates:
                self.beat(cue, .31)
                self.play(FadeIn(estimate), run_time=.62)
            self.remove(faces, *estimates)
            self.add(block)

    def equally_likely(self):
        with self.seg('classical') as cue:
            self.show(derivation([
                r'\mathbf{P}\{E_i\}=\dfrac{1}{N}',
                r'\mathbf{P}\{A\}=\dfrac{|A|}{N}=\dfrac{\text{favourable cases}}{\text{all cases}}',
            ]), step_time=min(3, cue.left()*.21))
        with self.seg('classical_example'):
            matrix, _ = dice_matrix(total=7, sum_label='Sum is seven', show_odd=False)
            result = equation(fraction(SUM_COUNTS[7], len(DICE)) + '=' +
                              fraction(ONE_SIX), 47, ACCENT)
            example = box('example', 'Example', ['Two fair dice'])
            self.show(VGroup(matrix, stack_content(example.scale(.68), result)).arrange(RIGHT, buff=.48))

    def dice_sums(self):
        with self.seg('sums_trap'):
            tiles = VGroup()
            for value in SUM_COUNTS:
                panel = card(1.0, 1.55)
                words = stack_content(mono(str(value), 30, TEXT, 'BOLD'),
                                      equation(fraction(1, len(SUM_COUNTS)) + '?', 29, WARN), gap=.16)
                tiles.add(VGroup(panel, words.move_to(panel)))
            tiles.arrange(RIGHT, buff=.10)
            self.show(stack_content(pill('Careful', WARN, 34), tiles, gap=.51))

        with self.seg('sums_truth'):
            self.show(sums_chart())
        with self.seg('classical_caution') as cue:
            coin = stack_content(fair_coin_face().scale(.72),
                                 equation(r'p\ \text{and}\ q=1-p', 36, ACCENT), gap=.30)
            births = VGroup(sans('Boys and girls', 31, TEXT, 'BOLD'),
                            sans('are not born', 28, TEXT2),
                            sans('equally often', 28, TEXT2)).arrange(DOWN, buff=.14)
            table = comparison_card(decimals=False).scale(.51)
            table = comparison_card(decimals=False).scale(.44)
            row = VGroup(labeled_card(coin, 'Biased coin', width=3.3, height=3.3),
                         VGroup(card(3.3, 3.3), births.move_to([0, 0, 0])),
                         labeled_card(table, 'Same balls, two models', width=5.6, height=3.3))
            self.place(row.arrange(RIGHT, buff=.25))
            for panel in row:
                self.play(FadeIn(panel), run_time=.54)
                self.beat(cue, .19)
            self.remove(*row)
            self.add(row)

        with self.seg('next_chapter'):
            self.show(pill('Next chapter: counting', NEXT, 47))

    def code_lab(self):
        with self.seg('code') as cue:
            self.show(code_cell(CODE, OUTPUT), step_time=min(1.8, cue.left() / 12))
        with self.seg('code_result'):
            self.show(simulation_bars())

    def finish_lesson(self):
        with self.seg('recall'):
            ideas = key_ideas(KEY_IDEAS, pause=5)
            self.place(ideas)
            ideas.start_recall(self)
        ideas.countdown(self)
        with self.seg('ideas') as cue:
            ideas.reveal_items(self, step_time=cue.left()*.20)
            self.remove(*ideas.submobjects)
            self.add(ideas)
        with self.seg('end'):
            self.show(end_card('The multiplication rule and ordered samples'))
