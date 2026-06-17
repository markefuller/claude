import random
import sys


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

    def _build_canvas(self) -> list[list[bool]]:
        """Return a boolean grid: True = wall, False = open passage/cell."""
        height = 2 * self.rows + 1
        width = 2 * self.cols + 1
        canvas = [[True] * width for _ in range(height)]

        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                dr, dc = 2 * r + 1, 2 * c + 1
                canvas[dr][dc] = False

                if not cell.walls["top"]:
                    canvas[dr - 1][dc] = False
                if not cell.walls["bottom"]:
                    canvas[dr + 1][dc] = False
                if not cell.walls["left"]:
                    canvas[dr][dc - 1] = False
                if not cell.walls["right"]:
                    canvas[dr][dc + 1] = False

        canvas[1][0] = False                               # entrance
        canvas[2 * self.rows - 1][2 * self.cols] = False  # exit
        return canvas

    def display(self) -> str:
        """Render the maze using '#' for walls and spaces for passages."""
        canvas = self._build_canvas()
        return "\n".join(
            "".join(("#" if wall else " ") + " " for wall in row)
            for row in canvas
        )

    def display_unicode(self) -> str:
        """Render the maze using Unicode box-drawing characters for walls."""
        BOX = {
            (False, False, False, False): " ",
            (True,  False, False, False): "╵",
            (False, True,  False, False): "╷",
            (False, False, True,  False): "╴",
            (False, False, False, True ): "╶",
            (True,  True,  False, False): "│",
            (False, False, True,  True ): "─",
            (True,  False, True,  False): "┘",
            (True,  False, False, True ): "└",
            (False, True,  True,  False): "┐",
            (False, True,  False, True ): "┌",
            (True,  True,  True,  False): "┤",
            (True,  True,  False, True ): "├",
            (False, True,  True,  True ): "┬",
            (True,  False, True,  True ): "┴",
            (True,  True,  True,  True ): "┼",
        }

        canvas = self._build_canvas()
        height = len(canvas)
        width = len(canvas[0])

        def box_char(r: int, c: int) -> str:
            if not canvas[r][c]:
                return " "
            up    = r > 0          and canvas[r - 1][c]
            down  = r < height - 1 and canvas[r + 1][c]
            left  = c > 0          and canvas[r][c - 1]
            right = c < width - 1  and canvas[r][c + 1]
            return BOX[(up, down, left, right)]

        rows_out = []
        for r in range(height):
            row_chars = []
            for c in range(width):
                ch = box_char(r, c)
                # Extend horizontal wall segments with an extra '─' to match the
                # spacing used for the '#' display; otherwise pad with a space.
                extra = "─" if (r % 2 == 0 and c + 1 < width
                                and canvas[r][c] and canvas[r][c + 1]) else " "
                row_chars.append(ch + extra)
            rows_out.append("".join(row_chars))

        return "\n".join(rows_out)

    def as_code(self, var_name: str = "maze_grid") -> str:
        """Return a Python source snippet that declares the wall canvas as a 2D list.
        1 = wall, 0 = open passage/cell."""
        canvas = self._build_canvas()
        inner = ",\n    ".join(
            "[" + ", ".join("1" if wall else "0" for wall in row) + "]"
            for row in canvas
        )
        return f"{var_name} = [\n    {inner}\n]"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        rows = int(input("Rows  (default 10): ") or 10)
        cols = int(input("Cols  (default 20): ") or 20)
    except ValueError:
        print("Invalid input — using defaults (10 x 20).")
        rows, cols = 10, 20

    maze = Maze(rows, cols)
    print()
    print(maze.display())
    print()

    choice = input("\nDisplay with Unicode box-drawing symbols? [y/N]: ").strip().lower()
    if choice == "y":
        print()
        print(maze.display_unicode())
        print()
    print(maze.as_code())


if __name__ == "__main__":
    main()
