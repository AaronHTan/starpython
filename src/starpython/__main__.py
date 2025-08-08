'''
Main function to run starpython. Run it via python -m starpython
'''
import pygame
import esper

from starpython.physics import MovementSystem, Position, Velocity
from starpython.graphics import RenderSystem, Sprite
from starpython.input import Input, InputSystem
from starpython.gameplay import Player, GameplaySystem
from starpython.physics.physics import Acceleration


def game_loop():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Star Python")
    clock = pygame.time.Clock()
    esper.switch_world("game")
    running = True
    esper.add_processor(InputSystem(), priority=10)
    esper.add_processor(GameplaySystem(), priority=0)
    esper.add_processor(MovementSystem(), priority=5)
    esper.add_processor(RenderSystem(screen), priority=-10)

    # TEMPORARY: Create player entity for testing
    player_entity = esper.create_entity()
    key_just_pressed = set()
    key_just_released = set()

    # TEMPORARY: Simple colored rectangle as the player sprite
    player_surface = pygame.Surface((32, 32))
    player_surface.fill((0, 255, 0))  # Green square for the player

    # TEMPORARY: Add basic components to the player entity
    esper.add_component(player_entity, Position(x=400.0, y=300.0))
    esper.add_component(player_entity, Velocity(dx=50.0, dy=30.0))
    esper.add_component(player_entity, Acceleration(ax=0.0, ay=0.0))
    esper.add_component(player_entity, Sprite(image=player_surface))
    esper.add_component(player_entity, Player())
    esper.add_component(player_entity, Input(key_just_pressed=key_just_pressed, key_just_released=key_just_released))
    while running:

        key_just_pressed.clear()
        key_just_released.clear()
        dt = clock.tick(60) / 1000
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                key_just_pressed.add(event.key)

            elif event.type == pygame.KEYUP:
                key_just_released.add(event.key)

        screen.fill((0, 0, 0))
        esper.process(dt=dt)

        pygame.display.flip()


def main():
    game_loop()
    return


if __name__ == "__main__":
    main()
