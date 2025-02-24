import pygame
import copy
from settings import (WIDTH, HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT, 
                      SIDE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, GRAY, BLUE, grid, COLORS)
from piece import Piece

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_piece = Piece()
        self.next_pieces = [Piece(), Piece(), Piece()]  
        self.hold_piece = None
        self.hold_used = False
        self.score = 0          
        self.level = 1 
        self.game_over = False 
        self.lines_cleared = 0 
        self.paused = False

    def new_piece(self):
        self.current_piece = self.next_pieces.pop(0)
        self.next_pieces.append(Piece())
        self.hold_used = False
        for i, row in enumerate(self.current_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    if grid[self.current_piece.y + i][self.current_piece.x + j] != 0:
                        self.game_over = True
                        break
            if self.game_over:
                break

    def hold_current_piece(self):
        if self.hold_used:
            return
        if self.hold_piece is None:
            self.hold_piece = self.current_piece
            self.new_piece()
        else:
            self.current_piece, self.hold_piece = self.hold_piece, self.current_piece
            self.current_piece.x = WIDTH // 2 - len(self.current_piece.shape[0]) // 2
            self.current_piece.y = 0
        self.hold_used = True

    def clear_lines(self):
        lines_cleared_now = 0
        new_grid = []
        for row in grid:
            if 0 not in row:
                lines_cleared_now += 1
            else:
                new_grid.append(row)
        for _ in range(lines_cleared_now):
            new_grid.insert(0, [0 for _ in range(WIDTH)])
        for i in range(HEIGHT):
            grid[i] = new_grid[i]
        if lines_cleared_now > 0:
            scoring = {1: 40, 2: 100, 3: 300, 4: 1200}
            self.score += scoring.get(lines_cleared_now, 0) * self.level
            self.lines_cleared += lines_cleared_now  

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
        current_color = COLORS[self.current_piece.color]
        ghost_color = tuple(min(255, int(c + (255 - c) * 0.5)) for c in current_color)
        dark_ghost_color = tuple(max(0, int(c * 0.75)) for c in ghost_color)
        for i, row in enumerate(ghost_piece.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid_y = ghost_piece.y + i
                    grid_x = ghost_piece.x + j
                    x_pos = grid_x * CELL_SIZE
                    y_pos = grid_y * CELL_SIZE
                    if 0 <= grid_y < HEIGHT and 0 <= grid_x < WIDTH and grid[grid_y][grid_x] == 0:
                        pygame.draw.rect(self.screen, dark_ghost_color, (x_pos, y_pos, CELL_SIZE, CELL_SIZE))
                        pygame.draw.rect(self.screen, ghost_color, (x_pos, y_pos, CELL_SIZE, CELL_SIZE), 1)
                    else:
                        pygame.draw.rect(self.screen, ghost_color, (x_pos, y_pos, CELL_SIZE, CELL_SIZE), 1)
                        
    def side_panel(self):
        pygame.draw.rect(self.screen, BLUE, (GRID_WIDTH, 0, SIDE_WIDTH, WINDOW_HEIGHT))
        font = pygame.font.SysFont('Times New Roman', 30)
        title_text = font.render('Tetris', False, BLACK)
        self.screen.blit(title_text, (GRID_WIDTH + 20, 20))
        # Render score, level, and lines text
        score_str = f"Score: {self.score}"
        level_str = f"Level: {self.level}"
        lines_str = f"Lines: {self.lines_cleared}"
        score_text = font.render(score_str, False, BLACK)
        level_text = font.render(level_str, False, BLACK)
        lines_text = font.render(lines_str, False, BLACK)
        self.screen.blit(score_text, (GRID_WIDTH + 20, 60))
        self.screen.blit(level_text, (GRID_WIDTH + 20, 100))
        self.screen.blit(lines_text, (GRID_WIDTH + 20, 140))
        margin = 5  
        max_width = max(font.size(score_str)[0], font.size(level_str)[0], font.size(lines_str)[0])
        text_height = font.get_height()
        border_x = GRID_WIDTH + 20 - margin
        border_y = 60 - margin
        border_width = max_width + 2 * margin
        border_height = (140 + text_height - 60) + 2 * margin
        pygame.draw.rect(self.screen, BLACK, (border_x, border_y, border_width, border_height), 2)
        preview_font = pygame.font.SysFont('Times New Roman', 20)
        hold_text = preview_font.render('Hold:', False, BLACK)
        self.screen.blit(hold_text, (GRID_WIDTH + 20, 180))
        if self.hold_piece is not None:
            for i, row in enumerate(self.hold_piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(GRID_WIDTH + 20 + j * (CELL_SIZE // 2),
                                           210 + i * (CELL_SIZE // 2),
                                           CELL_SIZE // 2, CELL_SIZE // 2)
                        pygame.draw.rect(self.screen, COLORS[self.hold_piece.color], rect)
                        pygame.draw.rect(self.screen, GRAY, rect, 1)
        next_text = preview_font.render('Next:', False, BLACK)
        self.screen.blit(next_text, (GRID_WIDTH + 20, 280))
        for index, piece in enumerate(self.next_pieces):
            for i, row in enumerate(piece.shape):
                for j, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(GRID_WIDTH + 20 + j * (CELL_SIZE // 2),
                                           320 + index * 80 + i * (CELL_SIZE // 2),
                                           CELL_SIZE // 2, CELL_SIZE // 2)
                        pygame.draw.rect(self.screen, COLORS[piece.color], rect)
                        pygame.draw.rect(self.screen, GRAY, rect, 1)

    def display_pause(self):
        font = pygame.font.SysFont('Times New Roman', 30)
        text = font.render("Paused - Press P to resume", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        padding = 10
        bg_rect = pygame.Rect(text_rect.left - padding,
                              text_rect.top - padding,
                              text_rect.width + 2 * padding,
                              text_rect.height + 2 * padding)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect)  
        pygame.draw.rect(self.screen, BLACK, bg_rect, 2) 
        self.screen.blit(text, text_rect)

    def display_game_over(self):
        font = pygame.font.SysFont('Times New Roman', 30)
        text = font.render("Game Over - Press R to restart", True, BLACK)
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        padding = 10
        bg_rect = pygame.Rect(text_rect.left - padding,
                              text_rect.top - padding,
                              text_rect.width + 2 * padding,
                              text_rect.height + 2 * padding)
        pygame.draw.rect(self.screen, (200, 200, 200), bg_rect)
        pygame.draw.rect(self.screen, BLACK, bg_rect, 2)
        self.screen.blit(text, text_rect)

    def update(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_ghost_piece()
        self.draw_piece()
        self.side_panel()

        if self.paused:
            self.display_pause()
        elif self.game_over:
            self.display_game_over()
        elif self.current_piece.locked:
            self.clear_lines()
            self.new_piece()