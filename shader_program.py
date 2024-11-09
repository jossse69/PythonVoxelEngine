from settings import *

class ShaderProgram:
    def __init__(self, game):
        self.game = game
        self.ctx = game.ctx
        self.player = game.player
        #---Shaders---#
        self.chunk = self.get_program("chunk")
        self.water = self.get_program("water")
        self.voxel_marker = self.get_program("voxel_marker")
        self.ui = self.get_program("ui")
        #------#
        self.set_unifroms_on_init()

    def set_unifroms_on_init(self):
        self.chunk["projection_matrix"].write(self.player.projection_matrix)
        self.chunk["model_matrix"].write(glm.mat4())
        self.chunk["texture_array_id_0"] = 1

        self.water['projection_matrix'].write(self.player.projection_matrix)
        self.water['water_area'] = WATER_AREA
        self.water['water_line'] = WATER_LINE

        self.voxel_marker["projection_matrix"].write(self.player.projection_matrix)
        self.voxel_marker["model_matrix"].write(glm.mat4())
        self.voxel_marker["texture_id_0"] = 0

        self.ui["texture_array_id_1"] = 2

    def update(self):
        self.chunk["view_matrix"].write(self.player.view_matrix)
        self.voxel_marker["view_matrix"].write(self.player.view_matrix)
        self.water["view_matrix"].write(self.player.view_matrix)

    def get_program(self, shader_name):
        with open("shaders/" + shader_name + ".vert") as file:
            vertex_shader = file.read()

        with open("shaders/" + shader_name + ".frag") as file:
            fragment_shader = file.read()

        return self.ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)