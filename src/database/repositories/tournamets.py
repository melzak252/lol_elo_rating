from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Tournament
from database.schemas import TournamentCreate


class TournamentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Tournament:
        return await self.session.get(Tournament, id)

    async def get_all(self) -> list[Tournament]:
        result = await self.session.execute(select(Tournament))
        return result.scalars().all()

    async def get_by_name(self, name: str) -> Tournament:
        result = await self.session.execute(
            select(Tournament).where(Tournament.name == name)
        )
        return result.scalars().first()

    async def create(self, t_create: TournamentCreate) -> Tournament:
        tournament = Tournament(**t_create.model_dump())

        self.session.add(tournament)

        try:
            await self.session.commit()
            await self.session.refresh(tournament)
        except Exception as ex:
            await self.session.rollback()
            raise ex

        return tournament
