from game import Game
from numba import njit 
import numba
from numba import int64
import numpy as np

# Enums to represent a move in either direction.
# Using ints seems easier for the jit
UP, DOWN, LEFT, RIGHT  = "UP", "DOWN", "LEFT", "RIGHT"
IMPOSSIBLE_MOVE = "IMPOSSIBLE_MOVE"

EMPTY_FIELD = 0

# Setting fastmath=True will allow less precise calculation, but improve performance
# Since the heuristic is in essence not precise, this should not matter much and
# being able to go steps deeper (which comes with better performance) seems like
# a good tradeoff.
@njit(fastmath=True, cache=True)
def h(game_state):
    weights = [
      [15, 14, 13, 12], 
      [8, 9, 10, 11], 
      [7, 6, 5, 4], 
      [0, 1, 2, 3]
    ]

    score = 0
    for i in range(4):
        for j in range(4):
            if not game_state[i][j] == EMPTY_FIELD:
                score += 2**weights[i][j] * game_state[i][j]
            else:
                score += 2**(15-weights[i][j])

    penalty = 0
    for i in range(4):
        for j in range(4):
            if not game_state[i][j] == EMPTY_FIELD: 
                if i == 0:
                    if game_state[i+1][j] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i+1][j])
                    if j != 3 and game_state[i][j+1]!= EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i][j+1])
                    if j != 0 and game_state[i][j-1]:
                        penalty += abs(game_state[i][j] - game_state[i][j-1])
                elif i == 3: 
                    if game_state[i-1][j] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i-1][j])
                    if j != 3 and game_state[i][j+1] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i][j+1])
                    if j != 0 and game_state[i][j-1] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i][j-1])
                else:
                    if game_state[i+1][j] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i+1][j])
                    if game_state[i-1][j] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i-1][j])
                    if j != 3 and game_state[i][j+1] != EMPTY_FIELD: 
                        penalty += abs(game_state[i][j] - game_state[i][j+1])
                    if j != 0 and game_state[i][j-1] != EMPTY_FIELD:
                        penalty += abs(game_state[i][j] - game_state[i][j-1])
    score -= penalty*0.1
    return score


# Counting down the depth instead of up, makes caching better 
@njit(cache=True)
def h_min_max(game_state, depth=5):
    possible_moves_to_make = possible_moves(game_state)
    if len(possible_moves_to_make) == 0:
        return IMPOSSIBLE_MOVE, h(game_state) 

    if depth <= 0:
        return IMPOSSIBLE_MOVE, h(game_state) 

    down_score = 0
    up_score = 0
    left_score = 0
    right_score = 0

    for move in possible_moves_to_make:
        if move == UP:
            moved_game_state = moved_up(game_state)
        elif move == DOWN:
            moved_game_state = moved_down(game_state)
        elif move == LEFT:
            moved_game_state = moved_left(game_state)
        else:
            moved_game_state = moved_right(game_state)

        empty_fields = find_empty_fields(moved_game_state)
        depth_increase = 1 if len(empty_fields) < 6 else 2

        
        new_game = moved_game_state.copy() 
        if len(empty_fields) == 0:
            expected_score = h_min_max(new_game, depth=depth - depth_increase)[1]
            if move == DOWN:
                down_score += expected_score
            elif move == UP:
                up_score += expected_score
            elif move == LEFT:
                left_score += expected_score
            else:
                right_score += expected_score

        else:
            for (col, row) in empty_fields:
                new_game[col, row] = 2
                expected_score =  h_min_max(new_game, depth=depth - depth_increase)[1]
                if move == DOWN:
                    down_score += expected_score / len(empty_fields)
                elif move == UP:
                    up_score += expected_score / len(empty_fields)
                elif move == LEFT:
                    left_score += expected_score / len(empty_fields)
                else:
                    right_score += expected_score / len(empty_fields) 


    max_score = max(up_score, left_score, down_score, right_score)
    if max_score <= up_score:
        return UP, up_score
    elif max_score <= down_score:
        return DOWN, down_score
    elif max_score <= left_score:
        return LEFT, left_score
    else:
        return RIGHT, right_score

