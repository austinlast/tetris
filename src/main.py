import pygame
from game import screen, new_piece, draw_grid, draw_piece, side_panel, current_piece
from settings import BLACK

def main():
    running = True
    clock = pygame.time.Clock()
    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_piece()
        side_panel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)

        pygame.display.flip()
        # clock.tick(60)  

    pygame.quit()

if __name__ == '__main__':
    main()
