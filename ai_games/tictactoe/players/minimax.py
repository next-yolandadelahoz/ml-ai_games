
import functools
import random

import numpy as np


class Minimax:

    INFINITE = 1000000

    def __init__(self, player):
        self.set_player(player)


    def set_player(self, player):
        self.player = player
        self.opponent = 2 if player==1 else 1


    def _max_score(self, board, alpha, beta):
        """Agent moves, pick best action.
        """
        if board.is_winner(self.opponent):  # Terminal: opponent wins
            score = -1
        elif board.is_finished():  # Terminal: it's a draw
            score = 0
        else: # Non terminal
            score = -self.INFINITE
            for _, new_board in board.get_candidates(self.player):
                cand_score = self._min_score(new_board, alpha, beta)
                score = cand_score if cand_score>score else score # pick Max
                if score>=beta:  # Prune branch
                    break
                alpha = score if score>alpha else alpha
        return score


    def _min_score(self, board, alpha, beta):
        """Opponent moves, pick best action.

        RETURN
        score: number
            Minimum score for that board
        """
        # Terminal position, player made the last move
        if board.is_winner(self.player):  # Terminal: player wins
            score = 1
        elif board.is_finished():  # Terminal: it's a draw
            score = 0
        else:
            score = self.INFINITE
            for _, new_board in board.get_candidates(self.opponent):
                cand_score = self._max_score(new_board, alpha, beta)
                score = cand_score if cand_score<score else score # pick Min
                if score<=alpha: # Prune branch
                    break
                beta = score if score<beta else beta
        return score


    def get_move(self, board):
        """Perform a move based on a minimax strategy with alpha-beta prunning.
        """
        if np.all(board.board==0):  # Speedup: first move is random, same scoring.
            move = (random.randint(0,2), random.randint(0,2))
        else:
            candidates = ([
                (self._min_score(new_board, -self.INFINITE, self.INFINITE), move)
                for move, new_board
                in board.get_candidates(self.player)
            ])
            random.shuffle(candidates)  # Pick random from same max values.
            move = max(candidates, key=lambda x:x[0])[1]
        return move
