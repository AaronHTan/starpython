'''
Main function to run starpython. Run it via python -m starpython
'''
import pygame
import esper


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    world = esper.switch_world("game")
    running = True

    while running:

        screen.fill((0, 0, 0))
        clock.tick(60)  # 60 FPS


def main():
    game_loop()
    return


if __name__ == "__main__":
    main()
