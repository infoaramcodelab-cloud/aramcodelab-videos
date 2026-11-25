# Probability Theory · Lesson 5 — Occupancy Problems and the Three Statistics

The narration and visual plan of the lesson. `script.py` holds the same narration split at the visual cues.
Voice: Orpheus, Tara. The published narration was sped up by 7 % after generation
(`ffmpeg -filter:a atempo=1.07`), and `audio/durations.json` holds the timings of the sped-up clips.
`check_numbers.py` checks every number in the narration and on screen.

Site section: 3.1 Occupancy problems and the three statistics (slug `occupancy-problems-and-the-three-statistics`).
Next lesson: 3.2 The hypergeometric distribution and waiting times. Built with the lesson kit.

Colour code (as in Lesson 4):
- sample points and unused slots: muted; current choices and favourable outcomes: teal;
- the second group or sampling procedure: indigo;
- repeat draws, excluded cases and “Careful” cards: amber.

For 1440p, keep headings, formulas and labels inside padded cards. Split wide equations into successive reveals.
Draw dice faces and pips as shapes. Use paired text and colour labels for the probability models.

Chapters: Welcome · Occupancy numbers · Stars and bars · No empty cells · Dice and derivatives ·
Labelled balls and probability · Count cells, then count balls · All fifteen configurations · The three statistics ·
One pattern, three probabilities · Runs · The lunch counter · Code Lab · Key ideas
(timestamps come from the render)

---

## 1. Welcome (≈ 35 s) · `welcome`, `recap`

**Visual.** title_card("3.1", "Occupancy Problems and the Three Statistics", lesson 5). Reprise the dot-divider
strip from Lesson 4, then put its dots into cells. Keep the colour of the dots and dividers as they move.

> Welcome back. Last time we promised to come back to these dots and dividers. Here they are. The dots are
> balls, and the dividers tell us where one cell ends and the next begins. This little picture will help us
> count distributions, compare ways of assigning probabilities, and even make sense of where people sit.

**Visual.** Bring back the Lesson 4 Summary 2 × 2 table. Outline the unordered columns, then highlight
$\binom nr$ and $\binom{n+r-1}{r}$ in turn. Beside it, show the labelled groups from Lesson 4 and
$n!/(r_1!\cdots r_k!)$.

> Remember n choose r, for picking a subset. When the order of draws matters, we use the ordered counts
> from the other column. And when we split a population into labelled groups, we use a multinomial coefficient.
> Today we'll start in the unordered column with replacement, then bring back the multinomial when we need labels.

## 2. Occupancy numbers (≈ 50 s) · `count_cells`, `forget_labels`

**Visual.** Use 5 labelled cells. Place 8 balls in them with occupancies $(3,1,0,0,4)$, matching
`stars-bars.svg`. Write a count under each cell and reveal $3+1+0+0+4=8$. Generalise underneath to
$r_1+\cdots+r_n=r,\quad r_k\ge0$ (3.1).

> Suppose we put eight balls into five cells. Read the counts from left to right. Three, one, zero, zero, four.
> Those are the occupancy numbers. Empty cells get a zero, and every ball belongs to exactly one cell.
> So the numbers are nonnegative integers and they add up to the number of balls. This same record works
> for accidents per weekday, birthdays per date, or dice counted by face.

**Visual.** Give the balls temporary letters. Exchange two balls in different occupied cells, leaving the counts
unchanged. Then slide one ball to an empty cell and highlight the changed entries.

> If we only record the counts, exchanging two balls leaves the record alone. Moving one ball into an empty cell
> changes the record. Watch the second count drop to zero as its ball moves to the third cell.
> The total stays at eight because we only moved a ball. The positions of the cells still matter. A zero in one position means a different cell is
> empty than a zero somewhere else. So our outcome is a whole vector of counts in cell order.

## 3. Stars and bars (≈ 55 s) · `make_symbol`, `count_symbols`

**Visual.** box(theorem, "Theorem 3.1"). Flatten the 5 cells into `|***|*|||****|`. Tint the two outer bars
muted and the four inner ones indigo. Keep the occupancies under the gaps. Lift the two outer bars off the strip,
leaving 12 movable positions.

> Turn each ball into a star and put a bar at each cell boundary. The stars between adjacent bars belong to one
> cell. Two bars next to each other mark an empty cell. Read between the bars and you can recover the counts.
> Start from the counts and you can rebuild the same symbol. That means every valid symbol represents exactly
> one occupancy vector. In our picture the third and fourth cells are empty, so the strip has three
> bars in a row. The two spaces between them are exactly where those two zeros come from.

