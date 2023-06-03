import datetime as _dt
import sqlalchemy as _sql
from database import Base


class Team(Base):
    __tablename__ = "team"
    id = _sql.Column(_sql.Integer, index=True, primary_key=True)
    unique_name = _sql.Column(_sql.String, unique=True)
    name = _sql.Column(_sql.String)
    short_name = _sql.Column(_sql.String)
    region = _sql.Column(_sql.String)
    location = _sql.Column(_sql.String)
    team_location = _sql.Column(_sql.String)
    is_disbanded = _sql.Column(_sql.Boolean)
    img_name = _sql.Column(_sql.String)


class TeamRename(Base):
    __tablename__ = "team_rename"
    id = _sql.Column(_sql.Integer, index=True, primary_key=True)
    prev_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    new_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    actual_team_id = _sql.Column(_sql.Integer, _sql.ForeignKey(Team.id))
    prev_name = _sql.Column(_sql.String)
    new_name = _sql.Column(_sql.String)
    team_changed = _sql.Column(_sql.Boolean)
    date = _sql.Column(_sql.Date)
    change_type = _sql.Column(_sql.String)
