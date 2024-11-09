from settings import *
from frustum import Frustum

class Camera:
    def __init__(self, position, yaw, pitch):
        self.position = glm.vec3(position)
        self.yaw = glm.radians(yaw)
        self.pitch = glm.radians(pitch)

        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.right = glm.vec3(1.0, 0.0, 0.0)

        self.view_matrix = glm.mat4()
        self.projection_matrix = glm.perspective(V_FOV, ASPECT_RATIO, NEAR, FAR)
        self.frustum = Frustum(self)

    def update(self):
        self.update_vectors()
        self.update_view_matrix()

    def update_view_matrix(self):
        self.view_matrix = glm.lookAt(self.position, self.position + self.front, self.up)

    def update_vectors(self):
        self.front.x = glm.cos(self.yaw) * glm.cos(self.pitch)
        self.front.y = glm.sin(self.pitch)
        self.front.z = glm.sin(self.yaw) * glm.cos(self.pitch)

        self.front = glm.normalize(self.front)
        self.right = glm.normalize(glm.cross(self.front, glm.vec3(0.0, 1.0, 0.0)) )
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def rotate_pitch(self, delta_y):
        self.pitch -= delta_y
        self.pitch = glm.clamp(self.pitch, -PITCH_MAX, PITCH_MAX)

    def rotate_yaw(self, delta_x):
        self.yaw += delta_x

    def move_left(self, vel):
        self.position -= self.right * vel

    def move_right(self, vel):
        self.position += self.right * vel

    def move_up(self, vel):
        self.position += self.up * vel

    def move_down(self, vel):
        self.position -= self.up * vel

    def move_forward(self, vel):
        self.position += self.front * vel

    def move_backward(self, vel):
        self.position -= self.front * vel