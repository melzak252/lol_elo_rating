import datetime
from dataclasses import dataclass


@dataclass
class MatchType:
    string_id: str
    team1: str
    team2: str
    winner: int
    team1_score: int
    team2_score: int
    best_of: int
    game_date: datetime.datetime
