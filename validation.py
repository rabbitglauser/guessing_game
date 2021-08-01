from pprint import pprint

from user import InvalidAPIUsage


def validate_word_game_parameters(content):
    if "answer" not in content and "question" in content:
        raise InvalidAPIUsage(f"Word games must specify the question and answer")
    answer = content["answer"]
    if type(answer) != str:
        raise InvalidAPIUsage(f"Word games must specify the answer as a string")


def validate_number_game_parameters(content):
    # check game variables
    if "answer" not in content and type(content["answer"]) != int:
        raise InvalidAPIUsage(f"Number games must specify the answer as a int")
    #  sammy does magic


def validate_geo_game_parameters(content):
    # sammy does magic
    raise NotImplementedError("Sorry we have not created this game type yet")


def validate_grid_game_parameters(content):

    #  sammy does magic




    pass
