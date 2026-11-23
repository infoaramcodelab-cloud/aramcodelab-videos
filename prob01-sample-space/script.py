"""Lesson 1 v2 narration, split at visual cues from SCRIPT.md."""

ENGINE = 'orpheus'   # lib/orpheus_voice.py (Kokoro: lib/narrate.py voice)
VOICE = 'tara'
SPEED = 0.90

CHAPTERS = [('welcome', 'Welcome'),
 ('model_intro', 'Why a model first'),
 ('dice_intro', 'Simple and compound events'),
 ('definition', 'Sample points and the sample space'),
 ('cells', 'Three balls in three cells'),
 ('formula', 'One scheme, many stories'),
 ('collapse', 'Distinguishable or not'),
 ('smokers', 'Sampling: counting smokers'),
 ('three_coins', 'Three coins'),
 ('axes', 'The ages of a couple'),
 ('bridge', 'Bridge and aces'),
 ('events_equal', 'The algebra of events'),
 ('identity_one', 'Four identities and a trap'),
 ('discrete_row', 'Discrete spaces and a tournament'),
 ('code', 'Code Lab'),
 ('recall', 'Key ideas')]

SEGMENTS = [('welcome',
  "Welcome to the first lesson of a course in probability theory. It's about discrete "
  'probability: coins, dice, cards, random walks, and the surprising laws that appear '
  'when an experiment is repeated many times.'),
 ('site',
  "Every lesson matches a section on Aram Code Lab. There you'll find the full text, the proofs, the "
  'problems with solutions, and Python code you can run in your browser. The link is in the '
  'description.'),
 ('question',
  'Before we compute a single probability, we have to answer a simpler question. Probability of what?'),
 ('model_intro',
  'Probability becomes useful when we apply it to concrete experiments, real or imagined. We toss a '
  'coin, throw dice, deal cards, pick people at random from a population, or count the calls arriving '
  'at a telephone exchange. Each description stays vague until we agree on one thing: what exactly '
  'counts as a possible outcome?'),
 ('coin',
  "Every theory idealizes. A real coin can land on its edge. We agree that it can't, so the only "
  'results are heads and tails.'),
 ('age',
  "Nobody's age can be measured exactly, but we treat it as an exact number. These conventions don't "
  'make the theory less useful. They are what makes a mathematical model possible in the first place.'),
 ('dice_intro',
  'We call the results of an experiment events. Some events can be split into simpler ones, and others '
  "can't."),
 ('dice_sum',
  'Throw two dice. The event "the sum is six" really means that the throw was one of five results: one '
  "and five, two and four, three and three, four and two, or five and one. It's a compound event made "
  'of five simple ones.'),
 ('dice_odd',
  'Now look at three-three. It also makes another event happen: "both faces are odd". So compound '
  'events can occur together. Simple events never can. Each throw produces exactly one of them.'),
 ('definition',
  'Here is the first definition of the course. The simple, indecomposable outcomes of an idealized '
  'experiment are called sample points, or just points. Every possible outcome is represented by one '
  'and only one point. The set of all points is the sample space, written with the Greek letter Omega. '
  'And an event is simply a set of sample points.'),
 ('geometry',
  'Think of the sample space like "point" and "line" in geometry. It\'s a primitive notion. The theory '
  'starts only after the sample space has been chosen. An event makes sense only if, for every '
  'outcome, we can say whether it happened. Then the event is just the set of points where it did. And '
  'we never talk about a probability without saying which sample space we mean.'),
 ('cells',
  "Here's an example we'll use again and again. Place three different balls, a, b and c, into three "
  'cells. Ball a has three choices. So does b, and so does c. That gives three times three times '
  'three, twenty-seven arrangements. Each arrangement is one sample point.'),
 ('grid',
  'Here they all are. Points one to three put all three balls into one cell. Points four to twenty-one '
  'put two balls into one cell and the third ball elsewhere. And points twenty-two to twenty-seven '
  'spread the balls out, one in each cell.'),
 ('event_crowded',
  'Now every statement about the experiment becomes a set of points. "Some cell holds at least two '
  'balls" is points one to twenty-one.'),
 ('event_first',
  '"The first cell is not empty" is point one, points four to fifteen, and points twenty-two to '
  'twenty-seven: nineteen points.'),
 ('event_full', '"Every cell is occupied" is just the last six.'),
 ('event_first_empty',
  '"The first cell is empty and some cell has two balls" is points two and three and sixteen to '
  'twenty-one, eight points.'),
 ('event_empty',
  'And "every cell holds two balls"? Three balls can\'t do that. No point qualifies, and the event is '
  'empty. We call it the impossible event.'),
 ('formula',
  'In general, r different balls can be placed into n cells in n to the power r ways. Four balls in '
  'three cells give eighty-one points. Ten balls in ten cells give ten to the tenth, ten billion.'),
 ('schemes',
  "The nature of the points doesn't matter. Only the structure does. The same scheme describes many "
  'different stories. With birthdays, the people are the balls and the three hundred sixty-five days '
  'are the cells. Throwing r dice is placing r balls into six cells, and a coin has just two cells. '
  'Passengers leaving an elevator choose floors. Random digits distribute positions among the ten '
  'digits. When bridge is dealt, the four aces fall to four players. And misprints land on the pages '
  'of a book.'),
 ('scheme_caution',
  'All these problems are the same abstract problem in different words. One caution, though: the right '
  "probabilities are not always the same. That's the topic of the next lesson."),
 ('collapse',
  'Now stop telling the balls apart. Arrangements four, five and six used to be different: a and b in '
  'the first cell, or a and c, or b and c. Without labels, they all look the same: two balls in the '
  'first cell and one in the second. The twenty-seven points collapse to just ten.'),
 ('model_choice',
  "Can real balls be told apart? It doesn't matter. Distinguishing them or not is our choice of model. "
  "The four aces in bridge are certainly different cards, yet it's often convenient to treat them as "
  "identical. Again, the theory begins only after we've made this choice."),
 ('smokers',
  'A sampling example. We ask a hundred people whether they smoke, and record only the number of '
  'smokers. The sample space is the numbers from zero to a hundred: a hundred and one points.'),
 ('majority', '"The majority are smokers" is the event fifty-one up to a hundred.'),
 ('quadruples',
  'If we also record sex, a point becomes four numbers: male smokers, female smokers, male non-smokers '
  'and female non-smokers, adding up to a hundred. There are a hundred seventy-six thousand eight '
  "hundred fifty-one such quadruples. We'll learn to count them in the next chapter. The point is that "
  'the same survey gives different sample spaces depending on what we record.'),
 ('three_coins', 'Toss a coin three times. The sample space has eight points.'),
 ('heads_event', '"Two or more heads" is the first four.'),
 ('tail_event',
  '"Exactly one tail" is three of them: HHT, HTH and THH. Notice that the second event is inside the '
  "first. We'll name that relation in a minute."),
 ('axes',
  "Events don't have to be finite lists. Let x be a husband's age and y his wife's age. A sample point "
  'is a pair x, y of positive numbers: a point in the first quadrant of the plane.'),
 ('age_a',
  '"The husband is older than forty" is everything to the right of the vertical line x equals forty.'),
 ('age_b', '"The husband is older than his wife" is everything below the diagonal.'),
 ('age_c',
  '"The wife is older than forty" is everything above the horizontal line y equals forty. Each event '
  'is a region, and relations between events become relations between regions you can see.'),
 ('age_ab',
  'For example, "the husband is over forty and older than his wife" is where the first two regions '
  'overlap.'),
 ('bridge',
  'One more example. Deal fifty-two cards to four bridge players, North, East, South and West, '
  'thirteen each. Let N one be the event that North has at least one ace, and the same for the '
  'others.'),
 ('bridge_union',
  'The union of the four events is the whole sample space, because somebody always holds an ace.'),
 ('bridge_all',
  'And the event that all four happen together means that every player has exactly one ace.'),
 ('events_equal',
  'Once events are sets, the language of events is the language of sets. Fix a sample space. Two '
  'events are equal if they contain the same points.'),
 ('empty', 'An event with no points is impossible, and we write it as the empty set.'),
 ('complement',
  'The event "A does not occur" contains all the points not in A. It\'s called the complement of A, '
  'and we write A prime. The complement of the whole space is the empty set.'),
 ('intersection',
  '"Both A and B occur" is the intersection: the points in both. In probability we usually write it as a product, A B, '
  'and so will we.'),
 ('union', '"At least one of them occurs" is the union. The same works for any number of events.'),
 ('exclusive',
  'And events are mutually exclusive if no two of them have a point in common: they can never happen '
  'together.'),
 ('implies',
  'If every point of A is also in B, we write A is contained in B, and say "A implies B". Whenever A '
  'happens, B happens too.'),
 ('coin_implies', 'In the coin example, "exactly one tail" implies "two or more heads".'),
 ('difference', 'In that case B minus A means "B happens but A doesn\'t".'),
 ('omega_difference', 'For instance, the complement of A is Omega minus A.'),
 ('exclusive_implies',
  'If A and B are mutually exclusive, then A is contained in the complement of B.'),
 ('a_not_both', 'And A minus AB means "A, but not both".'),
 ('identity_one',
  'Four identities are worth knowing. "Neither A nor B" is the same as "not A and not B".'),
 ('identity_two', '"Not both" is the same as "not A or not B".'),
 ('identity_three', '"A but not both" is A together with the complement of B.'),
 ('identity_four',
  'And the union of A and B splits into A and the part of B outside A. Those two pieces never overlap, '
  'which will matter when we add probabilities.'),
 ('identity_proof',
  'How do we prove them? Just check points. A point lies outside the union exactly when it lies '
  "outside A and outside B. That's the first identity. The others work the same way, and you'll find "
  'them in the problems.'),
 ('trap',
  'Watch the order of operations. The complement of a union is not the union of the complements, and '
  'the complement of an intersection is not the intersection of the complements. The pictures make the '
  'difference obvious.'),
 ('discrete_row',
  'So far our sample spaces were finite. Sometimes we need infinitely many points. Toss a coin until '
  'the first head appears. The outcomes are H, TH, TTH, and so on, without end. We might also add a '
  'point E zero for "heads never appears".'),
 ('discrete_definition',
  'A sample space is called discrete if it is finite, or if its points can be arranged in a sequence, '
  'E one, E two, E three, and so on.'),
 ('tournament',
  "Here's a richer example. Three players, a, b and c, play games with no draws. First a plays b while "
  'c waits. The loser is replaced by c, the winner plays c, and so on. The tournament ends as soon as '
  'someone wins two games in a row.'),
 ('tournament_outcomes',
  'Write down the winner of each game, and you get the possible outcomes. a a: a wins twice. a c c: a '
  'wins, then c beats a and then b. Then a c b b, a c b a a, and so on, and the same list starting '
  'with b.'),
 ('tournament_endless',
  'There are also two endless sequences in which nobody ever wins twice in a row.'),
 ('tournament_list',
  'Is this sample space discrete? Yes. List the two endless sequences first, then a a, b b, a c c, b c '
  'c, and so on. Every point gets a number. On the site we put probabilities on this tournament in the '
  'problems.'),
 ('discrete_caution',
  'Not every sample space is discrete. The ages of a couple form a region of the plane, and its points '
  "can't be put into a sequence. In discrete spaces, probabilities of events are sums. In general they "
  'would need integrals. In this course we work only with discrete spaces.'),
 ('code',
  'In Python, a sample point is a tuple holding the cell of ball a, ball b and ball c. The product '
  'function lists all twenty-seven. Events are sets built with a condition. A set of cells with fewer '
  'than three elements means that two balls share a cell. We get the same counts as before: '
  'twenty-one, six and nineteen.'),
 ('code_check',
  'The last line checks the first identity on real sets. Take A as "crowded" and B as "ball a is in '
  'the first cell". The points outside both form a set of four points, and the comparison says True. '
  'Try changing the events and checking the other identities yourself.'),
 ('recall', 'Before we finish, pause the video and try to recall the main ideas of this lesson.'),
 ('ideas',
  'Each elementary outcome is one sample point, and an event is a set of points of the sample space. A '
  'B means both events occur, A union B means at least one does, and mutually exclusive events have no '
  'common point. The complement of A holds everything outside A, and the complement of a union is the '
  'intersection of the complements.'),
 ('end',
  'The full section, with all the examples and the problems, is on Aram Code Lab. The link is in the '
  'description. Next time, we put probabilities on these points.')]
