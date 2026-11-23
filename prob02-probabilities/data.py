"""Computed values for the lesson's charts, examples, and Code Lab."""

from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction as F
from io import StringIO
from itertools import accumulate, combinations_with_replacement, product
from pathlib import Path
from random import Random
from runpy import run_path

REFERENCE = run_path(str(Path(__file__).resolve().parents[1] / 'prob01-sample-space' / 'data.py'))
ARRANGEMENTS = REFERENCE['ARRANGEMENTS']
COIN_TOSSES = REFERENCE['COIN_TOSSES']
TOURNAMENT_FINITE = REFERENCE['TOURNAMENT_FINITE']
TOURNAMENT_ENDLESS = REFERENCE['TOURNAMENT_ENDLESS']

EVENTS = {
    'crowded': lambda cells: max(cells) >= 2,
    'occupied': lambda cells: min(cells) >= 1,
    'first': lambda cells: cells[0] >= 1,
    'together': lambda cells: max(cells) == 3,
}
OCCUPANCIES = {index: tuple(map(len, cells)) for index, cells in ARRANGEMENTS.items()}
MULTIPLICITY = Counter(OCCUPANCIES.values())
CONFIGURATIONS = {
    tuple(config.count(cell) for cell in range(3))
    for config in combinations_with_replacement(range(3), 3)
}
assert CONFIGURATIONS == set(MULTIPLICITY)
assert (len(OCCUPANCIES), len(CONFIGURATIONS)) == (27, 10)
MB_LABELS = {
    event: tuple(index for index, cells in OCCUPANCIES.items() if predicate(cells))
    for event, predicate in EVENTS.items()
}
MB = {key: F(len(labels), len(OCCUPANCIES)) for key, labels in MB_LABELS.items()}
BE = {key: F(sum(predicate(cells) for cells in CONFIGURATIONS), len(CONFIGURATIONS))
      for key, predicate in EVENTS.items()}
assert tuple(map(len, MB_LABELS.values())) == (21, 6, 19, 3)
assert MB == {'crowded': F(7, 9), 'occupied': F(2, 9), 'first': F(19, 27), 'together': F(1, 9)}
assert BE == {'crowded': F(9, 10), 'occupied': F(1, 10), 'first': F(6, 10), 'together': F(3, 10)}

WEIGHT_COUNTS = dict(sorted(Counter(MULTIPLICITY.values()).items()))
WEIGHTS = {weight: F(weight, len(OCCUPANCIES)) for weight in WEIGHT_COUNTS}
assert WEIGHT_COUNTS == {1: 3, 3: 6, 6: 1}
assert WEIGHTS == {1: F(1, 27), 3: F(1, 9), 6: F(2, 9)}
assert sum(WEIGHT_COUNTS[weight] * p for weight, p in WEIGHTS.items()) == 1

THROWS = 10_000
GROUP_SIZE = 100
FREQUENCY_STEPS = (10, 100, 1000, THROWS)
FREQUENCY_BAND = (45, 55)
rng = Random(14)
TOSSES = tuple(int(rng.random() < 0.5) for _ in range(THROWS))
RUNNING_HEADS = tuple(accumulate(TOSSES))
PREFIX = {n: RUNNING_HEADS[n - 1] for n in FREQUENCY_STEPS}
GROUP_HEADS = tuple(sum(TOSSES[i:i+GROUP_SIZE]) for i in range(0, THROWS, GROUP_SIZE))
GROUP_HISTOGRAM = Counter(GROUP_HEADS)
IN_BAND = sum(FREQUENCY_BAND[0] <= heads <= FREQUENCY_BAND[1] for heads in GROUP_HEADS)
assert PREFIX == {10: 4, 100: 57, 1000: 525, THROWS: 4989}
assert (len(GROUP_HEADS), min(GROUP_HEADS), max(GROUP_HEADS), IN_BAND) == (100, 37, 63, 72)

COINS_TWO = tuple(''.join(outcome) for outcome in product('HT', repeat=2))
COIN_A = {outcome for outcome in COINS_TWO if outcome[0] == 'H'}
COIN_B = {outcome for outcome in COINS_TWO if outcome[1] == 'H'}
COIN_WEIGHTS = tuple(F(len(event), len(COINS_TWO)) for event in
                     (COIN_A, COIN_B, COIN_A & COIN_B, COIN_A | COIN_B))
assert len(COIN_TOSSES) == 2**3
assert COIN_WEIGHTS == (F(1, 2), F(1, 2), F(1, 4), F(3, 4))

DICE = tuple(product(range(1, 7), repeat=2))
SUM_SIX = {pair for pair in DICE if sum(pair) == 6}
BOTH_ODD = {pair for pair in DICE if all(die % 2 for die in pair)}
SUM_COUNTS = dict(sorted(Counter(map(sum, DICE)).items()))
DICE_WEIGHTS = tuple(F(len(event), len(DICE)) for event in
                     (SUM_SIX, BOTH_ODD, SUM_SIX & BOTH_ODD, SUM_SIX | BOTH_ODD))
assert len(DICE) == 36
assert SUM_SIX & BOTH_ODD == {(1, 5), (3, 3), (5, 1)}
assert DICE_WEIGHTS == (F(5, 36), F(9, 36), F(3, 36), F(11, 36))
assert list(SUM_COUNTS.values()) == [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]
assert F(SUM_COUNTS[7], len(DICE)) == F(1, 6)
ONE_SIX = F(1, 6)
BOOLE_BOUND = 3 * ONE_SIX
EXACT_SIX = 1 - (1 - ONE_SIX)**3
assert (BOOLE_BOUND, EXACT_SIX) == (F(1, 2), F(91, 216))
assert EXACT_SIX == F(sum(6 in toss for toss in product(range(1, 7), repeat=3)), 6**3)

POINT_MASSES = (F(3, 8), F(1, 4), F(1, 8), F(1, 8), F(1, 16), F(1, 16))
MASS_EVENT = (1, 2, 3)
assert sum(POINT_MASSES) == 1
assert sum(POINT_MASSES[index] for index in MASS_EVENT) == F(1, 2)

KEY_IDEAS = (
    r'In a discrete space, assign nonnegative probabilities to points with total $1$. Add the probabilities of the points in an event to obtain its probability.',
    r'For $A\cup B$, add the two probabilities and subtract the probability of $AB$, which was counted twice (Theorem 1.1).',
    'A union has probability at most the sum of the probabilities. For mutually exclusive events the sum is exact (Property 1.2).',
)

CODE = '''from random import Random
from itertools import combinations_with_replacement
rng = Random(1)
configs = list(combinations_with_replacement(range(3), 3))   # 10 configurations
N = 100_000
mb = sum(len({rng.randrange(3) for ball in "abc"}) == 3 for _ in range(N))
be = sum(len(set(rng.choice(configs))) == 3 for _ in range(N))
print(len(configs), mb / N, be / N)'''

OUTPUT = '10 0.22234 0.10054'

buffer = StringIO()
with redirect_stdout(buffer):
    exec(compile(CODE, 'Lesson 2 Code Lab', 'exec'), {})
assert buffer.getvalue().strip() == OUTPUT == '10 0.22234 0.10054'
config_count, mb_simulated, be_simulated = OUTPUT.split()
assert int(config_count) == len(CONFIGURATIONS)
SIMULATED_OCCUPIED = F(mb_simulated), F(be_simulated)
