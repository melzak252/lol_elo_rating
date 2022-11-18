import sqlalchemy as _sql

from app.lol_games.teams.models import Team
from db import Base


class Player(Base):
    __tablename__ = "players"
    id = _sql.Column(_sql.Integer, index=True, primary_key=True)
    nick = _sql.Column(_sql.String)
    unique_nick = _sql.Column(_sql.String, unique=True)
    full_name = _sql.Column(_sql.String)
    country = _sql.Column(_sql.String)
    residency = _sql.Column(_sql.String)
    age = _sql.Column(_sql.Integer)
    birthdate = _sql.Column(_sql.Date)
    actual_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    main_position = _sql.Column(_sql.String)
    retired = _sql.Column(_sql.Boolean)
    elo_rating = _sql.Column(_sql.Numeric)
