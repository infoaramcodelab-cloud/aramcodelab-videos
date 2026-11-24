# Probability Theory · Lesson 4 — Subpopulations and Partitions

The narration and visual plan of the lesson. `script.py` holds the same narration split at the visual cues.
Voice: Orpheus, Tara. The published narration was sped up by 7 % after generation
(`ffmpeg -filter:a atempo=1.07`), and `audio/durations.json` holds the timings of the sped-up clips.
`check_numbers.py` checks every number in the narration and on screen.

Site section: 2.2 Subpopulations and partitions (slug `subpopulations-and-partitions`).
Next lesson: 3.1 Occupancy problems and the three statistics. Built with the lesson kit.

Colour code (as in Lesson 3):
- sample points and unused slots: muted; current choices and favourable outcomes: teal;
- the second group or sampling procedure: indigo;
- repeat draws, excluded cases and “Careful” cards: amber.

For 1440p, keep headings, formulas and labels inside padded cards. Give long formulas and exact deal counts their own rows.
Use suit initials C, S, H and D on cards. Build large counts and dense tables across successive reveals.

Chapters: Welcome · Forgetting the order · Choosing who stays · Poker ranks and suits · The senators' committee ·
Exactly k balls in one cell · Arrangements of two kinds · Shortest paths · Partitions into labelled groups ·
An ace for each bridge player · Each die face exactly twice · Four ways to sample · Code Lab · Key ideas
(timestamps come from the render)

---

## 1. Welcome (≈ 35 s) · `welcome`, `recap`

**Visual.** title_card("2.2", "Subpopulations and Partitions", lesson 4). Open a hand of cards and swap two of them.

> Welcome back. If I shuffle the cards already in my hand, I'm still holding the same cards. But if I swap one
> for a card from the deck, my hand changes. Today we'll count selections where only membership matters, then
> use that idea to split a whole population into groups. The same question comes up when you pick a committee
> or deal cards to several people. What has to change before we count the result as a new outcome?

**Visual.** Bring back the Lesson 3 trays with counts $n^r$ and $(n)_r$. Beside them, show the birthday curve
crossing one half between 22 and 23 people, with the caption “At 23, a shared birthday is more likely.”

> Last time, we counted ordered samples. With replacement we got n to the power r. Without replacement we got
> n sub r. Counting ordered dates helped us see why a shared birthday is already more likely than no match
> with twenty-three people. Let's start with those ordered counts and see what happens when we forget the order.

## 2. Forgetting the order (≈ 50 s) · `collapse_orders`, `choose_rule`

**Visual.** Arrange 5 population tiles A–E. Show the six ordered rows ABC, ACB, BAC, BCA, CAB, CBA, then fold
them into one tray labelled $\{A,B,C\}$. Group the $60$ ordered rows into stacks of $3!=6$, giving $10$ sets.

> Take three of these five tiles. A, B, C and C, A, B are different ordered samples. They give the same subset
> because they contain exactly the same tiles. Any three distinct tiles can be ordered in six ways. There are
> sixty ordered samples, so bundle them six at a time. We get ten subsets. Now try A, B, D. That belongs in a
> different bundle, because D has taken the place of C. The bundles are exactly the sets we want to count.

**Visual.** box(theorem, "Theorem 2.4"). Build $(n)_r=\binom nr\,r!$ from “Choose the set” and “Order the set”.
Then reveal
$\binom nr=\dfrac{(n)_r}{r!}=\dfrac{n(n-1)\cdots(n-r+1)}{1\cdot2\cdots r}$ (2.6).

> In general, every subset of size r has exactly r factorial orderings. Each ordered sample comes from just
> one subset. So we can count the ordered samples by choosing a subset first and ordering it second.
> Divide the ordered count by r factorial. The result is called n choose r, the binomial coefficient.

## 3. Choosing who stays (≈ 45 s) · `choose_complement`, `choose_factorial`

