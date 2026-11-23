# A positive test: am I ill?

Target length: 5:30, including the pause and time to read the visuals. Voice: am_fenrir, speed 0.98.
Style: AramCodeLab (near-black cards, teal glow, Inter, JetBrains Mono). Teal circles mark people with the condition. Indigo diamonds mark people without it. An amber outline and a plus sign mark a positive result in either group. Keep these meanings as the dots become rectangles and the rectangles become terms in the formula.

Chapters: 0:00 Cold open · 0:30 The puzzle · 1:10 The experiment · 1:50 Why: count the positives ·
2:42 From the picture to the formula · 3:37 Code Lab · 4:27 What it means · 5:02 Challenge

---

## 1. Cold open (≈ 30 s)

**Visual.** A single rounded test card shows **POSITIVE**. It slides up to reveal two identical amber-outlined tiles, one with a teal circle and one with an indigo diamond. The tiles lock side by side under **50%**. Let the result sit for a beat.

> Imagine a test that catches ninety-nine percent of people who have a condition. Your result comes back positive. In the example we’re about to build, the chance that you have the condition is exactly fifty percent.
>
> Half the positive results are real cases. The other half are false alarms. Where did all those false alarms come from? To find out, we’ll follow the people behind the percentages.

**Visual.** The tiles become the dot and diamond in the title card. **PROBABILITY · CONDITIONAL CHANCE** / **A positive test: am I ill?**

## 2. The puzzle (≈ 40 s)

**Visual.** Three cards enter as each fact is spoken. **1% have the condition** · **99% positive among people with it** · **1% positive among people without it**. Keep each rate next to its group label. The last two cards transfer their amber plus signs to a single **POSITIVE** tray.

> Here are the rules of our imaginary test. In the group being tested, one percent of people have the condition. Among people who have it, ninety-nine percent get a positive result. Among people who don’t, one percent still get a positive result. That last number is the false-positive rate.
>
> You already know the answer is half. Here’s the part to guess. If ten thousand people take the test, how many false alarms should we expect? About one? About a hundred? About a thousand? Hold on to your guess. We’ll count them two ways.

**Visual.** Answer cards labeled **About 1**, **About 100**, and **About 1,000**. Hold a silent **Pause and think** ring for four seconds.

## 3. The experiment (≈ 40 s)

**Visual.** A 100-by-100 dot grid grows out of the result tray. Label it **One simulated group · 10,000 people**. Reveal condition status first, then test outcomes. Trace a few outlined positives from across the grid into two tally cards. Show **107 true positives** and **97 false positives**, then **107 / 204 ≈ 52.5%**. Keep a small **One run** pill beside the tally.

> Let’s give the test to ten thousand simulated people. For each person we draw their condition status, then draw their result using the rate for that group. Watch the grid light up. Lights cluster in the small group. Across the much bigger group, they’re scattered.
>
> In this run, we got a hundred and seven true positives and ninety-seven false positives. That’s about fifty-two and a half percent of the positives coming from people with the condition. Run it again and the counts will move. To see why they’re so close, let’s take the randomness out of the picture.

## 4. Why: count the positives (≈ 52 s)

**Visual.** Reuse the grid and visibly change its label to **Expected counts · 10,000 people**. Regroup it into an oversized view of **100 with the condition** beside **9,900 without it**, with a zoom callout for the smaller group. Highlight 99 positives in the first group and 99 in the second. Dim the negatives and slide the two positive stacks into the same tray.

> Out of ten thousand, one percent gives us a hundred people with the condition. The test catches ninety-nine of those. Now look at the other group. There are nine thousand nine hundred people without the condition. Even one percent of that group gives us ninety-nine false positives.
>
> Both groups send the same number into the tray. There are a hundred and ninety-eight positives altogether, and ninety-nine come from people with the condition. That’s exactly half.
>
> Here’s the switch that makes this puzzle tricky. When you hear “ninety-nine percent,” you’re standing in the group that has the condition and looking for plus signs. Once you’ve seen a plus sign, you’re standing in a different group. Now you’re looking for people who have the condition.

**Visual.** First bracket all 100 people with the condition and highlight 99. Then move the bracket to all 198 positives and keep the same 99 highlighted. Match the framing so the viewer sees the denominator change.

## 5. From the picture to the formula (≈ 55 s)

**Visual.** Transform the expected-count grid into one unit-area rectangle. Split its width into the proportions with and without the condition. In each column, shade the positive fraction of its height from the same baseline. Use callouts for the thin regions. Keep the full rectangle and the two positive areas at true scale when they are compared. Label the first positive area \(P(D)P(+\mid D)\) and the second \(P(\bar D)P(+\mid\bar D)\).

