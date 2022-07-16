import random
import pickle
import time
from rest_network import Network
from ttt_game import Game, Tafel


class Spieler:
    def __init__(self, sign):
        self.sign = sign

    # hier wird der Spieler aufgefordert eine Eingabe zwischen 1 und 9
    # zu tätigen. Des Weiteren wird geprüft, ob die Eingabe gültig oder ungültig ist.
    def you_turn(self):
        turn = 0
        while turn < 1 or turn > 9:
            try:
                turn = int(input("Wähle eine Zahl zwischen 1 und 9: "))
                if turn < 1 or turn > 9:
                    print("ungültige Eingabe")
                    continue
                turn_list = [turn - 1, self.sign]
            except ValueError:
                print("ungültige Eingabe")
                continue
        return turn_list


class KI_Spieler:
    def __init__(self, sign):
        self.sign = sign
        self.enemy_sign = None
        if self.sign == "X":
            self.enemy_sign = "O"
        else:
            self.enemy_sign = "X"

    # siehe Dokumentation 
    def you_turn(self, turn_count, tafel_state):
        tafel_state = tafel_state[:]
        turn_list = [0, self.sign]
        empty_field_list = []
        for i in range(9):
            if (tafel_state[i] == " "):
                empty_field_list.append(i)
        if turn_count == 1:
            turn_list = [4, self.sign]
        if turn_count == 2:
            if tafel_state[4] == " ":
                turn_list = [4, self.sign]
            else:
                turn_list = [8, self.sign]
        if turn_count == 3:
            if tafel_state[1] == "O" or tafel_state[5] == "O":
                turn_list = [6, self.sign]
            if tafel_state[3] == "O" or tafel_state[7] == "O":
                turn_list = [2, self.sign]
            if tafel_state[0] == "O" or tafel_state[6] == "O":
                turn_list = [3, self.sign]
            if tafel_state[2] == "O" or tafel_state[8] == "O":
                turn_list = [5, self.sign]
        if turn_count == 4:
            if tafel_state[0] == "O" and tafel_state[5] == "O":
                return [6, self.sign]
        if turn_count > 3 and turn_count < 9:
            for i in empty_field_list:
                test_tafel = Tafel(tafel_state[:])
                test_tafel.add_turn([i, self.sign])
                if test_tafel.check_if_win():
                    return [i, self.sign]
                test_tafel = None
            for i in empty_field_list:
                test_tafel = Tafel(tafel_state[:])
                test_tafel.add_turn([i, self.enemy_sign])
                if test_tafel.check_if_win():
                    return [i, self.sign]
            rand_field = empty_field_list[random.randint(0, len(empty_field_list) - 1)]
            turn_list = [rand_field, self.sign]
        if turn_count == 9:
            turn_list = [empty_field_list[0], self.sign]
        return turn_list

def get_enemy_sign(playing_sign):
    signs = ['X', 'O']
    return signs[signs.index(playing_sign)-1]


if __name__ == "__main__":

    n = Network()

    data = n.getP()
    playing_sign = data['player']
    gaming_id = data['id']

    print('You are ', playing_sign)

    enemy = get_enemy_sign(playing_sign)

    session = input("Enter C(Computer)/P(Player) : ")

    if session == "C":
        computer_network = Network()
        computer = KI_Spieler(computer_network.getP())
    else:
        pass

    player = Spieler(playing_sign)

    game = None

    print("Lets play TicTacToe!")

    while game != "NONE" and not game:
        try:
            game_json = n.get(gaming_id)
            # game = Game(game_json["id"])
            # game.unPack(game_json)
            print(game)

        except Exception as e:
            run = False
            print("Couldn't get game")
            print(str(e))

    if not game.connected():
        print("Waiting for player...")

    while not game.ready:
        
        try:
            game_json = n.get(gaming_id)
            game = Game(game_json["id"])
            game.unPack(game_json)

        except Exception as e:
            print("Couldn't get game")
            print(str(e))
            break        

    while game.board.not_full() and not game.winner():

        if game.current_player == player.sign:
            game.board.print_board()
            turn_list = player.you_turn()
            game = n.play(gaming_id, str(turn_list))
            game.board.print_board()
            if game.message != 'None':
                print(game.message)
        else:
            if session == "C":
                game.board.print_board()
                print("Computer playing...")
                computer_turn_list = computer.you_turn(game.turn_count, game.board.state)
                game = computer_network.play(gaming_id, str(computer_turn_list))
            else:
                print(f"{enemy} is playing...")
                while game.current_player != player.sign:
                    game_json = n.get(gaming_id)
                    if game_json:
                        game = Game(game_json["id"])
                        game.unPack(game_json)
                    if game.current_player == player.sign:
                        break
                continue

    if game.winner():
        game.board.print_board()
        if game.winner() != player.sign:
            print("you lose")
        else:
            print("you win!!!!!!!!!!!!")
    else:
        game.board.print_board()
        print("draw")
        print("end")
