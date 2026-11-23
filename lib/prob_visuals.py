"""Reusable outcome graphics for the Probability Theory lessons."""

from collections import Counter
from collections.abc import Sequence
from itertools import product

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UP, Circle, Ellipse, FadeIn, Line, MathTex, Rectangle,
    RoundedRectangle, Star, Transform, VGroup,
)

from brand import ACCENT, BG, BORDER2, MUTED, NEXT, SURFACE, TEXT, TEXT2, WARN, card, mono, pill
from lesson_kit import inline_text

BALL_COLORS = {'a': ACCENT, 'b': NEXT, 'c': WARN}
MINI_BALL_RADIUS = 0.185


def labelled_ball(label, radius, show_label=True):
    if not show_label:
        return Star(n=5, outer_radius=radius, color=TEXT2, fill_opacity=0.85, stroke_width=0)

    disc = Circle(radius=radius, color=BALL_COLORS[label], fill_opacity=1, stroke_width=0)
    reference = mono('Habc', 48, BG, 'BOLD', disable_ligatures=True)
    cap, x_height, ascender = reference[0], reference[1], reference[2]
    # One font scale and one baseline for all three glyphs.
    optical_center = cap.get_bottom()[1] + (x_height.height + ascender.height) / 4
    letter = reference['abc'.index(label) + 1]
    letter.shift(LEFT * letter.get_x() + DOWN * optical_center)
    letter.scale(2 * radius * 0.65 / ascender.height, about_point=ORIGIN)
    return VGroup(disc, letter)


def cells_for(cells, *, compact=False, labelled=True):
    width, height, radius = (0.405, 1.18, MINI_BALL_RADIUS) if compact else (2.4, 1.55, 0.31)
    boxes = VGroup(*(card(width, height) for _ in cells)).arrange(RIGHT, buff=0.055 if compact else 0.19)
    balls = VGroup()
    spacing = 2.10 if compact else 2.25
    direction = DOWN if compact else RIGHT
    for cell, cell_box in zip(cells, boxes, strict=True):
        for index, label in enumerate(cell):
            offset = (index - (len(cell) - 1) / 2) * radius * spacing
            balls.add(labelled_ball(label, radius, labelled).move_to(cell_box).shift(direction * offset))
    return boxes, balls


TILE_CELL = 0.38        # width of one compartment in a 27-grid tile
TILE_PAD = 0.05
TILE_HEIGHT = 1.12
GRID_BALL = 0.16


def arrangement(cells, index=None):
    """One sample point: a closed box with three compartments, numbered underneath.
    tile[0] = VGroup(frame, dividers), tile[1] = balls, tile[2] = number (when labelled)."""
    labelled = index is not None
    width = 3 * TILE_CELL + 2 * TILE_PAD
    frame = RoundedRectangle(width=width, height=TILE_HEIGHT, corner_radius=0.12, fill_color=SURFACE,
                             fill_opacity=1, stroke_color=BORDER2, stroke_width=1.6)
    left = frame.get_left()[0] + TILE_PAD
    top, bottom = frame.get_top()[1] - 0.10, frame.get_bottom()[1] + 0.10
    dividers = VGroup(*(Line([left + k * TILE_CELL, bottom, 0], [left + k * TILE_CELL, top, 0],
                             color=BORDER2, stroke_width=1.2) for k in (1, 2)))
    balls = VGroup()
    for k, cell in enumerate(cells):
        x = left + (k + 0.5) * TILE_CELL
        for j, label in enumerate(cell):
            y = frame.get_y() + ((len(cell) - 1) / 2 - j) * GRID_BALL * 2.12
            balls.add(labelled_ball(label, GRID_BALL, labelled).move_to([x, y, 0]))
    body = VGroup(VGroup(frame, dividers), balls)
    if labelled:
        body.add(mono(f'{index:02d}', 29, MUTED).next_to(frame, DOWN, buff=0.09))
    return body


def arrangement_grid(arrangements):
    return VGroup(*(arrangement(row, index) for index, row in arrangements.items())).arrange_in_grid(
        rows=3, cols=9, buff=(0.22, 0.15),
    )


def formula_pill(label, size):
    text = inline_text(label, size, ACCENT)
    return VGroup(card(text.width + 0.55, text.height + 0.34).move_to(text), text)


