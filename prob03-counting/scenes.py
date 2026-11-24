"""Manim lesson on the multiplication rule and ordered samples."""

from fractions import Fraction
from math import cos, pi, sin
from pathlib import Path
import sys

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Create, Dot, FadeIn, FadeOut, LaggedStart, Line,
    MathTex, Polygon, Rectangle, SurroundingRectangle, Transform, TransformFromCopy, VGroup, VMobject, DashedLine,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))

from brand import ACCENT, BORDER2, MUTED, NEXT, SKY, TEXT, TEXT2, WARN, axes, card, mono, pill, sans
from data import (
    ACCIDENTS, ACE, ALL_FACES, ALPHABET, ARRANGEMENTS, AT_LEAST_ONE_ACE, BIRTHDAYS, BIRTHDAY_PAIRS,
    BRANCH_COUNTS, BULB_COUNT, CODE, CODE_OUTPUT, CROSSING, DAYS, DECK, DESSERTS, DICE, DIE_FACES,
    DIFFERENT_FLOORS, DIGITS, DIGIT_DRAWS, DISTINCT_DIGITS, DISTINCT_E_GROUPS, E_DIGITS,
    EMPTY_SAMPLE_COUNT, E_FREQUENCY, E_GROUPS, FLAG_DISPLAYS, FLAG_SLOTS, FLAGS, FLOORS,
    FLOOR_CHOICES, HALF, HATS, INCLUSION_WITH, INCLUSION_WITHOUT, KEY_IDEAS, LAMP_LIT, LAMP_SETTINGS,
    LARGE_GROUP, LOG_DENOMINATOR, LOG_ESTIMATE, LOG_NUMERATOR, MEALS, MENUS, NO_ACE_CHOICES, OUTFITS,
    OVERSIZE_SAMPLE_COUNT, PASSENGERS, PER_LETTER, PERMUTATIONS, PIECE_COUNT, POLES, POP_SIZE,
    POPULATION, RANKS, SAMPLE_LENGTH, SEVEN_COUNT, SHIRTS, SUITS, SUM_COUNTS, SWITCH_LEVELS,
    WEEK_DAYS, WITH_COUNT, WITH_MISSES, WITHOUT_COUNT, WITHOUT_MISSES, WORD_LENGTH,
)
from lesson_kit import LessonScene, box, code_cell, derivation, end_card, key_ideas, svg_figure, title_card
from prob_visuals import arrangement_grid, dice_matrix, formula_pill


def math(text, size=42, color=TEXT):
    return MathTex(text, font_size=size, color=color)


def frac(numerator, denominator=None):
    if denominator is None:
        numerator, denominator = numerator.numerator, numerator.denominator
    return rf'\tfrac{{{numerator}}}{{{denominator}}}'


def stack(*items, gap=.30):
    return VGroup(*items).arrange(DOWN, buff=gap)


def row(*items, gap=.25):
    return VGroup(*items).arrange(RIGHT, buff=gap)


def panel(contents, width=0, height=0, color=BORDER2):
    width = max(width, contents.width + .36)
    height = max(height, contents.height + .26)
    frame = card(width, height).set_stroke(color).move_to(contents)
    return VGroup(frame, contents)


def label(text, width=0, height=0, size=30, color=TEXT2):
    return panel(sans(str(text), size, color), width, height)


def exact_box(kind, title, lines):
    result = box(kind, title, lines)
    if title in ('Corollary', 'Remark'):
        heading = sans(title, 44, ACCENT, 'BOLD')
        result.heading.become(heading.move_to(result.heading).align_to(result.heading, LEFT))
    return result


def example(number, *lines):
    return box('example', f'Example 2.{number}', lines)


def choice_tile(value, color=TEXT2):
    return panel(mono(str(value), 35, color, 'BOLD'), .72, .68, color if color != TEXT2 else BORDER2)


def tile_row(values, colors=None):
    if colors is None:
        colors = [TEXT2] * len(values)
    return row(*(choice_tile(v, color) for v, color in zip(values, colors, strict=True)), gap=.13)


def recap_sums():
    cards = []
    for value in SUM_COUNTS:
        color = ACCENT if value == 7 else TEXT2
        cards.append(choice_tile(value, color))
    return row(*cards, gap=.11), formula_pill(
        rf'${frac(SEVEN_COUNT, len(DICE))}={frac(Fraction(SEVEN_COUNT, len(DICE)))}$', 39)


def outfits_table():
    cells = [label('Shirt / hat', 1.8, .69, 26)]
    cells.extend(label(hat, 1.8, .69, 29, NEXT) for hat in HATS)
    for shirt in SHIRTS:
        cells.append(label(shirt, 1.8, .69, 29, ACCENT))
        cells.extend(label(f'{shirt} + {hat}', 1.8, .69, 24)
                     for a, hat in OUTFITS if a == shirt)
    return VGroup(*cells).arrange_in_grid(rows=len(SHIRTS) + 1, cols=len(HATS) + 1, buff=.14)


