import sqlalchemy as _sql

from app.lol_games.players.models import Player
from app.lol_games.teams.models import Team
from db import Base


class Game(Base):
    __tablename__ = "games"
    id = _sql.Column(_sql.Integer, unique=True, index=True, primary_key=True)
    string_id = _sql.Column(_sql.String, unique=True, index=True, primary_key=True)
    blue_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    red_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    winner_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    game_date = _sql.Column(_sql.Date)


class PlayerGame(Base):
    __tablename__ = "players_games"
    id = _sql.Column(_sql.Integer, index=True, primary_key=True)
    player_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Player.id))
    game_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Game.id))
    kills = _sql.Column(_sql.Integer)
    deaths = _sql.Column(_sql.Integer)
    assists = _sql.Column(_sql.Integer)
    team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
