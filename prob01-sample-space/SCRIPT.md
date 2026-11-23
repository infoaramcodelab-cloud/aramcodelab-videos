# Probability Theory · Lesson 1 — Sample Space and Events

The narration and visual plan of the lesson. `script.py` holds the same narration split at the visual cues.

Site section:  1.1 Sample space and events (slug `sample-space-and-events`). Built with the lesson kit.

Colour code:
- sample points: muted dots;
- the event under discussion: teal;
- a second event: indigo;
- the complement: amber outline.

Chapters (approximate):
- 0:00 Welcome
- 0:50 Why a model first
- 1:50 Simple and compound events
- 3:00 Sample points and the sample space
- 4:10 Three balls in three cells
- 6:20 One scheme, many stories
- 7:30 Distinguishable or not
- 8:30 Sampling: counting smokers
- 9:20 Three coins
- 9:50 The ages of a couple
- 10:50 Bridge and aces
- 11:30 The algebra of events
- 13:20 Four identities and a trap
- 14:30 Discrete spaces and a tournament
- 16:10 Code Lab
- 17:00 Key ideas

---

## 1. Welcome (≈ 50 s)

**Visual.** title_card: eyebrow **PROBABILITY THEORY · LESSON 1**, title **Sample Space and Events**, small line
**Section 1.1 on Aram Code Lab**. No chapter strip and no total.

> Welcome to the first lesson of a course in probability theory. It's about discrete probability: coins, dice,
> cards, random walks, and the surprising laws that appear when an experiment is repeated many times.
>
> Every lesson matches a section on Aram Code Lab. There you'll find the full text, the proofs, the problems with
> solutions, and Python code you can run in your browser. The link is in the description.
>
> Before we compute a single probability, we have to answer a simpler question. Probability of *what*?

## 2. Why a model first (≈ 60 s)

**Visual.** Five small experiment cards: coin, dice, cards, people chosen at random, a telephone exchange with
calls arriving. Then a coin spins and lands on its edge; a red "×" appears and two clean cards **H** and **T** remain.
A ruler measures an age, 34.2817…, which snaps to an exact number.

> Probability becomes useful when we apply it to concrete experiments, real or imagined. We toss a coin, throw
> dice, deal cards, pick people at random from a population, or count the calls arriving at a telephone exchange.
> Each description stays vague until we agree on one thing: what exactly counts as a possible outcome?
>
> Every theory idealizes. A real coin can land on its edge. We agree that it can't, so the only results are heads
> and tails. Nobody's age can be measured exactly, but we treat it as an exact number. These conventions don't make
> the theory less useful. They are what makes a mathematical model possible in the first place.

## 3. Simple and compound events (≈ 70 s)

**Visual.** Two dice are thrown. The statement "the sum is six" splits into five dot-pairs (1,5) (2,4) (3,3) (4,2)
(5,1), outlined in teal. Then "both faces odd" outlines (1,1) (1,3) … (5,5) in indigo; (3,3) is inside both outlines
and pulses.

> We call the results of an experiment events. Some events can be split into simpler ones, and others can't.
>
> Throw two dice. The event "the sum is six" really means that the throw was one of five results: one and five,
> two and four, three and three, four and two, or five and one. It's a compound event made of five simple ones.
>
> Now look at three-three. It also makes another event happen: "both faces are odd". So compound events can occur
> together. Simple events never can. Each throw produces exactly one of them.

## 4. Sample points and the sample space (≈ 70 s)

**Visual.** box(definition, "Definition 1.1"), revealed line by line:
- the simple events are called **sample points**;
- every indecomposable outcome is represented by exactly one point;
- the set of all points is the **sample space** Ω;
- an **event** is a set of sample points.

> Here is the first definition of the course. The simple, indecomposable outcomes of an idealized experiment are
> called sample points, or just points. Every possible outcome is represented by one and only one point. The set of
> all points is the sample space, written with the Greek letter Omega. And an event is simply a set of sample
> points.

**Visual.** Geometry analogy: a point and a line drawn with "primitive notion" labels, next to Ω.

> Think of the sample space like "point" and "line" in geometry. It's a primitive notion. The theory starts only
> after the sample space has been chosen. An event makes sense only if, for every outcome, we can say whether it
> happened. Then the event is just the set of points where it did. And we never talk about a probability without
> saying which sample space we mean.

## 5. Three balls in three cells (≈ 130 s)

**Visual.** Three cells; balls a (teal), b (indigo), c (amber) drop in one by one; each has 3 choices: 3 · 3 · 3 = 27.
Then the full table of 27 arrangements, numbered 1–27 exactly as in the site's Example 1.1, is built up as a large
3 × 9 grid with legible letters.

