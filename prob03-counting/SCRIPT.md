# Probability Theory · Lesson 3 — The Multiplication Rule and Ordered Samples

The narration and visual plan of the lesson. `script.py` holds the same narration split at the visual cues.
Voice: Orpheus, Tara. The published narration was sped up by 7 % after generation
(`ffmpeg -filter:a atempo=1.07`), and `audio/durations.json` holds the timings of the sped-up clips.
`check_numbers.py` checks every number in the narration and on screen.

Site section: 2.1 The multiplication rule and ordered samples (slug `the-multiplication-rule-and-ordered-samples`).
Next lesson: 2.2 Subpopulations and partitions. Built with the lesson kit.

Colour code (as in Lesson 2):
- sample points and unused slots: muted; current choices and favourable outcomes: teal;
- the second sampling procedure and the birthday plot's dashed one-half line: indigo;
- repeat draws, shared birthdays and “Careful” cards: amber.

Chapters: Welcome · Counting pairs · Successive choices · Cards, lamps, balls and dice · Flags on poles ·
Ordered samples · Permutations · Letters and pieces of type · Random samples · Will a particular element appear? ·
No repetition · Accidents, dice and elevators · The birthday problem · Code Lab · Key ideas
(timestamps come from the render)

---

## 1. Welcome (≈ 35 s) · `welcome`, `recap`

**Visual.** title_card("2.1", "The Multiplication Rule and Ordered Samples", lesson 3).

> Welcome back. Last time we saw how probability becomes a fraction when every outcome is equally likely.
> Today we'll work on the two counts in that fraction. A few rules will take us from a deck of cards to a room
> full of birthdays.

**Visual.** Show $\mathbf P\{A\}=|A|/|\Omega|$ with “Favourable outcomes” above the numerator and “All outcomes” below the denominator.
Use the Lesson 2 dice matrix and its sum cards. Highlight sum 7 and its 6 pairs: $6/36=1/6$. Mark $1/11$ as the
incorrect shortcut.

> Remember the dice trap? There are eleven possible sums, but they aren't equally likely. Six of the thirty-six
> ordered pairs give a sum of seven. So the chance is one sixth. Before you count, decide what a single outcome
> represents and why the outcomes you count should have equal weight.

## 2. Counting pairs (≈ 40 s) · `pairs`, `pair_table`

**Visual.** box(theorem, "Theorem 2.1"): $m$ choices from the first group and $n$ from the second give $mn$
pairs. Build a 2×3 table of two shirt colours and three hat colours. Then show the general table
from `mult-table.svg`, highlighting cell $(a_j,b_k)$.

> Say you have two shirts and three hats. How many outfits use one of each? Put the shirts down the side
> of a table and the hats across the top. Each shirt has three possible partners. That's two times three,
> so six outfits.

> Now call the group sizes m and n. The pair with the j-th shirt and the k-th hat goes in row j, column k.
> Every pair goes in exactly one cell, and every cell gives a pair. So there are m times n pairs.

## 3. Successive choices (≈ 55 s) · `multiplets`, `fixed_counts`

**Visual.** box(theorem, "Theorem 2.2"): $n_1 n_2\cdots n_r$ ordered tuples. Group the first two entries as
a pair, then attach a third choice. Pause on a decision tree with branch counts 3, 2 and 4 and 24 leaves.

> What if an order has a starter, a main dish and a dessert? With three starters and two mains, we have six
> starter and main pairs. Treat each pair as a single choice and attach any of four desserts. That gives
> twenty-four meals. To go further, repeat the same step. Each time you add a group, multiply by its size.
> For r groups, that's n one times n two, all the way through n r.

**Visual.** Label the 3 levels of the tree with their branch counts. At the second level, show different
lists of mains for different starters, each containing exactly 2 choices.

> The rule also works when a choice changes what's available later. The starter might change which mains
> the restaurant offers you. As long as each starter still has exactly two mains, and each starter and main
> pair still has four desserts, the count stays the same. At step k, the number of options has to be fixed.
> The options themselves can change. If the count changes too, count the different branches separately.

## 4. Cards, lamps, balls and dice (≈ 70 s) · `cards_lamp`, `balls_cells`, `no_ace`

**Visual.** box(example, "Example 2.1"). Show 4 suit symbols across 13 ranks. Beside it, show a lamp with
3 bulbs controlled by a switch and an indirect light with 4 levels, each switch labelled 0 through 3.
In the 4×4 settings grid, cross out $(0,0)$: $16-1=15$.

