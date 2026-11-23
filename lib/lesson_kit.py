"""Reusable, narrated Manim blocks for the Probability Theory playlist."""

import re
from collections import Counter
from html import escape
from math import pi
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree as ET

from manim import (
    DOWN, LEFT, ORIGIN, RIGHT, UL, UP, AddTextLetterByLetter, Arc, Circle,
    Create, Difference, Dot, FadeIn, FadeOut, Intersection, MarkupText, MathTex,
    SVGMobject, Union,
    SurroundingRectangle, TransformMatchingTex, Uncreate, VGroup,
    Write, config, linear,
)
from pygments.lexers import PythonLexer
from pygments.token import Comment, Keyword, Name, Number, Operator, String
from svgelements import Text as SVGText

from brand import (
    ACCENT, BORDER2, MUTED, NEXT, SKY, SURFACE, TEXT, TEXT2, WARN,
    background, card, logo, mono, pill, sans,
)
from narrate import Narrated, load_script

COURSE = 'Probability Theory'
SUCCESS = '#34d399'
BOX_COLORS = dict(definition=ACCENT, theorem=ACCENT, property=SUCCESS,
                  example=WARN, remark=MUTED)
CONTENT_TOP = 2.65
CONTENT_BOTTOM = -3.60
CONTENT_WIDTH = 13.2
PROSE_SIZE = 40
FIGURES = Path(__file__).resolve().parents[1] / 'figures'   # SVG figures shared with the site


def _fit(mob, width=None, height=None):
    width = config.frame_width - 1.2 if width is None else width
    height = config.frame_height - 2.4 if height is None else height
    factor = min(1, width / max(mob.width, 0.01), height / max(mob.height, 0.01))
    return mob.scale(factor) if factor < 1 else mob


def _panel(contents, accent=None, width=0):
    bg = card(max(width, contents.width + 0.85), contents.height + 0.65).move_to(contents)
    if accent:
        bg.set_stroke(accent, width=2)
    return bg


class LessonScene(Narrated):
    """Set folder, number, section_title and lesson_k on a subclass.

    Use inherited seg(key) for narration and show(block) to replace the
    current content while keeping the playlist label and section heading.
    """

    number = ''
    section_title = ''
    lesson_k = 1
    lesson_n = None

    def setup(self):
        super().setup()
        self.folder = str(Path(self.folder).resolve())
        self.segments = dict(load_script(self.folder).SEGMENTS)
        self.body = None
        self.add(background().set_z_index(-10))
        label = mono(f'{COURSE} · Lesson {self.lesson_k}', 18, ACCENT)
        self.playlist_label = label.to_corner(UL, buff=0.45).set_z_index(10)
        heading = sans(f'{self.number} · {self.section_title}', 30, TEXT, 'SEMIBOLD')
        self.section_heading = _fit(heading).next_to(
            self.playlist_label, DOWN, aligned_edge=LEFT, buff=0.14,
        ).set_z_index(10)
        self.header_visible = False

    def seg(self, key):
        """Start a segment declared in script.py using narrate.py's timings."""
        if key not in self.segments:
            raise KeyError(f'Unknown narration segment {key!r} in {self.folder}/script.py')
        return super().seg(key)

    def place(self, block):
        """Clear the previous block and position its replacement before revealing it."""
        if self.body is not None:
            self.play(FadeOut(self.body), run_time=0.35)
        opening = getattr(block, 'is_title_card', False)
        if not opening and not self.header_visible:
            self.add(self.playlist_label, self.section_heading)
            self.header_visible = True
        header_gap = 44 * config.frame_height / 1080
        top = CONTENT_TOP if opening else min(CONTENT_TOP, self.section_heading.get_bottom()[1] - header_gap)
        height = top - CONTENT_BOTTOM
        center = ORIGIN if opening else UP * (top + CONTENT_BOTTOM) / 2
        _fit(block, width=CONTENT_WIDTH, height=height).move_to(center)
        self.body = block

    def show(self, block, *, run_time=0.8, step_time=0.6):
        """Center and animate a block, replacing the previous block."""
        self.place(block)
        reveal = getattr(block, 'reveal', None)
        if reveal is None:
            self.play(FadeIn(block), run_time=run_time)
        else:
            reveal(self, run_time=run_time, step_time=step_time)
            self.remove(*block.submobjects)
            self.add(block)


