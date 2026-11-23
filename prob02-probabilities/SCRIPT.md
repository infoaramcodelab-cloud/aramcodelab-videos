# Probability Theory · Lesson 2 — Probabilities in Discrete Sample Spaces

The narration and visual plan of the lesson. `script.py` holds the same narration split at the visual cues.
Voice: Orpheus, Tara. The published narration was sped up by 7 % after generation
(`ffmpeg -filter:a atempo=1.07`), and `audio/durations.json` holds the timings of the sped-up clips.

Site section: 1.2 Probabilities in discrete sample spaces (slug `probabilities-in-discrete-sample-spaces`).
Next lesson: 2.1 The multiplication rule and ordered samples. Built with the lesson kit.

Colour code (as in Lesson 1):
- sample points: muted dots; probability "mass" of a point = the dot's area;
- event A (or A1) = teal; B (or A2) = indigo; overlap = both outlines; "careful" cards = amber;
- the 27-grid uses the Lesson 1 tiles (closed boxes with three compartments).

Chapters: 0:00 Welcome · Numbers like lengths and masses · Same balls, model one · Same balls, model two ·
What frequencies say · The rules · Adding over an event · Probability of a union · Unions with dice ·
Boole's inequality · Equally likely points · A trap with two dice · Code Lab · Key ideas
(timestamps come from the render)

---

## 1. Welcome (≈ 40 s) · `welcome`, `recap`

**Visual.** title_card("1.2", "Probabilities in Discrete Sample Spaces", lesson 2). Then the 27-grid of Lesson 1
fades in, small, with the pill "Ω: 27 points".

> Welcome back. In the first lesson we built sample spaces. Every possible outcome became a point, and every event
> became a set of points. Three balls in three cells gave us twenty-seven points. Two dice gave us thirty-six.

> But we never said how likely anything is. That's today's job. We'll put probabilities on the points, and we'll
> learn the first rules for combining them. And we'll see something surprising: the same sample space can carry
> very different probabilities.

## 2. Numbers like lengths and masses (≈ 70 s) · `like_lengths`, `fair_coin`, `model_use`

**Visual.** Three cards side by side: a ruler (**length**), a weight (**mass**), a coin (**probability**).

> So what is a probability? Think of geometry. Geometry doesn't tell you how to measure the length of a real table.
> It assumes lengths are given and studies how they fit together. Mechanics does the same with masses.
> Probability theory treats probabilities the same way. They're numbers we're given, and the theory studies how
> they combine. How to find them in the real world is the job of applications, and of statistics.

**Visual.** The coin card shows **H: 1/2**, **T: 1/2**. Then three tosses: the 8 outcomes HHH … TTT as cards, each
labelled 1/8. Pill: $2^n$ outcomes, each $1/2^n$.

> Take a fair coin. We give heads probability one half, and tails probability one half. Toss it three times, and
> each of the eight outcomes gets probability one eighth. With n tosses, all two to the n outcomes get the same
> probability.

**Visual.** A slightly bent coin; a deck of cards with a visible clump of red cards. Caption: "departures from the
model tell us something".

> Is that true of a real coin? Not exactly. No coin is perfectly fair. "Fair" is a convention, a model. But it's a
> useful model, for two reasons. It describes real coins well enough. And when reality departs from it, the
> departure itself tells us something: maybe the coin is loaded, or the deck wasn't shuffled properly.

## 3. Same balls, model one (≈ 75 s) · `mb_intro`, `mb_events`

**Visual.** The 27-grid; every tile gets a small label 1/27. Pill: **Maxwell–Boltzmann**. box(example,
"Example 1.9 · distinguishable balls").

> Let's go back to three balls in three cells. The balls are different: a, b and c. Each ball lands in a cell, and
> nothing favours one arrangement over another. So it's natural to give each of the twenty-seven points the same
> probability, one over twenty-seven. In physics this is called the Maxwell–Boltzmann model. It's a good first
> model for birthdays, for passengers leaving an elevator, and for collecting coupons.

**Visual.** The Lesson 1 events light up one by one on the grid, with their probabilities:
- "Some cell has at least two balls": 21 tiles → **21/27 = 7/9**;
- "Every cell is occupied": 6 tiles → **6/27 = 2/9**;
- "The first cell is not empty": 19 tiles → **19/27**.

