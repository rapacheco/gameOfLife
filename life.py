    # Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
    # Any live cell with two or three live neighbours lives on to the next generation.
    # Any live cell with more than three live neighbours dies, as if by overpopulation.
    # Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction
import pygame
from pygame.locals import *
from math import ceil
from random import random

HEIGHT = 768
WIDTH = 1024
GRID_HEIGHT = 75
GRID_WIDTH = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PROB = 0.90
LAPSE = 300

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
    pygame.display.set_caption("Conway's Game of Life")
    clock = pygame.time.Clock()
    pygame.time.set_timer(USEREVENT+1, LAPSE)
    grid = Grid()
    grid.initiate()

    done = False
    while not done:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            # elif event.type == pygame.KEYDOWN:
            #     if event.key == pygame.K_SPACE:
            #         grid.tick()

            elif event.type == USEREVENT+1:
                grid.tick()

        screen.fill(WHITE)
        grid.draw(screen)
        pygame.display.flip()
    pygame.quit()

class Grid:
    def __init__(self):
        self.height = GRID_HEIGHT
        self.width = GRID_WIDTH
        self.grid = [[0 for _ in range(self.width)] for _ in range(self.height)]

    def get_value(self, pos):
        return self.grid[pos[1]][pos[0]]

    def insert_cell(self, pos):
        self.grid[pos[1]][pos[0]] = 1

    def erase_cell(self, pos):
        self.grid[pos[1]][pos[0]] = 0

    def initiate(self):
        for row in range(self.height):
            for col in range(self.width):
                n = random()
                if n > PROB:
                    self.grid[row][col] = 1

    def tick(self):
        to_die, to_live = [], []

        for row in range(self.height):
            for col in range(self.width):
                cell = (col, row)
                neighbors = self.get_neighbors(cell)
                if (len(neighbors) < 2 or len(neighbors) > 3) and self.get_value(cell) == 1:
                    to_die.append(cell)
                elif len(neighbors) == 3 and self.get_value(cell) == 0:
                    to_live.append(cell)

        for cell in to_die:
            self.erase_cell(cell)
        for cell in to_live:
            self.insert_cell(cell)

    def get_neighbors(self, pos):
        x, y = pos
        moves = [(0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        # return [move for move in moves if x + move[0] >= 0 and x + move[0] <= GRID_WIDTH-1 and
        #                                   y + move[1] >= 0 and y + move[1] <= GRID_HEIGHT-1 and
        #                                   self.get_value((x+move[0], y+move[1])) == 1]
        return [move for move in moves if self.get_value(((x+move[0])%GRID_WIDTH, (y+move[1])%GRID_HEIGHT)) == 1]

    def draw(self, screen):
        for i in range(1, self.height):
            pygame.draw.line(screen, BLACK, (0, i * (HEIGHT / self.height)), (WIDTH, i * (HEIGHT / self.height)))
        for i in range(1, self.width):
            pygame.draw.line(screen, BLACK, (i * (WIDTH / self.width), 0), (i * (WIDTH / self.width), HEIGHT))
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 1:
                    pygame.draw.rect(screen, BLACK, ([col * (WIDTH / self.width), row * (HEIGHT / self.height)],
                                                     [ceil(WIDTH / self.width), ceil(HEIGHT / self.height)]))

if __name__ == '__main__':
    main()
