from typing import AsyncGenerator

from sqlalchemy import and_, select

from src.infrastructure.database import BaseRepository, HorizonTable

from .entities import HorizonFlat, HorizonUncommited

all = ("HorizonRepository",)


class HorizonRepository(BaseRepository[HorizonTable]):
    schema_class = HorizonTable

    async def all(self) -> AsyncGenerator[HorizonFlat, None]:
        async for instance in self._all():
            yield HorizonFlat.model_validate(instance)

    async def get(self, id_: int) -> HorizonFlat:
        instance = await self._get(key="id", value=id_)
        return HorizonFlat.model_validate(instance)

    async def create(self, schema: HorizonUncommited) -> HorizonFlat:
        instance: HorizonTable = await self._save(schema.model_dump())
        return HorizonFlat.model_validate(instance)

    async def all_by_user(
        self, user_id: int
    ) -> AsyncGenerator[HorizonFlat, None]:
        query = select(self.schema_class).where(
            self.schema_class.user_id == user_id
        )
        query = query.order_by(self.schema_class.updated_at.desc())
        async for instance in self._all(query=query):
            yield HorizonFlat.model_validate(instance)
