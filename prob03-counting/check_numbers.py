"""Verify the worked numbers and run the Code Lab from the lesson script."""

import re
from contextlib import redirect_stdout
from decimal import Decimal, localcontext
from fractions import Fraction
from io import StringIO
from itertools import permutations, product
from math import comb, exp, factorial, perm, prod
from pathlib import Path


def check_multiplication():
    dice = tuple(product(range(1, 7), repeat=2))
    sums = sorted({sum(pair) for pair in dice})
    sevens = sum(sum(pair) == 7 for pair in dice)
    assert len(dice) == 36 and sums == list(range(2, 13)) and len(sums) == 11
    assert sevens == 6 and Fraction(sevens, len(dice)) == Fraction(1, 6) != Fraction(1, len(sums))

    assert len(tuple(product(range(2), range(3)))) == 6
    mains = {'soup': ('fish', 'pasta'), 'salad': ('pasta', 'rice'), 'bread': ('rice', 'fish')}
    starter_main_pairs = [(starter, main) for starter, choices in mains.items() for main in choices]
    assert len(mains) == 3 and all(len(choices) == 2 for choices in mains.values())
    assert len(starter_main_pairs) == 6
    assert len(tuple(product(starter_main_pairs, range(4)))) == 24

    assert len(tuple(product(range(4), range(13)))) == 52
    settings = range(3 + 1)
    switch_pairs = set(product(settings, repeat=2))
    assert tuple(settings) == (0, 1, 2, 3)
    assert len(switch_pairs) == 16 and len(switch_pairs - {(0, 0)}) == 15
    assert len(set(product(range(3), repeat=3))) == 27
    faces = tuple(range(1, 7))
    ace = faces[0]
    all_rolls = tuple(product(faces, repeat=6))
    no_ace = sum(ace not in rolls for rolls in all_rolls)
    assert ace == 1 and len(all_rolls) == 6**6 == 46_656 and no_ace == 5**6 == 15_625
    at_least_one = 1 - Fraction(no_ace, len(all_rolls))
    assert at_least_one == 1 - Fraction(5, 6)**6 < Fraction(2, 3)
    assert f'{float(at_least_one):.3f}' == '0.665' and f'{float(at_least_one):.1%}' == '66.5%'

    displays = {((), (), ())}
    for flag, slots in enumerate((3, 4, 5)):
        assert {sum(len(pole) + 1 for pole in display) for display in displays} == {slots}
        displays = {
            display[:i] + (pole[:j] + (flag,) + pole[j:],) + display[i + 1:]
            for display in displays
            for i, pole in enumerate(display)
            for j in range(len(pole) + 1)
        }
    assert len(displays) == prod((3, 4, 5)) == 60


def check_samples():
    n, r = 5, 3
    with_replacement = tuple(product(range(n), repeat=r))
    without_replacement = tuple(permutations(range(n), r))
    assert len(with_replacement) == n**r == 125
    assert len(without_replacement) == perm(n, r) == 60
    assert Fraction(1, len(with_replacement)) == Fraction(1, 125)
    assert Fraction(1, len(without_replacement)) == Fraction(1, 60)
    assert tuple(permutations(range(n), 0)) == ((),) and perm(n, 0) == 1
    assert all(perm(n, k) == 0 for k in range(n + 1, n + 4))
    assert len(tuple(permutations(range(3)))) == factorial(3) == 3 * 2 * 1 == 6

    letters, length, per_letter = 26, 10, 1000
    pieces = letters * per_letter
    assert letters**length == 141_167_095_653_376 and pieces == 26_000
    ordinary, distinct = pieces**length, perm(pieces, length)
    assert ordinary >= distinct > 10**44
    assert f'{float(Fraction(distinct, ordinary)):.6f}' == '0.998271'

    misses_without = sum(0 not in sample for sample in without_replacement)
    misses_with = sum(0 not in sample for sample in with_replacement)
    assert misses_without == perm(n - 1, r) == 24
    assert 1 - Fraction(misses_without, perm(n, r)) == Fraction(r, n) == Fraction(3, 5)
    assert misses_with == (n - 1)**r == 64
    assert 1 - Fraction(misses_with, n**r) == 1 - Fraction(4, 5)**3 == Fraction(61, 125)

    digits = range(10)
    assert digits[0] == 0 and digits[-1] == 9
    no_repeat = Fraction(perm(len(digits), 5), len(digits)**5)
    assert no_repeat == Fraction('0.3024') and f'{float(no_repeat):.0%}' == '30%'
    with localcontext() as ctx:
        # Extra digits keep rounding at the end of the expansion away from the slice.
        ctx.prec = 2508
        first_digits = str(Decimal(1).exp()).partition('.')[2][:2500]
    groups = [first_digits[i:i + 5] for i in range(0, len(first_digits), 5)]
    assert len(first_digits) == 2500 and len(groups) == 500
    distinct_groups = sum(len(set(group)) == 5 for group in groups)
    assert distinct_groups == 150 and f'{float(Fraction(distinct_groups, len(groups))):.3f}' == '0.300'
    return len(first_digits), len(groups), distinct_groups