def dice_matrix(total=6, sum_label='Sum is six', show_odd=True):
    points = VGroup()
    intersection = None
    for a, b in product(range(1, 7), repeat=2):
        pair = MathTex(f'({a},{b})', font_size=25, color=TEXT2 if a + b == total or (show_odd and a % 2 == b % 2 == 1) else MUTED)
        marks = VGroup()
        if a + b == total:
            marks.add(RoundedRectangle(width=1.09, height=0.63, corner_radius=0.09,
                                       color=ACCENT, stroke_width=2.8))
        if (show_odd and a % 2 == b % 2 == 1):
            marks.add(Ellipse(width=0.92, height=0.50, color=NEXT, stroke_width=3))
        square = Rectangle(width=1.10, height=0.64, stroke_width=0)
        outcome = VGroup(square, pair, marks)
        points.add(outcome)
        if (a, b) == (3, 3):
            intersection = outcome
    points.arrange_in_grid(rows=6, cols=6, buff=(0.21, 0.08))
    labels = VGroup(pill(sum_label, ACCENT, 31))
    if show_odd:
        labels.add(pill('Both faces odd', NEXT, 31))
    labels.arrange(RIGHT, buff=0.35)
    return VGroup(labels, points).arrange(DOWN, buff=0.34), intersection


def coin_outcome_cards(outcomes):
    tiles = VGroup()
    for outcome in outcomes:
        tile = card(2.30, 1.25)
        tiles.add(VGroup(tile, mono(outcome, 54, TEXT).move_to(tile)))
    tiles.arrange_in_grid(rows=len(outcomes) // 4, cols=4, buff=(0.34, 0.30))
    return tiles


def tournament_sequences(outcomes: Sequence[str], size=54, color=NEXT, gap=.28):
    return VGroup(*(mono(outcome, size, color) for outcome in outcomes)).arrange(DOWN, buff=gap)


def collapse_arrangements(self, arrangements, g, *, pace=1.0):
    """Animate numbered arrangements becoming weighted occupancy configurations."""
    grid = arrangement_grid(arrangements)
    note = pill(f'{len(arrangements)} distinguishable arrangements', ACCENT, 37)
    self.show(VGroup(grid, note).arrange(DOWN, buff=0.38), run_time=.8 * pace)
    self.wait(max(1 / 60, g.left() * 0.16))
    swaps = []
    for tile in grid:
        for ball in tile[1]:
            star = labelled_ball('*', MINI_BALL_RADIUS, False).match_height(ball).move_to(ball)
            swaps.append(Transform(ball, star))
    self.play(*swaps, run_time=0.90 * pace)
    self.play(*(tile[2].animate.set_opacity(0) for tile in grid), run_time=0.55 * pace)

    stacks = {}
    for cells, tile in zip(arrangements.values(), grid, strict=True):
        tile.remove(tile[2])
        stacks.setdefault(tuple(map(len, cells)), []).append(tile)

    patterns = sorted(stacks, key=lambda pattern: (len(stacks[pattern]), pattern))
    targets, badges, slots = {}, VGroup(), VGroup()
    for pattern in patterns:
        front = stacks[pattern][-1].copy()
        badge = pill(f'×{len(stacks[pattern])}', ACCENT, 29).next_to(front, DOWN, buff=0.20)
        targets[pattern] = front
        badges.add(badge)
        slots.add(VGroup(front, badge))
    slots.arrange_in_grid(rows=2, cols=5, buff=(0.78, 0.40))
    slots.next_to(note, UP, buff=0.43).set_x(grid.get_x())

    moves = []
    for pattern in patterns:
        center = targets[pattern].get_center()
        for depth, tile in enumerate(stacks[pattern]):
            tile.set_z_index(depth)
            offset = (len(stacks[pattern]) - 1 - depth) * (RIGHT * 0.045 + UP * 0.052)
            moves.append(tile.animate.move_to(center + offset))
    self.play(*moves, run_time=2.25 * pace)
    self.play(FadeIn(badges), run_time=0.60 * pace)
    self.wait(max(1 / 60, g.left() * 0.18))

    counts = Counter(map(len, stacks.values()))
    products = '+'.join(rf'{counts[multiplicity]}\cdot{multiplicity}' for multiplicity in sorted(counts))
    check = formula_pill(f'${products}={len(arrangements)}$', 39).move_to(note)
    self.play(Transform(note, check), run_time=0.60 * pace)
    self.wait(max(1 / 60, g.left() * 0.35))

    fronts = VGroup()
    collapse = []
    for members in stacks.values():
        front = members[-1]
        fronts.add(front)
        collapse.extend(tile.animate.move_to(front).set_opacity(0) for tile in members[:-1])
    self.play(*collapse, run_time=1.00 * pace)
    replacement = pill(f'{len(arrangements)} → {len(stacks)} configurations', ACCENT, 37).move_to(note)
    self.play(Transform(note, replacement), run_time=0.55 * pace)
    self.remove(grid, *grid, badges, note)
    self.body = VGroup(fronts, badges, note)
    self.add(self.body)
