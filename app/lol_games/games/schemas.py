import datetime as _dt
from pydantic import BaseModel


class _GameBase(BaseModel):
    string_id: str
    game_date: _dt.date | None



class GameCreate(_GameBase):
    blue_team_id: int | None
    red_team_id: int | None
    winner_team_id: int | None

    class Config:
        orm_mode = True


class GameResponse(_GameBase):
    id: int

    class Config:
        orm_mode = True
