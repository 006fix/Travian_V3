
import Function_Repository.Create_and_Populate_Map as populate_map
import Function_Repository.Create_and_Populate_Players as populate_players
import Classes.Game_World.Villages.Village as village

# successful test of the basic map creation, including summaries of various types of villages etc

tile_squares = populate_map.create_map(100)
num_wilderness = 0
num_oasis = 0
num_habitable = 0
total_squares = 0
hab_type_dict = {}
for i in tile_squares:
    total_squares += 1
    if i.type_square == 'wilderness':
        num_wilderness += 1
    elif i.type_square == 'oasis':
        num_oasis += 1
    elif i.type_square == 'habitable':
        num_habitable += 1
        holdval = str(i.type_hab)
        try:
            holdval2 = hab_type_dict[holdval]
            holdval2 += 1
            hab_type_dict[holdval] = holdval2
        except:
            hab_type_dict[holdval] = 1
    else:
        raise ValueError("Unknown type of square encountered, please investigate.")

print(f'Map has been fully created, with {total_squares} squares, {num_wilderness} wilderness tiles, {num_oasis} oasis tiles, and {num_habitable} habitable tiles')
print('Among our various habitable squares, we have numerous types of squares:')
for key in hab_type_dict:
    print(f'For the type: {key}, we have a record of {hab_type_dict[key]} entries')

# successful test of the player creation function.
playerbase = populate_players.create_playerbase(100)
print(f'There are {len(playerbase)} players')
print(f'As an example, the name of the final player is {playerbase[-1].name}')


# testing basic logic for creation of village.
# successful test, but a true creation function will need to overwrite the values in the core map space.
not_found_test = True
while not_found_test:
    for i in tile_squares:
        if i.type_square != 'habitable':
            pass
        else:
            # stopping the test now we've found a habitable square
            not_found_test = False
            test_loc = i.location
            test_type_hab = i.type_hab
            test_field_list_dict = i.field_list_dict
            test_village = village.Village(test_loc, test_type_hab, test_field_list_dict, "test_owner")
            print(f'We used test logic of location {test_loc}, type_hab {test_type_hab}, and fields {test_field_list_dict}')
            print(f'Post creation, we have values of location {test_village.location}, type_hab {test_village.type_hab}, and fields {test_village.field_list_dict}')
            break