def menu_tree():
    """One dot per meal, including branches whose main dishes differ."""
    starters, mains, desserts = BRANCH_COUNTS
    gap = .44
    leaf_x = [(i - (MEALS - 1) / 2) * gap for i in range(MEALS)]
    root = label('Meal', 1.15, .51, 29, TEXT).move_to([0, 2.06, 0])
    edges, nodes, leaves = VGroup(), VGroup(root), VGroup()
    for i, (starter, options) in enumerate(MENUS):
        subset = leaf_x[i * mains * desserts:(i + 1) * mains * desserts]
        color = (ACCENT, NEXT, SKY)[i]
        start = label(starter, 1.40, .49, 26, color).move_to([sum(subset) / len(subset), .99, 0])
        edges.add(Line(root.get_bottom(), start.get_top(), color=color, stroke_width=1.7))
        nodes.add(start)
        for j, option in enumerate(options):
            positions = subset[j * desserts:(j + 1) * desserts]
            main = label(option, 1.16, .49, 25, color).move_to([sum(positions) / len(positions), -.08, 0])
            edges.add(Line(start.get_bottom(), main.get_top(), color=color, stroke_width=1.6))
            nodes.add(main)
            for x in positions:
                point = Dot([x, -1.22, 0], radius=.065, color=color)
                edges.add(Line(main.get_bottom(), point.get_top(), color=color, stroke_width=1.3))
                leaves.add(point)
    counts = VGroup(*(mono(f'×{number}', 30, ACCENT).move_to([6.05, y, 0])
                      for number, y in zip((starters, mains, desserts), (.99, -.08, -1.22), strict=True)))
    result = formula_pill(rf'${starters}\cdot{mains}\cdot{desserts}={MEALS}$', 38)
    result.next_to(VGroup(leaves, counts), DOWN, buff=.30).set_x(0)
    return VGroup(edges, nodes, leaves, counts, result)


def suit_symbol(suit):
    color = WARN if suit in ('Hearts', 'Diamonds') else TEXT2
    if suit == 'Diamonds':
        return Polygon([0,.27,0], [.19,0,0], [0,-.27,0], [-.19,0,0],
                       color=color, fill_opacity=1, stroke_width=0)
    if suit == 'Clubs':
        lobes = VGroup(*(Dot([x, y, 0], radius=.127, color=color)
                         for x, y in ((0,.12), (-.115,-.03), (.115,-.03))))
    else:
        heart = VMobject(color=color, fill_opacity=1, stroke_width=0)
        heart.start_new_path([0,-.23,0])
        heart.add_cubic_bezier_curve_to([-.18,-.09,0], [-.34,.12,0], [-.19,.21,0])
        heart.add_cubic_bezier_curve_to([-.10,.27,0], [-.035,.20,0], [0,.12,0])
        heart.add_cubic_bezier_curve_to([.035,.20,0], [.10,.27,0], [.19,.21,0])
        heart.add_cubic_bezier_curve_to([.34,.12,0], [.18,-.09,0], [0,-.23,0])
        if suit == 'Hearts':
            return heart
        lobes = VGroup(heart.rotate(pi).shift(UP * .055))
    stem = Polygon([-.06,-.095,0], [.06,-.095,0], [.10,-.23,0], [-.10,-.23,0],
                   color=color, fill_opacity=1, stroke_width=0)
    return VGroup(lobes, stem)


def deck_grid():
    cells = [mono('Suit / rank', 23, MUTED)]
    cells.extend(mono(rank, 26, NEXT) for rank in RANKS)
    for suit in SUITS:
        cells.append(row(suit_symbol(suit).scale_to_fit_height(.31), sans(suit, 27, TEXT2), gap=.13))
        cells.extend(Dot(radius=.054, color=ACCENT) for name, _ in DECK if name == suit)
    grid = VGroup(*cells).arrange_in_grid(rows=len(SUITS) + 1, cols=len(RANKS) + 1, buff=(.21, .16))
    return stack(sans('Deck of cards', 36, TEXT, 'BOLD'), panel(grid),
                 formula_pill(rf'${len(SUITS)}\cdot{len(RANKS)}={len(DECK)}$', 38))


def lamp_grid():
    bulbs = row(*(Circle(radius=.13, color=WARN, fill_opacity=.5) for _ in range(BULB_COUNT)), gap=.09)
    indirect = row(*(Rectangle(width=.10, height=.19 + .05 * level, color=NEXT, fill_opacity=.6)
                     for level in SWITCH_LEVELS), gap=.06)
    controls = row(stack(bulbs, sans('Bulbs', 26), gap=.12),
                   stack(indirect, sans('Indirect light', 26), gap=.12), gap=.48)
    squares = []
    for setting in LAMP_SETTINGS:
        text = mono(f'{setting[0]},{setting[1]}', 25, WARN if not any(setting) else TEXT2)
        tile = panel(text, .88, .57)
        if not any(setting):
            tile.add(Line(tile[0].get_corner(UP + LEFT), tile[0].get_corner(DOWN + RIGHT),
                          color=WARN, stroke_width=3))
        squares.append(tile)
    grid = VGroup(*squares).arrange_in_grid(rows=len(SWITCH_LEVELS), cols=len(SWITCH_LEVELS), buff=.09)
    return stack(controls, grid, formula_pill(rf'${len(LAMP_SETTINGS)}-1={LAMP_LIT}$', 36))


