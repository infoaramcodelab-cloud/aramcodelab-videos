"""Narration and chapter cues from the approved Lesson 4 script."""

ENGINE = 'orpheus'
VOICE = 'tara'

CHAPTERS = [('welcome', 'Welcome'),
 ('collapse_orders', 'Forgetting the order'),
 ('choose_complement', 'Choosing who stays'),
 ('poker_hands', 'Poker ranks and suits'),
 ('state_absent', "The senators' committee"),
 ('cell_count', 'Exactly k balls in one cell'),
 ('two_kinds', 'Arrangements of two kinds'),
 ('lattice_word', 'Shortest paths'),
 ('partition_formula', 'Partitions into labelled groups'),
 ('bridge_deals', 'An ace for each bridge player'),
 ('dice_pairs', 'Each die face exactly twice'),
 ('summary_without', 'Four ways to sample'),
 ('code', 'Code Lab'),
 ('recall', 'Key ideas')]

SEGMENTS = [('welcome',
  "Welcome back. If I shuffle the cards already in my hand, I'm still holding the same cards. But "
  "if I swap one for a card from the deck, my hand changes. Today we'll count selections where "
  'only membership matters, then use that idea to split a whole population into groups. The same '
  'question comes up when you pick a committee or deal cards to several people. What has to change '
  'before we count the result as a new outcome?'),
 ('recap',
  'Last time, we counted ordered samples. With replacement we got n to the power r. Without '
  'replacement we got n sub r. Counting ordered dates helped us see why a shared birthday is '
  "already more likely than no match with twenty-three people. Let's start with those ordered "
  'counts and see what happens when we forget the order.'),
 ('collapse_orders',
  'Take three of these five tiles. A, B, C and C, A, B are different ordered samples. They give '
  'the same subset because they contain exactly the same tiles. Any three distinct tiles can be '
  'ordered in six ways. There are sixty ordered samples, so bundle them six at a time. We get ten '
  'subsets. Now try A, B, D. That belongs in a different bundle, because D has taken the place of '
  'C. The bundles are exactly the sets we want to count.'),
 ('choose_rule',
  'In general, every subset of size r has exactly r factorial orderings. Each ordered sample comes '
  'from just one subset. So we can count the ordered samples by choosing a subset first and '
  'ordering it second. Divide the ordered count by r factorial. The result is called n choose r, '
  'the binomial coefficient.'),
 ('choose_complement',
  'Say two of five people stay and the other three leave. Tell me who stays, and I know exactly '
  'who leaves. Tell me who leaves, and I can recover the other group. Every choice on one side has '
  "one partner on the other. That's why five choose two and five choose three are both ten."),
 ('choose_factorial',
  'The falling product is the beginning of n factorial. Multiply top and bottom by the factorial '
  'of n minus r to get n factorial over r factorial times the factorial of n minus r. There is one '
  'way to take nothing, just as there is one way to take everything. Setting zero factorial to one '
  'keeps the formula working at both ends.'),
 ('poker_hands',
  'A poker hand has five cards from a standard deck of fifty-two. The deal order makes no '
  'difference once the cards are in your hand. Every five-card subset is equally likely in a fair '
  "deal. That's about two point six million hands. You could count the deal as a sequence first, "
  'but each hand would appear once for every possible order of its cards. The binomial coefficient '
  'does that division for us.'),
 ('poker_distinct',
  'To get five different ranks, choose the five ranks first. For each chosen rank there are four '
  'suits. Each completed hand tells us exactly which ranks and suits we picked. Multiply the rank '
  'count by four to the power five and divide by the total. The chance is a little over one half.'),
 ('bridge_ranks',
  'A single bridge hand has thirteen cards. There are about six hundred thirty-five billion '
  'possible hands. To get thirteen different ranks you need one card of every rank. Each rank '
  "still has four possible suits. Divide four to the power thirteen by the number of hands. That's "
  'about one chance in ten thousand.'),
 ('state_absent',
  'Imagine fifty states with two senators each. We pick a committee of fifty senators uniformly. '
  'Will your state have a seat? Count the opposite case first. Both your senators are left out, '
  'and the committee comes entirely from the other ninety-eight. The probability of missing your '
  "state is about one quarter. So the chance of representation is about three quarters. There's a "
  'quick way to see that quarter. Half the senators stay off the committee, so your first senator '
  'stays off with chance fifty out of a hundred. Then forty-nine of the other ninety-nine senators '
  'stay off, so your second one does too with chance forty-nine out of ninety-nine. Multiply, and '
  'you get just under one quarter.'),
 ('all_states',
  'Could every state have a seat? With fifty seats that means exactly one senator per state. Each '
  'state offers two choices, giving two to the power fifty such committees. That sounds huge until '
  'you divide by the number of unrestricted committees. The chance is around one in ninety '
  'trillion, even though any single state is quite likely to be represented. Getting every state '
  'in is a different question from getting any one particular state in.'),
 ('cell_count',
  "Drop three labelled balls into three cells independently and uniformly. What's the chance that "
  "this particular cell gets exactly two balls? Choose which two go there. That's three possible "
  'pairs. The remaining ball has two other cells to choose from. Six arrangements work out of '
  'twenty-seven, so the probability is two ninths. Keep your eye on the outlined cell. If we were '
  'looking for two balls in any cell, we would be counting a different event.'),
 ('cell_formula',
  'In general, choose which k of the r balls land in the given cell. Each remaining ball has n '
  'minus one choices. Divide by n to the power r to get the probability. The product form tells '
  'the same story. Each chosen ball hits the cell with probability one over n, and each remaining '
  'ball misses it. This is exactly what the binomial distribution counts.'),
 ('two_kinds',
  'Now arrange two alpha tiles and three beta tiles. Give every tile a number first. We could '
  'order the five labelled tiles in five factorial ways. For every colour pattern, two factorial '
  'orderings of the alpha labels and three factorial orderings of the beta labels give that same '
  'pattern. Divide by both factorials. You can also just choose the two alpha positions. Once '
  'those positions are fixed, the beta tiles fill every empty slot. Choosing the beta positions '
  'instead must give the same count, by symmetry.'),
 ('same_colour_flags',
  'The same idea works with flags. On three poles there are sixty displays of three '
  'distinguishable flags. Now make two flags the same colour. Exchanging their labels leaves the '
  'display unchanged, wherever they hang. Divide the old count by two factorial times one '
  'factorial. That leaves thirty displays.'),
 ('lattice_word',
  'Walk along the grid lines from the lower left corner to the upper right. You need five moves '
  'right and three moves up. A step left or down makes you spend another step getting back. So a '
  'shortest path is exactly eight moves long. We can read a path as a word made from R and U. '
  'Follow the highlighted path with your finger. Each time a segment turns, the next letter tells '
  'you which direction to go.'),
 ('path_count',
  'Choose the three positions for the up moves. The other positions have to be right moves, and '
  'the word determines the path. Eight choose three gives fifty-six. If we choose uniformly among '
  'these shortest paths, the highlighted one has probability one in fifty-six. Across a '
  'chessboard, eight moves each way give twelve thousand eight hundred seventy shortest paths. '
  "We'll use paths like these in random walks."),
 ('partition_formula',
  'Divide five people among three teams. Pick two for team A from all five, then two for team B '
  'from the remaining three. The last person goes to team C. Ten choices times three choices times '
  'one gives thirty. Switching the membership of teams A and B changes the partition. Rearranging '
  'the names within one team keeps its membership the same.'),
 ('partition_cancel',
  'For more teams, keep choosing each team from whoever remains. Expand each binomial coefficient '
  'into factorials. The factorial for the people left after one choice cancels with the numerator '
  'of the next. The result is n factorial over the product of all the group size factorials. An '
  'empty group is allowed and contributes a factor of one. Notice what the denominator does. It '
  'removes all the ways of ordering people within their groups, while keeping the group labels '
  'attached.'),
 ('bridge_deals',
  'Now deal all fifty-two cards to four bridge players. Each hand has thirteen cards. The hands '
  'belong to different players, so swapping two hands gives a different deal. The count is '
  "fifty-two factorial over thirteen factorial to the fourth. That's about five times ten to the "
  'twenty-eight possible deals. We can build one deal by choosing a hand for the first player, '
  'then choosing from the remaining deck for the second, and continuing until everybody has a '
  'hand.'),
 ('bridge_aces',
  'For everyone to get an ace, first assign the four aces to the four players. There are '
  'twenty-four ways. Then split the forty-eight remaining cards into four hands of twelve. '
  'Multiply those counts, then divide by all the deals. The chance that each player gets one ace '
  'is a little over one in ten.'),
 ('dice_pairs',
  'Roll twelve fair dice and keep track of which die is which. Suppose every face appears twice. '
  'We need to split the dice into six labelled groups of two. The group label tells us the face on '
  'both dice. Inside each pair, switching the order describes the same roll. Divide twelve '
  'factorial by two factorial to the sixth.'),
 ('dice_chance',
  'Each die has six possible faces, so there are six to the power twelve equally likely outcomes. '
  'Divide the successful count by that total. The probability is about a third of one percent. '
  'Even though each face is expected to show up twice on average, seeing exactly that balance is '
  'rare. A roll with a third six and a missing face still belongs in the total, even though it '
  'fails our test.'),
 ('summary_without',
  'Ask two questions before you count. Does order matter? Can an element repeat? Draw two of three '
  'tiles without replacement. If order matters, there are six sequences. Forget the order and '
  'those six fold into three subsets. Those are the falling product and the binomial coefficient. '
  'Say you drew A, then B. Is B, then A, the same result for you? If it is, count in the right '
  'column. If not, use the left one.'),
 ('summary_with',
  'Put the tiles back and you can repeat a letter. There are nine ordered sequences. If only the '
  'counts of A, B and C matter, there are six outcomes. To see the general rule, use two dividers '
  'to make three groups and put a dot in the appropriate group for each draw. An empty group means '
  'that tile was never drawn. Choose the dot positions among all four positions. With r dots and n '
  "minus one dividers, that's n plus r minus one choose r. We'll meet these dots and dividers "
  'again next time.'),
 ('code',
  "Let's simulate one hundred thousand bridge deals. We only need the positions of the four aces. "
  'Imagine the deck laid out in four blocks of thirteen slots, one block per player. Choose four '
  'distinct slots at random. Every set of four slots is equally likely in a fair deal. Integer '
  'division by thirteen identifies the block. We count a success when the aces occupy all four '
  'blocks.'),
 ('code_result',
  'For the exact check, choose one slot in each block, then divide by the number of ways of '
  'choosing any four slots. The simulated and exact results both land just above one in ten. The '
  'exact expression looks different from the one with factorials, but it counts the same event.'),
 ('recall',
  'Before we finish, try to explain why we divide by a factorial. Think of a hand of cards or of a '
  'team whose members can stand in any order.'),
 ('ideas',
  'We divide by r factorial because every subset has that many orderings. Choosing who stays is '
  'equivalent to choosing who leaves. When we split a population into labelled groups, divide by a '
  'factorial for each group. Every arrangement inside a group still gives the same membership.'),
 ('end',
  "The full section and exercises are on Aram Code Lab. Next time we'll look at occupancy "
  "problems. We'll ask how the way we model balls and cells changes the probabilities.")]
