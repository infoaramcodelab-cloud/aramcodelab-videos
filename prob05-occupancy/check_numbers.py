"""Check the on-screen examples and run the Code Lab from SCRIPT.md."""

import re
from collections import Counter
from contextlib import redirect_stdout
from fractions import Fraction
from io import StringIO
from itertools import combinations, groupby, product
from math import comb, factorial, prod
from pathlib import Path


def occupancies(placements, cells):
    counts = Counter(placements)
    return tuple(counts[cell] for cell in range(cells))


def compositions(balls, cells):
    """Enumerate occupancies by choosing the inner-bar positions."""
    width = balls + cells - 1
    for bars in combinations(range(width), cells - 1):
        edges = (-1, *bars, width)
        yield tuple(right - left - 1 for left, right in zip(edges, edges[1:]))


def multinomial(sizes):
    return factorial(sum(sizes)) // prod(factorial(size) for size in sizes)


def run_lengths(sequence):
    return tuple(sum(1 for _ in run) for _, run in groupby(sequence))


def seating(size, marked):
    marked = set(marked)
    return "".join("O" if index in marked else "E" for index in range(size))


def check_counting():
    symbol = "|***|*|||****|"
    example = tuple(map(len, symbol.split("|")[1:-1]))
    assert example == (3, 1, 0, 0, 4) and sum(example) == 8 and len(example) == 5
    assert symbol.count("|") == 6 and symbol[1:-1].count("|") == 4
    assert len(symbol[1:-1]) == 12
    vectors = set(compositions(8, 5))
    assert example in vectors
    assert len(vectors) == comb(12, 8) == comb(12, 4) == 495
    assert 8 - 1 == 7 and 8 - 5 == 3
    nonempty = {vector for vector in vectors if all(vector)}
    restored = {tuple(count + 1 for count in vector) for vector in compositions(3, 5)}
    assert nonempty == restored and len(nonempty) == comb(7, 4) == 35

    dice = {occupancies(roll, 6) for roll in product(range(6), repeat=3)}
    assert dice == set(compositions(3, 6)) and len(dice) == comb(8, 5) == 56
    assert 6 - 1 == 5 and occupancies((1, 1, 4), 6) == (0, 2, 0, 0, 1, 0)
    assert occupancies((0, 1, 0, 2), 3) == (2, 1, 1)
    assert len(set(compositions(4, 3))) == comb(6, 4) == 15
    assert len(set(compositions(5, 3))) == comb(7, 5) == 21

    placements = list(product(range(3), repeat=3))
    vector = (2, 1, 0)
    matches = sum(occupancies(placement, 3) == vector for placement in placements)
    assert len(placements) == 3**3 == 27 and matches == multinomial(vector) == 3
    assert Fraction(matches, len(placements)) == Fraction(1, 9)


def check_configuration_table(script):
    site_rows = {
        (2, 2, 1, 1, 1, 0, 0): "0.321295",
        (3, 2, 1, 1, 0, 0, 0): "0.214197",
        (2, 1, 1, 1, 1, 1, 0): "0.128518",
        (2, 2, 2, 1, 0, 0, 0): "0.107098",
        (3, 1, 1, 1, 1, 0, 0): "0.107098",
        (4, 1, 1, 1, 0, 0, 0): "0.035699",
        (3, 2, 2, 0, 0, 0, 0): "0.026775",
        (4, 2, 1, 0, 0, 0, 0): "0.026775",
        (3, 3, 1, 0, 0, 0, 0): "0.017850",
        (1, 1, 1, 1, 1, 1, 1): "0.006120",
        (5, 1, 1, 0, 0, 0, 0): "0.005355",
        (4, 3, 0, 0, 0, 0, 0): "0.001785",
        (5, 2, 0, 0, 0, 0, 0): "0.001071",
        (6, 1, 0, 0, 0, 0, 0): "0.000357",
        (7, 0, 0, 0, 0, 0, 0): "0.000008",
    }
    counts = Counter()
    for vector in compositions(7, 7):
        counts[tuple(sorted(vector, reverse=True))] += multinomial(vector)
    total = 7**7
    assert total == 823_543 and sum(counts.values()) == total
    assert len(counts) == len(site_rows) == 15
    assert counts.keys() == site_rows.keys()

    for vector, count in counts.items():
        assert count == multinomial(Counter(vector).values()) * multinomial(vector)

    probabilities = {vector: Fraction(count, total) for vector, count in counts.items()}
    assert sum(probabilities.values()) == 1
    formatted = {vector: f"{float(value):.6f}" for vector, value in probabilities.items()}
    # The second-highest value in the site table rounds incorrectly. Keep the source values above so
    # any additional discrepancy fails the check.
    source_typo = (3, 2, 1, 1, 0, 0, 0)
    differences = {
        vector: (site_rows[vector], value)
        for vector, value in formatted.items()
        if value != site_rows[vector]
    }
    assert differences == {source_typo: ("0.214197", "0.214196")}
    assert counts[source_typo] == 176_400
    corrected_rows = dict(site_rows)
    corrected_rows[source_typo] = formatted[source_typo]
    script_rows = re.findall(r"^\| ((?:\d,){6}\d) \| (0\.\d{6}) \|$", script, re.M)
    assert len(script_rows) == 15
    parsed_rows = [(tuple(map(int, vector.split(","))), value) for vector, value in script_rows]
    assert parsed_rows == list(corrected_rows.items())
    assert list(map(counts.get, site_rows)) == sorted(counts.values(), reverse=True)
    assert sum(map(Fraction, site_rows.values())) == Fraction("1.000001")
    assert sum(map(Fraction, corrected_rows.values())) == 1

    target = (2, 2, 1, 1, 1, 0, 0)
    assert max(counts, key=counts.get) == target
    roles = tuple(target.count(count) for count in (2, 1, 0))
    assert roles == (2, 3, 2) and multinomial(roles) == 210
    assert multinomial(target) == 1_260
    assert counts[target] == 210 * 1_260 == 264_600
    assert probabilities[target] == Fraction(264_600, 823_543)
    assert f"{float(probabilities[target]):.4f}" == "0.3213"
    even = (1,) * 7
    assert counts[even] == factorial(7)
    assert f"{float(probabilities[even]):.4f}" == "0.0061"
    return target, probabilities[target]