> In a standard deck, each card has one of four suits and one of thirteen ranks, for fifty-two cards.
> Now take a lamp with two switches. One selects how many of its three bulbs are on. The other sets the
> indirect light. Each switch has four settings, including zero. There are sixteen pairs of settings,
> and both at zero means off. That leaves fifteen ways to use the lamp.

**Visual.** Each labelled ball chooses a cell. Show $n$ choices for each of $r$ labelled balls and
$n\cdot n\cdots n=n^r$. Bring back the 27-tile grid for 3 balls and 3 cells.

> For the labelled balls from our first lesson, record the cell chosen by each ball in order. Each of r
> balls has n cells to choose from, so there are n to the power r arrangements. Three balls and three
> cells give three times three times three, or twenty-seven.

**Visual.** Show a fair die with the one face marked “Ace”. Use $6^r$ total sequences and $5^r$ without an ace.
Derive $(5/6)^r$ and $1-(5/6)^6\approx0.665<2/3$.

> An ace on a die means a one. When you roll a fair die r times, there are six to the power r equally likely
> sequences. Avoid the ace, and there are only five choices per roll. Divide those counts and you get
> five sixths to the power r. To get at least one ace in six rolls, subtract the no-ace probability from one.
> The answer is about sixty-six and a half percent, a little under two thirds.

## 5. Flags on poles (≈ 45 s) · `flag_slots`, `flag_count`

**Visual.** box(example, "Example 2.2"). Show 3 poles in a row and 3 different flags. After each placement,
mark every legal insertion slot. Move the first flag to another pole and show that the second flag
still has 4 slots. After placing the second flag, show 5 slots.

> Hang three different flags on three poles. Top to bottom matters on each pole. The first flag has three
> places to go. Wherever it lands, its old slot becomes two slots, one above it and one below it.
> So the next flag has four choices. Placing that flag splits another slot, and now there are five.

**Visual.** Derive $3\cdot4\cdot5=60$, then $n(n+1)(n+2)\cdots(n+r-1)$ for $r$ flags and $n$ poles.

> That gives sixty displays. Every finished display tells you where the last flag went. Remove that flag
> and you can work backwards through the earlier decisions. So each display gets counted once.
> With n poles and r flags, the product starts at n and goes up to n plus r minus one.

## 6. Ordered samples (≈ 65 s) · `sample_order`, `replacement`, `falling_product`

**Visual.** A population of 5 tiles labelled A through E and a sample tray with 3 slots. Swap A and B
in two trays to compare $(A,B,C)$ with $(B,A,C)$.

> A population is the group we're drawing from. Draw some elements and write them down in draw order.
> That's an ordered sample. A, B, C and B, A, C count separately. Even with the same elements, the first
> two positions tell different stories.

**Visual.** Parallel trays, “With replacement” and “Without replacement”. In the first, copy the drawn tile to
the tray and leave the original available. In the second, move it out of the population. Highlight a repeated
tile in amber. Show $5\cdot5\cdot5=125$ and $5\cdot4\cdot3=60$.

> With replacement, put each element back after recording it. A repeat is possible, and each of the three slots
> still has five choices. That gives a hundred twenty-five sequences. Without replacement, the chosen element
> stays out. The available counts drop from five to four to three, giving sixty sequences.

**Visual.** box(theorem, "Theorem 2.3"): $n^r$ with replacement and $(n)_r$ without replacement. Show
$(n)_r=n(n-1)\cdots(n-r+1)$ (2.1), $(n)_0=1$ and $(n)_r=0$ for integers $r>n$. Use the empty tray and an
overfilled tray beside the 5-tile population to illustrate the boundary cases.

> In general, with replacement the count is n to the power r. Without replacement, multiply n times n minus one,
> down to n minus r plus one. We write that product as n sub r. If you ask for more elements than the population
> contains, there are zero samples without replacement. If you ask for no elements, the empty sequence
> is the only sample.

## 7. Permutations (≈ 35 s) · `permutations`

**Visual.** Theorem-style box titled “Corollary”. Fill a tray using every piece of a 3-tile population and show all
$3!=6$ orderings. Then show $n!=n(n-1)\cdots2\cdot1=(n)_n$ (2.2).

> Now draw until the population is empty. The sample contains every element once. It's a permutation,
> which just means a reordering. With three tiles, you have three choices for the first tile, two for the
> second, and the last tile goes in the remaining spot. That makes six permutations. In general we multiply
> down to one and call that n factorial.

## 8. Letters and pieces of type (≈ 45 s) · `type_pieces`

**Visual.** box(example, "Example 2.3"). Compare a 10-letter string from a 26-letter alphabet with a row
of 10 labelled pieces drawn from 1,000 pieces per letter. Show $26^{10}$ letter strings and
$(26\,000)_{10}\approx26\,000^{10}>10^{44}$ sequences of physical pieces.

