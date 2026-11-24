"""Manim lesson on subpopulations, partitions and binomial coefficients."""

from importlib.util import module_from_spec, spec_from_file_location
from math import factorial
from pathlib import Path
import sys

from manim import (
    DOWN, LEFT, RIGHT, UP, Circle, Create, Dot, FadeIn, FadeOut, LaggedStart, Line,
    Rectangle, SurroundingRectangle, Transform, TransformFromCopy, VGroup,
)

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))

from brand import ACCENT, BORDER2, MUTED, NEXT, SKY, SURFACE, TEXT, TEXT2, WARN, card, mono, pill, sans
from lesson_kit import LessonScene, box, code_cell, derivation, end_card, key_ideas, svg_figure, title_card
from prob_visuals import formula_pill


def load_lesson_three():
    """Load the earlier scene's helpers with their own lesson data."""
    earlier = HERE.parent / 'prob03-counting' / 'scenes.py'
    spec = spec_from_file_location('lesson_three_visuals', earlier)
    module = module_from_spec(spec)
    paths = sys.path[:]
    names = ('data', 'check_numbers')
    saved = {name: sys.modules.pop(name) for name in names if name in sys.modules}
    try:
        sys.path.insert(0, str(earlier.parent))
        spec.loader.exec_module(module)
    finally:
        sys.path[:] = paths
        for name in names:
            sys.modules.pop(name, None)
        sys.modules.update(saved)
    return module


lesson_three = load_lesson_three()

from data import (
    ABSENT, ACE_ORDERS, ALL_STATES, BALLS, BRIDGE_DEALS, BRIDGE_HANDS, BRIDGE_PROB, CELLS, CELL_FAVOURABLE,
    CELL_OTHER_CHOICES, CELL_PAIRS, CELL_PROB, CELL_TARGET, CELL_TOTAL, CHESS_PATHS, CHESS_SIZE, CODE,
    CODE_OUTPUT, COLOUR_DISPLAYS, DECK, DICE, DICE_OUTCOMES, DICE_PER_FACE, DICE_PROB, DICE_SUCCESS,
    DIE_FACES, DIE_ORDER, DIFFERENT_BRIDGE_RANKS, FLAG_COLOURS, FLAG_SLOTS, GROUP_CHOICES, GROUPS,
    HAND_SIZE, HEIGHT, KEY_IDEAS, LEAVE, NON_ACES, NON_ACE_HAND_SIZE, ORDERED_TOTAL, ORDERINGS, OUTSIDE_STATE,
    PARTITIONS, PATH_COUNT, PATH_WORD, PER_STATE, PLAYERS, POKER_HAND, POKER_PROB, POKER_RANKS, POKER_TOTAL,
    POPULATION, RANK_CHOICES, RANKS, REPEATED_ORDERED, REPEATED_SETS, REPRESENTED, SAMPLE_POOL, SAMPLE_SIZE,
    SEATS, SENATORS, STATE_COLUMNS, STATE_ROWS, STATES, STAY, SUBSETS, SUITS, SUIT_CHOICES, TWO_KIND_COUNT,
    TWO_KINDS, UNREPEATED_ORDERED, UNREPEATED_SETS, WIDTH,
)

math, frac = lesson_three.math, lesson_three.frac
stack, row, panel, label = lesson_three.stack, lesson_three.row, lesson_three.panel, lesson_three.label
tile_row = lesson_three.tile_row


def example(number, subtitle):
    return box('example', f'Example 2.{number}', [subtitle])


def large_number(value):
    return f'{value:,}'.replace(',', r'\,')


def equation_badge(tex, size=39):
    return formula_pill('$' + tex + '$', size)


def card_face(rank, suit):
    suit_color = WARN if suit in 'HD' else NEXT
    return panel(stack(mono(rank, 44, TEXT, 'BOLD'), mono(suit, 25, suit_color), gap=.14), 1.08, 1.54)


def card_hand(cards):
    return row(*(card_face(rank, suit) for rank, suit in cards), gap=.15)


def letter_tray(title, items, color=ACCENT):
    return panel(stack(sans(title, 31, color, 'BOLD'), tile_row(items, [color] * len(items)), gap=.22),
                 2.45, 1.52)


def senate_grid(*, all_states=False):
    states = VGroup()
    for i in range(STATES):
        focus = i == 0 and not all_states
        color = WARN if focus else BORDER2
        dots = row(*(Dot(radius=.09, color=ACCENT if all_states and j == 0 else MUTED)
                     .set_opacity(.25 if focus else .96) for j in range(PER_STATE)), gap=.14)
        states.add(panel(dots, .78, .50, color))
    return states.arrange_in_grid(rows=STATE_ROWS, cols=STATE_COLUMNS, buff=(.11, .11))


def ball_bank():
    return row(*(VGroup(Circle(radius=.31, color=color, fill_opacity=.23),
                        mono(letter, 29, color, 'BOLD'))
                 for letter, color in zip(BALLS, (ACCENT, NEXT, SKY), strict=True)), gap=.19)


