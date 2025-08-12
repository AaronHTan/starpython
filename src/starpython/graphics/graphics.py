''':wq
graphics processing for various sprites
'''
import pygame
import esper

from dataclasses import dataclass, field
from typing import Any

from starpython.physics import Position


@dataclass
class Sprite:
    image: pygame.Surface
    rect: pygame.Rect = field(init=False)
    layer: int = 0

    def __post_init__(self):
        self.rect = self.image.get_rect()


class RenderSystem(esper.Processor):
    def __init__(self, screen: pygame.Surface, entity: int) -> None:
        super().__init__()
        self.screen = screen
        self.entity = entity

    def process(self, *args: Any, **kwargs: Any) -> None:
        player_position = esper.component_for_entity(self.entity, Position)
        window_size = pygame.display.get_window_size()
        
        camera_offset_x = window_size[0] / 2 - player_position.x
        camera_offset_y = window_size[1] / 2 - player_position.y
        
        for _, (sprite, position) in esper.get_components(Sprite, Position):
            sprite.rect.x = int(position.x + camera_offset_x)
            sprite.rect.y = int(position.y + camera_offset_y)
            self.screen.blit(sprite.image, sprite.rect)
