# The Arc Sine Law

Target length: about 9–10 minutes. Voice: am_puck, slightly slower (speed 0.9).
Style: AramCodeLab (dark, teal glow, Inter, cards). Objects morph into each other instead of
"clear screen → new picture". Colour code everywhere: **Alice = teal**, **Bob = indigo**,
**ties / key moments = amber**. Every number below has been checked by simulation or exact enumeration.

Chapters: 0:00 Cold open · 0:40 The puzzle · 1:40 The experiment · 3:00 Why: reflections ·
5:00 The last tie · 6:15 From bars to a curve · 7:15 Code Lab · 8:15 What it means · 8:50 Challenge

---

## 1. Cold open (≈ 40 s)

**Visual.** Eight small games appear one by one in cards, already coloured teal/indigo, with the
percentage of time Alice leads. Six cards light up amber.

> Here are eight games of coin tossing. A fair coin, a thousand tosses each.
> In six of them, one player was ahead for at least eighty percent of the game.
> In one, Bob led from the very first toss to the very last.
> Nothing is wrong with the coin. This is what fairness actually looks like.
> And by the end of this video, you will be able to compute exactly how often it happens.

**Visual.** Title card: `PROBABILITY · RANDOM WALKS` / **The Arc Sine Law**.

## 2. The puzzle (≈ 60 s)

**Visual.** Alice and Bob card; a score line starts at zero and moves up/down with each toss
(a coin flips in the corner for the first ten tosses, then speeds up).

> Alice and Bob toss a fair coin. Heads, Alice gets a point; tails, Bob does.
> We follow one number: Alice's score minus Bob's. Each toss moves it one step up or one step down.
> Above the line, Alice is ahead. Below it, Bob is ahead.

**Visual.** Three answer cards appear: **A** a hill centred at ½, **B** flat, **C** a valley (U).
A "pause and think" timer ring fills for 3 seconds.

> Here is the question. Play a thousand tosses and record what fraction of the time Alice was ahead.
> Repeat this many times. Which picture do you expect for those fractions?
> A hill around one half? Something flat? Or a valley?
> Take a moment and make a guess.

> Most people choose the hill. The coin is fair, so surely each player leads about half the time.

## 3. The experiment (≈ 80 s)

**Visual.** Games run quickly one after another in a small card at the top; at the end of each,
an amber dot drops from the card into the right bin of a histogram below (Galton-board style).
First slowly (10 games), then faster (100), then a flood (10,000). The U shape grows in front of the viewer.

> Let's not argue. Let's play.
> Each game ends with one number, the fraction of time Alice led, and that number drops into its bin.
> Ten games. A hundred. Ten thousand.

**Visual.** The dashed hill (the intuitive guess) is drawn over the histogram, then fades.
The two edge bins pulse amber.

> It is not a hill. It is a valley. The most likely outcomes are the most lopsided ones:
> Alice leads almost the whole game, or almost none of it.
> A fair looking split, between forty and sixty percent, happens only about thirteen percent of the time.
> And with probability about forty one percent, one of the players is ahead for more than ninety percent of the game.

> Why? To understand it, we need one beautiful trick.

## 4. Why: the reflection trick (≈ 2 min)

**Visual.** A path that starts above the axis, touches zero, and ends above. The part before the
first touch is reflected (mirror animation); the reflected start lies below the axis.

> Take any path that starts above zero and ends above zero, but touches zero somewhere in between.
> Reflect everything up to the first touch in the axis.
> You get a path that starts below zero and ends where the original ended.
> This works in both directions: every path from below must cross zero, and reflecting it back
> gives a touching path from above. So touching paths and paths from the mirror image start
> are in one to one correspondence. That is the reflection principle.

**Visual.** Counting paths that never return to zero. A stack of path counts
"paths to level r" with a minus sign "reflected paths"; the terms cancel in a telescoping cascade
(amber strike-through), leaving a single term.

> Now we can count the games in which the score never returns to zero.
> Split them by where they end. For each final level, reflection tells us how many paths
> sneak back to zero, and we subtract them.
> Something lovely happens when we add these up: almost everything cancels, like a collapsing telescope,
> and a single term is left.

**Visual.** Formula card builds up, with colour-coded terms:
`P(no return to zero in 2n tosses) = u₂ₙ`, `u₂ₙ = P(level after 2n tosses) = C(2n, n) / 2²ⁿ`.

> The result: the probability that the score never returns to zero in two n tosses
> is exactly the same as the probability that it is level at time two n.
> We call this number u two n. It is a simple binomial probability.

