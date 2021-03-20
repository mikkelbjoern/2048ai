import copy
import random
from random import randint


def fold_4_list(l):
    """
    Determines what happens when a column or a row is _compressed_. 
    This might be able to be done by using some sort fo recursion, but since the amount of cases
    are quite short, then we simply consider all options by themselves.

    The function returns a list of the not-None values from the list. 
    Examples:
    ```python
    fold_4_list([1,1,None,None]) == [2]
    fold_4_list([1,None,1,None]) == [2]
    fold_4_list([1,None,2,None]) == [1, 2]
    fold_4_list([1,1,2,2]) == [2, 4]
    fold_4_list([2,2,2,2]) == [4, 4]
    fold_4_list([None, None, None, None]) == []
    ```
    """
    # All None values are redundant for the problem and are therefore ignored
    values = [x for x in l if x is not None]
    if len(values) == 0:
        return values
    elif len(values) == 1:
        return values
    elif len(values) == 2:
        x, y = values
        if x == y:
            return [2 * x]
        else:
            return [x, y]
    elif len(values) == 3:
        v1, v2, v3 = values
        if v1 == v2:
            return [2 * v1, v3]
        elif v2 == v3:
            return [v1, 2 * v2]
        else:
            return values
    elif len(values) == 4:
        v1, v2, v3, v4 = values
        if v1 == v2:
            if v3 == v4:
                return [2 * v1, 2 * v3]
            else:
                return [2 * v1, v3, v4]
        elif v2 == v3:
            return [v1, 2 * v2, v4]
        elif v3 == v4:
            return [v1, v2, 2 * v3]
        else:
            return values
    else:
        raise Exception(f"Tried to fold list \"{l}\ which is too long")


LEFT = "l"
RIGHT = "r"
UP = "u"
DOWN = "d"


class Game:
    def __init__(self, game_state=None):
        if game_state is None:
            init_board = [[None for _ in range(4)] for _ in range(4)]
            self.state = init_board
            self.__fill_random_field()
            self.__fill_random_field()
        if not game_state is None:
            self.state = game_state

    def __eq__(self, other):
        return self.state == other.state

    def copy(self):
        state = copy.deepcopy(self.state)
        return Game(state)

    def __right(self):
        """
        Returns what state the game would be in if moved right BEFORE placing a new random field.
        """
        new_board = self.copy()
        for i in range(4):
            row = self.__get_row(i)

            row.reverse()
            row = fold_4_list(row)
            row = row + [None] * (4 - len(row))
            row.reverse()

            new_board.__set_row(i, row)
        return new_board.state

    def __down(self):
        """
        Returns what state the game would be in if moved down BEFORE placing a new random field.
        """
        new_board = self.copy()
        for i in range(4):
            col = self.__get_column(i)

            col.reverse()
            col = fold_4_list(col)
            col = col + [None] * (4 - len(col))
            col.reverse()

            new_board.__set_column(i, col)
        return new_board.state

    def __up(self):
        """
        Returns what state the game would be in if moved up BEFORE placing a new random field.
        """
        new_board = self.copy()
        for i in range(4):
            col = self.__get_column(i)
            col = fold_4_list(col)
            col = col + [None] * (4 - len(col))
            new_board.__set_column(i, col)
        return new_board.state

    def __left(self):
        """
        Returns what state the game would be in if moved left BEFORE placing a new random field.
        """
        new_board = self.copy()
        for i in range(4):
            row = self.__get_row(i)
            row = fold_4_list(row)
            row = row + [None] * (4 - len(row))
            new_board.__set_row(i, row)
        return new_board.state

    def left(self):
        """
        Will peform a move to the left (if possible).
        """
        if LEFT in self.possible_moves():
            self.state = self.__left()
            self.__fill_random_field()

    def right(self):
        """
        Will peform a move to the right (if possible).
        """
        if RIGHT in self.possible_moves():
            self.state = self.__right()
            self.__fill_random_field()

    def up(self):
        """
        Will peform a move up (if possible).
        """
        if UP in self.possible_moves():
            self.state = self.__up()
            self.__fill_random_field()

    def down(self):
        """
        Will peform a move down (if possible).
        """
        if DOWN in self.possible_moves():
            self.state = self.__down()
            self.__fill_random_field()

    def possible_moves(self):
        """
        Returns the moves that are allowed with the current board.
        """
        moves = []
        if not self.__up() == self.state:
            moves.append(UP)
        if not self.__down() == self.state:
            moves.append(DOWN)
        if not self.__left() == self.state:
            moves.append(LEFT)
        if not self.__right() == self.state:
            moves.append(RIGHT)
        return moves

    def score(self):
        """
        Calculates the current score of the game.
        This is simply the sum over all the values on the board.
        """
        s = 0
        for v in self.state:
            for w in v:
                if w != None:
                    s += w
        return s

    def __get_column(self, i):
        """
        Will extract a copy of column i from the game state
        """
        return [row[i] for row in self.state]

    def __get_row(self, i):
        """
        Will extract a copy of row i from the game state
        """
        return self.state[i].copy()

    def __set_column(self, i, value):
        """
        Will modify column i to be the provided value, if too short then None are added onto the end, until reaching a length of 4.
        """
        if len(value) > 4:
            raise Exception(
                f"Tried to put more values into column {i} than what fits ({value})"
            )
        else:
            new_col = value + [None] * (4 - len(value))
            for col_index in range(4):
                self.state[col_index][i] = new_col[col_index]

    def __set_row(self, i, value):
        """
        Will modify row i to be the provided value, if too short then None are added onto the end until reaching a length of 4.
        """
        if len(value) > 4:
            raise Exception(
                f"Tried to put more values into row {i} than what fits ({value})"
            )
        else:
            new_row = value + [None] * (4 - len(value))
            self.state[i] = new_row
            return new_row

    def __fill_random_field(self):
        """
        Will fill a random empty field on the board with a 2-tile.
        """
        value = random.choice([2]*9 + [4]) # Get a 4 with a 10% chance
        empty_fields = fields = self.__empty_fields()
        if not empty_fields == []:
            col, row = random.choice(empty_fields)
            self.state[col][row] = value

    def __empty_fields(self):
        """
        Returns all coordinates (0-indexed) in which there is currently no tile
        """
        return [(col, row) for row in range(4) for col in range(4)
                if self.state[col][row] == None]

    def __repr__(self):
        show_field = lambda field: "-" if field == None else str(field)
        out = ""
        for row in self.state:
            out += "\t".join([show_field(f) for f in row])
            out += "\n"
        return out

    def __hash__(self):
        s = ""
        for v in self.state:
            s += "|{}|".format(v)
        return hash(s)