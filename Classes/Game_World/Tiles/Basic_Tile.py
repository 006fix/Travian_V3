# this serves as a PARENT class for subsidiary types of different squares
import random

class Square:
    # location is fed in at creation
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
        # subclasses should have the ability to act on this information.
        self.Sleep = True
        randval = random.randint(1,100)
        # 10% odds wilderness
        # 20% odds oasis
        # otherwise habitable
        if randval <= 10:
            self.type_square = 'wilderness'
        elif randval <= 30:
            self.type_square = 'oasis'
        else:
            self.type_square = 'habitable'