**Visual.** Start with 5 tiles. Highlight 2 staying in teal and 3 leaving in indigo. Reverse which group is
being chosen while preserving membership. Show $\binom52=\binom53=10$ on two balanced cards.

> Say two of five people stay and the other three leave. Tell me who stays, and I know exactly who leaves.
> Tell me who leaves, and I can recover the other group. Every choice on one side has one partner on the other.
> That's why five choose two and five choose three are both ten.

**Visual.** Extend the numerator of (2.6) by its missing factorial and divide by the same factor. Show
$\binom nr=\binom n{n-r}$, $\binom nr=\dfrac{n!}{r!(n-r)!}$, and $\binom n0=1, 0!=1$ together as (2.7).
Beside the formula use an empty tray and $\binom50=\binom55=1$.

> The falling product is the beginning of n factorial. Multiply top and bottom by the factorial of n minus r to
> get n factorial over r factorial times the factorial of n minus r. There is one way to take nothing, just as there
> is one way to take everything. Setting zero factorial to one keeps the formula working at both ends.

## 4. Poker ranks and suits (≈ 55 s) · `poker_hands`, `poker_distinct`, `bridge_ranks`

**Visual.** box(example, "Example 2.9"). Show a five-card hand using rank and suit initials, then shuffle
the positions. Put $\binom{52}{5}=2\,598\,960$ on its own row.

> A poker hand has five cards from a standard deck of fifty-two. The deal order makes no difference once
> the cards are in your hand. Every five-card subset is equally likely in a fair deal. That's about two
> point six million hands. You could count the deal as a sequence first, but each hand would appear once
> for every possible order of its cards. The binomial coefficient does that division for us.

**Visual.** Use 13 rank tiles, highlight 5 distinct ranks, then reveal a row of 4 suit choices for each
chosen rank. Show $\binom{13}{5}=1\,287$, $4^5=1\,024$, their product $1\,317\,888$, and
$\binom{13}{5}4^5/\binom{52}{5}\approx0.5071$.

> To get five different ranks, choose the five ranks first. For each chosen rank there are four suits.
> Each completed hand tells us exactly which ranks and suits we picked. Multiply the rank count by four
> to the power five and divide by the total. The chance is a little over one half.

**Visual.** Extend to a single bridge hand. Show one rank slot for each of the 13 ranks on two lines.
Use $\binom{52}{13}=635\,013\,559\,600$ and $4^{13}/\binom{52}{13}\approx0.0001057$.

> A single bridge hand has thirteen cards. There are about six hundred thirty-five billion possible
> hands. To get thirteen different ranks you need one card of every rank. Each rank still has four
> possible suits. Divide four to the power thirteen by the number of hands. That's about one chance
> in ten thousand.

## 5. The senators' committee (≈ 55 s) · `state_absent`, `all_states`

**Visual.** box(example, "Example 2.10"). Show 50 state tiles in five rows of ten, two senator dots per tile.
Highlight one state and mute both its dots. Point to the remaining 98 senators and the 50-seat committee.
Show $q=\binom{98}{50}/\binom{100}{50}=(50\cdot49)/(100\cdot99)\approx0.24747$ and
$1-q\approx0.753$ on separate rows.

> Imagine fifty states with two senators each. We pick a committee of fifty senators uniformly. Will your
> state have a seat? Count the opposite case first. Both your senators are left out, and the committee
> comes entirely from the other ninety-eight. The probability of missing your state is about one quarter.
> So the chance of representation is about three quarters. There's a quick way to see that quarter.
> Half the senators stay off the committee, so your first senator stays off with chance fifty out of a hundred.
> Then forty-nine of the other ninety-nine senators stay off, so your second one does too with chance
> forty-nine out of ninety-nine. Multiply, and you get just under one quarter.

**Visual.** In the same grid, light one dot in each state. Show $2^{50}$ as the favourable count and
$2^{50}/\binom{100}{50}\approx1.1\times10^{-14}$ as the probability.

