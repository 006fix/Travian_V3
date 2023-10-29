
# this class simply serves to define the basic "wilderness" class of square
# this square cannot be interacted with in any way, and is a non entity beyond providing
# blockages to the map

class Wilderness:
    def __init__(self, location):
        # location of square within world map
        self.location = location
        # interactable flag serves to identify if square can be interacted with by players
        self.interactable = False
        # identifies which play owns this square, "False" here as impossible
        self.owner = False
        # identifies when this square was last active, with reference to the global game clock
        self.Last_Active = 0
        # identifies whether this square is asleep or not. If it changes to false, subsidary
        # functions should have the ability to act on this information.
        self.Sleep = True
        # serves to identify what type of square this is
        self.type_square = 'wilderness'
