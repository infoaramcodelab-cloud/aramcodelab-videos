"""Manim lesson on occupancy problems, particle models and runs."""

import sys
from importlib.util import module_from_spec, spec_from_file_location
from itertools import groupby
from math import pi
from pathlib import Path

from manim import (
    DOWN, LEFT, RIGHT, UP, Arc, Circle, Create, Dot, FadeIn, FadeOut, LaggedStart, Line,
    MathTex, Rectangle, Star, SurroundingRectangle, Transform, VGroup,
)

HERE = Path(__file__).resolve().parent
sys.path[:0] = [str(HERE), str(HERE.parent / 'lib')]

from brand import ACCENT, BG, BORDER2, MUTED, NEXT, SKY, TEXT, TEXT2, WARN, card, mono, pill, sans
from lesson_kit import LessonScene, box, code_cell, derivation, end_card, key_ideas, svg_figure, title_card
from prob_visuals import arrangement_grid

import data as d


def earlier_module(lesson, file, name):
    path = HERE.parent / lesson / file
    spec = spec_from_file_location(name, path)
    module = module_from_spec(spec)
    paths = sys.path[:]
    local_names = ('data', 'check_numbers')
    saved = {key: sys.modules.pop(key) for key in local_names if key in sys.modules}
    try:
        sys.path.insert(0, str(path.parent))
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = paths
        for key in local_names:
            sys.modules.pop(key, None)
        sys.modules.update(saved)
    return module


four = earlier_module('prob04-subpopulations', 'scenes.py', 'lesson_four_visuals')
placements = earlier_module('prob01-sample-space', 'data.py', 'lesson_one_data').ARRANGEMENTS
stack, row, panel, math, frac = four.stack, four.row, four.panel, four.math, four.frac


def choose(n, k):
    return rf'\binom{{{n}}}{{{k}}}'


def vector(counts):
    return '(' + ','.join(map(str, counts)) + ')'


def grouped(value):
    return f'{value:,}'.replace(',', r'\,')


def mark(color=ACCENT, *, star=False, radius=.125):
    if star:
        return Star(outer_radius=radius * 1.3, color=color, fill_opacity=1, stroke_width=0)
    return Dot(radius=radius, color=color)


def divider(color=NEXT):
    return Line(DOWN * .28, UP * .28, color=color, stroke_width=4)


