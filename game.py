import os

class Game:
    def __init__(self, pile):
        self.board = pile
        self.history = [pile]

    def develop(self, index, amount):
        if(index >= len(self.board)):
            print("Invalid")
            return None

        result = []
        amount = int(amount)
        if( (self.board[index] < amount) | (self.board[index] < 3) ):
            print("Not allowed: Cannot take {} from {}".format(amount, self.board[index]))
            return None
        
        for i in range(0,index):
            result.append(self.board[i])
        
        result.append(int(self.board[index])-amount)
        result.append(amount)
        
        for i in range(index+1, len(self.board)):
            result.append(self.board[i])
        
        self.history.append(result)
        self.board = result
        return result

    def is_over(self):
        for pile in self.board:
            if(pile > 2):
                return False
        return True

    def play(self, player1, player2, clean=False):
        players = [player1, player2]
        turn = -1
        while(not self.is_over()):
            if(clean) : self.clear()
            turn += 1
            turn %= 2
            print(players[turn].name+"'s turn:")
            i, a = players[turn].move(self.board)
            print(players[turn].name + " takes {} from index {} ".format(a, i))
            self.develop(i, a)
            self.draw()
            
        print(players[turn].name+" wins.")


    def draw(self):
        for ele in self.board :
            print("| {} |".format(ele))
        
    def clear(self):
        # for mac and linux(here, os.name is 'posix')
        if os.name == 'posix':
            _ = os.system('clear')
        else:
            # for windows platfrom
            _ = os.system('cls')

def line():
    for _ in range(10): print("_", end="_")
    print()

if __name__ == "__main__":
    import players
    
    game = Game([3, 5, 3])
    player1 = players.MinimaxAlphaBeta()
    player2 = players.Human("Yu")
    
    game.play(player1, player2 )

    line()
    print("Informations about the players: ")
    line()
    print(player1.info()  )
    line()
    print(player2.info())
    line()