from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime


# Tournament Schema
class TournamentBase(BaseModel):
    name: str
    source: str
    region: str | None = None
    number_of_games: int = 0
    start_date: date | None = None
    end_date: date | None = None


class TournamentCreate(TournamentBase):
    pass


class TournamentUpdate(TournamentBase):
    pass


class TournamentSchema(TournamentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


# Team Schema
class TeamBase(BaseModel):
    name: str
    source: str
    rating: float = 1500.0


class TeamCreate(TeamBase):
    pass


class TeamUpdate(TeamBase):
    pass


class TeamSchema(TeamBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# Player Schema
class PlayerBase(BaseModel):
    nick: str
    full_name: Optional[str] = None
    rating: Optional[float] = 1500.0
    source: str


class PlayerCreate(PlayerBase):
    team_id: int


class PlayerUpdate(PlayerBase):
    pass


class PlayerSchema(PlayerBase):
    id: int
    team_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Match Schema
class MatchBase(BaseModel):
    tournament_id: int
    team_1_id: int
    team_2_id: int
    team_1_score: int = 0
    team_2_score: int = 0
    match_date: date | None = None
    best_of: int | None = None
    source: str


class MatchCreate(MatchBase):
    pass


class MatchUpdate(MatchBase):
    pass


class MatchSchema(MatchBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    tournament: Optional[TournamentSchema] = None

    class Config:
        from_attributes = True


# Game Schema
class GameBase(BaseModel):
    match_id: int
    winner_id: int | None = None
    blue_team_id: int
    red_team_id: int
    game_date: date = None
    duration: int | None = None
    source: str


class GameCreate(GameBase):
    pass


class GameUpdate(GameBase):
    pass


class GameSchema(GameBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


# GamePlayer Schema
class GamePlayerBase(BaseModel):
    game_id: int
    player_id: int
    team_id: int
    source: str
    kills: int = 0
    deaths: int = 0
    assists: int = 0
    cs: int = 0
    gold: int = 0
    champion: str | None = None
    role: str | None = None


class GamePlayerCreate(GamePlayerBase):
    pass


class GamePlayerUpdate(GamePlayerBase):
    pass


class GamePlayerSchema(GamePlayerBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True
