
import random

class Random:

    def __init__(self, player):
        self.set_player(player)


    def set_player(self, player):
        self.player = player

    
    def get_move(self, board):
        return random.choice(board.get_candidates(self.player))[0]
