import random
import time

from db import DB
from game_factory import make_game
from user import InvalidAPIUsage

GUESSING_GAME_DATABASE = "GuessingGame"
GAME_COLLECTION = "Game"
USERS_COLLECTION = "User"


class GuessingGame:
    def __init__(self):
        self.db = DB(GUESSING_GAME_DATABASE)

    def is_user_name_invalid(self, user_name):
        users_collection = self.db.get_collection(USERS_COLLECTION)
        response = users_collection.find_one({"user_name": user_name})
        if response is None:
            print("the user does not exist in the database")
            return True
        else:
            return False

    def create_game(self, user_name, content):
        if self.is_user_name_invalid(user_name):
            return None

        game = make_game(user_name, content)
        games_collection = self.db.get_collection(GAME_COLLECTION)
        response = games_collection.insert_one(game)
        return self.start_game(response.inserted_id)

    def join_game(self, user_name, game_id):
        if self.is_user_name_invalid(user_name):
            return None
        games_collection = self.db.get_collection(GAME_COLLECTION)
        filter_criteria = {"_id": game_id}
        projection = {"_id": 0, "start_time": 1, "finish_time": 1, "winner": 1}
        game = games_collection.find_one(filter_criteria, projection)
        if not game:
            return "That game does not exist. Try another game"

        if game["finish_time"] or game["winner"]:
            return "You can not join a game that has already finished"
        start_time = game["start_time"]
        if not start_time and int(start_time) > int(time.time()):
            return f"The game has not started yet. It will start at [{GuessingGame.print_time(start_time)}]"

        response = games_collection.update_one({'_id': game_id}, {"$addToSet": {"players": {"$each": [user_name]}}})
        if response.matched_count <= 0:
            return "Could not find the user"
        return f"Congratulations, you joined the game"

    def get_created_games(self):
        filter_criteria = {"finish_time": {"$eq": None}}
        projection = {"name": 1, "question": 1, "players": 1, "start_time": 1}
        return self.get_games(filter_criteria, projection)

    def get_finished_games(self):
        filter_criteria = {"finish_time": {"$ne": None}}
        projection = {"name": 1, "question": 1, "answer": 1, "winner": 1, "players": 1, "start_time": 1,
                      "finish_time": 1}
        return self.get_games(filter_criteria, projection)

    def get_my_games(self, user_name):
        filter_criteria = {"$and": [{"players": {"$in": [user_name]}},
                                    {"finish_time": {"$eq": None}}]}
        projection = {"name": 1, "question": 1, "players": 1, "start_time": 1}
        return self.get_games(filter_criteria, projection)

    # gets games by filter criteria and projection
    def get_games(self, filter_criteria, projection):
        games_collection = self.db.get_collection(GAME_COLLECTION)
        games_cursor = games_collection.find(filter_criteria, projection)
        games_list = {}
        for game in games_cursor:
            games_list[game["_id"]] = game
        return games_list

    #  play the actual game
    def play_game(self, user_name, game_id, user_answer):
        if self.is_user_name_invalid(user_name):
            return "You are not permitted to play this game"

        #  get the game from the db
        games_collection = self.db.get_collection(GAME_COLLECTION)
        filter_criteria = {"_id": game_id}
        projection = {"_id": 0, "answer": 1, "players": 1, "start_time": 1, "finish_time": 1, "winner": 1}
        game = games_collection.find_one(filter_criteria, projection)
        if not game:
            return "That game does not exist. Try another game"
        error_message = self.check_game_state_valid(game, user_name)
        if error_message:
            return error_message

        game_type = game["type"]
        if game_type == "WORD":
            return self.play_word_game(game_id, game, user_name, user_answer)
        elif game_type == "NUMBER":
            return self.play_number_game(game_id, game, user_name, user_answer)
        elif game_type == "GEO":
            return self.play_geo_game(game_id, game, user_name, user_answer)
        elif game_type == "GRID":
            return self.play_grid_game(game_id, game, user_name, user_answer)
        else:
            raise InvalidAPIUsage(f"The game type {game_type} is not supported")

    def play_number_game(self, game_id, game, user_name, user_answer):
        if not user_answer.isdigit():
            return "Incorrect guess. Should be an integer"
        answer = int(game["answer"])
        guess = int(user_answer)
        if answer == guess:
            self.end_game(game_id, user_name)
            return "Congratulations you won"
        elif answer > guess:
            return "You guess too low. Number is greater"
        elif answer < guess:
            return "You guess too high. Number is lower"

    def play_word_game(self, game_id, game, user_name, user_answer):
        if str(game["answer"]).lower() == user_answer.lower():
            self.end_game(game_id, user_name)
            return "Congratulations you won"
        else:
            return "That is not the right answer. Keep trying"

    def play_grid_game(self, game_id, game, user_name, user_answer):
        raise NotImplementedError(f"The grid game has not been implemented yet")

    def play_geo_game(self, game_id, game, user_name, user_answer):
        raise NotImplementedError(f"The geo game has not been implemented yet")

    def end_game(self, game_id, user_name):
        games_collection = self.db.get_collection(GAME_COLLECTION)
        games_collection.update_one({'_id': game_id}, {"$set": {"winner": user_name, "finish_time": int(time.time())}})

    @staticmethod
    def check_game_state_valid(game, user_name):
        # has the game already finished .... then tell user who was the winner
        if game["finish_time"]:
            return f"The game already finished. [{game['winner']}] was the winner. Try another game, dummy!!"

        # has the game not started ... then do not let anyone play
        start_time = game["start_time"]
        if not start_time and int(start_time) > int(time.time()):
            return f"The game has not started yet. It will start at [{GuessingGame.print_time(start_time)}]"

        # is the user allow to play? ... tell user they can not play... must join game first
        if user_name not in game["players"]:
            return f"You must join the game first. You are [{user_name}] Current players are: {game['players']}"
        return None

    # Figure out how to start the game
    def start_game(self, game_id):
        games_collection = self.db.get_collection(GAME_COLLECTION)
        five_minutes = 60 * 5
        now = int(time.time())
        start_time = now + five_minutes
        games_collection.update_one({'_id': game_id}, {"$set": {"start_time": start_time}})
        return f"Game [{game_id}] starts in 5 mins at {self.print_time(start_time)}. now [{self.print_time(now)}]"

    @staticmethod
    def print_time(start_time):
        return time.strftime('%H:%M:%S', time.gmtime(start_time))
