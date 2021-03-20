import random
from game import *

def run():
    """
    Will simulate a game where the moves are chosen completely at random from the possible moves.
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
            action = random.choice(actions)
            if action.lower() == UP:
                game.up()
            elif action.lower() == DOWN:
                game.down()
            elif action.lower() == LEFT:
                game.left()
            elif action.lower() == RIGHT:
                game.right()
        