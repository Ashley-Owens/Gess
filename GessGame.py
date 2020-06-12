# Author: Ashley Owens
# Date: 6/4/2020
# Description: CS 162, Portfolio Project
# Implementation of the board game Gess.
# Please set PyCharm to Dark Mode for best game board experience.


class GessGame:
    """
    Class designed for playing Gess, an abstract board game. GessGame tracks player turn, game
    state, game board, and board positions. Allows for a player to resign, make a move, uses
    helper methods to determine valid piece movements based on stone locations, and updates the
    game attributes accordingly. Communicates with GessBoard using composition to gain access to
    the game board and stone locations.
    """
    def __init__(self):
        """
        Initializes private data members.
        """
        self._turn = 'BLACK'
        self._game_state = 'UNFINISHED'
        self._obj_board = GessBoard()
        self._positions = self._obj_board.set_positions()

    def get_turn(self):
        """
        :return: current player turn (string)
        """
        return self._turn

    def get_game_state(self):
        """
        :return: current game state (string)
        """
        return self._game_state

    def get_board(self):
        """
        :return: game board instance
        """
        return self._obj_board.get_board()

    def print_board(self):
        """
        :return: prints the game board
        """
        return self._obj_board.print_board()

    def set_turn(self):
        """
        Sets the player turn to the opposite player.
        :return: None
        """
        if self._turn == 'BLACK':
            self._turn = 'WHITE'
        else:
            self._turn = 'BLACK'

    def resign_game(self):
        """
        Allows current player to resign, changing the game state.
        :return: current game state (string)
        """
        if self._game_state == 'UNFINISHED':
            if self._turn == 'BLACK':
                self._game_state = 'WHITE_WON'
            else:
                self._game_state = 'BLACK_WON'
        return self._game_state

    def make_move(self, xy, xy2):
        """
        Utilizing helper methods, determines if start and end piece positions are valid movements
        based on Gess game rules. If valid, updates stone locations, player turn, and game state.
        :param xy: center position of starting piece (string)
        :param xy2: center position of ending piece (string)
        :return: True if move is valid, else False.
        """
        xy, xy2 = xy.upper(), xy2.upper()

        # Changes inputs to a (row, column) tuple.
        tup = self.get_coordinates(xy)
        tup2 = self.get_coordinates(xy2)

        # Checks for out of bounds row/column coordinates or identical coordinates.
        if tup is False or tup2 is False or tup == tup2:
            return False

        # Stores piece values in a list.
        piece = self.get_footprint(tup)
        piece2 = self.get_footprint(tup2)

        # Checks for illegal starting move conditions.
        if self.legal_start(piece) is False:
            return False

        # If center position is blank, piece may only move up to 3 squares.
        if self._positions.get(xy) == ' ':
            if self.move_three(tup, tup2, piece) is False:
                return False

        # If center position contains a stone, piece may move any unobstructed distance.
        if self._positions.get(xy) != ' ':
            if self.legal_move(tup, tup2, piece) is False:
                return False

        # Updates starting and ending footprint values.
        self.set_footprint(tup, [" ", " ", " ", " ", " ", " ", " ", " ", " "])
        self.set_footprint(tup2, piece)

        if self._turn == 'BLACK':

            # Reverts footprint values to disallow player from destroying their own ring.
            if self.ring_present('B') is False:
                self.set_footprint(tup, piece)
                self.set_footprint(tup2, piece2)
                return False

            # If move results in destruction of WHITE player's ring, updates game state.
            if self.ring_present('W') is False:
                self._game_state = 'BLACK_WON'

        if self._turn == 'WHITE':

            # Reverts footprint values to disallow player from destroying their own ring.
            if self.ring_present('W') is False:
                self.set_footprint(tup, piece)
                self.set_footprint(tup2, piece2)
                return False

            # If move results in destruction of BLACK player's ring, updates game state.
            if self.ring_present('B') is False:
                self._game_state = 'WHITE_WON'

        self.del_edges()
        self.set_turn()
        return True

    def get_coordinates(self, xy):
        """
        Uses input parameter to find row, column coordinates on game board.
        :param xy: center piece position (string)
        :return: tuple of (row, column) coordinates
        """
        # Obtains row and column coordinates from input.
        col = ord(xy[0]) - ord('A')
        try:
            row = int(xy[1:])
        except ValueError:
            return False

        # Checks for out of bounds piece positions.
        if col not in range(1, 19) or row not in range(2, 20):
            return False

        return row, col

    def get_footprint(self, tup):
        """
        Using tuple information, finds associated board values contained in the piece footprint.
        :param tup: (row, column) tuple
        :return: list of board values (list of strings)
        """
        row, col = tup
        piece = [self._obj_board.get_board()[i][col-1:col+2] for i in range(row-1, row+2)]
        return [item for sublist in piece for item in sublist]

    def legal_start(self, piece):
        """
        Checks all starting conditions to ensure piece is valid.
        :param piece: list of board values (strings)
        :return: True if start conditions and move are valid, else False.
        """
        # Game has already been won.
        if self._game_state != 'UNFINISHED':
            return False

        # Invalid piece due to presence of opponent's stone or lack of
        # player's stone. Also catches incorrect player calling make_move.
        if self._turn == 'BLACK':
            if 'W' in piece or 'B' not in piece:
                return False
        if self._turn == 'WHITE':
            if 'B' in piece or 'W' not in piece:
                return False

        # Invalid piece due to only one stone in the center.
        if piece[4] != ' ':
            count = 0
            for i in piece:
                if i == ' ':
                    count += 1
            if count == 8:
                return False
        return True

    def ring_present(self, player):
        """
        Searches the game board for presence of a player's ring.
        :param player: 'B' or 'W' (string)
        :return: True if ring present, else False
        """
        # Searches all empty board positions for a ring surrounding them.
        for key, value in self._positions.items():
            if value == ' ':
                tup = self.get_coordinates(key)
                if tup is False:
                    continue
                else:
                    piece = self.get_footprint(tup)
                    count = 0
                    for i in piece:
                        if i == player:
                            count += 1
                    if count == 8:
                        return True
        return False

    def move_three(self, tup, tup2, piece):
        """
        Checks coordinates to ensure they are within three positions of each other.
        Uses helper functions to determine if move is unobstructed.
        :param tup: (row, column) tuple of starting piece coordinates
        :param tup2: (row, column) tuple of ending piece coordinates
        :param piece: list of board values (list of strings)
        :return: True if move is valid, else False
        """
        row, col = tup
        row2, col2 = tup2

        if row2 in range(row, row+4) or row2 in range(row, row-4, -1):
            if col2 in range(col, col+4) or col2 in range(col, col-4, -1):
                if self.legal_move(tup, tup2, piece) is True:
                    return True
        return False

    def legal_move(self, tup, tup2, piece):
        """
        Using stone positions on piece, determines direction of piece movement by start and end coordinates.
        Once directional movement is obtained, uses helper functions to determine if move is unobstructed.
        :param tup: (row, column) tuple of starting piece coordinates
        :param tup2: (row, column) tuple of ending piece coordinates
        :param piece: list of board values (list of strings)
        :return: True if move is valid, else False
        """
        row, col = tup
        row2, col2 = tup2

        # Checks for stone position in NW coordinate.
        if piece[0] != ' ':
            if row2 in range(row-1, row-18, -1) and col2 in range(col-1, col-18, -1):
                if self.move_nw(row, row2, col) is True:
                    return True
        # Checks for stone position in N coordinate.
        if piece[1] != ' ':
            if row2 in range(row-1, row-18, -1) and col2 in range(col, col+1):
                if self.move_north(row, row2, col) is True:
                    return True
        # Checks for stone position in NE coordinate.
        if piece[2] != ' ':
            if row2 in range(row-1, row-18, -1) and col2 in range(col+1, col+18):
                if self.move_ne(row, row2, col) is True:
                    return True
        # Checks for stone position in W coordinate.
        if piece[3] != ' ':
            if row2 in range(row, row+1) and col2 in range(col-1, col-18, -1):
                if self.move_west(row, col, col2) is True:
                    return True
        # Checks for stone position in E coordinate.
        if piece[5] != ' ':
            if row2 in range(row, row+1) and col2 in range(col+1, col+18):
                if self.move_east(row, col, col2) is True:
                    return True
        # Checks for stone position in SW coordinate.
        if piece[6] != ' ':
            if row2 in range(row+1, row+18) and col2 in range(col-1, col-18, -1):
                if self.move_sw(row, row2, col) is True:
                    return True
        # Checks for stone position in S coordinate.
        if piece[7] != ' ':
            if row2 in range(row+1, row+18) and col2 in range(col, col+1):
                if self.move_south(row, row2, col):
                    return True
        # Checks for stone position in SE coordinate.
        if piece[8] != ' ':
            if row2 in range(row+1, row+18) and col2 in range(col+1, col+18):
                if self.move_se(row, row2, col) is True:
                    return True
        return False

    def move_nw(self, row, row2, col):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param row2: ending row location of piece center (int)
        :param col: starting column location of piece center (int)
        :return: True if move is valid, else False
        """
        row_move = row - row2
        for i in range(row_move-1):

            # Checks NW piece positions for stones.
            if self._obj_board.get_board()[row-2-i][col-2-i] != ' ':
                return False
            # Checks N piece positions for stones.
            if self._obj_board.get_board()[row-2-i][col-1-i] != ' ':
                return False
            # Checks NE piece positions for stones.
            if self._obj_board.get_board()[row-2-i][col-i] != ' ':
                return False
            # Checks W piece positions for stones.
            if self._obj_board.get_board()[row-1-i][col-2-i] != ' ':
                return False
            # Checks SW piece positions for stones.
            if self._obj_board.get_board()[row-i][col-2-i] != ' ':
                return False
        return True

    def move_north(self, row, row2, col):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param row2: ending row location of piece center (int)
        :param col: starting column location of piece center (int)
        :return: True if move is valid, else False
        """
        for i in range(row-2, row2-1, -1):

            # Checks NW, N, and NE piece positions for stones.
            if self._obj_board.get_board()[i][col-1:col+2] != [' ', ' ', ' ']:
                return False
        return True

    def move_ne(self, row, row2, col):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param row2: ending row location of piece center (int)
        :param col: starting column location of piece center (int)
        :return: True if move is valid, else False
        """
        row_move = row - row2
        for i in range(row_move-1):

            # Checks NW piece positions for stones.
            if self._obj_board.get_board()[row-2-i][col+i] != ' ':
                return False
            # Checks N piece positions for stones.
            if self._obj_board.get_board()[row-2-i][col+1+i] != ' ':
                return False
            # Checks NE piece positions for stones.
            if self._obj_board.get_board()[row-2-i][col+2+i] != ' ':
                return False
            # Checks E piece positions for stones.
            if self._obj_board.get_board()[row-1-i][col+2+i] != ' ':
                return False
            # Checks SE piece positions for stones.
            if self._obj_board.get_board()[row-i][col+2+i] != ' ':
                return False
        return True

    def move_west(self, row, col, col2):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param col: starting column location of piece center (int)
        :param col2: ending column location of piece center (int)
        :return: True if move is valid, else False
        """
        for i in range(col-2, col2, -1):

            # Checks NW piece positions for stones.
            if self._obj_board.get_board()[row-1][i] != ' ':
                return False
            # Checks W piece positions for stones.
            if self._obj_board.get_board()[row][i] != ' ':
                return False
            # Checks SW piece positions for stones.
            if self._obj_board.get_board()[row+1][i] != ' ':
                return False
        return True

    def move_east(self, row, col, col2):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param col: starting column location of piece center (int)
        :param col2: ending column location of piece center (int)
        :return: True if move is valid, else False
        """
        for i in range(col+2, col2+1):

            # Checks NE piece positions for stones.
            if self._obj_board.get_board()[row-1][i] != ' ':
                return False
            # Checks E piece positions for stones.
            if self._obj_board.get_board()[row][i] != ' ':
                return False
            # Checks SE piece positions for stones.
            if self._obj_board.get_board()[row+1][i] != ' ':
                return False
        return True

    def move_sw(self, row, row2, col):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param row2: ending row location of piece center (int)
        :param col: starting column location of piece center (int)
        :return: True if move is valid, else False
        """
        row_move = row2 - row
        for i in range(row_move-1):

            # Checks SW piece positions for stones.
            if self._obj_board.get_board()[row+2+i][col-2-i] != ' ':
                return False
            # Checks S piece positions for stones.
            if self._obj_board.get_board()[row+2+i][col-1-i] != ' ':
                return False
            # Checks SE piece positions for stones.
            if self._obj_board.get_board()[row+2+i][col-i] != ' ':
                return False
            # Checks W piece positions for stones.
            if self._obj_board.get_board()[row+1+i][col-2-i] != ' ':
                return False
            # Checks NW piece positions for stones.
            if self._obj_board.get_board()[row+i][col-2-i] != ' ':
                return False
        return True

    def move_south(self, row, row2, col):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param row2: ending row location of piece center (int)
        :param col: starting column location of piece center (int)
        :return: True if move is valid, else False
        """
        for i in range(row+2, row2+1):

            # Checks SW, S, and SE piece positions for stones.
            if self._obj_board.get_board()[i][col-1: col+2] != [' ', ' ', ' ']:
                return False
        return True

    def move_se(self, row, row2, col):
        """
        Checks the leading edge of piece as it moves to determine if move is unobstructed.
        :param row: starting row location of piece center (int)
        :param row2: ending row location of piece center (int)
        :param col: starting column location of piece center (int)
        :return: True if move is valid, else False
        """
        row_move = row2 - row
        for i in range(row_move-1):

            # Checks NE piece positions for stones.
            if self._obj_board.get_board()[row+i][col+2+i] != ' ':
                return False
            # Checks SE piece positions for stones.
            if self._obj_board.get_board()[row+2+i][col+2+i] != ' ':
                return False
            # Checks S piece positions for stones.
            if self._obj_board.get_board()[row+2+i][col+1+i] != ' ':
                return False
            # Checks SW piece positions for stones.
            if self._obj_board.get_board()[row+2+i][col+i] != ' ':
                return False
            # Checks E piece positions for stones.
            if self._obj_board.get_board()[row+1+i][col+2+i] != ' ':
                return False
        return True

    def set_footprint(self, tup, piece):
        """
        Using tuple coordinates and piece information, updates board values.
        :param tup: (row, column) of desired piece coordinates (tuple)
        :param piece: list of board values (list of strings)
        :return: None
        """
        row, col = tup
        # Updates NW position
        self._obj_board.set_board(row-1, col-1, piece[0])
        # Updates N position
        self._obj_board.set_board(row-1, col, piece[1])
        # Updates NE position
        self._obj_board.set_board(row-1, col+1, piece[2])
        # Updates W position
        self._obj_board.set_board(row, col-1, piece[3])
        # Updates C position
        self._obj_board.set_board(row, col, piece[4])
        # Updates E position
        self._obj_board.set_board(row, col+1, piece[5])
        # Updates SW position
        self._obj_board.set_board(row+1, col-1, piece[6])
        # Updates S position
        self._obj_board.set_board(row+1, col, piece[7])
        # Updates SE position
        self._obj_board.set_board(row+1, col+1, piece[8])
        # Updates positions dictionary
        self._positions = self._obj_board.set_positions()

    def del_edges(self):
        """
        Removes any stones from the board edges.
        :return: None
        """
        # Deletes stones in the top and bottom rows.
        for n in range(20):
            self._obj_board.set_board(1, n, " ")
            self._obj_board.set_board(20, n, " ")
        # Deletes stones in the A and T columns.
        for n in range(1, 21):
            self._obj_board.set_board(n, 0, " ")
            self._obj_board.set_board(n, 19, " ")
        # Updates positions dictionary
        self._positions = self._obj_board.set_positions()


class GessBoard:
    """
    Creates the Gess game board, initializes stone positions, tracks positions, and prints the board.
    Communicates with GessGame class to enable player moves across the game board.
    """
    def __init__(self):
        """
        Initializes the game board, all 86 stone positions, alphabetizes game board
        column headers, creates a dictionary to track all game board positions.
        """
        self._board = [
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' '],
            [' ', 'B', 'B', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', ' '],
            [' ', ' ', 'B', ' ', 'B', ' ', 'B', 'B', 'B', 'B', 'B', 'B', 'B', 'B', ' ', 'B', ' ', 'B', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' ', 'B', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' ', 'W', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
            [' ', 'W', 'W', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', ' '],
            [' ', ' ', 'W', ' ', 'W', ' ', 'W', 'W', 'W', 'W', 'W', 'W', 'W', 'W', ' ', 'W', ' ', 'W', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']]
        self._column_header = [chr(x) for x in range(ord('A'), ord('U'))]
        self._alpha_num_dict = dict(zip(self._column_header, [x for x in range(0, 20)]))
        self._positions = {}

    def get_board(self):
        """
        :return: game board (list of lists)
        """
        return self._board

    def get_positions(self):
        """
        :return: self._positions (dictionary)
        """
        return self._positions

    def set_board(self, row, col, val):
        """
        Updates board positions. Row indices are 1-20, columns 0-19.
        :param row: row coordinate (int)
        :param col: column coordinate (int)
        :param val: 'B', 'W', or ' ' (string)
        :return: None
        """
        self._board[row][col] = val

    def set_positions(self):
        """
        Adds all board positions to the dictionary. Keys are labeled by alphanumeric position
        on the game board ('A2'), values are "B", "W", or " " to indicate presence of player's stones.
        :return: self._positions (dictionary)
        """
        count = -1
        # Iterates through game board rows, keeping track of row position.
        for row in self._board:
            count += 1
            for i in range(len(row)):

                # Skips row 0 to begin tracking positions at row 1.
                if count == 0:
                    continue
                else:
                    # Finds the alphabet letter corresponding to the column index.
                    for key, value in self._alpha_num_dict.items():
                        if i == value:
                            # Labels stone position: alphabet column header + row index.
                            position = key+str(count)

                            # Adds the board position to the dictionary.
                            self._positions[position] = self._board[count][value]
        return self._positions

    def print_board(self):
        """
        Uses ANSI Escape Sequences to print a colorful game board.
        :return: None
        """
        # Enables ANSI Escape Sequences to operate on Windows 10.
        # import os
        # os.system("")

        # Provides spacing for column header alignment and prints column headers.
        print("  ", end=' ')
        for i in self._column_header:
            print('\u001b[4m\u001b[1m\u001b[95m', i + ' ', end="")

        print('\033[04m\033[35m')
        for i in range(1, 21):

            # Assists with alignment for single and double digit row numbers.
            if i < 10:
                print('\u001b[4m\u001b[95m' + str(i) + '\033[35m', '', end=" ")
            else:
                print('\u001b[4m\u001b[95m' + str(i) + '\033[35m', end=" ")

            # Creates columns to complete game board.
            for j in range(20):
                if self._board[i][j] == 'B':
                    print(u'\u2502\u001b[34;1m'+self._board[i][j]+'\u001b[35m', end=' ')
                elif self._board[i][j] == 'W':
                    print(u'\u2502\u001b[30;1m'+self._board[i][j]+'\u001b[35m', end=' ')
                else:
                    print(u'\u2502' + self._board[i][j], end=' ')
            print(u'\u2502')
        print('\033[00m')

game = GessGame()
board = GessBoard()
# print(game.make_move("d7", 'c7'))
print(game.print_board())