def check_occupancy():
    accidents = Fraction(factorial(7), 7**7)
    assert f'{float(accidents):.5f}' == '0.00612'
    assert f'{float(1 / accidents):.1f}' == '163.4' and round(1 / accidents) == 163

    all_faces = Fraction(factorial(6), 6**6)
    assert f'{float(all_faces):.4f}' == '0.0154' and f'{float(all_faces):.1%}' == '1.5%'

    floors, passengers = 10, 7
    choices = tuple(range(floors, floors - passengers, -1))
    assert choices == (10, 9, 8, 7, 6, 5, 4) and perm(floors, passengers) == prod(choices)
    different_floors = Fraction(prod(choices), floors**passengers)
    assert different_floors == Fraction('0.06048') and f'{float(different_floors):.0%}' == '6%'


def check_birthdays():
    days = 365
    domain = range(1, 61)
    assert (domain[0], domain[-1]) == (1, 60)
    no_match = {r: Fraction(perm(days, r), days**r) for r in domain}
    assert all(
        no_match[r] == prod(Fraction(days - k, days) for k in range(r))
        for r in domain
    )
    assert all(no_match[r + 1] < no_match[r] for r in range(1, 60))
    assert min(r for r in domain if 1 - no_match[r] > Fraction(1, 2)) == 23
    assert no_match[22] > Fraction(1, 2) > no_match[23]
    assert [f'{float(no_match[r]):.3f}' for r in (22, 23, 30)] == ['0.524', '0.493', '0.294']
    assert f'{float(1 - no_match[23]):.3f}' == '0.507' and no_match[30] < Fraction(3, 10)

    r = 30
    assert r * (r - 1) == 870 and 2 * days == 730
    assert f'{exp(-r * (r - 1) / (2 * days)):.3f}' == '0.304'
    assert Fraction(days, days**2) == Fraction(1, 365)
    assert comb(23, 2) == 23 * 22 // 2 == 253
    return 1 - no_match[23]


def check_code_lab(exact_probability):
    script = Path(__file__).with_name('SCRIPT.md').read_text(encoding='utf-8')
    marker = '```'
    code, stated_output = re.search(
        rf'{marker}python\n(.*?)\n{marker}\n\nOutput:\n{marker}\n(.*?)\n{marker}', script, re.S
    ).groups()
    assert len(code.splitlines()) <= 12
    printed = StringIO()
    scope = {}
    with redirect_stdout(printed):
        exec(compile(code, 'Lesson 3 Code Lab', 'exec'), scope)
    assert (scope['people'], scope['days'], scope['trials']) == (23, 365, 100_000)
    assert scope['matches'] == 50_649
    assert scope['exact'] == exact_probability
    assert f'{float(exact_probability):.4f}' == '0.5073'
    assert printed.getvalue().strip() == stated_output == '0.5065 0.5073'
    return stated_output


if __name__ == '__main__':
    check_multiplication()
    check_samples()
    check_occupancy()
    exact_probability = check_birthdays()
    print(f'All checked numbers passed. Code Lab: {check_code_lab(exact_probability)}')