> Now every event from last time gets a number. "Some cell has at least two balls" covered twenty-one points, so its
> probability is twenty-one over twenty-seven, which is seven ninths. "Every cell is occupied" had six points: two
> ninths. And "the first cell is not empty" had nineteen points, so nineteen over twenty-seven. Counting points is
> all it takes, because every point weighs the same.

## 4. Same balls, model two (≈ 110 s) · `be_collapse`, `be_weights`, `be_equal`, `be_compare`, `be_lesson`

**Visual.** The letters turn into stars and the 27 tiles collapse into the 10 configuration tiles with ×1/×3/×6
badges, exactly as in Lesson 1. box(example, "Example 1.10 · indistinguishable balls").

> Now let's stop telling the balls apart. As we saw last time, the twenty-seven arrangements collapse into just ten
> configurations.

**Visual.** Table builds row by row:

| configuration | {★★★\|–\|–} (3 of them) | {★★\|★\|–} (6 of them) | {★\|★\|★} (1) |
|---|---|---|---|
| from the 27 arrangements | 1/27 | 3/27 = 1/9 | 6/27 = 2/9 |

Then derivation: $3\cdot\tfrac1{27} + 6\cdot\tfrac19 + 1\cdot\tfrac29 = \tfrac19 + \tfrac69 + \tfrac29 = 1$.

> If we keep the probabilities from the twenty-seven arrangements, these ten configurations are not equally likely.
> "All three in one cell" comes from a single arrangement, so it has probability one over twenty-seven. "Two in one
> cell and one in another" comes from three arrangements, so three over twenty-seven, one ninth. And "one ball in
> each cell" comes from six arrangements: two ninths. Check the total: three times one over twenty-seven, plus six
> times one ninth, plus two ninths. That's exactly one.

**Visual.** A second table row slides in: **Bose–Einstein: 1/10, 1/10, 1/10**. Pill: **Bose–Einstein**.

> But here's another choice. Why not give all ten configurations the same probability, one tenth each? It looks
> artificial. And yet it's exactly how certain elementary particles behave. Physicists call it Bose–Einstein
> statistics.

**Visual.** Two-column comparison card, MB (teal) vs BE (indigo):
- every cell occupied: **2/9 ≈ 0.22** vs **1/10**;
- all three in one cell: **1/9 ≈ 0.11** vs **3/10**;
- some cell has two balls or more: **7/9 ≈ 0.78** vs **9/10**.

> The two models really disagree. The chance that every cell is occupied is two ninths in the first model, about
> twenty-two percent, and only one tenth in the second. The chance that all three balls share a cell is one ninth
> against three tenths. Almost three times bigger!

**Visual.** Big text: **The sample space does not decide the probabilities.** Small: "Which model fits is a question
of experience, not of logic."

> Both models are mathematically correct. Which one fits a real situation is a question of experience, not of
> logic. So here's the lesson: the sample space alone doesn't decide the probabilities. We have to choose them,
> and the choice is part of the model.

## 5. What frequencies say (≈ 80 s) · `frequency_idea`, `frequency_run`, `frequency_groups`

**Visual.** Text card: "Repeat the experiment many times: the fraction of trials in which A occurs ≈ P{A}."

> What does "probability one half" mean in the real world? The frequency interpretation says this: repeat the
> experiment many times, and the fraction of trials in which A happens should be close to the probability of A.

**Visual.** A running-frequency plot: x = number of tosses (log scale, 1 to 10,000), y = fraction of heads, dashed
line at 1/2. Data: `Random(14)`, 10,000 fair tosses. Pills appear at n = 10, 100, 1,000, 10,000: **4/10**,
**57/100**, **525/1,000**, **4,989/10,000**.

> Here are ten thousand simulated coin tosses. After ten tosses we have four heads. After a hundred, fifty-seven.
> After a thousand, five hundred twenty-five. And after ten thousand, four thousand nine hundred eighty-nine. The
> fraction settles down, very close to one half.

**Visual.** The 10,000 tosses cut into 100 groups of 100; a dot plot of heads per group, from **37** to **63**, with
the band 45–55 shaded (**72** of the 100 groups fall inside).

