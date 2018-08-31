
import random

class Random:

    def __init__(self, player):
        self.set_player(player)
        self.all_moves = [(row,col) for col in range(3) for row in range(3)]


    def set_player(self, player):
        self.player = player


    def get_move(self, board):
        """Get a random possible move.
        Implement as fast as possible.
        """
        random.shuffle(self.all_moves)
        for row,col in self.all_moves:
            if board.board[row,col]==0:
                break
        return (row,col)
