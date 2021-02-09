from game import Game
import players

def main():
    # input board
    board = [1, 7, 5]
    game = Game(board)
    game.play(players.human("Yu"), players.human("Long") )
    print(game.history)