> Could every state have a seat? With fifty seats that means exactly one senator per state. Each state
> offers two choices, giving two to the power fifty such committees. That sounds huge until you divide
> by the number of unrestricted committees. The chance is around one in ninety trillion, even though
> any single state is quite likely to be represented. Getting every state in is a different question
> from getting any one particular state in.

## 6. Exactly k balls in one cell (≈ 55 s) · `cell_count`, `cell_formula`

**Visual.** box(example, "Example 2.11"). Show 3 labelled balls and 3 cells. Outline one cell in teal and
choose 2 of the balls for it. Animate the third ball taking either remaining cell.
Show $\binom32\cdot2^1=6$ out of $3^3=27$, so $6/27=2/9$.

> Drop three labelled balls into three cells independently and uniformly. What's the chance that this
> particular cell gets exactly two balls? Choose which two go there. That's three possible pairs.
> The remaining ball has two other cells to choose from. Six arrangements work out of twenty-seven,
> so the probability is two ninths. Keep your eye on the outlined cell. If we were looking for two balls
> in any cell, we would be counting a different event.

**Visual.** Replace the example counts with $r$, $n$ and $k$. Reveal the count of choices for the highlighted
cell and the count for the other cells before dividing by $n^r$. Show
$p_k=\binom rk\dfrac{(n-1)^{r-k}}{n^r}=\binom rk\left(\dfrac1n\right)^k\left(1-\dfrac1n\right)^{r-k}$ (2.8).

> In general, choose which k of the r balls land in the given cell. Each remaining ball has n minus one
> choices. Divide by n to the power r to get the probability. The product form tells the same story.
> Each chosen ball hits the cell with probability one over n, and each remaining ball misses it.
> This is exactly what the binomial distribution counts.

## 7. Arrangements of two kinds (≈ 50 s) · `two_kinds`, `same_colour_flags`

**Visual.** Put 2 labelled alpha tiles and 3 labelled beta tiles into a row of 5 slots. Keep the alpha
and beta positions fixed while permuting labels within both colours. Remove labels to reveal one row.
Show $5!/(2!3!)=10$, then
$\dfrac{(p+q)!}{p!q!}=\binom{p+q}{p}=\binom{p+q}{q}$ (2.9).

> Now arrange two alpha tiles and three beta tiles. Give every tile a number first. We could order the five
> labelled tiles in five factorial ways. For every colour pattern, two factorial orderings of the alpha
> labels and three factorial orderings of the beta labels give that same pattern. Divide by both factorials.
> You can also just choose the two alpha positions. Once those positions are fixed, the beta tiles fill
> every empty slot. Choosing the beta positions instead must give the same count, by symmetry.

**Visual.** Bring back the 3 poles and 3 flags from Lesson 3. Use 2 same-colour flags and 1 flag of the
other colour. Briefly swap the matching flags' temporary labels. Show
$n(n+1)\cdots(n+r-1)/(p!q!)$ and $3\cdot4\cdot5/(2!1!)=30$.

> The same idea works with flags. On three poles there are sixty displays of three distinguishable flags.
> Now make two flags the same colour. Exchanging their labels leaves the display unchanged, wherever they
> hang. Divide the old count by two factorial times one factorial. That leaves thirty displays.

## 8. Shortest paths (≈ 55 s) · `lattice_word`, `path_count`

**Visual.** box(example, "Example 2.12"). Use the grid and endpoints from `lattice-path.svg`. On the 5 × 3
grid, trace the highlighted path and spell the move word R U R R U R R U beneath it, one tile per step.
Teal for R, indigo for U. Illustrate why any backward move increases the length.

> Walk along the grid lines from the lower left corner to the upper right. You need five moves right and
> three moves up. A step left or down makes you spend another step getting back. So a shortest path is
> exactly eight moves long. We can read a path as a word made from R and U. Follow the highlighted path
> with your finger. Each time a segment turns, the next letter tells you which direction to go.

**Visual.** Highlight the 3 U slots of the 8-letter word. Show $\binom83=56$ and $1/56$ for one specified
path when all shortest paths are sampled uniformly. Then show an 8 × 8 chessboard and
$\binom{16}{8}=12\,870$.

