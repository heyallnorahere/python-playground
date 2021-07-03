from pyplayground.gameobject import GameObject
class Scene(GameObject):
    def __init__(self):
        super().__init__()
        self.frame_count = 0
    def update(self):
        self.frame_count += 1
        if self.frame_count % 10000 == 0:
            print("Frame count:", self.frame_count)
        super().update()
