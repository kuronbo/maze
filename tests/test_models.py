import pytest

from maze.exceptions import OutOfRange, BuildInValidError
from maze.models import MazeBuilder, Cell, Maze


class TestMazeBuilder_init:
    def test_init_ok(self):
        MazeBuilder(3, 3)

    def test_init_small_width_ng(self):
        with pytest.raises(OutOfRange):
            MazeBuilder(2, 3)

    def test_init_small_height_ng(self):
        with pytest.raises(OutOfRange):
            MazeBuilder(3, 2)


class TestMazeBuilder_set_cell:
    def setup_method(self):
        self.instance = MazeBuilder(3, 3)

    @pytest.mark.parametrize('position', [
        (0, 1), (1, 0), (2, 1), (1, 2)
    ])
    def test_set_cell_valid_position_ok(self, position):
        x, y = position
        self.instance.set_cell(x, y, Cell.road)

    @pytest.mark.parametrize('position', [
        (-1, 0), (0, -1), (3, 2), (2, 3)
    ])
    def test_set_cell_invalid_position_ng(self, position):
        x, y = position
        with pytest.raises(OutOfRange):
            self.instance.set_cell(x, y, Cell.road)


class TestMazeBuilder_build:
    BASIC_MAP = {
        (1, 0): 1,
        (0, 1): 1, (1, 1): 0, (2, 1): 1,
        (1, 2): 1,
    }

    def setup_method(self):
        self.instance = MazeBuilder(3, 3)

    def test_build_ok(self):
        start = goal = (1, 1)
        expected_map = {k: Cell(v) for k, v in self.BASIC_MAP.items()}
        for k, v in self.BASIC_MAP.items():
            self.instance.set_cell(k[0], k[1], Cell(v))
        actual = self.instance.build(start, goal)

        assert actual.start == start
        assert actual.goal == goal
        assert actual.cellmap == expected_map

    @pytest.mark.parametrize('kind', [
        'del', 'road'
    ])
    def test_not_closed_maze_ng(self, kind):
        start = goal = (1, 1)
        map = dict(self.BASIC_MAP)
        if kind == 'del':
            del map[(1, 0)]
        else:
            map[(1, 0)] = 0
        for k, v in map.items():
            self.instance.set_cell(k[0], k[1], Cell(v))
        with pytest.raises(BuildInValidError):
            self.instance.build(start, goal)

    def test_not_exist_road_ng(self):
        start = goal = (1, 1)
        map = dict(self.BASIC_MAP)
        map[(1, 1)] = 1
        with pytest.raises(BuildInValidError):
            self.instance.build(start, goal)

    @pytest.mark.parametrize('start', [
        (0, 0), (1, 0)
    ])
    def test_start_on_not_road_ng(self, start):
        goal = (1, 1)
        for k, v in self.BASIC_MAP.items():
            self.instance.set_cell(k[0], k[1], Cell(v))
        with pytest.raises(BuildInValidError):
            self.instance.build(start, goal)