> Choose the three positions for the up moves. The other positions have to be right moves, and the word
> determines the path. Eight choose three gives fifty-six. If we choose uniformly among these shortest paths,
> the highlighted one has probability one in fifty-six. Across a chessboard, eight moves each way give
> twelve thousand eight hundred seventy shortest paths. We'll use paths like these in random walks.

## 9. Partitions into labelled groups (≈ 55 s) · `partition_formula`, `partition_cancel`

**Visual.** box(theorem, "Theorem 2.5"). Deal 5 tiles into labelled trays A, B and C with sizes 2, 2 and 1.
Show $\binom52\binom32\binom11=10\cdot3\cdot1=30$. Swap the whole contents of A and B, then swap the
positions inside one tray.

> Divide five people among three teams. Pick two for team A from all five, then two for team B from the
> remaining three. The last person goes to team C. Ten choices times three choices times one gives thirty.
> Switching the membership of teams A and B changes the partition. Rearranging the names within one team
> keeps its membership the same.

**Visual.** Reveal $\binom n{r_1}\binom{n-r_1}{r_2}\cdots$. On the next row, expand the first two factors into
$\dfrac{n!}{r_1!(n-r_1)!}\cdot\dfrac{(n-r_1)!}{r_2!(n-r_1-r_2)!}\cdots$.
Mark the matching intermediate factorials, then cancel through the last group. Show
$\dfrac{n!}{r_1!r_2!\cdots r_k!}$ with $r_1+\cdots+r_k=n$ and $r_i\ge0$ (2.10).
Add an empty labelled tray and the note $0!=1$.

> For more teams, keep choosing each team from whoever remains. Expand each binomial coefficient into
> factorials. The factorial for the people left after one choice cancels with the numerator of the next.
> The result is n factorial over the product of all the group size factorials. An empty group is allowed
> and contributes a factor of one. Notice what the denominator does. It removes all the ways of ordering
> people within their groups, while keeping the group labels attached.

## 10. An ace for each bridge player (≈ 55 s) · `bridge_deals`, `bridge_aces`

**Visual.** box(example, "Example 2.13"). Show four labelled stacks of 13 cards with the top card visible.
Order inside each hand fades out. Show $D=52!/(13!)^4$ with its own full-width exact count row
$53\,644\,737\,765\,488\,792\,839\,237\,440\,000$; add $D\approx5.36\times10^{28}$ below.

> Now deal all fifty-two cards to four bridge players. Each hand has thirteen cards. The hands belong to
> different players, so swapping two hands gives a different deal. The count is fifty-two factorial over
> thirteen factorial to the fourth. That's about five times ten to the twenty-eight possible deals.
> We can build one deal by choosing a hand for the first player, then choosing from the remaining deck
> for the second, and continuing until everybody has a hand.

**Visual.** Draw the four aces as rank A plus suit initials. Send one to each player, followed by four stacks
of 12 non-aces. Reveal $4!=24$, then $48!/(12!)^4$. Use two rows for the probability
$\dfrac{24\,[48!/(12!)^4]}{52!/(13!)^4}=\dfrac{24\cdot48!\cdot13^4}{52!}\approx0.105$.

> For everyone to get an ace, first assign the four aces to the four players. There are twenty-four ways.
> Then split the forty-eight remaining cards into four hands of twelve. Multiply those counts, then divide
> by all the deals. The chance that each player gets one ace is a little over one in ten.

## 11. Each die face exactly twice (≈ 45 s) · `dice_pairs`, `dice_chance`

**Visual.** box(example, "Example 2.14"). Roll 12 labelled dice. Sort a successful roll into six labelled
groups, two dice showing each face from 1 to 6. Swap the two dice in any group and keep the roll fixed.
Show $12!/(2!)^6=7\,484\,400$.

