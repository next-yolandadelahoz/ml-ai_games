
import numpy as np


class Minimax:
    """
    TODO: review algorithm
    Note, loses with: 7,5,3,9 (wrong), 1,8, 2
    """

    """ Heuristic Scoring
    Number of possible wins (lines) available per position
    """
    H = [
        [3,2,3],
        [2,4,2],
        [3,2,3]
    ]

    def __init__(self, player, human=False):
        """
        human: bool
            Flag to decide probabilistically from actions based on their score.
            Be a vulnerable player.
        """
        self.player = player
        self.opponent = 2 if player==1 else 1
        self.human = human


    def _score_board(self, board, player):
        score = 0
        if board.is_winner(player):
            score  = 100
        else:
            for row in board.vals:
                for col in board.vals:
                    if board.board[row, col]==player:
                        score += self.H[row][col]
        return score


    def get_move(self, board):
        """Perform a move based on a minimax strategy.

        TODO: if some actions are equally scored, choose randomly one
        TODO:
        """
        # 'p'layer moves
        p_cands = [
            (self._score_board(p_board, self.player), p_move, p_board)
            for p_move, p_board in board.get_candidates(self.player)
        ]
        # 'o'pponent moves
        o_cands = []
        for p_score, p_move, p_board in p_cands:
            o_moves = p_board.get_candidates(self.opponent)
            if o_moves:
                o_cands.append((
                    p_score - 0.9*max([  # Short time actions are (a bit) more important, force the agent to win
                        self._score_board(o_board, self.opponent)
                        for _, o_board in o_moves
                    ]),
                    p_move
                ))
            else:  # Case 1 move left
                o_cands.append((p_score, p_move))
        if self.human==True:
            scores = np.array([s for s,_ in o_cands], dtype=np.float)
            scores += abs(scores.min())+0.1  # No 0 probabilities
            scores /= scores.sum()  # Normalize to probabilities
            o_cand = o_cands[ np.random.choice(len(o_cands), 1, p=scores) ]
        else:
            o_cand = max(o_cands)
        return o_cand[1]  # Return the best move
