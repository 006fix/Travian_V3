
# this will serve as the holder for the "village" class
# this village class will serve to overwrite the "habitable" class squares
# it will "inherit" various features from it, but WILL NOT use child inheritance
# this is because it needs to inherit specific random instantiations of the parent class, and not the general logic

class Village:
    def __init__(self, location, type_hab, field_list_dict):
        # location of square within world map
        self.location = location
        # interactable flag serves to identify if square can be interacted with by players
        self.interactable = True
        # identifies which play owns this square
        self.owner = None
        # identifies when this square was last active, with reference to the global game clock
        self.Last_Active = 0
        # identifies whether this square is asleep or not. If it changes to false, subsidary
        self.Sleep = True
        # serves to identify what type of square this is
        self.type_square = 'habitable'
        # this serves to be updated as required to trigger the village to update its stats
        self.next_action = False

        # on instantiation, we will pull the instance specific logic of type hab, and store it here too
        self.type_hab = type_hab
        # we also pull the entire list of fields that are already created as part of the habitable instantion
        self.field_list_dict = field_list_dict


