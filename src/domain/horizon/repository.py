from typing import AsyncGenerator

from sqlalchemy import and_

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
        condition = and_(self.schema_class.user_id == user_id)
        async for instance in self._all(condition):
            yield HorizonFlat.model_validate(instance)
