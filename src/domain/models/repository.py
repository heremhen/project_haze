from typing import Any, AsyncGenerator, Union

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound

from src.infrastructure.application import NotFoundError
from src.infrastructure.database import BaseRepository, ModelsTable

from .entities import ModelsFlat, ModelsUncommited, ModelsUncommitedOptional

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

    async def all_by_user(
        self, user_id: int
    ) -> AsyncGenerator[ModelsFlat, None]:
        condition = and_(self.schema_class.user_id == user_id)
        async for instance in self._all(condition):
            yield ModelsFlat.model_validate(instance)

    async def update(
        self,
        key: str,
        value: Any,
        payload: Union[dict[str, Any], ModelsUncommitedOptional],
    ) -> ModelsFlat:
        if isinstance(payload, ModelsUncommitedOptional):
            payload = payload.model_dump()
        try:
            instance: ModelsTable = await self._update(key, value, payload)
            return ModelsFlat.model_validate(instance)
        except NoResultFound:
            raise NotFoundError(f"No model found with {key} = {value}")