**Visual.** Reveal
$A_{r,n}=\binom{n+r-1}{r}=\binom{n+r-1}{n-1}$ (3.2), then
$\binom{12}{8}=\binom{12}{4}=495$. Outline the 8 star positions and then the 4 complementary bar positions.

> The first and last bars stay fixed. Inside, eight stars and four bars occupy twelve positions. Choose the
> eight positions for the stars, or choose the four positions for the bars. Either way gives four hundred
> ninety-five. In general, the count is n plus r minus one choose r, which also equals n plus r minus one
> choose n minus one.

## 4. No empty cells (≈ 45 s) · `bars_in_gaps`, `reserve_one`

**Visual.** Return to the same Theorem 3.1 box, part (ii). Lay out 8 stars with 7 clearly marked internal gaps.
Drop the 4 inner bars into distinct gaps. Leave the two outer bars fixed and show $\binom74=35$.

> Now require a ball in every cell. If we put two bars together, the cell between them is empty. Instead, line
> up the stars and put each inner bar into a different gap between stars. Eight stars give seven gaps.
> Choose four of those gaps and you get thirty-five distributions. For r balls and n cells, that's r minus one
> choose n minus one.

**Visual.** Set one star aside in each of the 5 cells. Move the remaining 3 stars into a separate row.
Show $A_{r-n,n}=\binom{r-1}{n-1}$ when $r\ge n$, and mark the case $r<n$ with an amber “Impossible” card.

> Here's the same count from the other direction. Give every cell one ball first. With eight balls and five
> cells, that leaves three to place freely. We can use the original rule on those leftover balls and get the
> same answer. If there are fewer balls than cells, there's no way to start by giving each cell one.

## 5. Dice and derivatives (≈ 55 s) · `dice_outcomes`, `derivative_orders`

**Visual.** box(example, "Example 3.1"). Roll 3 identical dice, drawn with pips. Sort the faces into six
labelled cells using the example roll $(2,2,5)$. Show the occupancy vector $(0,2,0,0,1,0)$, then
$\binom{r+5}{5}$ and $\binom85=56$.

> Roll three dice and record how many ones, twos, and so on you see. If two dice show two and the other shows
> five, that record is the same whichever die shows five. We have three balls and six face cells.
> Five dividers go with the three stars, so eight choose five gives fifty-six different records. This counts
> records, and we'll see in a moment why their probabilities can differ.

**Visual.** Use three cells labelled $x,y,z$. Sort the differentiation tiles $x,y,x,z$ into counts $(2,1,1)$.
Then show the counts $\binom64=15$ and $\binom75=21$ on separate cards.

> The same rule even counts partial derivatives of a smooth function. The cells are the variables, and a star
> records one differentiation with respect to a variable. You can switch the order of the differentiations
> without changing the result, so only the counts matter. For instance, differentiating twice with respect to x and
> once each with respect to y and z gives the same mixed derivative wherever the x steps occur. For three variables there are fifteen possible
> choices of counts at fourth order and twenty-one at fifth order.

## 6. Labelled balls and probability (≈ 45 s) · `fixed_vector`, `mb_probability`

**Visual.** Put 3 labelled balls into 3 labelled cells, with counts $(2,1,0)$. Show the 3 assignments with
this exact cell order beside the full 27-placement grid from Lesson 1.

> Now give the balls their labels back. Suppose each ball independently chooses a cell uniformly. Three
> balls in three cells give twenty-seven placements of equal probability. To get exactly two in the first
> cell and one in the second, choose which ball goes to the second cell. There are three choices.
> That particular vector has probability three over twenty-seven, or one ninth.

**Visual.** Partition the labelled balls into cell groups of sizes $r_1,\dots,r_n$. Derive
$\dfrac{r!}{r_1!\cdots r_n!}\,n^{-r}$ (3.3). Place “Maxwell–Boltzmann” beside the formula and keep
the fixed-order example visible as a small comparison card.

> In general, a placement with specified occupancies is a partition of the labelled balls into groups.
> The cells are the group labels. So the favourable count is r factorial over the product of the occupancy
> factorials. Divide by n to the power r for the probability. This is the Maxwell–Boltzmann model.
> Equal chances for placements can give different chances for their occupancy vectors.

## 7. Count cells, then count balls (≈ 55 s) · `choose_cell_roles`, `assign_balls`

