import enum

from maze.exceptions import OutOfRange, BuildInValidError


class Cell(enum.Enum):
    road = 0
    wall = 1


class Maze:
    """迷路クラス

    内部に位置(x, y)をkey、`Cell`をvalueとする辞書(`cellmap`)を持ち、
    その辞書を元にした操作が用意されている。

    Parameters:
        cellmap (dict):　(x, y)のタプルをkey, `Cell`をvalueとした辞書
        max_width (int): 最大ヨコ長さ。
        max_height (int): 最大タテ長さ。
        start (tuple): 迷路のスタート位置。(x, y)のタプル。
        goal (tuple): 迷路のゴール位置。(x, y)のタプル。
    """
    def __init__(self, cellmap, max_width, max_height, start, goal):
        self.cellmap = cellmap
        self.max_width = max_width
        self.max_height = max_height
        self.start = start
        self.goal = goal

    def next_road_positions(self, target):
        """指定のセルに隣接する道の位置を返す。

        Args:
            target (tuple): 指定のセルの位置。(x, y)のタプル。

        Returns:
            list<tuple>: `target`に隣接するセルの位置。(x, y)を要素としたリスト
        """
        x, y = target
        positions = [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]
        return [p for p in positions if self.cellmap.get(p) == Cell.road]

    def is_road(self, target):
        """指定のセルが道かどうか"""
        return self.cellmap.get(target) == Cell.road

    def is_wall(self, target):
        """指定のセルが壁かどうか"""
        return self.cellmap.get(target) == Cell.wall

    def is_goal(self, target):
        """指定のセルがゴールかどうか。

        Args:
            target (tuple): 指定のセルの位置。(x, y)のタプル。

        Returns:
            bool: ゴールかどうか
        """
        x, y = target
        return (x, y) == self.goal


class MazeBuilder:
    """迷路を生成するBuilderクラス

    `Maze`（迷路）を制約に沿って生成するクラス。
    生成のイメージとしては、長方形の作業台(width, height)を置いて、
    その上で壁やら道やらを作っていく(`set_cell`)イメージ。
    注意としては、必ずしも迷路の形が長方形にはならないということである。
    また、作成するのは迷路であり、buildの際には、スタート位置(start)とゴール位置(goal)を
    指定する必要がある。

    制約：
        1. width, heightは、3以上の整数。
        2. 位置指定は、x座標とy座標で行い。座標の範囲はそれぞれ、0以上width未満、
            0以上height未満となる。
        3-1. 迷路は閉じた状態でなければならない。つまり、外と中の行き来ができない状態。
        3-2. 道は斜めにつながらないため、道をふさぐ際に斜めに壁を置く必要はない。
             ex) 以下は閉じた状態。     以下も、もちろん可。
                      #                   ###
                     # #                  # #
                     # #                  # #
        4. 迷路には少なくとも1つ、道が存在しなければならない。
        5. start位置、goal位置ともに、道が存在している位置でなければならない。

    Parameters:
        width (int): 作業台の横の長さ。
        height (int): 作業台の縦の長さ。
    """
    def __init__(self, width, height):
        if width < 3 or height < 3:
            raise OutOfRange('widthおよびheightは、3以上であるべきです。')

        self.width = width
        self.height = height
        self._cellmap = {}

    def set_cell(self, x, y, cell):
        """セルの位置と値を設定する。

        Args:
            x (int): x座標。ヨコの位置。0以上`width`未満の整数型。
            y (int): y座標。タテの位置。0以上`height`未満の整数型。
            cell (Cell): セルの値。道か壁か。

        Raises:
            OutOfRange: `x`および`y`の値が、範囲外であるとき送出。
        """
        assert isinstance(x, int)
        assert isinstance(y, int)
        assert isinstance(cell, Cell)

        self._send_out_of_range_error(x, y)
        self._cellmap[(x, y)] = cell

    def build(self, start, goal):
        """迷路(`Maze`)を生成する。

        内部の辞書と引数の`start`、`goal`から`Maze`を生成する。
        クラスドキュメントに記してある制約の3-5を満たしていなければ、例外を送出する。

        Args:
            start (tuple): 迷路のスタート位置。(x、y)のタプル。
            goal (tuple): 迷路のゴール位置。(x, y)のタプル。

        Returns:
            Maze: 迷路。`Maze`インスタンス。

        Raises:
            BuildInValidError: ビルドの制約を満たしていない場合に送出。
        """
        assert isinstance(start, tuple)
        assert isinstance(goal, tuple)

        if not self._is_closed_maze():
            raise BuildInValidError('迷路が閉じていません。')
        if not self._has_road():
            raise BuildInValidError('道が一つも存在しません。')
        if not self._is_road(*start):
            raise BuildInValidError('startの位置に道が存在しません。start={}'.
                                    format(start))
        if not self._is_road(*goal):
            raise BuildInValidError('goalの位置に道が存在しません。goal={}'.
                                    format(goal))

        return Maze(self._cellmap, self.width, self.height, start, goal)

    def _is_closed_maze(self):
        all_roads = []
        for k, v in self._cellmap.items():
            if v == Cell.road:
                all_roads.append(k)
        for road in all_roads:
            x, y = road
            around_p = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
            for p in around_p:
                if self._cellmap.get(p) is None:
                    return False
        return True

    def _has_road(self):
        return Cell.road in self._cellmap.values()

    def _is_road(self, x, y):
        return self._cellmap.get((x, y)) == Cell.road

    def _send_out_of_range_error(self, x, y):
        msg = 'xは0以上{}未満、yは0以上{}未満であるべきです。: (x={}, y={})'\
            .format(self.width, self.height, x, y)
        if not 0 <= x < self.width or not 0 <= y < self.height:
            raise OutOfRange(msg)
