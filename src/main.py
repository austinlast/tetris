import pygame
from game import screen, new_piece, draw_grid, draw_piece, side_panel, current_piece
from settings import BLACK

FALL_EVENT = pygame.USEREVENT + 1

def main():
    running = True
    clock = pygame.time.Clock()
    drop_speed = 1000  # milliseconds

    pygame.time.set_timer(FALL_EVENT, drop_speed)
    pygame.key.set_repeat(200, 50)

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_piece()
        side_panel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    current_piece.move(0, 1)
            elif event.type == FALL_EVENT:
                current_piece.move(0, 1)

        pygame.display.flip()
        clock.tick(60)  

    pygame.quit()

if __name__ == '__main__':
    main()
