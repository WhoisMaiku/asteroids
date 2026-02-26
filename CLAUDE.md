# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Game

```bash
python main.py
```

Dependencies are managed with `uv`. To install:

```bash
uv sync
```

## Architecture

This is an Asteroids arcade game built with Pygame (Python 3.13, pygame 2.6.1).

### Core Pattern: Sprite Groups + Container Registration

The game uses Pygame's sprite group system. All drawable/updatable objects inherit from `CircleShape` (`circleshape.py`), which extends `pygame.sprite.Sprite`. Subclasses automatically register themselves into groups via the `containers` class variable set before instantiation in `main.py`:

```python
Player.containers = (updatable, drawable)
player = Player(...)  # auto-joins both groups
```

The game loop calls `updatable.update(dt)` and `drawable.draw(screen)` each frame.

### Key Files

- **`main.py`** — Game loop: initializes pygame, creates sprite groups, instantiates objects, runs 60 FPS loop with delta-time
- **`circleshape.py`** — Abstract base class for all game entities (position, velocity, radius; abstract `draw()` and `update(dt)`)
- **`player.py`** — Player spaceship: WASD controls, triangle rendering, rotation-based movement using `pygame.Vector2`
- **`asteroid.py`** — Asteroid entity: white circle that drifts in a straight line each frame
- **`asteroidfield.py`** — Spawner/manager (extends `pygame.sprite.Sprite` directly, not `CircleShape`); periodically spawns asteroids of random size from random screen edges; only joins `updatable`, not `drawable`
- **`shot.py`** — Bullet entity: small white circle fired by the player; travels in a straight line at `PLAYER_SHOOT_SPEED`; auto-registers into `shots` and `drawable`/`updatable` groups
- **`constants.py`** — All tunable values (screen size 1280×720, player radius, speeds, asteroid sizing/spawn rate, shot radius/speed, etc.)
- **`logger.py`** — Frame-by-frame game state logger; introspects the call stack to extract sprite state, writes JSONL to `game_state.jsonl` (stops after 16s)

### Adding New Game Entities

1. Create a class inheriting from `CircleShape`
2. Implement `draw(self)` and `update(self, dt)`
3. Set `MyClass.containers = (updatable, drawable)` before instantiation in `main.py`

> **Note:** Manager/spawner objects (like `AsteroidField`) that aren't themselves drawn can extend `pygame.sprite.Sprite` directly and only join `updatable`.

## Learning Style

Follow the Learning output style strictly:
- For tasks generating 20+ lines involving design decisions, business logic, or key algorithms: build the scaffolding, place a `TODO(human)` at the meaningful decision point, then present a **"Learn by Doing"** request — do NOT implement that section yourself.
- Always wrap code explanations in insight blocks before and after writing code.
- Wait for the human's implementation before proceeding after a Learn by Doing request.

### Current State

- Player movement and rotation (WASD)
- Asteroids spawning from screen edges via `AsteroidField`
- Shooting mechanic: SPACE fires bullets (`Shot` instances) in the player's facing direction
- Collision detection: asteroid–player collision ends the game (`sys.exit()`)
- Still to add: shot–asteroid collision (split/destroy asteroids), scoring, lives/respawn, game-over screen
