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
GRID_HEIGHT = 150
GRID_WIDTH = 200
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PROB = 0.90
LAPSE = 500

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

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    grid.tick()

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

    def get_cells(self, live):
        result = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == live:
                    result.append((col, row))
        return result

    def initiate(self):
        for row in range(self.height):
            for col in range(self.width):
                n = random()
                if n > PROB:
                    self.grid[row][col] = 1

    def tick(self):
        to_die = []
        to_live = []

        lives = self.get_cells(1)
        for cell in lives:
            neighbors = self.get_neighbors(cell)
            if len(neighbors) < 2 or len(neighbors) > 3:
                to_die.append(cell)

        deads = self.get_cells(0)
        for cell in deads:
            neighbors = self.get_neighbors(cell)
            if len(neighbors) == 3:
                to_live.append(cell)

        for cell in to_die:
            self.erase_cell(cell)
        for cell in to_live:
            self.insert_cell(cell)

    def get_neighbors(self, pos):
        x, y = pos
        if x == 0 and y == 0:
            neighbors = [(x+1, y), (x+1, y+1), (x, y+1)]
        elif x == GRID_WIDTH - 1 and y == GRID_HEIGHT - 1:
            neighbors = [(x-1, y), (x-1, y-1), (x, y-1)]
        elif x == 0 and y == GRID_HEIGHT - 1:
            neighbors = [(x, y-1), (x+1, y-1), (x+1, y)]
        elif x == GRID_WIDTH - 1 and y == 0:
            neighbors = [(x, y+1), (x-1, y+1), (x-1, y)]
        elif x == 0:
            neighbors = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1)]
        elif x == GRID_WIDTH - 1:
            neighbors = [(x, y-1), (x, y+1), (x-1, y+1), (x-1, y), (x-1, y-1)]
        elif y == 0:
            neighbors = [(x+1, y), (x+1, y+1), (x, y+1), (x-1, y+1), (x-1, y)]
        elif y == GRID_HEIGHT - 1:
            neighbors = [(x, y-1), (x+1, y-1), (x+1, y), (x-1, y), (x-1, y-1)]
        else:
            neighbors = [(x, y-1), (x+1, y-1), (x+1, y), (x+1, y+1), (x, y+1),
                         (x-1, y+1), (x-1, y), (x-1, y-1)   ]
        result = [i for i in neighbors if self.get_value(i) == 1]
        return result

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
