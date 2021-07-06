from posixpath import realpath
from pyplayground.display import Display
from pyplayground.gameobject import GameObject
from pyplayground.image import Image
from pyplayground.components import TilesetComponent
import yaml
import os.path
def multiply_tuples(t1: tuple, t2: tuple):
    elements = []
    for index in range(len(t1)):
        elements.append(t1[index] * t2[index])
    return tuple(elements)
class TileDescriptor:
    def __init__(self, tile_position: tuple[int, int]):
        self.tile_position = tile_position
        # todo: add more fields later
class TileManager:
    def __init__(self, display: Display):
        self.display = display
        self.tiles = list[GameObject]()
        self.tileset = None
        self.tileset_path = None
        self.cell_size = (0, 0)
    def load(self, path: str):
        data = None
        with open(path, "r") as stream:
            try:
                data = yaml.load(stream, Loader=yaml.Loader)
            except yaml.YAMLError as exc:
                print(exc)
        if data == None:
            print("Could not load scene data; aborting...")
            exit(1)
        self.tileset_path = data["tileset"]
        real_tileset_path = os.path.realpath(os.path.join(os.path.dirname(path), self.tileset_path))
        self.cell_size = data["cell_size"]
        self.tileset = Image(real_tileset_path, self.display)
        # pyplayground expects tilesets to be 3x3
        self.tiles.clear()
        for descriptor in data["tiles"]:
            tile = GameObject(self.cell_size)
            tile.pos = multiply_tuples(self.cell_size, descriptor.tile_position)
            tile.add_component(TilesetComponent(self.tileset, self.cell_size, (0, 0)))
            self.tiles.append(tile)
    def update(self):
        # todo: cycle through each tile to determine which sprite to use
        pass
    def render(self, display: Display):
        for tile in self.tiles:
            tile.render(display)