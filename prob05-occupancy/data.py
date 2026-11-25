"""Computed screen values for occupancy models and runs."""

import re
from collections import Counter
from fractions import Fraction
from itertools import product
from math import comb, factorial
from pathlib import Path

from check_numbers import (
    check_code_lab, check_configuration_table, check_counting, check_runs,
    check_three_statistics, compositions, multinomial, occupancies, run_lengths,
)

SOURCE = Path(__file__).with_name('SCRIPT.md').read_text(encoding='utf-8')
fence = chr(96) * 3
CODE, CODE_OUTPUT = re.search(
    rf'{fence}python\n(.*?)\n{fence}\n\nOutput:\n{fence}\n(.*?)\n{fence}', SOURCE, re.S
).groups()
KEY_IDEAS = tuple(
    re.findall(r'^- (.+)$', SOURCE.split('**Visual.** key_ideas', 1)[1].split('\n\n> ', 1)[0], re.M)
)
NEXT_TITLE = 'The hypergeometric distribution and waiting times'

SYMBOL = '|***|*|||****|'
CELLS = tuple(map(len, SYMBOL.split('|')[1:-1]))
BALLS, CELL_COUNT = sum(CELLS), len(CELLS)
INNER_BARS = CELL_COUNT - 1
MOVABLE = BALLS + INNER_BARS
STAR_ORDERS = comb(MOVABLE, BALLS)
GAPS = BALLS - 1
NONEMPTY = comb(GAPS, INNER_BARS)
LEFTOVER = BALLS - CELL_COUNT
BAR_GAPS = (1, 3, 5, 6)
NONEMPTY_VECTOR = tuple(
    right - left for left, right in zip((0, *BAR_GAPS), (*BAR_GAPS, BALLS), strict=True)
)
DIE_FACES = tuple(range(1, 7))
ROLL = (2, 2, 5)
DICE_VECTOR = occupancies(tuple(face - 1 for face in ROLL), len(DIE_FACES))
DICE_RECORDS = comb(len(ROLL) + len(DIE_FACES) - 1, len(DIE_FACES) - 1)
DIFFERENTIATIONS = 'xyxz'
VARIABLES = 'xyz'
DIFFERENTIATION_VECTOR = tuple(DIFFERENTIATIONS.count(letter) for letter in VARIABLES)
ORDERS = tuple(range(len(DIFFERENTIATIONS), len(DIFFERENTIATIONS) + 2))
DERIVATIVE_COUNTS = tuple(comb(order + len(VARIABLES) - 1, order) for order in ORDERS)

FIXED_VECTOR = (2, 1, 0)
FIXED_N = len(FIXED_VECTOR)
FIXED_TOTAL = FIXED_N ** sum(FIXED_VECTOR)
FIXED_COUNT = sum(
    occupancies(p, FIXED_N) == FIXED_VECTOR for p in product(range(FIXED_N), repeat=sum(FIXED_VECTOR))
)
FIXED_PROB = Fraction(FIXED_COUNT, FIXED_TOTAL)

TARGET, EXACT = check_configuration_table(SOURCE)
TARGET_N, TARGET_BALLS = len(TARGET), sum(TARGET)
TARGET_ROLES = dict(sorted(Counter(TARGET).items(), reverse=True))
CELL_CHOICES = multinomial(TARGET_ROLES.values())
BALL_CHOICES = multinomial(TARGET)
ALL_PLACEMENTS = TARGET_N ** TARGET_BALLS
FAVOURABLE = CELL_CHOICES * BALL_CHOICES
EXPECTED_ROWS = re.findall(r'^\| ((?:\d,){6}\d) \| (0\.\d{6}) \|$', SOURCE, re.M)
CONFIGURATIONS = tuple(tuple(map(int, vector.split(','))) for vector, _ in EXPECTED_ROWS)
ALL_CONFIGURATIONS = {tuple(sorted(v, reverse=True)) for v in compositions(TARGET_BALLS, TARGET_N)}
TABLE = tuple(
    (v, Fraction(multinomial(Counter(v).values()) * multinomial(v), ALL_PLACEMENTS))
    for v in CONFIGURATIONS
)
EVEN = (1,) * TARGET_N

MODEL_VECTOR = (1, 0, 1, 1, 0)
MODEL_N, MODEL_BALLS = len(MODEL_VECTOR), sum(MODEL_VECTOR)
MODEL_TOTALS = (
    MODEL_N**MODEL_BALLS,
    comb(MODEL_N + MODEL_BALLS - 1, MODEL_BALLS),
    comb(MODEL_N, MODEL_BALLS),
)
MODEL_PROBABILITIES = tuple(
    Fraction(matches, total)
    for matches, total in zip((factorial(MODEL_BALLS), 1, 1), MODEL_TOTALS, strict=True)
)

RUN_WORD = 'AAABAABBBA'
RUN_SIZES = run_lengths(RUN_WORD)
AB_WORD = 'BABBAAB'
A_RUNS = 2
A_COUNT, B_COUNT = AB_WORD.count('A'), AB_WORD.count('B')
A_SPLITS, B_SPLITS = comb(A_COUNT - 1, A_RUNS - 1), comb(B_COUNT - 1, A_RUNS)
RUN_COUNT = A_SPLITS * B_SPLITS

COUNTER = 'EOEEOEEEOEEEOEOE'
OCCUPIED, EMPTY = COUNTER.count('O'), COUNTER.count('E')
MAX_RUNS = 2 * OCCUPIED + 1
COUNTER_TOTAL = comb(len(COUNTER), OCCUPIED)
COUNTER_MATCHES = comb(OCCUPIED - 1, OCCUPIED - 1) * comb(EMPTY - 1, OCCUPIED)
COUNTER_PROB = Fraction(COUNTER_MATCHES, COUNTER_TOTAL)

check_counting()
check_three_statistics()
check_runs()
assert check_code_lab(SOURCE, TARGET, EXACT) == CODE_OUTPUT
assert len(KEY_IDEAS) == 3
assert (STAR_ORDERS, NONEMPTY, LEFTOVER) == (495, 35, 3)
assert sum(NONEMPTY_VECTOR) == BALLS and len(NONEMPTY_VECTOR) == CELL_COUNT and min(NONEMPTY_VECTOR) >= 1
assert (DICE_RECORDS, DERIVATIVE_COUNTS) == (56, (15, 21))
assert (FIXED_COUNT, FIXED_TOTAL, FIXED_PROB) == (3, 27, Fraction(1, 9))
assert (CELL_CHOICES, BALL_CHOICES, FAVOURABLE, ALL_PLACEMENTS) == (210, 1260, 264600, 823543)
assert EXACT == Fraction(FAVOURABLE, ALL_PLACEMENTS)
assert len(TABLE) == 15 and set(CONFIGURATIONS) == ALL_CONFIGURATIONS
assert [f'{float(value):.6f}' for _, value in TABLE] == [value for _, value in EXPECTED_ROWS]
assert sum(probability for _, probability in TABLE) == 1
assert TABLE[0] == (TARGET, EXACT) and f'{float(dict(TABLE)[EVEN]):.6f}' == '0.006120'
assert MODEL_PROBABILITIES == (Fraction(6, 125), Fraction(1, 35), Fraction(1, 10))
assert RUN_COUNT == 6 and (OCCUPIED, EMPTY, MAX_RUNS) == (5, 11, 11)
assert (COUNTER_MATCHES, COUNTER_TOTAL, COUNTER_PROB) == (252, 4368, Fraction(3, 52))
