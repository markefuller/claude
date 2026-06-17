import random


class Cell:
    def __init__(self):
        self.walls = {"top": True, "right": True, "bottom": True, "left": True}
        self.visited = False


class Maze:
    OPPOSITE = {"top": "bottom", "bottom": "top", "left": "right", "right": "left"}
    DIRECTIONS = [("top", -1, 0), ("right", 0, 1), ("bottom", 1, 0), ("left", 0, -1)]

    def __init__(self, rows: int, cols: int):
        if rows < 2 or cols < 2:
            raise ValueError("Maze must be at least 2x2")
        self.rows = rows
        self.cols = cols
        self.grid: list[list[Cell]] = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self._generate()

    def _generate(self):
        """Iterative DFS (recursive backtracking) to carve a perfect maze."""
        stack = [(0, 0)]
        self.grid[0][0].visited = True

        while stack:
            row, col = stack[-1]
            unvisited = [
                (direction, row + dr, col + dc)
                for direction, dr, dc in self.DIRECTIONS
                if 0 <= row + dr < self.rows
                and 0 <= col + dc < self.cols
                and not self.grid[row + dr][col + dc].visited
            ]

            if unvisited:
                direction, nr, nc = random.choice(unvisited)
                self.grid[row][col].walls[direction] = False
                self.grid[nr][nc].walls[self.OPPOSITE[direction]] = False
                self.grid[nr][nc].visited = True
                stack.append((nr, nc))
            else:
                stack.pop()

    def display(self) -> str:
        """
        Render the maze as ASCII art.
        '#' = wall, ' ' = passage/cell interior.
        Entrance is top-left, exit is bottom-right.
        """
        height = 2 * self.rows + 1
        width = 2 * self.cols + 1
        canvas = [["#"] * width for _ in range(height)]

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                dr, dc = 2 * r + 1, 2 * c + 1
                canvas[dr][dc] = " "

                if not cell.walls["top"]:
                    canvas[dr - 1][dc] = " "
                if not cell.walls["bottom"]:
                    canvas[dr + 1][dc] = " "
                if not cell.walls["left"]:
                    canvas[dr][dc - 1] = " "
                if not cell.walls["right"]:
                    canvas[dr][dc + 1] = " "

        canvas[1][0] = " "                                    # entrance
        canvas[2 * self.rows - 1][2 * self.cols] = " "       # exit

        return "\n".join("".join(ch + " " for ch in row) for row in canvas)


def main():
    try:
        rows = int(input("Rows  (default 10): ") or 10)
        cols = int(input("Cols  (default 20): ") or 20)
    except ValueError:
        print("Invalid input — using defaults (10 x 20).")
        rows, cols = 10, 20

    maze = Maze(rows, cols)
    print()
    print(maze.display())


if __name__ == "__main__":
    main()
