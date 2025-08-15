'''
Handles gameplay
'''

import pygame
import esper

from dataclasses import dataclass
from typing import Any


@dataclass
class Player:
    name: str = "Testing"


class GameplaySystem(esper.Processor):
    def process(self, *args: Any, **kwargs: Any) -> None:
        return
