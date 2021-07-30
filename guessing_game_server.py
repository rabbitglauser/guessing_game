from flask import Flask, json
from flask import jsonify, request

from user import InvalidAPIUsage, checkUserLoggedIn
from guessing_game import GuessingGame

app = Flask(__name__)

game = GuessingGame()


@app.errorhandler(InvalidAPIUsage)
def invalid_api_usage(e):
    return jsonify(e.to_dict())


@app.route('/api/game', methods=['POST'])
def create_game():
    user_name = checkUserLoggedIn()
    content = request.get_json(force=True)
    if "question" not in content:
        return "invalid request parameters"
    message = game.create_game(user_name, content["name"], content["question"], content["answer"])
    if message is None:
        return {"error": "unable to create the game"}
    return {"message": message}


@app.route('/api/all_games', methods=['GET'])
def get_created_games():
    return game.get_created_games()


@app.route('/api/finished_games', methods=['GET'])
def get_finished_games():
    return game.get_finished_games()


@app.route('/api/my_games', methods=['GET'])
def get_my_games():
    user_name = checkUserLoggedIn()
    return game.get_my_games(user_name)


@app.route('/api/game/join/<int:game_id>', methods=['GET'])
def join_game(game_id):
    user_name = checkUserLoggedIn()
    message = game.join_game(user_name, game_id)
    return message


@app.route('/api/game/play/<int:game_id>', methods=['POST'])
def play_game(game_id):
    user_name = checkUserLoggedIn()
    content = request.get_json(force=True)
    if "answer" not in content:
        return "you did not give me a answer to the question"
    response = game.play_game(user_name, game_id, content["answer"])
    return {"message": response}


if __name__ == '__main__':
    app.run()
