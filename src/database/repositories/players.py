from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Player
from database.schemas import PlayerCreate


class PlayersRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Player:
        return await self.session.get(Player, id)

    async def get_all(self) -> list[Player]:
        result = await self.session.execute(select(Player))
        return result.scalars().all()

    async def get_by_nick(self, nick: str) -> Player:
        result = await self.session.execute(select(Player).where(Player.nick == nick))
        return result.scalars().first()

    async def create(self, player: PlayerCreate) -> Player:
        player = Player(**player.model_dump())

        self.session.add(player)

        try:
            await self.session.commit()
            await self.session.refresh(player)
        except Exception as ex:
            await self.session.rollback()
            raise ex
