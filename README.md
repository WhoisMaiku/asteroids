# Asteroids

A recreation of the classic Asteroids arcade game built with Python and Pygame.

You pilot a spaceship through a field of drifting asteroids, navigating to survive as long as possible.

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
| `player.py` | Player ship: rendering, rotation, WASD movement |
| `asteroid.py` | Asteroid entity |
| `asteroidfield.py` | Spawns asteroids at random screen edges |
| `constants.py` | All tunable values (screen size, speeds, radii) |
| `logger.py` | Frame-by-frame state logger (writes to `game_state.jsonl`) |

### Adding New Entities

1. Create a class inheriting from `CircleShape`
2. Implement `draw(self, screen)` and `update(self, dt)`
3. In `main.py`, set `MyClass.containers = (...)` before instantiating