> Roll twelve fair dice and keep track of which die is which. Suppose every face appears twice. We need
> to split the dice into six labelled groups of two. The group label tells us the face on both dice.
> Inside each pair, switching the order describes the same roll. Divide twelve factorial by two factorial
> to the sixth.

**Visual.** Put the favourable count above $6^{12}=2\,176\,782\,336$ and derive
$12!/[(2!)^6\cdot6^{12}]=12!/[2^6\cdot6^{12}]\approx0.003438$.

> Each die has six possible faces, so there are six to the power twelve equally likely outcomes.
> Divide the successful count by that total. The probability is about a third of one percent. Even
> though each face is expected to show up twice on average, seeing exactly that balance is rare.
> A roll with a third six and a missing face still belongs in the total, even though it fails our test.

## 12. Four ways to sample (≈ 65 s) · `summary_without`, `summary_with`

**Visual.** box(note, "Summary"). Fill the 2 × 2 table a cell at a time. Columns are “Order matters” and
“Order does not matter”. Rows are “Without replacement” and “With replacement”. Start with the top row.
On separate strips, use 3 tiles A, B, C and 2 draws. Show 6 ordered results folding into 3 subsets.

| | Order matters | Order does not matter |
|---|---|---|
| Without replacement | $(n)_r$ | $\binom nr$ |
| With replacement | $n^r$ | $\binom{n+r-1}{r}$ |

> Ask two questions before you count. Does order matter? Can an element repeat? Draw two of three tiles
> without replacement. If order matters, there are six sequences. Forget the order and those six fold
> into three subsets. Those are the falling product and the binomial coefficient. Say you drew A, then B.
> Is B, then A, the same result for you? If it is, count in the right column. If not, use the left one.

**Visual.** Fill the bottom row. Show 9 ordered two-draw results, then the 6 sorted outcomes AA, AB, AC,
BB, BC, CC. For AB, draw one dot, a divider, one dot, a divider. Use two dots and two dividers, showing
$r$ dots and $n-1$ dividers in general, then $\binom42=6$.

> Put the tiles back and you can repeat a letter. There are nine ordered sequences. If only the counts of
> A, B and C matter, there are six outcomes. To see the general rule, use two dividers to make three groups
> and put a dot in the appropriate group for each draw. An empty group means that tile was never drawn.
> Choose the dot positions among all four positions. With r dots and n minus one dividers, that's
> n plus r minus one choose r. We'll meet these dots and dividers again next time.

## 13. Code Lab (≈ 45 s) · `code`, `code_result`

**Visual.** code_cell with the program below and its exact output. Put “Simulated” and “Exact (rounded)” in
side-by-side result cards. Match each slot block to one hand as in Example 2.13.

```python
from fractions import Fraction
from math import comb
from random import Random

rng = Random(4)
trials = 100_000
hits = sum(len({slot // 13 for slot in rng.sample(range(52), 4)}) == 4
           for _ in range(trials))
exact = Fraction(13**4, comb(52, 4))
print(f"{hits / trials:.6f} {float(exact):.6f}")
```

Output:
```
0.105010 0.105498
```

> Let's simulate one hundred thousand bridge deals. We only need the positions of the four aces. Imagine
> the deck laid out in four blocks of thirteen slots, one block per player. Choose four distinct slots at
> random. Every set of four slots is equally likely in a fair deal. Integer division by thirteen identifies the block. We count a success when the aces occupy all
> four blocks.

> For the exact check, choose one slot in each block, then divide by the number of ways of choosing any
> four slots. The simulated and exact results both land just above one in ten. The exact expression looks
> different from the one with factorials, but it counts the same event.

## 14. Key ideas (≈ 40 s) · `recall`, `ideas`, `end`

**Visual.** key_ideas with the three points below. Pause ≥ 5 s before revealing them.
- For an unordered subset, divide the ordered count by $r!$, giving $\binom nr=(n)_r/r!$.
- Choosing who stays and choosing who is left out give the same count.
- For labelled groups with sizes summing to $n$, divide $n!$ by the product of their size factorials.

