from fastapi import (
    Depends,
    FastAPI,
)
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from database import create_session
from database.repositories.tournamets import TournamentRepository
from database.schemas import TournamentSchema
import scrapper
from utils import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(scrapper.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def hello():
    return {"message": "Welcome to the Game API!"}


@app.get("/tournaments", response_model=list[TournamentSchema])
async def get_tournaments(
    session: AsyncSession = Depends(create_session),
):
    t_repo = TournamentRepository(session)

    return await t_repo.get_all()
