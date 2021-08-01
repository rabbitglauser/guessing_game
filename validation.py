from pprint import pprint

from user import InvalidAPIUsage


def validate_word_game_parameters(content):
    if "answer" not in content or "question" not in content:
        raise InvalidAPIUsage(f"Word games must specify the question and answer")
    answer = content["answer"]
    if type(answer) != str:
        raise InvalidAPIUsage(f"Word games must specify the answer as a string")


def validate_number_game_parameters(content):
    if "answer" not in content or "question" not in content:
        raise InvalidAPIUsage(f"Number games must specify the question and answer")
    if type(content["answer"]) != int:
        raise InvalidAPIUsage(f"Number games must specify the answer as a int")


def validate_geo_game_parameters(content):
    raise NotImplementedError("Sorry we have not created this game type yet")


def validate_grid_game_parameters(content):
    if "grid_size" not in content:
        raise InvalidAPIUsage("The grid_size is a mandatory parameter for this game")

    grid_size = content["grid_size"]
    if grid_size < 10 or grid_size > 100:
        raise InvalidAPIUsage("sorry you cant have a grid bigger than 100 or less than 10")

    if "difficulty" in content:
        difficulty = content["difficulty"]
        if difficulty not in ["LOW", "HIGH"]:
            raise InvalidAPIUsage("The difficulty parameter must be one of [LOW,HIGH]")
    else:
        raise InvalidAPIUsage("The difficulty parameter is MANDATORY. Must be one of [LOW,HIGH]")

