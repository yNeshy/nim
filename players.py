from iplayer import IPlayer
import time

class Human(IPlayer):
    def __init__(self, name):
        self.name = name
        self.number_moves = 0

    def move(self, board):
        if(self.is_final(board)):
            return None, None
       
        # Cute input form:
        for pile in board:
            print('-', end="-")
        print()
        for pile in board:
            print(pile, end=" ")
        print()
        
        # Index of pile to treat
        unvalid = True
        while(unvalid):
            index = int(input("Choissez une pile à dépiler: "))
            unvalid = (index < 0) | (index > len(board)+1) | (board[index] <= 2)

        # Choose number of coins to pop
        unvalid = True
        while(unvalid):
            amount = int(input("Nombre de jetons à depiler: "))
            unvalid = (amount < 1) | (amount > board[index]-1 ) | ( board[index] == amount*2 )
        print("\n")
        self.number_moves += 1
        return index, amount

    def info(self):
        return self.name+":\nMoved: "+str(self.number_moves)+" times."



# Question 1
class Minimax(IPlayer):
    def __init__(self):
        self.name = "Minimax"
        self.visited_nodes = 0
        self.time_total = .0

    def rewind_move(self, before, after):
        """
        find the move that led to the current state.
        """
        if(len(before) != len(after)-1):
            return None, None

        for i in range(len(before)):
            if(after[i] != before[i]):
                return i, before[i] - after[i]
        return None, None                

    def move(self, board):
        start = time.time()
        result = self.rewind_move(board, self.simulate(board, True)[1][1] )
        self.time_total += time.time() - start
        return result

    def valid_moves(self, pile):
        return [_ for _ in range(1, int(pile/2) +1) if(_*2 != pile) ]

    def simuate_develop(self, board, index, amount):
        if(index >= len(board)):
            print("Invalid")
            return None
        result = []
        amount = int(amount)
        if( (board[index] < amount) | (board[index] < 3) ):
            print("Not allowed: Cannot take {} from {}".format(amount, board[index]))
            return None
        
        for i in range(0,index):
            result.append(board[i])
        
        result.append(int(board[index])-amount)
        result.append(amount)
        
        for i in range(index+1, len(board)):
            result.append(board[i])
        
        return result

    def next_boards(self, board):
        result = []
        for i in range(len(board)):
            pile = board[i]
            for move in self.valid_moves(pile):
                result.append(self.simuate_develop(board, i, move))

        return result
            
    def build_graph(self, board):
        visited = set()
        res = []
        
        for i in range(len(board)):
            for m in range(1, board[i] + 1):
                temp = list(board[:])
                temp[i] -= m
                
                # check if the stage already exists
                rearranged = tuple(sorted(temp))
                if rearranged not in visited:
                    res.append(temp)
                    visited.add(rearranged)
        
        return res   
    
    def simulate(self, board, maxTurn):
        # determining final board
        if (self.is_final(board) and maxTurn) : return (-1, [board])
        if (self.is_final(board) and not maxTurn) : return (1, [board])
        
        if maxTurn:
            res_max = -float('inf')
            res = None
            for i in self.next_boards(board):
                # Question 3
                self.visited_nodes += 1
                # recursively search for the next possible move
                val, temp = self.simulate(i, not maxTurn)
                if val > res_max:
                    res_max = val
                    res = temp
                
            return res_max, [board] + res
        else:
            res_min = float('inf')
            res = None
            for i in self.next_boards(board):
                # Question 3
                self.visited_nodes += 1
                val, temp = self.simulate(i, not maxTurn)
                if val < res_min:
                    res_min = val
                    res = temp
            return res_min, [board] + res

    def info(self):
        return "{}:\n Nodes visited: {}\nTime elapsed: {:.2f}s".format(self.name, self.visited_nodes, self.time_total)

# Question 2
class MinimaxAlphaBeta(Minimax):
    def __init__(self):
        self.name = "Minimax αβ"
        self.visited_nodes = 0
        self.time_total = .0

    def move(self, board):
        start = time.time()
        result = self.rewind_move(board, self.simulate(board, -float('inf'), float('inf'), True)[1][1] )
        self.time_total += time.time() - start
        return result

    def simulate(self, board, alpha, beta, maxTurn):
        # determining final board
        if (self.is_final(board) and maxTurn) : return (-1, [board])
        if (self.is_final(board) and not maxTurn) : return (1, [board])
        
        if maxTurn:
            res_max = -float('inf')
            res = None
            for i in self.next_boards(board):
                # Question 3
                self.visited_nodes += 1
                # recursively search for the next possible move
                val, temp = self.simulate(i, alpha, beta, not maxTurn)
                if val > res_max:
                    res_max = val
                    res = temp
                # update the upper bound
                alpha = max(alpha, val)
                # pruning
                if alpha >= beta:
                    break
            return res_max, [board] + res
        else:
            res_min = float('inf')
            res = None
            for i in self.next_boards(board):
                # Question 3
                self.visited_nodes += 1
                val, temp = self.simulate(i, alpha, beta, not maxTurn)
                if val < res_min:
                    res_min = val
                    res = temp
                
                beta = min(beta, val)
                if alpha >= beta:
                    break
            return res_min, [board] + res


if __name__ == "__main__":
    m = MinimaxAlphaBeta()

    BOARD = [1, 9, 1, 8]
    print(m.move(BOARD))