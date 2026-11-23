"""Narration for "The Arc Sine Law" (flagship version). Approved draft: SCRIPT.md."""
VOICE = 'am_puck'
SPEED = 0.92

SEGMENTS = [
    # 1. cold open
    ('c1', "Here are eight games of coin tossing. A fair coin, a thousand tosses each."),
    ('c2', "In six of them, one player was ahead for at least eighty percent of the game."),
    ('c3', "In one, Bob led from the very first toss to the very last."),
    ('c4', "Nothing is wrong with the coin. This is what fairness actually looks like. "
           "And by the end of this video, you will be able to compute exactly how often it happens."),
    # 2. the puzzle
    ('p1', "Alice and Bob toss a fair coin. Heads, Alice gets a point. Tails, Bob does."),
    ('p2', "We follow one number: Alice's score minus Bob's. Each toss moves it one step up, or one step down. "
           "Above the line, Alice is ahead. Below it, Bob is ahead."),
    ('p3', "Here is the question. Play a thousand tosses, and record what fraction of the time Alice was ahead. "
           "Repeat this many times. Which picture do you expect for those fractions? "
           "A hill around one half? Something flat? Or a valley?"),
    ('p4', "Take a moment, and make a guess."),
    ('p5', "Most people choose the hill. The coin is fair, so surely each player leads about half the time."),
    # 3. the experiment
    ('e1', "Let's not argue. Let's play. Each game ends with one number, the fraction of time Alice led, "
           "and that number drops into its bin."),
    ('e2', "Ten games. A hundred. Ten thousand."),
    ('e3', "It is not a hill. It is a valley. The most likely outcomes are the most lopsided ones: "
           "Alice leads almost the whole game, or almost none of it."),
    ('e4', "A fair looking split, between forty and sixty percent, happens only about thirteen percent of the time."),
    ('e5', "And with probability about forty one percent, one of the players is ahead "
           "for more than ninety percent of the game."),
    ('e6', "Why? To understand it, we need one beautiful trick."),
    # 4. reflection
    ('r1', "Take any path that starts above zero and ends above zero, but touches zero somewhere in between."),
    ('r2', "Reflect everything up to the first touch in the axis. "
           "You get a path that starts below zero, and ends where the original ended."),
    ('r3', "This works in both directions. Every path from below must cross zero, and reflecting it back "
           "gives a touching path from above. So the touching paths, and the paths from the mirror image start, "
           "are in one to one correspondence. That is the reflection principle."),
    ('r4', "Now we can count the games in which the score never returns to zero. Split them by where they end. "
           "For each final level, reflection tells us how many paths sneak back to zero, and we subtract them."),
    ('r5', "Something lovely happens when we add these up. Almost everything cancels, like a collapsing telescope, "
           "and a single term is left."),
    ('r6', "The result: the probability that the score never returns to zero in two n tosses "
           "is exactly the same as the probability that it is level at time two n. "
           "We call this number u two n. It is a simple binomial probability."),
    ('r7', "And u two n shrinks slowly, like one over the square root of pi n. "
           "After a thousand tosses, it is still about two and a half percent. "
           "Returns to zero are rare, and they get rarer as the game goes on."),
    # 5. the last tie
    ('l1', "Here is where it all comes together. Ask: when was the last time the score was tied?"),
    ('l2', "Cut the game at the last tie, at time two k. "
           "Before the cut, the path goes from zero back to zero. Probability: u two k."),
    ('l3', "After the cut, it never returns to zero. By our lemma, probability: u of two n minus two k."),
    ('l4', "So the probability that the last tie happens at time two k is u two k, times u two n minus two k. "
           "Each factor is large when its piece is short, so the product is largest at the two ends."),
    ('l5', "The last tie is most likely to happen either very early, or very late."),
    ('l6', "And here is the surprise. The fraction of time Alice spends in the lead has exactly the same distribution. "
           "The proof of that takes a little more work. It is written out in full on our site."),
    # 6. bars to a curve
    ('b1', "Now let the game grow. Use the estimate: u two m is about one over the square root of pi m, "
           "and set x equal to k over n."),
    ('b2', "The bars settle onto a single curve: one over pi, times one over the square root of x times one minus x."),
    ('b3', "The area under this curve, from zero to x, is two over pi, times the arc sine of the square root of x. "
           "That is the arc sine law, and it is where the name comes from."),
    # 7. code lab
    ('k1', "You do not have to trust me. Here are ten lines of Python."),
    ('k2', "One game counts the steps on which Alice is ahead. We play ten thousand games, "
           "and ask how often someone leads more than ninety percent of the time."),
    ('k3', "About forty one percent, just as the formula says. "
           "You can run this code right in your browser on Aram Code Lab, and change it."),
    # 8. what it means
    ('m1', "So the next time someone has been ahead for a long time, in a game, in a season, "
           "in a contest decided by luck, remember: long leads are exactly what pure chance produces."),
    ('m2', "The coin has no memory. But the score does."),
    # 9. challenge
    ('z1', "Here is a challenge for you, and it uses the reflection trick. "
           "In an election, candidate A gets sixty votes, and B gets forty. The votes are counted in random order. "
           "What is the probability that A is strictly ahead during the whole count?"),
    ('z2', "The answer and its solution are on Aram Code Lab. The link is in the description."),
]
