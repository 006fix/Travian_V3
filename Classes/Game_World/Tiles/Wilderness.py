
import Classes.Game_World.Tiles.Basic_Tile as base_tile

class Wilderness(base_tile.Square):
    def __init__(self, location):
        super().__init__(location)
        self.interactable = False
