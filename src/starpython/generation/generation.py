import pygame
import esper
import random
import math
from typing import Tuple, List, Set

from starpython.physics import Position
from starpython.graphics import Sprite


class TerrainGenerator:
    def __init__(self, chunk_size: int = 200, seed: int = None):
        self.chunk_size = chunk_size
        self.seed = seed if seed is not None else random.randint(0, 10000)
        random.seed(self.seed)
        self.generated_chunks: Set[Tuple[int, int]] = set()
        
    def get_chunk_coords(self, x: float, y: float) -> Tuple[int, int]:
        chunk_x = int(x // self.chunk_size)
        chunk_y = int(y // self.chunk_size)
        return (chunk_x, chunk_y)
    
    def generate_terrain_chunk(self, chunk_x: int, chunk_y: int):
        if (chunk_x, chunk_y) in self.generated_chunks:
            return
            
        self.generated_chunks.add((chunk_x, chunk_y))
        
        base_x = chunk_x * self.chunk_size
        base_y = chunk_y * self.chunk_size
        
        colors = [(100, 100, 100), (150, 150, 150), (80, 80, 80)]
        
        num_objects = random.randint(3, 8)
        for _ in range(num_objects):
            obj_entity = esper.create_entity()
            
            size = random.randint(15, 30)
            obj_surface = pygame.Surface((size, size))
            obj_surface.fill(random.choice(colors))
            
            obj_x = base_x + random.uniform(0, self.chunk_size)
            obj_y = base_y + random.uniform(0, self.chunk_size)
            
            esper.add_component(obj_entity, Position(x=obj_x, y=obj_y))
            esper.add_component(obj_entity, Sprite(image=obj_surface))


class EntityGenerator:
    def __init__(self, spawn_radius: float = 1000):
        self.spawn_radius = spawn_radius
        self.spawned_entities: List[int] = []
        
    def generate_decorative_entities(self, center_x: float, center_y: float, count: int = 15):
        colors = [(255, 0, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]
        
        for _ in range(count):
            obj_entity = esper.create_entity()
            self.spawned_entities.append(obj_entity)
            
            obj_surface = pygame.Surface((20, 20))
            obj_surface.fill(random.choice(colors))
            
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(50, self.spawn_radius)
            obj_x = center_x + distance * math.cos(angle)
            obj_y = center_y + distance * math.sin(angle)
            
            esper.add_component(obj_entity, Position(x=obj_x, y=obj_y))
            esper.add_component(obj_entity, Sprite(image=obj_surface))
    
    def clear_entities(self):
        for entity_id in self.spawned_entities:
            try:
                esper.delete_entity(entity_id)
            except KeyError:
                pass
        self.spawned_entities.clear()


class WorldGenerator:
    def __init__(self, generation_radius: float = 600, chunk_size: int = 200):
        self.generation_radius = generation_radius
        self.terrain_gen = TerrainGenerator(chunk_size=chunk_size)
        self.entity_gen = EntityGenerator()
        self.last_player_pos = None
        self.update_threshold = chunk_size / 4
        
    def initialize_world(self, player_x: float, player_y: float):
        self.generate_area_around_player(player_x, player_y)
        self.entity_gen.generate_decorative_entities(player_x, player_y, count=15)
        self.last_player_pos = (player_x, player_y)
        
    def update(self, player_x: float, player_y: float):
        if self.last_player_pos is None:
            self.initialize_world(player_x, player_y)
            return
            
        dx = player_x - self.last_player_pos[0]
        dy = player_y - self.last_player_pos[1]
        distance_moved = math.sqrt(dx * dx + dy * dy)
        
        if distance_moved > self.update_threshold:
            self.generate_area_around_player(player_x, player_y)
            self.last_player_pos = (player_x, player_y)
    
    def generate_area_around_player(self, player_x: float, player_y: float):
        current_chunk = self.terrain_gen.get_chunk_coords(player_x, player_y)
        
        chunks_to_generate = int(self.generation_radius / self.terrain_gen.chunk_size) + 1
        
        for dx in range(-chunks_to_generate, chunks_to_generate + 1):
            for dy in range(-chunks_to_generate, chunks_to_generate + 1):
                chunk_x = current_chunk[0] + dx
                chunk_y = current_chunk[1] + dy
                
                chunk_center_x = (chunk_x + 0.5) * self.terrain_gen.chunk_size
                chunk_center_y = (chunk_y + 0.5) * self.terrain_gen.chunk_size
                distance = math.sqrt((chunk_center_x - player_x) ** 2 + 
                                   (chunk_center_y - player_y) ** 2)
                
                if distance <= self.generation_radius:
                    self.terrain_gen.generate_terrain_chunk(chunk_x, chunk_y)