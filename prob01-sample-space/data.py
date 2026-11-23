"""Numbering and wording from the site, with the approved Code Lab cell."""

ARRANGEMENTS = {1: ('abc', '', ''),
 2: ('', 'abc', ''),
 3: ('', '', 'abc'),
 4: ('ab', 'c', ''),
 5: ('ac', 'b', ''),
 6: ('bc', 'a', ''),
 7: ('ab', '', 'c'),
 8: ('ac', '', 'b'),
 9: ('bc', '', 'a'),
 10: ('a', 'bc', ''),
 11: ('b', 'ac', ''),
 12: ('c', 'ab', ''),
 13: ('a', '', 'bc'),
 14: ('b', '', 'ac'),
 15: ('c', '', 'ab'),
 16: ('', 'ab', 'c'),
 17: ('', 'ac', 'b'),
 18: ('', 'bc', 'a'),
 19: ('', 'a', 'bc'),
 20: ('', 'b', 'ac'),
 21: ('', 'c', 'ab'),
 22: ('a', 'b', 'c'),
 23: ('a', 'c', 'b'),
 24: ('b', 'a', 'c'),
 25: ('b', 'c', 'a'),
 26: ('c', 'a', 'b'),
 27: ('c', 'b', 'a')}

EVENTS = {
    'crowded': tuple(index for index, cells in ARRANGEMENTS.items() if max(map(len, cells)) >= 2),
    'first': tuple(index for index, cells in ARRANGEMENTS.items() if cells[0]),
    'full': tuple(index for index, cells in ARRANGEMENTS.items() if all(cells)),
    'first_empty': tuple(index for index, cells in ARRANGEMENTS.items() if not cells[0] and max(map(len, cells)) >= 2),
    'impossible': tuple(index for index, cells in ARRANGEMENTS.items() if all(len(cell) == 2 for cell in cells)),
}

COIN_TOSSES = ('HHH', 'HHT', 'HTH', 'THH', 'HTT', 'THT', 'TTH', 'TTT')
MAJORITY_HEADS = frozenset(outcome for outcome in COIN_TOSSES if outcome.count('H') >= 2)
EXACTLY_ONE_TAIL = frozenset(outcome for outcome in COIN_TOSSES if outcome.count('T') == 1)

TOURNAMENT_FINITE = (
    ('aa', 'acc', 'acbb', 'acbaa', 'acbacc'),
    ('bb', 'bcc', 'bcaa', 'bcabb', 'bcabcc'),
)
TOURNAMENT_ENDLESS = ('acbacbacb…', 'bcabcabca…')

KEY_IDEAS = ['Each elementary outcome is one sample point. An event is a subset of the sample space $\\Omega$.',
 '$AB$ means both events occur, and $A\\cup B$ means at least one occurs. Mutually exclusive '
 'events have empty intersection.',
 "The complement $A'$ contains outcomes outside $A$. In particular, $(A\\cup B)'=A'B'$."]

CODE = '''from itertools import product
points = list(product("123", repeat=3))   # cells of balls a, b, c
crowded = {p for p in points if len(set(p)) < 3}
full = {p for p in points if len(set(p)) == 3}
first_used = {p for p in points if "1" in p}
print(len(points), len(crowded), len(full), len(first_used))
S, A, B = set(points), crowded, {p for p in points if p[0] == "1"}
print(len(S - (A | B)), S - (A | B) == (S - A) & (S - B))'''

OUTPUT = '''27 21 6 19
4 True'''
