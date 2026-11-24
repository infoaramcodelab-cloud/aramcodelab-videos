"""Check every worked example and run the Code Lab from SCRIPT.md."""

import re
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from io import StringIO
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial, perm, prod
from pathlib import Path


def multinomial(*sizes):
    return factorial(sum(sizes)) // prod(factorial(size) for size in sizes)


def check_subsets():
    days = 365

    def shared_birthday(people):
        return 1 - Fraction(perm(days, people), days**people)

    assert shared_birthday(22) < Fraction(1, 2) < shared_birthday(23)
    tiles = 'ABCDE'
    triples = Counter(frozenset(order) for order in permutations(tiles, 3))
    assert sum(triples.values()) == perm(len(tiles), 3) == 60
    assert set(triples.values()) == {factorial(3)} == {6}
    assert len(triples) == comb(len(tiles), 3) == 10
    couples = {frozenset(pair) for pair in combinations(tiles, 2)}
    assert {frozenset(tiles) - pair for pair in couples} == set(triples)
    assert len(couples) == comb(len(tiles), 2) == 10
    assert comb(len(tiles), 0) == comb(len(tiles), len(tiles)) == factorial(0) == 1
    for r in range(len(tiles) + 1):
        n = len(tiles)
        assert comb(n, r) == perm(n, r) // factorial(r)
        assert comb(n, r) == factorial(n) // (factorial(r) * factorial(n - r))


def check_cards():
    ranks, suits, poker_size = 13, 4, 5
    deck = ranks * suits
    assert deck == 52 and comb(deck, poker_size) == 2_598_960
    assert f'{comb(deck, poker_size) / 10**6:.1f}' == '2.6'
    rank_sets = comb(ranks, poker_size)
    suit_choices = suits**poker_size
    favourable = rank_sets * suit_choices
    assert (rank_sets, suit_choices, favourable) == (1287, 1024, 1_317_888)
    poker = Fraction(favourable, comb(deck, poker_size))
    assert poker > Fraction(1, 2) and f'{float(poker):.4f}' == '0.5071'

    bridge_hands = comb(deck, ranks)
    bridge_rank_probability = Fraction(suits**ranks, bridge_hands)
    assert bridge_hands == 635_013_559_600 and round(bridge_hands / 10**9) == 635
    assert f'{float(bridge_rank_probability):.7f}' == '0.0001057'
    assert abs(bridge_rank_probability / Fraction(1, 10_000) - 1) < Fraction(1, 10)


def check_senators_and_cells():
    states, per_state, seats = 50, 2, 50
    senators = states * per_state
    outside = senators - per_state
    assert (senators, outside, senators - seats, senators - seats - 1) == (100, 98, 50, 49)
    committees = comb(senators, seats)
    absent = Fraction(comb(outside, seats), committees)
    assert absent == Fraction(50 * 49, 100 * 99) == Fraction(49, 198)
    assert 1 - absent == Fraction(149, 198)
    assert f'{float(absent):.5f}' == '0.24747' and f'{float(1 - absent):.3f}' == '0.753'
    assert round(absent * 4) == 1 and round((1 - absent) * 4) == 3
    all_states = Fraction(per_state**states, committees)
    assert f'{float(all_states):.1e}' == '1.1e-14'
    assert round(float(1 / all_states) / 10**13) * 10 == 90

    cells, balls, selected = 3, 3, 2
    assignments = tuple(product(range(cells), repeat=balls))
    favourable = sum(item.count(0) == selected for item in assignments)
    choices = comb(balls, selected)
    other_assignments = (cells - 1)**(balls - selected)
    assert (choices, other_assignments, favourable, len(assignments)) == (3, 2, 6, 27)
    assert favourable == choices * other_assignments
    hit = Fraction(1, cells)
    assert hit == Fraction(1, 3)
    assert Fraction(favourable, len(assignments)) == choices * hit**selected * (1 - hit)**(balls - selected)
    assert Fraction(favourable, len(assignments)) == Fraction(2, 9)


