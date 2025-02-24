import pygame
import copy
from settings import (WIDTH, HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, 
                      SIDE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, GRAY, BLUE, grid, COLORS)
from piece import Piece

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_piece = Piece()
        self.next_pieces = [Piece(), Piece(), Piece()] # Shows the next 3 pieces
        self.hold_piece = None
        self.hold_used = False
        self.score = 0          
        self.level = 1 
        self.game_over = False 

    def new_piece(self):
        self.current_piece = self.next_pieces.pop(0)
        self.next_pieces.append(Piece())
        self.hold_used = False
        if self.current_piece.is_valid(0, 0):
            self.game_over = True

    def hold_current_piece(self):
        if self.hold_used:
            return
        if self.hold_piece is None:
            self.hold_piece = self.current_piece
            self.new_piece()
        else:
            # Swap the current piece with the held piece.
            self.current_piece, self.hold_piece = self.hold_piece, self.current_piece
            self.current_piece.x = WIDTH // 2 - len(self.current_piece.shape[0]) // 2
            self.current_piece.y = 0
        self.hold_used = True

    def clear_lines(self):
        lines_cleared = 0
        new_grid = []
        for row in grid:
            if 0 not in row:
                lines_cleared += 1
            else:
                new_grid.append(row)
        for _ in range(lines_cleared):
            new_grid.insert(0, [0 for _ in range(WIDTH)])
        for i in range(HEIGHT):
            grid[i] = new_grid[i]
        if lines_cleared > 0:
            scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
            self.score += scoring.get(lines_cleared, 0) * self.level

    def draw_grid(self):
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pygame.draw.rect(self.screen, COLORS[grid[y][x]],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, GRAY,
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_piece(self):
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(self.screen, COLORS[self.current_piece.color],
                                     ((self.current_piece.x + j) * CELL_SIZE,
                                      (self.current_piece.y + i) * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE))
                    pygame.draw.rect(self.screen, GRAY,
                                     ((self.current_piece.x + j) * CELL_SIZE,
                                      (self.current_piece.y + i) * CELL_SIZE,
                                      CELL_SIZE, CELL_SIZE), 1)

    def draw_ghost_piece(self):
        ghost_piece = copy.deepcopy(self.current_piece)
        while not ghost_piece.is_valid(0, 1):
            ghost_piece.y += 1
        ghost_color = (60, 240, 0)
        for i, row in enumerate(ghost_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    rect = pygame.Rect((ghost_piece.x + j) * CELL_SIZE,
                                       (ghost_piece.y + i) * CELL_SIZE,
                                       CELL_SIZE, CELL_SIZE)
                    pygame.draw.rect(self.screen, ghost_color, rect, 1)

    def side_panel(self):
        pygame.draw.rect(self.screen, BLUE, (GRID_WIDTH, 0, SIDE_WIDTH, WINDOW_HEIGHT))
        font = pygame.font.SysFont('Times New Roman', 30)
        title_text = font.render('Tetris', False, BLACK)
        self.screen.blit(title_text, (GRID_WIDTH + 20, 20))
        score_text = font.render(f'Score: {self.score}', False, BLACK)
        self.screen.blit(score_text, (GRID_WIDTH + 20, 60))
        level_text = font.render(f'Level: {self.level}', False, BLACK)
        self.screen.blit(level_text, (GRID_WIDTH + 20, 100))
        preview_font = pygame.font.SysFont('Times New Roman', 20)
        hold_text = preview_font.render('Hold:', False, BLACK)
        self.screen.blit(hold_text, (GRID_WIDTH + 20, 150))
        if self.hold_piece is not None:
            for i, row in enumerate(self.hold_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(GRID_WIDTH + 20 + j * (CELL_SIZE // 2),
                                           180 + i * (CELL_SIZE // 2),
                                           CELL_SIZE // 2, CELL_SIZE // 2)
                        pygame.draw.rect(self.screen, COLORS[self.hold_piece.color], rect)
                        pygame.draw.rect(self.screen, GRAY, rect, 1)
        next_text = preview_font.render('Next:', False, BLACK)
        self.screen.blit(next_text, (GRID_WIDTH + 20, 250))
        for index, piece in enumerate(self.next_pieces):
            for i, row in enumerate(piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(GRID_WIDTH + 20 + j * (CELL_SIZE // 2),
                                           280 + index * 80 + i * (CELL_SIZE // 2),
                                           CELL_SIZE // 2, CELL_SIZE // 2)
                        pygame.draw.rect(self.screen, COLORS[piece.color], rect)
                        pygame.draw.rect(self.screen, GRAY, rect, 1)

    def display_game_over(self):
        # Added: Draw the Game Over message centered on the screen
        font = pygame.font.SysFont('Times New Roman', 40)
        text = font.render("Game Over - Press R to restart", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(text, text_rect)

    def update(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_ghost_piece()
        self.draw_piece()
        self.side_panel()

        if self.current_piece.locked:   
            self.clear_lines()
            self.new_piece()