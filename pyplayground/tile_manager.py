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
def subtract_tuples(t1: tuple, t2: tuple):
    elements = []
    for index in range(len(t1)):
        elements.append(t1[index] - t2[index])
    return tuple(elements)
class TileDescriptor:
    def __init__(self, tile_position: tuple[int, int]):
        self.tile_position = tile_position
        # todo: add more fields later
class TileListElement:
    def __init__(self, object: GameObject, tile_position: tuple[int, int]):
        self.object = object
        self.tile_position = tile_position
UP = 0b1000
DOWN = 0b0100
LEFT = 0b0010
RIGHT = 0b0001
# this function is going to be MUCH more complicated in the future, just a fair warning
def determine_tile_sprite(tiles: list[TileListElement], index: int) -> tuple[int, int]:
    coords = {
        #^ edges
        DOWN | LEFT | RIGHT: (1, 0),
        UP | DOWN | RIGHT: (0, 1),
        UP | LEFT | RIGHT: (1, 2),
        UP | DOWN | LEFT: (2, 1),

        #* corners
        DOWN | RIGHT: (0, 0),
        UP | RIGHT: (0, 2),
        UP | LEFT: (2, 2),
        DOWN | LEFT: (2, 0),

        #! middle
        UP | DOWN | LEFT | RIGHT: (1, 1)
    }
    element = tiles[index]
    key = 0
    for tile in tiles:
        difference = subtract_tuples(tile.tile_position, element.tile_position)
        dict = {
            (1, 0): RIGHT,
            (-1, 0): LEFT,
            (0, 1): DOWN,
            (0, -1): UP
        }
        try:
            key |= dict[difference]
        except KeyError: pass
    try:
        return coords[key]
    except KeyError:
        return (1, 1)
class TileManager:
    def __init__(self, display: Display):
        self.display = display
        self.tiles = list[TileListElement]()
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
            tile_descriptor: TileDescriptor = descriptor
            tile = GameObject(self.cell_size)
            tile.pos = multiply_tuples(self.cell_size, tile_descriptor.tile_position)
            tile.add_component(TilesetComponent(self.tileset, self.cell_size, (0, 0)))
            self.tiles.append(TileListElement(tile, tile_descriptor.tile_position))
    def update(self):
        for index in range(len(self.tiles)):
            sprite = determine_tile_sprite(self.tiles, index)
            self.tiles[index].object.get_component(TilesetComponent).tile = sprite
        pass
    def render(self, display: Display):
        for tile in self.tiles:
            tile.object.render(display)