> But look closer. Cut the same tosses into a hundred groups of a hundred. One group has only thirty-seven heads,
> another has sixty-three. Only seventy-two groups out of a hundred land between forty-five and fifty-five. Swings
> like these are completely normal. So how do we decide whether real data agree with a model? To answer that, we
> need the theory itself. We'll get there later in the course.

## 6. The rules (≈ 70 s) · `convention`, `zero_points`

**Visual.** A row of points E1, E2, E3, … as dots whose areas are proportional to their probabilities. Then
box(definition, "Fundamental convention"): $\mathbf P\{E_i\} \ge 0$, $\mathbf P\{E_1\} + \mathbf P\{E_2\} + \dots = 1$   (1.1)

> Now let's write the rules down. Take a discrete sample space with points E one, E two, and so on. To each point
> we assign a number, its probability. These numbers are never negative, and together they add up to exactly one.
> That's the fundamental convention of the whole course.

**Visual.** The tournament from Lesson 1: the two endless sequences "abcabc…" and "acbacb…", each with the label
P = 0, next to the finite outcomes.

> A point is even allowed to have probability zero. In a discrete space we could simply remove such points. But
> often we don't know in advance which outcomes are really possible. Remember the tournament from last time, with
> its two endless games where nobody ever wins twice in a row? We kept them as points. In the problems on the site
> it turns out that they have probability zero.

## 7. Adding over an event (≈ 70 s) · `event_sum`, `consequences`

**Visual.** An event A outlined in teal around some dots; their masses slide together into one bar.
box(definition, "Definition 1.7"): $\mathbf P\{A\} = \sum_{E_i \in A} \mathbf P\{E_i\}$.

> And here's the definition that ties everything together. The probability of an event A is the sum of the
> probabilities of all the points in A. That's it. An event is a set of points, so its probability is the total
> weight of those points.

**Visual.** derivation, three lines appearing one by one: $\mathbf P\{\Omega\} = 1$, $\mathbf P\{\varnothing\} = 0$,
$0 \le \mathbf P\{A\} \le 1$   (1.2).

> Three facts follow at once. The whole sample space contains every point, so its probability is one. The empty set
> contains no points, so its probability is zero. And any other event collects some of the weight, never negative
> and never more than the total, so its probability lies between zero and one.

## 8. Probability of a union (≈ 100 s) · `union_question`, `union_overcount`, `union_theorem`, `union_coins`

**Visual.** Two overlapping regions of dots: A1 teal, A2 indigo, Ω around them.

> Now the first real question. What's the probability that A one or A two happens, at least one of them? We need
> the probabilities of all the points in the union, each point counted once.

**Visual.** Add P{A1}: teal dots light up. Add P{A2}: indigo dots light up, and the dots in the overlap get a
"×2" badge. Inequality (1.3): $\mathbf P\{A_1 \cup A_2\} \le \mathbf P\{A_1\} + \mathbf P\{A_2\}$.

> What if we simply add the two probabilities? Every point that lies only in A one is counted once. Every point that
> lies only in A two is counted once. But a point in the overlap, in both events, is counted twice. So the plain sum
> can only be too big, never too small.

**Visual.** Subtract P{A1A2}: the ×2 badges disappear. box(theorem, "Theorem 1.1"):
$\mathbf P\{A_1 \cup A_2\} = \mathbf P\{A_1\} + \mathbf P\{A_2\} - \mathbf P\{A_1A_2\}$   (1.4)

> The fix is easy. Every point of the overlap was counted exactly one time too many, so we subtract the overlap
> once. The probability of the union is the probability of A one, plus the probability of A two, minus the
> probability that both happen. And that short argument is the complete proof of the first theorem of the course.

**Visual.** box(example, "Example 1.11"). Four cards HH, HT, TH, TT, each 1/4. A1 = {HH, HT} teal, A2 = {HH, TH}
indigo; HH gets both outlines. derivation: $\tfrac12 + \tfrac12 - \tfrac14 = \tfrac34$.

> Let's try it. Toss a coin twice. The four outcomes each have probability one quarter. "Heads on the first toss" is
> H H and H T: probability one half. "Heads on the second toss" is H H and T H: also one half. Does "at least one
> head" have probability one half plus one half, which is one? Of course not. H H was counted twice. Subtract its
> quarter, and the answer is three quarters. And that's right: only T T is missing.