> From an alphabet of twenty-six letters, you can make twenty-six to the power ten strings of length ten.
> Now picture a printer with a thousand pieces of type for each letter. Two pieces may print the same letter,
> and they're still different pieces. Draw ten of those pieces without replacement. There are twenty-six
> thousand sub ten possible sequences of pieces. That's more than ten to the power forty-four.
> Compared with twenty-six thousand to the power ten, the difference is tiny. Taking out a few pieces
> barely changes the size of the pool.

## 9. Random samples (≈ 45 s) · `uniform_sample`, `survey_order`

**Visual.** box(definition, "Definition 2.1"). Use the two trays from chapter 6 and show
$n^{-r}=1/n^r$ and $1/(n)_r$. Example tags: $1/125$ with replacement and $1/60$ without replacement.

> A random sample here means every possible ordered sample has the same probability. To get that model,
> choose uniformly from what's available at each draw. If we return each of the five tiles, any particular
> three-draw sequence has probability one over a hundred twenty-five. If we keep the tiles out, each
> allowable sequence has probability one over sixty.

**Visual.** Note-style box titled “Remark”. Show a smoking survey with distinguishable respondents and tag
the third person interviewed. Then show $(n)_r/n^r\approx1$ when the sample is small relative to the population,
using the printer example as the visual reference.

> In a survey of smokers you may only report how many people said yes. Still, you can imagine interviewing
> them one by one. "The third person interviewed" is a particular person, and choosing uniformly at each draw
> gives every interview order the same weight. When the sample is small compared with the population,
> the two sampling procedures give nearly the same counts, just as they did for the printer.

## 10. Will a particular element appear? (≈ 65 s) · `include_without`, `include_with`

**Visual.** box(example, "Example 2.4"). Highlight one tile in a 5-tile population. Count the sequences that
miss it when drawing 3 without replacement: $1-24/60=3/5$. Cancel the common factors in
$1-(n-1)_r/(n)_r=1-(n-r)/n=r/n$.

> What's the chance that a particular tile appears? Draw three out of five without replacement. It's easier
> to count the sequences that miss our tile. Those draws have to come from the other four tiles, giving
> twenty-four miss sequences out of sixty. Subtract that fraction from one and you get three fifths.
> In the general ratio, the factors shared by the two products cancel. The chance of missing the tile is
> n minus r, divided by n. So the chance of including it is r over n.

**Visual.** Switch to replacement. Count misses with $(n-1)^r$ and all sequences with $n^r$. Show
$1-(1-1/n)^r$ and $1-(4/5)^3=61/125$ using the same tiles.

> Return whichever tile you draw, and the count changes. Each draw has four choices that miss our tile,
> so there are sixty-four miss sequences out of a hundred twenty-five. The inclusion chance drops to
> sixty-one over a hundred twenty-five. In general, the miss probability is one minus one over n, all
> raised to the power r. Subtract that from one to get the chance of seeing the tile at least once.

## 11. No repetition (≈ 55 s) · `no_repeat`, `random_digits`

**Visual.** Start with all $n^r$ ordered samples with replacement. Highlight the subset with no repeats,
then derive $p=(n)_r/n^r=(1-1/n)(1-2/n)\cdots(1-(r-1)/n)$ (2.3) by dividing each factor by $n$.

> Now keep replacement in the experiment, and ask whether all the draws happen to be different.
> Each repeat-free sequence could have come from drawing without replacement, so there are n sub r of them.
> Divide by n to the power r. You can divide each factor on top by n. The first factor becomes one.
> Then come one minus one over n, one minus two over n, and so on.

**Visual.** box(example, "Example 2.5"). Show 5 slots for digits 0 through 9 and
$(10)_5/10^5=0.3024$. Next to it, use the first 2,500 decimal digits of $e$ in 500 non-overlapping groups
of 5. Highlight the 150 groups with all digits different: $150/500=0.300$.

> Draw five random digits. Repeats are allowed, and only about thirty percent of the sequences have five
> different digits. For a comparison, take the first two thousand five hundred digits after the decimal point
> of e, in groups of five. A hundred fifty of those five hundred groups have all different digits.
> That's close to the random model for this test. The digits of e themselves come from a fixed number.

## 12. Accidents, dice and elevators (≈ 70 s) · `occupancy`, `accidents_dice`, `elevator`

**Visual.** box(example, "Example 2.6"). Drop $n$ labelled balls into $n$ cells. Highlight the arrangements
with each cell occupied, then show $n!/n^n$. Use a 7-day calendar and a fair six-sided die.
Show $7!/7^7\approx0.00612$ (about once in 163 weeks) and $6!/6^6\approx0.0154$.

