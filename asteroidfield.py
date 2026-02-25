import pygame
import random
from asteroid import Asteroid
from constants import *


# Manager object that periodically spawns asteroids from random screen edges.
# Extends Sprite directly (not CircleShape) since it has no position or visual of its own.
class AsteroidField(pygame.sprite.Sprite):
    # Each entry defines one screen edge as [inward_direction_vector, spawn_position_fn].
    # The direction vector points toward the center of the screen (the default travel direction).
    # The lambda takes a 0–1 random float and returns a spawn point just off that edge.
    edges = [
        [
            pygame.Vector2(1, 0),                                            # left edge → travel right
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),                                           # right edge → travel left
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),                                            # top edge → travel down
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),                                           # bottom edge → travel up
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0

    def spawn(self, radius, position, velocity):
        # Instantiate an asteroid; it auto-joins `asteroids`, `updatable`, and `drawable` groups.
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def update(self, dt):
        self.spawn_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE_SECONDS:
            self.spawn_timer = 0

            # Pick a random edge, then randomise spawn position, speed, size tier, and a ±30° heading jitter.
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)