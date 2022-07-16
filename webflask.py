import flask
from flask import request, jsonify
import json
from game import *


Players = (PIECE_ONE, PIECE_TWO)
Winner = None
Board = create_board()

app = flask.Flask(__name__)
app.config["DEBUG"] = True

#route to reset the board and start a new game
@app.route('/start', methods=['GET'])
def api_start():
	reset_board(Board)
	return jsonify("READY")

#route to move the piece for the player one to the desired column number,
#if the column is invalid return invalid else the move is valid,
#if there are four connecting pieces return Winner
@app.route('/move/1/<col>', methods=['GET', 'POST'])
def api_player1_move(col):
	col = int(col)
	if(col < 0 or col > COLUMNS):
		return "INVALID"
	else:
		possible = drop_piece(Board, col, Players[0])
		if(possible == False):
			return jsonify("INVALID")
		Winner = find_winner(Board)
		if(Winner != None):
			
			reset_board(Board)
			return "{} wins".format(PIECE_COLOR_MAP[Winner])
		else:
			print_board(Board)
			return jsonify("VALID") #jsonify(Board)
	
#route to move the piece for the player two to the desired column number,
#if the column is invalid return invalid else the move is valid,
#if there are four connecting pieces return Winner	

@app.route('/move/2/<col>', methods=['GET'])
def api_player2_move(col):
	col = int(col)
	if(col < 0 or col > COLUMNS):
		return jsonify("INVALID")
	else:
		possible = drop_piece(Board, col, Players[1])
		if(possible == False):
			return jsonify("INVALID")
		# check the winner
		Winner = find_winner(Board)
		if(Winner != None):
			# return(jsonify(Board))
			reset_board(Board)
			return "{} wins".format(PIECE_COLOR_MAP[Winner])
		else:
			print_board(Board)
			return jsonify("VALID")#jsonify(Board)

def main():
	
	app.run()


if __name__ == "__main__":
	main()