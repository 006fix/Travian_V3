
# this function will serve to create a map, and populate it with a number of squares of appropriate types
# 10% wilderness, 10% oasis, 80% habitable
import random
import Classes.Game_World.Tiles.Oasis as oasis
import Classes.Game_World.Tiles.Wilderness as wilderness
import Classes.Game_World.Tiles.Habitable as habitable

def create_map(size):
    map_squares = []
    # all maps are square
    # we iterate from neg to pos. i.e size 200 = 400*400 square, ranging from (-200,-200) to (200,200)
    for i in range(-size, size):
        for j in range(-size, size):
            holdval = random.randint(1,100)
            if holdval <= 10:
                holder_tile = wilderness.Wilderness([i, j])
            elif holdval <= 20:
                holder_tile = oasis.Oasis([i, j])
            else:
                holder_tile = habitable.Habitable([i, j])
            map_squares.append(holder_tile)

    return map_squares

