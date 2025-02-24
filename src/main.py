import pygame
import game 
from settings import BLACK

FALL_EVENT = pygame.USEREVENT + 1

def main():
    running = True
    clock = pygame.time.Clock()
    drop_speed = 1000  # milliseconds

    # timer for slow and fast drop
    pygame.time.set_timer(FALL_EVENT, drop_speed)
    pygame.key.set_repeat(200, 50)

    while running:
        game.screen.fill(BLACK)
        game.draw_grid()
        game.draw_ghost_piece()
        game.draw_piece()
        game.side_panel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    game.current_piece.move(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    game.current_piece.move(1, 0)
                elif event.key == pygame.K_DOWN:
                    game.current_piece.move(0, 1)
                elif event.key == pygame.K_UP:
                    game.current_piece.rotate()
                elif event.key == pygame.K_SPACE:
                    game.current_piece.instant_drop()

            elif event.type == FALL_EVENT:
                game.current_piece.move(0, 1)

        pygame.display.flip()
        clock.tick(60)  

    pygame.quit()

if __name__ == '__main__':
    main()
