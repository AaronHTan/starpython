'''
Handles inputs from events
'''
import pygame
import esper

from dataclasses import dataclass, field
from typing import Any

from starpython.physics import Acceleration
from starpython.gameplay import Player

@dataclass
class Input:
    key_just_pressed: set[int] = field(default_factory=set)
    key_just_released: set[int] = field(default_factory=set)


class InputSystem(esper.Processor):
    def process(self, *args: Any, **kwargs: Any) -> None:
        for entity, (inp, player, acl) in esper.get_components(Input, Player, Acceleration):
            if pygame.K_LEFT in inp.key_just_pressed:
                acl.ax -= 50
            if pygame.K_RIGHT in inp.key_just_pressed:
                acl.ax += 50
            if pygame.K_UP in inp.key_just_pressed:
                acl.ay -= 50
            if pygame.K_DOWN in inp.key_just_pressed:
                acl.ay += 50


