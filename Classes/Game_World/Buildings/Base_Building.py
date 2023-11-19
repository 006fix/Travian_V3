
import Base_Data.Buildings_Data as b_data
import Function_Repository.duration_calc as duration_calc

# due to the varied requirements of various buildings, i've decided to make a class for buildings
# this will be the generic baseline class, which all others willl build on
# basic logic for things which are universal : can you be upgraded, level, upgrade_cost, name, type,
# cp, pop, upgrade time
# also needs a function to update some of these core metrics
# then we need subtypes which extend functionality as needed
class Building:
    def __init__(self, level=0):
        #can it be upgraded
        self.upgradable = True
        self.level = level
        self.name = ""
        self.type = ""
        self.upgrade_cost = False
        self.cp = False
        self.pop = False
        self.upgrade_time = False

        def update_stats(self):
            #this will also need a specialist version to be created for each type of building
            holdval = self.level
            self.level = holdval + 1
            self.upgrade_cost = b_data.building_dict[self.type][self.level][0]
            self.cp = int(b_data.building_dict[self.type][self.level][1])
            self.pop = int(b_data.building_dict[self.type][self.level][2])
            self.upgrade_time = int(duration_calc.sec_val(b_data.building_dict[self.type][self.level][3]))