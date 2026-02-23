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
- **`constants.py`** — All tunable values (screen size 1280×720, player radius, speeds, etc.)
- **`logger.py`** — Frame-by-frame game state logger; introspects the call stack to extract sprite state, writes JSONL to `game_state.jsonl` (stops after 16s)

### Adding New Game Entities

1. Create a class inheriting from `CircleShape`
2. Implement `draw(self)` and `update(self, dt)`
3. Set `MyClass.containers = (updatable, drawable)` before instantiation in `main.py`

The project currently has player movement/rotation but no asteroids, bullets, or collision detection yet.
