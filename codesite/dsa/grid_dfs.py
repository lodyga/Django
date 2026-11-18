from typing import List


class Solution:
    def numIslands(self, grid: List[List[str]]) -> List[int]:
        ROWS = len(grid)
        COLS = len(grid[0])
        DIRECTIONS = ((-1, 0), (1, 0), (0, -1), (0, 1))
        visited = [[False] * COLS for _ in range(ROWS)]
        order = []

        def dfs(row: int, col: int) -> int:
            if (
                row == -1 or row == ROWS or
                col == -1 or col == COLS or
                grid[row][col] == "0" or
                visited[row][col]
            ):
                return 0

            visited[row][col] = True
            order.append([row, col])

            for dr, dc in DIRECTIONS:
                dfs(row + dr, col + dc)

            return 1

        sum(
            dfs(row, col)
            for row in range(ROWS)
            for col in range(COLS)
        )
        return order
