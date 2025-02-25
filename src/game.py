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
        self.high_scores = []
        self.new_high = False
        self.high_scores_updated = False

    def load_high_scores(self):
        try:
            with open("highscores.txt", "r") as f:
                lines = f.read().strip().splitlines()
                scores = []
                for line in lines:
                    parts = line.rsplit(" ", 1) 
                    if len(parts) == 2 and parts[1].isdigit():
                        scores.append((parts[0], int(parts[1]))) 
                return scores
        except:
            return []
        
    def save_high_scores(self, scores):
        with open("highscores.txt", "w") as f:
            for initials, score in scores:
                f.write(f"{initials} {score}\n")

    def update_high_scores(self, current_score):
        old_scores = self.load_high_scores()
        is_new_high = False
        new_initials = None

        if len(old_scores) < 3 or current_score > min(score for _, score in old_scores):
            is_new_high = True
            new_initials = self.get_initials_input(current_score)  

        if is_new_high:
            scores = old_scores + [(new_initials, current_score)]
            scores = sorted(scores, key=lambda x: x[1], reverse=True)[:3]  # Keep top 3
            self.save_high_scores(scores)
            return scores, is_new_high
        else:
            return old_scores, is_new_high
    
    def get_initials_input(self, new_score):
        initials = ""  
        font = pygame.font.SysFont("Times New Roman", 24, bold=True)
        input_active = True

        formatted_score = f"{new_score:06d}"

        while input_active:
            self.screen.fill(BLACK)
            
            box_width, box_height = 300, 200  
            box_x = (WINDOW_WIDTH - box_width) // 2  
            box_y = (WINDOW_HEIGHT - box_height) // 2  
            pygame.draw.rect(self.screen, "black", (box_x, box_y, box_width, box_height))
            pygame.draw.rect(self.screen, "white", (box_x, box_y, box_width, box_height), 2)

            new_high_text = font.render("NEW HIGH SCORE!", True, "red")
            score_text = font.render(formatted_score, True, "#00bfff")  # Cyan for formatted score
            prompt_text = font.render("Enter Your Initials", True, "white")
            initials_display = initials if initials else "_ _ _"  
            initials_text = font.render(initials_display, True, "#ffd700")  # Gold for initials
            confirm_text = font.render("Press Enter to Confirm", True, "gray")

            self.screen.blit(new_high_text, (box_x + (box_width - new_high_text.get_width()) // 2, box_y + 20))
            self.screen.blit(score_text, (box_x + (box_width - score_text.get_width()) // 2, box_y + 60))
            self.screen.blit(prompt_text, (box_x + (box_width - prompt_text.get_width()) // 2, box_y + 100))
            self.screen.blit(initials_text, (box_x + (box_width - initials_text.get_width()) // 2, box_y + 140))
            self.screen.blit(confirm_text, (box_x + (box_width - confirm_text.get_width()) // 2, box_y + 170))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(initials) > 0:
                        input_active = False  
                    elif event.key == pygame.K_BACKSPACE and len(initials) > 0:
                        initials = initials[:-1]  
                    elif len(initials) < 3 and event.unicode.isalpha():
                        initials += event.unicode.upper()  

        return initials 
    
    def format_score(score):
        return f"{score:06d}"

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
        score_str = f"Score: {self.score:06d}"
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
        font = pygame.font.SysFont("Times New Roman", 30, bold=True)
        # Specify each line along with its color
        lines = []
        lines.append(("Game Over", "red"))
        if self.new_high:
            lines.append(("Congrats, New High Score!", "#ffd700"))  # Gold
        lines.append(("High Scores:", "white"))
        for initials, score in self.high_scores:
            # Ensure score is formatted as six digits
            lines.append((f"{initials} {score:06d}", "#00bfff"))  # Cyan
        lines.append(("Press R to restart", "white"))
        
        # Render each line with its corresponding color
        rendered_lines = [ (font.render(text, True, color), color) for text, color in lines ]
        
        spacing = 10
        total_height = sum(surf.get_height() for surf, _ in rendered_lines) + spacing * (len(rendered_lines) - 1)
        padding = 15
        max_width = max(surf.get_width() for surf, _ in rendered_lines)
        container_width = max_width + 2 * padding
        container_height = total_height + 2 * padding
        container_x = (WINDOW_WIDTH - container_width) // 2
        container_y = (WINDOW_HEIGHT - container_height) // 2
        container_rect = pygame.Rect(container_x, container_y, container_width, container_height)
        
        # Draw the container box with dark gray background and white border
        pygame.draw.rect(self.screen, "#1a1a1a", container_rect)
        pygame.draw.rect(self.screen, "white", container_rect, 2)
        
        current_y = container_y + padding
        for surf, _ in rendered_lines:
            x = container_x + (container_width - surf.get_width()) // 2
            self.screen.blit(surf, (x, current_y))
            current_y += surf.get_height() + spacing


    def update(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_ghost_piece()
        self.draw_piece()
        self.side_panel()
        if self.paused:
            self.display_pause()
        elif self.game_over:
            if not self.high_scores_updated:
                self.high_scores, self.new_high = self.update_high_scores(self.score)
                self.high_scores_updated = True
            self.display_game_over()
        elif self.current_piece.locked:
            self.clear_lines()
            self.new_piece()