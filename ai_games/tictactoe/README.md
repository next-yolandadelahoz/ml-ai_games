# Tic-tac-toe

This is the classic [tic-tac-toe](https://en.wikipedia.org/wiki/Tic-tac-toe) game on a 3x3 board.


## Agents
* Human player.
* Random.
* Minimax with alpa-beta prunning (this agent NEVER loses).
* Q-Learning (Reinforcement Learning).
* Inverse Reinforcement Learning.


## Play a game!
It is possible to make agents play against each other. So a human can play against an optimal minimax agent or other human; or even face two minimax agents.

Activate the environment
```bash
source venv/bin/activate
```

Play a game!
```
tictactoe
```

Or get some help
```
tictactoe -h
```


## Experiments
* [Q-Learning training](NB01-rl_tests.ipynb).
* [Inverse Reinforcement Learning](NB02-irl.ipynb).
