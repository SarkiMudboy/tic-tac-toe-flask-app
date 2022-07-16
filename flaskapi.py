from flask import Flask, request, session, jsonify
from ttt_game import Game
import json

app = Flask(__name__)
app.secret_key = "gameplay101"

connected = set()
games = {}
idCount = 0

@app.route("/", methods=["GET"])
def connect_player():
	global idCount
	idCount += 1
	p = "X"
	gameId = (idCount - 1) // 2
	if idCount % 2 == 1:
		games[gameId] = Game(gameId)
		games[gameId].player_1 = p
		print('Creating new game...')
	else:
		games[gameId].ready = True
		p = "O"
		games[gameId].player_2 = p
		games[gameId].resetTurn(starter=True)

	response = {'id': gameId, 'player': p}
	return jsonify(response)


@app.route("/<gameId>/<player>/play/<move>", methods=["POST"])
def play(gameId, player, move):

	if gameId in games:
		game = games[gameId]

		game.play(player, eval(move))

		return jsonify(game.toJson())

	else:
		return jsonify("NONE")


@app.route("/<gameId>/<player>/get", methods=["GET"])
def get_game(gameId, player):

	if int(gameId) in games:
		print('Its in games')
		game = games[int(gameId)]

		return jsonify(game.toJson())

	return jsonify("NONE")


if __name__ == "__main__":
	app.run(debug=True)