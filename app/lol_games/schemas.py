import datetime as _dt
from pydantic import BaseModel


class _LolTeamBase(BaseModel):
    email: str
    username: str


class LolTeamCreate(_LolTeamBase):
    password: str
    login: str


class LolTeamResponse(_LolTeamBase):
    id: int

    class Config:
        orm_mode = True