def title_card(number, title, lesson_k, lesson_n=None):
    """Build an opening card. The legacy lesson_n argument is optional."""
    title = _fit(sans(title, 60, TEXT, 'BOLD'), width=config.frame_width - 2.2)
    contents = VGroup(
        mono(f'{COURSE.upper()} · LESSON {lesson_k}', 24, ACCENT),
        title,
        sans(f'Section {number} on Aram Code Lab', 30, MUTED),
    ).arrange(DOWN, buff=0.36)
    opening = VGroup(_panel(contents), contents)
    opening.is_title_card = True
    return opening

def inline_text(line, size=PROSE_SIZE, color=TEXT2):
    """Lay out Inter prose and $math$ on a shared baseline."""
    chunks = re.split(r'(\$[^$]+\$)', line)
    pieces = VGroup()
    cursor = 0
    for index, chunk in enumerate(chunks):
        if not chunk:
            continue
        if index % 2:
            formula = MathTex(r'\mathrm{H}', chunk[1:-1], font_size=size, color=color)
            # Match the cap height across the Pango and TeX renderers.
            formula.scale(sans('H', size).height / formula[0].height)
            reference, math = formula
            math.shift(UP * -reference.get_bottom()[1])
            math.shift(RIGHT * (cursor - math.get_left()[0]))
            cursor = math.get_right()[0]
            pieces.add(math)
        else:
            # The framing glyphs preserve leading and trailing space in Pango's
            # advance and give each prose run the same baseline as LaTeX.
            text = sans(f'H{chunk}H', size, color, disable_ligatures=True)
            left, right = text[0], text[-1]
            origin = left.get_right()[0]
            glyphs = VGroup(*(glyph for glyph in text[1:-1] if glyph.has_points()))
            glyphs.shift(RIGHT * (cursor - origin) + UP * -left.get_bottom()[1])
            cursor += right.get_left()[0] - origin
            if len(glyphs):
                pieces.add(glyphs)
    return pieces


def _wrapped_rows(text, width, size=PROSE_SIZE):
    for line in text.splitlines():
        if not line.strip():
            continue
        words = re.findall(r"(?:\$[^$]+\$|[^\s$])+", line)
        row = inline_text(line, size)
        while len(words) > 1 and row.width > width:
            end = max(1, min(len(words) - 1, int(len(words) * width / row.width)))
            head = inline_text(' '.join(words[:end]), size)
            while end > 1 and head.width > width:
                end -= 1
                head = inline_text(' '.join(words[:end]), size)
            yield head
            words = words[end:]
            row = inline_text(' '.join(words), size)
        yield row


def _prose_rows(text, width, size):
    rows = VGroup(*_wrapped_rows(text, width, size)).arrange(DOWN, buff=0.12)
    for row in rows:
        row.shift(LEFT * row.get_left()[0])
    return rows

class _Box(VGroup):
    def __init__(self, kind, title, lines):
        color = BOX_COLORS[kind]
        heading = title if title.lower().startswith(kind) else f'{kind.title()} · {title}'
        width = config.frame_width * 0.75
        self.heading = sans(heading, 44, color, 'BOLD')
        self.lines = VGroup(*(row for line in lines for row in _wrapped_rows(line, width - 0.85)))
        contents = VGroup(self.heading, *self.lines).arrange(DOWN, aligned_edge=LEFT, buff=0.26)
        self.panel = _panel(contents, color, width=width)
        contents.align_to(self.panel, LEFT).shift(RIGHT * 0.425)
        super().__init__(self.panel, self.heading, *self.lines)

    def reveal(self, scene, *, run_time=0.8, step_time=0.6):
        scene.play(FadeIn(self.panel), FadeIn(self.heading), run_time=run_time)
        for line in self.lines:
            scene.play(FadeIn(line, shift=UP * 0.08), run_time=step_time)


