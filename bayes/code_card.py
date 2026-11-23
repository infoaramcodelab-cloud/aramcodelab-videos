"""Syntax-coloured JetBrains Mono that retains the source indentation."""

from html import escape

from manim import DOWN, LEFT, RIGHT, MarkupText, Text, VGroup
from pygments.lexers import PythonLexer
from pygments.token import Keyword, Name, Number, Operator, String

from brand import ACCENT, NEXT, SKY, TEXT, TEXT2, WARN


def code_lines(source):
    colors = (
        (Keyword, NEXT), (Name.Builtin, ACCENT), (Name.Function, SKY),
        (Number, WARN), (Operator, TEXT2), (String, '#86efac'),
    )
    font = 'JetBrains Mono'
    size = 24
    glyphs = Text('M' * 21, font=font, font_size=size)
    column = glyphs.width / 21
    row_height = Text('Mg', font=font, font_size=size).height * 1.55
    lexer = PythonLexer()
    rows = VGroup()
    for index, line in enumerate(source.splitlines()):
        body = line.lstrip(' ')
        indent = len(line) - len(body)
        spans = []
        for token, value in lexer.get_tokens(body):
            value = value.rstrip('\n')
            if value:
                color = next((color for kind, color in colors if token in kind), TEXT)
                spans.append(f'<span foreground="{color}">{escape(value)}</span>')
        row = MarkupText(''.join(spans), font=font, font_size=size)
        row.move_to(RIGHT * column * indent + DOWN * row_height * index, aligned_edge=LEFT)
        rows.add(row)
    return rows
