from numba import njit
import numpy as np
import glm
import math

# Window resoluion
WIN_RES = glm.vec2(1600, 900)

# Background color
BG_COLOR = (204 / 255, 255 / 255, 255 / 255)

# World gen
SEED = 18

# Ray casting
MAX_RAY_DIST = 6

# Camera settings
ASPECT_RATIO = WIN_RES.x / WIN_RES.y
FOV_DEG = 60
V_FOV = glm.radians(FOV_DEG) # Vertical field of view
H_FOV = 2 * math.atan(math.tan(V_FOV / 2) * ASPECT_RATIO) # Horizontal field of view
NEAR = 0.1
FAR = 1000.0
PITCH_MAX = glm.radians(89.0)

# chunks
CHUNK_SIZE = 48
H_CHUNK_SIZE = CHUNK_SIZE // 2
CHUNK_AREA = CHUNK_SIZE ** 2
CHUNK_VOLUME = CHUNK_SIZE ** 3
CHUNK_SPHERE_RADIUS = H_CHUNK_SIZE * math.sqrt(3)

# World settings
WORLD_WIDTH, WORLD_HEIGHT = 20, 8 # in chunks
WORLD_D = WORLD_WIDTH
WORLD_AREA = WORLD_WIDTH * WORLD_D
WORLD_VOLUME = WORLD_AREA * WORLD_HEIGHT

# World center
CENTER_XZ = WORLD_WIDTH * H_CHUNK_SIZE
CENTER_Y = WORLD_HEIGHT * H_CHUNK_SIZE

# Player
PLAYER_SPEED = 0.005
PLAYER_ROT_SPEED = 0.003
PLAYER_POS = glm.vec3(CENTER_XZ, CENTER_Y / 3, CENTER_XZ)
MOUSE_SENSITIVITY = 0.002

# Voxel enum
AIR = 0
DIRT = 1
GRASS = 2
STONE = 3
SAND = 4
LOG = 5
LEAVES = 6
PLANKS = 7

# Terrain levels
SAND_LVL = 7
GRASS_LVL = 8
DIRT_LVL = 40
STONE_LVL = 50

# Tree spawning related settings
TREE_CHANCE = 0.02
TREE_WIDTH, TREE_HEIGHT = 4, 8
TREE_H_WIDTH, TREE_H_HEIGHT = TREE_WIDTH // 2, TREE_HEIGHT // 2

# water
WATER_LINE = 5.6
WATER_AREA = 5 * CHUNK_SIZE * WORLD_WIDTH