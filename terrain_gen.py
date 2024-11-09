from noise import noise2D, noise3D
from random import random
from settings import *

@njit
def get_height(x, y):
    island = 1 / (pow(0.0025 * math.hypot(x - CENTER_XZ, y - CENTER_XZ), 20) + 0.0001)
    island = min(island, 1)

    a1 = CENTER_Y / 3
    f1 = 0.005
    a2, a4, a8 = a1 * 0.5, a1 * 0.25, a1 * 0.125
    f2, f4, f8 = f1 * 2, f1 * 4, f1 * 8

    height = 0
    height += noise2D(x * f1, y * f1) * a1 + a1
    height += noise2D(x * f2, y * f2) * a2 - a2
    height += noise2D(x * f4, y * f4) * a4 + a4
    height += noise2D(x * f8, y * f8) * a8 - a8

    height *= island
    height = max(height, 1)

    return int(height)

@njit
def get_index(x, y, z):
    return x + CHUNK_SIZE * z + CHUNK_AREA * y

@njit
def set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height):
    voxel_id = AIR

    if wy < world_height - 1:
        if (noise3D(wx * 0.09, wy * 0.09, wz * 0.09) > 0 and noise2D(wx * 0.1, wz * 0.1) * 3 + 3 < wy < world_height - 10):
            voxel_id = AIR
        else:
            voxel_id = STONE
    else:
        rng = int(7 * random())
        ry = wy - rng

        if STONE_LVL <= ry < world_height:
            voxel_id = STONE
        elif DIRT_LVL <= ry < STONE_LVL:
            voxel_id = DIRT
        elif GRASS_LVL <= ry < DIRT_LVL:
            voxel_id = GRASS
        else:
            voxel_id = SAND

    voxels[get_index(x, y, z)] = voxel_id

    if wy < DIRT_LVL:
        place_tree(voxels, x, y, z, voxel_id)

@njit
def place_tree(voxels, x, y, z, voxel_id):
    rng = random()

    if y + TREE_HEIGHT >= CHUNK_SIZE:
        return None
    if x - TREE_H_WIDTH < 0 or x + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    if z - TREE_H_WIDTH < 0 or z + TREE_H_WIDTH >= CHUNK_SIZE:
        return None
    
    if voxel_id == GRASS and rng < TREE_CHANCE:
        voxels[get_index(x, y, z)] = DIRT

        m = 0
        for n, iy in enumerate(range(TREE_H_HEIGHT, TREE_HEIGHT - 1)):
            k = iy % 2
            rng = int(random() * 2)
            for ix in range(-TREE_H_WIDTH + m, TREE_H_WIDTH - m * rng):
                for iz in range(-TREE_H_WIDTH + m * rng, TREE_H_WIDTH - m):
                    if (ix + iz) % 4:
                        voxels[get_index(x + ix + k, y + iy, z + iz + k)] = LEAVES
            m += 1 if n > 0 else 3 if n > 1 else 0

        for iy in range(1, TREE_HEIGHT - 2):
            voxels[get_index(x, y + iy, z)] = LOG

        voxels[get_index(x, y + TREE_HEIGHT - 2, z)] = LEAVES