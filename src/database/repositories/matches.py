from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Match
from database.schemas import MatchCreate


class MatchesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Match:
        return await self.session.get(Match, id)

    async def get_all(self) -> list[Match]:
        result = await self.session.execute(select(Match))
        return result.scalars().all()

    async def create(self, match: MatchCreate) -> Match:
        match = Match(**match.model_dump())

        self.session.add(match)

        try:
            await self.session.commit()
            await self.session.refresh(match)
        except Exception as ex:
            await self.session.rollback()
            raise ex
