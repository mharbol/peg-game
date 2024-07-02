import peg_game as game
import unittest

class TestPegBoard(unittest.TestCase):

    vsauce_solution = [((2, 2), (0, 0)), ((2, 0), (2, 2)), ((0, 0), (2, 0)),
                       ((3, 3), (1, 1)), ((3, 0), (1, 0)), ((4, 2), (2, 0)),
                       ((2, 0), (0, 0)), ((0, 0), (2, 2)), ((4, 4), (4, 2)),
                       ((4, 1), (4, 3)), ((2, 2), (4, 2)), ((4, 3), (4, 1)),
                       ((4, 0), (4, 2))]

    def test_init(self):
        board = game.Board(5)
        self.assertEqual(board.count, 14)
        self.assertEqual(board.board[0], [0])
        self.assertEqual(board.board[1], [1, 1])
        self.assertEqual(board.board[2], [1, 1, 1])
        self.assertEqual(board.board[3], [1, 1, 1, 1])
        self.assertEqual(board.board[4], [1, 1, 1, 1, 1])
        self.assertEqual(board.move_log, [])
        self.assertFalse(board.is_win())

    def test_str(self):
        board = game.Board(5)
        self.assertEqual(str(board), "o\n**\n***\n****\n*****")

    def test_vsause_solution(self):
        board = game.Board(5)
        for move in TestPegBoard.vsauce_solution:
            board = board.make_move(move[0], move[1])
        self.assertTrue(board.is_win())
        self.assertEqual(1, board.board[4][2])
        self.assertEqual(TestPegBoard.vsauce_solution, board.move_log)

    def test_all_possible_moves(self):
        board = game.Board(7)
        self.assertEqual(sorted(board.all_possible_moves()), sorted([((2, 2), (0, 0)), ((2, 0), (0, 0))]))
        board.board[4][2] = 0
        # board.board = [[0],
        #                [1, 1],
        #                [1, 1, 1],
        #                [1, 1, 1, 1],
        #                [1, 1, 0, 1, 1],
        #                [1, 1, 1, 1, 1, 1],
        #                [1, 1, 1, 1, 1, 1, 1]]
        self.assertEqual(sorted(board.all_possible_moves()), sorted([((2, 0), (0, 0)), ((2, 2), (4, 2)),
                                                                     ((2, 2), (0, 0)), ((4, 0), (4, 2)),
                                                                     ((4, 4), (4, 2)), ((6, 2), (4, 2)),
                                                                     ((6, 4), (4, 2))]))

        board.board[6][0] = 0
        # board.board = [[0],
        #                [1, 1],
        #                [1, 1, 1],
        #                [1, 1, 1, 1],
        #                [1, 1, 0, 1, 1],
        #                [1, 1, 1, 1, 1, 1],
        #                [0, 1, 1, 1, 1, 1, 1]]
        self.assertEqual(sorted(board.all_possible_moves()), sorted([((2, 0), (0, 0)), ((2, 2), (4, 2)),
                                                                     ((2, 2), (0, 0)), ((4, 0), (4, 2)),
                                                                     ((4, 0), (6, 0)), ((4, 4), (4, 2)),
                                                                     ((6, 2), (6, 0)), ((6, 2), (4, 2)),
                                                                     ((6, 4), (4, 2))]))
        board.board[3][1] = 0
        # board.board = [[0],
        #                [1, 1],
        #                [1, 1, 1],
        #                [1, 0, 1, 1],
        #                [1, 1, 0, 1, 1],
        #                [1, 1, 1, 1, 1, 1],
        #                [0, 1, 1, 1, 1, 1, 1]]
        self.assertEqual(sorted(board.all_possible_moves()), sorted([((1, 1), (3, 1)), ((2, 0), (0, 0)),
                                                                     ((2, 2), (4, 2)), ((2, 2), (0, 0)),
                                                                     ((3, 3), (3, 1)), ((4, 0), (4, 2)),
                                                                     ((4, 0), (6, 0)), ((4, 4), (4, 2)),
                                                                     ((5, 1), (3, 1)), ((6, 2), (6, 0)),
                                                                     ((6, 2), (4, 2)), ((6, 4), (4, 2))]))
        board.board = [[0],
                       [1, 1],
                       [1, 0, 0],
                       [0, 0, 0, 0],
                       [1, 0, 0, 0, 0],
                       [1, 0, 0, 0, 0, 0],
                       [0, 1, 0, 0, 0, 1, 1]]
        self.assertEqual(sorted(board.all_possible_moves()), sorted(
            [((1, 0), (3, 0)), ((2, 0), (0, 0)), ((4, 0), (6, 0)), ((5, 0), (3, 0)), ((6, 6), (6, 4))]))

class TestUtils(unittest.TestCase):

    def test_triangle_number(self):
        self.assertEqual(game.triangle_number(1), 1)
        self.assertEqual(game.triangle_number(2), 3)
        self.assertEqual(game.triangle_number(3), 6)
        self.assertEqual(game.triangle_number(4), 10)
        self.assertEqual(game.triangle_number(5), 15)
