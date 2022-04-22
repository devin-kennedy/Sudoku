class Sudoku:
    def __init__(self, board=None):
        self.changed = False
        if board is None:
            self.parse(""".........
.........
.........
.........
.........
.........
.........
.........
.........""")
        else:
            self.parse(board)

    def parse(self, board):
        board = board.split('\n')

        def process_char(c):
            try:
                if int(c) in {1, 2, 3, 4, 5, 6, 7, 8, 9}:
                    return int(c)
                else:
                    return None
            except:
                return None

        self.board = []

        for line in board:
            self.board.append([process_char(c) for c in line])

    def __repr__(self):
        out_string = ""
        for line in self.board:
            for c in line:
                if c is not None:
                    out_string += str(c)
                    out_string += " "
                else:
                    out_string += "□"
                    out_string += " "
            out_string += "\n"
        return out_string

    def poss(self, i, j):
        if self.board[j][i] is None:
            poss_digits = {1, 2, 3, 4, 5, 6, 7, 8, 9}
            poss_digits -= set(self.board[j])
            poss_digits -= set([self.board[k][i] for k in range(9)])

            box_i = 3 * (i // 3)
            box_j = 3 * (j // 3)

            for k in range(3):
                poss_digits -= set(self.board[box_j + k][box_i:box_i + 3])

            return poss_digits
        else:
            return {self.board[j][i]}

    def reduce_one_poss(self):
        for i in range(9):
            for j in range(9):
                if self.board[j][i] is None:
                    square_poss = self.poss(i, j)
                    if len(square_poss) == 1:
                        self.board[j][i] = list(square_poss)[0]
                        self.changed = True

    def reduce_row_poss(self):
        for i in range(9):
            row_poss = [self.poss(i, j) for j in range(9)]
            for digit in range(1, 10):
                poss_cells = [k for k, square in enumerate(row_poss) if digit in square]
                if len(poss_cells) == 1 and self.board[poss_cells[0]][i] is None:
                    self.board[poss_cells[0]][i] = digit
                    self.changed = True

    def reduce_col_poss(self):
        raise NotImplementedError("TODO")

    def is_solved(self):
        for i in range(9):
            for j in range(9):
                if self.board[j][i] is None:
                    return False
        return True

    def solve(self):
        while True:
            self.changed = False
            self.reduce_one_poss()
            self.reduce_row_poss()

            if not self.changed:
                break


def main():
    board = \
        """..3.549..
.1.6....2
.......5.
..24...6.
59..6...4
7...38.2.
...3....6
.....658.
..68...43"""

    t_board = Sudoku(board)

    print(t_board)
    t_board.solve()
    print(t_board)
    for i in range(9):
        print(t_board.board[i])


if __name__ == "__main__":
    main()
