from const import *
from move import Move
from piece import *
from square import Square


class Board:

    def __init__(self):
        self.squares = [['0', '0', '0', '0', '0', '0', '0', '0', ] for col in range(COLS)]

        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def calc_moves(self, piece, row, col):
        """
            Calculates all the possible (valid) moves of a specific piece on a specific position
        """

        def pawn_moves():
            steps = 1 if piece.moved else 2
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for move_row in range(start, end, piece.dir):
                if Square.in_range(move_row):
                    if self.squares[move_row][col].empty():
                        initial = Square(row, col)
                        final = Square(move_row, col)
                        move = Move(initial, final)
                        piece.add_move(move)
                    else:
                        break
                else:
                    break
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def knight_moves():
            possible_moves = [
                (row - 2, col + 1),
                (row - 1, col + 2),
                (row + 1, col + 2),
                (row + 2, col + 1),
                (row + 2, col - 1),
                (row + 1, col - 2),
                (row - 1, col - 2),
                (row - 2, col - 1),
            ]

            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].empty_or_enemy(piece.color):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        piece.add_move(move)

        def straighline_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        move = Move(initial, final)
                        # Empty Square
                        if self.squares[possible_move_row][possible_move_col].empty():
                            piece.add_move(move)
                        # Enemy Piece
                        if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            piece.add_move(move)
                            break
                        # Team Piece
                        if self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    else:
                        break

                    # Incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr

        if isinstance(piece, Pawn):
            pawn_moves()

        elif isinstance(piece, Knight):
            knight_moves()

        elif isinstance(piece, Bishop):
            straighline_moves([
                (-1, 1),   # up right
                (-1, -1),  # up left
                (1, 1),    # down right
                (1, -1),   # down left
            ])

        elif isinstance(piece, Rook):
            straighline_moves([
                (-1, 0),  # up
                (1, 0),   # down
                (0, 1),   # left
                (0, -1),  # right
            ])

        elif isinstance(piece, Queen):
            straighline_moves([
                (-1, 1),   # up right
                (-1, -1),  # up left
                (1, 1),    # down right
                (1, -1),   # down left
                (-1, 0),   # up
                (1, 0),    # down
                (0, 1),    # left
                (0, -1),   # right
            ])

        elif isinstance(piece, King):
            pass

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # Pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # Knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # Bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # Rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        self.squares[4][4] = Square(4, 4, Rook(color))

        # Queens
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        self.squares[3][3] = Square(3, 3, Queen(color))

        # Kings
        self.squares[row_other][4] = Square(row_other, 4, King(color))
