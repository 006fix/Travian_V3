
# this is the specific class for a main building
# will need a function to specifically update building time modifier

import Base_Data.Buildings_Data as b_data
import Function_Repository.duration_calc as duration_calc
import Classes.Game_World.Buildings.Base_Building as base_model

class Granary(base_model):
    def __init__(self, building_list):
        super.__init__()

        self.name = f'main_building'
        self.type = 'main_building'
        self.update_stats()
        self.upgrade_time_modifier = 1

        # new function to provide and update building specific variable
        def update_modifier(self):
            self.upgrade_time_modifier = b_data.building_dict[self.type][self.level][4]

        self.update_modifier()
