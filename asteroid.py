import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH

# A single asteroid: a white wireframe circle that drifts at a constant velocity.
# Radius is set by AsteroidField at spawn time based on the asteroid's size tier (kind 1–3).
class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # Move in a straight line — velocity is assigned by AsteroidField at spawn time.
        self.position += self.velocity * dt
    
