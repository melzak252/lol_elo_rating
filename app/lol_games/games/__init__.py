from fastapi import APIRouter
import app.lol_games.games.models as games_models
from db import engine

router = APIRouter(
    prefix="/games",
    tags=["games"]
)

games_models.Base.metadata.create_all(engine)
