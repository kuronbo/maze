def xy_positions(target_chars, text):
    """テキストに存在するすべての指定文字の位置(x, y)を返す。"""
    positions = []
    for y, line in enumerate(text.splitlines()):
        for x, char in enumerate(line):
            if char in target_chars:
                positions.append((x, y))
    return positions
