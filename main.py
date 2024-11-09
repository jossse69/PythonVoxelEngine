from settings import *
import moderngl as mgl
import pygame as pg
import sys
from shader_program import ShaderProgram
from scene import Scene
from player import Player
from textures import Textures
from ui_manager import UiManager

class Game:
    def __init__(self):
        pg.init()
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        pg.display.gl_set_attribute(pg.GL_DEPTH_SIZE, 24)

        self.screen = pg.display.set_mode(WIN_RES, pg.OPENGL | pg.DOUBLEBUF)
        self.ctx = mgl.create_context()

        self.ctx.enable(mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)
        self.ctx.gc_mode = 'auto'

        self.clock = pg.time.Clock()
        self.delta_time = 0
        self.time = 0
        self.running = True

        pg.event.set_grab(True)
        pg.mouse.set_visible(False)

        pg.display.set_caption("Python Voxel Game (Loading... Be a patient pickle!)")

        self.on_init()

    def on_init(self):
        self.textures = Textures(self)
        self.player = Player(self)
        self.shader_program = ShaderProgram(self)
        self.scene = Scene(self)
        self.ui_manager = UiManager(self)


    def update(self):
        self.player.update()
        self.shader_program.update()
        self.scene.update()
        self.ui_manager.update()

        self.delta_time = self.clock.tick()
        self.time = pg.time.get_ticks() * 0.001
        pg.display.set_caption("Python Voxel Game (FPS: " + str(round(self.clock.get_fps())) + ")")


    def render(self):
        self.ctx.clear(BG_COLOR[0], BG_COLOR[1], BG_COLOR[2])
        self.scene.render()
        self.ui_manager.render()
        pg.display.flip()

    def handle_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.running = False
            self.player.handle_event(event=event)


    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        pg.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()