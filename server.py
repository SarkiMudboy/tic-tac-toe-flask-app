import socket
from _thread import *
from ttt_game import Game
import pickle

server = '192.168.43.50'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print('Waiting for connection, Server started')

connected = set()
games = {}
idCount = 0


def threaded_client(conn, p, gameId):

    global idCount
    conn.send(str.encode(str(p)))
    reply = ''
    while True:
        try:

            data = conn.recv(4096).decode()

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data != 'get':
                        data = eval(data)
                        game.play(p, data)

                    conn.sendall(pickle.dumps(game))
            else:
                break
        except:
            break

    print('Lost connection')
    try:
        del games[gameId]
        print('Closing', gameId)
    except:
        pass
    idCount -= 1
    conn.close()


while True:
    conn, addr = s.accept()
    print('Connected to ', addr)
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

    start_new_thread(threaded_client, (conn, p, gameId))
