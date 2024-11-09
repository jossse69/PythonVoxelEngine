from settings import *
from world_objects.chunk import Chunk
from voxel_handler import VoxelHandler

class World:
    def __init__(self, game):
        self.game = game
        self.chunks = [None for _ in range(WORLD_VOLUME)]
        self.voxels = np.empty([WORLD_VOLUME, CHUNK_VOLUME], dtype="uint8")
        self.build_chunks()
        self.build_chunk_mesh()
        self.voxel_handler = VoxelHandler(self)

    def build_chunks(self):
        for x in range(WORLD_WIDTH):
            for z in range(WORLD_WIDTH):
                for y in range(WORLD_HEIGHT):
                    chunk = Chunk(self, position=(x, y, z))

                    chunk_id = x + WORLD_WIDTH * z + WORLD_AREA * y
                    self.chunks[chunk_id] = chunk
                    self.voxels[chunk_id] = chunk.build_voxels()

                    chunk.voxels = self.voxels[chunk_id]



    def build_chunk_mesh(self):
        for chunk in self.chunks:
            chunk.build_mesh()

    def update(self):
        self.voxel_handler.update()

    def get_current_chunk(self, px, py, pz):
        # Calculate the chunk coordinates
        chunk_x = int(px // CHUNK_SIZE)
        chunk_y = int(py // CHUNK_SIZE)
        chunk_z = int(pz // CHUNK_SIZE)

        # Ensure the coordinates are within the world bounds
        chunk_x = max(0, min(chunk_x, WORLD_WIDTH - 1))
        chunk_y = max(0, min(chunk_y, WORLD_HEIGHT - 1))
        chunk_z = max(0, min(chunk_z, WORLD_WIDTH - 1))

        # Calculate the chunk ID
        chunk_id = chunk_x + WORLD_WIDTH * chunk_z + WORLD_AREA * chunk_y

        return self.chunks[chunk_id]

    def render(self, px, py, pz):
        player_pos = glm.vec3(px, py, pz)

        # Order chunks from farthest to nearest from the player
        farest_to_nearest_chunks = sorted(
            self.chunks,
            key=lambda chunk: glm.distance(player_pos, ((glm.vec3(*chunk.position) * CHUNK_SIZE) - glm.vec3(WORLD_WIDTH / 2, WORLD_HEIGHT / 2, WORLD_WIDTH / 2)) + glm.vec3(H_CHUNK_SIZE, H_CHUNK_SIZE, H_CHUNK_SIZE)),
            reverse=True
        )

        current_chunk = self.get_current_chunk(px, py, pz)

        farest_to_nearest_chunks.remove(current_chunk)

        # Render chunks in the sorted order
        for chunk in farest_to_nearest_chunks:
            chunk.render()

        current_chunk.render()
