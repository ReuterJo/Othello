# Author: Jonathan Reuter
# GitHub username: ReuterJo
# Date: 5/27/2023
# Description: This program implements a text-based version of the strategy board game called Othello. For more
# information about this game, including the rules and history, please see https://en.wikipedia.org/wiki/Reversi.

class Othello:
    """
    Represents a game of Othello, including board state, players, and game rules. Uses the Player class to keep
    track of player information.
    """
    def __init__(self):
        """Creates a new game, with white and black pieces setup corresponding to their starting positions"""
        self._board = [['*', '*', '*', '*', '*', '*', '*', '*', '*', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'O', 'X', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', 'X', 'O', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '.', '.', '.', '.', '.', '.', '.', '.', '*'],
                       ['*', '*', '*', '*', '*', '*', '*', '*', '*', '*']]
        self._player_list = []

    def get_player_list(self):
        """Returns the list of players playing the game"""
        return self._player_list

    def get_board(self):
        """Returns the state of the board as a 2D list"""
        return self._board

    def return_player_name_for_color(self, player_color):
        """Returns the name of the player of the selected color. Assumes one white player and one black player."""
        for player in self._player_list:
            if player_color == player.get_player_color():
                return player.get_player_name()
        return 'Invalid - a player of that color was not found'

    def print_board(self):
        """Prints the state of the game board to the display"""
        # print column numbering
        print(' ', end=' ')
        for column in range(len(self._board[0])):
            print(column, end=' ')
        print()

        # print the board including row numbering
        for row in range(len(self._board)):
            print(row, end=' ')
            for column in range(len(self._board[0])):
                print(self._board[row][column], end=' ')
            print()

    def create_player(self, player_name, color):
        """Creates a new player and adds them to the player list"""
        self._player_list.append(Player(player_name, color))

    def return_winner(self):
        """Returns the winner of the game, or tie if both the black and white player have an equal number of pieces"""
        # tabulate number of pieces of each color on the board
        score = self.tabulate_score()

        # if white has the higher score, declare the white player the winner
        if score[0] > score[1]:
            return "Winner is white player: " + self.return_player_name_for_color('white')

        # if black has the higher score, declare the black player the winner
        elif score[0] < score[1]:
            return "Winner is black player: " + self.return_player_name_for_color('black')

        # otherwise, declare a tie
        else:
            return "It's a tie"

    def return_available_positions(self, color):
        """Returns the available move positions for a player of a chosen color"""
        # initialize an empty set for available positions
        available_positions = set()

        # determine piece type based upon color
        if color == 'white':
            own_piece = 'O'
            opponent_piece = 'X'
        else:
            own_piece = 'X'
            opponent_piece = 'O'

        # iterate through the board position by position and identify the position of all own_pieces
        for row in range(len(self._board)):
            for column in range(len(self._board[0])):
                if self._board[row][column] == own_piece:
                    # for each position of own_piece, find all valid moves originating from that position, and
                    # add them to the available positions set
                    available_positions.update(self.find_valid_moves((row, column), own_piece, opponent_piece))

        # convert set of available positions into a list of available positions
        return list(available_positions)

    def find_valid_moves(self, position, own_piece, opponent_piece):
        """
        Helper function for rec_find_valid_moves. Given a position, searches in all directions for an opponents piece,
        before starting the recursive process of moving piece by piece in a direction to evaluate if there exists a
        valid move or not. Returns the valid moves as a set of positions.
        """
        # initialize an empty set of valid moves for that position
        valid_moves = set()

        # create a list of all 8 directions relative to the position received
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        # search in all directions from the position for an opponents piece
        for direction in directions:
            if self._board[position[0] + direction[0]][position[1] + direction[1]] == opponent_piece:
                # if found, start the recursive process of determining if there is a valid move in that direction
                result = self.rec_find_valid_moves((position[0] + direction[0], position[1] + direction[1]), direction,
                                                   own_piece, opponent_piece)
                if result is not None:
                    valid_moves.add(result)

        # return the set of valid moves for that position
        return valid_moves

    def rec_find_valid_moves(self, position, direction, own_piece, opponent_piece):
        """
        Recursively walks from a position in a direction to determine if a valid move exists. If so, returns that valid
        position. Otherwise, return None.
        """
        # name board spaces representing empty spaces and the edge for better readability
        edge = '*'
        blank = '.'

        # base case - if next position is edge, return none
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == edge:
            return None

        # base case - if next position is blank, return the position of the blank space
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == blank:
            return position[0] + direction[0], position[1] + direction[1]

        # base case - if next position is own_piece, return none
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == own_piece:
            return None

        # recursive case - if next position is opponent_piece, check next position in direction
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == opponent_piece:
            return self.rec_find_valid_moves((position[0] + direction[0], position[1] + direction[1]),
                                             direction, own_piece, opponent_piece)

    def make_move(self, color, piece_position):
        """Places a piece of the chosen color at the corresponding location. Returns the updated board state."""
        # place a piece of the chosen color at the board location
        if color == 'white':
            self._board[piece_position[0]][piece_position[1]] = 'O'
        else:
            self._board[piece_position[0]][piece_position[1]] = 'X'

        # flip any pieces captured by placing that piece
        self.flip_captured_pieces(color, piece_position)

        # return the new state of the board after the piece has been placed and all captures are made
        return self._board

    def flip_captured_pieces(self, color, position):
        """
        Helper function for rec_flip_captured pieces. Given a position, searches in all directions for an opponents
        piece, before starting the recursive process of moving piece by piece in a direction to evaluate if there are
        captured pieces or not.
        """
        # determine piece type based upon color
        if color == 'white':
            own_piece = 'O'
            opponent_piece = 'X'
        else:
            own_piece = 'X'
            opponent_piece = 'O'

        # create a list of all 8 directions relative to the position received
        directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

        # search in all directions from the position for an opponents piece
        for direction in directions:
            if self._board[position[0] + direction[0]][position[1] + direction[1]] == opponent_piece:
                # if found, start the recursive process of determining if there is any captured pieces in that direction
                self.rec_flip_captured_pieces((position[0] + direction[0], position[1] + direction[1]), direction,
                                              own_piece, opponent_piece)

    def rec_flip_captured_pieces(self, position, direction, own_piece, opponent_piece, positions_visited=None):
        """
        Recursively walks from a position in a direction to determine if a captured pieces exist. If so, it converts
        those positions to be the color representing the capturing player.
        """
        # name board spaces representing empty spaces and the edge for better readability
        edge = '*'
        blank = '.'

        # if not positions have been visited, create an empty set
        if positions_visited is None:
            positions_visited = set()

        # add the current position to the list of positions visited, to keep track of pieces that could potentially be
        # captured
        positions_visited.add(position)

        # base case - if next position in the direction is edge, do nothing
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == edge:
            return

        # base case - if next position in the direction is blank, do nothing
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == blank:
            return

        # base case - if next position in the direction is own_piece, flip all pieces recorded in positions_visited
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == own_piece:
            for update_position in positions_visited:
                self._board[update_position[0]][update_position[1]] = own_piece
            return

        # recursive case - if next position in the direction is opponent_piece, step to next position and evaluate again
        if self._board[position[0] + direction[0]][position[1] + direction[1]] == opponent_piece:
            next_position = (position[0] + direction[0], position[1] + direction[1])
            self.rec_flip_captured_pieces(next_position, direction, own_piece, opponent_piece, positions_visited)
            return

    def play_game(self, player_color, piece_position):
        """
        Attempts to make a game move by placing a piece of the player's color at the chosen position. If no there are
        no available moves for both players, the game ends. If there are no available moves for the active player,
        an empty list is returned, indicating that they must pass. If the chosen position is invalid, a list of valid
        available positions is printed, and 'Invalid Move' is return. Lastly, if the move is valid, then the board is
        updated accordingly.
        """
        # determine the active player's available positions
        active_player_available_positions = self.return_available_positions(player_color)

        # determine the inactive player's available positions
        if player_color == 'white':
            inactive_player_available_positions = self.return_available_positions('black')
        else:
            inactive_player_available_positions = self.return_available_positions('white')

        # if both the active and inactive player have no available positions to move to, end the game
        if len(active_player_available_positions) == 0 and len(inactive_player_available_positions) == 0:
            # calculate the score and display it
            score = self.tabulate_score()
            print('Game is ended  white piece: ', score[0], ' black piece: ', score[1])

            # and return the winner of the game
            return self.return_winner()

        # if only the active player has no available positions, return an empty list indicating that he/she must pass
        if len(active_player_available_positions) == 0:
            return active_player_available_positions

        # if the position chosen is valid, update the board accordingly
        if piece_position in active_player_available_positions:
            self.make_move(player_color, piece_position)
            return
        # if the position is invalid, do not update the board and inform the user of the valid positions
        # for his/her color
        else:
            print("Here are the valid moves:", active_player_available_positions)
            return "Invalid move"

    def tabulate_score(self):
        """
        Tabulates the current score determine by the number of pieces on the board of each color. Returns the score as a
        tuple (white_score, black_score).
        """
        # set score for white and black to be zero
        white_score = 0
        black_score = 0

        # iterate through the board position by position, incrementing score each time a piece of the corresponding
        # color is found
        for row in range(len(self._board)):
            for column in range(len(self._board[0])):
                if self._board[row][column] == 'O':
                    white_score += 1
                elif self._board[row][column] == 'X':
                    black_score += 1

        # return score as a tuple
        return white_score, black_score


class Player:
    """
    Represents a player participating in the Othello board game. Is used by the Othello class as part of
    keeping track of the game state.
    """
    def __init__(self, player_name, color):
        """Creates a new player"""
        self._player_name = player_name
        self._color = color

    def get_player_name(self):
        """Returns the name of the player"""
        return self._player_name

    def get_player_color(self):
        """Returns the color of pieces representing the player in the game"""
        return self._color
