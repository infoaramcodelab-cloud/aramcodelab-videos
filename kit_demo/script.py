"""Narration for the lesson kit demonstration."""

SEGMENTS = [
    ('title', 'Probability theory begins by asking what can happen. Our example is one roll of a fair die. We will use that experiment to connect a picture, a calculation and a short Python program.'),
    ('definition', 'The sample space lists every possible outcome. For a single die roll, it contains the numbers one through six. An event is a subset of that space. Several different rolls, for instance, can all satisfy the same condition.'),
    ('points', 'Here is one point for each possible face. The bottom row is the event that the roll is greater than three. It contains four, five and six. Whenever any one of those three faces appears, the event occurs.'),
    ('derivation', 'Each face is equally likely. Three of the six possibilities are in our event. Divide the number of favourable outcomes by the total, and simplify to one half.'),
    ('code', 'We can do the same count in Python. Build the list of possible rolls, keep those greater than three, and divide by the size of the original list. The output is zero point five.'),
    ('figure', 'Sets can also be drawn as overlapping regions. Here, a number inside a region counts how many of the three events contain it. In the middle, all three events share the same outcomes.'),
    ('bullets', 'When you set up a probability problem, list the outcomes first. Then describe the event and check whether the outcomes are equally likely.'),
    ('recall', 'Pause and try to recall.'),
    ('end', 'The course page has full proofs, exercises and runnable code. Next we look more closely at probabilities in discrete sample spaces.'),
]
