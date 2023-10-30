
import random
import Classes.Game_World.Tiles.Fields as fields

# this class serves as the holder for the most common type of square, "habitable"
# this square is interactable, ownable, and comes in various types
# the majority of actions undertaken by players will take place within a square of this type

class Habitable:
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
        self.Sleep = True
        # serves to identify what type of square this is
        self.type_square = 'habitable'
        # this serves to be updated as required to trigger the village to update its stats
        self.next_action = False

        # here we're determining what type of village it is
        # as ever, follows the rule ['wood','clay','iron','crop']
        randval = random.randint(1, 100)
        if randval <= 10:
            self.type_hab = [1, 1, 1, 15]
        elif randval <= 25:
            self.type_hab = [3, 3, 3, 9]
        elif randval <= 35:
            self.type_hab = [4, 3, 4, 7]
        elif randval <= 45:
            self.type_hab = [4, 4, 3, 7]
        elif randval <= 55:
            self.type_hab = [3, 4, 4, 7]
        else:
            self.type_hab = [4, 4, 4, 6]

        # now we expand this out a bit, to create the fields
        # fields occur in list, wood,clay,iron,crop
        # we're using lists above so we can iterate through them to create
        # without doing this seperately dependent on the type above
        field_list = ['Wood', 'Clay', 'Iron', 'Crop']
        self.field_list_dict = {}
        for i in range(len(self.type_hab)):
            for j in range(1, self.type_hab[i] + 1):
                # note - due to the presence of multiple fields of the same type, these are internally identified
                # i.e, wood3, the 3rd wood field within the settlement
                # this is primarily of relevance only when searching individual entries.
                key = field_list[i] + str(j)
                holdval = fields.Field(field_list[i])
                self.field_list_dict[key] = holdval

    # to do later : add in ability for village to check its resources and update as needed based on elapsed time since last action





