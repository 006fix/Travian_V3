
# this will serve as the holder for the "village" class
# this village class will serve to overwrite the "habitable" class squares
# it will "inherit" various features from it, but WILL NOT use child inheritance
# this is because it needs to inherit specific random instantiations of the parent class, and not the general logic

import Base_Data.Buildings_Data as building_data
import Base_Data.Fields_Data as fields_data
import Function_Repository.duration_calc as duration_calc
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
        self.fields = field_list_dict

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

        # both of these variables are two part lists. First part is for buildings, second is for fields
        # this is needed as they're stored in subtly different ways
        # holder variable for the buildings that can be built
        possible_buildings = [[],[]]
        # holder variable for theoretically buildable, but not with current stored resources
        possible_buildings_later = [[],[]]

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
                if holdval[2] == True:
                    # get the level of the building
                    building_level = holdval[1]
                    # take building name for lookup in building data
                    keyval = holdval[0]
                    # controls for buildings that can dupe
                    if 'warehouse' in keyval:
                        keyval = 'warehouse'
                    if 'granary' in keyval:
                        keyval = 'granary'
                    upgrade_cost = building_data.building_dict[keyval][building_level][0]
                    # we need to know how much pop this upgrade will cost
                    # this is defined as the pop usage of the next level, minus the pop usage of the current level
                    upgrade_pop_cost = building_data.building_dict[keyval][building_level+1][2] - building_data.building_dict[keyval][building_level][2]

                    # now we need to identify whether the upgrade is actually possible
                    # this has three elements :
                        # 1: does any part of the upgrade require more than we can maximally store?
                        # 2: does any part of the upgrade require more than we current have?
                        #3 : is the crop usage higher than our current crop total?
                    # if 2 is true, but 1 isn't, we can't build it now, but we could eventually
                    # if 3 is true, we can't build it regardless
                    # we have three lists, and can compare item by item. for each cond, True = allowed, False = not allowed
                    cond1 = True
                    cond2 = True
                    cond3 = True
                    # cond1
                    for i in range(len(upgrade_cost)):
                        if upgrade_cost[i] > self.storage_cap[i]:
                            cond1 = False
                    # cond2
                    for i in range(len(upgrade_cost)):
                        if upgrade_cost[i] > self.stored[i]:
                            cond2 = False
                    # cond3
                    if (upgrade_pop_cost/3600) > current_crop:
                        cond3 = False

                    #can build at this moment in time
                    if cond1 and cond2 and cond3:
                        # passing building to build as key, name, and level (current)
                        final_value = [key, holdval[0], building_level]
                        possible_buildings[0].append(final_value)

                    #can build but not with stored resources
                    if (cond1 and cond3) and cond2 == False:
                        # passing building to build as key, name, and level (current)
                        final_value = [key, holdval[0], building_level]
                        possible_buildings_later[0].append(final_value)

        # now we need to search through all fields
        for key in self.fields:
            holdval = self.fields[key]
            field_level = holdval.level
            # we now need the true key for lookups. i.e if the field is "Wood3", we just need "Wood"
            key2 = key[:4]
            # for fields : if upgrade_cost == False, can't upgrade. as such, subset all else to this logic.
            upgrade_cost = fields_data.field_dict[key2][field_level][0]
            if upgrade_cost == False:
                #if unupgradeable, just skip this loop and carry on
                continue
            upgrade_pop_cost = fields_data.field_dict[key2][field_level+1][2] - fields_data.field_dict[key2][field_level][2]

            # now we need to identify whether the upgrade is actually possible
            # this has three elements :
            # 1: does any part of the upgrade require more than we can maximally store?
            # 2: does any part of the upgrade require more than we current have?
            # 3 : is the crop usage higher than our current crop total?
            # if 2 is true, but 1 isn't, we can't build it now, but we could eventually
            # if 3 is true, we can't build it regardless
            # we have three lists, and can compare item by item. for each cond, True = allowed, False = not allowed
            cond1 = True
            cond2 = True
            cond3 = True
            # cond1
            for i in range(len(upgrade_cost)):
                if upgrade_cost[i] > self.storage_cap[i]:
                    cond1 = False
            # cond2
            for i in range(len(upgrade_cost)):
                if upgrade_cost[i] > self.stored[i]:
                    cond2 = False
            # cond3
            if (upgrade_pop_cost / 3600) > current_crop:
                cond3 = False
            # cond3 has an extra piece of logic. If the building that would be built is for crop, it can always be built regardless
            # cond4 : is crop in key
            if key2 == 'Crop':
                cond4 = True
            else:
                cond4 = False

            # if cond4 is true, we simply force cond3 into being true
            if cond4:
                cond3 = True

            # can build at this moment in time
            if cond1 and cond2 and cond3:
                # passing building to build as key, name, and level (current)
                final_value = [key, field_level]
                possible_buildings[1].append(final_value)

            # can build but not with stored resources
            if (cond1 and cond3) and cond2 == False:
                # passing building to build as key, name, and level (current)
                final_value = [key, field_level]
                possible_buildings_later[1].append(final_value)

        return possible_buildings, possible_buildings_later

    # in the original code, there was a function which returned every possible non crop locked upgrade
    # im going to avoid that for now, since i feel the possible buildings later from the above function serves a similar purpose

    def upgrade_structure(self, upgrade_target):
        # this function is called when a building or field is chosen to be upgraded.
        # it returns the duration of this building to take place as a sleep duration
        # this combines what were previosuly seperate functions, so will need to identify what is what

        # step 1 : identify if building or field
        if len(upgrade_target) == 3:
            is_building = True
        else:
            is_building = False

        if is_building:
            building_dict_key = upgrade_target[0]
            relevant_target = self.buildings[building_dict_key]
            current_level = relevant_target[1]
            upgradeable_check = relevant_target[2]
            if upgradeable_check != True:
                print(f" You are upgrading {upgrade_target}")
                raise ValueError("You appear to have attempted to upgrade a building that cannot be upgraded :(")
            # from the above we have some basic data, but we need a subset of the name to actually link
            # to the building data field, due to duplicate buildings. This follows:
            building_data_key = upgrade_target[1]
            if 'warehouse' in building_data_key:
                building_data_key = 'warehouse'
            if 'granary' in building_data_key:
                building_data_key = 'granary'
            # now get upgrade costs
            upgrade_cost = building_data.building_dict[building_data_key][current_level][0]
            upgrade_time = building_data.building_dict[building_data_key][current_level][3]
            true_upgrade_time = int(duration_calc.sec_val(upgrade_time) * self.upgrade_time_modifier)
            # now update how many resources you have on hand
            hold_vals = self.stored
            for i in range(len(hold_vals)):
                hold_vals[i] -= upgrade_cost[i]
            self.stored = hold_vals
            self.currently_upgrading.append(upgrade_target)

            sleep_duration = true_upgrade_time

        else:
            field_data = self.fields[upgrade_target]
            field_dict_key = upgrade_target[:4]

            current_level = field_data.level
            upgradeable_check = field_data.upgradeable
            if upgradeable_check != True:
                print(f"you are upgrading {upgrade_target}")
                raise ValueError("You appear to have attempted to upgrade a field that cannot be upgraded :(")
            upgrade_cost = fields_data.field_dict[field_dict_key][current_level][0]
            upgrade_time = fields_data.field_dict[field_dict_key][current_level][3]
            true_upgrade_time = int(generic_funcs.sec_val(upgrade_time) * self.upgrade_time_modifier)
            # update what is currently stored as resources
            hold_vals = self.stored
            for i in range(len(hold_vals)):
                hold_vals[i] -= upgrade_cost[i]
            self.stored = hold_vals
            self.currently_upgrading.append(upgrade_target)

            sleep_duration = true_upgrade_time

        return sleep_duration

    def structure_upgraded(self, upgrade_target):





