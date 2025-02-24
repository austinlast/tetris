import pygame
import copy
from settings import (WIDTH, HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, 
                      SIDE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, GRAY, BLUE, grid, COLORS)
from piece import Piece

# starts ui
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Tetris')

current_piece = Piece()

def new_piece():
    global current_piece
    current_piece = Piece()

def draw_grid():
    for y in range(HEIGHT):
        for x in range(WIDTH):
            pygame.draw.rect(screen, COLORS[grid[y][x]],
                             (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY,
                             (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_piece():
    for i, row in enumerate(current_piece.shape):
        for j, cell in enumerate(row):
            if cell:
                pygame.draw.rect(screen, COLORS[current_piece.color],
                                 ((current_piece.x + j) * CELL_SIZE,
                                  (current_piece.y + i) * CELL_SIZE,
                                  CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, GRAY,
                                 ((current_piece.x + j) * CELL_SIZE,
                                  (current_piece.y + i) * CELL_SIZE,
                                  CELL_SIZE, CELL_SIZE), 1)

def side_panel():
    score = 0
    pygame.draw.rect(screen, BLUE, (GRID_WIDTH, 0, SIDE_WIDTH, WINDOW_HEIGHT))  # Background
    font = pygame.font.SysFont('Times New Roman', 30)
    title_text = font.render('Tetris', False, BLACK)
    screen.blit(title_text, (GRID_WIDTH + 20, 20))
    score_text = font.render(f'Score: {score}', False, BLACK)
    screen.blit(score_text, (GRID_WIDTH + 20, 100))

def draw_ghost_piece(): 
    ghost_piece = copy.deepcopy(current_piece)
    while not ghost_piece.is_valid(0, 1):
        ghost_piece.y += 1
    ghost_color = (60, 240, 0) # Ghost color - Green
    for i, row in enumerate(ghost_piece.shape):
        for j, cell in enumerate(row):
            if cell:
                rect = pygame.Rect((ghost_piece.x + j) * CELL_SIZE,
                                   (ghost_piece.y + i) * CELL_SIZE,
                                   CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, ghost_color, rect, 1)