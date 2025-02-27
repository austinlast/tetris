import pygame
import copy
from settings import (WIDTH, HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
                      SIDE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, GRAY, BLUE, grid, COLORS)
from piece import Piece


class Game:
    def __init__(self):
        """
        Initializes the game.

        Parameters:
        None

        Returns:
        None
        """
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.current_piece = Piece()
        self.hold_piece = None
        self.hold_used = False
        self.score = 0
        self.level = 1
        self.game_over = False
        self.lines_cleared = 0

    def new_piece(self):
        """
        Creates a new piece and checks for game over condition.

        Parameters:
        None

        Returns:
        None
        """
        self.current_piece = Piece()
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
        """
        This Function holds the current piece then it swaps it with the held piece.

        Parameters:
        None

        Returns:
        None
        """
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
        """
        This function erases completed lines so the game can continue

        Parameters:
        None

        Returns:
        None
        """
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
        """
        This function draws the game grid onto the screen

        Parameters:
        None

        Returns:
        None
        """
        for y in range(HEIGHT):
            for x in range(WIDTH):
                pygame.draw.rect(self.screen, COLORS[grid[y][x]],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, GRAY,
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    def draw_piece(self):
        """
        Draws the current piece on the screen.

        Parameters:
        None

        Returns:
        None
        """
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
        """
        This function draws the ghost piece onto the bottom of the screen. 

        Parameters:
        None

        Returns:
        None
        """
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
                        pygame.draw.rect(self.screen, dark_ghost_color,
                                         (x_pos, y_pos, CELL_SIZE, CELL_SIZE))
                        pygame.draw.rect(self.screen, ghost_color,
                                         (x_pos, y_pos, CELL_SIZE, CELL_SIZE), 1)
                    else:
                        pygame.draw.rect(self.screen, ghost_color,
                                         (x_pos, y_pos, CELL_SIZE, CELL_SIZE), 1)

    def side_panel(self):
        """
        This function draws the side panel which shows the score and level.

        Parameters:
        None

        Returns:
        None
        """
        pygame.draw.rect(self.screen, BLUE, (GRID_WIDTH, 0, SIDE_WIDTH, WINDOW_HEIGHT))
        font = pygame.font.SysFont('Times New Roman', 30)
        title_text = font.render('Tetris', False, BLACK)
        self.screen.blit(title_text, (GRID_WIDTH + 20, 20))
        # Render score and level text
        score_str = f"Score: {self.score:06d}"
        level_str = f"Level: {self.level}"
        score_text = font.render(score_str, False, BLACK)
        level_text = font.render(level_str, False, BLACK)
        self.screen.blit(score_text, (GRID_WIDTH + 20, 60))
        self.screen.blit(level_text, (GRID_WIDTH + 20, 100))

    def display_game_over(self):
        """
        This function displays the game over screen with instructions to restart (press R).

        Parameters:
        None

        Returns:
        None
        """
        font = pygame.font.SysFont("Times New Roman", 30, bold=True)
        lines = [("Game Over", "red")]
        lines.append(("Press R to restart", "white"))

        rendered_lines = [(font.render(text, True, color), color) for text, color in lines]

        spacing = 10
        total_height = sum(surf.get_height() for surf, _ in rendered_lines) + spacing * (len(rendered_lines) - 1)
        padding = 15
        max_width = max(surf.get_width() for surf, _ in rendered_lines)
        container_width = max_width + 2 * padding
        container_height = total_height + 2 * padding
        container_x = (WINDOW_WIDTH - container_width) // 2
        container_y = (WINDOW_HEIGHT - container_height) // 2
        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)

        pygame.draw.rect(self.screen, "#1a1a1a", container_rect)
        pygame.draw.rect(self.screen, "white", container_rect, 2)

        current_y = container_y + padding
        for surf, _ in rendered_lines:
            x = container_x + (container_width - surf.get_width()) // 2
            self.screen.blit(surf, (x, current_y))
            current_y += surf.get_height() + spacing

    def update(self):
        """
        This function is called to update the display.

        Parameters:
        None

        Returns:
        None
        """
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_ghost_piece()
        self.draw_piece()
        self.side_panel()
        if self.game_over:
            self.display_game_over()
        elif self.current_piece.locked:
            self.clear_lines()
            self.new_piece()
