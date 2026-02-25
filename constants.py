# Screen — pixels
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

# Player — sizes in pixels, speeds in pixels/second, turn speed in degrees/second
PLAYER_RADIUS = 20
LINE_WIDTH = 2           # stroke width used for all wireframe shapes
PLAYER_TURN_SPEED = 300  # degrees per second
PLAYER_SPEED = 200       # pixels per second
PLAYER_SHOOT_SPEED = 500 # pixels per second

# Asteroids — sizes in pixels, rate in seconds
ASTEROID_MIN_RADIUS = 20             # radius of the smallest asteroid (kind 1)
ASTEROID_KINDS = 3                   # size tiers; largest asteroid radius = MIN * KINDS
ASTEROID_SPAWN_RATE_SECONDS = 0.8    # one new asteroid spawned every 0.8 seconds
ASTEROID_MAX_RADIUS = ASTEROID_MIN_RADIUS * ASTEROID_KINDS

# Shots — size in pixels
SHOT_RADIUS = 5
