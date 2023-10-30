
# this will serve as the holder for the "village" class
# this village class will serve to overwrite the "habitable" class squares
# it will "inherit" various features from it, but WILL NOT use child inheritance
# this is because it needs to inherit specific random instantiations of the parent class, and not the general logic

import Base_Data.Buildings_Data as building_data

class Village:
    def __init__(self, location, type_hab, field_list_dict, owner, name):
        # location of square within world map
        self.location = location
        # interactable flag serves to identify if square can be interacted with by players
        self.interactable = True
        # identifies which play owns this square
        self.owner = owner
        # identifies when this square was last active, with reference to the global game clock
        self.Last_Active = 0
        # identifies whether this square is asleep or not. If it changes to false, subsidary
        self.Sleep = True
        # serves to identify what type of square this is
        self.type_square = 'habitable'
        # this serves to be updated as required to trigger the village to update its stats
        self.next_action = False
        # we also give each village a name. This can be overwritten and changed, but must be DISTINCT globally
        # to do later : create function for village names which ensures global stability
        self.name = name

        # on instantiation, we will pull the instance specific logic of type hab, and store it here too
        self.type_hab = type_hab
        # we also pull the entire list of fields that are already created as part of the habitable instantion
        self.field_list_dict = field_list_dict

        # now we add some of the village specific pieces of logic

        # to do later : add function which on instantion or takeover, modifies player self.villages holdings to include/exclude this village

        self.buildings = {0: '', 1: '', 2: '', 3: '', 4: '', 5: '', 6: '', 7: '', 8: '',
                          9: '', 10: '', 11: '', 12: '', 13: '', 14: '', 15: '', 16: '',
                          17: '', 18: '', 19: '', 20: '', 21: '', 22: ''}
        # structure of the below - reference key for buildings_dict lookup, level, upgradeable bool.
        self.buildings[0] = ['main_building', 1, True]
        self.buildings[1] = ['warehouse1', 0, True]
        self.buildings[2] = ['granary1', 0, True]
        # to do later : add walls and rally point, enable this logic
        # self.buildings[22] = ['wall', 0, True]
        # self.buildings[21] = ['rally_point', 0, True]

        # the two below items WILL need to be changed later, but these are instantiation standard
        # as ever, follows the rule ['wood','clay','iron','crop']
        self.storage_cap = [800, 800, 800, 800]
        self.stored = [500, 500, 500, 500]

        # this is the storage for anything you're currently building, in sequential order
        # to do : figure out how we actually use this
        # for now we'll only allow one upgrade
        self.currently_upgrading = []

        # these store the pop and cp, which will need to be updated and modified later
        self.pop = 0
        self.cp = 0

        # this stores the upgrade time modifier (based on main building level)
        self.upgrade_time_modifier = 1

    # now have a series of class specific functions

    def modify_building_time(self):
        #this function serves to identify the main building level, the associated modifiers to building time
        # and then update the self.upgrade_time_modifier value
        # to do : BUT WHEN AND HOW SHOULD IT BE CALLED?
        main_building_key = self.buildings[0][0]
        main_building_level = self.buildings[0][1]
        building_time = building_data.building_dict[main_building_key][main_building_level][4]
        self.upgrade_time_modifier = building_time

    def calculate_storage(self):
        # this function serves to identify our various warehouse and granaries, pull their storage, and calculate our storage
        # this then modifies self values
        warehouse_storage = 0
        granary_storage = 0
        for key in self.buildings:
            holder = self.buildings[key]
            # check if its empty
            if len(holder) > 0:
                if 'warehouse' in holder[0]:
                    level = holder[1]
                    storage = building_data.building_dict['warehouse'][level][4]
                    warehouse_storage += storage
                if 'granary' in holder[0]:
                    level = holder[1]
                    storage = building_data.building_dict['granary'][level][4]
                    granary_storage += storage
        self.storage_cap = [warehouse_storage, warehouse_storage, warehouse_storage, granary_storage]
