import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, SHOT_RADIUS

# A bullet fired by the player: a small white circle that travels in a straight line.
# Velocity is set by Player.shoot() to match the player's facing direction and shoot speed.
class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        # Move in a straight line — no gravity or drag.
        self.position += self.velocity * dt