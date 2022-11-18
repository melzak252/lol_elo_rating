import datetime as _dt
from pydantic import BaseModel


class _PlayerBase(BaseModel):
    nick: str
    unique_nick: str
    full_name: str | None


class PlayerCreate(_PlayerBase):
    country: str | None
    residency: str | None
    age: int | None
    birthdate: _dt.date | None
    actual_team_id: int | None
    main_position: str | None
    retired: bool

    class Config:
        orm_mode = True


class PlayerResponse(_PlayerBase):
    id: int

    class Config:
        orm_mode = True
