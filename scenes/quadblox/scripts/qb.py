from enum import Enum, auto
import random

# from https://colorkit.co/palette/ffadad-ffd6a5-fdffb6-caffbf-9bf6ff-a0c4ff-bdb2ff-ffc6ff/
colors = [
    (0, 0, 0),
    '#ffadad',
    '#ffd6a5',
    '#fdffb6',
    '#caffbf',
    '#9bf6ff',
    '#a0c4ff',
    '#bdb2ff',
    '#ffc6ff',
    (255, 255, 255),

]

class Shapes(Enum):
    I = auto()
    J = auto()
    L = auto()
    O = auto()
    S = auto()
    T = auto()
    Z = auto()


class Piece:

    def __init__(self, shape: Shapes | None = None):

        if shape is None:
            shape = random.choice(list(Shapes))

        # set our x and y start positions
        self.x = 4
        self.y = 0

        # store which shape we are
        self.shape = shape

        # make our box 4x4
        self.box_size = 4
        self.grid = [[0 for _ in range(self.box_size)] for _ in range(self.box_size)]

        # set our color
        self.color = int(shape.value)
        # set our shape
        self.set_shape()

        # rotate 1-4 times to normalize the shifting logic in rotate
        # and set the height and width of the piece in the grid
        rotations = random.randint(1, 4)
        while rotations:
            rotations -= 1
            self.rotate()

    def set_shape(self):
        shape = self.shape
        # populate our box with our shape
        if shape == Shapes.I:
            self.grid[0] = [1, 1, 1, 1]
        elif shape == Shapes.J:
            self.grid[0] = [1, 1, 1, 0]
            self.grid[1] = [0, 0, 1, 0]
        elif shape == Shapes.L:
            self.grid[0] = [1, 1, 1, 0]
            self.grid[1] = [1, 0, 0, 0]
        elif shape == Shapes.O:
            self.grid[1] = [0, 1, 1, 0]
            self.grid[2] = [0, 1, 1, 0]
        elif shape == Shapes.S:
            self.grid[0] = [0, 1, 1, 0]
            self.grid[1] = [1, 1, 0, 0]
        elif shape == Shapes.T:
            self.grid[0] = [1, 1, 1, 0]
            self.grid[1] = [0, 1, 0, 0]
        elif shape == Shapes.Z:
            self.grid[0] = [1, 1, 0, 0]
            self.grid[1] = [0, 1, 1, 0]


    def reverse_rotate_and_size(self):
        self.rotate()
        self.rotate()
        self.rotate()


    def rotate(self):
        # make our box 4x4
        new_grid = [[0 for _ in range(self.box_size)] for _ in range(self.box_size)]

        # special handling for I shape
        if self.shape == Shapes.I:
            if self.grid[1][1] == 1:
                # set horizontal
                new_grid[0] = [1, 1, 1, 1]
            else:
                # set vertical
                new_grid[0] = [0, 1, 0, 0]
                new_grid[1] = [0, 1, 0, 0]
                new_grid[2] = [0, 1, 0, 0]
                new_grid[3] = [0, 1, 0, 0]
        else:
            # rotate our shape in the new box
            new_grid[0] = [self.grid[3][0], self.grid[2][0], self.grid[1][0], self.grid[0][0]]
            new_grid[1] = [self.grid[3][1], self.grid[2][1], self.grid[1][1], self.grid[0][1]]
            new_grid[2] = [self.grid[3][2], self.grid[2][2], self.grid[1][2], self.grid[0][2]]
            new_grid[3] = [self.grid[3][3], self.grid[2][3], self.grid[1][3], self.grid[0][3]]


            # shift the piece up so the top most row is not empty
            while not any(new_grid[0]):
                new_grid.pop(0)
                new_grid.append([0, 0, 0, 0])

            # shift the piece left so the left most column is not empty
            while not any(row[0] for row in new_grid):
                for row in new_grid:
                    row.pop(0)
                    row.append(0)


        self.grid = new_grid

    def collides(self, board):


        for row in range(self.box_size):
            for col in range(self.box_size):
                x = self.x + col
                y = self.y + row

                # check if we have a piece in the grid here
                if self.grid[row][col]:
                    # check if we are out of bounds
                    if x < 0 or x >= board.cols or y >= board.rows:
                        return True
                    # check if we collide with another piece
                    if y >= 0 and board.grid[y][x]:
                        return True

        return False

    def __str__(self):
        return "\n".join("".join(str(cell) for cell in row) for row in self.shape[self.rotation])


class Board:
    def __init__(self, pos=(0, 0), block_size=12):
        self.rows = 24
        self.cols = 10
        self.pos = pos
        self.grid = [[random.randint(1,len(colors) - 1) for _ in range(self.cols)] for _ in range(self.rows)]
        self.block_size = block_size
        self.game_over = True

        # scoring variables
        self.points = 0
        self.lines_cleared = 0
        self.clears = [0, 0, 0, 0]
        self.blocks_placed = 0
        self.players = 0

    def place(self, piece: Piece):
        self.blocks_placed += 1
        for row in range(piece.box_size):
            for col in range(piece.box_size):
                if piece.grid[row][col]:
                    self.grid[piece.y + row][piece.x + col] = piece.color

        self.score()

    def score(self):
        lines_cleared = 0
        for row in range(self.rows):
            if all(self.grid[row]):
                lines_cleared += 1
                self.grid.pop(row)
                self.grid.insert(0, [0 for _ in range(self.cols)])

        self.lines_cleared += lines_cleared

        if lines_cleared:
            self.clears[lines_cleared - 1] += 1

        self.points = (
            (   10 * self.clears[0]) +
            (  100 * self.clears[1]) +
            ( 1000 * self.clears[2]) +
            (10000 * self.clears[3]) +
            self.blocks_placed
        )

        return lines_cleared

    def dead(self):
        return any(self.grid[0]) or any(self.grid[1]) or any(self.grid[2]) or any(self.grid[3])

    def clear(self):
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def kill(self):
        self.grid = [[random.randint(1,len(colors) - 1) for _ in range(self.cols)] for _ in range(self.rows)]

    def reset(self):
        self.score = 0
        self.lines_cleared = 0
        self.clears = [0, 0, 0, 0]
        self.blocks_placed = 0
        self.clear()

    def export_board(self) -> str:
        """Export the board state as a string usable by the import function

        Returns:
            str: _description_
        """
        return ";".join(":".join(str(cell) for cell in row) for row in self.grid)

    def import_board(self, board_state_string: str) -> None:
        """Import a board state from a string

        Args:
            board_state_string (str): The string to import
        """
        self.grid = [[int(cell) for cell in row.split(":")] for row in board_state_string.split(";")]

    def add_line_to_bottom(self):
        self.grid.pop(0)
        self.grid.append([random.randint(1,len(colors) - 1) for _ in range(self.cols)])
        # empty 1 cell
        self.grid[-1][random.randint(0, self.cols - 1)] = 0

    def __str__(self):
        return "\n".join("".join(str(cell) for cell in row) for row in self.grid)
