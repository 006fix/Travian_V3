
import random
# this class serves as the holder for the slightly more advanced type of square, the oasis
# the oasis can be owned by players, gathers animals, and gathers resources into itself
# it can also be of various types.

class Oasis:
    def __init__(self, location):
        # location of square within world map
        self.location = location
        # interactable flag serves to identify if square can be interacted with by players
        self.interactable = True
        # identifies which play owns this square
        self.owner = None
        # identifies when this square was last active, with reference to the global game clock
        self.Last_Active = 0
        # identifies whether this square is asleep or not. If it changes to false, subsidary
        # functions should have the ability to act on this information.
        self.Sleep = True
        # serves to identify what type of square this is
        self.type_square = 'oasis'
        # this serves to be updated as required to trigger the oasis to update its stats
        self.next_action = False
        # adding in a "resource_types" field, to determine type of oasis
        self.resource_types = []
        # 25% odds to be each type of resource
        # additional 20% odds to hold a secondary crop type
        randval = random.randint(1, 100)
        if randval <= 25:
            self.resource_types.append('wood')
        elif randval <= 50:
            self.resource_types.append('clay')
        elif randval <= 75:
            self.resource_types.append('iron')
        else:
            self.resource_types.append('crop')
        # second iteration to handle secondary crop types
        randval = random.randint(1, 100)
        if randval > 80:
            self.resource_types.append('crop')

        # now we define the storage holdings of the oasis and storage cap, and refill rate
        #as always : storage is defined as ['wood','clay','iron','crop']
        # if only one type of resource, cap = 1k of each. if 2, 2k of each
        if len(self.resource_types) == 1:
            self.storage_cap = [1000, 1000, 1000, 1000]
        else:
            self.storage_cap = [2000, 2000, 2000, 2000]
        # we also need to define a refill rate (figures given per hour). This is base 10 of each. If double crop, 10 of each 80 of crop
        self.default_refill_rate = {'wood': 10, 'clay': 10, 'iron': 10, 'crop': 10}
        if self.resource_types == ['crop','crop']:
            self.refill_rate = [10, 10, 10, 80]
        else:
            for item in self.resource_types:
                self.default_refill_rate[item] = 40
            self.refill_rate = [self.default_refill_rate['wood'], self.default_refill_rate['clay'],
                           self.default_refill_rate['iron'], self.default_refill_rate['crop']]

        # initial storage is the maximum possible storage.
        self.resource_storage = self.storage_cap

        # to do later : add function to limit withdrawls via raids from any individual player

        # to do later : add in oasis defenders, actually make these defenders.

    # to do later : add in ability for oasis to check its resources and update as needed based on elapsed time since last action


