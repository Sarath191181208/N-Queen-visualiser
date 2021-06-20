board = []


def create_board(grid: tuple = (4, 4)) -> list[int]:
    x, y = grid
    for i in range(0, x):
        help = []
        for j in range(0, y):
            help.append(0)
        board.append(help)
    return board


def printBoard(board: list[int]) -> None:
    for i in range(len(board)):
        for j in range(len(board[0])):
            temp = board[i][j]
            if temp == 1:
                temp = "Q"
            else:
                temp = " "
            print(" | "+temp, end="")
            if j == len(board[0])-1:
                print(" |")


def validate(board: list[int], pos: tuple) -> bool:
    # check row
    x, y = pos
    for i in range(len(board[x])):
        if board[x][i] == 1 and not i == y:
            return False

    # check diagonal
    for i, j in zip(range(x, -1, -1), range(y, -1, -1)):
        if board[i][j] == 1:
            return False
    for i, j in zip(range(x, len(board), 1), range(y, -1, -1)):
        if board[i][j] == 1:
            return False
    return True


def solve(board: list[int], col: int) -> bool:
    if col >= len(board):
        return True
    for i in range(len(board)):
        if validate(board, (i, col)):
            board[i][col] = 1
            if solve(board, col+1):
                return True

            board[i][col] = 0
    return False


def main():
    create_board((9, 9))
    if not solve(board, 0):
        print("board cant be solved")
    printBoard(board)
    # for i in range(len(board)):
    #     for j in range(len(board[0])):
    #         print(validate(board, 1, (i, j)), i, j)


if __name__ == '__main__':
    main()