## 9. Unions with dice (≈ 60 s) · `dice_union`

**Visual.** The 6×6 dice matrix from Lesson 1. "The sum is six" (5 points, teal) and "both faces odd" (9 points,
indigo outline). The 3 shared points (1,5), (3,3), (5,1) get both. box(example, "Example"): derivation
$\tfrac5{36} + \tfrac9{36} - \tfrac3{36} = \tfrac{11}{36}$.

> One more, with two dice, using the two events from last time. "The sum is six" has five points, so probability
> five over thirty-six. "Both faces odd" has nine points: nine over thirty-six. They share three points: one and
> five, three and three, five and one. So the probability that the sum is six, or both faces are odd, is five plus
> nine minus three, over thirty-six. Eleven over thirty-six. Count the highlighted squares, and you'll find exactly
> eleven.

## 10. Boole's inequality (≈ 80 s) · `exclusive_add`, `boole`, `boole_dice`

**Visual.** The two regions slide apart until the overlap is empty. (1.5):
$A_1A_2 = \varnothing \Rightarrow \mathbf P\{A_1 \cup A_2\} = \mathbf P\{A_1\} + \mathbf P\{A_2\}$.

> When the events are mutually exclusive, there's no overlap and nothing to subtract. Then probabilities simply add.

**Visual.** Many overlapping regions A1, A2, A3, … box(property, "Property 1.2 · Boole's inequality"):
$\mathbf P\{A_1 \cup A_2 \cup \dots\} \le \mathbf P\{A_1\} + \mathbf P\{A_2\} + \dots$   (1.6), and for mutually
exclusive events equality   (1.7).

> The same idea works for any number of events, even infinitely many. Add up their probabilities, and every point
> of the union is counted at least once, maybe more. So the probability that at least one of the events happens is
> at most the sum of their probabilities. This is Boole's inequality. And if the events are mutually exclusive,
> every point is counted exactly once, and the sum is exact.

**Visual.** Three dice; each shows a six with probability 1/6. Bound: $\tfrac16 + \tfrac16 + \tfrac16 = \tfrac12$.
Then the exact value appears beside it: $1 - \left(\tfrac56\right)^3 = \tfrac{91}{216} \approx 0.42$.

> Here's how it helps. Throw three dice. What's the chance of at least one six? Each die shows a six with probability
> one sixth, so Boole's inequality says: at most one half. The exact answer, which we'll be able to compute in a
> later chapter, is ninety-one over two hundred sixteen, about forty-two percent. The bound is rough, but it's
> instant, and it never lies. That kind of quick bound will save us many times in this course.

## 11. Equally likely points (≈ 60 s) · `classical`, `classical_example`

**Visual.** derivation: $\mathbf P\{A\} = \dfrac{|A|}{N} = \dfrac{\text{favourable cases}}{\text{all cases}}$.

> A very common special case: the sample space has N points, and all of them are equally likely, each with
> probability one over N. Then the probability of any event is just the number of its points divided by N.
> Favourable cases over all cases.

**Visual.** The dice matrix; the six points with sum seven (the anti-diagonal) light up: $\tfrac6{36} = \tfrac16$.

> For two fair dice, all thirty-six points are equally likely. The sum is seven at six of them: one and six, two and
> five, and so on up to six and one. So the probability of a seven is six over thirty-six, one sixth.

## 12. A trap with two dice (≈ 90 s) · `sums_trap`, `sums_truth`, `classical_caution`, `next_chapter`

**Visual.** A "Careful" card (amber). Eleven tiles 2, 3, …, 12, each labelled "1/11?" with a question mark.

> Now a trap. Someone says: "The sum of two dice is one of eleven numbers, from two to twelve. So the chance of a
> seven is one in eleven." Favourable cases over all cases. What went wrong?

**Visual.** Above each sum, a column of its dice pairs: heights 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1. Labels 1/36 under
the 2 and the 12, 6/36 under the 7.

