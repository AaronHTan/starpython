import esper
from starpython.physics import Position
from starpython.gameplay import Player
from .generation import WorldGenerator


class GenerationSystem(esper.Processor):
    def __init__(self, world_generator: WorldGenerator):
        self.world_generator = world_generator
        self.initialized = False
        
    def process(self, dt: float = 0):
        for ent, (pos, player) in esper.get_components(Position, Player):
            if not self.initialized:
                self.world_generator.initialize_world(pos.x, pos.y)
                self.initialized = True
            else:
                self.world_generator.update(pos.x, pos.y)