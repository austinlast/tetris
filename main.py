import pygame
from game import Game
from settings import BLACK, grid, WIDTH, HEIGHT

FALL_EVENT = pygame.USEREVENT + 1

def main():
    #Initializes variables
    running = True
    clock = pygame.time.Clock()
    drop_speed = 1000

    pygame.time.set_timer(FALL_EVENT, drop_speed)
    pygame.key.set_repeat(200, 50)

    game_instance = Game()

    # Starts gameplay loop
    while running:
        game_instance.update()

        #Handles all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == FALL_EVENT and not game_instance.game_over:
                game_instance.current_piece.move(0, 1)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    for i in range(HEIGHT):
                        grid[i] = [0] * WIDTH
                    game_instance = Game()
                elif event.key == pygame.K_p:
                    game_instance.paused = not game_instance.paused  
                elif not game_instance.game_over and not game_instance.paused:
                    if event.key == pygame.K_LEFT:
                        game_instance.current_piece.move(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game_instance.current_piece.move(1, 0)
                    elif event.key == pygame.K_DOWN:
                        game_instance.current_piece.move(0, 1)
                    elif event.key == pygame.K_UP or event.key == pygame.K_z:
                        game_instance.current_piece.rotate()
                    elif event.key == pygame.K_x:
                        game_instance.current_piece.rotate_ccw()
                    elif event.key == pygame.K_SPACE:
                        game_instance.current_piece.instant_drop()
                    elif event.key == pygame.K_c:
                        game_instance.hold_current_piece()

        # Updates the display after iteration
        pygame.display.flip()
        clock.tick(60)

    #Ends the game
    pygame.quit()

if __name__ == '__main__':
    main()
