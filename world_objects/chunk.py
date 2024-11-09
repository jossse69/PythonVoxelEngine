from settings import *
from meshes.chunk_mesh import ChunkMesh
from terrain_gen import *

class Chunk:
    def __init__(self, world, position):
        self.game = world.game
        self.world = world
        self.position = position
        self.model_matrix = self.get_model_matrix()
        self.voxels:np.array = None
        self.mesh:ChunkMesh = None
        self.is_empty = True
        self.center = (glm.vec3(self.position) + 0.5) * CHUNK_SIZE
        self.is_on_frustum = self.game.player.frustum.is_on_frustum

    def get_model_matrix(self):
        m_model = glm.translate(glm.mat4(), glm.vec3(self.position) * CHUNK_SIZE)
        return m_model

    def set_uniform(self):
        self.mesh.shader_program["model_matrix"].write(self.model_matrix)

    def build_mesh(self):
        self.mesh = ChunkMesh(self)

    def render(self):
        if not self.is_empty and self.is_on_frustum(self):
            self.set_uniform()
            self.mesh.render()

    def build_voxels(self):
        voxels = np.zeros(CHUNK_VOLUME, dtype=np.uint8)
        
        cx, cy, cz = glm.vec3(self.position) * CHUNK_SIZE
        self.generate_terrain(voxels, cx, cy, cz)

        if np.any(voxels):
            self.is_empty = False

        return voxels
    
    @staticmethod
    @njit
    def generate_terrain(voxels, cx, cy, cz):
        
        for x in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                wx = cx + x
                wz = cz + z
                world_height = get_height(wx, wz)
                local_height = min(world_height - cy, CHUNK_SIZE)


                for y in range(local_height):
                    wy = cy + y
                    set_voxel_id(voxels, x, y, z, wx, wy, wz, world_height)