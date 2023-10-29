
class Player:
    def __init__(self, name, race="holder_race", population=0, attack_points=0, defence_points=0,
                 raid_points=0, culture_points=0, villages=[]):
        # basic holder for the players name
        self.name = name
        # stores the players race, although at present this is meaningless
        # to do : add in various playable races
        self.race = race
        # measure of the advancement of the player (sum of all villages)
        self.culture_points = culture_points
        # measure of the total size of the player (sum of all villages)
        self.population = population
        # total number of enemies killed in attacks
        self.attack_points = attack_points
        # total number of enemies killed while defending
        self.defence_points = defence_points
        # stores the total number of resources stolen by the player
        self.raid_points = raid_points
        # stores the number of villages held by the player
        self.villages = villages
        # stores the last time in global game time that the player was active
        self.Last_Active = 0
        # stores whether or not the player is awake (needs to act)
        self.Sleep = False
        # to do at a later date, create a hero class and assign to players based on race, then update.
        self.Hero = None