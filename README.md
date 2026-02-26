# Asteroids

A recreation of the classic Asteroids arcade game built with Python and Pygame.

You pilot a spaceship through a field of drifting asteroids, shooting them down to survive as long as possible.

## Setup

Dependencies are managed with [`uv`](https://github.com/astral-sh/uv).

```bash
uv sync
```

## Running

```bash
python main.py
```

Requires Python 3.13+ and pygame 2.6.1 (installed via `uv sync`).

## Controls

| Key | Action |
|-----|--------|
| `W` | Thrust forward |
| `S` | Thrust backward |
| `A` | Rotate left |
| `D` | Rotate right |
| `SPACE` | Fire |

## Gameplay

- Shoot asteroids to destroy them — large asteroids split into two smaller, faster ones
- Asteroids that reach minimum size are destroyed outright when hit
- Flying into an asteroid ends the game

## Architecture

All game entities inherit from `CircleShape` (`circleshape.py`), which extends `pygame.sprite.Sprite`. Objects self-register into sprite groups via the `containers` class variable set before instantiation:

```python
Player.containers = (updatable, drawable)
player = Player(...)  # auto-joins both groups
```

The game loop calls `updatable.update(dt)` and `drawable.draw(screen)` each frame at 60 FPS using delta-time for frame-rate-independent movement.

### Key Files

| File | Purpose |
|------|---------|
| `main.py` | Game loop, sprite group setup, object instantiation |
| `circleshape.py` | Abstract base class for all entities |
| `player.py` | Player ship: rendering, rotation, WASD movement, rate-limited shooting |
| `asteroid.py` | Asteroid entity: drifts in a straight line, splits into two on hit |
| `asteroidfield.py` | Spawns asteroids of random size from random screen edges |
| `shot.py` | Bullet entity: travels in a straight line at `PLAYER_SHOOT_SPEED` |
| `constants.py` | All tunable values (screen size, speeds, radii, shoot cooldown) |
| `logger.py` | Frame-by-frame state logger (writes to `game_state.jsonl`) |

### Adding New Entities

1. Create a class inheriting from `CircleShape`
2. Implement `draw(self, screen)` and `update(self, dt)`
3. In `main.py`, set `MyClass.containers = (...)` before instantiating

> Manager/spawner objects (like `AsteroidField`) that aren't drawn can extend `pygame.sprite.Sprite` directly and only join `updatable`.

## Ideas for Expansion

| Idea | Description |
|------|-------------|
| **Scoring system** | Award points for destroying asteroids — more for smaller ones. Display score on screen and track a high score. |
| **Multiple lives & respawning** | Give the player 3 lives; respawn with brief invincibility after each death instead of immediately ending the game. |
| **Explosion effects** | Spawn particle fragments when an asteroid is destroyed to give hits visual feedback. |
| **Player acceleration** | Replace instant velocity with gradual thrust and drag so the ship feels more physics-driven. |
| **Screen wrapping** | When an object moves off one edge, have it reappear on the opposite side — the classic Asteroids feel. |
| **Background image** | Replace the black background with a starfield texture or parallax star layer. |
| **Weapon types** | Add alternative weapons: spread shot, laser beam, or a rapid-fire mode with reduced damage. |
| **Lumpy asteroids** | Render asteroids as irregular polygons rather than perfect circles for a more authentic retro look. |
| **Triangular ship hitbox** | Replace the player's circular collision boundary with a triangle that matches the visible ship shape. |
| **Shield power-up** | Collectible that grants temporary invincibility; visualised as a glowing ring around the ship. |
| **Speed power-up** | Collectible that temporarily increases thrust and top speed. |
| **Bombs** | A limited-use weapon that detonates after a short delay, destroying all asteroids within a radius. |
