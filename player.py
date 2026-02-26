import pygame
from circleshape import CircleShape
from constants import PLAYER_RADIUS, LINE_WIDTH, PLAYER_TURN_SPEED, PLAYER_SPEED, PLAYER_SHOOT_SPEED, PLAYER_SHOOT_COOLDOWN_SECONDS
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0  # degrees; 0 points down, increases clockwise
        self.shot_cooldown_timer = 0 

    def triangle(self):
        # Computes the 3 world-space vertices of the ship triangle from the current rotation.
        # `forward` is the nose direction; `right` is perpendicular for the two wing tips.
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius           # nose
        b = self.position - forward * self.radius - right  # left wing
        c = self.position - forward * self.radius + right  # right wing
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        # Adjusts heading by PLAYER_TURN_SPEED degrees per second; negative dt rotates left.
        self.rotation += (PLAYER_TURN_SPEED * dt)

    def update(self, dt):
        # Poll keyboard state each frame; all movement is dt-scaled for frame-rate independence.
        keys = pygame.key.get_pressed()
        self.shot_cooldown_timer -= dt

        if keys[pygame.K_w]:
            self.move(dt)

        if keys[pygame.K_s]:
            self.move((dt * -1))

        if keys[pygame.K_a]:
            self.rotate((dt * -1))

        if keys[pygame.K_d]:
            self.rotate(dt)

        if keys[pygame.K_SPACE]:
                self.shoot()

    def move(self, dt):
        # Rotate a downward unit vector by the player's heading to get the movement direction,
        # then scale by speed and elapsed time to get the frame displacement.
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        # Prevents the player from shooting continuously by returning whilst the cooldown is higher than 0
        if self.shot_cooldown_timer > 0:
            return
        self.shot_cooldown_timer = PLAYER_SHOOT_COOLDOWN_SECONDS

        # Spawn a shot at the player's position traveling in the current facing direction.
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = (pygame.Vector2(0,1).rotate(self.rotation) * PLAYER_SHOOT_SPEED)
