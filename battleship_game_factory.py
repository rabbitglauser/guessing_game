import json
import random

from flask import jsonify

from global_constants import HORIZONTAL, VERTICAL, MAX_BOAT_PLACEMENTS_ATTEMPTS, HORIZONTAL_STR, MIN_BOAT_LENGTH, \
    MAX_BOAT_LENGTH, VERTICAL_STR, DIFFICULTY_ADJUSTMENT_LOW, DIFFICULTY_ADJUSTMENT_HIGH, DIFFICULTY_LEVEL_LOW, \
    GRID_DIVISOR, MAX_GRID_SIZE, MIN_GRID_SIZE
from user import InvalidAPIUsage

battle_ship_list = []
with open("us_states.txt", "r") as f:
    states = f.readlines()
    for state in states:
        battle_ship_list.append("USS " + state.replace("\n", ""))


def make_battle_ship_game(user_name, game, content):
    grid_size = content["grid_size"]
    difficulty_level = content["difficulty"]
    # create random number of random sized boats
    num_boats = calculate_number_of_boats(grid_size, difficulty_level)
    boat_names = get_unique_boat_names(num_boats)
    boats = []
    for i in range(len(boat_names)):
        boats.append(make_random_boat(boat_names[i], grid_size, boats))
    game["grid_size"] = grid_size
    game["num_boats"] = len(boats)
    game["boats"] = boats
    return game


def calculate_number_of_boats(grid_size, difficulty_level):
    difficulty_adjustment = DIFFICULTY_ADJUSTMENT_LOW if difficulty_level == DIFFICULTY_LEVEL_LOW else DIFFICULTY_ADJUSTMENT_HIGH
    num_boats = int(round(((float(grid_size) / float(GRID_DIVISOR)) * difficulty_adjustment), 0))
    return num_boats


def make_random_boat(boat_name, grid_size, boats):
    boat_length = random.randint(MIN_BOAT_LENGTH, MAX_BOAT_LENGTH)
    orientation = random.randint(HORIZONTAL, VERTICAL)
    coordinates = find_random_location_for_boat(grid_size, boat_length, orientation, boats)
    boat = {
        "name": boat_name,
        "length": boat_length,
        "orientation": HORIZONTAL_STR if orientation == 0 else VERTICAL_STR,
        "coordinates": coordinates
    }
    return boat


# Get a list boats with Unique names
def get_unique_boat_names(num_boats):
    boat_names = set()
    while len(boat_names) < num_boats:
        random_boat_name = random.randint(0, len(battle_ship_list) - 1)
        boat_names.add(battle_ship_list[random_boat_name])
    return list(boat_names)


def find_random_location_for_boat(grid_size, boat_length, orientation, boats):
    # while there is an collision of existing boats
    num_searches = 0
    while True:
        num_searches += 1
        # search for a boat location that is on the grid and possible to add
        start_coordinate = get_location_in_grid(grid_size, boat_length, orientation)
        coordinates = calculate_boat_coordinates(start_coordinate, orientation, boat_length)

        # check if the new boat is going to intersection with the existing boats
        if no_collision_with_existing_boats(coordinates, boats):
            return coordinates
        if num_searches > MAX_BOAT_PLACEMENTS_ATTEMPTS:
            print(f"FAILED: Num attempts [{num_searches}] to place boat into grid [{grid_size}]"
                  f" num boats[{len(boats)}] boats[{json.dumps(boats)}]")
            raise InvalidAPIUsage(
                "Unable to construct the game with the given parameters. Can not places boats on grid")


#  Get the starting point coordinates for the boat, taking into account
#  the length and orientation of the boat
def get_location_in_grid(grid_size, boat_length, orientation):
    if boat_length > grid_size:
        raise InvalidAPIUsage(f"Unable to construct the game. "
                              f"Boat length [{boat_length}] must be less than the grid_size [{grid_size}]")

    # get a random location for the boat
    x_limits = grid_size - boat_length if orientation == HORIZONTAL else grid_size - 1
    y_limits = grid_size - boat_length if orientation == VERTICAL else grid_size - 1
    x_loc = random.randint(0, x_limits)
    y_loc = random.randint(0, y_limits)
    return {"x": x_loc, "y": y_loc}


# return a list of the x,y coordinates of every point in the boat
def calculate_boat_coordinates(start_coordinate, orientation, boat_length):
    coordinates = [start_coordinate]
    x = start_coordinate["x"]
    y = start_coordinate["y"]
    for _ in range(boat_length - 1):
        x = x + 1 if orientation == HORIZONTAL else x
        y = y + 1 if orientation == VERTICAL else y
        coordinates.append({"x": x, "y": y})
    return coordinates


# Check if the coordinates of the boat collide with any of the coordinates of the other boats
def no_collision_with_existing_boats(new_boat_coordinates, boats):
    all_boat_coordinates = [coords for boat in boats for coords in boat["coordinates"]]
    for boat_grid_ref in new_boat_coordinates:
        for grid_ref in all_boat_coordinates:
            if boat_grid_ref["x"] == grid_ref["x"] and boat_grid_ref["y"] == grid_ref["y"]:
                return False
    return True