**Visual.** box(example, "Example 3.2"). Lay out 7 labelled cells. Show the target
$(2,2,1,1,1,0,0)$, then permute their roles. Label the role groups “Double”, “Single”, “Empty”.
Show $7!/(2!3!2!)=210$.

> Put seven labelled balls into seven cells. We want two double cells, three single cells, and two empty cells.
> This time we accept those counts in any order. First decide which cells have each role. Partition the seven
> cells into groups of sizes two, three and two. That gives two hundred ten choices of cell roles.
> For example, the first two cells could be the doubles, the next three the singles, and the last two empty.
> So far, no ball has moved.

**Visual.** Freeze one cell-role assignment. Deal 7 labelled balls into the marked cells. Reveal
$7!/(2!2!1!1!1!0!0!)=1\,260$, then $210\cdot1\,260=264\,600$.
Finish on $264\,600/7^7\approx0.3213$ (3.4), with the two multinomial factors on individual rows.

> Now freeze those roles and choose which balls go into each cell. Divide seven factorial by the factorials
> of the individual occupancies. That gives one thousand two hundred sixty placements for each choice of roles.
> Multiply the two counts, then divide by seven to the power seven. The probability is about
> zero point three two one three. We used the multinomial once on cells and once on balls.

## 8. All fifteen configurations (≈ 45 s) · `configuration_table`, `even_and_typical`

**Visual.** Reveal the entire table in two padded columns, 8 rows and 7 rows. Animate the rows in the order below.
Use small occupancy chips and six-decimal probability labels. Once the full table is visible, highlight the
most probable row in teal and the perfectly even row in amber.

| Occupancies up to cell order | Probability |
|---|---:|
| 2,2,1,1,1,0,0 | 0.321295 |
| 3,2,1,1,0,0,0 | 0.214196 |
| 2,1,1,1,1,1,0 | 0.128518 |
| 2,2,2,1,0,0,0 | 0.107098 |
| 3,1,1,1,1,0,0 | 0.107098 |
| 4,1,1,1,0,0,0 | 0.035699 |
| 3,2,2,0,0,0,0 | 0.026775 |
| 4,2,1,0,0,0,0 | 0.026775 |
| 3,3,1,0,0,0,0 | 0.017850 |
| 1,1,1,1,1,1,1 | 0.006120 |
| 5,1,1,0,0,0,0 | 0.005355 |
| 4,3,0,0,0,0,0 | 0.001785 |
| 5,2,0,0,0,0,0 | 0.001071 |
| 6,1,0,0,0,0,0 | 0.000357 |
| 7,0,0,0,0,0,0 | 0.000008 |

> Repeat the two counts for every possible pattern. There are fifteen rows. Each placement belongs to exactly
> one row, so the exact probabilities add to one. The table rounds each row separately. Compare the first
> two rows. Each has the same total number of balls, but a cell with three balls changes both the cell
> roles and the number of ways we can fill them.

> The most likely pattern is the one we just counted. The perfectly even pattern is much rarer. It has
> probability around zero point zero zero six one. Equal chances for the cells can still leave several cells
> empty, because there are many more labelled placements that produce those uneven results.

## 9. The three statistics (≈ 65 s) · `mb_model`, `be_model`, `fd_model`

**Visual.** Show physical states as labelled cells. Use a first card titled “Maxwell–Boltzmann”. Show labelled
particles selecting cells independently, with $n^r$ equally likely placements and the weight (3.3).

> In statistical mechanics, we use cells to represent the states a particle can occupy. Maxwell–Boltzmann counts
> placements of distinguishable particles. You can follow the label on each particle and see where it goes.
> It's the classical model, and it can approximate a dilute gas. For identical quantum particles, counting
> permutations of labels this way doesn't give their exact statistics.

**Visual.** Turn the labelled particles into identical stars. A card titled “Bose–Einstein” shows equally
weighted occupancy vectors, including a cell with several stars. Reveal $1/A_{r,n}$.

> For Bose–Einstein, count each occupancy vector just once, and give the vectors equal probabilities in
> this model. Several particles can share a state. Photons are an example. Some composite particles, including
> atoms and nuclei with integer spin, also behave this way.

**Visual.** A card titled “Fermi–Dirac” locks a cell once it is occupied. Show $r\le n$ and
$\binom nr$ possible sets of occupied cells, with weight $1/\binom nr$.

> Fermi–Dirac allows at most one particle in each state. In our model the set of occupied cells is a
> uniformly chosen subset. Electrons, protons and neutrons obey this kind of statistics. The rule tells
> us which arrangements are allowed. It still takes experience to tell us which model describes nature.

