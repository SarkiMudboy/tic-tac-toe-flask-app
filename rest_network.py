import requests
import json

class Network:
    def __init__(self):
        self.addr = 'http://127.0.0.1:5000/'
        self.p = self.connect()

    def getP(self):
        return self.p

    def connect(self):
        try:
            response = requests.get(self.addr)
            return json.loads(response.text)
        except Exception as e:
            print(str(e))

    def get(self, game_id):
        try:
            response = requests.get(self.addr + str(game_id) + "/" + f"{self.p['player']}" + "/get")
            # print(response.text)
            return json.loads(response.text)
        except Exception as e:
            print(str(e))

    def play(self, game_id, data):
        try:
            response = requests.get(self.addr + str(game_id) + "/" + f"{self.p['player']}" + "/play/" + data)
            return json.loads(response.text)
        except Exception as e:
            print(str(e))