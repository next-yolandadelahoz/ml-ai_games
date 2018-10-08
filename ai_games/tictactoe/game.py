
from board import Board
from players.human import Human
from players.minimax import Minimax
from players.qlearner import QLearner
from players.random import Random
import argparse


def play_game(player1, player2, board, print_board=False):
    """Play a game until endself.
    PARAMETERS:
    player1:
    player2:
    board:
    print_board: whether to print the board on every turn.

    RETURN:
    winner: int
        1 (player1 wins)
        2 (player2 wins)
        -1 (draw, no more moves)
    """
    if print_board:
        print(board)
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
            if print_board:
                print(board)
            if board.is_winner(p.player):
                winner = p.player
        else:
            winner=-1
    return (winner, board)



if __name__=="__main__":
    # Argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-p1", default='human', choices=['human', 'minimax', 'qlearner', 'random'], help="Add player 1")
    parser.add_argument("-p2", default='minimax', choices=['human', 'minimax', 'qlearner', 'random'], help="Add player 2")
    args = parser.parse_args()

    players = {
        'human': Human,
        'minimax': Minimax,
        'qlearner': QLearner,
        'random': Random
    }

    winner, board = play_game(
        players.get(args.p1)(1),
        players.get(args.p2)(2),
        Board(),
        print_board=True
    )

    # TODO: clear screen
    if winner==-1:
        print("It's a draw")
    else:
        print("Player{} wins!".format(winner))
    # print("Board:\n{}".format(board.get_txt()))