def run():
    """
    Will simulate a game using the heristic h in expectimax 
    The score is returned when the game is lost.
    """
    game = Game()
    i = 0
    while True:
        print(i, "\n\n" + str(game))
        i += 1
        actions = game.possible_moves()
        if actions == []:
            return game.score()
        else:
            game_state = replace_none(np.array(game.state))
            action = h_min_max(game_state)[0]
            if action == UP:
                game.up()
            elif action == DOWN:
                game.down()
            elif action== LEFT:
                game.left()
            elif action== RIGHT:
                game.right()
            else:
                print("Didn't move")
    return game

def replace_none(game_state):
    game_state_copy = game_state.copy()
    m, n = game_state.shape
    for j in range(m):
        for i in range(n):
            if game_state[j][i] == None:
                game_state_copy[j][i] = EMPTY_FIELD
    return np.array(game_state_copy, dtype=np.dtype("int64"))

@njit(cache=True)
def find_empty_fields(game_state):
    empty_fields = []
    m, n = game_state.shape
    for i in range(m):
        for j in range(n):
            if game_state[i][j] == EMPTY_FIELD:
                empty_fields.append((i,j))
    return empty_fields

@njit(cache=True)
def moved_up(game_state):
    new_board = game_state.copy() 
    for i in range(4):
        col = new_board[:, i] 
        col = jitted_fold_list(col)
        col = np.append(col, np.array([EMPTY_FIELD] * (4 - len(col))), 0 )
        new_board[:, i] = col 
    return new_board

@njit(cache=True)
def moved_left(game_state):
    new_board = game_state.copy()
    for i in range(4):
        col = new_board[i, :]
        col = jitted_fold_list(col)
        col = np.append(col, np.array([EMPTY_FIELD] * (4 - len(col))), 0 )
        new_board[i, :] = col 
    return new_board


@njit(cache=True)
def moved_down(game_state):
    # Flip board upside down, move up, flip the board back
    return np.flipud(moved_up(np.flipud(game_state)))

@njit(cache=True)
def moved_right(game_state):
    # Mirror board vertically, move left, mirror back
    return np.fliplr(moved_left(np.fliplr(game_state)))

@njit(cache=True)
def possible_moves(game_state):
    moves = []
    if not (moved_left(game_state) == game_state).all():
        moves.append(LEFT)
    if not (moved_right(game_state) == game_state).all():
        moves.append(RIGHT)
    if not (moved_down(game_state) == game_state).all():
        moves.append(DOWN)
    if not (moved_up(game_state) == game_state).all():
        moves.append(UP)
    return moves

@njit(cache=True)
def jitted_fold_list(l):
    """
    Determines what happens when a column or a row is _compressed_. 
    This might be able to be done by using some sort fo recursion, but since the amount of cases
    are quite short, then we simply consider all options by themselves.

    The function returns a list of the not-EMPTY_FIELD values from the list. 
    Examples:
    ```python
    fold_4_list([1,1,EMPTY_FIELD,EMPTY_FIELD]) == [2]
    fold_4_list([1,EMPTY_FIELD,1,EMPTY_FIELD]) == [2]
    fold_4_list([1,EMPTY_FIELD,2,EMPTY_FIELD]) == [1, 2]
    fold_4_list([1,1,2,2]) == [2, 4]
    fold_4_list([2,2,2,2]) == [4, 4]
    fold_4_list([EMPTY_FIELD, EMPTY_FIELD, EMPTY_FIELD, EMPTY_FIELD]) == []
    ```
    """
    # All EMPTY_FIELD values are redundant for the problem and are therefore ignored
    values = l[l != EMPTY_FIELD] 
    if len(values) == 0:
        return values
    elif len(values) == 1:
        return values
    elif len(values) == 2:
        x, y = values
        if x == y:
            return np.array([2 * x])
        else:
            return np.array([x, y])
    elif len(values) == 3:
        v1, v2, v3 = values
        if v1 == v2:
            return np.array([2 * v1, v3])
        elif v2 == v3:
            return np.array([v1, 2 * v2])
        else:
            return values
    elif len(values) == 4:
        v1, v2, v3, v4 = values
        if v1 == v2:
            if v3 == v4:
                return np.array([2 * v1, 2 * v3])
            else:
                return np.array([2 * v1, v3, v4])
        elif v2 == v3:
            return np.array([v1, 2 * v2, v4])
        elif v3 == v4:
            return np.array([v1, v2, 2 * v3])
        else:
            return values
    else:
        return values

