"""Narration and chapter cues from the approved Lesson 3 script."""

ENGINE = 'orpheus'
VOICE = 'tara'

CHAPTERS = [('welcome', 'Welcome'),
 ('pairs', 'Counting pairs'),
 ('multiplets', 'Successive choices'),
 ('cards_lamp', 'Cards, lamps, balls and dice'),
 ('flag_slots', 'Flags on poles'),
 ('sample_order', 'Ordered samples'),
 ('permutations', 'Permutations'),
 ('type_pieces', 'Letters and pieces of type'),
 ('uniform_sample', 'Random samples'),
 ('include_without', 'Will a particular element appear?'),
 ('no_repeat', 'No repetition'),
 ('occupancy', 'Accidents, dice and elevators'),
 ('birthday_model', 'The birthday problem'),
 ('code', 'Code Lab'),
 ('recall', 'Key ideas')]

SEGMENTS = [('welcome',
  'Welcome back. Last time we saw how probability becomes a fraction when every outcome is equally '
  "likely. Today we'll work on the two counts in that fraction. A few rules will take us from a "
  'deck of cards to a room full of birthdays.'),
 ('recap',
  "Remember the dice trap? There are eleven possible sums, but they aren't equally likely. Six of "
  'the thirty-six ordered pairs give a sum of seven. So the chance is one sixth. Before you count, '
  'decide what a single outcome represents and why the outcomes you count should have equal '
  'weight.'),
 ('pairs',
  'Say you have two shirts and three hats. How many outfits use one of each? Put the shirts down '
  "the side of a table and the hats across the top. Each shirt has three possible partners. That's "
  'two times three, so six outfits.'),
 ('pair_table',
  'Now call the group sizes m and n. The pair with the j-th shirt and the k-th hat goes in row j, '
  'column k. Every pair goes in exactly one cell, and every cell gives a pair. So there are m '
  'times n pairs.'),
 ('multiplets',
  'What if an order has a starter, a main dish and a dessert? With three starters and two mains, '
  'we have six starter and main pairs. Treat each pair as a single choice and attach any of four '
  'desserts. That gives twenty-four meals. To go further, repeat the same step. Each time you add '
  "a group, multiply by its size. For r groups, that's n one times n two, all the way through n "
  'r.'),
 ('fixed_counts',
  "The rule also works when a choice changes what's available later. The starter might change "
  'which mains the restaurant offers you. As long as each starter still has exactly two mains, and '
  'each starter and main pair still has four desserts, the count stays the same. At step k, the '
  'number of options has to be fixed. The options themselves can change. If the count changes too, '
  'count the different branches separately.'),
 ('cards_lamp',
  'In a standard deck, each card has one of four suits and one of thirteen ranks, for fifty-two '
  'cards. Now take a lamp with two switches. One selects how many of its three bulbs are on. The '
  'other sets the indirect light. Each switch has four settings, including zero. There are sixteen '
  'pairs of settings, and both at zero means off. That leaves fifteen ways to use the lamp.'),
 ('balls_cells',
  'For the labelled balls from our first lesson, record the cell chosen by each ball in order. '
  'Each of r balls has n cells to choose from, so there are n to the power r arrangements. Three '
  'balls and three cells give three times three times three, or twenty-seven.'),
 ('no_ace',
  'An ace on a die means a one. When you roll a fair die r times, there are six to the power r '
  'equally likely sequences. Avoid the ace, and there are only five choices per roll. Divide those '
  'counts and you get five sixths to the power r. To get at least one ace in six rolls, subtract '
  'the no-ace probability from one. The answer is about sixty-six and a half percent, a little '
  'under two thirds.'),
 ('flag_slots',
  'Hang three different flags on three poles. Top to bottom matters on each pole. The first flag '
  'has three places to go. Wherever it lands, its old slot becomes two slots, one above it and one '
  'below it. So the next flag has four choices. Placing that flag splits another slot, and now '
  'there are five.'),
 ('flag_count',
  'That gives sixty displays. Every finished display tells you where the last flag went. Remove '
  'that flag and you can work backwards through the earlier decisions. So each display gets '
  'counted once. With n poles and r flags, the product starts at n and goes up to n plus r minus '
  'one.'),
 ('sample_order',
  "A population is the group we're drawing from. Draw some elements and write them down in draw "
  "order. That's an ordered sample. A, B, C and B, A, C count separately. Even with the same "
  'elements, the first two positions tell different stories.'),
 ('replacement',
  'With replacement, put each element back after recording it. A repeat is possible, and each of '
  'the three slots still has five choices. That gives a hundred twenty-five sequences. Without '
  'replacement, the chosen element stays out. The available counts drop from five to four to '
  'three, giving sixty sequences.'),
 ('falling_product',
  'In general, with replacement the count is n to the power r. Without replacement, multiply n '
  'times n minus one, down to n minus r plus one. We write that product as n sub r. If you ask for '
  'more elements than the population contains, there are zero samples without replacement. If you '
  'ask for no elements, the empty sequence is the only sample.'),
 ('permutations',
  "Now draw until the population is empty. The sample contains every element once. It's a "
  'permutation, which just means a reordering. With three tiles, you have three choices for the '
  'first tile, two for the second, and the last tile goes in the remaining spot. That makes six '
  'permutations. In general we multiply down to one and call that n factorial.'),
 ('type_pieces',
  'From an alphabet of twenty-six letters, you can make twenty-six to the power ten strings of '
  'length ten. Now picture a printer with a thousand pieces of type for each letter. Two pieces '
  "may print the same letter, and they're still different pieces. Draw ten of those pieces without "
  "replacement. There are twenty-six thousand sub ten possible sequences of pieces. That's more "
  'than ten to the power forty-four. Compared with twenty-six thousand to the power ten, the '
  'difference is tiny. Taking out a few pieces barely changes the size of the pool.'),
 ('uniform_sample',
  'A random sample here means every possible ordered sample has the same probability. To get that '
  "model, choose uniformly from what's available at each draw. If we return each of the five "
  'tiles, any particular three-draw sequence has probability one over a hundred twenty-five. If we '
  'keep the tiles out, each allowable sequence has probability one over sixty.'),
 ('survey_order',
  'In a survey of smokers you may only report how many people said yes. Still, you can imagine '
  'interviewing them one by one. "The third person interviewed" is a particular person, and '
  'choosing uniformly at each draw gives every interview order the same weight. When the sample is '
  'small compared with the population, the two sampling procedures give nearly the same counts, '
  'just as they did for the printer.'),
 ('include_without',
  "What's the chance that a particular tile appears? Draw three out of five without replacement. "
  "It's easier to count the sequences that miss our tile. Those draws have to come from the other "
  'four tiles, giving twenty-four miss sequences out of sixty. Subtract that fraction from one and '
  'you get three fifths. In the general ratio, the factors shared by the two products cancel. The '
  'chance of missing the tile is n minus r, divided by n. So the chance of including it is r over '
  'n.'),
 ('include_with',
  'Return whichever tile you draw, and the count changes. Each draw has four choices that miss our '
  'tile, so there are sixty-four miss sequences out of a hundred twenty-five. The inclusion chance '
  'drops to sixty-one over a hundred twenty-five. In general, the miss probability is one minus '
  'one over n, all raised to the power r. Subtract that from one to get the chance of seeing the '
  'tile at least once.'),
 ('no_repeat',
  'Now keep replacement in the experiment, and ask whether all the draws happen to be different. '
  'Each repeat-free sequence could have come from drawing without replacement, so there are n sub '
  'r of them. Divide by n to the power r. You can divide each factor on top by n. The first factor '
  'becomes one. Then come one minus one over n, one minus two over n, and so on.'),
 ('random_digits',
  'Draw five random digits. Repeats are allowed, and only about thirty percent of the sequences '
  'have five different digits. For a comparison, take the first two thousand five hundred digits '
  'after the decimal point of e, in groups of five. A hundred fifty of those five hundred groups '
  "have all different digits. That's close to the random model for this test. The digits of e "
  'themselves come from a fixed number.'),
 ('occupancy',
  'If the numbers of balls and cells match, filling every cell means putting exactly one ball in '
  'each. Each ball chooses a cell independently and uniformly. We count all arrangements by giving '
  'each ball n choices. The successful arrangements are the n factorial ways to put different '
  'balls in different cells.'),
 ('accidents_dice',
  'Imagine exactly seven accidents each week, with their days independently and uniformly '
  'assigned. Exactly one accident on each day is rare: about once in a hundred sixty-three weeks '
  'on average in this model. With six rolls of a fair die, seeing each face exactly once has '
  'probability about one and a half percent.'),
 ('elevator',
  'An elevator has seven passengers and stops at ten floors. Suppose each passenger chooses '
  'independently and all floors are equally likely. We want different floors, so the favourable '
  'count has ten choices for the first passenger, nine for the second, down to four for the last. '
  'Divide by ten to the power seven. The probability is roughly six percent.'),
 ('birthday_model',
  'Imagine a room full of people. How many do you need before a shared birthday is more likely '
  'than none? Use a year with three hundred sixty-five days. Ignore leap days and seasonal '
  "differences, and treat the people's birthdays as independent. Count the opposite event first. "
  "For everyone's birthday to be different, the next person has to avoid every date we've already "
  'used. For the second person the factor is one minus one over three hundred sixty-five. For the '
  "third it's one minus two over three hundred sixty-five. Multiply these factors through the last "
  'person.'),
 ('birthday_crossing',
  "The chance of no match keeps falling as more people join. With twenty-two people it's still "
  "above one half. With twenty-three it's below one half for the first time. So a shared birthday "
  'is already slightly more likely than no shared birthday. With thirty people, the chance that '
  'everyone has a different birthday is under thirty percent.'),
 ('birthday_log',
  "Here's a shortcut. Logs turn that long product into a sum. For a small x, the log of one minus "
  'x is close to minus x. Add the integers from one to r minus one, then divide by three hundred '
  'sixty-five and put a minus sign in front. With thirty people, this shortcut gives about zero '
  'point three zero four. The exact product gives about zero point two nine four.'),
 ('birthday_pairs',
  'The same sum counts pairs of people. With twenty-three people there are two hundred fifty-three '
  "pairs, and each pair has a one in three hundred sixty-five chance of a match. We're checking "
  'every pair in the room, not just checking who shares your birthday. Adding the pair '
  'probabilities would count some rooms more than once, so use the product for the exact answer.'),
 ('code',
  "Let's simulate a hundred thousand groups of twenty-three people in Python. The random generator "
  'picks a day for each person. A set keeps each day only once. If the set has fewer entries than '
  'there are people, we count a match in that group. For the exact answer, multiply the factors '
  'for all birthdays being different and take the complement.'),
 ('code_result',
  'The simulation gives point five zero six five. The exact product gives point five zero seven '
  'three after rounding. Both put the chance just above one half. Try changing the number of '
  'people. With one extra person, every existing person gets a new partner to compare birthdays '
  'with.'),
 ('recall',
  'Before we finish, pause and see if you can explain when to multiply and when a choice gets '
  'removed.'),
 ('ideas',
  'Multiply the choice counts if each step has a fixed number of options. With replacement, the '
  'count stays the same at each draw. Without replacement, it drops by one. Draw everything '
  'without replacement and you have a permutation. In a uniform ordered sample, every allowable '
  'sequence has the same probability.'),
 ('end',
  "The full section and exercises are on Aram Code Lab. Next time we'll count subpopulations, "
  'where only membership matters. That will give us the binomial coefficients.')]
