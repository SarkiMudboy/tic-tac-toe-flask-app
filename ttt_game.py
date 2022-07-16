import random
import json

class Tafel:
	def __init__(self, state):
		self.state = state

	# gibt das Spielfeld im aktuellen Zustand auf der Konsole aus.
	def print_board(self):
		print(" " + self.state[0] + " | " + self.state[1] + " | " + self.state[2] + " \n"
			  + " " + self.state[3] + " | " + self.state[4] + " | " + self.state[5] + " \n"
			  + " " + self.state[6] + " | " + self.state[7] + " | " + self.state[8] + " \n")

	# fügt das Zeichen des Spielers auf das gesetzten Feld hinzu und prüft ob die Eingabe gültig ist oder nicht.
	def add_turn(self, turn_list):
		if self.state[turn_list[0]] == " ":
			self.state[turn_list[0]] = turn_list[1]
			return 'None'
		else:
			return "Bereits gesetzt"

	# prüft ob alle Felder des Boards belegt worden sind und gibt einen booleschen Wert zurück.
	def not_full(self):
		for e in self.state:
			if e == " ":
				print(e)
				return True
		return False

	# prüft ob ein Spieler gewonnen hat indem es die entsprechenden Kombinationen durchgeht und gibt einen booleschen Wert zurück.
	def check_if_win(self):
		if self.state[0] == self.state[1] == self.state[2] != " ":
			return self.state[0]
		elif self.state[3] == self.state[4] == self.state[5] != " ":
			return self.state[3]
		elif self.state[6] == self.state[7] == self.state[8] != " ":
			return self.state[6]

		elif self.state[0] == self.state[3] == self.state[6] != " ":
			return self.state[0]
		elif self.state[1] == self.state[4] == self.state[7] != " ":
			return self.state[1]
		elif self.state[2] == self.state[5] == self.state[8] != " ":
			return self.state[2]

		elif self.state[0] == self.state[4] == self.state[8] != " ":
			return self.state[0]
		elif self.state[2] == self.state[4] == self.state[6] != " ":
			return self.state[2]
		else:
			return False


class Game:
	def __init__(self, id):
		self.board = Tafel([" ", " ", " ", " ", " ", " ", " ", " ", " "])
		self.player_1 = None
		self.player_2 = None
		self.ready = False
		self.turn_count = 1
		self.players = [self.player_1, self.player_2]
		self.current_player = None
		self.id = id
		self.message = 'None'
		self.winner = ''

	def get_player_move(self, p):
		"""
		:param p: [0, 1]
		:return: Move
		"""
		return self.moves[p]

	def play(self, player, move):

		print("playing...")

		self.message = self.board.add_turn(move)
		self.resetTurn()
		self.turn_count += 1

	def connected(self):
		return self.ready

	def winner(self):

		return self.board.check_if_win()

	def resetTurn(self, starter=False):

		if starter:
			self.current_player = random.choice(["X", "O"])

		if self.current_player == self.player_1:
			self.current_player = self.player_2
		else:
			self.current_player = self.player_1

	def toJson(self):
		return json.dumps(self, default=lambda o:o.__dict__, sort_keys=True, indent=4)

	def unPack(self, **kwargs):
		self.board = Tafel(kwargs.get("board")["state"])
		self.player_1 = kwargs.get("player_1")
		self.player_2 = kwargs.get("player_2")
		self.turn_count = kwargs.get("turn_count")
		self.ready = kwargs.get("ready")
		self.current_player = kwargs.get("current_player")
		self.message = kwargs.get("message")
		self.players = kwargs.get("players")
		self.winner = kwargs.get("winner")