> If the numbers of balls and cells match, filling every cell means putting exactly one ball in each.
> Each ball chooses a cell independently and uniformly. We count all arrangements by giving each ball n choices.
> The successful arrangements are the n factorial ways to put different balls in different cells.

> Imagine exactly seven accidents each week, with their days independently and uniformly assigned.
> Exactly one accident on each day is rare: about once in a hundred sixty-three weeks on average in this model.
> With six rolls of a fair die, seeing each face exactly once has probability about one and a half percent.

**Visual.** box(example, "Example 2.7"). Match 7 passengers to 10 floors. Show
$(10)_7/10^7=(10\cdot9\cdot8\cdot7\cdot6\cdot5\cdot4)/10^7=0.06048$.

> An elevator has seven passengers and stops at ten floors. Suppose each passenger chooses independently
> and all floors are equally likely. We want different floors, so the favourable count has ten choices for
> the first passenger, nine for the second, down to four for the last. Divide by ten to the power seven.
> The probability is roughly six percent.

## 13. The birthday problem (≈ 105 s) · `birthday_model`, `birthday_crossing`, `birthday_log`, `birthday_pairs`

**Visual.** box(example, "Example 2.8"). Sample $r$ birthdays with replacement from 365 dates. Mark assumptions
“Ignore leap days”, “Equal chance per day” and “Independent birthdays”. Derive
$p_r=(365)_r/365^r=\prod_{k=1}^{r-1}(1-k/365)$ (2.4).

> Imagine a room full of people. How many do you need before a shared birthday is more likely than none?
> Use a year with three hundred sixty-five days. Ignore leap days and seasonal differences, and treat the
> people's birthdays as independent. Count the opposite event first. For everyone's birthday to be different,
> the next person has to avoid every date we've already used. For the second person the factor is one minus
> one over three hundred sixty-five. For the third it's one minus two over three hundred sixty-five.
> Multiply these factors through the last person.

**Visual.** Animate the birthday curve for $r=1,\dots,60$, based on `birthday.svg`.
Mark $p_{22}\approx0.524$, $p_{23}\approx0.493$ and the crossing of $1/2$; then $p_{30}\approx0.294$.
At $r=23$, display the complement $1-p_{23}\approx0.507$.

> The chance of no match keeps falling as more people join. With twenty-two people it's still above one half.
> With twenty-three it's below one half for the first time. So a shared birthday is already slightly more likely
> than no shared birthday. With thirty people, the chance that everyone has a different birthday is under
> thirty percent.

**Visual.** Derive $\log p_r=\sum_{k=1}^{r-1}\log(1-k/365)\approx-\sum_{k=1}^{r-1}k/365=-r(r-1)/730$ (2.5).
For $r=30$ compare the approximation $e^{-870/730}\approx0.304$ with the exact-product value rounded to $0.294$.

> Here's a shortcut. Logs turn that long product into a sum. For a small x, the log of one minus x is close
> to minus x. Add the integers from one to r minus one, then divide by three hundred sixty-five and put a
> minus sign in front. With thirty people, this shortcut gives about zero point three zero four. The exact
> product gives about zero point two nine four.

**Visual.** Join 23 dots with $\binom{23}{2}=253$ lines, highlighting one line at a time before revealing the
crowded diagram. Show $1/365$ next to one pair, and
$\binom r2=r(r-1)/2$ beside the numerator in the log approximation.

> The same sum counts pairs of people. With twenty-three people there are two hundred fifty-three pairs,
> and each pair has a one in three hundred sixty-five chance of a match. We're checking every pair in the
> room, not just checking who shares your birthday. Adding the pair probabilities would count some rooms
> more than once, so use the product for the exact answer.

## 14. Code Lab (≈ 55 s) · `code`, `code_result`

**Visual.** code_cell with the code below and its exact output. Label the two results “Simulated” and “Exact (rounded)”.

```python
from fractions import Fraction
from math import prod
from random import Random

rng = Random(5)
people, days, trials = 23, 365, 100_000
matches = sum(
    len({rng.randrange(days) for _ in range(people)}) < people
    for _ in range(trials)
)
exact = 1 - prod(Fraction(days - k, days) for k in range(people))
print(f"{matches / trials:.4f} {float(exact):.4f}")
```

Output:
```
0.5065 0.5073
```

> Let's simulate a hundred thousand groups of twenty-three people in Python. The random generator picks a
> day for each person. A set keeps each day only once. If the set has fewer entries than there are people,
> we count a match in that group. For the exact answer, multiply the factors for all birthdays being different
> and take the complement.