> Before we finish, try to explain why we divide by a factorial. Think of a hand of cards or of a team
> whose members can stand in any order.

> We divide by r factorial because every subset has that many orderings. Choosing who stays is equivalent
> to choosing who leaves. When we split a population into labelled groups, divide by a factorial for each
> group. Every arrangement inside a group still gives the same membership.

**Visual.** end_card: “Full proofs, exercises and runnable code” · “Link in the description” ·
“Next lesson: Occupancy problems and the three statistics”.

> The full section and exercises are on Aram Code Lab. Next time we'll look at occupancy problems.
> We'll ask how the way we model balls and cells changes the probabilities.

---

### Checked numbers (production notes; all computed in code)

- Lesson 3 recap: in the uniform 365-day birthday model, the probability of a shared birthday is below $1/2$
  at 22 people and above $1/2$ at 23.
- Theorem 2.4: 5 tiles taken 3 at a time give 60 ordered samples, six orderings per subset and 10 subsets.
  $\binom52=\binom53=10$ and $\binom50=\binom55=0!=1$.
- Example 2.9: 13 ranks × 4 suits = 52 cards. $\binom{52}{5}=2\,598\,960$ (about 2.6 million);
  $\binom{13}{5}=1\,287$, $4^5=1\,024$, $1\,317\,888$ favourable hands, probability $0.5071$ rounded.
  Bridge rank comparison: $\binom{52}{13}=635\,013\,559\,600$ (about 635 billion);
  $4^{13}/\binom{52}{13}\approx0.0001057$, about one in 10,000.
- Example 2.10: 50 states with 2 senators each, 100 senators total, 98 outside the selected state and 50
  committee seats. $q=(50\cdot49)/(100\cdot99)=49/198\approx0.24747$; $1-q=149/198\approx0.753$.
  All states represented: $2^{50}/\binom{100}{50}\approx1.1\times10^{-14}$, about one in 90 trillion.
- Example 2.11: 3 balls into 3 cells with exactly 2 in one specified cell of hit probability $1/3$. $\binom32=3$ pairs, 2 choices for
  the remaining ball, $6$ favourable arrangements of $27$ and probability $2/9$.
- Two kinds: 2 alpha tiles and 3 beta tiles yield $5!/(2!3!)=10$. For 3 flags on 3 poles, with colour
  multiplicities 2 and 1, $3\cdot4\cdot5=60$ labelled displays and $60/(2!1!)=30$ colour displays.
- Example 2.12: $5\times3$ grid, 5 R moves and 3 U moves, 8 total, $\binom83=56$ paths. The word
  R U R R U R R U ends at $(5,3)$ and has probability $1/56$ under uniform shortest-path sampling.
  On the $8\times8$ chessboard, $\binom{16}{8}=12\,870$.
- Theorem 2.5: sizes 2, 2 and 1 give $10\cdot3\cdot1=30$ partitions of 5; adding an empty group leaves 30.
- Example 2.13: $52!/(13!)^4=53\,644\,737\,765\,488\,792\,839\,237\,440\,000\approx5.36\times10^{28}$
  (roughly $5\times10^{28}$ aloud). Four aces give $4!=24$ assignments; the 48 other cards go into four groups
  of size 12. The exact probability is $2197/20825\approx0.105$.
- Example 2.14: 12 dice with face labels 1 through 6, group size 2 and expected count 2 per face; $6^{12}=2\,176\,782\,336$,
  $12!/(2!)^6=7\,484\,400$, probability $1925/559872\approx0.003438$ (about one third of one percent).
- Summary: 3 tiles, 2 draws. Without replacement: 6 ordered and 3 unordered. With replacement: 9 ordered
  and 6 unordered; two dots and two dividers give $\binom42=6$.
- Code Lab: seed 4, 100,000 trials; four different slots among 52, four blocks of 13. The exact slot
  probability is $13^4/\binom{52}{4}=2197/20825$. Run as written, output `0.105010 0.105498`.
