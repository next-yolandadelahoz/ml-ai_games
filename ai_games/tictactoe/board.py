import numpy as np


class Board:

    def __init__(self, N=3, board=None):
        """
        PARAMETERS
        N: int
            Number of dimensions of the board.
        board: np.array NxN
            Initialization board, 0 matrix if none.
        """
        if type(board)!=np.ndarray:
            self.board = np.zeros((N,N), dtype=np.uint8)
        else:
            self.board = board
        self.N = self.board.shape[0]
        self.txt_symbols = ' XO'
        self.vals = list(range(self.N))  # Speedup iterations


    def is_winner(self, player):
        """Return True if player is the winner

        player: int
            Player to check for victory
        """
        return any([
            any([ all(self.board[row,:]==player) for row in self.vals ]),  # 3x horizontal
            any([ all(self.board[:,col]==player) for col in self.vals ]),  # 3x vertical
            all([ self.board[i,i]==player for i in self.vals ]),  # diagonal \
            all([ self.board[self.N-1-i,i]==player for i in self.vals ]) # diagonal /
        ])


    def move(self, row, col, player):
        """Make a move in the board
        SIDE-EFFECT: modify board with the move.

        RETURN
        retval: Bool
            True if move is allowed, else False
        """
        retval = False
        if (0<=row<self.N and 0<=col<self.N and self.board[row,col]==0 ):
            self.board[row,col] = player
            retval = True
        return retval


    def get_candidates(self, player):
        """Return a list of posible-move board objects for player.

        RETURN
        retval: [ ((row,col), board) ]
            Ordered list of possible movement-board elements.
        """
        retval = []
        for row in self.vals:
            for col in self.vals:
                if self.board[row,col]==0:  # Available position
                    b = self.copy()
                    b.board[row,col] = player
                    retval.append(((row,col),b))
        return retval


    def copy(self):
        """Return a copy of the board
        """
        return( Board(board=self.board.copy()) )


    def get_txt(self):
        """Return a pretty string representation of the board.
        """
        row_sep = '\n'+'+'.join('-'*self.N)+'\n'
        return row_sep.join([
            '|'.join([
                self.txt_symbols[element] for element in self.board[row,:]
            ])
            for row in self.vals
        ])


    def get_state(self):
        # return hash(self.board.tobytes())  # More efficient, but less debuggable (IRL)
        return tuple(self.board.flat)


    def is_finished(self):
        """Check if there are NOT possible moves. There are 0s left.
        """
        return not np.any(self.board==0)
