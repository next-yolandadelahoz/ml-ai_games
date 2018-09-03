
import time

from board import Board
from game import play_game


def test_players(p1, p2, n_games):
	result = {
		1: 0,  # Player 1 wins
		2: 0,  # Player 2 wins
		-1: 0  # Draws
	}
	p1.set_player(1)
	p2.set_player(2)
	for i in range(n_games):
		winner,board = play_game(p1, p2, Board())
		result[winner] += 1
	return result


def train_player_seconds(learner, teacher, train_func, seconds):
	games_played = 0
	time_stop = time.time() + seconds
	while time.time() < time_stop:
		# As player 1
		learner.set_player(1)
		teacher.set_player(2)
		train_func(Board(), learner, teacher)
		games_played += 1
		# As player 2
		teacher.set_player(1)
		learner.set_player(2)
		board = Board()
		board.move(*teacher.get_move(board), player=1)
		train_func(board, learner, teacher)
		games_played += 1
	return games_played


def train_player_games(learner, teacher, train_func, games):
	time_start = time.time()
	for game in range(games):
		# As player 1
		learner.set_player(1)
		teacher.set_player(2)
		train_func(Board(), learner, teacher)
		# As player 2
		teacher.set_player(1)
		learner.set_player(2)
		board = Board()
		board.move(*teacher.get_move(board), player=1)
		train_func(board, learner, teacher)
	return time.time()-time_start
