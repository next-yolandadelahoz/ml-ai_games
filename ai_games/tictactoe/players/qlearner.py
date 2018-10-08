
from collections import defaultdict
import random

import numpy as np


class QLearner:

    Q = None  # This is Q(state,action) -> score. Implemented as a dict

    def __init__(self, player, Qfile=None):
        self.set_player(player)
        if Qfile!=None:
            # TODO: load from file ¿use pickle?
            pass
        else:
            # Q[state = hash(board)][action = (x,y)]
            self.Q = defaultdict(lambda : defaultdict(lambda : 0.0))


    def set_player(self, player):
        self.player = player


    def get_move(self, board, p=False):
        """
        PARAMETERS
        board: Board
          Current game state.
        p: bool
          If True, the next will be randomly sampled from Q values.
          If False, choose randomly from the best Q values (if several).

        RETURNS
        retval: (int,int)
            Action to take (row, col).
        """
        state = board.get_state()  # Must be hasheable
        candidates = list(self.Q[state].items())  # [(action,value)]
        # print(candidates)
        if candidates == []:  # Generate candidates, any possible move is OK
            candidates = [
                action
                for action,_
                in board.get_candidates(self.player)
            ]
            # Initialize candidates in Q so they apear in next iterations
            for action in candidates:
                self.Q[state][action] = 0
        elif p==True:  # Sample from Q values
            actions, values = zip(*candidates)
            probs = np.exp(np.array(values)*5)  # No 0 probs, scaling *5
            probs /= probs.sum()  # Probs vector sum 1
            candidate_i = np.random.choice(len(actions), size=1, p=probs)[0]
            candidates = [actions[candidate_i]]
        else:  # Pick randomly from best moves
            max_score = max(candidates, key=lambda x: x[1])[1]
            candidates = [
                action
                for action, score
                in candidates
                if score==max_score
            ]
        return random.choice(candidates)  # Return action



    def _update_Q(self, state, action, reward, lr, df):
        """Update the Q function

        RETURN:
        retval: float
            Change in the Q value for the (state, action).
        """
        old_Q = self.Q[state][action]
        self.Q[state][action] = (
            (1-lr) * self.Q[state][action] +  # exploitation
            lr * (reward + df * max(self.Q[state].values()))  # exploration
        )
        return old_Q - self.Q[state][action]


    def _train_1_game(self, lr, f_df, board, opponent):
        """Update the Q function from the result of 1 played game.
        It is always QLearner turn.

        PARAMETERS
        lr: float
            Learning rate
            Range: [0 (exploitation, no learn), 1 (exploration)]
        f_df: lambda float: float
            Function (int: depth) -> float: df.
            depth: how far is the move to the end of the game (1).
                Range. [1 (last move of the game), 9 (first move if all the board is populated)]
            df: discount factor
                Range df: [0(short term), 1 (long term)]
        board:
            Game board
        opponent: from players
            Object with "get_move()" method
        """
        reward = None  # Calculate a reward for the move
        # Agent's move
        # print("agent")
        action = row,col = self.get_move(board, p=True) # Will be a good action?
        state = board.get_state()  # This is the state!
        board.move(row, col, self.player)
        # print(board.get_txt())
        if board.is_winner(self.player):  # Agent wins
            reward = 1
        elif board.is_finished():  # Draw
            reward = 0
        if reward!=None:
            depth = 1  # Game Over
            Q_diff_avg = 0
        else:
            # print("opponent")
            #  Opponent's move
            row,col = opponent.get_move(board)
            board.move(row, col, opponent.player)
            # print(board.get_txt())
            if board.is_winner(opponent.player):  # Opponent wins
                reward = -1
            elif board.is_finished(): # Draw
                reward = 0
            if reward!=None:  # Game over
                depth = 2
                Q_diff_avg = 0
            else:  # Don't know reward, play more...
                reward, Q_diff_avg, depth  = self._train_1_game(lr, f_df, board, opponent)
                depth += 1
        # I know how good the action is (reward)
        Q_diff = self._update_Q(state, action, reward, lr, f_df(depth))
        Q_diff_avg += Q_diff/(depth)
        return (reward, Q_diff_avg, depth)



    def _autotrain_1_game(self, lr, f_df, board):
        """Train agent by playing against itself
        """
        reward = None  # Calculate a reward for the move
        # Agent's move
        # print("agent")
        row,col = self.get_move(board, p=True)
        state = board.get_state()  # This is the state!
        action = (row, col)  # Will be a good action?
        board.move(row, col, self.player)
        # print(board.get_txt())
        if board.is_winner(self.player):  # Agent wins
            reward = 1
        elif board.is_finished():  # Draw
            reward = 0
        if reward!=None:
            depth = 1  # Game Over
            Q_diff_avg = 0
        else:
            self.player = 2 if self.player==1 else 1  # Now I'm opponent
            reward, Q_diff_avg, depth  = self._autotrain_1_game(lr, f_df, board)
            depth += 1
            self.player = 2 if self.player==1 else 1  # Back to player
            reward = -reward
        # I know how good the action is (reward)
        Q_diff = self._update_Q(state, action, reward, lr, f_df(depth))
        Q_diff_avg += Q_diff/(depth)
        return (reward, Q_diff_avg, depth)
