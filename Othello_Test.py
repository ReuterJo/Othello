# Author: Jonathan Reuter
# GitHub username: ReuterJo
# Date: 5/27/2023
# Description: Contains test cases for Othello.py

import unittest
from Othello import Othello, Player


class TestOthello(unittest.TestCase):
    """Test cases for Othello.py"""

    def test_case_1(self):
        """Test init and get methods for Othello class"""
        game = Othello()
        self.assertEqual([], game.get_player_list())
        self.assertEqual([['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']],
                         game.get_board())

    def test_case_2(self):
        """Test create_player method and Player class"""
        game = Othello()
        self.assertEqual([], game.get_player_list())
        game.create_player('Bob', 'white')
        players = game.get_player_list()
        self.assertEqual('Bob', players[0].get_player_name())
        self.assertEqual('white', players[0].get_player_color())
        game.create_player('Sarah', 'black')
        players = game.get_player_list()
        self.assertEqual('Bob', players[0].get_player_name())
        self.assertEqual('white', players[0].get_player_color())
        self.assertEqual('Sarah', players[1].get_player_name())
        self.assertEqual('black', players[1].get_player_color())

    def test_case_3(self):
        """Test return_player_name_for_color"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        self.assertEqual('Bob', game.return_player_name_for_color('white'))
        self.assertEqual('Sarah', game.return_player_name_for_color('black'))

    def test_case_4(self):
        """Test print_board"""
        game = Othello()
        # game.print_board()

    def test_case_5(self):
        """Test return_winner"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        self.assertEqual("It's a tie", game.return_winner())
        game.make_move('black', (7, 7))
        self.assertEqual("Winner is black player: Sarah", game.return_winner())
        game.make_move('white', (7, 7))
        self.assertEqual("Winner is white player: Bob", game.return_winner())

    def test_case_6(self):
        """Test return_available_positions, which includes find_valid_moves, and rec_find_valid_moves"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        self.assertEqual([(3, 4), (5, 6), (6, 5), (4, 3)], game.return_available_positions('black'))
        self.assertEqual([(5, 3), (4, 6), (6, 4), (3, 5)], game.return_available_positions('white'))

    def test_case_7(self):
        """Test make_move, which includes flip_captured_pieces, and rec_flip_captured_pieces"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        game.make_move('black', (6, 5))
        board = game.get_board()
        self.assertEqual('X', board[6][5])
        self.assertEqual('X', board[5][5])

    def test_case_8(self):
        """Test tabulate_score"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        self.assertEqual((2, 2), game.tabulate_score())

    def test_case_9(self):
        """Test play_game, when making a valid move"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        game.play_game('black', (6, 5))
        board = game.get_board()
        self.assertEqual('X', board[6][5])
        self.assertEqual('X', board[5][5])

    def test_case_10(self):
        """Test play_game, when making an invalid move"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        # self.assertEqual("Invalid move", game.play_game('black', (7, 7)))

    def test_case_11(self):
        """Test play_game, when the active player has no valid moves"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        game.make_move('black', (4, 4))
        game.print_board()
        game.make_move('black', (5, 5))
        game.print_board()
        game.make_move('white', (4, 6))
        game.make_move('white', (4, 7))
        game.make_move('white', (4, 8))
        game.make_move('white', (3, 7))
        game.make_move('white', (2, 8))
        self.assertEqual([], game.play_game('black', (7, 7)))

    def test_case_12(self):
        """Test play_game, when both active and inactive players have no valid moves; end the game"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        game.make_move('black', (4, 4))
        game.make_move('black', (5, 5))
        game.make_move('white', (4, 6))
        game.make_move('white', (4, 7))
        game.make_move('white', (4, 8))
        game.make_move('white', (3, 7))
        game.make_move('white', (2, 8))
        game.make_move('black', (4, 3))
        game.make_move('black', (4, 2))
        game.make_move('black', (4, 1))
        game.make_move('black', (6, 4))
        game.make_move('black', (7, 3))
        game.make_move('black', (8, 2))
        # self.assertEqual('Winner is black player: Sarah', game.play_game('black', (7, 7)))

    def test_case_13(self):
        """Actually play a real game of Othello, just for fun"""
        game = Othello()
        game.create_player('Bob', 'white')
        game.create_player('Sarah', 'black')
        # game.print_board()
        game.play_game('black', (3, 4))
        # game.print_board()
        game.play_game('white', (3, 5))
        # game.print_board()
        game.play_game('black', (3, 6))
        # game.print_board()
        game.play_game('white', (2, 5))
        # game.print_board()
        game.play_game('black', (2, 6))
        game.play_game('white', (4, 7))
        # game.print_board()
        game.play_game('black', (2, 7))
        game.play_game('white', (4, 3))
        # game.print_board()
        game.play_game('black', (3, 2))
        game.play_game('white', (3, 3))
        # game.print_board()
        game.play_game('black', (1, 5))
        game.play_game('white', (5, 3))
        # game.print_board()
        game.play_game('black', (6, 2))
        game.play_game('white', (2, 1))
        # game.print_board()
        game.play_game('black', (3, 1))
        game.play_game('white', (5, 2))
        # game.print_board()
        game.play_game('black', (1, 1))
        game.play_game('white', (1, 6))
        # game.print_board()
        game.play_game('black', (1, 4))
        game.play_game('white', (2, 2))
        # game.print_board()
        game.play_game('black', (1, 3))
        game.play_game('white', (7, 2))
        # game.print_board()
        game.play_game('black', (6, 3))
        game.play_game('white', (6, 5))
        # game.print_board()
        game.play_game('black', (8, 1))
        game.play_game('white', (1, 8))
        # game.print_board()
        game.play_game('black', (5, 8))
        game.play_game('white', (8, 2))
        # game.print_board()
        game.play_game('black', (8, 3))
        game.play_game('white', (7, 4))
        # game.print_board()
        game.play_game('black', (6, 1))
        game.play_game('white', (4, 6))
        # game.print_board()
        game.play_game('black', (7, 1))
        game.play_game('white', (2, 3))
        # game.print_board()
        game.play_game('black', (6, 4))
        game.play_game('white', (7, 3))
        # game.print_board()
        game.play_game('black', (5, 6))
        game.play_game('white', (8, 4))
        # game.print_board()
        game.play_game('black', (1, 2))
        game.play_game('white', (5, 7))
        # game.print_board()
        game.play_game('black', (1, 7))
        game.play_game('white', (3, 7))
        # game.print_board()
        game.play_game('black', (3, 8))
        game.play_game('white', (2, 8))
        # game.print_board()
        game.play_game('black', (6, 8))
        game.play_game('white', (5, 1))
        # game.print_board()
        game.play_game('black', (4, 1))
        game.play_game('white', (7, 5))
        # game.print_board()
        game.play_game('black', (4, 8))
        game.play_game('white', (2, 4))
        # game.print_board()
        game.play_game('black', (4, 2))
        game.play_game('white', (7, 8))
        # game.print_board()
        game.play_game('black', (8, 6))
        game.play_game('white', (8, 5))
        # game.print_board()
        game.play_game('black', (6, 6))
        game.play_game('white', (8, 7))
        # game.print_board()
        game.play_game('black', (8, 8))
        game.play_game('white', (7, 6))
        # game.print_board()
        game.play_game('black', (7, 7))
        game.play_game('white', (6, 7))
        # game.print_board()
        # print(game.play_game('black', (8,8)))
