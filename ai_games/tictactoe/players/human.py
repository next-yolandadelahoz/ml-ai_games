

class Human:

    def __init__(self, player):
        self.player = player

    def get_move(self, board):
        #print(board.get_txt())
        # TODO: clear screen
        cell = -1
        while cell not in range(9):
            cell = input("Player {}, choose the cell (1-9) to put your '{}': ".format(
                self.player,
                board.txt_symbols[self.player])
            )
            try:
                cell = int(cell)-1  # -1 to easy transformation to indices
            except Exception:
                pass
        return (cell//board.N, cell%board.N)