def check_three_statistics():
    vector = (1, 0, 1, 1, 0)
    assert tuple(index for index, count in enumerate(vector, start=1) if count) == (1, 3, 4)
    placements = list(product(range(5), repeat=3))
    favourable = sum(occupancies(placement, 5) == vector for placement in placements)
    assert favourable == factorial(3) == 6 and len(placements) == 5**3 == 125
    assert Fraction(favourable, len(placements)) == Fraction(6, 125)

    vectors = list(compositions(3, 5))
    assert vectors.count(vector) == 1 and len(vectors) == comb(7, 3) == 35
    assert Fraction(1, len(vectors)) == Fraction(1, 35)
    single_occupancy = [candidate for candidate in vectors if all(count <= 1 for count in candidate)]
    assert single_occupancy.count(vector) == 1 and len(single_occupancy) == comb(5, 3) == 10
    assert Fraction(1, len(single_occupancy)) == Fraction(1, 10)


def check_runs():
    assert run_lengths("AAABAABBBA") == (3, 1, 2, 3, 1)
    words = (seating(7, indices) for indices in combinations(range(7), 3))
    matching = sum(
        word.startswith("E") and word.endswith("E") and len(run_lengths(word)) == 5
        for word in words
    )
    assert matching == comb(2, 1) * comb(3, 2) == 2 * 3 == 6

    observed = "EOEEOEEEOEEEOEOE"
    assert len(observed) == 16 and observed.count("O") == 5 and observed.count("E") == 11
    groups = [(kind, sum(1 for _ in group)) for kind, group in groupby(observed)]
    assert [length for kind, length in groups if kind == "O"] == [1] * 5
    assert sum(kind == "E" for kind, _ in groups) == 6
    assert len(groups) == 11
    counts = Counter()
    for indices in combinations(range(16), 5):
        word = seating(16, indices)
        runs = len(run_lengths(word))
        counts[runs] += 1
        assert (runs == 11) == (word[0] == word[-1] == "E" and "OO" not in word)

    assert max(counts) == 11 and counts[11] == comb(4, 4) * comb(10, 5) == 252
    assert sum(counts.values()) == comb(16, 5) == 4_368
    probability = Fraction(counts[11], sum(counts.values()))
    assert probability == Fraction(3, 52) and f"{float(probability):.4f}" == "0.0577"


def check_code_lab(script, target, probability):
    match = re.search(r"```python\n(.+?)\n```\n\nOutput:\n```\n(.+?)\n```", script, re.S)
    assert match is not None
    code, expected = match.groups()
    assert len(code.splitlines()) <= 12
    output = StringIO()
    state = {}
    with redirect_stdout(output):
        exec(compile(code, "SCRIPT.md: Code Lab", "exec"), state)
    assert state["cells"] == 7 and state["trials"] == 100_000
    assert tuple(state["target"]) == tuple(sorted(target)) and state["hits"] == 32_159
    assert re.search(r"^rng = Random\(5\)$", code, re.M)
    assert output.getvalue() == expected + "\n"
    assert expected == f"{state['hits'] / state['trials']:.6f} {float(probability):.6f}"
    assert expected == "0.321590 0.321295"
    return expected


if __name__ == "__main__":
    script = Path(__file__).with_name("SCRIPT.md").read_text(encoding="utf-8")
    check_counting()
    target, probability = check_configuration_table(script)
    check_three_statistics()
    check_runs()
    print(check_code_lab(script, target, probability))
    print("All checked numbers match.")
