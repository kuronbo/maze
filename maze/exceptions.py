class MazeError(Exception):
    """ルート例外"""


class OutOfRange(MazeError):
    """範囲外に操作を行った場合"""


class BuildInValidError(MazeError):
    """ビルドの制約に反していた場合"""


class ParseError(MazeError):
    """迷路原稿の解析に失敗した場合"""
