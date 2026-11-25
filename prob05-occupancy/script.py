"""Approved Lesson 5 narration in cue order."""

ENGINE = 'orpheus'
VOICE = 'tara'

CHAPTERS = [('welcome', 'Welcome'),
 ('count_cells', 'Occupancy numbers'),
 ('make_symbol', 'Stars and bars'),
 ('bars_in_gaps', 'No empty cells'),
 ('dice_outcomes', 'Dice and derivatives'),
 ('fixed_vector', 'Labelled balls and probability'),
 ('choose_cell_roles', 'Count cells, then count balls'),
 ('configuration_table', 'All fifteen configurations'),
 ('mb_model', 'The three statistics'),
 ('three_probabilities', 'One pattern, three probabilities'),
 ('find_runs', 'Runs'),
 ('counter_runs', 'The lunch counter'),
 ('code', 'Code Lab'),
 ('recall', 'Key ideas')]

SEGMENTS = [('welcome',
  'Welcome back. Last time we promised to come back to these dots and dividers. Here they are. The '
  'dots are balls, and the dividers tell us where one cell ends and the next begins. This little '
  'picture will help us count distributions, compare ways of assigning probabilities, and even '
  'make sense of where people sit.'),
 ('recap',
  'Remember n choose r, for picking a subset. When the order of draws matters, we use the ordered '
  'counts from the other column. And when we split a population into labelled groups, we use a '
  "multinomial coefficient. Today we'll start in the unordered column with replacement, then bring "
  'back the multinomial when we need labels.'),
 ('count_cells',
  'Suppose we put eight balls into five cells. Read the counts from left to right. Three, one, '
  'zero, zero, four. Those are the occupancy numbers. Empty cells get a zero, and every ball '
  'belongs to exactly one cell. So the numbers are nonnegative integers and they add up to the '
  'number of balls. This same record works for accidents per weekday, birthdays per date, or dice '
  'counted by face.'),
 ('forget_labels',
  'If we only record the counts, exchanging two balls leaves the record alone. Moving one ball '
  'into an empty cell changes the record. Watch the second count drop to zero as its ball moves to '
  'the third cell. The total stays at eight because we only moved a ball. The positions of the '
  'cells still matter. A zero in one position means a different cell is empty than a zero '
  'somewhere else. So our outcome is a whole vector of counts in cell order.'),
 ('make_symbol',
  'Turn each ball into a star and put a bar at each cell boundary. The stars between adjacent bars '
  'belong to one cell. Two bars next to each other mark an empty cell. Read between the bars and '
  'you can recover the counts. Start from the counts and you can rebuild the same symbol. That '
  'means every valid symbol represents exactly one occupancy vector. In our picture the third and '
  'fourth cells are empty, so the strip has three bars in a row. The two spaces between them are '
  'exactly where those two zeros come from.'),
 ('count_symbols',
  'The first and last bars stay fixed. Inside, eight stars and four bars occupy twelve positions. '
  'Choose the eight positions for the stars, or choose the four positions for the bars. Either way '
  'gives four hundred ninety-five. In general, the count is n plus r minus one choose r, which '
  'also equals n plus r minus one choose n minus one.'),
 ('bars_in_gaps',
  'Now require a ball in every cell. If we put two bars together, the cell between them is empty. '
  'Instead, line up the stars and put each inner bar into a different gap between stars. Eight '
  'stars give seven gaps. Choose four of those gaps and you get thirty-five distributions. For r '
  "balls and n cells, that's r minus one choose n minus one."),
 ('reserve_one',
  "Here's the same count from the other direction. Give every cell one ball first. With eight "
  'balls and five cells, that leaves three to place freely. We can use the original rule on those '
  "leftover balls and get the same answer. If there are fewer balls than cells, there's no way to "
  'start by giving each cell one.'),
 ('dice_outcomes',
  'Roll three dice and record how many ones, twos, and so on you see. If two dice show two and the '
  'other shows five, that record is the same whichever die shows five. We have three balls and six '
  'face cells. Five dividers go with the three stars, so eight choose five gives fifty-six '
  "different records. This counts records, and we'll see in a moment why their probabilities can "
  'differ.'),
 ('derivative_orders',
  'The same rule even counts partial derivatives of a smooth function. The cells are the '
  'variables, and a star records one differentiation with respect to a variable. You can switch '
  'the order of the differentiations without changing the result, so only the counts matter. For '
  'instance, differentiating twice with respect to x and once each with respect to y and z gives '
  'the same mixed derivative wherever the x steps occur. For three variables there are fifteen '
  'possible choices of counts at fourth order and twenty-one at fifth order.'),
 ('fixed_vector',
  'Now give the balls their labels back. Suppose each ball independently chooses a cell uniformly. '
  'Three balls in three cells give twenty-seven placements of equal probability. To get exactly '
  'two in the first cell and one in the second, choose which ball goes to the second cell. There '
  'are three choices. That particular vector has probability three over twenty-seven, or one '
  'ninth.'),
 ('mb_probability',
  'In general, a placement with specified occupancies is a partition of the labelled balls into '
  'groups. The cells are the group labels. So the favourable count is r factorial over the product '
  'of the occupancy factorials. Divide by n to the power r for the probability. This is the '
  'Maxwell–Boltzmann model. Equal chances for placements can give different chances for their '
  'occupancy vectors.'),
 ('choose_cell_roles',
  'Put seven labelled balls into seven cells. We want two double cells, three single cells, and '
  'two empty cells. This time we accept those counts in any order. First decide which cells have '
  'each role. Partition the seven cells into groups of sizes two, three and two. That gives two '
  'hundred ten choices of cell roles. For example, the first two cells could be the doubles, the '
  'next three the singles, and the last two empty. So far, no ball has moved.'),
 ('assign_balls',
  'Now freeze those roles and choose which balls go into each cell. Divide seven factorial by the '
  'factorials of the individual occupancies. That gives one thousand two hundred sixty placements '
  'for each choice of roles. Multiply the two counts, then divide by seven to the power seven. The '
  'probability is about zero point three two one three. We used the multinomial once on cells and '
  'once on balls.'),
 ('configuration_table',
  'Repeat the two counts for every possible pattern. There are fifteen rows. Each placement '
  'belongs to exactly one row, so the exact probabilities add to one. The table rounds each row '
  'separately. Compare the first two rows. Each has the same total number of balls, but a cell '
  'with three balls changes both the cell roles and the number of ways we can fill them.'),
 ('even_and_typical',
  'The most likely pattern is the one we just counted. The perfectly even pattern is much rarer. '
  'It has probability around zero point zero zero six one. Equal chances for the cells can still '
  'leave several cells empty, because there are many more labelled placements that produce those '
  'uneven results.'),
 ('mb_model',
  'In statistical mechanics, we use cells to represent the states a particle can occupy. '
  'Maxwell–Boltzmann counts placements of distinguishable particles. You can follow the label on '
  "each particle and see where it goes. It's the classical model, and it can approximate a dilute "
  "gas. For identical quantum particles, counting permutations of labels this way doesn't give "
  'their exact statistics.'),
 ('be_model',
  'For Bose–Einstein, count each occupancy vector just once, and give the vectors equal '
  'probabilities in this model. Several particles can share a state. Photons are an example. Some '
  'composite particles, including atoms and nuclei with integer spin, also behave this way.'),
 ('fd_model',
  'Fermi–Dirac allows at most one particle in each state. In our model the set of occupied cells '
  'is a uniformly chosen subset. Electrons, protons and neutrons obey this kind of statistics. The '
  'rule tells us which arrangements are allowed. It still takes experience to tell us which model '
  'describes nature.'),
 ('three_probabilities',
  'Use five cells and three particles, with one particle in the first, third and fourth cells. '
  'With labels, the three particles can swap places among those cells. That gives six placements '
  'out of a hundred twenty-five. With Bose–Einstein, this vector is one out of thirty-five. With '
  'Fermi–Dirac, this set of occupied cells is one out of ten. The picture stays the same while the '
  'probabilities change. What changes from card to card is the set of outcomes we give equal '
  'chances to.'),
 ('misprints',
  'Think of misprints on a printed page. When we mark each letter position as correct or '
  "misprinted, there's room for at most one mark per position. That gives the same kind of "
  'occupancy restriction as Fermi–Dirac. Equal chances for the marked sets would be a further '
  'modelling assumption.'),
 ('find_runs',
  'A run is a block of consecutive equal letters, extended as far as it can go. Here the first '
  "three A's make one run. The next B starts a new one, and later A's start another. The run "
  'lengths are three, one, two, three, one. Runs of A and B alternate, so neither kind can have '
  'more than one extra run.'),
 ('run_count',
  'Count arrangements with n one A runs and one more B run. The extra B run means the sequence '
  'starts and ends with B. Now split the A letters into nonempty blocks, and do the same for B. '
  "The no-empty-cells rule counts the lengths for each kind, and we multiply. With three A's and "
  "four B's, two A runs give two choices of A lengths and three choices of B lengths. That's six "
  'sequences.'),
 ('counter_runs',
  'At a lunch counter with sixteen seats, an observer sees five occupied seats and eleven empty '
  'seats. No two occupied seats are next to each other, and both end seats are empty. Each '
  'occupied seat makes its own run. The empty seats form six runs between and around them. That '
  'gives eleven runs, the maximum with only five occupied seats. With five occupied runs you can '
  'have at most six empty ones, because the runs alternate. If either end seat is occupied, there '
  'is room for at most five empty runs.'),
 ('counter_probability',
  'Under a uniform seating model, choose any five of the sixteen seats. For the maximum number of '
  'runs, all the occupied blocks have length one. The eleven empty seats must split into six '
  'nonempty blocks. That gives two hundred fifty-two seatings out of four thousand three hundred '
  'sixty-eight, or about zero point zero five seven seven. Many runs can suggest mixing or '
  'avoidance, and very few can suggest clustering. This one observation hints that people might '
  "avoid sitting next to strangers. We'd want more data before drawing a conclusion."),
 ('code',
  "Let's check the seven-cell example in Python. Each trial sends seven labelled balls "
  'independently to cells chosen with replacement. Count the balls in each cell and sort those '
  'counts. Sorting is how we accept the target pattern in any cell order. Record a hit whenever '
  'the sorted counts match.'),
 ('code_result',
  'In a hundred thousand trials, the simulated frequency and the exact probability are both about '
  'zero point three two. Their small difference is expected with a finite simulation. Try watching '
  'what happens to that difference if you increase the number of trials. A larger sample tends to '
  'give a more stable estimate, though any single new run can land farther from the exact value.'),
 ('recall',
  'Before we finish, pause and picture the difference between a list of cell counts and a '
  'placement of labelled balls. Where do the bars go when every cell needs a ball?'),
 ('ideas',
  'Stars and bars counts occupancy vectors. To require nonempty cells, set one ball aside for each '
  'cell. With labelled balls placed independently and uniformly, count how many placements give '
  'the vector you want. Those counts are why some patterns are more likely than others.'),
 ('end',
  "The full section and exercises are on Aram Code Lab. Next time we'll draw from a mixed "
  'population without replacement and ask how many successes we get, or how long we have to wait '
  'for them.')]
