import random
from settings import WIDTH, HEIGHT, SHAPES, grid, COLORS, BLOCK_TEXTURES


class Piece:
    def __init__(self):
        self.label, self.shape = random.choice(SHAPES)
        self.color = max(max(row) for row in self.shape)
        self.x = WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.locked = False

    def move(self, dir_x, dir_y):
        """
            This function Is what helps move the pieces side to side (x to y).

            Parameters:
                dir_x (int): The x movement
                dir_y (int): The y movement

            Returns:
                None
        """
        if not self.is_valid(dir_x, dir_y):
            self.x += dir_x
            self.y += dir_y
        elif dir_y == 1:
            self.stop()

    def stop(self):
        """
            This function will lock the piece in place if it is unable to move further.

            Parameters:
                None

            Returns:
                None
        """
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    grid[self.y + i][self.x + j] = BLOCK_TEXTURES[str(self.color)]
        self.locked = True

    def is_valid(self, dir_x, dir_y):
        """
            This function Helps determine if the move your making is valid.

            Parameters:
                dir_x (int): The x movement
                dir_y (int): The y movement

            Returns:
                Boolean: True if the move is valid, False if not
        """
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
        """
            This function allows the pieces to be rotated by hitting the up arrow.

            Parameters:
                None

            Returns:
                None
        """
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
                        return

    def rotate_ccw(self):
        """
            This function allows the pieces to be rotated counter clockwise.

            Parameters:
                None

            Returns:
                None
        """
        old_shape = self.shape
        self.shape = [list(row) for row in zip(*self.shape)][::-1]
        for i, row in enumerate(self.shape):
            for j, cell in enumerate(row):
                if cell:
                    new_x = self.x + j
                    new_y = self.y + i
                    # Check for out-of-bounds or collision
                    if new_x < 0 or new_x >= WIDTH or new_y >= HEIGHT:
                        self.shape = old_shape
                        return
                    if new_y >= 0 and grid[new_y][new_x] != 0:
                        self.shape = old_shape
                        return

    def instant_drop(self):
        """
            Instantly moves the current piece to the lowest valid position on the board.

            Parameters:
                None

            Returns:
                None
        """ 
        while not self.is_valid(0, 1):
            self.y += 1
        self.stop()     
