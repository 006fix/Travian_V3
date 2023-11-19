# this is the specific class for a warehouse
# will need a function to specifically update storage

import Base_Data.Buildings_Data as b_data
import Function_Repository.duration_calc as duration_calc
import Classes.Game_World.Buildings.Base_Building as base_model


class Granary(base_model):
    def __init__(self, building_list):
        super.__init__()

        # mini loop to create the correct name for the building, allowing for duplicates
        rel_names = []
        for key in building_list:
            if 'warehouse' in key:
                rel_names.append(key)
        if len(rel_names) == 0:
            identifier = '1'
        else:
            rel_nums = []
            for i in rel_names:
                holdkey = i[-1]
                rel_num.append(holdkey)
            max_num = max(rel_nums)
            identifier = max_num + 1

        self.name = f'warehouse{identifier}'
        self.type = 'warehouse'
        self.update_stats()
        self.storage = 0

        # new function to provide and update building specific variable
        def update_storage(self):
            self.storage = b_data.building_dict[self.type][self.level][4]

        self.update_storage()
