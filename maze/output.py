def text_from_solved_maze(maze, path):
    """迷路とゴールまでの道のりからテキストを作成する。"""
    lines = []
    for y in range(maze.max_height):
        line = []
        for x in range(maze.max_width):
            target = (x, y)
            if maze.is_wall(target):
                line.append('1')
            else:
                line.append(' ')
        lines.append(line)
    for x, y in path:
        lines[y][x] = '*'
    s, g = maze.start, maze.goal
    lines[s[1]][s[0]], lines[g[1]][g[0]] = 's', 'g'
    lines = [''.join(line) for line in lines]
    return '\n'.join(lines)