def box(kind, title, body_tex):
    """Build a styled box from prose with inline $math$, one row per line."""
    lines = body_tex.splitlines() if isinstance(body_tex, str) else body_tex
    return _Box(kind, title, (line for line in lines if line.strip()))


class _Derivation(VGroup):
    def __init__(self, lines):
        formulas = VGroup(*(MathTex(line, font_size=46, color=TEXT) for line in lines))
        if not formulas:
            raise ValueError('A derivation requires at least one formula')
        formulas.arrange(DOWN, aligned_edge=LEFT, buff=0.48)
        self.panel = _panel(formulas)
        self.formulas = formulas
        super().__init__(self.panel, *formulas)

    def reveal(self, scene, *, run_time=0.8, step_time=0.6):
        first = self.formulas[0]
        scene.play(FadeIn(self.panel), Write(first), run_time=run_time)
        for previous, current in zip(self.formulas[:-1], self.formulas[1:]):
            remaining = Counter(part.tex_string for part in previous)
            changed = []
            for part in current:
                if remaining[part.tex_string]:
                    remaining[part.tex_string] -= 1
                else:
                    changed.append(part)
            for part in changed:
                part.set_color(ACCENT)
            source = previous.copy().set_color(TEXT)
            scene.play(TransformMatchingTex(source, current), run_time=step_time)


def derivation(lines):
    """Reveal a vertical formula chain, keeping each previous step visible.

    Enclose matching or changed parts in Manim's double braces, e.g.
    r'{{ P(A) }} = {{ 3/6 }}', to highlight specific changes.
    """
    return _Derivation(lines)


def _python_rows(code):
    colors = (
        (Comment, MUTED), (Keyword, NEXT), (Name.Builtin, ACCENT),
        (Name.Function, SKY), (Number, WARN), (Operator, TEXT2), (String, SUCCESS),
    )
    rows = [[]]
    # Lex the full cell so strings and other tokens can span multiple lines.
    code = code.replace('\r\n', '\n').replace('\r', '\n').expandtabs(4)
    lexer = PythonLexer(stripnl=False, ensurenl=False)
    for token, value in lexer.get_tokens(code):
        color = next((shade for kind, shade in colors if token in kind), TEXT)
        for index, fragment in enumerate(value.split('\n')):
            if index:
                rows.append([])
            if fragment:
                # Nonbreaking spaces preserve spacing between highlighted tokens.
                text = escape(fragment).replace(' ', '\u00a0')
                rows[-1].append(
                    f'<span foreground="{color}" font_features="calt=0,liga=0,clig=0,dlig=0,hlig=0">{text}</span>'
                )
    result = VGroup()
    pitch = mono('Mg', 26).height * 1.55
    column = mono('MM', 26).width - mono('M', 26).width
    for index, (source, fragments) in enumerate(zip(code.split('\n'), rows, strict=True)):
        markup = ''.join(fragments) or '\u00a0'
        line = MarkupText(markup, font='JetBrains Mono', font_size=26, disable_ligatures=True)
        indent = len(source) - len(source.lstrip(' '))
        line.move_to(RIGHT * column * indent + DOWN * pitch * index, aligned_edge=UL)
        result.add(line)
    return result


