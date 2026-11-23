"""English narration approved in SCRIPT.md, in rendering order."""

VOICE = 'am_fenrir'
SPEED = 0.98

SEGMENTS = [
    ('cold1',
     'Imagine a test that catches ninety-nine percent of people who have a condition. Your '
     "result comes back positive. In the example we're about to build, the chance that you "
     'have the condition is exactly fifty percent.'),
    ('cold2',
     'Half the positive results are real cases. The other half are false alarms. Where did '
     "all those false alarms come from? To find out, we'll follow the people behind the "
     'percentages.'),
    ('puzzle1',
     'Here are the rules of our imaginary test. In the group being tested, one percent of '
     'people have the condition. Among people who have it, ninety-nine percent get a '
     "positive result. Among people who don't, one percent still get a positive result. "
     'That last number is the false-positive rate.'),
    ('puzzle2',
     "You already know the answer is half. Here's the part to guess. If ten thousand "
     'people take the test, how many false alarms should we expect? About one? About a '
     "hundred? About a thousand? Hold on to your guess. We'll count them two ways."),
    ('experiment1',
     "Let's give the test to ten thousand simulated people. For each person we draw their "
     'condition status, then draw their result using the rate for that group. Watch the '
     'grid light up. Lights cluster in the small group. Across the much bigger group, '
     "they're scattered."),
    ('experiment2',
     'In this run, we got a hundred and seven true positives and ninety-seven false '
     "positives. That's about fifty-two and a half percent of the positives coming from "
     "people with the condition. Run it again and the counts will move. To see why they're "
     "so close, let's take the randomness out of the picture."),
    ('count1',
     'Out of ten thousand, one percent gives us a hundred people with the condition. The '
     'test catches ninety-nine of those. Now look at the other group. There are nine '
     'thousand nine hundred people without the condition. Even one percent of that group '
     'gives us ninety-nine false positives.'),
    ('count2',
     'Both groups send the same number into the tray. There are a hundred and ninety-eight '
     "positives altogether, and ninety-nine come from people with the condition. That's "
     'exactly half.'),
    ('count3',
     "Here's the switch that makes this puzzle tricky. When you hear “ninety-nine "
     "percent,” you're standing in the group that has the condition and looking for plus "
     "signs. Once you've seen a plus sign, you're standing in a different group. Now "
     "you're looking for people who have the condition."),
    ('area1',
     'Turn the crowd into a rectangle. The width of each column is how common that group '
     'is. The shaded height is the chance of a positive result within that group. Multiply '
     'width by height and you get the share of the whole crowd that lands in that positive '
     'region.'),
    ('area2',
     'The teal column is narrow and almost entirely shaded. The indigo column is wide and '
     'barely shaded. In this example, their shaded areas are equal.'),
    ('area3',
     'Call having the condition D, and testing positive plus. Once we see a positive, the '
     "two shaded regions are the entire group we're choosing from. Put the teal area on "
     'top. Put both shaded areas together on the bottom. That fraction is exactly the rule '
     "we've been using since we counted people."),
    ('code1',
     "Here's the same experiment in Python. The first random draw decides whether a person "
     'has the condition. That tells us which rate to use for the second draw. Whenever the '
     'test is positive, one counter goes up. The other counter only goes up if that person '
     'also has the condition.'),
    ('code2',
     'At the end we divide the true-positive count by the total number of positives. With '
     'a million simulated people, this run gives fifty point seven percent. The fraction '
     'we derived is exactly fifty percent. The simulation gives us a way to check that our '
     'counting rule behaves the way we expect. Try changing the starting rate. Watch what '
     'happens, even though the test itself stays the same.'),
    ('meaning1',
     'The same question comes up when a system flags a payment as suspicious. If almost '
     'all payments are legitimate, even a small false-alarm rate in that group can account '
     'for a large share of the flags.'),
    ('meaning2',
     'The starting share of real cases is called the base rate. It tells you how wide to '
     'draw the first column before you know the result. When you see a flag, ask how often '
     'it comes from each group and how big those groups were to begin with.'),
    ('meaning3',
     'This example is about mathematics, not diagnosis.'),
    ('challenge1',
     'Your turn. Keep the same test, but suppose only zero point one percent of the people '
     'being tested have the condition. Among people who test positive, what fraction now '
     'have it?'),
    ('challenge2',
     'Start with a crowd. Count the two ways to get a positive result, then see what share '
     'comes from the group with the condition. The worked answer is on Aram Code Lab. The '
     'link is in the description.'),
]
