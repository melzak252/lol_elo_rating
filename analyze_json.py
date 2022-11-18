import json
from time import sleep

import requests

limit = 2000
offset = 0
PLAYERS_URL = "https://lol.fandom.com/wiki/Special:CargoExport?tables=Players%2C&&fields=Players.ID%2C+Players.Player%2C+Players.Name%2C+Players.Country%2C+Players.Age%2C+Players.Birthdate%2C+Players.Nationality%2C+Players.Role%2C+Players.IsRetired%2C+Players.FavChamps%2C+Players.Team%2C+Players.Residency%2C&&order+by=%60cargo__Players%60.%60ID%60%2C%60cargo__Players%60.%60Player%60%2C%60cargo__Players%60.%60Name%60%2C%60cargo__Players%60.%60Country%60%2C%60cargo__Players%60.%60Age%60&limit={}&offset={}&format=json"
players = []

while (data := requests.get(PLAYERS_URL.format(limit, offset))).json():
    offset += limit
    print(json.dumps(data.json(), indent=4))

    sleep(1)

