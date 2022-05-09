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
                    #out_string += " "
                else:
                    out_string += "."
                    #out_string += " "
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
        for j in range(9):
            col_poss = [self.poss(i, j) for i in range(9)]
            for digit in range(1, 10):
                poss_cells = [k for k, square in enumerate(col_poss) if digit in square]
                if len(poss_cells) == 1 and self.board[j][poss_cells[0]] is None:
                    self.board[j][poss_cells[0]] = digit
                    self.changed = True

    def is_solved(self):
        for i in range(9):
            for j in range(9):
                if self.board[j][i] is None:
                    return False
        return True

    def is_error(self):
        for i in range(9):
            for j in range(9):
                if len(self.poss(i, j)) == 0:
                    return True
            row_digits = [k for k in self.board[i] if k != "."]
            col_digits = [self.board[k][i] for k in range(9) if self.board[k][i] != "."]
            if len(row_digits) != len(set(row_digits)):
                return True
            if len(col_digits) != len(set(col_digits)):
                return True
        return False

    def find_guess(self):
        for i in range(9):
            for j in range(9):
                if len(self.poss(i, j)) == 2:
                    ind = i
                    j_ind = j
                    poss = list(self.poss(i, j))
                    myguess = poss[0]
                    return ind, j_ind, poss, myguess

    def guess(self):
        ind, j_ind, poss, myguess = self.find_guess()
        print(ind, j_ind, poss, myguess)
        print(self.board[ind][j_ind])
        new_board = Sudoku(str(self))
        new_board.reduce()
        new_board.board[ind][j_ind] = myguess
        if new_board.is_solved() and not new_board.is_error():
            self.board = new_board.board
        else:
            myguess = poss[1]
            self.board[ind][j_ind] = myguess

    def reduce(self):
        while True:
            self.changed = False
            self.reduce_one_poss()
            self.reduce_row_poss()
            self.reduce_col_poss()

            if not self.changed:
                break

    def solve(self):
        self.reduce()
        if not self.is_solved():
            self.guess()


def main():
    board = \
        """...769.1.
..1.3...6
......42.
1....65.8
.........
3.89....4
.36......
4...7.9..
.1.458..."""

    t_board = Sudoku(board)

    print(t_board)
    t_board.solve()
    print(t_board)


if __name__ == "__main__":
    main()