> The eleven sums are perfectly good outcomes, but they're not equally likely. A sum of two needs a double one: just
> one of the thirty-six points. A sum of seven comes from six points. The classical formula only works when the
> points really are equally likely. Here they aren't.

**Visual.** Three small cards: a biased coin "p and q = 1 − p"; a card "boys and girls are not born equally often";
the MB vs BE table from chapter 4.

> That's why the classical formula is not the definition of probability. It's only a special case. A biased coin
> still has two outcomes, but with probabilities p and one minus p. Boys and girls are not born exactly equally
> often. And we saw with the balls that "equally likely" on one sample space and on another can give different
> answers.

**Visual.** A pill: "Next chapter: counting".

> So the real work is to choose a sample space whose points really are equally likely. Then everything reduces to
> counting points. And counting, done carefully, is exactly what the next chapter is about.

## 13. Code Lab (≈ 45 s) · `code`, `code_result`

**Visual.** code_cell with the code below; output panel; then two bars "every cell occupied": **0.222** (MB, exact
2/9) and **0.101** (BE, exact 1/10).

```python
from random import Random
from itertools import combinations_with_replacement
rng = Random(1)
configs = list(combinations_with_replacement(range(3), 3))   # 10 configurations
N = 100_000
mb = sum(len({rng.randrange(3) for ball in "abc"}) == 3 for _ in range(N))
be = sum(len(set(rng.choice(configs))) == 3 for _ in range(N))
print(len(configs), mb / N, be / N)
```

Output:
```
10 0.22234 0.10054
```

> Let's test the two models in Python. In the first model, each of the three balls picks a cell on its own. In the
> second, we pick one of the ten configurations, all equally likely. We ask both models the same question, a
> hundred thousand times: is every cell occupied?

> The first model says about twenty-two percent, close to two ninths. The second says about ten percent, close to
> one tenth. Same balls, same cells, same question, two different answers. The model decides. Try changing the
> question, and see which events the two models agree on.

## 14. Key ideas (≈ 50 s) · `recall`, `ideas`, `end`

**Visual.** key_ideas with the three items of the site's Key ideas card for section 1.2; pause ≥ 5 s before the
items appear. end_card: "Full proofs, exercises and runnable code" · "Link in the description" ·
"Next lesson: The multiplication rule and ordered samples".

> Before we finish, pause the video and try to recall the main ideas of this lesson.

> In a discrete space, we give the points non-negative probabilities that add up to one, and the probability of an
> event is the sum over its points. For a union of two events, add the two probabilities and subtract the overlap,
> which was counted twice. And a union never has more probability than the sum of its parts. For mutually exclusive
> events, the sum is exact.

> The full section, with the problems, is on Aram Code Lab. The link is in the description. Next time, we start
> counting: ordered samples and the multiplication rule.

---

### Checked numbers (production notes; all computed in code)
- Maxwell–Boltzmann on the 27 arrangements: some cell has ≥ 2 balls 21/27 = 7/9; every cell occupied 6/27 = 2/9;
  first cell not empty 19/27; all three in one cell 3/27 = 1/9.
- Bose–Einstein on the 10 configurations: some cell has ≥ 2 balls 9/10; every cell occupied 1/10;
  all three in one cell 3/10; (first cell not empty 6/10, not used).
- Weights: 3·(1/27) + 6·(1/9) + 1·(2/9) = 1.
- Frequencies, `Random(14)`, 10,000 tosses with `rng.random() < 0.5`: prefix counts 4 of 10, 57 of 100, 525 of 1,000,
  4,989 of 10,000; groups of 100: min 37, max 63, 72 groups within 45–55. (The site's text mentions another simulated
  series with 4,979 heads; the video shows its own simulation and does not quote the site's number.)
- Example 1.11: 1/2 + 1/2 − 1/4 = 3/4.
- Dice: sum six 5 points, both odd 9 points, shared 3 points ((1,5), (3,3), (5,1)); union 11/36.
- Three dice, at least one six: Boole bound 1/2; exact 1 − (5/6)³ = 91/216 ≈ 0.4213.
- Sums of two dice: counts 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1 for sums 2 … 12; P(7) = 6/36 = 1/6.
- Code Lab: run as written, output `10 0.22234 0.10054`. Exact values: 2/9 ≈ 0.2222 and 1/10.