> Here's an example we'll use again and again. Place three different balls, a, b and c, into three cells. Ball a
> has three choices. So does b, and so does c. That gives three times three times three, twenty-seven arrangements.
> Each arrangement is one sample point.
>
> Here they all are. Points one to three put all three balls into one cell. Points four to twenty-one put two balls
> into one cell and the third ball elsewhere. And points twenty-two to twenty-seven spread the balls out, one in
> each cell.

**Visual.** Events light up in turn on the grid, each with a count pill:
- "some cell has at least two balls": points 1–21, **21**;
- "the first cell is not empty": points 1, 4–15, 22–27, **19**;
- "every cell is occupied": points 22–27, **6**;
- "first cell empty and some cell has two balls": points 2, 3, 16–21, **8**;
- "every cell has two balls": nothing lights up, **0**, label "impossible event ∅".

> Now every statement about the experiment becomes a set of points. "Some cell holds at least two balls" is points
> one to twenty-one. "The first cell is not empty" is point one, points four to fifteen, and points twenty-two to
> twenty-seven: nineteen points. "Every cell is occupied" is just the last six. "The first cell is empty and some
> cell has two balls" is points two and three and sixteen to twenty-one, eight points.
>
> And "every cell holds two balls"? Three balls can't do that. No point qualifies, and the event is empty. We call
> it the impossible event.

## 6. One scheme, many stories (≈ 70 s)

**Visual.** Formula card: **r balls → n cells: n^r points**, with two separate lines:
"4 balls in 3 cells: 3^4 = 81" and "10 balls in 10 cells: 10^10". Then bullet_list with icons:
birthdays (people → 365 days), dice (dice → 6 faces; a coin → 2), elevator (passengers → floors),
random digits (positions → 10 digits), aces in bridge (4 aces → 4 players), misprints (misprints → pages).

> In general, r different balls can be placed into n cells in n to the power r ways. Four balls in three cells
> give eighty-one points. Ten balls in ten cells give ten to the tenth, ten billion.
>
> The nature of the points doesn't matter. Only the structure does. The same scheme describes many different
> stories. With birthdays, the people are the balls and the three hundred sixty-five days are the cells. Throwing r
> dice is placing r balls into six cells, and a coin has just two cells. Passengers leaving an elevator choose
> floors. Random digits distribute positions among the ten digits. When bridge is dealt, the four aces fall to four
> players. And misprints land on the pages of a book.
>
> All these problems are the same abstract problem in different words. One caution, though: the right
> *probabilities* are not always the same. That's the topic of the next lesson.

## 7. Distinguishable or not (≈ 60 s)

**Visual.** The 27-grid; the letters fade, balls become identical stars. Arrangements 4, 5 and 6 slide on top of each
other ("ab | c | –", "ac | b | –", "bc | a | –" become "** | * | –"), and so on. The grid collapses to **10**
configurations: {*** | – | –}, …, {** | * | –}, …, {* | * | *}.

> Now stop telling the balls apart. Arrangements four, five and six used to be different: a and b in the first
> cell, or a and c, or b and c. Without labels, they all look the same: two balls in the first cell and one in the
> second. The twenty-seven points collapse to just ten.
>
> Can real balls be told apart? It doesn't matter. Distinguishing them or not is our choice of model. The four
> aces in bridge are certainly different cards, yet it's often convenient to treat them as identical. Again, the
> theory begins only after we've made this choice.

## 8. Sampling: counting smokers (≈ 50 s)

**Visual.** 100 small person icons; the smokers among them glow. The sample space is a number line 0, 1, …, 100
(**101 points**); the event "majority are smokers" = {51, …, 100} is shaded teal. Then each point becomes a
quadruple (M_s, F_s, M_n, F_n) with sum 100. Pill: **176,851 points**, with "counted in Lesson 2.2" as a small note.

> A sampling example. We ask a hundred people whether they smoke, and record only the number of smokers. The sample
> space is the numbers from zero to a hundred: a hundred and one points. "The majority are smokers" is the event
> fifty-one up to a hundred.
>
> If we also record sex, a point becomes four numbers: male smokers, female smokers, male non-smokers and female
> non-smokers, adding up to a hundred. There are a hundred seventy-six thousand eight hundred fifty-one such
> quadruples. We'll learn to count them in the next chapter. The point is that the same survey gives different
> sample spaces depending on what we record.

## 9. Three coins (≈ 30 s)

**Visual.** Eight cards HHH, HHT, HTH, THH, HTT, THT, TTH, TTT. "Two or more heads" outlines the first four (teal),
and "exactly one tail" outlines HHT, HTH, THH (indigo).