> Turn the crowd into a rectangle. The width of each column is how common that group is. The shaded height is the chance of a positive result within that group. Multiply width by height and you get the share of the whole crowd that lands in that positive region.
>
> The teal column is narrow and almost entirely shaded. The indigo column is wide and barely shaded. In this example, their shaded areas are equal.
>
> Call having the condition D, and testing positive plus. Once we see a positive, the two shaded regions are the entire group we’re choosing from. Put the teal area on top. Put both shaded areas together on the bottom. That fraction is exactly the rule we’ve been using since we counted people.

**Visual.** Move a copy of the teal area label into the numerator, and copies of both labels into the denominator. Keep the areas visible beside the fraction until it simplifies.

$$
P(D\mid +)=
\frac{P(D)P(+\mid D)}{P(D)P(+\mid D)+P(\bar D)P(+\mid\bar D)}
=\frac{0.0099}{0.0099+0.0099}=\frac12.
$$

**Visual.** Add the **Bayes’ rule** pill once the viewer has seen where both terms came from.

## 6. Code Lab (≈ 50 s)

**Visual.** The two positive areas settle into tally counters beside a JetBrains Mono code card. Highlight the draw for condition status, then the draw for the test result, then the tally. Run the code and show **50.7%** next to **Exact: 50%**. Use a shared scale for both values.

```python
from random import Random
rng = Random(7)
positives = true_positives = 0
for _ in range(1_000_000):
    ill = rng.random() < 0.01
    rate = 0.99 if ill else 0.01
    if rng.random() < rate:
        positives += 1
        true_positives += ill
print(f"{true_positives / positives:.1%}")
```

> Here’s the same experiment in Python. The first random draw decides whether a person has the condition. That tells us which rate to use for the second draw. Whenever the test is positive, one counter goes up. The other counter only goes up if that person also has the condition.
>
> At the end we divide the true-positive count by the total number of positives. With a million simulated people, this run gives fifty point seven percent. The fraction we derived is exactly fifty percent. The simulation gives us a way to check that our counting rule behaves the way we expect. Try changing the starting rate. Watch what happens, even though the test itself stays the same.

## 7. What it means (≈ 35 s)

**Visual.** The test card becomes a **Flagged transaction** card. Keep the same two columns, now labeled **Fraud** and **Legitimate**. Keep each column’s shaded height fixed as its width changes. Reuse the amber outline for flagged transactions.

> The same question comes up when a system flags a payment as suspicious. If almost all payments are legitimate, even a small false-alarm rate in that group can account for a large share of the flags.
>
> The starting share of real cases is called the base rate. It tells you how wide to draw the first column before you know the result. When you see a flag, ask how often it comes from each group and how big those groups were to begin with.
>
> This example is about mathematics, not diagnosis.

## 8. Challenge (≈ 28 s)

**Visual.** Return to the original test card. Keep **99% positive with the condition** and **1% positive without it** pinned in place. Change **1% have the condition** to **0.1%**. Put a question mark in the positive tray. Hold the card long enough to read, then show the end card with the logo and **Answer · worked example · Python**.

> Your turn. Keep the same test, but suppose only zero point one percent of the people being tested have the condition. Among people who test positive, what fraction now have it?
>
> Start with a crowd. Count the two ways to get a positive result, then see what share comes from the group with the condition. The worked answer is on Aram Code Lab. The link is in the description.

**Description link.** [The test is positive. Am I ill?](https://aramcodelab.pythonanywhere.com/articles/positive-test-am-i-ill/). The answer is in “Everything depends on the base rate.”

---

### Checked numbers

Production notes. Keep the challenge answer below out of the narration and end card.

- **Baseline.** Exact rational arithmetic gives the four probabilities in the order true positive, false negative, false positive, true negative: \((99,1,99,9801)/10000\). This gives 100 people with the condition, 9,900 without it, 198 positives, and \(99/198=1/2\). Both shaded rectangle areas are \(99/10000=0.0099\). The 100-by-100 grid has 10,000 positions.
- **Grid experiment.** Python’s `Random(7)`, using two draws per person, gives \((107,0,97,9796)\) over 10,000 people: 204 positives and \(107/204=52.45098\ldots\%\), shown as 52.5%. This is one simulated sample. The exact counts above are expectations for the same model.
- **Code Lab.** The displayed snippet was run as written. The four counts over 1,000,000 people were \((10098,86,9809,980007)\), so \(10098/19907=50.72588\ldots\%\), printed as 50.7%. Exact expected counts are \((9900,100,9900,980100)\), giving 50%. The empirical positive rates within the two groups were 99.16% and 0.99%, compared with the input rates of 99% and 1%.
- **Challenge.** At a base rate of 0.1%, exact expected counts per 100,000 are \((99,1,999,98901)\). Thus \(99/(99+999)=11/122=9.01639\ldots\%\), displayed on the site as 9.0%. A separate run with the base rate changed to 0.001 and `Random(17)` for 1,000,000 people gives \((985,6,10015,988994)\): \(985/11000\approx8.95\%\).
