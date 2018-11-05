from collections import namedtuple

from maze.exceptions import ParseError
from maze.utils import xy_positions


ParseResult = namedtuple('ParseResult', (
    'valuemap', 'width', 'height', 'start', 'goal'))


def one_zero_parse(text):
    """0と1で構成されたテキストベースの迷路を解析する"""
    if 's' not in text or 'g' not in text:
        raise ParseError('textにはスタート地点(s)とゴール地点(g)が必要です。')
    for t in text:
        if t not in ' sg10\n':
            raise ParseError('textには[\s10sg]以外の文字が使用できません。')

    max_width = max(len(line) for line in text.splitlines())
    max_height = len(text.splitlines())
    start = xy_positions('s', text)[0]
    goal = xy_positions('g', text)[0]
    road_positions = xy_positions('0', text)
    wall_positions = xy_positions('1', text)

    valuemap = {k: 0 for k in road_positions}
    valuemap.update({k: 1 for k in wall_positions})
    valuemap.update({start: 0, goal: 0})
    return ParseResult(valuemap=valuemap, width=max_width, height=max_height,
                       start=start, goal=goal)