> Toss a coin three times. The sample space has eight points. "Two or more heads" is the first four. "Exactly one
> tail" is three of them: HHT, HTH and THH. Notice that the second event is inside the first. We'll name that
> relation in a minute.

## 10. The ages of a couple (≈ 60 s)

**Visual.** First quadrant; x = husband's age, y = wife's age. Region A = {x > 40} right of x = 40 (teal); region
B = {x > y} below the diagonal (indigo); region C = {y > 40} above y = 40 (amber). Then AB is shown as the overlap of A
and B, and A ∪ C as their union.

> Events don't have to be finite lists. Let x be a husband's age and y his wife's age. A sample point is a pair x,
> y of positive numbers: a point in the first quadrant of the plane.
>
> "The husband is older than forty" is everything to the right of the vertical line x equals forty. "The husband is
> older than his wife" is everything below the diagonal. "The wife is older than forty" is everything above the
> horizontal line y equals forty. Each event is a region, and relations between events become relations between
> regions you can see. For example, "the husband is over forty *and* older than his wife" is where the first two
> regions overlap.

## 11. Bridge and aces (≈ 40 s)

**Visual.** Four seats N, E, S, W, each dealt 13 cards; the four aces glow. N1 ∪ E1 ∪ S1 ∪ W1 = Ω, and N1E1S1W1 is
shown as one ace per player.

> One more example. Deal fifty-two cards to four bridge players, North, East, South and West, thirteen each. Let N
> one be the event that North has at least one ace, and the same for the others. The union of the four events is
> the whole sample space, because somebody always holds an ace. And the event that all four happen together means
> that every player has exactly one ace.

## 12. The algebra of events (≈ 110 s)

**Visual.** A rectangle Ω with dots. box(definition, "Definitions 1.2–1.4"), each line animated on the dots:
- ∅, the impossible event: no dots highlighted;
- A′, the complement: everything outside A, amber;
- AB = A ∩ B, the intersection: the overlap of teal and indigo;
- A ∪ B, the union: both regions;
- mutually exclusive events: disjoint regions, AB = ∅.

> Once events are sets, the language of events is the language of sets. Fix a sample space. Two events are equal if
> they contain the same points.
>
> An event with no points is impossible, and we write it as the empty set. The event "A does not occur" contains
> all the points not in A. It's called the complement of A, and we write A prime. The complement of the whole space
> is the empty set.
>
> "Both A and B occur" is the intersection: the points in both. In probability we usually write it as a product, A B, and so will we.
> "At least one of them occurs" is the union. The same works for any number of events. And events are mutually
> exclusive if no two of them have a point in common: they can never happen together.

**Visual.** box(definition, "Definition 1.5"): A ⊂ B, "A implies B"; B − A = BA′. Examples animate:
A′ = Ω − A; if AB = ∅ then A ⊂ B′; A − AB = AB′ ("A, but not both").

> If every point of A is also in B, we write A is contained in B, and say "A implies B". Whenever A happens, B
> happens too. In the coin example, "exactly one tail" implies "two or more heads". In that case B minus A means "B
> happens but A doesn't". For instance, the complement of A is Omega minus A. If A and B are mutually exclusive, then
> A is contained in the complement of B. And A minus AB means "A, but not both".

## 13. Four identities and a trap (≈ 70 s)

**Visual.** box(property, "Property 1.1"), with the four identities:
(A ∪ B)′ = A′B′,  (AB)′ = A′ ∪ B′,  A − AB = AB′,  A ∪ B = A ∪ (B − AB).
Each identity is shaded on two side-by-side Ω pictures that end up identical. For the last one, B − AB slides next to A
without overlap.
Then "Careful": (A ∪ B)′ ≠ A′ ∪ B′ and (AB)′ ≠ A′B′, with the two different shadings side by side.

> Four identities are worth knowing. "Neither A nor B" is the same as "not A and not B". "Not both" is the same as
> "not A or not B". "A but not both" is A together with the complement of B. And the union of A and B splits into A
> and the part of B outside A. Those two pieces never overlap, which will matter when we add probabilities.
>
> How do we prove them? Just check points. A point lies outside the union exactly when it lies outside A and
> outside B. That's the first identity. The others work the same way, and you'll find them in the problems.
>
> Watch the order of operations. The complement of a union is not the union of the complements, and the complement
> of an intersection is not the intersection of the complements. The pictures make the difference obvious.

## 14. Discrete spaces and a tournament (≈ 100 s)

**Visual.** A coin is tossed until the first head: E1 = H, E2 = TH, E3 = TTH, … stretch into an endless row; E0
("heads never appears") sits at the start with a question mark. box(definition, "Definition 1.6").

