def dfs(maze):
    """深さ優先探索により迷路のスタートからゴールまでの経路を探す"""
    def _dfs(path):
        if maze.is_goal(path[-1]):
            return path
        for posi in maze.next_road_positions(path[-1]):
            new_path = None
            if posi not in path:
                new_path = _dfs(path+[posi])
            if new_path:
                return new_path
    return _dfs([maze.start])
