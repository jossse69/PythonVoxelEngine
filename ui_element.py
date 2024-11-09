from settings import *

class UiElement:
    def __init__(self, x, y, width, height, uvs):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.uvs = uvs

    def update(self):
        pass

    def get_vertex_data(self) -> np.ndarray:
        vertices = [
            (self.x, self.y, 0.0), (self.x + self.width, self.y, 0.0), (self.x + self.width, self.y + self.height, 0.0),
            (self.x, self.y, 0.0), (self.x + self.width, self.y + self.height, 0.0), (self.x, self.y + self.height, 0.0)
        ]
        vertex_data = np.hstack([vertices], dtype="float32")
        return vertex_data
    
    def get_uv_data(self) -> np.ndarray:
        uvs = [
            (self.uvs[0], self.uvs[1]), (self.uvs[2], self.uvs[1]), (self.uvs[2], self.uvs[3]),
            (self.uvs[0], self.uvs[1]), (self.uvs[2], self.uvs[3]), (self.uvs[0], self.uvs[3])
        ]
        return np.hstack([uvs], dtype="float32")