def check_arrangements_and_paths():
    p, q = 2, 3
    letters = {''.join(order) for order in permutations('A' * p + 'B' * q)}
    assert len(letters) == multinomial(p, q) == comb(p + q, p) == comb(p + q, q) == 10

    displays = {((), (), ())}
    for flag in 'ABC':
        displays = {
            display[:i] + (pole[:j] + (flag,) + pole[j:],) + display[i + 1:]
            for display in displays
            for i, pole in enumerate(display)
            for j in range(len(pole) + 1)
        }
    by_colour = {tuple(''.join(pole).replace('B', 'A') for pole in display) for display in displays}
    assert len(displays) == prod((3, 4, 5)) == 60
    assert len(by_colour) == len(displays) // (factorial(2) * factorial(1)) == 30

    paths = {''.join(word) for word in product('RU', repeat=8) if word.count('R') == 5 and word.count('U') == 3}
    assert len(paths) == comb(5 + 3, 3) == 56
    highlighted = 'RURRURRU'
    assert highlighted in paths and (highlighted.count('R'), highlighted.count('U')) == (5, 3)
    assert Fraction(1, len(paths)) == Fraction(1, 56)
    assert comb(8 + 8, 8) == 12_870


def check_partitions():
    assert (comb(5, 2), comb(3, 2), comb(1, 1)) == (10, 3, 1)
    assert comb(5, 2) * comb(3, 2) * comb(1, 1) == multinomial(2, 2, 1) == multinomial(2, 2, 1, 0) == 30

    players, hand_size, aces = 4, 13, 4
    deck = players * hand_size
    deals = multinomial(*([hand_size] * players))
    assert deals == 53_644_737_765_488_792_839_237_440_000
    assert f'{deals:.2e}' == '5.36e+28' and f'{deals:.0e}' == '5e+28'
    assert deck - aces == 48 and hand_size - 1 == 12 and factorial(aces) == 24
    remaining = multinomial(*([hand_size - 1] * players))
    bridge = Fraction(factorial(aces) * remaining, deals)
    assert bridge == Fraction(24 * factorial(48) * 13**4, factorial(52)) == Fraction(2197, 20825)
    assert bridge == Fraction(hand_size**players, comb(deck, aces))
    assert Fraction(1, 10) < bridge < Fraction(11, 100) and f'{float(bridge):.3f}' == '0.105'

    dice = 12
    faces = tuple(range(1, 7))
    per_face = 2
    assert Fraction(dice, len(faces)) == per_face
    assert (dice, faces[0], faces[-1], per_face) == (12, 1, 6, 2)
    outcomes = len(faces)**dice
    successes = multinomial(*([per_face] * len(faces)))
    assert (outcomes, successes) == (2_176_782_336, 7_484_400)
    assert successes == factorial(dice) // (2**6)
    balanced_dice = Fraction(successes, outcomes)
    assert balanced_dice == Fraction(1925, 559872) and f'{float(balanced_dice):.6f}' == '0.003438'
    assert abs(balanced_dice - Fraction(1, 300)) < Fraction(1, 1000)
    return bridge


def check_summary_and_code(bridge):
    tiles = 'ABC'
    draws = 2
    assert len(list(permutations(tiles, draws))) == perm(len(tiles), draws) == 6
    assert len(list(combinations(tiles, draws))) == comb(len(tiles), draws) == 3
    assert len(list(product(tiles, repeat=draws))) == len(tiles)**draws == 9
    repeated = [''.join(sample) for sample in combinations_with_replacement(tiles, draws)]
    assert repeated == ['AA', 'AB', 'AC', 'BB', 'BC', 'CC']
    assert len(repeated) == comb(draws + len(tiles) - 1, draws) == comb(4, 2) == 6

    source = Path(__file__).with_name('SCRIPT.md').read_text(encoding='utf-8')
    fence = chr(96) * 3
    match = re.search(rf'{fence}python\n(.*?)\n{fence}\n\nOutput:\n{fence}\n(.*?)\n{fence}', source, re.S)
    assert match, 'Code Lab program or output is missing'
    code, expected = match.groups()
    assert len(code.splitlines()) <= 12
    output = StringIO()
    values = {}
    with redirect_stdout(output):
        exec(compile(code, 'Lesson 4 Code Lab', 'exec'), values)
    assert values['trials'] == 100_000 and values['hits'] == 10_501 and values['exact'] == bridge
    assert output.getvalue().strip() == expected == '0.105010 0.105498'
    print(f'All checked numbers passed. Code Lab: {expected}')


if __name__ == '__main__':
    check_subsets()
    check_cards()
    check_senators_and_cells()
    check_arrangements_and_paths()
    check_summary_and_code(check_partitions())
