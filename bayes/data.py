"""Probability model, exact frequencies and reproducible trials for the video."""

from dataclasses import dataclass
from fractions import Fraction
from itertools import islice
from random import Random


PEOPLE = 10_000
CODE_PEOPLE = 1_000_000
GRID_SIDE = 100
BASE_RATE = Fraction(1, 100)
RARE_RATE = Fraction(1, 1_000)
SENSITIVITY = Fraction(99, 100)
FALSE_POSITIVE_RATE = Fraction(1, 100)
SEED = 7
CHALLENGE_SEED = 17
GUESS_SECONDS = 4
GUESS_OPTIONS = (1, 100, 1_000)


@dataclass(frozen=True)
class Counts:
    true_positive: int
    false_negative: int
    false_positive: int
    true_negative: int

    @property
    def positives(self):
        return self.true_positive + self.false_positive

    @property
    def ill(self):
        return self.true_positive + self.false_negative

    @property
    def healthy(self):
        return self.false_positive + self.true_negative

    @property
    def posterior(self):
        return Fraction(self.true_positive, self.positives)


def exact_frequencies(prevalence, size):
    rates = (
        prevalence * SENSITIVITY,
        prevalence * (1 - SENSITIVITY),
        (1 - prevalence) * FALSE_POSITIVE_RATE,
        (1 - prevalence) * (1 - FALSE_POSITIVE_RATE),
    )
    amounts = [size * rate for rate in rates]
    if any(amount.denominator != 1 for amount in amounts):
        raise ValueError("Choose a population that gives integral expected counts")
    return Counts(*(int(amount) for amount in amounts))


def trials(prevalence, seed):
    rng = Random(seed)
    while True:
        ill = rng.random() < float(prevalence)
        rate = SENSITIVITY if ill else FALSE_POSITIVE_RATE
        yield ill, rng.random() < float(rate)


def tally(outcomes):
    counts = [0] * 4
    for ill, positive in outcomes:
        counts[2 * (not ill) + (not positive)] += 1
    return Counts(*counts)


EXACT = exact_frequencies(BASE_RATE, PEOPLE)
GRID = tuple(islice(trials(BASE_RATE, SEED), PEOPLE))
GRID_COUNTS = tally(GRID)
CODE_COUNTS = tally(islice(trials(BASE_RATE, SEED), CODE_PEOPLE))
CHALLENGE_EXACT = exact_frequencies(RARE_RATE, 100_000)

CODE = f"""from random import Random
rng = Random({SEED})
positives = true_positives = 0
for _ in range({CODE_PEOPLE:_}):
    ill = rng.random() < {float(BASE_RATE)}
    rate = {float(SENSITIVITY)} if ill else {float(FALSE_POSITIVE_RATE)}
    if rng.random() < rate:
        positives += 1
        true_positives += ill
print(f"{{true_positives / positives:.1%}}")"""


if __name__ == '__main__':
    assert GRID_SIDE**2 == PEOPLE
    assert EXACT == Counts(99, 1, 99, 9801)
    assert GRID_COUNTS == Counts(107, 0, 97, 9796)
    assert CODE_COUNTS == Counts(10098, 86, 9809, 980007)
    assert CHALLENGE_EXACT.posterior == Fraction(11, 122)
    assert tally(islice(trials(RARE_RATE, CHALLENGE_SEED), CODE_PEOPLE)) == (
        Counts(985, 6, 10015, 988994)
    )
    exec(CODE)