> The simulation gives point five zero six five. The exact product gives point five zero seven three after
> rounding. Both put the chance just above one half. Try changing the number of people. With one extra person,
> every existing person gets a new partner to compare birthdays with.

## 15. Key ideas (≈ 40 s) · `recall`, `ideas`, `end`

**Visual.** key_ideas with the three items below, matching the site. Pause ≥ 5 s before revealing the items.
- Multiply the number of available choices at each step when that number is fixed for every preceding choice.
- An ordered sample of size $r$ from $n$ objects has $n^r$ possibilities with replacement and $(n)_r$ without
  replacement (Theorem 2.3).
- Without replacement, selecting all $n$ objects gives $n!$ permutations. In a uniform ordered sample, every
  admissible sequence has the same probability.

> Before we finish, pause and see if you can explain when to multiply and when a choice gets removed.

> Multiply the choice counts if each step has a fixed number of options. With replacement, the count stays the
> same at each draw. Without replacement, it drops by one. Draw everything without replacement and you have
> a permutation. In a uniform ordered sample, every allowable sequence has the same probability.

**Visual.** end_card: “Full proofs, exercises and runnable code” · “Link in the description” ·
“Next lesson: Subpopulations and partitions”.

> The full section and exercises are on Aram Code Lab. Next time we'll count subpopulations, where only
> membership matters. That will give us the binomial coefficients.

---

### Checked numbers (production notes; all computed in code)

- Dice recap: 2 six-sided dice give 36 ordered pairs, with 11 possible sums from 2 through 12. Sum 7 has 6 pairs
  and probability $6/36=1/6$, distinct from the incorrect shortcut $1/11$.
- Pair table: 2 shirts × 3 hats = 6 outfits. Three decisions with 3, 2 and 4 choices give 6 starter-main
  pairs and 24 meals, including when the lists of 2 mains differ.
- Example 2.1: 4 suits × 13 ranks = 52 cards. The 3-bulb switch and the indirect light each have 4 settings
  (0 through 3). Their 16 setting pairs include $(0,0)$, leaving 15 ways with light on. Three labelled
  balls in 3 cells give $3^3=27$. In 6 die rolls there are $6^6=46\,656$ sequences, of which $5^6=15\,625$
  avoid the ace (face 1). $1-(5/6)^6\approx0.665$ (about 66.5%), below $2/3$.
- Example 2.2: with 3 distinct flags and 3 poles, insertion slot counts are 3, 4 and 5, giving 60 displays.
- Ordered samples and permutations: with $n=5$, $r=3$, the counts are 125 and 60, and the probabilities per
  sample are $1/125$ and $1/60$. For empty or oversize draws without replacement, $(n)_0=1$, $(n)_r=0$ for
  integers $r>n$. The three-tile permutation example has $3\cdot2\cdot1=3!=6$ outcomes.
- Example 2.3 and Remark: $26^{10}=141\,167\,095\,653\,376$ ten-letter strings. With 1,000 pieces per letter,
  $n=26\,000$ and $(26\,000)_{10}/26\,000^{10}\approx0.998271$. Both piece-sequence counts exceed $10^{44}$.
- Example 2.4: a sample of 3 from 5 has $24$ miss sequences out of $60$ without replacement, giving
  inclusion probability $3/5$. With replacement there are $64$ misses out of $125$, giving $61/125$.
- Example 2.5: 5 draws from digits 0 through 9 have no-repeat probability $(10)_5/10^5=0.3024$ (about 30%).
  The first 2,500 decimal digits of $e$ make 500 groups of 5, with 150 successes ($0.300$).
- Examples 2.6–2.7: $7!/7^7\approx0.00612$ gives a reciprocal of about $163.4$ weeks, rounded to 163.
  $6!/6^6\approx0.0154$ (about 1.5%). Seven passengers and ten floors give $(10)_7/10^7=0.06048$ (about 6%).
- Example 2.8: use 365 days, plot $r=1,\dots,60$ and mark $p_{22}\approx0.524$, $p_{23}\approx0.493$ and
  $1-p_{23}\approx0.507$. The shared-birthday probability first exceeds $1/2$ at 23. At 30, the parameter
  $r(r-1)=870$ and $2\cdot365=730$, giving $e^{-870/730}\approx0.304$ against $p_{30}\approx0.294<0.30$.
  Each pair matches with probability $1/365$, and $\binom{23}{2}=253$.
- Code Lab: seed 5, 100,000 trials of 23 dates each from 365 days. Run as written, exact printed output
  `0.5065 0.5073`.
