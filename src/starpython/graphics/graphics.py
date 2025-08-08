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
    def __init__(self, screen: pygame.Surface) -> None:
        super().__init__()
        self.screen = screen


    def process(self, *args: Any, **kwargs: Any) -> None:
        for entity, (sprite, position) in esper.get_components(Sprite, Position):
            sprite.rect.x = int(position.x)
            sprite.rect.y = int(position.y)
            self.screen.blit(sprite.image, (sprite.rect))
            sprite.rect.topleft
