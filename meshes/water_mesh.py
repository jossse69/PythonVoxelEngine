from settings import *
from meshes.base_mesh import BaseMesh

class WaterMesh(BaseMesh):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.ctx = game.ctx
        self.shader_program = game.shader_program.water

        self.vbo_format = '3f'
        self.attrs = ('in_position',)
        self.vao = self.get_vao() 

    def get_vertex_data(self):
        vertices = [
            (0, 0, 0), (1, 0, 1), (1, 0, 0),
            (0, 0, 0), (0, 0, 1), (1, 0, 1)
        ]

        vertex_data = np.hstack([vertices], dtype=np.float32)
        return vertex_data