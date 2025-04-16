import pygame
import copy

import settings
from settings import (WIDTH, HEIGHT, CELL_SIZE, GRID_WIDTH, GRID_HEIGHT,
                      SIDE_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT, BLACK, GRAY, BLUE, grid, COLORS, BLOCK_TEXTURES)
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
        self.high_scores = []
        self.new_high = False
        self.high_scores_updated = False

    def load_high_scores(self):
        """
            Loads high scores from a text file and returns them as a list of (name, score) tuples.

            Parameters:
                None

            Returns:
                list: list of tuples containing player names and their corresponding scores.
                    Returns an empty list if the file cannot be read or is improperly formatted.
        """
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
        """
            Saves the given list of high scores to a text file.

            Parameters:
                scores (list): A list of tuples containing player initials and their scores.

            Returns:
            None
        """
        with open("highscores.txt", "w") as f:
            for initials, score in scores:
                f.write(f"{initials} {score}\n")

    def update_high_scores(self, current_score):
        """
            Updates the high score list if the current score qualifies as a new high score.

            Parameters:
                current_score (int): The score achieved in the current game session.

            Returns:
            tuple:
                - list: Updated list of top high scores (max 3 entries).
                - bool: Indicates whether the current score was a new high score.
        """
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
        """
            Displays a prompt for the player to enter their initials after achieving a high score.

            Parameters:
                new_score (int): The new high score to display during the input prompt.

            Returns:
                str: A string of up to 3 uppercase letters entered by the player.
        """
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
        """
            Formats a numerical score as a six-digit string, padding with leading zeros if necessary.

            Parameters:
                score (int): The score to format.

            Returns:
                str: The formatted score as a six-digit string.
        """
        return f"{score:06d}"

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
                # If grid is empty
                if grid[y][x] == 0:
                    self.screen.blit(BLOCK_TEXTURES[str(grid[y][x])],
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                    pygame.draw.rect(self.screen, GRAY,
                                     (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
                # If grid is filled by a piece
                else:
                    self.screen.blit((grid[y][x]),
                                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

                # Adds gray lines to placed pieces
                #pygame.draw.rect(self.screen, GRAY,
                #                 (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


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
                    self.screen.blit(BLOCK_TEXTURES[str(self.current_piece.color)],
                                     ((self.current_piece.x + j) * CELL_SIZE,
                                      (self.current_piece.y + i) * CELL_SIZE))

                    # Uncomment to add gray lines to falling pieces
                    #pygame.draw.rect(self.screen, GRAY,
                    #                 ((self.current_piece.x + j) * CELL_SIZE,
                    #                  (self.current_piece.y + i) * CELL_SIZE,
                    #                  CELL_SIZE, CELL_SIZE), 1)


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
                        #Makes ghost outline
                        #pygame.draw.rect(self.screen, dark_ghost_color,
                        #                 (x_pos, y_pos, CELL_SIZE, CELL_SIZE))
                        pygame.draw.rect(self.screen, ghost_color,
                                         (x_pos, y_pos, CELL_SIZE, CELL_SIZE), 2)
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
        # lines_str = f"Lines: {self.lines_cleared}"
        score_text = font.render(score_str, False, BLACK)
        level_text = font.render(level_str, False, BLACK)
        # lines_text = font.render(lines_str, False, BLACK)
        self.screen.blit(score_text, (GRID_WIDTH + 20, 60))
        self.screen.blit(level_text, (GRID_WIDTH + 20, 100))
        # self.screen.blit(lines_text, (GRID_WIDTH + 20, 140))

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
        if self.new_high:
            lines.append(("Congrats, New High Score!", "#ffd700"))  # Gold
        lines.append(("High Scores:", "white"))
        for initials, score in self.high_scores:
            # Ensure score is formatted as six digits
            lines.append((f"{initials} {score:06d}", "#00bfff"))  # Cyan
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
            if not self.high_scores_updated:
                self.high_scores, self.new_high = self.update_high_scores(self.score)
                self.high_scores_updated = True
            self.display_game_over()
        elif self.current_piece.locked:
            self.clear_lines()
            self.new_piece()



