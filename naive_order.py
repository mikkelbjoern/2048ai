from game import *

def run():
    """
    Will simulate a game where the moves are chosen in a preference order as follows:
        UP, LEFT, RIGHT, DOWN
    The score after the game is lost will be returned.
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
            if UP in actions:
                game.up()
            elif LEFT in actions:
                game.left()
            elif RIGHT in actions:
                game.right()
            elif DOWN in actions:
                game.down()
    
