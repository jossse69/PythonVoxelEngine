import pygame as pg
from camera import Camera
from settings import *

class Player(Camera):
    def __init__(self, game, position=PLAYER_POS, yaw=270, pitch=0):
        self.game = game
        super().__init__(position, yaw, pitch)

    def update(self):
        self.keyboard_conrols()
        self.mouse_controls()
        return super().update()

    def mouse_controls(self):
        mouse_dx, mouse_dy = pg.mouse.get_rel()
        if mouse_dx:
            self.rotate_yaw(mouse_dx * MOUSE_SENSITIVITY)
        if mouse_dy:
            self.rotate_pitch(mouse_dy * MOUSE_SENSITIVITY)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            voxel_handler = self.game.scene.world.voxel_handler
            if event.button == 1:
                voxel_handler.set_voxel()
            if event.button == 3:
                voxel_handler.switch_mode()

    def keyboard_conrols(self):
        key_state = pg.key.get_pressed()
        vel = PLAYER_SPEED * self.game.delta_time
        if key_state[pg.K_w]:
            self.move_forward(vel)
        if key_state[pg.K_s]:
            self.move_backward(vel)
        if key_state[pg.K_a]:
            self.move_left(vel)
        if key_state[pg.K_d]:
            self.move_right(vel)
        if key_state[pg.K_SPACE]:
            self.move_up(vel)
        if key_state[pg.K_LSHIFT]:
            self.move_down(vel)