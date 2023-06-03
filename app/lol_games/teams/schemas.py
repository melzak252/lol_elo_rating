import datetime as _dt
from pydantic import BaseModel, validator


class _TeamBase(BaseModel):
    unique_name: str
    name: str | None
    short_name: str | None


class TeamCreate(_TeamBase):
    region: str | None
    location: str | None
    team_location: str | None
    is_disbanded: bool
    img_name: str | None

    class Config:
        orm_mode = True


class TeamResponse(_TeamBase):
    id: int

    class Config:
        orm_mode = True


class _TeamRenameBase(BaseModel):
    prev_name: str
    new_name: str
    date: _dt.date

    @validator('date', pre=True)
    def date_validate(cls, v):
        return _dt.datetime.fromisoformat(v).date()



class TeamRenameCreate(_TeamRenameBase):
    change_type: str
    team_changed: bool

    class Config:
        orm_mode = True