## 10. One pattern, three probabilities (≈ 45 s) · `three_probabilities`, `misprints`

**Visual.** box(example, "Example 3.3"). Show 5 cells and 3 stars in cells 1, 3 and 4,
giving $(1,0,1,1,0)$. Reveal three cards side by side, using short headings and one formula per card.
- Maxwell–Boltzmann: $3!/5^3=6/125$.
- Bose–Einstein: $1/\binom73=1/35$.
- Fermi–Dirac: $1/\binom53=1/10$.

> Use five cells and three particles, with one particle in the first, third and fourth cells. With labels,
> the three particles can swap places among those cells. That gives six placements out of a hundred
> twenty-five. With Bose–Einstein, this vector is one out of thirty-five. With Fermi–Dirac, this set of
> occupied cells is one out of ten. The picture stays the same while the probabilities change.
> What changes from card to card is the set of outcomes we give equal chances to.

**Visual.** Replace the cells with letter positions on a printed line. Mark three positions with an amber
misprint indicator, and show that each position records at most one mark.

> Think of misprints on a printed page. When we mark each letter position as correct or misprinted,
> there's room for at most one mark per position. That gives the same kind of occupancy restriction
> as Fermi–Dirac. Equal chances for the marked sets would be a further modelling assumption.

## 11. Runs (≈ 60 s) · `find_runs`, `run_count`

**Visual.** Build the sequence AAAB AAB BBA as a continuous strip, then bracket its maximal blocks
AAA, B, AA, BBB, A. Reveal their lengths $(3,1,2,3,1)$. Use teal for A and indigo for B.

> A run is a block of consecutive equal letters, extended as far as it can go. Here the first three A's
> make one run. The next B starts a new one, and later A's start another. The run lengths are three,
> one, two, three, one. Runs of A and B alternate, so neither kind can have more than one extra run.

**Visual.** box(property, "Property 3.1"). Show $n_1$ nonempty A groups and $n_1+1$ nonempty B groups,
interleaved with B at both ends. Reveal
$\binom{a-1}{n_1-1}\binom{b-1}{n_1}$. For $a=3$, $b=4$, $n_1=2$ show
$\binom21\binom32=2\cdot3=6$.

> Count arrangements with n one A runs and one more B run. The extra B run means the sequence starts and
> ends with B. Now split the A letters into nonempty blocks, and do the same for B. The no-empty-cells
> rule counts the lengths for each kind, and we multiply. With three A's and four B's, two A runs give
> two choices of A lengths and three choices of B lengths. That's six sequences.

## 12. The lunch counter (≈ 60 s) · `counter_runs`, `counter_probability`

**Visual.** box(example, "Example 3.4"). Draw 16 seats and mark the observed sequence
`EOEEOEEEOEEEOEOE`. Bracket the 5 singleton occupied runs and 6 empty runs. Highlight the empty seats at
both ends, then move an occupied seat to an end briefly to show that the maximum needs both ends empty.

> At a lunch counter with sixteen seats, an observer sees five occupied seats and eleven empty seats.
> No two occupied seats are next to each other, and both end seats are empty. Each occupied seat makes its own
> run. The empty seats form six runs between and around them. That gives eleven runs, the maximum with only
> five occupied seats. With five occupied runs you can have at most six empty ones, because the runs
> alternate. If either end seat is occupied, there is room for at most five empty runs.

**Visual.** Keep the 5 occupied positions as dividers between 6 nonempty empty-seat blocks.
Show $\binom44\binom{10}5=252$ and $\binom{16}5=4\,368$, then
$252/4\,368=3/52\approx0.0577$.

> Under a uniform seating model, choose any five of the sixteen seats. For the maximum number of runs,
> all the occupied blocks have length one. The eleven empty seats must split into six nonempty blocks.
> That gives two hundred fifty-two seatings out of four thousand three hundred sixty-eight, or about
> zero point zero five seven seven. Many runs can suggest mixing or avoidance, and very few can suggest
> clustering. This one observation hints that people might avoid sitting next to strangers. We'd want more data
> before drawing a conclusion.

## 13. Code Lab (≈ 45 s) · `code`, `code_result`

**Visual.** code_cell with the program below and its exact output. Draw the 7 cells as a thumbnail.
Label the two results “Simulated” and “Exact (rounded)”.

```python
from random import Random

rng = Random(5)
cells, trials = 7, 100_000
target = [0, 0, 1, 1, 1, 2, 2]
hits = 0
for _ in range(trials):
    draws = rng.choices(range(cells), k=cells)
    hits += sorted(draws.count(cell) for cell in range(cells)) == target
print(f"{hits / trials:.6f} {264_600 / cells**cells:.6f}")
```