def flag_display(placements, *, count=True):
    poles, flags, slots = VGroup(), VGroup(), VGroup()
    colors = (ACCENT, NEXT, SKY)
    for i, pole_flags in enumerate(placements):
        x = (i - (POLES - 1) / 2) * 2.22
        mast = Line([x, -1.35, 0], [x, 1.33, 0], color=MUTED, stroke_width=4)
        foot = Line([x - .37, -1.35, 0], [x + .37, -1.35, 0], color=MUTED, stroke_width=4)
        poles.add(VGroup(mast, foot))
        levels = np.linspace(1.18, -1.13, 2 * len(pole_flags) + 3)[1:-1]
        for j, y in enumerate(levels):
            if j % 2 == 0:
                slots.add(Circle(radius=.086, color=WARN, stroke_width=2).move_to([x, y, 0]))
            else:
                color = colors[pole_flags[j // 2]]
                pennant = VMobject(color=color, fill_opacity=.80)
                pennant.set_points_as_corners([[x, y+.20, 0], [x+.53, y+.15, 0], [x+.35, y, 0],
                                                [x+.53, y-.15, 0], [x, y-.20, 0], [x, y+.20, 0]])
                flags.add(pennant)
    title = pill(f'{len(slots)} insertion slots', WARN, 29) if count else sans('Remove the last flag', 28, TEXT2)
    title.next_to(poles, DOWN, buff=.36)
    return VGroup(poles, flags, slots, title)


def tray_columns(draws, *, probability=False):
    columns = VGroup()
    for replace, draws_here, color in zip((True, False), draws, (ACCENT, NEXT), strict=True):
        used = set(draws_here)
        available = tile_row(POPULATION, [MUTED if not replace and item in used else TEXT2 for item in POPULATION])
        if not replace:
            for tile, item in zip(available, POPULATION, strict=True):
                if item in used:
                    tile.set_opacity(.24)
        sample = []
        seen = set()
        for item in draws_here:
            sample.append(choice_tile(item, WARN if item in seen else color))
            seen.add(item)
        choices = tuple(POP_SIZE if replace else POP_SIZE - k for k in range(SAMPLE_LENGTH))
        count = WITH_COUNT if replace else WITHOUT_COUNT
        product = r'\cdot'.join(map(str, choices))
        amount = frac(1, count) if probability else f'{product}={count}'
        heading = sans('With replacement' if replace else 'Without replacement', 31, color, 'BOLD')
        picked = stack(available, row(*sample, gap=.13), math(amount, 39, color), gap=.23)
        columns.add(panel(stack(heading, picked, gap=.32), 5.18, 3.08))
    return row(*columns, gap=.36)


def birthday_plot():
    ax, ticks = axes((0, max(BIRTHDAYS), 10), (0, 1, .25), 9.9, 3.25,
                     xt=(min(BIRTHDAYS), *range(10, max(BIRTHDAYS) + 1, 10)), yt=(0, .25, .5, .75, 1), size=24)
    expected = DashedLine(ax.c2p(0, float(HALF)), ax.c2p(max(BIRTHDAYS), float(HALF)),
                          color=NEXT, stroke_width=3)
    curve = VMobject(color=ACCENT, stroke_width=4)
    curve.set_points_as_corners([ax.c2p(r, float(p)) for r, p in BIRTHDAYS.items()])
    focus = VGroup(*(Dot(ax.c2p(r, float(BIRTHDAYS[r])), radius=.073,
                         color=WARN if r == CROSSING else ACCENT)
                     for r in (CROSSING - 1, CROSSING, LARGE_GROUP)))
    x = sans('People in the room', 27, TEXT2).next_to(ticks, DOWN, buff=.22)
    y = sans('Probability all birthdays differ', 34, TEXT, 'BOLD').next_to(ax, UP, buff=.25).align_to(ax, LEFT)
    note = row(*(formula_pill(rf'$p_{{{r}}}\approx {float(BIRTHDAYS[r]):.3f}$', 33)
                 for r in (CROSSING - 1, CROSSING, LARGE_GROUP)),
               formula_pill(rf'$1-p_{{{CROSSING}}}\approx {float(1 - BIRTHDAYS[CROSSING]):.3f}$', 33))
    note.next_to(x, DOWN, buff=.24)
    base = VGroup(ax, ticks, expected, x, y)
    return VGroup(base, curve, focus, note), base, curve, focus, note


def birthday_connections():
    radius_x = radius_y = 2.3
    points = [np.array([radius_x * cos(2 * pi * i / CROSSING), radius_y * sin(2 * pi * i / CROSSING), 0])
              for i in range(CROSSING)]
    edges = VGroup(*(Line(points[i], points[j], color=ACCENT, stroke_opacity=.19, stroke_width=1.1)
                     for i, j in BIRTHDAY_PAIRS))
    dots = VGroup(*(Dot(point, color=TEXT, radius=.062) for point in points))
    pairs = math(rf'\binom{{{CROSSING}}}{{2}}={len(BIRTHDAY_PAIRS)}', 51, ACCENT)
    pairs_caption = stack(sans('Pairs of people', 36, TEXT, 'BOLD'), pairs,
                          math(r'\binom r2=\frac{r(r-1)}{2}', 39),
                          formula_pill(rf'$P(\mathrm{{match\ for\ one\ pair}})={frac(1, DAYS)}$', 31))
    pairs_caption.next_to(dots, RIGHT, buff=.49)
    return VGroup(edges, dots, pairs_caption), edges, dots, pairs_caption


class Video(LessonScene):
    folder = str(HERE)
    number = '2.1'
    section_title = 'The Multiplication Rule and Ordered Samples'
    lesson_k = 3

    def construct(self):
        self.welcome()
        self.pairs()
        self.successive_choices()
        self.classic_examples()
        self.flags()
        self.samples()
        self.permutations()
        self.type_pieces()
        self.random_samples()
        self.inclusion()
        self.no_repetition()
        self.occupancy()
        self.birthdays()
        self.code_lab()
        self.finish_lesson()

    def beat(self, cue, proportion):
        self.wait(max(.08, cue.left() * proportion))

    def welcome(self):
        with self.seg('welcome'):
            self.show(title_card(self.number, self.section_title, self.lesson_k))
        with self.seg('recap') as cue:
            ratio = stack(sans('Favourable outcomes', 37, ACCENT),
                          math(r'\mathbf P\{A\}=\frac{|A|}{|\Omega|}', 57),
                          sans('All outcomes', 36, NEXT))
            self.show(ratio)
            self.beat(cue, .29)
            matrix, _ = dice_matrix(total=7, sum_label='Sum is seven', show_odd=False)
            sums, odds = recap_sums()
            incorrect = label(f'{1}/{len(SUM_COUNTS)}?  Sums are not equally likely', size=25, color=WARN)
            recap = stack(sans('Possible sums', 32, TEXT, 'BOLD'), sums, incorrect, odds)
            self.show(row(matrix.scale(.80), recap, gap=.37))

    def pairs(self):
        with self.seg('pairs') as cue:
            theorem = box('theorem', 'Theorem 2.1', [r'$m$ choices and $n$ choices give $mn$ pairs.'])
            table = outfits_table()
            result = formula_pill(rf'${len(SHIRTS)}\cdot{len(HATS)}={len(OUTFITS)}$', 37)
            block = stack(theorem, table, result)
            self.place(block)
            self.play(FadeIn(theorem), FadeIn(table), run_time=.83)
            self.beat(cue, .34)
            self.play(FadeIn(result), run_time=.55)
            self.remove(theorem, table, result)
            self.add(block)
        with self.seg('pair_table') as cue:
            figure = svg_figure('mult-table.svg').scale_to_fit_width(9.5)
            caption = formula_pill(r'$(a_j,b_k)$ goes in row $j$, column $k$', 36)
            cells = [shape for shape in figure if not getattr(shape, 'is_svg_label', False)]
            highlight = SurroundingRectangle(cells[len(cells) // 2], color=ACCENT, buff=.045, corner_radius=.08)
            block = stack(VGroup(figure, highlight), caption, gap=.37)
            self.place(block)
            self.play(FadeIn(figure), run_time=.72)
            self.beat(cue, .28)
            self.play(Create(highlight), FadeIn(caption), run_time=.70)
            self.remove(figure, highlight, caption)
            self.add(block)

    def successive_choices(self):
        with self.seg('multiplets') as cue:
            theorem = box('theorem', 'Theorem 2.2', [r'$n_1n_2\cdots n_r$ ordered tuples'])
            starter, main = MENUS[0][0], MENUS[0][1][0]
            pair = panel(row(label(starter, size=29, color=ACCENT), label(main, size=29, color=NEXT)),
                         color=ACCENT)
            detail = row(pair, math('+', 45, MUTED), label(DESSERTS[0], size=30, color=NEXT), gap=.35)
            count = formula_pill(rf'$({BRANCH_COUNTS[0]}\cdot{BRANCH_COUNTS[1]})'
                                 rf'\cdot {BRANCH_COUNTS[2]}={MEALS}$', 40)
            self.show(stack(theorem, detail, count, gap=.44))
            self.beat(cue, .50)
            tree = menu_tree()
            self.place(tree)
            edges, nodes, leaves, counts, result = tree
            self.play(FadeIn(nodes), Create(edges), FadeIn(leaves), run_time=1.35)
            self.play(FadeIn(counts), FadeIn(result), run_time=.50)
            self.remove(*tree)
            self.add(tree)
        with self.seg('fixed_counts'):
            self.play(*(node[1].animate.set_color(TEXT) for node in tree[1] if len(node) == 2),
                      run_time=.65)

    def classic_examples(self):
        with self.seg('cards_lamp') as cue:
            heading = example(1, 'Cards and lamp settings')
            cards, lamp = deck_grid(), lamp_grid()
            body = row(cards, lamp, gap=.52)
            block = stack(heading, body, gap=.32)
            self.place(block)
            self.play(FadeIn(heading), FadeIn(cards), run_time=.78)
            self.beat(cue, .30)
            self.play(FadeIn(lamp), run_time=.73)
            self.remove(heading, cards, lamp)
            self.add(block)
        with self.seg('balls_cells'):
            self.show(stack(arrangement_grid(ARRANGEMENTS),
                            formula_pill(r'$n\cdot n\cdots n=n^r$', 38),
                            pill(f'{len(ARRANGEMENTS)} arrangements', ACCENT, 29), gap=.30))
        with self.seg('no_ace') as cue:
            die = panel(Dot(radius=.16, color=ACCENT), 1.34, 1.34)
            faces = len(DIE_FACES)
            art = stack(die, sans('Ace', 32, ACCENT, 'BOLD'))
            steps = [
                rf'\text{{All sequences}}={faces}^r,\qquad \text{{No ace}}={NO_ACE_CHOICES}^r',
                rf'\mathbf P\{{\mathrm{{no\ ace}}\}}=\left({frac(NO_ACE_CHOICES, faces)}\right)^r',
                rf'\mathbf P\{{\mathrm{{at\ least\ one\ ace\ in\ {faces}\ rolls}}\}}'
                rf'=1-\left({frac(NO_ACE_CHOICES, faces)}\right)^{{{faces}}}'
                rf'\approx{float(AT_LEAST_ONE_ACE):.3f}<{frac(2, 3)}',
            ]
            first = derivation(steps[:2])
            self.show(row(art, first, gap=.55))
            self.beat(cue, .56)
            self.show(derivation(steps[1:]), step_time=.88)

    def flags(self):
        with self.seg('flag_slots') as cue:
            heading = example(2, 'Flags on poles')
            display = flag_display(((), (), ()))
            block = stack(heading, display, gap=.35)
            self.show(block)
            for placements in (((0,), (), ()), ((), (0,), ()), ((), (0,), (1,))):
                self.beat(cue, .15)
                target = flag_display(placements).match_width(display).move_to(display)
                self.play(Transform(display, target), run_time=.60)
        with self.seg('flag_count') as cue:
            display = flag_display(((2,), (0,), (1,)), count=False)
            product = r'\cdot'.join(map(str, FLAG_SLOTS))
            total = derivation([rf'{product}={FLAG_DISPLAYS}', r'n(n+1)(n+2)\cdots(n+r-1)'])
            block = stack(display, total, gap=.46)
            self.show(block)
            self.beat(cue, .32)
            previous = flag_display(((), (0,), (1,)), count=False).match_width(display).move_to(display)
            previous[3].set_opacity(0)
            self.play(Transform(display, previous), run_time=.66)

    def samples(self):
        with self.seg('sample_order') as cue:
            sample = POPULATION[:SAMPLE_LENGTH]
            switched = (sample[1], sample[0], *sample[2:])
            pool = stack(sans('Population', 39, TEXT, 'BOLD'), tile_row(POPULATION), gap=.21)
            first = tile_row(sample, [ACCENT] * SAMPLE_LENGTH)
            second = tile_row(switched, [NEXT] * SAMPLE_LENGTH)
            comparison = row(first, math(r'\ne', 40), second, gap=.42)
            block = stack(pool, comparison, gap=.55)
            self.place(block)
            self.play(FadeIn(pool), FadeIn(first), run_time=.65)
            self.beat(cue, .28)
            self.play(FadeIn(comparison[1]), FadeIn(second), run_time=.64)
            self.remove(pool, first, comparison[1], second)
            self.add(block)
        with self.seg('replacement') as cue:
            draws = (('A', 'A', 'C'), ('A', 'B', 'C'))
            columns = tray_columns(draws)
            self.place(columns)
            for column in columns:
                sources, targets, result = column[1][1]
                for source in sources:
                    source.set_opacity(1)
                for item in (*targets, result):
                    item.save_state().set_opacity(0)
            self.play(FadeIn(columns), run_time=.68)
            for column, sequence, replace in zip(columns, draws, (True, False), strict=True):
                sources, targets, result = column[1][1]
                self.beat(cue, .12)
                for letter, target in zip(sequence, targets, strict=True):
                    source = sources[POPULATION.index(letter)]
                    moving = target.saved_state.copy()
                    animations = [TransformFromCopy(source, moving)]
                    if not replace:
                        animations.append(source.animate.set_opacity(.24))
                    self.play(*animations, run_time=.54)
                    self.remove(moving)
                    target.restore()
                self.play(result.animate.restore(), run_time=.50)
        with self.seg('falling_product') as cue:
            theorem = box('theorem', 'Theorem 2.3',
                          [r'With replacement: $n^r$ · Without replacement: $(n)_r$'])
            definition = derivation([r'(n)_r=n(n-1)\cdots(n-r+1)\qquad(2.1)'])
            self.show(stack(theorem, definition))
            self.beat(cue, .49)
            pool = tile_row(POPULATION)
            empty = panel(stack(sans('Empty tray', 30, TEXT), card(2.35, .48),
                                math(rf'(n)_0={EMPTY_SAMPLE_COUNT}', 40, ACCENT)), 4.4, 1.78)
            excess = tile_row((*POPULATION, '?'), [*([NEXT] * POP_SIZE), WARN]).scale(.58)
            overflow = panel(stack(sans('Too many draws', 30, TEXT), excess,
                                   math(rf'(n)_r={OVERSIZE_SAMPLE_COUNT},\quad r>n', 38, WARN)), 4.4, 1.78)
            self.show(stack(theorem.copy(), pool, row(empty, overflow, gap=.45)))

    def permutations(self):
        with self.seg('permutations') as cue:
            corollary = exact_box('theorem', 'Corollary', ['Drawing the entire population gives a permutation.'])
            boards = VGroup(*(tile_row(items, [ACCENT] * len(items)) for items in PERMUTATIONS))
            boards.arrange_in_grid(rows=2, cols=len(PERMUTATIONS) // 2, buff=(.44, .19))
            sizes = tuple(range(SAMPLE_LENGTH, 0, -1))
            product = r'\cdot'.join(map(str, sizes))
            result = derivation([rf'{SAMPLE_LENGTH}!={product}={len(PERMUTATIONS)}',
                                 r'n!=n(n-1)\cdots2\cdot1=(n)_n\qquad(2.2)'])
            block = stack(corollary, boards, result, gap=.27)
            self.place(block)
            self.play(FadeIn(corollary), FadeIn(boards), run_time=.65)
            self.beat(cue, .24)
            result.reveal(self, run_time=.62, step_time=.65)
            self.remove(corollary, boards, *result.submobjects)
            self.add(block)

    def type_pieces(self):
        with self.seg('type_pieces') as cue:
            heading = example(3, 'Letters and pieces of type')
            letters = tile_row('PROBABILITY'[:WORD_LENGTH])
            pieces = tile_row([f'{letter}{number}' for number, letter in enumerate('PROBABILITY'[:WORD_LENGTH], 1)],
                              [NEXT] * WORD_LENGTH)
            letter_label = formula_pill(rf'${ALPHABET}^{{{WORD_LENGTH}}}$ letter strings', 37)
            piece_label = formula_pill(
                rf'$({PIECE_COUNT:,})_{{{WORD_LENGTH}}}\approx {PIECE_COUNT:,}^{{{WORD_LENGTH}}}>10^{{44}}$',
                38)
            sample = stack(letters, letter_label, gap=.14)
            stock = stack(sans(f'{PER_LETTER:,} pieces per letter', 28, TEXT2), pieces, piece_label, gap=.14)
            block = stack(heading, sample, stock, gap=.30)
            self.place(block)
            self.play(FadeIn(heading), FadeIn(sample), run_time=.60)
            self.beat(cue, .32)
            self.play(FadeIn(stock), run_time=.69)
            self.remove(heading, sample, stock)
            self.add(block)

    def random_samples(self):
        with self.seg('uniform_sample'):
            heading = exact_box('definition', 'Definition 2.1', [
                'Each possible ordered sample has the same probability.',
                r'With replacement: $1/n^r$ · Without replacement: $1/(n)_r$.',
            ])
            self.show(stack(heading, tray_columns((('A', 'A', 'C'), ('A', 'B', 'C')),
                                                 probability=True), gap=.31))
        with self.seg('survey_order') as cue:
            remark = exact_box('definition', 'Remark', ['The order of interviews identifies the sample.'])
            respondents = row(*(label(person, 1.24, .73, 31, ACCENT if i == SAMPLE_LENGTH else TEXT2)
                                for i, person in enumerate(POPULATION, 1)))
            caption = pill('Third person interviewed', ACCENT, 29).next_to(respondents[2], DOWN, buff=.22)
            ratio = formula_pill(r'$(n)_r/n^r\approx1$ when the sample is small', 38)
            block = stack(remark, VGroup(respondents, caption), ratio, gap=.39)
            self.place(block)
            self.play(FadeIn(remark), FadeIn(respondents), FadeIn(caption), run_time=.73)
            self.beat(cue, .49)
            self.play(FadeIn(ratio), run_time=.55)
            self.remove(remark, respondents, caption, ratio)
            self.add(block)

    def inclusion(self):
        with self.seg('include_without') as cue:
            population = tile_row(POPULATION, [WARN, *([TEXT2] * (POP_SIZE - 1))])
            head = example(4, 'Include a particular element')
            numeric = derivation([rf'1-{frac(WITHOUT_MISSES, WITHOUT_COUNT)}={frac(INCLUSION_WITHOUT)}'])
            self.show(stack(head, population, numeric))
            self.beat(cue, .52)
            self.show(derivation([
                r'\frac{(n-1)_r}{(n)_r}=\frac{(n-1)(n-2)\cdots(n-r)}'
                r'{n(n-1)\cdots(n-r+1)}=\frac{n-r}{n}',
                r'\mathbf P\{\mathrm{included}\}=1-\frac{n-r}{n}=\frac{r}{n}',
            ]), step_time=.80)
        with self.seg('include_with') as cue:
            head = pill('With replacement', NEXT, 30)
            result = derivation([
                rf'1-\frac{{(n-1)^r}}{{n^r}}=1-\left(1-\frac1n\right)^r',
                rf'1-\left({frac(POP_SIZE - 1, POP_SIZE)}\right)^{{{SAMPLE_LENGTH}}}'
                rf'=1-{frac(WITH_MISSES, WITH_COUNT)}={frac(INCLUSION_WITH)}',
            ])
            self.place(stack(head, result, gap=.45))
            self.play(FadeIn(head), run_time=.48)
            result.reveal(self, run_time=.77, step_time=max(.3, cue.left() * .25))
            self.remove(head, *result.submobjects)
            self.add(self.body)

    def no_repetition(self):
        with self.seg('no_repeat') as cue:
            total = Circle(radius=2.1, color=NEXT, fill_opacity=.10).stretch(1.58, 0)
            distinct = Circle(radius=1.05, color=ACCENT, fill_opacity=.23).shift(DOWN * .34)
            total_label = math(r'n^r', 43, NEXT).move_to(UP * 1.36)
            inside = math(r'(n)_r', 39, ACCENT).move_to(distinct)
            diagram = VGroup(total, distinct, total_label, inside)
            self.show(diagram)
            self.beat(cue, .35)
            self.show(derivation([
                r'p=\frac{(n)_r}{n^r}',
                r'p=\left(1-\frac{1}{n}\right)\left(1-\frac{2}{n}\right)\cdots'
                r'\left(1-\frac{r-1}{n}\right)\qquad(2.3)',
            ]), step_time=.91)
        with self.seg('random_digits') as cue:
            title = example(5, 'Random digits')
            slots = row(*(card(.72, .68) for _ in range(DIGIT_DRAWS)), gap=.13)
            digits = stack(sans('Digits', 30, TEXT2), tile_row(DIGITS).scale(.77), slots,
                           formula_pill(rf'$\frac{{({len(DIGITS)})_{{{DIGIT_DRAWS}}}}}{{{len(DIGITS)}^{{{DIGIT_DRAWS}}}}}'
                                        rf'={float(DISTINCT_DIGITS):.4f}$', 38))
            observed = panel(stack(sans(rf'{E_DIGITS:,} decimal digits of e', 32, TEXT, 'BOLD'),
                                   sans(f'{E_GROUPS} groups of {DIGIT_DRAWS}', 31, TEXT2),
                                   math(rf'{frac(DISTINCT_E_GROUPS, E_GROUPS)}={float(E_FREQUENCY):.3f}', 43, ACCENT),
                                   gap=.26))
            block = stack(title, row(digits, observed, gap=.47), gap=.45)
            self.place(block)
            self.play(FadeIn(title), FadeIn(digits), run_time=.75)
            self.beat(cue, .38)
            self.play(FadeIn(observed), run_time=.67)
            self.remove(title, digits, observed)
            self.add(block)

    def occupancy(self):
        with self.seg('occupancy') as cue:
            heading = example(6, 'Every cell occupied')
            boxes = row(*(card(1.30, 1.09) for _ in POPULATION[:SAMPLE_LENGTH]))
            dots = VGroup(*(Dot(color=color, radius=.16).move_to(slot).shift(UP * .87)
                            for color, slot in zip((ACCENT, NEXT, SKY), boxes, strict=True)))
            legend = formula_pill(r'$P(\mathrm{every\ cell\ occupied})=\frac{n!}{n^n}$', 43)
            block = stack(heading, VGroup(boxes, dots), legend, gap=.42)
            self.place(block)
            self.play(FadeIn(heading), FadeIn(boxes), FadeIn(dots), run_time=.72)
            self.beat(cue, .25)
            for dot, slot in zip(dots, boxes, strict=True):
                self.play(dot.animate.move_to(slot), run_time=.39)
            self.play(FadeIn(legend), run_time=.63)
            self.remove(heading, boxes, dots, legend)
            self.add(block)
        with self.seg('accidents_dice') as cue:
            days = len(WEEK_DAYS)
            faces = len(DIE_FACES)
            calendar = row(*(label(day, .84, .62, 25, color=ACCENT) for day in WEEK_DAYS), gap=.11)
            week = stack(sans('One accident per day', 37, TEXT, 'BOLD'), calendar,
                         math(rf'\frac{{{days}!}}{{{days}^{days}}}\approx{float(ACCIDENTS):.5f}', 40),
                         pill(f'About once in {round(1 / ACCIDENTS)} weeks', ACCENT, 30))
            die = stack(sans('All faces in six rolls', 37, TEXT, 'BOLD'), tile_row(DIE_FACES),
                        math(rf'\frac{{{faces}!}}{{{faces}^{faces}}}\approx{float(ALL_FACES):.4f}', 40))
            block = stack(week, die, gap=.62)
            self.place(block)
            self.play(FadeIn(week), run_time=.70)
            self.beat(cue, .48)
            self.play(FadeIn(die), run_time=.69)
            self.remove(week, die)
            self.add(block)
        with self.seg('elevator') as cue:
            head = example(7, 'Different floors')
            floor_numbers = tuple(range(FLOORS, 0, -1))
            levels = VGroup(*(label(f'{i:2d}', .78, .32, 19, NEXT) for i in floor_numbers)).arrange(DOWN, buff=.06)
            cabin = panel(levels, 1.52, color=BORDER2)
            passengers = row(*(Dot(radius=.088, color=ACCENT) for _ in range(PASSENGERS)), gap=.15)
            title = sans(f'{PASSENGERS} passengers, {FLOORS} floors', 36, TEXT, 'BOLD')
            numerator = r'\cdot'.join(map(str, FLOOR_CHOICES))
            result = derivation([
                rf'\frac{{({FLOORS})_{{{PASSENGERS}}}}}{{{FLOORS}^{{{PASSENGERS}}}}}',
                rf'\frac{{{numerator}}}{{{FLOORS}^{{{PASSENGERS}}}}}={float(DIFFERENT_FLOORS):.5f}',
            ])
            side = stack(head.scale(.64), title, passengers, result, gap=.35)
            block = row(cabin, side, gap=.55)
            self.place(block)
            self.play(FadeIn(cabin), FadeIn(head), FadeIn(title), FadeIn(passengers), run_time=.76)
            self.beat(cue, .26)
            self.play(LaggedStart(*(passenger.animate.move_to(levels[i].get_right() + RIGHT * .26)
                                    for i, passenger in enumerate(passengers)), lag_ratio=.18), run_time=1.38)
            self.beat(cue, .33)
            result.reveal(self, run_time=.66, step_time=.70)
            self.remove(cabin, head, title, passengers, *result.submobjects)
            self.add(block)

    def birthdays(self):
        with self.seg('birthday_model') as cue:
            head = example(8, 'Birthdays')
            assumptions = row(*(pill(note, NEXT, 29) for note in
                                ('Ignore leap days', 'Equal chance per day', 'Independent birthdays')))
            first = derivation([rf'p_r=\frac{{({DAYS})_r}}{{{DAYS}^r}}',
                                rf'p_r=\prod_{{k=1}}^{{r-1}}\left(1-\frac{{k}}{{{DAYS}}}\right)\qquad(2.4)'])
            block = stack(head, assumptions, first, gap=.43)
            self.place(block)
            self.play(FadeIn(head), FadeIn(assumptions), run_time=.78)
            self.beat(cue, .34)
            first.reveal(self, run_time=.78, step_time=max(.55, cue.left() * .23))
            self.remove(head, assumptions, *first.submobjects)
            self.add(block)
        with self.seg('birthday_crossing') as cue:
            block, base, curve, focus, note = birthday_plot()
            self.place(block)
            self.play(FadeIn(base), Create(curve), run_time=1.6)
            for dot, caption in zip(focus, note, strict=False):
                self.beat(cue, .14)
                self.play(FadeIn(dot), FadeIn(caption), run_time=.50)
            self.play(FadeIn(note[-1]), run_time=.55)
            self.remove(base, curve, *focus, *note)
            self.add(block)
        with self.seg('birthday_log') as cue:
            deriv = derivation([
                rf'\log p_r=\sum_{{k=1}}^{{r-1}}\log\left(1-\frac{{k}}{{{DAYS}}}\right)',
                rf'\log p_r\approx-\sum_{{k=1}}^{{r-1}}\frac{{k}}{{{DAYS}}}'
                rf'=-\frac{{r(r-1)}}{{{LOG_DENOMINATOR}}}\qquad(2.5)',
            ])
            compare = row(
                formula_pill(rf'Estimate: $e^{{-{LOG_NUMERATOR}/{LOG_DENOMINATOR}}}'
                             rf'\approx {LOG_ESTIMATE:.3f}$', 34),
                formula_pill(rf'Exact product: ${float(BIRTHDAYS[LARGE_GROUP]):.3f}$', 34),
            )
            block = stack(deriv, compare, gap=.48)
            self.place(block)
            deriv.reveal(self, run_time=.85, step_time=.94)
            self.beat(cue, .43)
            self.play(FadeIn(compare), run_time=.70)
            self.remove(*deriv.submobjects, compare)
            self.add(block)
        with self.seg('birthday_pairs') as cue:
            block, edges, points, caption = birthday_connections()
            self.place(block)
            self.play(FadeIn(points), run_time=.56)
            first_edges = VGroup(*(edges[i].copy().set_stroke(WARN, width=3.2, opacity=.96)
                                   for i in (0, CROSSING - 1, 2 * CROSSING - 3)))
            self.play(LaggedStart(*(Create(edge) for edge in first_edges), lag_ratio=.34), run_time=1.48)
            self.beat(cue, .18)
            self.play(FadeOut(first_edges), FadeIn(edges), FadeIn(caption), run_time=1.25)
            self.remove(points, edges, caption, *first_edges)
            self.add(block)

    def code_lab(self):
        with self.seg('code') as cue:
            self.show(code_cell(CODE, CODE_OUTPUT), step_time=min(1.4, cue.left() / 14))
        with self.seg('code_result'):
            sim, exact = CODE_OUTPUT.split()
            columns = row(panel(stack(sans('Simulated', 35, TEXT2), math(sim, 58, ACCENT)), 3.9, 2.1),
                          panel(stack(sans('Exact (rounded)', 35, TEXT2), math(exact, 58, NEXT)), 3.9, 2.1))
            self.show(stack(sans(f'Shared birthday among {CROSSING} people', 42, TEXT, 'BOLD'),
                            columns, gap=.42))

    def finish_lesson(self):
        with self.seg('recall'):
            ideas = key_ideas(KEY_IDEAS, pause=5)
            self.place(ideas)
            ideas.start_recall(self)
        ideas.countdown(self)
        with self.seg('ideas') as cue:
            ideas.reveal_items(self, step_time=max(.25, cue.left() * .23))
            self.remove(*ideas.submobjects)
            self.add(ideas)
        with self.seg('end'):
            self.show(end_card('Subpopulations and partitions'))
