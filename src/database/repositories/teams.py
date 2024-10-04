from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database.models import Team
from database.schemas import TeamCreate


class TeamsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, id: int) -> Team:
        return await self.session.get(Team, id)

    async def get_all(self) -> list[Team]:
        result = await self.session.execute(select(Team))
        return result.scalars().all()

    async def get_by_name(self, name: str) -> Team:
        result = await self.session.execute(select(Team).where(Team.name == name))
        return result.scalars().first()

    async def create(self, team: TeamCreate) -> Team:
        team = Team(**team.model_dump())

        self.session.add(team)

        try:
            await self.session.commit()
            await self.session.refresh(team)
        except Exception as ex:
            await self.session.rollback()
            raise ex
