# 2048 - Game and expectimax AI
This is a university project done in March 2021.

## Installation
To setup the project use 

### Without nix
```bash
pip install requirements.txt
```

### With nix
```bash
nix-shell
```

## Running
To run the program do
```bash
python3 main.py ARG
```
Where the `ARG` can be either of the following:
 * `expectimax` - run the expectimax ai
 * `random` - play using a completely random "ai"
 * `naive_order` - play with a simple ai using a prioritized preference for each move
 * `play` - To play a game yourself
