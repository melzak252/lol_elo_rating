from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Game
from database.schemas import GameCreate


class GamesRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int):
        return await self.session.get(Game, id)

    async def get_all(self):
        result = await self.session.execute(select(Game))
        return result.scalars().all()

    async def create(self, game: GameCreate):
        game = Game(**game.model_dump())

        self.session.add(game)

        try:
            await self.session.commit()
            await self.session.refresh(game)
        except Exception as ex:
            await self.session.rollback()
            raise ex
