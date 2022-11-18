from fastapi import APIRouter
import app.lol_games.players.models as player_model
from db import engine

router = APIRouter(
    prefix="/players",
    tags=["players"]
)

player_model.Base.metadata.create_all(engine)
