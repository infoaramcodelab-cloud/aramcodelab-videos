"""A short Probability Theory lesson using every public kit block."""

import sys
from pathlib import Path

from manim import Create, VGroup

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / 'lib'))

from brand import ACCENT
from lesson_kit import (
    LessonScene, box, bullet_list, code_cell, derivation, end_card,
    key_ideas, sample_points, svg_figure, title_card,
)

CODE = """rolls = list(range(1, 7))
event = [roll for roll in rolls if roll > 3]
print(len(event) / len(rolls))"""


class Video(LessonScene):
    folder = HERE
    number = '1.1'
    section_title = 'Sample space and events'
    lesson_k = 1

    def construct(self):
        with self.seg('title'):
            self.show(title_card(self.number, self.section_title, self.lesson_k))

        with self.seg('definition') as g:
            self.show(box('definition', 'Sample space', [
                r'The sample space $\Omega$ contains every possible outcome.',
                r'For one die roll, $\Omega = \{1,2,3,4,5,6\}$.',
                r'An event $A$ is a subset of $\Omega$.',
            ]), step_time=max(0.6, g.left() / 5))

        with self.seg('points') as g:
            points = sample_points(range(1, 7), cols=3)
            self.show(points)
            self.wait(max(0.1, g.left() * 0.45))
            event = (4, 5, 6)
            outline = points.outline(event)
            self.play(points.event(event).animate.set_color(ACCENT), Create(outline))
            self.remove(outline, *points.submobjects, points)
            self.body = VGroup(points, outline)
            self.add(self.body)

        with self.seg('derivation') as g:
            self.show(derivation([
                r'{{ P(A) }} = {{ \frac{|A|}{|\Omega|} }}',
                r'{{ P(A) }} = {{ \frac{3}{6} }}',
                r'{{ P(A) }} = {{ \frac{1}{2} }}',
            ]), step_time=max(0.6, g.left() / 4))

        with self.seg('code') as g:
            self.show(code_cell(CODE, '0.5'), step_time=max(0.6, g.left() / 5))

        with self.seg('figure'):
            self.show(svg_figure('venn-incl.svg'), run_time=2)

        with self.seg('bullets') as g:
            self.show(bullet_list([
                'List all possible outcomes.',
                'Identify the outcomes in the event.',
                'Check whether the outcomes are equally likely.',
            ]), step_time=max(0.6, g.left() / 4))

        with self.seg('recall'):
            self.show(key_ideas([
                r'$\Omega$ is the set of possible outcomes.',
                r'An event is a subset of $\Omega$.',
                r'For equally likely outcomes, $P(A) = |A|/|\Omega|$.',
            ]))
            self.wait(1)

        with self.seg('end'):
            self.show(end_card('Probabilities in discrete sample spaces'))
