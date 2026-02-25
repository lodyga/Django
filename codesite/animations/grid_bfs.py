from typing import List
from collections import deque


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        ROWS = len(grid)
        COLS = len(grid[0])
        DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
        visited = [[False] * COLS for _ in range(ROWS)]
        order = []

        def bfs(row: int, col: int) -> int:
            if (
                grid[row][col] == "0" or
                visited[row][col]
            ):
                return 0

            queue = deque([(row, col)])
            visited[row][col] = True
            order.append([row, col])

            while queue:
                (row, col) = queue.popleft()
                # order.append((row, col))

                for (dr, dc) in DIRECTIONS:
                    (r, c) = (row + dr, col + dc)
                    if (
                        r == -1 or r == ROWS or
                        c == -1 or c == COLS or
                        grid[r][c] == "0" or
                        visited[r][c]
                    ):
                        continue

                    queue.append((r, c))
                    visited[r][c] = True
                    order.append([r, c])

            return 1

        sum(
            bfs(row, col)
            for row in range(ROWS)
            for col in range(COLS)
        )
        return order
