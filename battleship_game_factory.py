
list_of_battle_ships = ["USS Missouri",
                        "USS Carolina",
                        "USS California"]


def make_battle_ship_game(user_name, game, content):
    grid_size = content["grid_size"]
    difficulty_level = content["difficulty"]

    # Sammy does his magic

    boats = []

    game["grid_size"] = grid_size
    game["boats"] = boats
    return game
