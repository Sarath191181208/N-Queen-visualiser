import pygame
from main import validate, printBoard
import os
import time

pygame.init()
clock = pygame.time.Clock()
WIN = pygame.display.set_mode((540, 600))
pygame.display.set_caption("N Queen")

# colours
WHITE = (255, 255, 255)  # board colour
GREAY = (70, 70, 70)  # text colour
BLACK = (0, 0, 0)  # line colour
BLUE = (10, 40, 100)  # checks colour
TRANSPARENT = (0, 0, 0, 0)

checksClr = BLUE
boardClr = WHITE
txtClr = GREAY

# converts normal text to pygametxt


def PYtxt(txt: str, fontSize: int = 28, font: str = 'freesansbold.ttf', fontColour: tuple = BLACK):
    return (pygame.font.Font(font, fontSize)).render(txt, True, fontColour)


# images
# 506 x 493
queenImg = pygame.image.load(os.path.join('Assets', 'queen.png'))

# wait time waits untill next step
wait_time = 0.75
# grid parameters
cols = 9
rows = cols
FPS = 20


class Grid():
    def __init__(self, cols: int = 4, rows: int = 4, width: int = 400, height: int = 400):
        self.rows = cols
        self.cols = rows
        self.board = self.create_board((cols, rows))
        self.cubes = [
            [Cube(self.board[i][j], i, j, width, height, self.cols, self.rows)
             for j in range(self.cols)]
            for i in range(self.rows)
        ]
        self.width = width
        self.height = height

    def create_board(self, grid: tuple = (4, 4)) -> list[int]:
        board = []
        x, y = grid
        for i in range(0, x):
            help = []
            for j in range(0, y):
                help.append(0)
            board.append(help)
        return board

    def drawGrid(self, win):
        win.fill(boardClr)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        # Draw Cubes
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].draw(win)

        thick = 1
        # pygame.draw.line(win, (0, 0, 0), (i * rowGap, 0),i * rowGap, self.height), thick)
        for i in range(self.rows+1):
            pygame.draw.line(win, BLACK, (0, i*rowGap),
                             (self.height, rowGap*i), thick)
        for i in range(self.cols+1):
            pygame.draw.line(win, BLACK, (i*colGap, 0), (colGap*i, self.width))
        pygame.display.update()

    def updateAt(self, value, i, j, win):
        self.cubes[i][j].value = value
        self.drawGrid(win)


class Cube():
    def __init__(self, value, row, col, width, height, cols, rows):
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.cols = cols
        self.rows = rows
        self.centerFactor = 10

    def draw(self, win):
        # fnt = pygame.font.SysFont("comicsans", 40)
        rowGap = self.height / self.rows
        colGap = self.width / self.cols
        x = self.col * colGap
        y = self.row * rowGap
        # if self.col % 2 == 0 and self.row % 2 == 0:
        if (self.col % 2) == (self.row % 2):
            pygame.draw.rect(win, checksClr, pygame.Rect(x, y, colGap, rowGap))
        # if self.col % 2 == 1 and self.row % 2 == 1:
        #     pygame.draw.rect(win, checksClr, pygame.Rect(x, y, colGap, rowGap))

        if self.value == 1:
            newImg = pygame.transform.scale(
                queenImg, (int(colGap-self.centerFactor), int(rowGap-self.centerFactor)))
            win.blit(newImg, (x+self.centerFactor/2, y+self.centerFactor/2))

        # text = fnt.render("Q", 1, txtClr)
        # win.blit(text, (x + (colGap/2 - text.get_width()/2),
        #                 y + (rowGap/2 - text.get_height()/2)))


def solve(Board: list[int], col: int, win) -> bool:
    board = Board.board
    if col >= len(board[0]):
        #Board.updateAt(1, len(board)-1, col, win)
        return True
    for i in range(len(board)):
        if validate(board, (i, col)):
            board[i][col] = 1
            Board.updateAt(1, i, col, win)
            time.sleep(wait_time)
            if solve(Board, col+1, win):
                return True
            time.sleep(wait_time)
            Board.updateAt(0, i, col, win)
            board[i][col] = 0
    return False


def main(cols, rows):
    no_rows = rows
    no_cols = cols
    run = True
    board = Grid(no_cols, no_rows, 540, 540)
    board.drawGrid(WIN)
    if solve(board, 0, WIN):
        WIN.blit(PYtxt("Solved"), (20, 560))
        pygame.display.update()

    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == '__main__':
    main(cols, rows)