> So far our sample spaces were finite. Sometimes we need infinitely many points. Toss a coin until the first head
> appears. The outcomes are H, TH, TTH, and so on, without end. We might also add a point E zero for "heads never
> appears". A sample space is called discrete if it is finite, or if its points can be arranged in a sequence, E
> one, E two, E three, and so on.

**Visual.** Example 1.8: players a, b, c; a game tree. First a plays b while c waits; the loser sits out; a
player who wins twice in a row wins the tournament. The outcome strings appear in two columns:
aa, acc, acbb, acbaa, acbacc, … and bb, bcc, bcaa, bcabb, bcabcc, …
Then the two endless strings acbacbacb… and bcabcabca… Finally all points are put into one numbered list:
the two endless strings first, then aa, bb, acc, bcc, ….

> Here's a richer example. Three players, a, b and c, play games with no draws. First a plays b while c waits. The
> loser is replaced by c, the winner plays c, and so on. The tournament ends as soon as someone wins two games in a
> row. Write down the winner of each game, and you get the possible outcomes. a a: a wins twice. a c c: a wins, then
> c beats a and then b. Then a c b b, a c b a a, and so on, and the same list starting with b.
>
> There are also two endless sequences in which nobody ever wins twice in a row. Is this sample space discrete? Yes.
> List the two endless sequences first, then a a, b b, a c c, b c c, and so on. Every point gets a number. On the
> site we put probabilities on this tournament in the problems.
>
> Not every sample space is discrete. The ages of a couple form a region of the plane, and its points can't be put
> into a sequence. In discrete spaces, probabilities of events are sums. In general they would need integrals. In
> this course we work only with discrete spaces.

## 15. Code Lab (≈ 50 s)

**Visual.** code_cell with the code below (no ligatures); output panel.

```python
from itertools import product
points = list(product("123", repeat=3))   # cells of balls a, b, c
crowded = {p for p in points if len(set(p)) < 3}
full = {p for p in points if len(set(p)) == 3}
first_used = {p for p in points if "1" in p}
print(len(points), len(crowded), len(full), len(first_used))
S, A, B = set(points), crowded, {p for p in points if p[0] == "1"}
print(len(S - (A | B)), S - (A | B) == (S - A) & (S - B))
```

Output:
```
27 21 6 19
4 True
```

> In Python, a sample point is a tuple holding the cell of ball a, ball b and ball c. The product function lists all
> twenty-seven. Events are sets built with a condition. A set of cells with fewer than three elements means that
> two balls share a cell. We get the same counts as before: twenty-one, six and nineteen.
>
> The last line checks the first identity on real sets. Take A as "crowded" and B as "ball a is in the first cell".
> The points outside both form a set of four points, and the comparison says True. Try changing the events and
> checking the other identities yourself.

## 16. Key ideas (≈ 50 s)

**Visual.** key_ideas with the three items of the site's Key ideas card for section 1.1, pause = 5 s.
end_card: logo, "Full proofs, exercises and runnable code", **Link in the description**, and
"Next lesson: Probabilities in discrete sample spaces".

> Before we finish, pause the video and try to recall the main ideas of this lesson.
>
> Each elementary outcome is one sample point, and an event is a set of points of the sample space. A B means both
> events occur, A union B means at least one does, and mutually exclusive events have no common point. The
> complement of A holds everything outside A, and the complement of a union is the intersection of the complements.
>
> The full section, with all the examples and the problems, is on Aram Code Lab. The link is in the description.
> Next time, we put probabilities on these points.

---

### Checked numbers (production notes)
Computed with itertools and math on 2026-11-23:
- 27 arrangements.
- Event counts on the 27 points: 21 (some cell has at least two balls), 19 (first cell non-empty), 6 (all occupied), 8 (first cell empty and some cell has two balls), 0 (every cell has two balls).
- 10 configurations of indistinguishable balls, which is C(5,2).
- 3^4 = 81.
- 101 points for the number of smokers. Quadruples with sum 100: C(103,3) = 176,851.
- 3 coins give 8 points. "Exactly one tail" ⊂ "two or more heads".
- The identities were checked on the 27 points with the Code Lab sets:
  - (A ∪ B)′ = A′B′;
  - (AB)′ = A′ ∪ B′;
  - A − AB = AB′;
  - A ∪ B = A ∪ (B − AB), with the two parts disjoint.
- Code Lab: output `27 21 6 19` / `4 True`. S − (A ∪ B) is the 6 full arrangements minus the 2 with ball a in cell 1, which leaves 4.
