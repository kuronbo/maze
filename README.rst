----
maze
----
迷路を解くプログラム。

Usage
=====
以下のような迷路を描いたテキストを用意する。
壁は1, 道は0, スタート位置はs, ゴール位置はgで表現している。

.. code-block::

    111111111111
    10s000000001
    101111011101
    111000000001
    101011111111
    1000000000g1
    111111111111

次に、このテキストが入力されたファイルを読み込む。
.. code-block:: python

    from maze.api import solve_maze

    solve_maze('sample.txt')

結果、以下のような迷路と経路が表示される。
.. code-block::

    111111111111
    1 s****    1
    1 1111*111 1
    111****    1
    1 1*11111111
    1  *******g1
    111111111111

