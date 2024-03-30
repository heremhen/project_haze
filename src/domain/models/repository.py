from typing import Any, AsyncGenerator, Optional, Union

from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound

from src.infrastructure.application import NotFoundError
from src.infrastructure.database import BaseRepository, ModelsTable

from .entities import (
    ModelsFlat,
    ModelsUncommited,
    ModelsUncommitedOptional,
    StatusType,
)

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
        self,
        user_id: int,
        limit: Optional[int] = None,
        status: Optional[StatusType] = None,
    ) -> AsyncGenerator[ModelsFlat, None]:
        query = select(self.schema_class).where(
            self.schema_class.user_id == user_id
        )
        if status is not None:
            query = query.where(self.schema_class.status == status)
        query = query.order_by(self.schema_class.updated_at.desc())
        if limit is not None:
            query = query.limit(limit)
        async for instance in self._all(query=query):
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
