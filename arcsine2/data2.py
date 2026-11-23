"""Extra data for the flagship video (everything else comes from ../arcsine/data.py)."""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'arcsine'))
from data import (EXACT, FRACS, HIST, GRID, GRID_FRAC, GRID_LOPSIDED, N, TH_40_60, TH_OVER_90, _S, lead_fraction, u, walk)  # noqa

# short game for the puzzle: 60 tosses, crosses zero a few times
def _short(seed):
    return walk(seed, 60)


PUZZLE = next(_short(s) for s in range(1, 500)
              if 3 <= np.sum(_short(s)[1:-1] == 0) <= 5 and _short(s).max() >= 4 and _short(s).min() <= -3)

# the reflection picture: starts at 2, first touch of 0 at t = 4, ends at 3
REFL = [2, 3, 2, 1, 0, 1, 2, 3, 2, 3, 4, 3, 4, 3]

# the last-tie picture: 40 tosses, last zero between 14 and 22, at least 3 earlier zeros, then stays away
def _lt(seed):
    s = walk(seed, 40)
    z = [i for i, v in enumerate(s) if v == 0]
    return s, z


LAST = next(_lt(s)[0] for s in range(1, 2000)
            if 14 <= _lt(s)[1][-1] <= 22 and 4 <= len(_lt(s)[1]) <= 6 and abs(_lt(s)[0][-1]) >= 5)
LAST_TIE = max(i for i, v in enumerate(LAST) if v == 0)

# bars -> curve: density n * u_2k u_2n-2k at x = k / n
def bars(n):
    return [n * u(2 * k) * u(2 * n - 2 * k) for k in range(n + 1)]


# a "season": 160 games, one team ahead almost all the time (not chosen for anything else)
SEASON = next(walk(s, 160) for s in range(3000, 4000) if lead_fraction(walk(s, 160)) > 0.92 and walk(s, 160)[-1] < 25)

# the ballot challenge: 60 A votes and 40 B votes in random order
_rng = np.random.default_rng(60)
BALLOT = _rng.permutation(np.array([1] * 60 + [-1] * 40))

if __name__ == '__main__':
    print('puzzle zeros', int(np.sum(PUZZLE[1:-1] == 0)), PUZZLE.min(), PUZZLE.max())
    print('last tie at', LAST_TIE, 'end', LAST[-1], 'zeros', [i for i, v in enumerate(LAST) if v == 0])
    print('season frac', lead_fraction(SEASON), SEASON[-1])
    print('bars 200 ends', bars(200)[0], bars(200)[100])
    print('ballot path min', np.cumsum(BALLOT).min())