class _CodeCell(VGroup):
    def __init__(self, code, output):
        self.rows = _python_rows(code.rstrip('\n'))
        code_label = mono('Python', 18, SKY)
        code_contents = VGroup(code_label, self.rows).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        self.output = VGroup(mono('Output', 18, MUTED), mono(str(output), 26, ACCENT, disable_ligatures=True))
        self.output.arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        contents = VGroup(code_contents, self.output).arrange(DOWN, aligned_edge=LEFT, buff=0.67)
        width = contents.width + 0.85
        self.code_panel = card(width, code_contents.height + 0.55).align_to(code_contents, LEFT)
        self.code_panel.set_y(code_contents.get_y()).shift(LEFT * 0.425)
        output_panel = card(width, self.output.height + 0.55).align_to(self.code_panel, LEFT)
        output_panel.set_y(self.output.get_y()).set_stroke(ACCENT, width=1.5)
        self.output.add_to_back(output_panel)
        self.code_label = code_label
        super().__init__(self.code_panel, self.code_label, *self.rows, self.output)

    def reveal(self, scene, *, run_time=0.8, step_time=0.6):
        scene.play(FadeIn(self.code_panel), FadeIn(self.code_label), run_time=run_time)
        for line in self.rows:
            if line.family_members_with_points():
                scene.play(AddTextLetterByLetter(line, run_time=step_time))
            else:
                scene.wait(step_time)
        scene.play(FadeIn(self.output, shift=UP * 0.1), run_time=run_time)


def code_cell(code, output):
    """Type syntax-coloured Python and then reveal the supplied output."""
    return _CodeCell(code, output)


SVG_COLORS = dict(accent=ACCENT, next=NEXT, warn=WARN, muted=MUTED, text=TEXT,
                  success=SUCCESS, danger='#f87171', border=BORDER2, surface=SURFACE)
_SUPERSCRIPT = str.maketrans('0123456789+-', '⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻')
_SUBSCRIPT = str.maketrans('0123456789+-k', '₀₁₂₃₄₅₆₇₈₉₊₋ₖ')


class _Figure(SVGMobject):
    def __init__(self, path, masks, targets):
        self.masks = masks
        self.targets = targets
        super().__init__(path, height=5)

    def get_mobjects_from(self, svg):
        mobjects, groups = super().get_mobjects_from(svg)
        visible = {}
        # The site masks use opaque white to reveal and black to subtract.
        for name in self.masks:
            region = None
            for shape in groups[name]:
                mobjects.remove(shape)
                if shape.get_fill_color().to_hex() == '#FFFFFF':
                    region = shape if region is None else Union(region, shape)
                elif region is not None:
                    region = Difference(region, shape)
            visible[name] = region
        for name, mask in self.targets.items():
            target = groups[name][0]
            region = visible[mask]
            if region is None:
                mobjects.remove(target)
            else:
                clipped = Intersection(target, region).match_style(target)
                mobjects[mobjects.index(target)] = clipped
        return mobjects, groups

    def get_mob_from_shape_element(self, shape):
        if not isinstance(shape, SVGText):
            return super().get_mob_from_shape_element(shape)
        label = self.text_to_mobject(shape)
        if label is not None:
            self.apply_style_to_mobject(label, shape)
            label.set_stroke(width=0)
            if shape.apply:
                self.handle_transform(label, shape.transform)
        return label

    @staticmethod
    def text_to_mobject(text):
        # SVGMobject flips SVG coordinates after parsing; flip glyphs beforehand.
        if not text.text or not text.text.strip():
            return None
        slant = 'ITALIC' if text.font_style == 'italic' else 'NORMAL'
        weight = {'600': 'SEMIBOLD', '700': 'BOLD', 'bold': 'BOLD'}.get(text.font_weight, 'NORMAL')
        label = sans(text.text + 'H', 48, weight=weight, slant=slant, disable_ligatures=True)
        reference = label[-1]
        baseline = reference.get_bottom()[1]
        glyphs = VGroup(*(glyph for glyph in label[:-1] if glyph.has_points()))
        glyphs.is_svg_label = True
        anchor = {'middle': 0, 'end': 1}.get(text.anchor, -1)
        x = glyphs.get_critical_point(anchor * RIGHT)[0]
        glyphs.shift(LEFT * x + DOWN * baseline)
        glyphs.scale(0.73 * text.font_size / reference.height, about_point=ORIGIN)
        return glyphs.flip(RIGHT, about_point=ORIGIN).shift(
            RIGHT * (text.x + text.dx) + UP * (text.y + text.dy),
        )

    @staticmethod
    def apply_style_to_mobject(mob, shape):
        SVGMobject.apply_style_to_mobject(mob, shape)
        opacity = float(shape.values.get('opacity', 1))
        mob.set_fill(opacity=mob.get_fill_opacity() * opacity)
        mob.set_stroke(opacity=mob.get_stroke_opacity() * opacity)

    def reveal(self, scene, *, run_time=0.8, step_time=0.6):
        scene.play(*(
            FadeIn(shape) if getattr(shape, 'is_svg_label', False) else Create(shape)
            for shape in self
        ), run_time=run_time)


