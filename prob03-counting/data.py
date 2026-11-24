"""Compute the worked counts and the data drawn in Lesson 3."""

from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from math import comb, exp, factorial, perm, prod
from pathlib import Path
from runpy import run_path

from check_numbers import (
    check_birthdays, check_code_lab, check_multiplication, check_occupancy, check_samples,
)

check_multiplication()
E_DIGITS, E_GROUPS, DISTINCT_E_GROUPS = check_samples()
check_occupancy()
EXACT_MATCH = check_birthdays()
CODE_OUTPUT = check_code_lab(EXACT_MATCH)

APPROVED_SCRIPT = Path(__file__).with_name('SCRIPT.md').read_text(encoding='utf-8')
FENCE = chr(96) * 3
CODE = APPROVED_SCRIPT.split(FENCE + 'python\n', 1)[1].split(FENCE, 1)[0].rstrip()
KEY_IDEAS = (
    'Multiply the number of available choices at each step when that number is fixed for every preceding choice.',
    r'An ordered sample of size $r$ from $n$ objects has $n^r$ possibilities with replacement and $(n)_r$ without replacement (Theorem 2.3).',
    r'Without replacement, selecting all $n$ objects gives $n!$ permutations. In a uniform ordered sample, every admissible sequence has the same probability.',
)

ARRANGEMENTS = run_path(str(Path(__file__).resolve().parents[1] / 'prob01-sample-space' / 'data.py'))['ARRANGEMENTS']
DIE_FACES = tuple(range(1, 7))
DICE = tuple(product(DIE_FACES, repeat=2))
SUM_COUNTS = dict(sorted(Counter(map(sum, DICE)).items()))
SEVEN_COUNT = SUM_COUNTS[7]
SHIRTS = ('Teal', 'Indigo')
HATS = ('Sand', 'Grey', 'White')
OUTFITS = tuple(product(SHIRTS, HATS))
MENUS = (('Soup', ('Fish', 'Pasta')), ('Salad', ('Pasta', 'Rice')), ('Bread', ('Rice', 'Fish')))
DESSERTS = ('Fruit', 'Cake', 'Pie', 'Tart')
BRANCH_COUNTS = (len(MENUS), len(MENUS[0][1]), len(DESSERTS))
MEALS = prod(BRANCH_COUNTS)
SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
RANKS = ('A', *map(str, range(2, 11)), 'J', 'Q', 'K')
DECK = tuple(product(SUITS, RANKS))
BULB_COUNT = 3
SWITCH_LEVELS = tuple(range(BULB_COUNT + 1))
LAMP_SETTINGS = tuple(product(SWITCH_LEVELS, repeat=2))
LAMP_LIT = sum(any(setting) for setting in LAMP_SETTINGS)
ACE = DIE_FACES[0]
NO_ACE_CHOICES = len(DIE_FACES) - 1
AT_LEAST_ONE_ACE = 1 - Fraction(NO_ACE_CHOICES, len(DIE_FACES))**len(DIE_FACES)
POLES = FLAGS = 3
FLAG_SLOTS = tuple(POLES + placed for placed in range(FLAGS))
FLAG_DISPLAYS = prod(FLAG_SLOTS)

POPULATION = tuple('ABCDE')
SAMPLE_LENGTH = 3
POP_SIZE = len(POPULATION)
WITH_COUNT = POP_SIZE**SAMPLE_LENGTH
WITHOUT_COUNT = perm(POP_SIZE, SAMPLE_LENGTH)
PERMUTATIONS = tuple(permutations(POPULATION[:SAMPLE_LENGTH]))
EMPTY_SAMPLE_COUNT = perm(POP_SIZE, 0)
OVERSIZE_SAMPLE_COUNT = perm(POP_SIZE, POP_SIZE + 1)
WITHOUT_MISSES = perm(POP_SIZE - 1, SAMPLE_LENGTH)
WITH_MISSES = (POP_SIZE - 1)**SAMPLE_LENGTH
INCLUSION_WITHOUT = 1 - Fraction(WITHOUT_MISSES, WITHOUT_COUNT)
INCLUSION_WITH = 1 - Fraction(WITH_MISSES, WITH_COUNT)
ALPHABET, WORD_LENGTH, PER_LETTER = 26, 10, 1000
PIECE_COUNT = ALPHABET * PER_LETTER
DIGITS = tuple(range(10))
DIGIT_DRAWS = 5
DISTINCT_DIGITS = Fraction(perm(len(DIGITS), DIGIT_DRAWS), len(DIGITS)**DIGIT_DRAWS)
E_FREQUENCY = Fraction(DISTINCT_E_GROUPS, E_GROUPS)
WEEK_DAYS = ('Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun')
ACCIDENTS = Fraction(factorial(len(WEEK_DAYS)), len(WEEK_DAYS)**len(WEEK_DAYS))
ALL_FACES = Fraction(factorial(len(DIE_FACES)), len(DIE_FACES)**len(DIE_FACES))
FLOORS, PASSENGERS = 10, 7
FLOOR_CHOICES = tuple(range(FLOORS, FLOORS - PASSENGERS, -1))
DIFFERENT_FLOORS = Fraction(prod(FLOOR_CHOICES), FLOORS**PASSENGERS)
DAYS = 365
BIRTHDAYS = {r: Fraction(perm(DAYS, r), DAYS**r) for r in range(1, 61)}
HALF = Fraction(1, 2)
CROSSING = next(r for r, p in BIRTHDAYS.items() if p < HALF)
LARGE_GROUP = 30
LOG_NUMERATOR = LARGE_GROUP * (LARGE_GROUP - 1)
LOG_DENOMINATOR = 2 * DAYS
LOG_ESTIMATE = exp(-LOG_NUMERATOR / LOG_DENOMINATOR)
BIRTHDAY_PAIRS = tuple(combinations(range(CROSSING), 2))

assert (len(OUTFITS), MEALS, len(DECK), LAMP_LIT, len(ARRANGEMENTS)) == (6, 24, 52, 15, 27)
assert FLAG_SLOTS == (3, 4, 5) and FLAG_DISPLAYS == 60
assert (WITH_COUNT, WITHOUT_COUNT, len(PERMUTATIONS)) == (125, 60, 6)
assert (EMPTY_SAMPLE_COUNT, OVERSIZE_SAMPLE_COUNT) == (1, 0)
assert (INCLUSION_WITHOUT, INCLUSION_WITH) == (Fraction(3, 5), Fraction(61, 125))
assert (E_FREQUENCY, DIFFERENT_FLOORS) == (Fraction('0.300'), Fraction('0.06048'))
assert 1 - BIRTHDAYS[CROSSING] == EXACT_MATCH
assert len(BIRTHDAY_PAIRS) == comb(CROSSING, 2) == 253