def cell_boxes():
    boxes = VGroup()
    for index, name in enumerate(CELLS):
        color = ACCENT if index == 0 else BORDER2
        face = card(2.30, 1.39).set_stroke(color, width=2.6)
        caption = mono(name, 31, color if index == 0 else MUTED).next_to(face, DOWN, buff=.14)
        boxes.add(VGroup(face, caption))
    return row(*boxes, gap=.20)


def path_word(*, selected=False):
    return tile_row(PATH_WORD, [NEXT if move == 'U' else MUTED if selected else ACCENT for move in PATH_WORD])


def path_grid():
    """Match the site figure's square grid, endpoints and step order."""
    spacing = .71

    def at(x, y):
        return [x * spacing, y * spacing, 0]

    base = VGroup(*(Line(at(x, 0), at(x, HEIGHT), color=BORDER2) for x in range(WIDTH + 1)),
                  *(Line(at(0, y), at(WIDTH, y), color=BORDER2) for y in range(HEIGHT + 1)))
    endpoints = VGroup(Dot(at(0, 0), radius=.065, color=TEXT), Dot(at(WIDTH, HEIGHT), radius=.065, color=TEXT))
    marks = VGroup(math('O', 30).next_to(endpoints[0], DOWN + LEFT, buff=.10),
                   math('P', 30).next_to(endpoints[1], UP + RIGHT, buff=.10))
    segments = VGroup()
    x = y = 0
    for move in PATH_WORD:
        next_x, next_y = x + (move == 'R'), y + (move == 'U')
        segments.add(Line(at(x, y), at(next_x, next_y), color=ACCENT if move == 'R' else NEXT,
                          stroke_width=5.5))
        x, y = next_x, next_y
    assert (x, y) == (WIDTH, HEIGHT)
    return VGroup(base, segments, endpoints, marks), segments


def chessboard():
    return VGroup(*(Rectangle(width=.34, height=.34, stroke_width=.78, stroke_color=BORDER2,
                              fill_color=NEXT if (r + c) % 2 else SURFACE, fill_opacity=.20)
                    for r in range(CHESS_SIZE) for c in range(CHESS_SIZE))).arrange_in_grid(
                        rows=CHESS_SIZE, cols=CHESS_SIZE, buff=0)


def bridge_stacks(*, aces=False):
    stacks = VGroup()
    for index, (player, suit) in enumerate(zip(PLAYERS, SUITS, strict=True)):
        size = NON_ACE_HAND_SIZE if aces else HAND_SIZE
        cards = VGroup(*(card(1.21, 1.48).shift(RIGHT * .039 * i + UP * .026 * i) for i in range(size)))
        rank, visible_suit = ('A', suit) if aces else POKER_HAND[index + 1]
        face = card_face(rank, visible_suit).move_to(cards[-1])
        if aces:
            face.shift(RIGHT * .46 + DOWN * .15)
        cards.add(face)
        name = sans(player, 29, ACCENT, 'BOLD')
        amount = mono(f'{size} non-aces' if aces else f'{size} cards', 24, TEXT2)
        stacks.add(panel(stack(name, cards, amount, gap=.18), 2.03, 2.53))
    return row(*stacks, gap=.21)


PIPS = {
    1: ((0, 0),),
    2: ((-1, 1), (1, -1)),
    3: ((-1, 1), (0, 0), (1, -1)),
    4: ((-1, 1), (1, 1), (-1, -1), (1, -1)),
    5: ((-1, 1), (1, 1), (0, 0), (-1, -1), (1, -1)),
    6: tuple((x, y) for x in (-1, 1) for y in (-1, 0, 1)),
}


def die(value, number):
    pips = VGroup(*(Dot([x * .18, y * .18, 0], radius=.043, color=TEXT) for x, y in PIPS[value]))
    face = panel(pips, .73, .66)
    identity = mono(f'{number:02d}', 20, MUTED)
    return stack(face, identity, gap=.08)


def summary_table():
    heads = [
        label('Order matters', 3.15, .66, 27, ACCENT),
        label('Order does not matter', 3.15, .66, 27, NEXT),
    ]
    titles = [
        label('Without replacement', 3.38, .66, 27),
        label('With replacement', 3.38, .66, 27),
    ]
    fills = [panel(math(tex, 43, color), 3.15, .92)
             for tex, color in zip((r'(n)_r', r'\binom nr', r'n^r', r'\binom{n+r-1}r'),
                                   (ACCENT, NEXT, ACCENT, NEXT), strict=True)]
    cells = VGroup(card(3.38, .66).set_opacity(0), *heads, titles[0], *fills[:2], titles[1], *fills[2:])
    cells.arrange_in_grid(rows=3, cols=3, buff=.11)
    return cells, fills


def combination_strip(words, color):
    return row(*(label(''.join(word), .65, .58, 25, color) for word in words), gap=.10)


