
import Classes.Game_World.Tiles.Basic_Tile as basic_tile
import Classes.Game_World.Tiles.Oasis as oasis
import Classes.Game_World.Tiles.Wilderness as wilderness

for i in range(10):
        test_tile = basic_tile.Square("test_loc")
        if test_tile.type_square == 'wilderness':
            new_test_tile = wilderness.Wilderness(test_tile)
            print(f'testing, {new_test_tile.wilderness_flag}')
        elif test_tile.type_square == 'oasis':
            new_test_tile = oasis.Oasis(test_tile)
            print(f'oasis tile created of type {new_test_tile.resource_types}')
