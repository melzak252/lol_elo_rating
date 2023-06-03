import datetime as _dt
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
from app.lol_games.teams.db import create_team, get_teams_by_name, create_team_rename
from app.lol_games.teams.models import Team
from app.lol_games.teams.schemas import TeamCreate, TeamRenameCreate
from database import get_db


class TeamsFetcher(Fetcher):
    _api_url = "https://lol.fandom.com/wiki/Special:CargoExport?tables=Teams&&fields=Teams.Name%2C+Teams.Short%2C+Teams.Location%2C+Teams.TeamLocation%2C+Teams.Region%2C+Teams.Image%2C+Teams.OverviewPage%2C+Teams.IsDisbanded%2C&&order+by=%60cargo__Teams%60.%60OverviewPage%60&limit={}&offset={}&format=json"
    headers = {
        "OverviewPage": "unique_name",
        "Name": "name",
        "Location": "location",
        "TeamLocation": "team_location",
        "Region": "region",
        "Short": "short_name",
        "IsDisbanded": "is_disbanded",
        "Image": "img_name"
    }

    def add_to_db(self, data):
        db: Session = next(get_db())

        duplicates = []
        empty_names = []
        for dict_obj in tqdm.tqdm(data):
            if dict_obj["unique_name"] is not None:
                dict_obj["unique_name"] = unidecode(str(dict_obj["unique_name"])).lower()
            else:
                empty_names.append(TeamCreate.parse_obj(dict_obj))

            result, duplicate = create_team(db, TeamCreate.parse_obj(dict_obj))

            if duplicate is not None and dict_obj["unique_name"] is not None:
                duplicates.append((TeamCreate.from_orm(result), TeamCreate.from_orm(duplicate)))

        print("Duplicates", duplicates)
        print(len(duplicates))


        print("Empty", empty_names)
        print(len(empty_names))
class TeamsRenamesFetcher(Fetcher):
    _api_url = "https://lol.fandom.com/wiki/Special:CargoExport?tables=TeamRenames%2C&&fields=TeamRenames.Date%2C+TeamRenames.OriginalName%2C+TeamRenames.NewName%2C+TeamRenames.Verb%2C+TeamRenames.IsSamePage%2C&&order+by=%60cargo__TeamRenames%60.%60Date%60+DESC&limit={}&offset={}&format=json"
    headers = {
        "Date": "date",
        "OriginalName": "prev_name",
        "NewName": "new_name",
        "Verb": "change_type",
        "IsSamePage": "same_page"
    }

    def add_to_db(self, data):
        db: Session = next(get_db())

        for dict_obj in tqdm.tqdm(data):
            dict_obj["team_changed"] = not (True if dict_obj["same_page"] == "Yes" else False)
            my_obj: TeamRenameCreate = TeamRenameCreate.parse_obj(dict_obj)
            create_team_rename(db, my_obj)


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
    _api_url = "https://lol.fandom.com/wiki/Special:CargoExport?tables=MatchScheduleGame&&fields=_pageName%3DPage%2CBlue%3DBlue%2CRed%3DRed%2CWinner%3DWinner%2CBlueScore%3DBlueScore%2CRedScore%3DRedScore%2CBlueFinal%3DBlueFinal%2CRedFinal%3DRedFinal%2CBlueFootnote%3DBlueFootnote%2CRedFootnote%3DRedFootnote%2CFootnote%3DFootnote%2CIsChronobreak%3DIsChronobreak%2CIsRemake%3DIsRemake%2CFF%3DFF%2CSelection%3DSelection%2CHasSelection%3DHasSelection%2CMatchHistory%3DMatchHistory%2CRecap%3DRecap%2CReddit%3DReddit%2CVod%3DVod%2CVodPB%3DVodPB%2CVodGameStart%3DVodGameStart%2CVodPostgame%3DVodPostgame%2CVodHighlights%3DVodHighlights%2CVodInterview%3DVodInterview%2CInterviewWith__full%3DInterviewWith%2CMVP%3DMVP%2CMVPPoints%3DMVPPoints%2COverviewPage%3DOverviewPage%2CN_MatchInTab%3DN+MatchInTab%2CN_TabInPage%3DN+TabInPage%2CN_GameInMatch%3DN+GameInMatch%2CN_Page%3DN+Page%2CGameId%3DGameId%2CMatchId%3DMatchId%2CRiotPlatformGameId%3DRiotPlatformGameId%2CRiotPlatformId%3DRiotPlatformId%2CRiotGameId%3DRiotGameId%2CRiotHash%3DRiotHash%2CRiotVersion%3DRiotVersion%2CHasRpgidInput%3DHasRpgidInput%2CIgnoreRpgid%3DIgnoreRpgid%2CVersionedRpgid%3DVersionedRpgid%2CWrittenSummary%3DWrittenSummary&&order+by=%60cargo__MatchScheduleGame%60.%60_ID%60%2C%60_pageName%60%2C%60Blue%60%2C%60Red%60%2C%60Winner%60%2C%60BlueScore%60&limit={}&offset={}&format=json"
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
                dict_game["game_date"] = _dt.datetime.strptime(dict_game["game_date"], '%Y-%m-%d %H:%M:%S').date()

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
    # pass
    # team_fetcher = TeamsFetcher()
    # team_fetcher.start_fetching()
    team_rename_fetcher = TeamsRenamesFetcher()
    team_rename_fetcher.start_fetching()
    # #     player_fetcher = PlayersFetcher()
    # #     player_fetcher.start_fetching()
    # game_fetcher = GamesFetcher(5000)
    # game_fetcher.start_fetching()