Output:
```
0.321590 0.321295
```

> Let's check the seven-cell example in Python. Each trial sends seven labelled balls independently to
> cells chosen with replacement. Count the balls in each cell and sort those counts. Sorting is how we
> accept the target pattern in any cell order. Record a hit whenever the sorted counts match.

> In a hundred thousand trials, the simulated frequency and the exact probability are both about
> zero point three two. Their small difference is expected with a finite simulation. Try watching what
> happens to that difference if you increase the number of trials. A larger sample tends to give a more
> stable estimate, though any single new run can land farther from the exact value.

## 14. Key ideas (≈ 40 s) · `recall`, `ideas`, `end`

**Visual.** key_ideas with the three points below. Pause ≥ 5 s before revealing the items.
- Count occupancy vectors of indistinguishable balls with $\binom{n+r-1}{n-1}$.
- For nonempty cells, reserve one ball per cell first. This gives $\binom{r-1}{n-1}$ when $r\ge n$.
- Independent uniform assignments of distinguishable balls give equally likely placements. Occupancy vectors can have different probabilities.

> Before we finish, pause and picture the difference between a list of cell counts and a placement of
> labelled balls. Where do the bars go when every cell needs a ball?

> Stars and bars counts occupancy vectors. To require nonempty cells, set one ball aside for each cell.
> With labelled balls placed independently and uniformly, count how many placements give the vector you
> want. Those counts are why some patterns are more likely than others.

**Visual.** end_card: “Full proofs, exercises and runnable code” · “Link in the description” ·
“Next lesson: The hypergeometric distribution and waiting times”.

> The full section and exercises are on Aram Code Lab. Next time we'll draw from a mixed population without
> replacement and ask how many successes we get, or how long we have to wait for them.

---

### Checked numbers (production notes; all computed in code)

- Occupancies and stars and bars: $(3,1,0,0,4)$ sums to 8 across 5 cells. There are 6 bars including the fixed
  ends, 4 inner bars and 12 movable slots. $\binom{12}{8}=\binom{12}{4}=495$. The 7 internal gaps give
  $\binom74=35$ nonempty distributions. Reserving 5 balls leaves 3 and gives the same count.
- Example 3.1: 3 indistinguishable dice over 6 faces give $\binom85=56$ records, with 5 inner bars in the
  encoding. The roll $(2,2,5)$ gives $(0,2,0,0,1,0)$. The mixed derivative example has counts $(2,1,1)$,
  and 3 variables give $\binom64=15$ at order 4 and $\binom75=21$ at order 5.
- Equation (3.3) worked example: 3 balls and 3 cells give $3^3=27$ placements. The fixed vector $(2,1,0)$
  has 3 assignments and probability $3/27=1/9$.
- Example 3.2: role sizes $(2,3,2)$ give 210 choices of cells, and $(2,2,1,1,1,0,0)$ gives 1,260 allocations
  of balls for each choice. The product is 264,600 placements out of $7^7=823\,543$, or about 0.3213.
  All 15 six-decimal rows are in chapter 8. The target $(2,2,1,1,1,0,0)$ is the most probable row. The perfectly even
  row is 0.006120, or about 0.0061 aloud. The exact probabilities sum to 1. The six-decimal labels shown
  here also sum to 1. $(3,2,1,1,0,0,0)$ is $176\,400/823\,543=3600/16807\approx0.214196$ (the site table
  printed 0.214197; fixed on the site on 2026-11-24).
- Example 3.3: 3 stars in 5 cells, with cells 1, 3 and 4 occupied. The three probabilities are
  $3!/5^3=6/125$, $1/\binom73=1/35$, and $1/\binom53=1/10$.
- Runs: AAABAABBBA has run lengths $(3,1,2,3,1)$. For 3 A's, 4 B's, 2 A runs and 3 B runs,
  there are $\binom21\binom32=2\cdot3=6$ arrangements.
- Example 3.4: the 16-seat sequence has 5 occupied and 11 empty seats, with 5 occupied runs and 6 empty runs.
  The maximum is 11 runs. There are $\binom44\binom{10}5=252$ such seatings of $\binom{16}5=4\,368$,
  giving $3/52\approx0.0577$.
- Code Lab: seed 5, 100,000 trials, 7 draws into 7 cells per trial. Exact printed output `0.321590 0.321295`.
