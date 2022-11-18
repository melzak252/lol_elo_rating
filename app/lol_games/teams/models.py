import datetime as _dt
import sqlalchemy as _sql
from db import Base


class Team(Base):
    __tablename__ = "teams"
    id = _sql.Column(_sql.Integer, index=True, primary_key=True)
    name = _sql.Column(_sql.String)
    short_name = _sql.Column(_sql.String)
    region = _sql.Column(_sql.String)
    location = _sql.Column(_sql.String)
    elo_ranking = _sql.Column(_sql.Numeric, default=0.0)
    is_disbanded = _sql.Column(_sql.Boolean)

class TeamRename(Base):
    pass