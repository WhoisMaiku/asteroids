import pygame
from constants import (
    SCREEN_WIDTH, SCREEN_HEIGHT, ASTEROID_SCORE,
    BUTTON_COLOUR, BUTTON_HOVER_COLOUR, BUTTON_TEXT_COLOUR, BUTTON_BORDER_COLOUR,
    GAMEOVER_TITLE_FONT_SIZE, GAMEOVER_SCORE_FONT_SIZE,
    BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_PADDING,
)
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
    AsteroidField()
    player = Player(x = (SCREEN_WIDTH / 2), y = (SCREEN_HEIGHT /2))

    score = 0
    game_state = "playing"
    final_score = 0

    font        = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 16)
    font_title  = pygame.font.Font("fonts/PressStart2P-Regular.ttf", GAMEOVER_TITLE_FONT_SIZE)
    font_score  = pygame.font.Font("fonts/PressStart2P-Regular.ttf", GAMEOVER_SCORE_FONT_SIZE)
    font_button = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 16)

    clock = pygame.time.Clock()
    dt = 0  # delta-time in seconds; 0 on the first frame

    print(f"Starting Asteroids with pygame version: {pygame.version.ver}")
    print (f"Screen width: {SCREEN_WIDTH}")
    print (f"Screen height: {SCREEN_HEIGHT}")

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Tears down all active sprites and re-creates the asteroid field and player,
    # returning the game to its initial state. Returns 0 to reset the score.
    def reset_game():
        nonlocal player
        updatable.empty()
        drawable.empty()
        asteroids.empty()
        shots.empty()
        Player.containers = (updatable, drawable)
        Asteroid.containers = (asteroids, updatable, drawable)
        AsteroidField.containers = (updatable)
        Shot.containers = (shots, drawable, updatable)
        AsteroidField()
        player = Player(x=(SCREEN_WIDTH / 2), y=(SCREEN_HEIGHT / 2))
        return 0  # reset score

    # Draws a single button: filled background (highlighted when hovered), a border outline,
    # and a text label centered inside the button area.
    def draw_button(surface, font, text, rect, hovered):
        if hovered:
            pygame.draw.rect(surface, BUTTON_HOVER_COLOUR, rect)
        else:
            pygame.draw.rect(surface, BUTTON_COLOUR, rect)
        pygame.draw.rect(surface, BUTTON_BORDER_COLOUR,rect, width=2)
        text_surf = font.render(text, True, BUTTON_TEXT_COLOUR)
        surface.blit(text_surf, text_surf.get_rect(center=rect.center))
        

    # Checks this frame's events for a left mouse click on either button.
    # Returns "try_again", "exit", or None if neither was clicked.
    def handle_game_over_input(mouse_pos, events, try_again_rect, exit_rect):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if try_again_rect.collidepoint(mouse_pos):
                    return "try_again"
                if exit_rect.collidepoint(mouse_pos):
                    return "exit"
        return None

    # Compute button rects once — centered horizontally, stacked vertically
    cx = SCREEN_WIDTH // 2
    try_again_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    try_again_rect.center = (cx, SCREEN_HEIGHT // 2 + 60)
    exit_rect = pygame.Rect(0, 0, BUTTON_WIDTH, BUTTON_HEIGHT)
    exit_rect.center = (cx, SCREEN_HEIGHT // 2 + 60 + BUTTON_HEIGHT + BUTTON_PADDING)

    # Main game loop — runs at 60 FPS
    while True:
        log_state()  # record frame state to game_state.jsonl (stops after 16s)

        events = list(pygame.event.get())
        for event in events:
            if event.type == pygame.QUIT:
                return

        # Clear the previous frame
        screen.fill("black")

        if game_state == "playing":
            # Advance all game objects by the elapsed time since the last frame
            updatable.update(dt)

            # Check if an asteroid is colliding with the player
            for ast in asteroids:
                if ast.collides_with(player):
                    log_event("player_hit")
                    final_score = score
                    game_state = "game_over"
                    break

                # Check if a shot is colliding with an asteroid and destroys it
                for shot in shots:
                    if shot.collides_with(ast):
                        log_event("asteroid_shot")
                        if ast.split():
                            score += ASTEROID_SCORE
                        shot.kill()

            # Draw every visible object onto the screen surface
            for obj in drawable:
                obj.draw(screen)

            # Render score overlay
            score_text = font.render(f"Score: {score}", True, "white")
            screen.blit(score_text, (10, 10))

        elif game_state == "game_over":
            mouse_pos = pygame.mouse.get_pos()

            title_surf = font_title.render("GAME OVER", True, "white")
            screen.blit(title_surf, title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80)))

            score_surf = font_score.render(f"Score: {final_score}", True, "white")
            screen.blit(score_surf, score_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

            draw_button(screen, font_button, "Try Again", try_again_rect, try_again_rect.collidepoint(mouse_pos))
            draw_button(screen, font_button, "Exit", exit_rect, exit_rect.collidepoint(mouse_pos))

            action = handle_game_over_input(mouse_pos, events, try_again_rect, exit_rect)
            if action == "try_again":
                score = reset_game()
                game_state = "playing"
            elif action == "exit":
                return

        # Push the completed frame to the display
        pygame.display.flip()

        # tick(60) caps the loop at 60 FPS and returns ms elapsed; divide for seconds
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
