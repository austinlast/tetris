import pygame

pygame.init()
pygame.font.init()

WIDTH = 10
HEIGHT = 20
CELL_SIZE = 30
GRID_WIDTH = WIDTH * CELL_SIZE
GRID_HEIGHT = HEIGHT * CELL_SIZE

SIDE_WIDTH = 180
WINDOW_WIDTH = GRID_WIDTH + SIDE_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (173, 216, 230)

grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]

# Tetrimino shapes
SHAPES = [
    ("I", [[1, 1, 1, 1]]),
    ("O", [[2, 2], [2, 2]]),
    ("T", [[0, 3, 0], [3, 3, 3]]),
    ("S", [[0, 4, 4], [4, 4, 0]]),
    ("Z", [[5, 5, 0], [0, 5, 5]]),
    ("J", [[6, 0, 0], [6, 6, 6]]),
    ("L", [[0, 0, 7], [7, 7, 7]])
]

COLORS = [
    (0, 0, 0),
    (0, 255, 255),
    (255, 255, 0),
    (128, 0, 128),
    (0, 255, 0),
    (255, 0, 0),
    (0, 0, 255),
    (255, 165, 0)
]
