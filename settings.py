import pygame

# Sets up pygame
pygame.init()
pygame.font.init()

# All global variables that we will use
WIDTH = 10
HEIGHT = 20
CELL_SIZE = 30
GRID_WIDTH = WIDTH * CELL_SIZE
GRID_HEIGHT = HEIGHT * CELL_SIZE

SIDE_WIDTH = 200
WINDOW_WIDTH = GRID_WIDTH + SIDE_WIDTH
WINDOW_HEIGHT = GRID_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
BLUE = (173, 216, 230)

# Sets the grid up 
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

# sets colors for the pieces
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

BLOCK_TEXTURES = {
    "0": pygame.transform.scale(pygame.image.load('images/black_background.png'), (CELL_SIZE, CELL_SIZE)),
    "1": pygame.transform.scale(pygame.image.load('images/light_blue_block.png'), (CELL_SIZE, CELL_SIZE)),
    "2": pygame.transform.scale(pygame.image.load('images/yellow_block.png'), (CELL_SIZE, CELL_SIZE)),
    "3": pygame.transform.scale(pygame.image.load('images/purple_block.png'), (CELL_SIZE, CELL_SIZE)),
    "4": pygame.transform.scale(pygame.image.load('images/green_block.png'), (CELL_SIZE, CELL_SIZE)),
    "5": pygame.transform.scale(pygame.image.load('images/red_block.png'), (CELL_SIZE, CELL_SIZE)),
    "6": pygame.transform.scale(pygame.image.load('images/dark_blue_block.png'), (CELL_SIZE, CELL_SIZE)),
    "7": pygame.transform.scale(pygame.image.load('images/orange_block.png'), (CELL_SIZE, CELL_SIZE)),
}
