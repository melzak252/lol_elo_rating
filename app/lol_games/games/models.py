import sqlalchemy as _sql

from app.lol_games.players.models import Player
from app.lol_games.teams.models import Team
from database import Base


class Match(Base):
    __tablename__ = "match"
    id = _sql.Column(_sql.Integer, unique=True, index=True, primary_key=True)
    string_id = _sql.Column(_sql.String, unique=True, index=True, primary_key=True)
    team1_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    team2_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    winner_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    game_date = _sql.Column(_sql.Date)

class Game(Base):
    __tablename__ = "game"
    id = _sql.Column(_sql.Integer, unique=True, index=True, primary_key=True)
    string_id = _sql.Column(_sql.String, unique=True, index=True, primary_key=True)
    team1_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    team2_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    winner_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    game_date = _sql.Column(_sql.Date)

class PlayerGame(Base):
    __tablename__ = "player_game"
    id = _sql.Column(_sql.Integer, index=True, primary_key=True)
    player_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Player.id))
    game_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Match.id))
    kills = _sql.Column(_sql.Integer)
    deaths = _sql.Column(_sql.Integer)
    assists = _sql.Column(_sql.Integer)
    team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
