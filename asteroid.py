import pygame
from circleshape import CircleShape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random

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
    
    def split(self):
        # Kill the asteroid that was shot before checking if it can split
        self.kill() 

        # Check if the asteroid is already at the smallest size. If so, it doesn't split
        if self.radius <= ASTEROID_MIN_RADIUS:
            return True  # terminal kill → award score

        # Split the asteroid into two smaller asteroids with a random vector and speed them up.
        log_event("asteroid_split")
        random_angle = random.uniform(20, 50)
        first_asteroid_vector = self.velocity.rotate(random_angle)
        second_asteroid_vector = self.velocity.rotate(random_angle * -1)
        new_radius = self.radius - ASTEROID_MIN_RADIUS
        asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
        asteroid1.velocity = first_asteroid_vector * 1.2
        asteroid2.velocity = second_asteroid_vector * 1.2
