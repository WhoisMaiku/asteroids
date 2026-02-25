import pygame
import sys
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()

    # Sprite groups control which objects participate in each phase of the game loop.
    # Objects register themselves into these groups via their class's `containers` variable.
    updatable = pygame.sprite.Group()   # receives update(dt) calls each frame
    drawable = pygame.sprite.Group()    # receives draw(screen) calls each frame
    asteroids = pygame.sprite.Group()   # tracked separately for collision detection
    shots = pygame.sprite.Group()       # tracked separately for shot-asteroid collision detection

    # Register groups before instantiation and auto-joins the object into whichever groups are listed there.
    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)  # field only needs update; it spawns drawables itself
    Shot.containers = (shots, drawable, updatable)

    # Spawn the asteroid field and the player at the center of the screen
    asteroid_field = AsteroidField()
    player = Player(x = (SCREEN_WIDTH / 2), y = (SCREEN_HEIGHT /2))

    clock = pygame.time.Clock()
    dt = 0  # delta-time in seconds; 0 on the first frame

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print (f"Screen width: {SCREEN_WIDTH}")
    print (f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Main game loop — runs at 60 FPS
    while True:
        log_state()  # record frame state to game_state.jsonl (stops after 16s)

        # Pump the event queue; exit cleanly when the window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # Clear the previous frame
        screen.fill("black")

        # Advance all game objects by the elapsed time since the last frame
        updatable.update(dt)

        for ast in asteroids:
            if ast.collides_with(player):
                log_event("player_hit")
                print("Game Over!")
                sys.exit()

        # Draw every visible object onto the screen surface
        for obj in drawable:
            obj.draw(screen)

        # Push the completed frame to the display
        pygame.display.flip()

        # tick(60) caps the loop at 60 FPS and returns ms elapsed; divide for seconds
        dt = (clock.tick(60) / 1000)

if __name__ == "__main__":
    main()
