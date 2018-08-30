
from board import Board
from players.human import Human
from players.minimax import Minimax
from players.qlearner import QLearner
from players.random import Random


def play_game(player1, player2, board):
    """Play a game until endself.
    PARAMETERS:
    player1:
    player2:
    board:

    RETURN:
    winner: int
        1 (player1 wins)
        2 (player2 wins)
        -1 (draw, no more moves)
    """
    winner = 0
    iter = 0
    while winner==0:
        iter +=1
        p = player1 if iter%2==1 else player2
        if not board.is_finished():
            valid_move = False
            while not valid_move: # Do not trust player
                row,col = p.get_move(board.copy())  # Modification-proof
                valid_move = board.move(row, col, p.player)
            if board.is_winner(p.player):
                winner = p.player
        else:
            winner=-1
    return (winner, board)



if __name__=="__main__":
    # TODO: from args choose players -p1 -p2 [ human, minimax, minimax_prob, qlearned ]
    winner, board = play_game(
        Human(1),
        Minimax(2),
        Board()
    )
    # TODO: clear screen
    if winner==-1:
        print("It's a draw")
    else:
        print("Player{} wins!".format(winner))
    print("Board:\n{}".format(board.get_txt()))