def svg_figure(path):
    """Draw a site SVG in brand colours using its static opening frame.

    Pass an existing path or a filename from the sibling site's figures folder.
    """
    path = Path(path)
    if not path.is_file():
        path = FIGURES / path
    source = path.read_text(encoding='utf-8')
    source = re.sub(
        r'var\(\s*--([\w-]+)\s*(?:,\s*([^)]*))?\)',
        lambda match: SVG_COLORS.get(match[1], match[2] or TEXT2),
        source,
    ).replace('currentColor', TEXT)
    # Inline HTML SVGs may contain bare boolean attributes and comparison signs.
    source = re.sub(r'\bdata-keep-color(?=\s*\/?>)', 'data-keep-color=""', source)
    source = re.sub(r'<(?=\s)', '&lt;', source)
    tree = ET.fromstring(source)
    tree.attrib.setdefault('stroke-width', '1')
    masks = []
    targets = {}
    for parent in list(tree.iter()):
        for index, child in enumerate(parent):
            mask = re.fullmatch(r'url\(#([\w-]+)\)', child.get('mask', ''))
            if mask:
                name = f'lesson-mask-target-{len(targets)}'
                del child.attrib['mask']
                wrapper = ET.Element(parent.tag.rsplit('}', 1)[0] + '}g' if '}' in parent.tag else 'g',
                                     id=name)
                wrapper.append(child)
                parent[index] = wrapper
                targets[name] = mask[1]
    for element in list(tree.iter()):
        for child in list(element):
            if child.tag.rsplit('}', 1)[-1] == 'mask' and child.get('id') in targets.values():
                child.tag = child.tag[:-4] + 'g'
                masks.append(child.get('id'))
                element.remove(child)
                tree.insert(0, child)
    for element in tree.iter():
        for child in list(element):
            tag = child.tag.rsplit('}', 1)[-1]
            if tag == 'animate':
                attribute = child.get('attributeName')
                initial = child.get('values', child.get('from', '')).split(';', 1)[0]
                if attribute and initial:
                    element.set(attribute, initial)
                element.remove(child)
            elif tag == 'tspan':
                # The site uses tspans for powers and subscripts.
                table = _SUPERSCRIPT if float(child.get('dy', '0')) < 0 else _SUBSCRIPT
                element.text = (element.text or '') + (child.text or '').translate(table) + (child.tail or '')
                element.remove(child)
    with TemporaryDirectory() as folder:
        resolved = Path(folder) / path.name
        ET.ElementTree(tree).write(resolved, encoding='utf-8')
        return _fit(_Figure(resolved, masks, targets))


class _BulletList(VGroup):
    def reveal(self, scene, *, run_time=0.8, step_time=0.6):
        for row in self:
            scene.play(FadeIn(row, shift=RIGHT * 0.12), run_time=step_time)


def bullet_list(items, *, icons=None, width=CONTENT_WIDTH, size=PROSE_SIZE):
    """Build an optionally illustrated list with inline $math$ and line breaks."""
    items = tuple(items)
    markers = icons if icons is not None else (Dot(radius=0.066, color=ACCENT) for _ in items)
    rows = _BulletList()
    for marker, item in zip(markers, items, strict=True):
        text = _prose_rows(item, width - marker.width - 0.28, size)
        marker.next_to(text[0], LEFT, buff=0.28)
        rows.add(VGroup(marker, text))
    rows.arrange(DOWN, buff=0.32)
    for row in rows:
        row.shift(LEFT * row[1].get_left()[0])
    return rows.center()


