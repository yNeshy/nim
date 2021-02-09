from copy import copy 

class IPlayer :
    def __init__(self):
        self.name = "Unnamed algorithm"

    def move(self, board) -> tuple:
        pass
        

    def is_final(self, board):
        for pile in board:
            if(pile > 2):
                return False
        return True

    def is_valid(self, board, index, amount):
        return not ( (amount < 1) | (amount > board[index]-1 ) | ( board[index] == amount*2 ) | (index < 0) | (index > len(board)+1) | (board[index] <= 2) )

    def info(self):
        pass
