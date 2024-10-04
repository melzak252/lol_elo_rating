from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import create_session
from database.repositories.tournamets import TournamentRepository
from database.schemas import TournamentSchema
from utils.scrappers import get_golgg_scrapper
from utils.scrappers.golgg import GolGGScrapper


router = APIRouter(
    prefix="/scrap",
    tags=["scrapper"],
    responses={404: {"description": "Not found"}},
)


@router.get("/tournaments", response_model=list[TournamentSchema])
async def scrap_tournaments(
    scrapper: GolGGScrapper = Depends(get_golgg_scrapper),
    session: AsyncSession = Depends(create_session),
):
    tournaments = await scrapper.get_all_tournaments()
    test = {}
    for t in tournaments:
        if t.name in test:
            print(test[t.name].model_dump())
            print(t.model_dump())

        test[t.name] = t

    t_repo = TournamentRepository(session)
    result = []

    for t in tournaments:
        try:
            tournament = await t_repo.create(t)
        except Exception as ex:
            print(ex)
            continue

        result.append(tournament)

    return result


@router.get("/games")
async def scrap_games(
    scrapper: GolGGScrapper = Depends(get_golgg_scrapper),
    session: AsyncSession = Depends(create_session),
):
    return {"message": "Not implemented yet"}
