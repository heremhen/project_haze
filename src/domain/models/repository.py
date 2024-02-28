from typing import AsyncGenerator

from src.infrastructure.database import BaseRepository, ModelsTable

from .entities import ModelsFlat, ModelsUncommited

all = ("ModelsRepository",)


class ModelsRepository(BaseRepository[ModelsTable]):
    schema_class = ModelsTable

    async def all(self) -> AsyncGenerator[ModelsFlat, None]:
        async for instance in self._all():
            yield ModelsFlat.model_validate(instance)

    async def get(self, id_: int) -> ModelsFlat:
        instance = await self._get(key="id", value=id_)
        return ModelsFlat.model_validate(instance)

    async def create(self, schema: ModelsUncommited) -> ModelsFlat:
        instance: ModelsTable = await self._save(schema.model_dump())
        return ModelsFlat.model_validate(instance)
