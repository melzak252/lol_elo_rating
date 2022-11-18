import datetime
import json

from typing import Dict, List, Callable

from unidecode import unidecode

import tqdm as tqdm
from sqlalchemy.orm.session import Session

from app.fetch_data.abc import Fetcher
from app.fetch_data.constants import TEAMS_URL, TEAMS_HEADERS
from app.lol_games.games.models import Game
from app.lol_games.games.schemas import GameCreate
from app.lol_games.players.db import create_player
from app.lol_games.players.schemas import PlayerCreate
from app.lol_games.teams.db import create_team, get_teams_by_name
from app.lol_games.teams.models import Team
from app.lol_games.teams.schemas import TeamCreate
from db import get_db


class TeamsFetcher(Fetcher):
    _api_url = "https://lol.fandom.com/wiki/Special:CargoExport?tables=Teams%2C&&fields=Teams.Name%2C+Teams.Location%2C+Teams.Region%2C+Teams.Short%2C+Teams.IsDisbanded%2C&&order+by=%60cargo__Teams%60.%60Name%60%2C%60cargo__Teams%60.%60Location%60%2C%60cargo__Teams%60.%60Region%60%2C%60cargo__Teams%60.%60Short%60%2C%60cargo__Teams%60.%60IsDisbanded%60&limit={}&offset={}&format=json"
    headers = {
        "Name": "name",
        "Location": "location",
        "Region": "region",
        "Short": "short_name",
        "IsDisbanded": "is_disbanded"
    }

    def add_to_db(self, data):
        db: Session = next(get_db())

        duplicates = []
        for dict_obj in tqdm.tqdm(data):
            if dict_obj["name"] is not None:
                dict_obj["name"] = unidecode(str(dict_obj["name"]))
            result, duplicate = create_team(db, TeamCreate.parse_obj(dict_obj))
            if duplicate is not None:
                duplicates.append((TeamCreate.from_orm(result), TeamCreate.from_orm(duplicate)))

        print("Duplicates", duplicates)
        print(len(duplicates))


class PlayersFetcher(Fetcher):
    _api_url = "https://lol.fandom.com/wiki/Special:CargoExport?tables=Players%2C&&fields=Players.ID%2C+Players.Player%2C+Players.Name%2C+Players.Country%2C+Players.Age%2C+Players.Birthdate%2C+Players.Role%2C+Players.IsRetired%2C+Players.Team%2C+Players.Residency%2C+Players.IsSubstitute%2C&&order+by=%60cargo__Players%60.%60ID%60%2C%60cargo__Players%60.%60Player%60%2C%60cargo__Players%60.%60Name%60%2C%60cargo__Players%60.%60Country%60%2C%60cargo__Players%60.%60Age%60&limit={}&offset={}&format=json"
    headers = {
        "ID": "nick",
        "Player": "unique_nick",
        "Name": "full_name",
        "Country": "country",
        "Age": "age",
        "Birthdate": "birthdate",
        "Role": "main_position",
        "IsRetired": "retired",
        "Team": "team",
        "Residency": "residency",
    }

    def add_to_db(self, data):
        db: Session = next(get_db())

        multi_teams = []
        for dict_player in tqdm.tqdm(data):
            player_teams: List[Team] = []
            if (team_name := dict_player["team"]) is not None:
                player_teams = get_teams_by_name(team_name, db)

            dict_player["actual_team_id"] = None
            if len(player_teams) == 1 and not dict_player["retired"]:
                dict_player["actual_team_id"] = player_teams[0].id

            player = PlayerCreate.parse_obj(dict_player)

            if len(player_teams) > 1:
                multi_teams.append((
                    player,
                    team_name
                ))

            create_player(db, player)

        print("MultiTeams:", multi_teams)
        print(len(multi_teams))


class GamesFetcher(Fetcher):
    _api_url = "https://lol.fandom.com/wiki/Special:CargoExport?tables=MatchScheduleGame%2C+MatchSchedule%2C&join+on=MatchSchedule.MatchId%3D+MatchScheduleGame.MatchId&fields=MatchScheduleGame._ID%2C+MatchScheduleGame.GameId%2C+MatchScheduleGame.Blue%2C+MatchScheduleGame.Red%2C+MatchScheduleGame.Winner%2C+MatchScheduleGame.MatchId%2C+MatchScheduleGame.GameId%2C+MatchSchedule.DateTime_UTC%2C&&order+by=%60cargo__MatchSchedule%60.%60DateTime_UTC%60&limit={}&offset={}&format=json"
    headers = {
        "GameId": "string_id",
        "Blue": "blue",
        "Red": "red",
        "Winner": "winner",
        "DateTime UTC": "game_date",
    }

    def add_to_db(self, data):
        db: Session = next(get_db())

        team_errors = []
        missing_teams = set()
        multiple_teams = []
        for dict_game in tqdm.tqdm(data):
            blue_team_id = None
            blue_teams: List[Game] = []
            if (blue_name := dict_game["blue"]) is not None:
                blue_name = unidecode(blue_name)
                blue_teams = get_teams_by_name(blue_name, db)

            red_team_id = None
            red_teams: List[Game] = []
            if (red_name := dict_game["red"]) is not None:
                red_name = unidecode(red_name)
                red_teams = get_teams_by_name(red_name, db)

            if blue_name is None and red_name is None:
                continue

            if dict_game["game_date"]:
                dict_game["game_date"] = datetime.datetime.strptime(dict_game["game_date"], '%Y-%m-%d %H:%M:%S').date()

            if not blue_teams:
                missing_teams.add(blue_name)

            if not red_teams:
                missing_teams.add(red_name)

            if len(blue_teams) > 1:
                multiple_teams.append([TeamCreate.from_orm(team) for team in blue_teams])

            if len(red_teams) > 1:
                multiple_teams.append([TeamCreate.from_orm(team) for team in red_teams])

            if len(blue_teams) == 1:
                blue_team_id = blue_teams[0].id

            if len(red_teams) == 1:
                red_team_id = red_teams[0].id

            dict_game["blue_team_id"] = blue_team_id
            dict_game["red_team_id"] = red_team_id

            dict_game["winner_team_id"] = blue_team_id if dict_game["winner"] == 1 else red_team_id

        print(missing_teams)
        print(len(missing_teams))
        print(multiple_teams)
        print(len(multiple_teams))


if __name__ == '__main__':
    #     team_fetcher = TeamsFetcher()
    #     team_fetcher.start_fetching()
    #     player_fetcher = PlayersFetcher()
    #     player_fetcher.start_fetching()
    game_fetcher = GamesFetcher(5000)
    game_fetcher.start_fetching()
