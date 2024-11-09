import pygame as pg
import moderngl as mgl

class Textures:
    def __init__(self, game):
        self.game = game
        self.ctx = game.ctx

        self.texture_0 = self.load("frame_voxel")
        self.texture_0.use(location=0)
        self.texture_array_0 = self.load("voxels", True)
        self.texture_array_0.use(location=1)
        self.texture_array_1 = self.load("ui_gfx", True)
        self.texture_array_1.use(location=2)

    def load(self, filename, is_texture_array=False, array_segments=3):
        texture = pg.image.load("assets/textures/" + filename + ".png")
        texture = pg.transform.flip(texture, True, False)

        if is_texture_array:
            num_layers = array_segments * texture.get_height() // texture.get_width()
            texture = self.game.ctx.texture_array(
                size=(texture.get_width(), texture.get_height() // num_layers, num_layers),
                components=4,
                data=pg.image.tostring(texture, "RGBA")
            )
        else:
            texture = self.ctx.texture(
                size=texture.get_size(),
                components=4,
                data=pg.image.tostring(texture, "RGBA", False)
            )
        texture.anisotropy = 32.0
        texture.build_mipmaps()
        texture.filter = (mgl.NEAREST, mgl.NEAREST)

        return texture