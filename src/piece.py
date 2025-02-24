import random
from settings import WIDTH, HEIGHT, SHAPES, grid, COLORS

class Piece:
    def __init__(self):
        self.label, self.shape = random.choice(SHAPES)
        self.color = max(max(row) for row in self.shape)
        self.x = WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0

    def move(self, dir_x, dir_y):
        if not self.is_valid(dir_x, dir_y):
            self.x += dir_x
            self.y += dir_y
        elif dir_y == 1:
            self.stop()

    def stop(self):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[self.y + i][self.x + j] = self.color
        # Import locally to avoid circular dependency
        from game import new_piece  
        new_piece()

    def is_valid(self, dir_x, dir_y):
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j + dir_x
                    new_y = self.y + i + dir_y
                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT:
                        return True
                    if new_y >= 0 and grid[new_y][new_x] != 0:
                        return True
        return False
    
    def rotate(self):
        prev_shape = self.shape
        self.shape = [list(row) for row in zip(*self.shape[::-1])]
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j
                    new_y = self.y + i
                    # Check for out-of-bounds or collision
                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT:
                        self.shape = prev_shape  
                        return
                    if new_y >= 0 and grid[new_y][new_x] != 0:
                        self.shape = prev_shape 

    def instant_drop(self):
        while not self.is_valid(0, 1):
            self.y += 1
        self.stop()