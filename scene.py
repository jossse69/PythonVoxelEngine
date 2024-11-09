from settings import *
import moderngl as mgl
from world import World
from world_objects.voxel_marker import VoxelMarker
from world_objects.water import Water

class Scene:
    def __init__(self, game):
        self.game = game
        self.world = World(self.game)
        self.water = Water(self.game)
        self.voxel_marker = VoxelMarker(self.world.voxel_handler)

    def update(self):
        self.world.update()
        self.voxel_marker.update()

    def render(self):
        self.world.render(self.game.player.position.x, self.game.player.position.y, self.game.player.position.z)

        self.game.ctx.disable(mgl.CULL_FACE)
        self.water.render()
        self.game.ctx.enable(mgl.CULL_FACE)

        self.voxel_marker.render()
