'''
Physics related components and systems
'''
import esper

from dataclasses import dataclass
from typing import Any

from pygame import error


@dataclass
class Position:
    x: float
    y: float


@dataclass
class Velocity:
    dx: float
    dy: float


@dataclass
class Acceleration:
    ax: float
    ay: float


class MovementSystem(esper.Processor):
    def process(self, *args: Any, **kwargs: Any) -> None:
        if "dt" not in kwargs:
            raise error("no time difference found")
        dt = kwargs["dt"]
        for entity, (pos, vel) in esper.get_components(Position, Velocity):
            pos.x += vel.dx * dt
            pos.y += vel.dy * dt

        for entity, (vel, acl) in esper.get_components(Velocity, Acceleration):
            vel.dx += acl.ax * dt
            vel.dy += acl.ay * dt
