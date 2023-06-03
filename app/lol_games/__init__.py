from fastapi import APIRouter
import app.lol_games.db as lol_games_db
import app.lol_games.models as lol_games_models

from app.lol_games.teams import router as teams_router
from app.lol_games.players import router as players_router
from app.lol_games.games import router as games_router

router = APIRouter(
    prefix="/lol_games",
    tags=["lol_games"]
)

router.include_router(teams_router)
# router.include_router(games_router)
# router.include_router(players_router)
