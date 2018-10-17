
import pickle
import random


class IRLFinite:

    R = None  # Rewards. dict(state)-> value

    def __init__(self, player, Rfile):
        self.set_player(player)
        with open("rewards.pickle", "rb") as fd:
            self.R = pickle.load( fd )


    def set_player(self, player):
        self.player = player


    def get_move(self, board):
        """
        PARAMETERS
        board: Board
          Current game state.

        RETURNS
        retval: (int,int)
            Action to take (row, col).
        """
        # Generate candidates [(action, next state)]
        actions = []
        for action, board in board.get_candidates(self.player):
            if board.get_state() in self.R:
                return action
            else:
                actions.append(action)
        # No action leads to a reward, return randomly
        return random.choice(actions)
