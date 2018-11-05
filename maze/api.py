from maze.models import MazeBuilder, Cell
from maze.output import text_from_solved_maze
from maze.parser import one_zero_parse
from maze.solver import dfs


def solve_maze(file_path):
    """テキストファイルにある迷路を解く。"""
    with open(file_path) as f:
        text = f.read()
    p_result = one_zero_parse(text)
    builder = MazeBuilder(p_result.width, p_result.height)
    for k, v in p_result.valuemap.items():
        builder.set_cell(k[0], k[1], Cell(v))
    maze = builder.build(p_result.start, p_result.goal)
    path = dfs(maze)
    print(text_from_solved_maze(maze, path))
