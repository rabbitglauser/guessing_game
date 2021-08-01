import random

battle_ship_list = []
with open("us_states.txt", "r") as f:
    states = f.readlines()
    for state in states:
        battle_ship_list.append("USS " + state.replace("\n",""))


def make_battle_ship_game(user_name, game, content):
    grid_size = content["grid_size"]
    difficulty_level = content["difficulty"]
    # create random number of random sized boats
    num_boats = calculate_number_of_boats(grid_size, difficulty_level)
    boat_names = get_unique_boat_names(num_boats)
    boats = []
    for i in range(len(boat_names)):
        boats.append(make_random_boat(boat_names[i], grid_size))
    game["grid_size"] = grid_size
    game["boats"] = boats
    return game


def calculate_number_of_boats(grid_size, difficulty_level):
    difficulty_adjustment = 1.2 if difficulty_level == "LOW" else 1.8
    num_boats = int(round(((float(grid_size) / float(5)) * difficulty_adjustment), 0))
    return num_boats


def make_random_boat(boat_name, grid_size):
    boat_length = random.randint(2 , 5)
    orientation = random.randint(0, 1)
    coordinates = find_random_location_for_boat(grid_size, boat_length, orientation)
    boat = {"name": boat_name, "coordinates": coordinates}
    return boat


# Get a list boats with Unique names
def get_unique_boat_names(num_boats):
    boat_names = set()
    while len(boat_names) < num_boats:
        random_boat_name = random.randint(0, len(battle_ship_list) - 1)
        boat_names.add(battle_ship_list[random_boat_name])
    return list(boat_names)


def find_random_location_for_boat(grid_size, boat_length, orientation):
    # TODO: find a random location that does not intersect another already existing boat
    coordinates = []

    return coordinates
