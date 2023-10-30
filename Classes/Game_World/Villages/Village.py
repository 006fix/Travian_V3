
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

    def calculate_pop(self):
        # this function serves to iterate through our buildings in the village and calculate total pop
        total_pop = 0
        # calculate pop from buildings
        for key in self.buildings:
            holder = self.buildings[key]
            # check if its empty
            if len(holder) > 0:
                building = holder[0]
                # controls for buildings that can duplicate
                if 'warehouse' in building:
                    building = 'warehouse'
                if 'granary' in building:
                    building = 'granary'
                level = holder[1]
                pop = building_data.building_dict[building][level][2]
                total_pop += pop
        for key in self.fields:
            pop = self.fields[key].pop
            total_pop += pop
        self.pop = total_pop

    def calculate_cp(self, game_counter, self_last_active):
        # this function serves to generate total CP generated since the last time the cp were calculated
        # HOWEVER, THIS IS WRONG
        # to do : modify this so that it doesn't include the newly built building in the totals.
        # this function uses self last active and global game counter.
        total_cp = 0
        # calculate pop from buildings
        for key in self.buildings:
            holder = self.buildings[key]
            # check if its empty
            if len(holder) > 0:
                building = holder[0]
                # controls for buildings that can duplicate
                if 'warehouse' in building:
                    building = 'warehouse'
                if 'granary' in building:
                    building = 'granary'
                level = holder[1]
                cp = building_data.building_dict[building][level][1]
                total_cp += cp
        for key in self.fields:
            pop = self.fields[key].cp
            total_cp += cp
        local_duration_slept = game_counter - self_last_active
        # 86400 = seconds in a day
        cp_per_sec = total_cp / 86400
        cp_gained = cp_per_sec * local_duration_slept
        current_cp = self.cp
        self.cp = current_cp + cp_gained

    def get_building_pop(self):
        # this function serves to identify total pop at a given point in time
        # this can be used in yield calculations to determine how much needs to be subtracted from crop
        total_pop_usage = 0
        for key in self.buildings:
            # this line below is to identify the null values
            holdval = self.buildings[key]
            if len(holdval) > 1:
                building = self.buildings[key][0]
                building_level = self.buildings[key][1]
                if 'warehouse' in building:
                    building = 'warehouse'
                if 'granary' in building:
                    building = 'granary'
                pop_usage = building_data.building_dict[building][building_level][2]
                total_pop_usage += pop_usage

            # now divide by 3600, to match the yield calc
            total_pop_usage /= 3600
            return total_pop_usage

    def yield_calc(self):
        # this function serves to calculate our yield, per second, for our various resources
        # this obviously generates fractional values, but that is what it is
        wood_yield = 0
        clay_yield = 0
        iron_yield = 0
        crop_yield = 0
        crop_usage = 0
        for key3 in self.fields:
            if 'Wood' in key3:
                wood_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
            if 'Clay' in key3:
                clay_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
            if 'Iron' in key3:
                iron_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
            if 'Crop' in key3:
                crop_yield += self.fields[key3].field_yield / 3600
                crop_usage += self.fields[key3].pop / 3600
        # now reduce crop yield by crop usage

        # modification to incorporate building pop usage
        building_pop_usage = self.get_building_pop()
        crop_usage += building_pop_usage
        # modification ends
        crop_yield -= crop_usage

        if crop_yield == 0:
            raise ValueError("This player now has zero crop yield, and must build crop")
            # to do :  I need to modify this such that it doesn't just break the code, but instead actually limits future options

        # now we've got the full yields out, so multiply by time passed
        yields = [wood_yield, clay_yield, iron_yield, crop_yield]
        return yields

    def possible_buildings(self):
        # this function is going to serve to identify what buildings can actually be built at any one time
        # this will incorporate restrictions on the ability to build when crop levels become too low

        # holder variable for the buildings that can be built
        possible_buildings = []
        # get readings of current yields so we know how much crop we have spare
        current_yields = self.yield_calc()
        # im going to keep this as the /3600 version, and will /3600 future crop usages of buildings
        current_crop = current_yields[3]

        #iterate through the buildings currently in the settlement:
        for key in self.buildings:
            holdval = self.buildings[key]
            if len(holdval) > 0:
                # now we check if the building is upgradeable
                # this is defined as the index 2 position of the building.
                # but this will need an update later where we actually lock some upgrades behind others
                # to do : build this upgrade restriction logic into code

