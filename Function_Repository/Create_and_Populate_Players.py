
import Classes.Players.Player as player

def create_playerbase(num_players):
    # create a holder that stores all the various players once created
    player_collection = []
    # iterate over number of players, starting at 1 index.
    for i in range(1, num_players+1):
        # at a later date, this should probably be modified such that player name can identify different approaches
        player_name = f"Base_Player_{i}"
        holder_player = player.Player(player_name)
        player_collection.append(holder_player)

    return player_collection