class _KeyIdeas(VGroup):
    def __init__(self, items, pause):
        if pause < 0:
            raise ValueError('The recall pause must be nonnegative')
        self.pause = pause
        self.heading = sans('Key ideas', 48, TEXT, 'BOLD')
        self.prompt = sans('Pause and try to recall', 36, ACCENT)
        self.ring = Arc(radius=0.15, start_angle=pi / 2, angle=-2 * pi, color=ACCENT, stroke_width=4)
        self.track = Circle(radius=0.15, color=BORDER2, stroke_width=4).move_to(self.ring)
        width = CONTENT_WIDTH - 0.42
        self.items = bullet_list(items, width=width - 0.85, size=36)
        contents = VGroup(self.heading, self.items).arrange(DOWN, aligned_edge=LEFT, buff=0.27)
        self.panel = _panel(contents, ACCENT, width=width)
        contents.align_to(self.panel, LEFT).shift(RIGHT * 0.425)
        super().__init__(self.panel, self.heading, self.items)

    def start_recall(self, scene, *, run_time=0.8):
        scene.play(FadeIn(self.panel), FadeIn(self.heading), run_time=run_time)
        if self.pause:
            self.track.next_to(self.prompt, RIGHT, buff=0.22)
            VGroup(self.prompt, self.track).move_to(self.items)
            self.ring.move_to(self.track)
            scene.play(FadeIn(self.prompt), FadeIn(self.track), FadeIn(self.ring), run_time=0.35)

    def countdown(self, scene):
        if self.pause:
            scene.play(Uncreate(self.ring, rate_func=linear), run_time=self.pause)
            scene.play(FadeOut(self.prompt), FadeOut(self.track), run_time=0.25)

    def reveal_items(self, scene, *, step_time=0.6):
        self.items.reveal(scene, step_time=step_time)
        scene.remove(*self.items.submobjects)
        scene.add(self.items)

    def reveal(self, scene, *, run_time=0.8, step_time=0.6):
        self.start_recall(scene, run_time=run_time)
        self.countdown(scene)
        self.reveal_items(scene, step_time=step_time)


def key_ideas(items, pause=4):
    """Show the recall prompt and countdown, then reveal the key ideas."""
    return _KeyIdeas(items, pause)


def end_card(next_title):
    """Build the closing card with the description-link cue and next lesson."""
    contents = VGroup(
        logo(44),
        sans('Full proofs, exercises and runnable code', 32, TEXT2),
        pill('Link in the description', ACCENT, 30),
        sans(f'Next lesson: {next_title}', 27, NEXT),
    ).arrange(DOWN, buff=0.36)
    return VGroup(_panel(contents), contents)


class _SamplePoints(VGroup):
    def __init__(self, labels, cols):
        labels = tuple(str(label) for label in labels)
        if not labels or cols < 1 or len(set(labels)) != len(labels):
            raise ValueError('Supply distinct sample point labels and a positive column count')
        points = [VGroup(Dot(radius=0.16, color=MUTED), mono(label, 46, TEXT2))
                  .arrange(DOWN, buff=0.17) for label in labels]
        self.by_label = dict(zip(labels, points, strict=True))
        super().__init__(*points)
        self.arrange_in_grid(cols=min(cols, len(points)), buff=(0.85, 0.36))

    def event(self, labels):
        """Return the selected point-and-label groups, sharing the original objects."""
        return VGroup(*(self.by_label[str(label)] for label in labels))

    def outline(self, labels, color=ACCENT):
        """Return a rounded outline around a selected event."""
        return SurroundingRectangle(self.event(labels), color=color, buff=0.22,
                                    corner_radius=0.22, stroke_width=2.5)


def sample_points(labels, cols):
    """Build a labelled grid with event(labels) and outline(labels, color)."""
    return _SamplePoints(labels, cols)
