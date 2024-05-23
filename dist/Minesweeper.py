import pygame
import random
import os

pygame.init()

# Constants
BG_COLOR = (192, 192, 192)
GRID_COLOR = (128, 128, 128)
GAME_WIDTH = 10
GAME_HEIGHT = 10
NUM_MINE = 9
GRID_SIZE = 32
BORDER = 16
TOP_BORDER = 100
DISPLAY_WIDTH = GRID_SIZE * GAME_WIDTH + BORDER * 2
DISPLAY_HEIGHT = GRID_SIZE * GAME_HEIGHT + BORDER + TOP_BORDER
score_uno = 0
score_duplication = False

gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
timer = pygame.time.Clock()
pygame.display.set_caption("Minesweeper")


def load_image(file_name):
    return pygame.image.load(os.path.join("mines", file_name))


spr_emptyGrid = load_image("empty.png")
spr_flag = load_image("flag.png")
spr_grid = load_image("grid.png")
spr_grid1 = load_image("grid1.png")
spr_grid2 = load_image("grid2.png")
spr_grid3 = load_image("grid3.png")
spr_grid4 = load_image("grid4.png")
spr_grid5 = load_image("grid5.png")
spr_grid6 = load_image("grid6.png")
spr_grid7 = load_image("grid7.png")
spr_grid8 = load_image("grid8.png")
spr_mine = load_image("mine.png")
spr_mineClicked = load_image("mineClicked.png")
spr_mineFalse = load_image("mineFalse.png")


# global values
grid = []
mines = []


def drawText(txt, s, yOff=0):
    screen_text = pygame.font.SysFont("Calibri", s, True).render(txt, True, (0, 0, 0))
    rect = screen_text.get_rect()
    rect.center = (GAME_WIDTH * GRID_SIZE / 2 + BORDER, GAME_HEIGHT * GRID_SIZE / 2 + TOP_BORDER + yOff)
    gameDisplay.blit(screen_text, rect)


class Grid:
    def __init__(self, xGrid, yGrid, type):
        self.xGrid = xGrid
        self.yGrid = yGrid
        self.clicked = False
        self.mineClicked = False
        self.mineFalse = False
        self.flag = False
        self.rect = pygame.Rect(BORDER + self.xGrid * GRID_SIZE, TOP_BORDER + self.yGrid * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        self.val = type

    def drawGrid(self):
        if self.mineFalse:
            gameDisplay.blit(spr_mineFalse, self.rect)
        else:
            if self.clicked:
                if self.val == -1:
                    if self.mineClicked:
                        gameDisplay.blit(spr_mineClicked, self.rect)
                    else:
                        gameDisplay.blit(spr_mine, self.rect)
                else:
                    if self.val == 0:
                        gameDisplay.blit(spr_emptyGrid, self.rect)
                    elif self.val == 1:
                        gameDisplay.blit(spr_grid1, self.rect)
                    elif self.val == 2:
                        gameDisplay.blit(spr_grid2, self.rect)
                    elif self.val == 3:
                        gameDisplay.blit(spr_grid3, self.rect)
                    elif self.val == 4:
                        gameDisplay.blit(spr_grid4, self.rect)
                    elif self.val == 5:
                        gameDisplay.blit(spr_grid5, self.rect)
                    elif self.val == 6:
                        gameDisplay.blit(spr_grid6, self.rect)
                    elif self.val == 7:
                        gameDisplay.blit(spr_grid7, self.rect)
                    elif self.val == 8:
                        gameDisplay.blit(spr_grid8, self.rect)

            else:
                if self.flag:
                    gameDisplay.blit(spr_flag, self.rect)
                else:
                    gameDisplay.blit(spr_grid, self.rect)

    def revealGrid(self):
        self.clicked = True
        if self.val == 0:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < GAME_WIDTH:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < GAME_HEIGHT:
                            if not grid[self.yGrid + y][self.xGrid + x].clicked:
                                grid[self.yGrid + y][self.xGrid + x].revealGrid()
        elif self.val == -1:
            for m in mines:
                if not grid[m[1]][m[0]].clicked:
                    grid[m[1]][m[0]].revealGrid()

    def updateValue(self):
        if self.val != -1:
            for x in range(-1, 2):
                if self.xGrid + x >= 0 and self.xGrid + x < GAME_WIDTH:
                    for y in range(-1, 2):
                        if self.yGrid + y >= 0 and self.yGrid + y < GAME_HEIGHT:
                            if grid[self.yGrid + y][self.xGrid + x].val == -1:
                                self.val += 1


def gameLoop():
    score_duplication = True
    gameState = "Playing"
    mineLeft = NUM_MINE
    global grid
    grid = []
    global mines
    time = 0

    mines = [[random.randrange(0, GAME_WIDTH),
              random.randrange(0, GAME_HEIGHT)]]

    for c in range(NUM_MINE - 1):
        pos = [random.randrange(0, GAME_WIDTH),
               random.randrange(0, GAME_HEIGHT)]
        same = True
        while same:
            for i in range(len(mines)):
                if pos == mines[i]:
                    pos = [random.randrange(0, GAME_WIDTH), random.randrange(0, GAME_HEIGHT)]
                    break
                if i == len(mines) - 1:
                    same = False
        mines.append(pos)

    # Generating entire grid
    for j in range(GAME_HEIGHT):
        line = []
        for i in range(GAME_WIDTH):
            if [i, j] in mines:
                line.append(Grid(i, j, -1))
            else:
                line.append(Grid(i, j, 0))
        grid.append(line)

    # Update of the grid
    for i in grid:
        for j in i:
            j.updateValue()

    # Main Loop
    while gameState != "Exit":
        # Reset screen
        gameDisplay.fill(BG_COLOR)

        # User inputs
        for event in pygame.event.get():
            # Check if player close window
            if event.type == pygame.QUIT:
                gameState = "Exit"
            # Check if play restart
            if gameState == "Game Over" or gameState == "Win":
                if gameState == "Win" and score_duplication:
                    score_duplication = False
                    try:
                        with open("score_uno.txt", "r") as file:
                            score_uno = int(file.read())
                    except FileNotFoundError:
                        pass

                    score_uno += 1

                    with open("score_uno.txt", "w") as file:
                        file.write(str(score_uno))
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        gameState = "Exit"
                        gameLoop()
            else:
                if event.type == pygame.MOUSEBUTTONUP:
                    for i in grid:
                        for j in i:
                            if j.rect.collidepoint(event.pos):
                                if event.button == 1:
                                    j.revealGrid()
                                    if j.flag:
                                        mineLeft += 1
                                        j.falg = False
                                    if j.val == -1:
                                        gameState = "Game Over"
                                        j.mineClicked = True
                                elif event.button == 3:
                                    if not j.clicked:
                                        if j.flag:
                                            j.flag = False
                                            mineLeft += 1
                                        else:
                                            j.flag = True
                                            mineLeft -= 1

        win = True

        for i in grid:
            for j in i:
                j.drawGrid()
                if j.val != -1 and not j.clicked:
                    win = False
        if win and gameState != "Exit":
            gameState = "Win"

        # Draw Texts
        if gameState != "Game Over" and gameState != "Win":
            time += 1
        elif gameState == "Game Over":
            drawText("Game Over!", 50, -220)
            drawText("R to restart", 35, -190)
            for i in grid:
                for j in i:
                    if j.flag and j.val != -1:
                        j.mineFalse = True
        else:
            drawText("You WON!", 50, -220)
            drawText("R to restart", 35, -190)

        pygame.display.update()

        timer.tick(15)  # fps


gameLoop()
pygame.quit()
quit()