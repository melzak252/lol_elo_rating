import datetime as _dt
from pydantic import BaseModel


class _TeamBase(BaseModel):
    name: str | None
    short_name: str | None


class TeamCreate(_TeamBase):
    region: str | None
    location: str | None
    is_disbanded: bool

    class Config:
        orm_mode = True


class TeamResponse(_TeamBase):
    id: int

    class Config:
        orm_mode = True
