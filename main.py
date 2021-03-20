import expectimax
import naive_order
import random_ai
import sys
from game import Game, UP, DOWN, LEFT, RIGHT

if __name__ == "__main__":
    try:
        argument = sys.argv[1]
    except IndexError:
        argument = ""

    if argument.lower() == "expectimax":
        score = expectimax.run()
        print(f"The final sum on the board was: {score}")
    elif argument.lower() == "random":
        score = random_ai.run()
        print(f"The final sum on the board was: {score}")
    elif argument.lower() == "naive_order":
        score = naive_order.run()
        print(f"The final sum on the board was: {score}")
    elif argument.lower() == "play":
        game = Game()
        while True:
            print(game)
            allowed_moves = game.possible_moves()
            print(allowed_moves)
            action = input(" > ")
            if allowed_moves == []:
                print(f"Game over! You got: {game.score()} points.")
                quit()
            elif action.lower() in allowed_moves:
                if action.lower() == UP:
                    game.up()
                elif action.lower() == DOWN:
                    game.down()
                elif action.lower() == LEFT:
                    game.left()
                elif action.lower() == RIGHT:
                    game.right()
            else:
                print(f" > '{action}' was not recognized as a legal move")
    else: # Displayu a help message if no valid command was given
        print("""
        Run by using `python3 main.py ARG` where ARG is one of the following
            * expectimax - run the expectimax
            * random - play using a completely random ai
            * naive_order - play with a simple ai using a prioritized preference for each move
            * play - To play a game yourself
        """.strip())
