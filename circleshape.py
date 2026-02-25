import pygame

# Abstract base class for all circular game entities (player, asteroids, shots).
# Subclasses inherit position/velocity/radius and must implement draw() and update().
class CircleShape(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        # If `containers` is set on the subclass before instantiation, pygame auto-registers
        # this object into those sprite groups (e.g. updatable, drawable) on creation.
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2(0, 0)
        self.radius = radius

    def draw(self, screen):
        # Subclasses must override — called each frame to render this object.
        pass

    def update(self, dt):
        # Subclasses must override — called each frame with seconds elapsed since last frame.
        pass

    def collides_with(self, other):
        # Circle-circle collision: true when the distance between centers is less than the sum of radii.
        distance = self.position.distance_to(other.position)
        radii = self.radius + other.radius

        if distance <= radii:
            return True
        return False