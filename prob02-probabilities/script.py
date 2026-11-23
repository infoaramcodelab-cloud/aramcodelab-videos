"""Lesson 2 narration and chapter cues from SCRIPT.md."""

ENGINE = 'orpheus'
VOICE = 'tara'

CHAPTERS = [
    ('welcome', 'Welcome'),
    ('like_lengths', 'Numbers like lengths and masses'),
    ('mb_intro', 'Same balls, model one'),
    ('be_collapse', 'Same balls, model two'),
    ('frequency_idea', 'What frequencies say'),
    ('convention', 'The rules'),
    ('event_sum', 'Adding over an event'),
    ('union_question', 'Probability of a union'),
    ('dice_union', 'Unions with dice'),
    ('exclusive_add', "Boole's inequality"),
    ('classical', 'Equally likely points'),
    ('sums_trap', 'A trap with two dice'),
    ('code', 'Code Lab'),
    ('recall', 'Key ideas'),
]

SEGMENTS = [
    ('welcome',
     'Welcome back. In the first lesson we built sample spaces. Every possible outcome became a point, '
     'and every event became a set of points. Three balls in three cells gave us twenty-seven points. Two '
     'dice gave us thirty-six.'),
    ('recap',
     "But we never said how likely anything is. That's today's job. We'll put probabilities on the "
     "points, and we'll learn the first rules for combining them. And we'll see something surprising: the "
     'same sample space can carry very different probabilities.'),
    ('like_lengths',
     "So what is a probability? Think of geometry. Geometry doesn't tell you how to measure the length of "
     'a real table. It assumes lengths are given and studies how they fit together. Mechanics does the '
     "same with masses. Probability theory treats probabilities the same way. They're numbers we're "
     'given, and the theory studies how they combine. How to find them in the real world is the job of '
     'applications, and of statistics.'),
    ('fair_coin',
     'Take a fair coin. We give heads probability one half, and tails probability one half. Toss it three '
     'times, and each of the eight outcomes gets probability one eighth. With n tosses, all two to the n '
     'outcomes get the same probability.'),
    ('model_use',
     'Is that true of a real coin? Not exactly. No coin is perfectly fair. "Fair" is a convention, a '
     "model. But it's a useful model, for two reasons. It describes real coins well enough. And when "
     'reality departs from it, the departure itself tells us something: maybe the coin is loaded, or the '
     "deck wasn't shuffled properly."),
    ('mb_intro',
     "Let's go back to three balls in three cells. The balls are different: a, b and c. Each ball lands "
     "in a cell, and nothing favours one arrangement over another. So it's natural to give each of the "
     'twenty-seven points the same probability, one over twenty-seven. In physics this is called the '
     "Maxwell–Boltzmann model. It's a good first model for birthdays, for passengers leaving an elevator, "
     'and for collecting coupons.'),
    ('mb_events',
     'Now every event from last time gets a number. "Some cell has at least two balls" covered twenty-one '
     'points, so its probability is twenty-one over twenty-seven, which is seven ninths. "Every cell is '
     'occupied" had six points: two ninths. And "the first cell is not empty" had nineteen points, so '
     'nineteen over twenty-seven. Counting points is all it takes, because every point weighs the same.'),
    ('be_collapse',
     "Now let's stop telling the balls apart. As we saw last time, the twenty-seven arrangements collapse "
     'into just ten configurations.'),
    ('be_weights',
     'If we keep the probabilities from the twenty-seven arrangements, these ten configurations are not '
     'equally likely. "All three in one cell" comes from a single arrangement, so it has probability one '
     'over twenty-seven. "Two in one cell and one in another" comes from three arrangements, so three '
     'over twenty-seven, one ninth. And "one ball in each cell" comes from six arrangements: two ninths. '
     'Check the total: three times one over twenty-seven, plus six times one ninth, plus two ninths. '
     "That's exactly one."),
    ('be_equal',
     "But here's another choice. Why not give all ten configurations the same probability, one tenth "
     "each? It looks artificial. And yet it's exactly how certain elementary particles behave. Physicists "
     'call it Bose–Einstein statistics.'),
    ('be_compare',
     'The two models really disagree. The chance that every cell is occupied is two ninths in the first '
     'model, about twenty-two percent, and only one tenth in the second. The chance that all three balls '
     'share a cell is one ninth against three tenths. Almost three times bigger!'),
    ('be_lesson',
     'Both models are mathematically correct. Which one fits a real situation is a question of '
     "experience, not of logic. So here's the lesson: the sample space alone doesn't decide the "
     'probabilities. We have to choose them, and the choice is part of the model.'),
    ('frequency_idea',
     'What does "probability one half" mean in the real world? The frequency interpretation says this: '
     'repeat the experiment many times, and the fraction of trials in which A happens should be close to '
     'the probability of A.'),
    ('frequency_run',
     'Here are ten thousand simulated coin tosses. After ten tosses we have four heads. After a hundred, '
     'fifty-seven. After a thousand, five hundred twenty-five. And after ten thousand, four thousand nine '
     'hundred eighty-nine. The fraction settles down, very close to one half.'),
    ('frequency_groups',
     'But look closer. Cut the same tosses into a hundred groups of a hundred. One group has only '
     'thirty-seven heads, another has sixty-three. Only seventy-two groups out of a hundred land between '
     'forty-five and fifty-five. Swings like these are completely normal. So how do we decide whether '
     "real data agree with a model? To answer that, we need the theory itself. We'll get there later in "
     'the course.'),
    ('convention',
     "Now let's write the rules down. Take a discrete sample space with points E one, E two, and so on. "
     'To each point we assign a number, its probability. These numbers are never negative, and together '
     "they add up to exactly one. That's the fundamental convention of the whole course."),
    ('zero_points',
     'A point is even allowed to have probability zero. In a discrete space we could simply remove such '
     "points. But often we don't know in advance which outcomes are really possible. Remember the "
     'tournament from last time, with its two endless games where nobody ever wins twice in a row? We '
     'kept them as points. In the problems on the site it turns out that they have probability zero.'),
    ('event_sum',
     "And here's the definition that ties everything together. The probability of an event A is the sum "
     "of the probabilities of all the points in A. That's it. An event is a set of points, so its "
     'probability is the total weight of those points.'),
    ('consequences',
     'Three facts follow at once. The whole sample space contains every point, so its probability is one. '
     'The empty set contains no points, so its probability is zero. And any other event collects some of '
     'the weight, never negative and never more than the total, so its probability lies between zero and '
     'one.'),
    ('union_question',
     "Now the first real question. What's the probability that A one or A two happens, at least one of "
     'them? We need the probabilities of all the points in the union, each point counted once.'),
    ('union_overcount',
     'What if we simply add the two probabilities? Every point that lies only in A one is counted once. '
     'Every point that lies only in A two is counted once. But a point in the overlap, in both events, is '
     'counted twice. So the plain sum can only be too big, never too small.'),
    ('union_theorem',
     'The fix is easy. Every point of the overlap was counted exactly one time too many, so we subtract '
     'the overlap once. The probability of the union is the probability of A one, plus the probability of '
     'A two, minus the probability that both happen. And that short argument is the complete proof of the '
     'first theorem of the course.'),
    ('union_coins',
     'Let\'s try it. Toss a coin twice. The four outcomes each have probability one quarter. "Heads on the '
     'first toss" is H H and H T: probability one half. "Heads on the second toss" is H H and T H: also '
     'one half. Does "at least one head" have probability one half plus one half, which is one? Of course '
     "not. H H was counted twice. Subtract its quarter, and the answer is three quarters. And that's "
     'right: only T T is missing.'),
    ('dice_union',
     'One more, with two dice, using the two events from last time. "The sum is six" has five points, so '
     'probability five over thirty-six. "Both faces odd" has nine points: nine over thirty-six. They '
     'share three points: one and five, three and three, five and one. So the probability that the sum is '
     'six, or both faces are odd, is five plus nine minus three, over thirty-six. Eleven over thirty-six. '
     "Count the highlighted squares, and you'll find exactly eleven."),
    ('exclusive_add',
     "When the events are mutually exclusive, there's no overlap and nothing to subtract. Then "
     'probabilities simply add.'),
    ('boole',
     'The same idea works for any number of events, even infinitely many. Add up their probabilities, and '
     'every point of the union is counted at least once, maybe more. So the probability that at least one '
     "of the events happens is at most the sum of their probabilities. This is Boole's inequality. And if "
     'the events are mutually exclusive, every point is counted exactly once, and the sum is exact.'),
    ('boole_dice',
     "Here's how it helps. Throw three dice. What's the chance of at least one six? Each die shows a six "
     "with probability one sixth, so Boole's inequality says: at most one half. The exact answer, which "
     "we'll be able to compute in a later chapter, is ninety-one over two hundred sixteen, about "
     "forty-two percent. The bound is rough, but it's instant, and it never lies. That kind of quick "
     'bound will save us many times in this course.'),
    ('classical',
     'A very common special case: the sample space has N points, and all of them are equally likely, each '
     'with probability one over N. Then the probability of any event is just the number of its points '
     'divided by N. Favourable cases over all cases.'),
    ('classical_example',
     'For two fair dice, all thirty-six points are equally likely. The sum is seven at six of them: one '
     'and six, two and five, and so on up to six and one. So the probability of a seven is six over '
     'thirty-six, one sixth.'),
    ('sums_trap',
     'Now a trap. Someone says: "The sum of two dice is one of eleven numbers, from two to twelve. So the '
     'chance of a seven is one in eleven." Favourable cases over all cases. What went wrong?'),
    ('sums_truth',
     "The eleven sums are perfectly good outcomes, but they're not equally likely. A sum of two needs a "
     'double one: just one of the thirty-six points. A sum of seven comes from six points. The classical '
     "formula only works when the points really are equally likely. Here they aren't."),
    ('classical_caution',
     "That's why the classical formula is not the definition of probability. It's only a special case. A "
     'biased coin still has two outcomes, but with probabilities p and one minus p. Boys and girls are '
     'not born exactly equally often. And we saw with the balls that "equally likely" on one sample space '
     'and on another can give different answers.'),
    ('next_chapter',
     'So the real work is to choose a sample space whose points really are equally likely. Then '
     'everything reduces to counting points. And counting, done carefully, is exactly what the next '
     'chapter is about.'),
    ('code',
     "Let's test the two models in Python. In the first model, each of the three balls picks a cell on "
     'its own. In the second, we pick one of the ten configurations, all equally likely. We ask both '
     'models the same question, a hundred thousand times: is every cell occupied?'),
    ('code_result',
     'The first model says about twenty-two percent, close to two ninths. The second says about ten '
     'percent, close to one tenth. Same balls, same cells, same question, two different answers. The '
     'model decides. Try changing the question, and see which events the two models agree on.'),
    ('recall',
     'Before we finish, pause the video and try to recall the main ideas of this lesson.'),
    ('ideas',
     'In a discrete space, we give the points non-negative probabilities that add up to one, and the '
     'probability of an event is the sum over its points. For a union of two events, add the two '
     'probabilities and subtract the overlap, which was counted twice. And a union never has more '
     'probability than the sum of its parts. For mutually exclusive events, the sum is exact.'),
    ('end',
     'The full section, with the problems, is on Aram Code Lab. The link is in the description. Next '
     'time, we start counting: ordered samples and the multiplication rule.'),
]