def dots_and_dividers():
    places = [1.30 * (i - (len(SAMPLE_POOL) - 1) / 2) for i in range(len(SAMPLE_POOL))]
    marks = VGroup(*(Dot([x, 0, 0], radius=.115, color=ACCENT) for x in places[:SAMPLE_SIZE]))
    for left, right in zip(places, places[1:]):
        line = Line(DOWN * .22, UP * .22, color=NEXT).set_x((left + right) / 2)
        marks.add(line)
    groups = VGroup(*(mono(letter, 25, TEXT2).move_to([x, -.48, 0])
                      for x, letter in zip(places, SAMPLE_POOL, strict=True)))
    slots = SAMPLE_SIZE + len(SAMPLE_POOL) - 1
    formula = equation_badge(rf'\binom{{n+r-1}}{{r}}=\binom{{{slots}}}{{{SAMPLE_SIZE}}}={len(REPEATED_SETS)}', 37)
    explanation = equation_badge(r'r\text{ dots and }n-1\text{ dividers}', 33)
    return panel(stack(VGroup(marks, groups), explanation, formula, gap=.20))


class Video(LessonScene):
    folder = str(HERE)
    number = '2.2'
    section_title = 'Subpopulations and Partitions'
    lesson_k = 4

    def construct(self):
        self.welcome()
        self.subsets()
        self.complements()
        self.ranks_and_suits()
        self.senators()
        self.occupancy()
        self.two_kinds()
        self.paths()
        self.partitions()
        self.bridge()
        self.dice()
        self.summary()
        self.code_lab()
        self.finish_lesson()

    def beat(self, cue, share):
        self.wait(max(.08, cue.left() * share))

    def welcome(self):
        with self.seg('welcome') as cue:
            self.show(title_card(self.number, self.section_title, self.lesson_k))
            self.beat(cue, .23)
            hand = card_hand(POKER_HAND)
            caption = pill('Same cards, same hand', NEXT, 31)
            block = stack(hand, caption, gap=.43)
            self.show(block)
            self.play(hand[0].animate.move_to(hand[1]), hand[1].animate.move_to(hand[0]), run_time=.72)
            self.beat(cue, .29)
            replacement = card_face('Q', 'D').match_height(hand[-1]).move_to(hand[-1])
            self.play(Transform(hand[-1], replacement),
                      Transform(caption, pill('New member, new hand', ACCENT, 31).move_to(caption)),
                      run_time=.68)
        with self.seg('recap'):
            trays = lesson_three.tray_columns((('A', 'A', 'C'), ('A', 'B', 'C')))
            for tray, tex, color in zip(trays, (r'n^r', r'(n)_r'), (ACCENT, NEXT), strict=True):
                result = tray[1][1][-1]
                result.become(math(tex, 39, color).move_to(result))
            _, base, curve, focus, _ = lesson_three.birthday_plot()
            crossing = lesson_three.CROSSING
            labels = VGroup(mono(str(crossing - 1), 29, ACCENT).next_to(focus[0], UP + LEFT, buff=.12),
                            mono(str(crossing), 29, WARN).next_to(focus[1], DOWN + RIGHT, buff=.12))
            graph = stack(VGroup(base, curve, *focus[:2], labels),
                          sans(f'At {lesson_three.CROSSING}, a shared birthday is more likely', 34, TEXT2),
                          gap=.28)
            self.show(row(trays.scale(.80), graph.scale(.66), gap=.53))

    def subsets(self):
        with self.seg('collapse_orders') as cue:
            pool = stack(sans('Population', 35, TEXT, 'BOLD'), tile_row(POPULATION), gap=.18)
            ordered = VGroup(*(combination_strip((order,), NEXT) for order in ORDERINGS))
            ordered.arrange_in_grid(rows=2, cols=3, buff=(.25, .16))
            result = letter_tray('One subset', ORDERINGS[0], ACCENT)
            summary = equation_badge(rf'{ORDERED_TOTAL}\div {len(ORDERINGS)}={len(SUBSETS)}', 43)
            arrow = math(r'\longrightarrow', 36, MUTED)
            block = stack(pool, row(ordered, arrow, result, gap=.29), summary, gap=.42)
            self.place(block)
            self.play(FadeIn(pool), FadeIn(ordered), run_time=.72)
            self.beat(cue, .28)
            travelling = ordered.copy()
            self.add(travelling)
            target = VGroup(*(word.copy().move_to(result) for word in ordered))
            self.play(Transform(travelling, target), ordered.animate.set_opacity(.55),
                      FadeIn(arrow), run_time=.88)
            self.play(FadeOut(travelling), FadeIn(result), FadeIn(summary), run_time=.54)
            self.remove(pool, ordered, arrow, result, summary)
            self.add(self.body)
            self.beat(cue, .33)
            bundles = VGroup(*(label(''.join(subset), 1.11, .52, 26,
                                      ACCENT if index == 0 else NEXT if index == 1 else TEXT2)
                               for index, subset in enumerate(SUBSETS)))
            bundles.arrange_in_grid(rows=2, cols=len(SUBSETS) // 2, buff=.14)
            self.show(stack(sans('One bundle per subset', 40, TEXT, 'BOLD'), bundles, summary.copy()))
        with self.seg('choose_rule') as cue:
            theorem = box('theorem', 'Theorem 2.4', [r'Choose $r$ of $n$ objects without replacement, where $0\le r\le n$.'])
            choices = row(letter_tray('Choose the set', ORDERINGS[0]),
                          label('×', 0, .55, 30, TEXT2),
                          letter_tray('Order the set', ORDERINGS[-1], NEXT), gap=.36)
            self.show(stack(theorem, choices, equation_badge(r'(n)_r=\binom nr\,r!', 43)))
            self.beat(cue, .44)
            self.show(derivation([
                r'\binom nr=\dfrac{(n)_r}{r!}',
                r'\binom nr=\dfrac{n(n-1)\cdots(n-r+1)}{1\cdot2\cdots r}\qquad(2.6)',
            ]), step_time=.76)

    def complements(self):
        with self.seg('choose_complement') as cue:
            stay = letter_tray('Stay', STAY, ACCENT)
            leave = letter_tray('Leave', LEAVE, NEXT)
            choose_stay = equation_badge(rf'\binom{{{len(POPULATION)}}}{{{len(STAY)}}}={len(SUBSETS)}', 45)
            choose_leave = equation_badge(rf'\binom{{{len(POPULATION)}}}{{{len(LEAVE)}}}={len(SUBSETS)}', 45)
            display = row(stack(stay, choose_stay), stack(leave, choose_leave), gap=.62)
            marker = SurroundingRectangle(stay, color=ACCENT, buff=.08, corner_radius=.12)
            marker.set_opacity(0)
            block = VGroup(display, marker)
            self.show(block)
            self.play(marker.animate.set_opacity(1), run_time=.45)
            self.beat(cue, .38)
            second = SurroundingRectangle(leave, color=NEXT, buff=.08, corner_radius=.12)
            self.play(Transform(marker, second), run_time=.66)
        with self.seg('choose_factorial') as cue:
            steps = derivation([
                r'\binom nr=\binom n{n-r}',
                r'\binom nr=\dfrac{(n)_r}{r!}\cdot\dfrac{(n-r)!}{(n-r)!}'
                r'=\dfrac{n!}{r!(n-r)!}',
                r'\binom n0=1,\qquad 0!=1\qquad(2.7)',
            ])
            empty = panel(stack(sans('Empty subset', 28, TEXT2), card(2.5, .43),
                                math(rf'\binom{{{len(POPULATION)}}}0=\binom{{{len(POPULATION)}}}{{{len(POPULATION)}}}'
                                     rf'={factorial(0)}', 36, ACCENT), gap=.20))
            block = stack(steps, empty, gap=.40)
            self.place(block)
            steps.reveal(self, run_time=.75, step_time=.76)
            self.beat(cue, .31)
            self.play(FadeIn(empty), run_time=.55)
            self.remove(*steps.submobjects, empty)
            self.add(block)

    def ranks_and_suits(self):
        with self.seg('poker_hands') as cue:
            hand = card_hand(POKER_HAND)
            metadata = equation_badge(
                rf'\binom{{{len(DECK)}}}{{{POKER_RANKS}}}={large_number(POKER_TOTAL)}', 45)
            self.show(stack(example(9, 'Poker ranks and suits'), hand, metadata, gap=.42))
            self.beat(cue, .34)
            self.play(hand[0].animate.move_to(hand[2]), hand[2].animate.move_to(hand[0]), run_time=.72)
        with self.seg('poker_distinct') as cue:
            chosen = {rank for rank, _ in POKER_HAND}
            ranks = tile_row(RANKS, [ACCENT if rank in chosen else MUTED for rank in RANKS]).scale(.83)
            suit_options = row(*(panel(stack(sans(rank, 30, ACCENT, 'BOLD'),
                                               tile_row(SUITS).scale(.62), gap=.20), 1.72)
                                 for rank, _ in POKER_HAND), gap=.16)
            counts = equation_badge(
                rf'\binom{{{len(RANKS)}}}{{{POKER_RANKS}}}={large_number(RANK_CHOICES)},\quad'
                rf'{len(SUITS)}^{{{POKER_RANKS}}}={large_number(SUIT_CHOICES)}', 38)
            win = equation_badge(
                rf'\dfrac{{{large_number(RANK_CHOICES * SUIT_CHOICES)}}}{{{large_number(POKER_TOTAL)}}}'
                rf'\approx{float(POKER_PROB):.4f}', 43)
            self.show(stack(ranks, suit_options, counts))
            self.beat(cue, .52)
            self.show(stack(ranks.copy(), suit_options.copy(), counts.copy(), win))
        with self.seg('bridge_ranks'):
            ranks = stack(tile_row(RANKS[:7], [ACCENT] * len(RANKS[:7])),
                          tile_row(RANKS[7:], [ACCENT] * len(RANKS[7:])), gap=.16)
            self.show(stack(sans('One bridge hand', 41, TEXT, 'BOLD'), ranks, derivation([
                rf'\binom{{{len(DECK)}}}{{{HAND_SIZE}}}={large_number(BRIDGE_HANDS)}',
                rf'\dfrac{{{len(SUITS)}^{{{HAND_SIZE}}}}}{{\binom{{{len(DECK)}}}{{{HAND_SIZE}}}}}'
                rf'\approx{float(DIFFERENT_BRIDGE_RANKS):.7f}',
            ]), gap=.36))

    def senators(self):
        with self.seg('state_absent') as cue:
            heading = example(10, 'A committee of senators')
            grid = senate_grid()
            counts = row(pill(f'{OUTSIDE_STATE} outside the chosen state', WARN, 29),
                         pill(f'{SEATS} committee seats', NEXT, 29), gap=.28)
            self.show(stack(heading, grid, counts, gap=.26))
            self.beat(cue, .33)
            result = derivation([
                rf'q=\dfrac{{\binom{{{OUTSIDE_STATE}}}{{{SEATS}}}}}{{\binom{{{SENATORS}}}{{{SEATS}}}}}'
                rf'=\dfrac{{{SENATORS-SEATS}\cdot{SENATORS-SEATS-1}}}{{{SENATORS}\cdot{SENATORS-1}}}'
                rf'\approx{float(ABSENT):.5f}',
                rf'P(\text{{represented}})=1-q\approx{float(REPRESENTED):.3f}',
            ])
            self.show(stack(grid.copy(), counts.copy(), result, gap=.30))
        with self.seg('all_states'):
            grid = senate_grid(all_states=True)
            numerator, exponent = f'{float(ALL_STATES):.1e}'.split('e')
            result = equation_badge(
                rf'\dfrac{{{PER_STATE}^{{{STATES}}}}}{{\binom{{{SENATORS}}}{{{SEATS}}}}}'
                rf'\approx {numerator}\times10^{{{int(exponent)}}}', 42)
            self.show(stack(sans('One senator from each state', 41, TEXT, 'BOLD'), grid, result, gap=.44))

    def occupancy(self):
        with self.seg('cell_count') as cue:
            head = example(11, 'Exactly k balls in a given cell')
            bank = ball_bank()
            boxes = cell_boxes()
            counts = equation_badge(
                rf'\binom{{{len(BALLS)}}}{{{CELL_TARGET}}}\cdot'
                rf'{CELL_OTHER_CHOICES}^{{{len(BALLS)-CELL_TARGET}}}={CELL_FAVOURABLE},\quad'
                rf'{len(CELLS)}^{{{len(BALLS)}}}={CELL_TOTAL},\quad'
                rf'{frac(CELL_FAVOURABLE,CELL_TOTAL)}={frac(CELL_PROB)}', 42)
            pairs = combination_strip(CELL_PAIRS, ACCENT)
            frame = stack(head, bank, boxes, row(pairs, counts, gap=.43), gap=.25)
            self.place(frame)
            self.play(FadeIn(head), FadeIn(bank), FadeIn(boxes), run_time=.70)
            self.beat(cue, .25)
            targets = VGroup(*(ball.copy() for ball in bank))
            targets[0].move_to(boxes[0][0]).shift(LEFT*.42)
            targets[1].move_to(boxes[0][0]).shift(RIGHT*.42)
            targets[2].move_to(boxes[1][0])
            self.play(*(TransformFromCopy(source, target) for source, target in zip(bank, targets, strict=True)),
                      FadeIn(pairs), run_time=.68)
            self.play(targets[2].animate.move_to(boxes[-1][0]), FadeIn(counts), run_time=.69)
            self.remove(head, bank, boxes, *targets, targets, pairs, counts)
            frame.add(targets)
            self.add(frame)
        with self.seg('cell_formula') as cue:
            self.show(derivation([
                r'p_k=\binom rk\dfrac{(n-1)^{r-k}}{n^r}',
                r'p_k=\binom rk\left(\dfrac1n\right)^k\left(1-\dfrac1n\right)^{r-k}\qquad(2.8)',
            ]), step_time=min(2.6, cue.left()*.25))

    def two_kinds(self):
        with self.seg('two_kinds') as cue:
            p, q = TWO_KINDS
            symbols = [rf'\alpha_{{{i}}}' for i in range(1,p+1)] + [rf'\beta_{{{i}}}' for i in range(1,q+1)]
            colors = [ACCENT]*p + [NEXT]*q
            items = row(*(panel(math(symbol,43,color), 1.04, .85)
                          for symbol, color in zip(symbols,colors,strict=True)), gap=.14)
            result = equation_badge(rf'\dfrac{{{p+q}!}}{{{p}!{q}!}}={TWO_KIND_COUNT}', 45)
            self.show(stack(sans('Arrangements of two kinds', 43, TEXT, 'BOLD'), items, result, gap=.48))
            self.beat(cue, .18)
            self.play(items[0].animate.move_to(items[1]), items[1].animate.move_to(items[0]),
                      items[p].animate.move_to(items[-1]), items[-1].animate.move_to(items[p]), run_time=.69)
            self.play(*(Transform(item[1], math(r'\alpha' if i < p else r'\beta',43,colors[i])
                                  .match_height(item[1]).move_to(item[1])) for i,item in enumerate(items)),
                      run_time=.66)
            self.beat(cue, .40)
            self.show(derivation([
                r'\dfrac{(p+q)!}{p!q!}=\binom{p+q}{p}=\binom{p+q}{q}\qquad(2.9)',
            ]))
        with self.seg('same_colour_flags') as cue:
            flags = lesson_three.flag_display(((0,), (1,), (2,)), count=False)
            flags[2].set_opacity(0)
            flags[3].set_opacity(0)
            _, second, third = flags[1]
            second.set_color(ACCENT)
            third.set_color(NEXT)
            tags = VGroup(*(mono(letter, 27, TEXT).next_to(flag, RIGHT, buff=.11)
                            for flag,letter in zip(flags[1], ('A', 'B', 'C'), strict=True)))
            terms = r'\cdot'.join(map(str,FLAG_SLOTS))
            p, q = FLAG_COLOURS
            fraction = equation_badge(
                rf'\dfrac{{{terms}}}{{{p}!{q}!}}={COLOUR_DISPLAYS}', 42)
            general = equation_badge(r'\dfrac{n(n+1)\cdots(n+r-1)}{p!q!}', 39)
            block = stack(VGroup(flags, tags), row(general, fraction, gap=.41))
            self.show(block)
            self.beat(cue, .36)
            self.play(tags[0].animate.move_to(tags[1]), tags[1].animate.move_to(tags[0]), run_time=.62)
            self.play(*(tag.animate.set_opacity(0) for tag in tags), run_time=.44)

    def paths(self):
        with self.seg('lattice_word') as cue:
            head = example(12, 'Shortest paths on a grid')
            reference = svg_figure('lattice-path.svg').scale_to_fit_width(6.8)
            self.show(stack(head, reference))
            self.beat(cue, .22)
            grid, segments = path_grid()
            grid.scale(1.20)
            base, _, ends, marks = grid
            letters = path_word()
            block = stack(head.copy(), grid, letters, gap=.34)
            self.place(block)
            self.play(FadeIn(block[0]), FadeIn(base), FadeIn(ends), FadeIn(marks), run_time=.66)
            step = segments[0]
            backwards = Line(step.get_end(), step.get_start(), color=WARN, stroke_width=5)
            note = pill('A step back must be made up', WARN, 25).next_to(grid, RIGHT, buff=.25)
            self.play(Create(backwards), FadeIn(note), run_time=.53)
            self.play(FadeOut(backwards), FadeOut(note), run_time=.34)
            for active, letter in zip(segments, letters, strict=True):
                self.play(Create(active), FadeIn(letter), run_time=.33)
            self.remove(block[0], base, ends, marks, *segments, *letters)
            self.add(block)
        with self.seg('path_count') as cue:
            grid, _ = path_grid()
            letters = path_word(selected=True)
            count = equation_badge(
                rf'\binom{{{len(PATH_WORD)}}}{{{HEIGHT}}}={PATH_COUNT},\qquad '
                rf'P(\text{{one specified path}})={frac(1,PATH_COUNT)}', 40)
            self.show(stack(grid, letters, count))
            self.beat(cue, .48)
            chess = chessboard()
            result = equation_badge(
                rf'\binom{{{2*CHESS_SIZE}}}{{{CHESS_SIZE}}}={large_number(CHESS_PATHS)}', 43)
            self.show(stack(sans(f'{CHESS_SIZE} × {CHESS_SIZE} chessboard', 39, TEXT, 'BOLD'),
                            chess, result))

    def partitions(self):
        with self.seg('partition_formula') as cue:
            head = box('theorem', 'Theorem 2.5', ['Partitions into labelled groups'])
            trays = VGroup()
            offset = 0
            for i, size in enumerate(GROUPS):
                trays.add(letter_tray(f'Team {POPULATION[i]}', POPULATION[offset:offset+size],
                                      (ACCENT,NEXT,SKY)[i]))
                offset += size
            trays.arrange(RIGHT, buff=.30)
            factors = ''.join(rf'\binom{{{len(POPULATION)-sum(GROUPS[:i])}}}{{{size}}}'
                              for i,size in enumerate(GROUPS))
            product = r'\cdot'.join(map(str,GROUP_CHOICES))
            self.show(stack(head, trays, equation_badge(rf'{factors}={product}={PARTITIONS}', 39), gap=.43))
            left, right = trays[0][1][1], trays[1][1][1]
            left.set_z_index(2)
            right.set_z_index(2)
            self.beat(cue, .40)
            self.play(left.animate.move_to(right), right.animate.move_to(left), run_time=.77)
            self.beat(cue, .20)
            self.play(left[0].animate.move_to(left[1]), left[1].animate.move_to(left[0]), run_time=.58)
        with self.seg('partition_cancel') as cue:
            formulas = derivation([
                r'\binom n{r_1}\binom{n-r_1}{r_2}\cdots',
                r'\dfrac{n!}{r_1!(n-r_1)!}\cdot\dfrac{(n-r_1)!}{r_2!(n-r_1-r_2)!}\cdots',
                r'\dfrac{n!}{r_1!r_2!\cdots r_k!},\quad r_1+\cdots+r_k=n,\quad r_i\ge0\qquad(2.10)',
            ])
            zero = panel(row(sans('Empty team', 29, TEXT2), card(1.15,.48),
                             math(rf'0!={factorial(0)}', 39, ACCENT), gap=.32))
            block = stack(formulas, zero, gap=.40)
            self.place(block)
            formulas.reveal(self, run_time=.76, step_time=1)
            self.beat(cue, .40)
            self.play(FadeIn(zero), run_time=.62)
            self.remove(*formulas.submobjects, zero)
            self.add(block)

    def bridge(self):
        with self.seg('bridge_deals') as cue:
            heading = example(13, 'Each bridge player gets an ace')
            hands = bridge_stacks()
            scientific, exponent = f'{BRIDGE_DEALS:.2e}'.split('e')
            count = math(large_number(BRIDGE_DEALS), 52, ACCENT)
            count.scale_to_fit_width(min(count.width, 10.2))
            full_width = panel(stack(math(rf'D=\dfrac{{{len(DECK)}!}}{{({HAND_SIZE}!)^{{{len(PLAYERS)}}}}}', 42),
                                     count,
                                     math(rf'D\approx {scientific}\times10^{{{int(exponent)}}}', 35, TEXT2),
                                     gap=.28), width=11.30)
            block = stack(heading, hands, full_width, gap=.30)
            self.place(block)
            self.play(FadeIn(heading), FadeIn(hands), run_time=.73)
            self.beat(cue, .37)
            layers = [layer for hand in hands for layer in hand[1][1][:-1]]
            self.play(*(layer.animate.set_opacity(.42) for layer in layers), FadeIn(full_width), run_time=.75)
            self.remove(heading, hands, full_width)
            self.add(block)
        with self.seg('bridge_aces') as cue:
            cards = card_hand([('A', suit) for suit in SUITS])
            hands = bridge_stacks(aces=True)
            aces = equation_badge(rf'{len(SUITS)}!={ACE_ORDERS}', 39)
            remaining = equation_badge(
                rf'\dfrac{{{NON_ACES}!}}{{({NON_ACE_HAND_SIZE}!)^{{{len(PLAYERS)}}}}}', 39)
            start = stack(cards, aces)
            self.show(start)
            self.beat(cue, .30)
            trace = card_hand([('A', suit) for suit in SUITS]).scale(.73)
            proof = row(aces.copy(), remaining, gap=.50)
            block = stack(trace, hands, proof, gap=.30)
            targets = [hand[1][1][-1] for hand in hands]
            self.place(block)
            for ace in targets:
                ace.save_state().set_opacity(0)
            self.play(FadeIn(trace), FadeIn(hands), run_time=.65)
            for source, target in zip(trace, targets, strict=True):
                moving = target.saved_state.copy()
                self.play(TransformFromCopy(source, moving), source.animate.set_opacity(.30), run_time=.33)
                self.remove(moving)
                target.restore()
            self.play(FadeIn(proof), run_time=.59)
            self.remove(trace, hands, proof)
            self.add(block)
            self.beat(cue, .37)
            self.show(derivation([
                rf'\dfrac{{{ACE_ORDERS}\,[{NON_ACES}!/({NON_ACE_HAND_SIZE}!)^{{{len(PLAYERS)}}}]}}'
                rf'{{{len(DECK)}!/({HAND_SIZE}!)^{{{len(PLAYERS)}}}}}',
                rf'\dfrac{{{ACE_ORDERS}\cdot{NON_ACES}!\cdot{HAND_SIZE}^{{{len(PLAYERS)}}}}}{{{len(DECK)}!}}'
                rf'\approx{float(BRIDGE_PROB):.3f}',
            ]), step_time=.68)

    def dice(self):
        with self.seg('dice_pairs') as cue:
            heading = example(14, 'Each face exactly twice')
            numbers = tuple(enumerate(DIE_ORDER, 1))
            tile_for = {idx: die(face,idx) for idx, face in numbers}
            rolled = row(*tile_for.values(), gap=.12)
            pairs = VGroup()
            destinations = {}
            for face in DIE_FACES:
                group = [(idx, die(value, idx)) for idx, value in numbers if value == face]
                destinations.update(group)
                twins = row(*(target for _, target in group), gap=.13)
                pairs.add(panel(stack(mono(f'Face {face}', 24, NEXT), twins, gap=.14)))
            pairs.arrange(RIGHT, buff=.15)
            result = equation_badge(
                rf'\dfrac{{{DICE}!}}{{({DICE_PER_FACE}!)^{{{len(DIE_FACES)}}}}}={large_number(DICE_SUCCESS)}', 43)
            block = stack(heading, rolled, pairs, result, gap=.37)
            self.place(block)
            self.play(FadeIn(heading), FadeIn(rolled), run_time=.74)
            self.beat(cue, .19)
            for target in destinations.values():
                target.save_state().set_opacity(0)
            self.play(FadeIn(pairs), run_time=.52)
            copies = {idx: target.saved_state.copy() for idx, target in destinations.items()}
            self.play(LaggedStart(*(TransformFromCopy(tile_for[idx], copy) for idx, copy in copies.items()),
                                  lag_ratio=.10), run_time=1.43)
            self.remove(*copies.values())
            for target in destinations.values():
                target.restore()
            first, second = pairs[0][1][1]
            self.play(first.animate.move_to(second), second.animate.move_to(first), run_time=.57)
            self.play(FadeOut(rolled), FadeIn(result), run_time=.61)
            rolled.set_opacity(0)
            self.remove(heading, *pairs, pairs, result)
            self.add(block)
        with self.seg('dice_chance') as cue:
            self.show(derivation([
                rf'{len(DIE_FACES)}^{{{DICE}}}={large_number(DICE_OUTCOMES)}',
                rf'\dfrac{{{DICE}!}}{{({DICE_PER_FACE}!)^{{{len(DIE_FACES)}}}\cdot'
                rf'{len(DIE_FACES)}^{{{DICE}}}}}=\dfrac{{{DICE}!}}{{{DICE_PER_FACE}^{{{len(DIE_FACES)}}}\cdot'
                rf'{len(DIE_FACES)}^{{{DICE}}}}}\approx{float(DICE_PROB):.6f}',
            ]), step_time=min(2.7, cue.left()*.25))

    def summary(self):
        with self.seg('summary_without') as cue:
            title = box('remark', 'Summary', ['Choosing elements from a population'])
            heading = sans('Summary', 44, MUTED, 'BOLD')
            title.heading.become(heading.move_to(title.heading).align_to(title.heading, LEFT))
            table, cells = summary_table()
            ordered = combination_strip(UNREPEATED_ORDERED, ACCENT)
            subsets = combination_strip(UNREPEATED_SETS, NEXT)
            arrow = math(r'\longrightarrow', 37, MUTED)
            strips = row(ordered, arrow, subsets, gap=.23)
            block = stack(title, table, strips, gap=.31)
            self.place(block)
            for item in (*cells, table[6], arrow, subsets):
                item.save_state().set_opacity(0)
            self.play(FadeIn(title), FadeIn(table), FadeIn(ordered), run_time=.68)
            self.beat(cue, .21)
            self.play(cells[0].animate.restore(), run_time=.56)
            self.beat(cue, .19)
            self.play(cells[1].animate.restore(), arrow.animate.restore(), subsets.animate.restore(), run_time=.65)
            self.remove(title, table, ordered, arrow, subsets)
            self.add(block)
        with self.seg('summary_with') as cue:
            ordered = combination_strip(REPEATED_ORDERED, ACCENT)
            unordered = combination_strip(REPEATED_SETS, NEXT)
            self.play(table[6].animate.restore(), cells[2].animate.restore(), run_time=.57)
            self.beat(cue, .15)
            self.play(cells[3].animate.restore(), run_time=.57)
            self.show(stack(title.copy(), table.copy(), row(ordered, math(r'\to',33), unordered, gap=.18), gap=.29))
            self.beat(cue, .30)
            diagram = dots_and_dividers()
            self.show(stack(title.copy(), table.copy(), diagram, gap=.28))

    def code_lab(self):
        with self.seg('code') as cue:
            self.show(code_cell(CODE, CODE_OUTPUT), step_time=min(1.44, cue.left()/12))
        with self.seg('code_result'):
            simulated, exact = CODE_OUTPUT.split()
            bars = row(panel(stack(sans('Simulated',35,TEXT2), math(simulated,55,ACCENT)), 4.2, 2.15),
                       panel(stack(sans('Exact (rounded)',35,TEXT2), math(exact,55,NEXT)), 4.2, 2.15))
            blocks = VGroup()
            for player in PLAYERS:
                slots = VGroup(*(card(.30, .32) for _ in range(HAND_SIZE)))
                slots.arrange_in_grid(cols=(HAND_SIZE + 1) // 2, buff=.05)
                slots[0].set_stroke(ACCENT, width=2)
                ace = mono('A', 18, ACCENT, 'BOLD').move_to(slots[0])
                blocks.add(panel(stack(sans(player, 28, TEXT2, 'BOLD'), VGroup(slots, ace),
                                        mono(f'{HAND_SIZE} slots', 24, MUTED), gap=.17)))
            blocks.arrange(RIGHT, buff=.22)
            self.show(stack(sans('One ace in each player’s block', 41, TEXT, 'BOLD'), blocks, bars))

    def finish_lesson(self):
        with self.seg('recall'):
            ideas = key_ideas(KEY_IDEAS, pause=5)
            self.place(ideas)
            ideas.start_recall(self)
        ideas.countdown(self)
        with self.seg('ideas') as cue:
            ideas.reveal_items(self, step_time=max(.25, cue.left()*.21))
            self.remove(*ideas.submobjects)
            self.add(ideas)
        with self.seg('end'):
            self.show(end_card('Occupancy problems and the three statistics'))
