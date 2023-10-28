
import Classes.Game_World.Tiles.Basic_Tile as base_tile
# this class simply serves to define the basic "wilderness" class of square
# this square cannot be interacted with in any way, and is a non entity beyond providing
# blockages to the map

class Wilderness(base_tile.Square):
    def __init__(self, location):
        super().__init__(location)
        self.interactable = False
