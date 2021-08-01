import random
import time

from battleship_game_factory import make_battle_ship_game
from user import InvalidAPIUsage
from validation import validate_word_game_parameters, validate_number_game_parameters, validate_geo_game_parameters, \
    validate_number_grid_parameters


def make_game(user_name, content):
    if "type" not in content:
        raise InvalidAPIUsage(f"The game type must be specified")

    game_type = content["type"]
    if game_type == "WORD":
        validate_word_game_parameters(content)
        return create_word_game(user_name, content)
    elif game_type == "NUMBER":
        validate_number_game_parameters(content)
        return create_number_game(user_name, content)
    elif game_type == "GEO":
        validate_geo_game_parameters(content)
        return create_geo_game(user_name, content)
    elif game_type == "GRID":
        validate_number_grid_parameters(content)
        return create_grid_game(user_name, content)
    else:
        raise InvalidAPIUsage(f"The game type {game_type} is not supported")


def create_word_game(user_name, content):
    # Create the game using the given parameters
    game = make_initial_game_object(user_name, content["type"], content["name"])
    game["question"] = content["question"]
    game["answer"] = content["answer"]
    return game


def create_number_game(user_name, content):
    game = make_initial_game_object(user_name, content["type"], content["name"])
    game["question"] = content["question"]
    # If the creator did not specify a number, then we randomly assign one
    game["answer"] = content["answer"] if content["answer"] is not None else random.randint(0, 100)
    return game


def create_grid_game(user_name, content):
    game = make_initial_game_object(user_name, content["type"], content["name"])
    return make_battle_ship_game(user_name, game, content)


def create_geo_game(user_name, content):
    raise Exception("Sorry, not implemented yet")


# make the generic game attributes as the base game object
def make_initial_game_object(user_name, game_type, name):
    game = {
        "_id": int(time.time()),
        "name": name,
        "type": game_type,
        "players": [user_name],
        "start_time": None,
        "finish_time": None,
        "winner": None
    }
    return game
