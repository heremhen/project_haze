from typing import AsyncGenerator

from src.infrastructure.database import BaseRepository, RegistryTable

from .entities import RegistryFlat, RegistryUncommited

all = ("RegistryRepository",)


class RegistryRepository(BaseRepository[RegistryTable]):
    schema_class = RegistryTable

    async def all(self) -> AsyncGenerator[RegistryFlat, None]:
        async for instance in self._all():
            yield RegistryFlat.model_validate(instance)

    async def get(self, id_: int) -> RegistryFlat:
        instance = await self._get(key="id", value=id_)
        return RegistryFlat.model_validate(instance)

    async def create(self, schema: RegistryUncommited) -> RegistryFlat:
        instance: RegistryTable = await self._save(schema.model_dump())
        return RegistryFlat.model_validate(instance)

    async def get_by_url(self, url_: str) -> RegistryFlat:
        instance = await self._get(key="url", value=url_)
        return RegistryFlat.model_validate(instance)
