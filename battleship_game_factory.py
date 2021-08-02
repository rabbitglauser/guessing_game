import random

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
    game["boats"] = boats
    return game


def calculate_number_of_boats(grid_size, difficulty_level):
    difficulty_adjustment = 1.2 if difficulty_level == "LOW" else 1.8
    num_boats = int(round(((float(grid_size) / float(5)) * difficulty_adjustment), 0))
    return num_boats


def make_random_boat(boat_name, grid_size, boats):
    boat_length = random.randint(2, 5)
    orientation = random.randint(0, 1)
    orientation_str = "H" if orientation == 0 else "V"
    coordinates = find_random_location_for_boat(grid_size, boat_length, orientation, boats)
    boat = {"name": boat_name, "length": boat_length, "orientation": orientation_str, "coordinates": coordinates}
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
        x_loc, y_loc = get_location_in_grid(grid_size, boat_length, orientation)
        coordinates = calculate_boat_coordinates(grid_size, x_loc, y_loc, boat_length)

        # check if the new boat is going to intersection with the existing boats
        if no_collision_with_existing_boats(coordinates, boats):
            return coordinates
        if num_searches > 100:
            raise InvalidAPIUsage(
                "Unable to construct the game with the given parameters. Can not places boats on grid")


#  Get the starting point coordinates for the boat, taking into account
#  the length and orientation of the boat
def get_location_in_grid(grid_size, boat_length, orientation):
    # TODO: Find a location in the grid which will actually be able to fit your boat in the grid

    # get a random location for the boat
    if orientation == 0:  # HORIZONTAL
        pass
    if orientation == 1:  # VERTICAL
        pass

    x_loc = random.randint(0, grid_size - 1)
    y_loc = random.randint(0, grid_size - 1)
    return x_loc, y_loc


# return a list of the x,y coordinates of every point in the boat
def calculate_boat_coordinates(grid_size, x_loc, y_loc, boat_length):
    # TODO: calculate the actual boat coordinates
    return [{"x": x_loc, "y": y_loc}]


# Check if the coordinates of the boat collide with any of the coordinates of the other boats
def no_collision_with_existing_boats(new_boat_coordinates, boats):
    # TODO check for an collision between new boat and existing boats

    return True