#@numba.cfunc("int64[:](int64[:])")
def fold_4_list(l):
    """
    Determines what happens when a column or a row is _compressed_. 
    This might be able to be done by using some sort fo recursion, but since the amount of cases
    are quite short, then we simply consider all options by themselves.

    The function returns a list of the not-EMPTY_FIELD values from the list. 
    Examples:
    ```python
    fold_4_list([1,1,EMPTY_FIELD,EMPTY_FIELD]) == [2]
    fold_4_list([1,EMPTY_FIELD,1,EMPTY_FIELD]) == [2]
    fold_4_list([1,EMPTY_FIELD,2,EMPTY_FIELD]) == [1, 2]
    fold_4_list([1,1,2,2]) == [2, 4]
    fold_4_list([2,2,2,2]) == [4, 4]
    fold_4_list([EMPTY_FIELD, EMPTY_FIELD, EMPTY_FIELD, EMPTY_FIELD]) == []
    ```
    """
    # All EMPTY_FIELD values are redundant for the problem and are therefore ignored
    values = l[l != EMPTY_FIELD] 
    if len(values) == 0:
        return values
    elif len(values) == 1:
        return values
    elif len(values) == 2:
        x, y = values
        if x == y:
            return np.array([2 * x])
        else:
            return np.array([x, y])
    elif len(values) == 3:
        v1, v2, v3 = values
        if v1 == v2:
            return np.array([2 * v1, v3])
        elif v2 == v3:
            return np.array([v1, 2 * v2])
        else:
            return values
    elif len(values) == 4:
        v1, v2, v3, v4 = values
        if v1 == v2:
            if v3 == v4:
                return np.array([2 * v1, 2 * v3])
            else:
                return np.array([2 * v1, v3, v4])
        elif v2 == v3:
            return np.array([v1, 2 * v2, v4])
        elif v3 == v4:
            return np.array([v1, v2, 2 * v3])
        else:
            return values
    else:
        return values


if __name__ == "__main__":
    game_state = np.array(
        [[2]*3 + 1*[EMPTY_FIELD], 
        [2]+ [EMPTY_FIELD]*3, 
        [EMPTY_FIELD]*4, 
        [EMPTY_FIELD]*4] )
    game_state = np.array(
        [ [64, 2, 32, EMPTY_FIELD],
          [2, 16, 4, 2],
          [256, 64, 32, 8],
          [2, 16, 8, 2]
        ]
    )
    print(game_state)
    print("Possible Moves: ", possible_moves(game_state))
    print(h_min_max(game_state))
    print(jitted_fold_list(np.array(game_state[1,:])))
    print(jitted_fold_list(np.array([EMPTY_FIELD, 2, 2, EMPTY_FIELD])))

    game_state = np.array(
        [[2]*3 + 1*[EMPTY_FIELD], 
        [2]+ [EMPTY_FIELD]*3, 
        [EMPTY_FIELD]*4, 
        [EMPTY_FIELD]*4] )
    print(game_state)
    print(jitted_moved_left(game_state))