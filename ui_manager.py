from settings import *
from ui_element import UiElement

class UiManager:
    def __init__(self, game):
        self.game = game
        self.vertex_data = np.array([], dtype="float32")
        self.ui_elements = []
        self.ui_elements.append(UiElement(50, 50, 100, 100, [0, 0, 1, 1])) # example ui element
        self.build_ui()
        
        self.vbo_format = "3f 2f"
        self.format_size = sum(int(fmt[:1]) for fmt in self.vbo_format.split())
        self.attrs = ("in_position", "uv")
        self.shader_program = self.game.shader_program.ui
        self.vao = self.get_vao()


    def build_ui(self):
        vertex_positions = []
        uvs = []
        for ui_element in self.ui_elements:
            vertex_positions.extend(ui_element.get_vertex_data())
            uvs.extend(ui_element.get_uv_data())

        self.vertex_data = np.hstack([vertex_positions, uvs], dtype="float32")
        print(self.vertex_data)

    def render(self):
        self.vao.render()

    def update(self):
        for ui_element in self.ui_elements:
            ui_element.update()

    def get_vao(self):
        ctx = self.game.ctx
        vbo = ctx.buffer(self.vertex_data)
        vao = ctx.vertex_array(self.shader_program, [(vbo, self.vbo_format, *self.attrs)], skip_errors=True)
        return vao