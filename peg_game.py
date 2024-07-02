from __future__ import annotations as _
from copy import deepcopy

class Board:
    """
    Peg board representing an n-depth Cracker Barrel peg board game.
    The board positions are represented in the end as:
           1
          2 3
         4 5 6
        7 8 9 10
      ...      ...

    and moves are displayed as "(<from>, <to>)" with the corresponding values.
    The underlying logic, however, is simplified with a 2D array.
    """

    def __init__(self, depth: int) -> None:
        """
        New board where all values are filled besides the apex position.
        `depth` is inclusive, meaning depth of 3 yields 3 rows.

        """
        self.depth = depth

        # logs the moves made to get to the current state
        # each "move" is a tuple of tuples containing the from and to coordinates
        self.move_log: [((int, int), (int, int))] = []

        # number of pegs remaining
        self.count: int = triangle_number(depth) - 1

        # 0 is vacant, 1 is filled
        self.board: [[int]] = [[0]]
        for x in range(1, depth):
            self.board.append([1] * (x + 1))  # pythonic repeated list

    def solve(self) -> Board:
        """
        Backtracking algorithm to find the first solved `Board`.
        Returns `None` if no solutions are possible.
        """
        # Base cases: win or stuck
        if self.is_win():
            return self
        all_moves = self.all_possible_moves()
        if 0 == len(all_moves):
            return None

        # Loop over all possbile, return first found solution
        for move in all_moves:
            solution = self.make_move(move[0], move[1]).solve()
            if solution is not None:
                return solution

        # if no solutions found, self is a dead-end position
        return None

    def all_possible_moves(self) -> [((int, int), (int, int))]:
        out = []
        for row in range(0, self.depth):
            for col in range(0, row + 1):
                # append all possible from each point
                out.extend(self.all_moves_from_point(row, col))
        return out

    def all_moves_from_point(self, row: int, col: int) -> iter((int, int), (int, int)):
        # exit if empty position
        if self.board[row][col] == 0:
            return []

        # theoretically 8 ways to move from any point
        # lots of filters...

        # they all start at (row, col) so this is just the list of terminal points
        # cannot have col + 2 on different rows in this flattened model, that is not in line with the
        # actual game and how each peg can have up to 6 holes surrounding it. col - 2 on different rows
        # is ok because in the 2D array everything is squished to the left
        potential_endpoints = [(row, col + 2), (row, col - 2), (row + 2, col), (row - 2, col),
                               (row + 2, col - 2), (row - 2, col - 2)]

        # keep only coordinates with positive values
        pos_idx_filter = filter(lambda coord: coord[0] >= 0 and coord[1] >= 0, potential_endpoints)

        # keep in bounds coordinates
        # row must be less than the depth and col must be less than or equal to the corresponding row
        potential_endpoints = filter(lambda coord: coord[0] < self.depth and coord[0] >= coord[1], pos_idx_filter)

        # keep only open endpoints
        avail_endpts = filter(lambda coord: self.board[coord[0]][coord[1]] == 0, potential_endpoints)

        # keep coordinates whose midpoints (jumped-over pegs) are filled (funky variable names here so I
        # don't have to wrap lines)
        all_eps = filter(lambda coord: self.board[(row + coord[0]) // 2][(col + coord[1]) // 2] == 1, avail_endpts)

        # map all possible endpoints to a move-style pair of tuples ((start_row, start_col), (end_row, end_col))
        return map(lambda endpoint: ((row, col), endpoint), all_eps)

    # assumes the input move is valid.
    def make_move(self, jump_from: (int, int), jump_to: (int, int)) -> Board:
        new_board: Board = self.copy()  # don't mutate current working board

        # peg jump
        new_board.board[jump_from[0]][jump_from[1]] = 0
        new_board.board[jump_to[0]][jump_to[1]] = 1

        # nullify jumped-over peg
        # since we are assuming this is a valid jump, it is just the midpoint
        row = (jump_from[0] + jump_to[0]) // 2
        col = (jump_from[1] + jump_to[1]) // 2
        new_board.board[row][col] = 0

        new_board.move_log.append((jump_from, jump_to))
        new_board.count -= 1
        return new_board

    def is_win(self) -> bool:
        return 1 == self.count

    def copy(self) -> Board:
        return deepcopy(self)

    # can make this fancier but not really worth the time
    def __str__(self) -> str:
        out: str = ""
        for row in self.board:
            for col in row:
                out += "*" if 1 == col else "o"
            out += "\n"
        return out.strip()

    def __repr__(self) -> str:
        return str(self)

    def pretty_solution(self) -> str:
        # peg position number as described at the top is triangle_number of the row
        # plus col number plus 1
        out: str = ""
        for move in self.move_log:
            start_coord = move[0]
            end_coord = move[1]
            out += str(triangle_number(start_coord[0]) + start_coord[1] + 1)
            out += " -> "
            out += str(triangle_number(end_coord[0]) + end_coord[1] + 1)
            out += ", "
        return out[:-2]  # prune off the last ", "

def triangle_number(n: int) -> int:
    return (n * (n + 1)) // 2


def main(argv: [str]) -> None:
    """
    The main function to make this program slightly interesting to use.
    `argv` should be a single arg with just the depth as an `int`.
    """
    try:
        depth = int(argv[0])
        board = Board(depth)
        solution = board.solve()
        if solution is not None:
            print(f"Solution: {solution.pretty_solution()}")
        else:
            print(f"No solution for depth of {depth}.")
    except ValueError:
        print(f"Expected an int, got: {argv[0]}")
        exit(1)


if __name__ == '__main__':
    from sys import argv
    # omit the program name in argv
    main(argv[1:])
