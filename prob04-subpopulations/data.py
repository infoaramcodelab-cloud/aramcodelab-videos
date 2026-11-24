"""Computed counts and screen values for Subpopulations and Partitions."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial, perm, prod
from pathlib import Path
import re

from check_numbers import (
    check_arrangements_and_paths, check_cards, check_partitions, check_senators_and_cells,
    check_subsets, check_summary_and_code, multinomial,
)

KEY_IDEAS = (
    r'For an unordered subset, divide the ordered count by $r!$, giving $\binom nr=(n)_r/r!$.',
    'Choosing who stays and choosing who is left out give the same count.',
    r'For labelled groups with sizes summing to $n$, divide $n!$ by the product of their size factorials.',
)
source = Path(__file__).with_name('SCRIPT.md').read_text(encoding='utf-8')
fence = chr(96) * 3
CODE, CODE_OUTPUT = re.search(
    rf'{fence}python\n(.*?)\n{fence}\n\nOutput:\n{fence}\n(.*?)\n{fence}', source, re.S
).groups()

POPULATION = tuple('ABCDE')
ORDERINGS = tuple(permutations(POPULATION[:3]))
SUBSETS = tuple(combinations(POPULATION, len(ORDERINGS[0])))
ORDERED_TOTAL = len(ORDERINGS) * len(SUBSETS)
STAY, LEAVE = POPULATION[:2], POPULATION[2:]
RANKS = ('A', *map(str, range(2, 11)), 'J', 'Q', 'K')
SUITS = tuple('CSHD')
DECK = tuple(product(RANKS, SUITS))
POKER_HAND = (('A', 'S'), ('3', 'D'), ('7', 'C'), ('J', 'H'), ('K', 'S'))
POKER_RANKS = len(POKER_HAND)
POKER_TOTAL = comb(len(DECK), POKER_RANKS)
RANK_CHOICES = comb(len(RANKS), POKER_RANKS)
SUIT_CHOICES = len(SUITS)**POKER_RANKS
POKER_PROB = Fraction(RANK_CHOICES * SUIT_CHOICES, POKER_TOTAL)
PLAYERS = tuple('NESW')
HAND_SIZE = len(DECK) // len(PLAYERS)
BRIDGE_HANDS = comb(len(DECK), HAND_SIZE)
DIFFERENT_BRIDGE_RANKS = Fraction(len(SUITS)**HAND_SIZE, BRIDGE_HANDS)
BRIDGE_DEALS = multinomial(*([HAND_SIZE] * len(PLAYERS)))
ACE_ORDERS = factorial(len(SUITS))
NON_ACES = len(DECK) - len(SUITS)
NON_ACE_HAND_SIZE = NON_ACES // len(PLAYERS)
NON_ACE_DEALS = multinomial(*([NON_ACE_HAND_SIZE] * len(PLAYERS)))
BRIDGE_PROB = Fraction(ACE_ORDERS * NON_ACE_DEALS, BRIDGE_DEALS)

STATE_ROWS, STATE_COLUMNS, PER_STATE = 5, 10, 2
STATES = STATE_ROWS * STATE_COLUMNS
SENATORS = STATES * PER_STATE
SEATS = STATES
OUTSIDE_STATE = SENATORS - PER_STATE
ABSENT = Fraction(comb(OUTSIDE_STATE, SEATS), comb(SENATORS, SEATS))
REPRESENTED = 1 - ABSENT
ALL_STATES = Fraction(PER_STATE**STATES, comb(SENATORS, SEATS))

BALLS, CELLS, CELL_TARGET = tuple('ABC'), tuple('XYZ'), 2
CELL_PAIRS = tuple(combinations(BALLS, CELL_TARGET))
CELL_OTHER_CHOICES = len(CELLS) - 1
CELL_TOTAL = len(CELLS)**len(BALLS)
CELL_FAVOURABLE = len(CELL_PAIRS) * CELL_OTHER_CHOICES**(len(BALLS) - CELL_TARGET)
CELL_PROB = Fraction(CELL_FAVOURABLE, CELL_TOTAL)
TWO_KINDS = (2, 3)
TWO_KIND_COUNT = multinomial(*TWO_KINDS)
FLAG_COLOURS = (2, 1)
POLE_COUNT = 3
FLAG_SLOTS = tuple(range(POLE_COUNT, POLE_COUNT + sum(FLAG_COLOURS)))
COLOUR_DISPLAYS = prod(FLAG_SLOTS) // prod(map(factorial, FLAG_COLOURS))

PATH_WORD = 'RURRURRU'
WIDTH, HEIGHT = PATH_WORD.count('R'), PATH_WORD.count('U')
PATHS = tuple(word for word in product('RU', repeat=len(PATH_WORD)) if word.count('U') == HEIGHT)
PATH_COUNT = comb(WIDTH + HEIGHT, HEIGHT)
CHESS_SIZE = 8
CHESS_PATHS = comb(2 * CHESS_SIZE, CHESS_SIZE)
GROUPS = (2, 2, 1)
GROUP_CHOICES = tuple(comb(len(POPULATION) - sum(GROUPS[:i]), size) for i, size in enumerate(GROUPS))
PARTITIONS = multinomial(*GROUPS)

DIE_FACES = tuple(range(1, 7))
DIE_ORDER = (6, 2, 5, 3, 1, 4, 3, 2, 6, 4, 1, 5)
DICE_PER_FACE = 2
DICE = len(DIE_ORDER)
DICE_OUTCOMES = len(DIE_FACES)**DICE
DICE_SUCCESS = multinomial(*([DICE_PER_FACE] * len(DIE_FACES)))
DICE_PROB = Fraction(DICE_SUCCESS, DICE_OUTCOMES)

SAMPLE_POOL = POPULATION[:3]
SAMPLE_SIZE = 2
UNREPEATED_ORDERED = tuple(permutations(SAMPLE_POOL, SAMPLE_SIZE))
UNREPEATED_SETS = tuple(combinations(SAMPLE_POOL, SAMPLE_SIZE))
REPEATED_ORDERED = tuple(product(SAMPLE_POOL, repeat=SAMPLE_SIZE))
REPEATED_SETS = tuple(combinations_with_replacement(SAMPLE_POOL, SAMPLE_SIZE))

assert len(ORDERINGS) == factorial(3) and ORDERED_TOTAL == perm(len(POPULATION), 3) == 60
assert len(SUBSETS) == comb(len(POPULATION), len(STAY)) == 10
assert (POKER_TOTAL, RANK_CHOICES, SUIT_CHOICES) == (2_598_960, 1287, 1024)
assert (POKER_PROB, ABSENT, CELL_PROB) == (Fraction(2112, 4165), Fraction(49, 198), Fraction(2, 9))
assert len(PATHS) == PATH_COUNT == 56 and tuple(PATH_WORD) in PATHS
assert TWO_KIND_COUNT == 10 and COLOUR_DISPLAYS == PARTITIONS == prod(GROUP_CHOICES) == 30
assert Counter(DIE_ORDER) == {face: DICE_PER_FACE for face in DIE_FACES}
assert DICE_PROB == Fraction(1925, 559872)
assert tuple(map(len, (UNREPEATED_ORDERED, UNREPEATED_SETS, REPEATED_ORDERED, REPEATED_SETS))) == (6, 3, 9, 6)

check_subsets()
check_cards()
check_senators_and_cells()
check_arrangements_and_paths()
assert BRIDGE_PROB == check_partitions()
check_summary_and_code(BRIDGE_PROB)