**Visual.** Dots of u₂ₘ for m = 1…50 and the curve 1/√(πm) through them.

> And u two n shrinks slowly, like one over the square root of pi n.
> After a thousand tosses, it is still about two and a half percent.
> Returns to zero are rare, and they get rarer as the game goes on.

## 5. The last tie (≈ 75 s)

**Visual.** A full game; the last visit to zero is marked with an amber flag; the game is split into
two coloured pieces: "ends level" (before) and "never returns" (after).

> Here is where it all comes together. Ask: when was the last time the score was tied?
> Cut the game at the last tie, at time two k.
> Before the cut, the path goes from zero back to zero: probability u two k.
> After the cut, it never returns to zero: by our lemma, probability u of two n minus two k.

**Visual.** Formula `P(last tie at 2k) = u₂ₖ · u₂ₙ₋₂ₖ` appears from the two pieces (each factor flies
out of its own piece). Bar chart for 2n = 20: tallest bars at both ends.

> So the probability that the last tie happens at time two k is u two k times u two n minus two k.
> Both factors are large when they are close to the start, so the product is largest at the two ends.
> The last tie is most likely to happen either very early or very late.

> And here is the surprise: the fraction of time Alice spends in the lead has exactly the same distribution.
> The proof of that takes a little more work. It is written out in full on our site.

## 6. From bars to a curve (≈ 60 s)

**Visual.** The bar chart for 2n = 10 morphs to 20, 50, 200, rescaled to the interval [0, 1];
the bars converge to the amber curve 1/(π√(x(1−x))). Then the area under the curve fills from 0 to x
while the formula for the arc sine law writes itself.

> Now let the game grow. Use the estimate u two m is about one over the square root of pi m,
> and set x equal to k over n. The bars settle onto a single curve:
> one over pi, times one over the square root of x times one minus x.
> The area under this curve, from zero to x, is two over pi times the arc sine of the square root of x.
> That is the arc sine law, and it is where the name comes from.

## 7. Code Lab (≈ 60 s)

**Visual.** A code card in JetBrains Mono (site style). The code types itself; a "Run" button is pressed;
the output appears; a small histogram is drawn from the results.

```python
import random

def lead_fraction(n=1000):
    s, ahead = 0, 0
    for _ in range(n):
        prev = s
        s += random.choice((-1, 1))
        ahead += max(prev, s) > 0
    return ahead / n

fracs = [lead_fraction() for _ in range(10_000)]
print(sum(f > 0.9 or f < 0.1 for f in fracs) / len(fracs))   # about 0.41
```

> You do not have to trust me. Here are ten lines of Python.
> One game counts the steps on which Alice is ahead. We play ten thousand games
> and ask how often someone leads more than ninety percent of the time.
> About forty one percent, just as the formula says.
> You can run this code right in your browser on Aram Code Lab, and change it.

## 8. What it means (≈ 35 s)

**Visual.** Two "season" lines of team standings, one team behind for most of the season;
caption: *a long lead is not evidence of skill*.

> So the next time someone has been ahead for a long time, in a game, in a season, in a contest
> decided by luck, remember: long leads are exactly what pure chance produces.
> The coin has no memory, but the score does.

## 9. Challenge (≈ 25 s)

**Visual.** Challenge card in the site style, with a ballot box: 60 votes for A, 40 for B,
counted in random order.

> Here is a challenge for you, and it uses the reflection trick.
> In an election, candidate A gets sixty votes and B gets forty. The votes are counted in random order.
> What is the probability that A is strictly ahead during the whole count?
> The answer and its solution are on Aram Code Lab. The link is in the description.

**Visual.** End card: logo, the arc sine law, "Full proof · exercises · code".

---

### Checked numbers
- Eight games (seeds not chosen): one player ≥ 80% in 6 of 8; one game Alice 0% (Bob led throughout).
- 10,000 games × 1000 tosses: P(split 40–60%) ≈ 0.128 (simulation 0.131); P(someone > 90%) ≈ 0.410 (simulation 0.414).
- Lemma P(no return in 2n) = u₂ₙ checked exactly for 2n = 10 (0.2461 = 0.2461).
- Last tie law checked exactly for 2n = 10.
- u₂ₘ vs 1/√(πm): m = 50 → 0.0796 vs 0.0798; after 1000 tosses (m = 500) u ≈ 0.025.
- Code Lab snippet output ≈ 0.417.
- Challenge (ballot problem): answer (60 − 40)/100 = 0.2, simulation 0.202.