def cell_boxes(counts, *, names=None, stars=False, letters=None, letter_tiles=False, width=1.14, color=ACCENT):
    """Build the frames and marks as separate groups so they can move independently."""
    names = range(1, len(counts) + 1) if names is None else names
    frames, labels, marks, totals = VGroup(), VGroup(), VGroup(), VGroup()
    for index, name in enumerate(names):
        frame = card(width, 1.28).shift(RIGHT * (width + .16) * (index - (len(counts) - 1) / 2))
        frames.add(frame)
        labels.add(mono(str(name), 26, MUTED).next_to(frame, UP, buff=.15))
        totals.add(mono(str(counts[index]), 36, color if counts[index] else MUTED).next_to(frame, DOWN, buff=.15))
    letters = iter(letters) if letters is not None else None
    for count, frame in zip(counts, frames, strict=True):
        cell = VGroup()
        for k in range(count):
            if letters is None:
                item = mark(color, star=stars)
            elif letter_tiles:
                item = panel(mono(next(letters), 21, color, 'BOLD'), .42, .39, color)
            else:
                disc = Circle(radius=.17, fill_color=color, fill_opacity=.96, stroke_width=0)
                item = VGroup(disc, mono(next(letters), 17, BG, 'BOLD').move_to(disc))
            cell.add(item.move_to(frame).shift(
                RIGHT * (k % 2 - (.5 if count > 1 else 0)) * .46
                + UP * ((.5 - k // 2) * .48 if count > 2 else 0)
            ))
        marks.add(cell)
    return frames, labels, marks, totals


def occupancy_strip(counts, *, stars=False):
    return VGroup(*cell_boxes(counts, stars=stars))


def symbol_parts(counts):
    """Use the site figure's one-slot spacing, including each empty gap."""
    bars, stars, labels = VGroup(), VGroup(), VGroup()
    x = 0
    stride = .72
    for i, count in enumerate(counts):
        bars.add(divider(MUTED if i == 0 else NEXT).set_x(x))
        left = x
        for _ in range(count):
            x += stride
            stars.add(mark(star=True, radius=.14).set_x(x))
        x += stride
        labels.add(mono(str(count), 34, TEXT2 if count else WARN).move_to([(left + x) / 2, -.58, 0]))
    bars.add(divider(MUTED).set_x(x))
    symbol = VGroup(bars, stars, labels).center()
    assert len(stars) == d.BALLS and len(bars) == d.CELL_COUNT + 1
    return symbol


def star_card():
    symbol = symbol_parts(d.CELLS)
    title = box('theorem', 'Theorem 3.1', ['(i) Count occupancy vectors'])
    return stack(title, panel(symbol, width=10.5, height=1.65), gap=.45), symbol


def gap_parts():
    stars = VGroup(*(mark(star=True, radius=.16).set_x(i * .93) for i in range(d.BALLS)))
    stars.center()
    gaps = VGroup(*(
        Dot((left.get_center() + right.get_center()) / 2, radius=.047, color=WARN)
        for left, right in zip(stars, stars[1:])
    ))
    bars = VGroup(*(divider().move_to(gaps[i - 1]) for i in d.BAR_GAPS))
    ends = VGroup(divider(MUTED).next_to(stars, LEFT, buff=.31),
                  divider(MUTED).next_to(stars, RIGHT, buff=.31))
    return stars, gaps, bars, ends


def die_face(value, size=.64, color=TEXT):
    pips = VGroup(*(Dot([x * size * .25, y * size * .25, 0], radius=size * .063, color=color)
                    for x, y in four.PIPS[value]))
    return panel(pips, size, size)


def dice_cells():
    frames = VGroup(*(card(1.38, 1.63) for _ in d.DIE_FACES)).arrange(RIGHT, buff=.15)
    labels = VGroup(*(mono(f'Face {face}', 25, MUTED).next_to(frame, UP, buff=.13)
                      for face, frame in zip(d.DIE_FACES, frames, strict=True)))
    counts = VGroup(*(mono(str(n), 33, ACCENT if n else MUTED).next_to(frame, DOWN, buff=.14)
                      for n, frame in zip(d.DICE_VECTOR, frames, strict=True)))
    dice = VGroup()
    for face, count, frame in zip(d.DIE_FACES, d.DICE_VECTOR, frames, strict=True):
        for index in range(count):
            dice.add(die_face(face, color=ACCENT).move_to(frame).shift(UP * .37 * (count - 1 - 2 * index)))
    return VGroup(frames, labels, counts), dice


def dice_card():
    base, dice = dice_cells()
    formula = math(rf'{choose("r+5", 5)}\qquad {choose(len(d.ROLL) + len(d.DIE_FACES) - 1, len(d.DIE_FACES) - 1)}'
                   rf'={d.DICE_RECORDS}', 46, ACCENT)
    title = box('example', 'Example 3.1', ['Three dice sorted by face'])
    return stack(title, VGroup(base, dice), math(vector(d.DICE_VECTOR), 42), formula, gap=.30), dice


def grid_block():
    grid = arrangement_grid(placements)
    chosen = [tile for tile, parts in zip(grid, placements.values(), strict=True)
              if tuple(map(len, parts)) == d.FIXED_VECTOR]
    assert len(chosen) == d.FIXED_COUNT and len(placements) == d.FIXED_TOTAL
    return grid, VGroup(*(SurroundingRectangle(tile, buff=.052, color=ACCENT, stroke_width=2.8,
                                              corner_radius=.08) for tile in chosen))


def role_cells(order, *, filled=False):
    names = tuple(range(1, d.TARGET_N + 1))
    colours = {2: ACCENT, 1: NEXT, 0: MUTED}
    titles = {2: 'Double', 1: 'Single', 0: 'Empty'}
    frames, labels, balls, totals = cell_boxes(order, names=names, width=1.23, letters='ABCDEFG')
    for frame, count in zip(frames, order, strict=True):
        frame.set_stroke(colours[count], width=2.5)
    for i, (number, count) in enumerate(zip(totals, order, strict=True)):
        totals[i] = mono(titles[count], 21, colours[count], 'BOLD').move_to(number)
    return VGroup(frames, labels, totals, balls if filled else VGroup())


def table_card():
    """Lay out the full table before revealing any rows to keep its columns fixed."""
    pattern_x, probability_x = -.92, 1.78

    def probability_row(pattern, probability):
        chips = VGroup()
        for value in pattern:
            tile = Rectangle(width=.43, height=.35, stroke_width=1, stroke_color=BORDER2,
                             fill_color='#161a1f', fill_opacity=1)
            number = mono(str(value), 26, TEXT if value else MUTED).move_to(tile)
            chips.add(VGroup(tile, number))
        chips.arrange(RIGHT, buff=.07)
        decimal = mono(f'{float(probability):.6f}', 24, TEXT, 'BOLD').set_x(probability_x)
        chips.set_x(pattern_x)
        backdrop = card(5.72, .47)
        assert chips.get_left()[0] - backdrop.get_left()[0] > .10
        assert backdrop.get_right()[0] - decimal.get_right()[0] > .15
        assert decimal.get_left()[0] - chips.get_right()[0] > .15
        return VGroup(backdrop, chips, decimal)

    entries = VGroup(*(probability_row(pattern, value) for pattern, value in d.TABLE))
    columns = VGroup()
    for _ in range(2):
        headings = VGroup(
            sans('Occupancy pattern', 24, TEXT2, 'SEMIBOLD').set_x(pattern_x),
            sans('Probability', 24, TEXT2, 'SEMIBOLD').set_x(probability_x),
        )
        frame = card(6.15, 4.95)
        headings.align_to(frame, UP).shift(DOWN * .26)
        columns.add(VGroup(frame, headings))
    columns.arrange(RIGHT, buff=.21, aligned_edge=UP)
    # The rows remain associated with the corresponding header after laying out both panels.
    for index, column in enumerate(columns):
        selection = entries[:8] if index == 0 else entries[8:]
        for offset, item in enumerate(selection):
            item.set_x(column[0].get_x()).set_y(column[1].get_bottom()[1] - .29 - offset * .525)
    title = sans('All fifteen configurations', 47, TEXT, 'BOLD')
    table = stack(title, VGroup(columns, entries), gap=.28)
    return table, entries


def highlight_row(entry, color):
    entry[0].set_stroke(color, width=2.6)
    entry[2].set_color(color)


MODEL_TITLES = ('Maxwell–Boltzmann', 'Bose–Einstein', 'Fermi–Dirac')
MODEL_COLOURS = (ACCENT, NEXT, WARN)


def comparison_cards():
    explanations = (
        rf'\dfrac{{{d.MODEL_BALLS}!}}{{{d.MODEL_N}^{d.MODEL_BALLS}}}',
        rf'\dfrac{{1}}{{{choose(d.MODEL_N + d.MODEL_BALLS - 1, d.MODEL_BALLS)}}}',
        rf'\dfrac{{1}}{{{choose(d.MODEL_N, d.MODEL_BALLS)}}}',
    )
    cards = VGroup()
    for title, color, formula, value in zip(MODEL_TITLES, MODEL_COLOURS, explanations, d.MODEL_PROBABILITIES, strict=True):
        exact = rf'\dfrac{{{value.numerator}}}{{{value.denominator}}}'
        heading = sans(title, 28, color, 'BOLD')
        if heading.width > 3.52:
            heading.scale_to_fit_width(3.52)
        body = math(rf'{formula}={exact}', 40)
        frame = card(3.95, 2.0).set_stroke(color, 2)
        heading.set_y(.62)
        body.set_y(-.24)
        assert frame.get_right()[0] - max(heading.get_right()[0], body.get_right()[0]) > .15
        assert body.get_bottom()[1] - frame.get_bottom()[1] > .10
        cards.add(VGroup(frame, heading, body))
    cards.arrange(RIGHT, buff=.20, aligned_edge=UP)
    answer = stack(box('example', 'Example 3.3', ['One arrangement, three probabilities']),
                   occupancy_strip(d.MODEL_VECTOR, stars=True),
                   math(vector(d.MODEL_VECTOR), 41), cards, gap=.29)
    return answer, cards


def sequence_parts(sequence, *, counter=False):
    colors = {'E': MUTED, 'O': ACCENT} if counter else {'A': ACCENT, 'B': NEXT}
    marks, lengths = VGroup(), VGroup()
    step = .75 if counter else .96
    for i, letter in enumerate(sequence):
        x = (i - (len(sequence) - 1) / 2) * step
        frame = card(step - .07, .74)
        color = colors[letter]
        shape = VGroup(frame, mono(letter, 29 if counter else 38, color, 'BOLD')).set_x(x)
        if counter:
            shape.add(Line(LEFT * .22, RIGHT * .22, color=color, stroke_width=3).move_to(
                frame.get_top() + UP * .08))
        marks.add(shape)
    brackets = VGroup()
    start = 0
    for letter, run in groupby(sequence):
        size = sum(1 for _ in run)
        color = colors[letter]
        left, right = marks[start].get_left().copy(), marks[start + size - 1].get_right().copy()
        left[1] = right[1] = -.72
        brackets.add(VGroup(Line(left, right, color=color),
                            Line(left, left + UP * .16, color=color),
                            Line(right, right + UP * .16, color=color)))
        lengths.add(mono(str(size), 29, color).move_to((left + right) / 2 + DOWN * .27))
        start += size
    return marks, brackets, lengths


def runs_card(*, counter=False):
    sequence = d.COUNTER if counter else d.RUN_WORD
    parts = sequence_parts(sequence, counter=counter)
    picture = VGroup(*parts)
    if counter:
        title = box('example', 'Example 3.4', [f'A lunch counter with {len(sequence)} seats'])
        caption = row(pill(f'{d.OCCUPIED} occupied runs', ACCENT, 29),
                      pill(f'{d.MAX_RUNS - d.OCCUPIED} empty runs', TEXT2, 29),
                      pill(f'{d.MAX_RUNS} runs total', NEXT, 29))
    else:
        title = sans('Runs of equal letters', 47, TEXT, 'BOLD')
        caption = math(vector(d.RUN_SIZES), 39, TEXT2)
    return stack(title, panel(picture, width=picture.width + .52), caption, gap=.39), parts


class Video(LessonScene):
    folder = str(HERE)
    number = '3.1'
    section_title = 'Occupancy Problems and the Three Statistics'
    lesson_k = 5

    def construct(self):
        self.welcome()
        self.occupancy()
        self.stars_and_bars()
        self.no_empty_cells()
        self.dice_and_derivatives()
        self.labelled_placements()
        self.cell_roles()
        self.configurations()
        self.statistics()
        self.compare_models()
        self.runs()
        self.lunch_counter()
        self.code_lab()
        self.finish_lesson()

    def beat(self, cue, share):
        self.wait(max(.10, cue.left() * share))

    def complete(self, block):
        self.remove(*block.get_family())
        self.add(block)

    def welcome(self):
        with self.seg('welcome') as cue:
            self.show(title_card(self.number, self.section_title, self.lesson_k))
            self.beat(cue, .25)
            old_strip = four.dots_and_dividers()
            self.show(old_strip)
            self.beat(cue, .33)
            marks = old_strip[1][0][0]
            prior_occupancy = (four.SAMPLE_SIZE, *((0,) * (len(four.SAMPLE_POOL) - 1)))
            boxes, names, balls, _ = cell_boxes(prior_occupancy)
            dividers = VGroup(*(divider().set_x((a.get_x() + b.get_x()) / 2).set_y(a.get_y())
                                for a, b in zip(boxes, boxes[1:])))
            result = panel(VGroup(boxes, names, balls, dividers), width=5.1)
            paths = [item.copy() for item in marks]
            self.place(result)
            self.add(*paths)
            self.play(FadeIn(result[0]), FadeIn(boxes), FadeIn(names),
                      *(Transform(source, target) for source, target in zip(
                          paths, (*balls[0], *dividers), strict=True)), run_time=1)
            self.remove(*paths)
            self.complete(result)
        with self.seg('recap') as cue:
            table, fills = four.summary_table()
            groups = VGroup()
            offset = 0
            for i, (size, color) in enumerate(zip(four.GROUPS, (ACCENT, NEXT, SKY), strict=True)):
                groups.add(four.letter_tray(f'Team {four.POPULATION[i]}',
                                            four.POPULATION[offset:offset + size], color))
                offset += size
            groups.arrange(DOWN, buff=.14)
            groups.scale(.70)
            multinomial = stack(groups, math(r'\dfrac{n!}{r_1!\cdots r_k!}', 38), gap=.26)
            block = row(table, panel(multinomial, width=2.55), gap=.36)
            self.show(block)
            unordered = SurroundingRectangle(VGroup(table[2], fills[1], fills[3]), color=NEXT, buff=.065)
            self.play(Create(unordered), run_time=.55)
            without = SurroundingRectangle(fills[1], color=ACCENT, buff=.035)
            with_replacement = SurroundingRectangle(fills[3], color=ACCENT, buff=.035)
            self.play(Create(without), run_time=.5)
            self.beat(cue, .55)
            self.play(Transform(without, with_replacement), run_time=.55)
            block.add(unordered, without)
            self.complete(block)

    def occupancy(self):
        with self.seg('count_cells') as cue:
            bins = occupancy_strip(d.CELLS)
            total = math('+'.join(map(str, d.CELLS)) + f'={d.BALLS}', 46, ACCENT)
            general = math(r'r_1+\cdots+r_n=r,\qquad r_k\ge0\qquad(3.1)', 43)
            block = stack(bins, total, general, gap=.39)
            self.place(block)
            self.play(FadeIn(bins), run_time=.85)
            self.beat(cue, .37)
            self.play(FadeIn(total), run_time=.55)
            self.beat(cue, .43)
            self.play(FadeIn(general), run_time=.55)
            self.complete(block)
        with self.seg('forget_labels') as cue:
            frames, names, balls, counts = cell_boxes(d.CELLS, letters='ABCDEFGH')
            total = math(rf'\text{{Total}}={d.BALLS}', 45, ACCENT)
            block = stack(VGroup(frames, names, balls, counts), total, gap=.43)
            self.show(block)
            a, b = balls[0][0], balls[1][0]
            self.beat(cue, .13)
            self.play(a.animate.move_to(b), b.animate.move_to(a), run_time=.95)
            self.beat(cue, .20)
            empty = mono('0', 36, WARN).move_to(counts[1])
            filled = mono('1', 36, ACCENT).move_to(counts[2])
            self.play(a.animate.move_to(frames[2]), Transform(counts[1], empty),
                      Transform(counts[2], filled), run_time=1.12)
            self.beat(cue, .23)
            self.play(Transform(total, math(vector((d.CELLS[0], 0, 1, *d.CELLS[3:])), 45, ACCENT)
                                .move_to(total)), run_time=.72)

    def stars_and_bars(self):
        with self.seg('make_symbol') as cue:
            block, symbol = star_card()
            original = occupancy_strip(d.CELLS)
            flat = block[1]
            self.place(block)
            original.move_to(symbol)
            self.play(FadeIn(block[0]), FadeIn(flat[0]), FadeIn(original), run_time=.8)
            self.beat(cue, .15)
            site_symbol = svg_figure('stars-bars.svg').scale_to_fit_width(symbol.width).move_to(symbol)
            # Match the site layout while preserving each dot as it turns into a star.
            moving = [item.copy() for cell in original[2] for item in cell]
            self.add(*moving)
            self.play(FadeOut(original), FadeIn(site_symbol), run_time=.60)
            self.play(FadeOut(site_symbol), FadeIn(symbol[0]), FadeIn(symbol[2]),
                      *(Transform(dot, star) for dot, star in zip(moving, symbol[1], strict=True)),
                      run_time=1.12)
            self.remove(*moving)
            self.complete(block)
            self.beat(cue, .50)
            empty_cells = SurroundingRectangle(VGroup(*symbol[0][2:5], *symbol[2][2:4]), color=WARN,
                                               buff=.12, corner_radius=.08)
            self.play(Create(empty_cells), run_time=.60)
            self.beat(cue, .44)
            self.play(FadeOut(empty_cells), run_time=.4)
        with self.seg('count_symbols') as cue:

            symbol = symbol_parts(d.CELLS)
            slot_marks = VGroup(*sorted([*symbol[0][1:-1], *symbol[1]], key=lambda mob: mob.get_x()))
            rectangles = VGroup(*(Rectangle(width=.62, height=.74, color=BORDER2, stroke_width=1.4)
                                  .move_to(item) for item in slot_marks))
            details = mono(f'{d.BALLS} stars  ·  {d.INNER_BARS} bars  ·  {d.MOVABLE} movable positions', 30, TEXT2)
            specific = rf'{choose(d.MOVABLE, d.BALLS)}={choose(d.MOVABLE, d.INNER_BARS)}={d.STAR_ORDERS}'
            general = r'A_{r,n}=\binom{n+r-1}{r}=\binom{n+r-1}{n-1}\qquad(3.2)'
            formulas = derivation([specific, general])
            marks = VGroup(symbol[0], symbol[1], rectangles)
            block = stack(marks, details, formulas, gap=.42)
            self.place(block)
            self.play(FadeIn(symbol[0]), FadeIn(symbol[1]), run_time=.65)
            self.play(symbol[0][0].animate.shift(UP * .53).set_opacity(.4),
                      symbol[0][-1].animate.shift(UP * .53).set_opacity(.4), FadeIn(rectangles), run_time=.82)
            self.play(FadeIn(details), run_time=.45)
            self.beat(cue, .26)
            for selection, color in ((symbol[1], ACCENT), (symbol[0][1:-1], NEXT)):
                self.play(*(frame.animate.set_stroke(
                    color if item in selection else BORDER2, width=2
                ) for frame, item in zip(rectangles, slot_marks, strict=True)), run_time=.62)
                self.beat(cue, .23)
            formulas.reveal(self, run_time=.7, step_time=.75)
            self.complete(block)

    def no_empty_cells(self):
        with self.seg('bars_in_gaps') as cue:
            stars, gaps, bars, ends = gap_parts()
            board = VGroup(stars, gaps, bars, ends)
            formula = math(rf'{choose(d.GAPS, d.INNER_BARS)}={d.NONEMPTY}\qquad\binom{{r-1}}{{n-1}}', 45)
            block = stack(box('theorem', 'Theorem 3.1', ['(ii) Require every cell to contain a ball']),
                          panel(board, width=8.5, height=1.25), formula, gap=.47)
            self.place(block)
            self.play(FadeIn(block[0]), FadeIn(block[1][0]), FadeIn(stars), FadeIn(ends), run_time=.75)
            self.beat(cue, .33)
            self.play(FadeIn(gaps), run_time=.64)
            self.beat(cue, .22)
            self.play(LaggedStart(*(FadeIn(bar, shift=DOWN * .40) for bar in bars), lag_ratio=.26), run_time=1.45)
            self.beat(cue, .26)
            self.play(FadeIn(formula), run_time=.58)
            self.complete(block)
        with self.seg('reserve_one') as cue:
            frames, labels, balls, _ = cell_boxes(d.NONEMPTY_VECTOR, stars=True)
            cells = VGroup(frames, labels, balls)
            extras = VGroup(*(source for cell in balls for source in cell[1:]))
            target = VGroup(*(mark(star=True, radius=.15) for _ in range(d.LEFTOVER))).arrange(RIGHT, buff=.24)
            spare = row(target, mono(f'{d.LEFTOVER} left to place', 29, NEXT))
            formula = math(r'A_{r-n,n}=\binom{r-1}{n-1}\quad(r\ge n)', 43)
            impossible = panel(row(sans('Impossible when', 31, WARN), math('r<n', 37, WARN)), color=WARN)
            block = stack(cells, spare, formula, impossible, gap=.35)
            self.place(block)
            self.play(FadeIn(cells), run_time=.73)
            self.beat(cue, .23)
            self.play(
                *(Transform(source, dest) for source, dest in zip(extras, target, strict=True)),
                *(cell[0].animate.move_to(frame) for cell, frame in zip(balls, frames, strict=True)),
                FadeIn(spare[1]), run_time=1.0,
            )
            self.remove(*extras)
            self.add(target)
            self.beat(cue, .29)
            self.play(FadeIn(formula), run_time=.65)
            self.beat(cue, .44)
            self.play(FadeIn(impossible), run_time=.6)
            block[0] = VGroup(frames, labels, VGroup(*(cell[0] for cell in balls)))
            self.complete(block)

    def dice_and_derivatives(self):
        with self.seg('dice_outcomes') as cue:
            block, dice = dice_card()
            base = block[1][0]
            roll = row(*(die_face(value, .72, ACCENT) for value in d.ROLL), gap=.24)
            self.place(block)
            roll.move_to(base)
            tilts = (.28, -.22, .19)
            for die, angle in zip(roll, tilts, strict=True):
                die.rotate(angle)
            self.play(FadeIn(block[0]), FadeIn(roll, shift=DOWN * .25), run_time=.76)
            self.play(*(die.animate.rotate(-angle) for die, angle in zip(roll, tilts, strict=True)),
                      run_time=.52)
            self.beat(cue, .25)
            self.play(FadeIn(base[0]), FadeIn(base[1]), *(Transform(a, b) for a, b in zip(
                roll, dice, strict=True)), run_time=1.1)
            self.beat(cue, .22)
            self.play(FadeIn(base[2]), FadeIn(block[2]), run_time=.65)
            self.beat(cue, .28)
            self.play(FadeIn(block[3]), run_time=.62)
            self.remove(*roll.get_family())
            self.complete(block)
        with self.seg('derivative_orders') as cue:
            frames, names, marks, totals = cell_boxes(d.DIFFERENTIATION_VECTOR, names=d.VARIABLES,
                                                      letters=''.join(sorted(d.DIFFERENTIATIONS)), letter_tiles=True)
            tiles = row(*(panel(mono(letter, 34, ACCENT), .56, .53)
                          for letter in d.DIFFERENTIATIONS), gap=.19)
            results = row(*(panel(stack(sans(f'Order {order}', 28, TEXT2),
                                        math(rf'{choose(order + len(d.VARIABLES) - 1, order)}={number}', 44, NEXT)),
                                   3, 1.4)
                            for order, number in zip(d.ORDERS, d.DERIVATIVE_COUNTS, strict=True)), gap=.31)
            bins = VGroup(frames, names, marks, totals)
            block = stack(tiles, bins, results, gap=.37)
            self.place(block)
            self.play(FadeIn(tiles), FadeIn(frames), FadeIn(names), run_time=.75)
            self.beat(cue, .21)
            sources = [tile.copy() for tile in tiles]
            destinations = (marks[0][0], marks[1][0], marks[0][1], marks[2][0])
            self.add(*sources)
            self.play(*(Transform(a, b) for a, b in zip(sources, destinations, strict=True)),
                      FadeIn(totals), run_time=1.06)
            self.remove(*sources)
            self.add(marks)
            self.beat(cue, .45)
            self.play(FadeIn(results[0]), run_time=.65)
            self.beat(cue, .34)
            self.play(FadeIn(results[1]), run_time=.65)
            self.complete(block)

    def labelled_placements(self):
        with self.seg('fixed_vector') as cue:
            grid, outlines = grid_block()
            grid.scale(.70)
            outlines.scale(.70, about_point=grid.get_center())
            subset = VGroup(*(tile.copy() for tile, parts in zip(grid, placements.values(), strict=True)
                              if tuple(map(len, parts)) == d.FIXED_VECTOR)).arrange(DOWN, buff=.20)
            left = stack(sans(f'All {d.FIXED_TOTAL} placements', 33, TEXT2), VGroup(grid, outlines), gap=.24)
            right = stack(sans(vector(d.FIXED_VECTOR), 35, ACCENT), subset, gap=.25)
            odds = math(rf'{frac(d.FIXED_COUNT, d.FIXED_TOTAL)}={frac(d.FIXED_PROB)}', 52, ACCENT)
            block = stack(row(left, panel(right, width=2.4), gap=.40), odds, gap=.26)
            self.place(block)
            self.play(FadeIn(left[0]), FadeIn(grid), run_time=.9)
            self.beat(cue, .40)
            self.play(*(Create(outline) for outline in outlines), FadeIn(block[0][1]), run_time=.95)
            self.beat(cue, .32)
            self.play(FadeIn(odds), run_time=.55)
            self.complete(block)
        with self.seg('mb_probability'):
            sample = VGroup(*cell_boxes(d.FIXED_VECTOR, names=('X', 'Y', 'Z'), letters='abc'))
            groups = math(r'(r_1,\ldots,r_n)', 42)
            formula = derivation([
                r'\dfrac{r!}{r_1!\cdots r_n!}\qquad\text{favourable placements}',
                r'\dfrac{r!}{r_1!\cdots r_n!}\,n^{-r}\qquad(3.3)',
            ])
            example = pill(f'{vector(d.FIXED_VECTOR)} has probability {d.FIXED_PROB}', ACCENT, 28)
            self.show(stack(sans(MODEL_TITLES[0], 43, TEXT, 'BOLD'),
                            row(sample, groups, gap=.55), formula, example, gap=.32))

    def cell_roles(self):
        sizes = ''.join(f'{size}!' for size in d.TARGET_ROLES.values())
        role_formula = rf'\dfrac{{{d.TARGET_N}!}}{{{sizes}}}={d.CELL_CHOICES}'
        with self.seg('choose_cell_roles') as cue:
            cells = role_cells(d.TARGET)
            header = box('example', 'Example 3.2', ['First choose the role of each cell'])
            target = math(vector(d.TARGET), 40)
            equation = math(role_formula, 48, ACCENT)
            block = stack(header, target, cells, equation, gap=.34)
            self.place(block)
            self.play(FadeIn(header), FadeIn(target), FadeIn(cells), run_time=.82)
            self.beat(cue, .32)
            rotation = (d.TARGET[-1], *d.TARGET[:-1])
            for order in (rotation, d.TARGET):
                alternate = role_cells(order).move_to(cells)
                self.play(Transform(cells, alternate), run_time=.75)
                self.beat(cue, .20)
            self.play(FadeIn(equation), run_time=.6)
            self.complete(block)
        with self.seg('assign_balls') as cue:
            cells = role_cells(d.TARGET, filled=True)
            factorials = ''.join(f'{count}!' for count in d.TARGET)
            ball_formula = rf'\dfrac{{{d.TARGET_BALLS}!}}{{{factorials}}}={grouped(d.BALL_CHOICES)}'
            counts = rf'{d.CELL_CHOICES}\cdot{grouped(d.BALL_CHOICES)}={grouped(d.FAVOURABLE)}'
            probability = (rf'\dfrac{{{grouped(d.FAVOURABLE)}}}{{{d.TARGET_N}^{d.TARGET_BALLS}}}'
                           rf'\approx{float(d.EXACT):.4f}\qquad(3.4)')
            factors = stack(row(pill('Cell roles', ACCENT, 27), math(role_formula, 40)),
                            row(pill('Ball allocations', NEXT, 27), math(ball_formula, 40)), gap=.20)
            counts_line = math(counts, 44)
            probability_line = math(probability, 46, ACCENT)
            block = stack(cells, factors, counts_line, probability_line, gap=.32)
            self.place(block)
            self.play(FadeIn(VGroup(*cells[:3])), FadeIn(factors[0]), run_time=.70)
            filled = [item for group in cells[3] for item in group]
            self.play(LaggedStart(*(FadeIn(item, shift=UP * .35) for item in filled), lag_ratio=.13), run_time=1.10)
            self.beat(cue, .26)
            self.play(FadeIn(factors[1]), run_time=.65)
            self.beat(cue, .28)
            self.play(FadeIn(counts_line), run_time=.55)
            self.beat(cue, .24)
            self.play(FadeIn(probability_line), run_time=.57)
            self.complete(block)

    def configurations(self):
        with self.seg('configuration_table') as cue:
            table, entries = table_card()
            self.place(table)
            self.play(FadeIn(table[0]), FadeIn(table[1][0]), run_time=.72)
            self.play(LaggedStart(*(FadeIn(entry, shift=UP * .09) for entry in entries),
                                  lag_ratio=.25), run_time=min(6, cue.left() * .37))
            self.complete(table)
        with self.seg('even_and_typical') as cue:
            even = entries[d.CONFIGURATIONS.index(d.EVEN)]
            top = entries[0]
            for entry, color in ((top, ACCENT), (even, WARN)):
                target = entry.copy()
                highlight_row(target, color)
                self.play(Transform(entry, target), run_time=.65)
                if entry is top:
                    self.beat(cue, .30)


    def statistics(self):
        example = d.FIXED_VECTOR
        vector_count = math(rf'{choose("n+r-1", "r")}=A_{{r,n}}', 40)
        with self.seg('mb_model') as cue:
            frames, labels, balls, _ = cell_boxes(example, names=('X', 'Y', 'Z'), letters='abc')
            cells = VGroup(frames, labels, balls)
            possibilities = math(r'n^r\text{ equally likely placements}', 40)
            weight = math(r'\dfrac{r!}{r_1!\cdots r_n!}\,n^{-r}\qquad(3.3)', 43)
            block = panel(stack(sans(MODEL_TITLES[0], 48, ACCENT, 'BOLD'), cells,
                                possibilities, weight, gap=.41), width=10.5)
            self.show(block)
            self.beat(cue, .42)
            self.play(balls[0][1].animate.move_to(frames[2]), run_time=1.0)
        with self.seg('be_model') as cue:
            stars = VGroup(*cell_boxes(example, names=('X', 'Y', 'Z'), stars=True, color=NEXT)[:3])
            heading = sans(MODEL_TITLES[1], 48, NEXT, 'BOLD')
            weights = row(vector_count, math(r'\dfrac{1}{A_{r,n}}\text{ each}', 43, NEXT), gap=.48)
            block = panel(stack(heading, stars, weights, gap=.45), width=10.5)
            # Carry the labelled particles through to the stars on the next card.
            sources = [item.copy() for cell in balls for item in cell]
            targets = [item for cell in stars[2] for item in cell]
            self.place(block)
            self.add(*sources)
            self.play(FadeIn(block[0]), FadeIn(heading), FadeIn(stars[0]), FadeIn(stars[1]),
                      *(Transform(source, target) for source, target in zip(sources, targets, strict=True)),
                      run_time=1.10)
            self.remove(*sources)
            self.add(stars[2])
            self.beat(cue, .26)
            self.play(FadeIn(weights), run_time=.68)
            self.complete(block)
        with self.seg('fd_model') as cue:
            frames, names, stars, _ = cell_boxes(tuple(int(n > 0) for n in example),
                                                 names=('X', 'Y', 'Z'), stars=True, color=WARN)
            occupied_frames = [frame for frame, group in zip(frames, stars, strict=True) if len(group)]
            locks = VGroup()
            for frame in occupied_frames:
                body = Rectangle(width=.23, height=.18, fill_color=WARN, fill_opacity=1, stroke_width=0)
                shackle = Arc(radius=.075, start_angle=0, angle=pi, color=WARN, stroke_width=3)
                shackle.move_arc_center_to(body.get_top())
                locks.add(VGroup(shackle, body).next_to(frame, DOWN, buff=.16))
            cells = VGroup(frames, names, stars, locks)
            restriction = math(r'r\le n,\qquad\binom nr\text{ subsets}', 43)
            weight = math(r'\dfrac{1}{\binom nr}\text{ each}', 44, WARN)
            block = panel(stack(sans(MODEL_TITLES[2], 48, WARN, 'BOLD'), cells,
                                row(restriction, weight, gap=.73), gap=.43), width=10.5)
            self.place(block)
            content = block[1]
            self.play(FadeIn(block[0]), FadeIn(content[0]), FadeIn(frames), FadeIn(names), FadeIn(stars), run_time=.75)
            self.beat(cue, .22)
            self.play(*(frame.animate.set_stroke(WARN, width=3) for frame in occupied_frames),
                      FadeIn(locks), run_time=.74)
            self.beat(cue, .26)
            self.play(FadeIn(content[2]), run_time=.6)
            self.complete(block)

    def compare_models(self):
        with self.seg('three_probabilities') as cue:
            block, cards = comparison_cards()
            self.place(block)
            self.play(FadeIn(block[0]), FadeIn(block[1]), FadeIn(block[2]), run_time=.8)
            self.beat(cue, .22)
            for card_ in cards:
                self.play(FadeIn(card_, shift=UP * .12), run_time=.64)
                self.beat(cue, .23)
            self.complete(block)
        with self.seg('misprints') as cue:
            word = 'THE PRINTED LINE'
            positions = tuple(i for i, char in enumerate(word) if char != ' ')
            errors = tuple(positions[i] for i, n in enumerate(d.MODEL_VECTOR) if n)
            letters = VGroup()
            for i, char in enumerate(word):
                if char != ' ':
                    letters.add(VGroup(card(.64, .73), mono(char, 35, TEXT2, 'BOLD')).set_x(i * .71))
            letters.center()
            marks = VGroup()
            for index in errors:
                letter = letters[positions.index(index)]
                marks.add(mono('×', 30, WARN, 'BOLD').next_to(letter, UP, buff=.13))
            rule = pill('At most one misprint mark per position', WARN, 33)
            block = stack(sans('Misprints', 46, TEXT, 'BOLD'),
                          panel(VGroup(letters, marks), width=11.7, height=1.65), rule, gap=.43)
            self.place(block)
            self.play(FadeIn(block[0]), FadeIn(block[1][0]), FadeIn(letters), run_time=.76)
            self.beat(cue, .29)
            self.play(LaggedStart(*(FadeIn(item, shift=DOWN * .12) for item in marks),
                                  lag_ratio=.28), run_time=1.06)
            self.beat(cue, .29)
            self.play(FadeIn(rule), run_time=.56)
            self.complete(block)

    def runs(self):
        with self.seg('find_runs') as cue:
            block, (letters, brackets, lengths) = runs_card()
            self.place(block)
            self.play(FadeIn(block[0]), FadeIn(block[1][0]), run_time=.66)
            self.play(LaggedStart(*(FadeIn(letter) for letter in letters), lag_ratio=.23), run_time=1.45)
            self.beat(cue, .20)
            self.play(LaggedStart(*(Create(bracket) for bracket in brackets), lag_ratio=.48), run_time=2.65)
            self.beat(cue, .37)
            self.play(FadeIn(lengths), FadeIn(block[2]), run_time=.65)
            self.complete(block)
        with self.seg('run_count') as cue:
            marks, brackets, _ = sequence_parts(d.AB_WORD)
            header = box('property', 'Property 3.1', [r'$n_1$ runs of A and $n_1+1$ runs of B'])
            rule = math(r'\binom{a-1}{n_1-1}\binom{b-1}{n_1}', 47)
            worked = math(rf'{choose(d.A_COUNT-1, d.A_RUNS-1)}{choose(d.B_COUNT-1, d.A_RUNS)}'
                          rf'={d.A_SPLITS}\cdot{d.B_SPLITS}={d.RUN_COUNT}', 47, ACCENT)
            block = stack(header, VGroup(marks, brackets), rule, worked, gap=.41)
            self.place(block)
            self.play(FadeIn(header), FadeIn(marks), run_time=.79)
            self.beat(cue, .22)
            self.play(*(Create(bracket) for bracket in brackets), run_time=.92)
            self.beat(cue, .23)
            self.play(FadeIn(rule), run_time=.64)
            self.beat(cue, .45)
            self.play(FadeIn(worked), run_time=.6)
            self.complete(block)

    def lunch_counter(self):
        with self.seg('counter_runs') as cue:
            block, (seats, brackets, lengths) = runs_card(counter=True)
            self.place(block)
            self.play(FadeIn(block[0]), FadeIn(block[1][0]), FadeIn(seats), run_time=.86)
            self.beat(cue, .23)
            self.play(LaggedStart(*(Create(bracket) for bracket in brackets), lag_ratio=.21), run_time=2.75)
            self.play(FadeIn(lengths), FadeIn(block[2]), run_time=.66)
            self.complete(block)
            self.beat(cue, .31)
            ends = VGroup(*(SurroundingRectangle(seats[index], color=WARN, buff=.046, corner_radius=.055)
                           for index in (0, -1)))
            self.play(*(Create(outline) for outline in ends), run_time=.61)
            self.beat(cue, .24)
            occupied_index = d.COUNTER.index('O')
            first, occupant = seats[0][1], seats[occupied_index][1]
            start_mark, occupied_mark = seats[0][2], seats[occupied_index][2]
            self.play(first.animate.move_to(occupant), occupant.animate.move_to(first),
                      start_mark.animate.set_color(ACCENT), occupied_mark.animate.set_color(MUTED),
                      FadeOut(brackets), FadeOut(lengths), FadeOut(block[2]), run_time=.85)
            self.beat(cue, .26)
            self.play(first.animate.move_to(occupant), occupant.animate.move_to(first),
                      start_mark.animate.set_color(MUTED), occupied_mark.animate.set_color(ACCENT),
                      FadeIn(brackets), FadeIn(lengths), FadeIn(block[2]), FadeOut(ends), run_time=.73)
            self.complete(block)
        with self.seg('counter_probability') as cue:
            marks, brackets, lengths = sequence_parts(d.COUNTER, counter=True)
            occupied = tuple(i for i, label in enumerate(d.COUNTER) if label == 'O')
            assert len(occupied) == d.OCCUPIED
            board = panel(VGroup(marks, brackets, lengths))
            favourable = rf'{choose(d.OCCUPIED-1, d.OCCUPIED-1)}{choose(d.EMPTY-1, d.OCCUPIED)}={d.COUNTER_MATCHES}'
            total = rf'{choose(len(d.COUNTER), d.OCCUPIED)}={grouped(d.COUNTER_TOTAL)}'
            result = (rf'\dfrac{{{d.COUNTER_MATCHES}}}{{{grouped(d.COUNTER_TOTAL)}}}'
                      rf'=\dfrac{{{d.COUNTER_PROB.numerator}}}{{{d.COUNTER_PROB.denominator}}}'
                      rf'\approx{float(d.COUNTER_PROB):.4f}')
            formula = derivation([favourable + r'\qquad\text{maximum-run seatings}',
                                  total + r'\qquad\text{all seatings}', result])
            block = stack(board, formula, gap=.55)
            self.place(block)
            self.play(FadeIn(board), run_time=.78)
            self.beat(cue, .16)
            self.play(*(Transform(marks[i][1], divider(ACCENT).match_height(marks[i][0]).scale(.74)
                                  .move_to(marks[i][1])) for i in occupied), run_time=.76)
            self.beat(cue, .22)
            formula.reveal(self, run_time=.8, step_time=1.05)
            self.complete(block)

    def code_lab(self):
        with self.seg('code') as cue:
            self.show(code_cell(d.CODE, d.CODE_OUTPUT), step_time=min(1.45, cue.left() / 13))
        with self.seg('code_result'):
            simulated, exact = d.CODE_OUTPUT.split()
            cards = row(panel(stack(sans('Simulated', 37, TEXT2), math(simulated, 58, ACCENT)), 4.30, 1.85, ACCENT),
                        panel(stack(sans('Exact (rounded)', 37, TEXT2), math(exact, 58, NEXT)), 4.30, 1.85, NEXT),
                        gap=.35)
            self.show(stack(occupancy_strip(d.TARGET), cards, gap=.62))

    def finish_lesson(self):
        with self.seg('recall'):
            ideas = key_ideas(d.KEY_IDEAS, pause=5)
            self.place(ideas)
            ideas.start_recall(self)
        ideas.countdown(self)
        with self.seg('ideas') as cue:
            ideas.reveal_items(self, step_time=max(.25, cue.left() * .20))
            self.complete(ideas)
        with self.seg('end'):
            self.show(end_card(d.NEXT_TITLE))


class StarsStill(Video):
    def construct(self):
        block, _ = star_card()
        self.place(block)
        self.add(block)


class DiceStill(Video):
    def construct(self):
        block, _ = dice_card()
        self.place(block)
        self.add(block)


class TableStill(Video):
    def construct(self):
        block, entries = table_card()
        highlight_row(entries[0], ACCENT)
        highlight_row(entries[d.CONFIGURATIONS.index(d.EVEN)], WARN)
        self.place(block)
        self.add(block)


class ModelsStill(Video):
    def construct(self):
        block, _ = comparison_cards()
        self.place(block)
        self.add(block)


class RunsStill(Video):
    def construct(self):
        block, _ = runs_card()
        self.place(block)
        self.add(block)


class CounterStill(Video):
    def construct(self):
        block, _ = runs_card(counter=True)
        self.place(block)
        self.add(block)
