from typing import Any, AsyncGenerator, Optional, Union

from sqlalchemy import desc, or_, select
from sqlalchemy.exc import NoResultFound

from src.infrastructure.application import NotFoundError
from src.infrastructure.database import BaseRepository, ModelsReportTable

from .entities import ModelsReportFlat, ModelsReportUncommited

all = ("ModelsReportRepository",)


class ModelsReportRepository(BaseRepository[ModelsReportTable]):
    schema_class = ModelsReportTable

    async def all(self) -> AsyncGenerator[ModelsReportFlat, None]:
        async for instance in self._all():
            yield ModelsReportFlat.model_validate(instance)

    async def get(self, id_: int) -> ModelsReportFlat:
        instance = await self._get(key="id", value=id_)
        return ModelsReportFlat.model_validate(instance)

    async def create(self, schema: ModelsReportUncommited) -> ModelsReportFlat:
        instance: ModelsReportTable = await self._save(schema.model_dump())
        return ModelsReportFlat.model_validate(instance)

    async def all_by_user(
        self,
        user_id: int,
        limit: Optional[int] = None,
    ) -> AsyncGenerator[ModelsReportFlat, None]:
        query = select(self.schema_class).where(
            self.schema_class.user_id == user_id
        )
        query = query.order_by(self.schema_class.updated_at.desc())
        if limit is not None:
            query = query.limit(limit)
        async for instance in self._all(query=query):
            yield ModelsReportFlat.model_validate(instance)

    async def update(
        self,
        key: str,
        value: Any,
        payload: Union[dict[str, Any], ModelsReportUncommited],
    ) -> ModelsReportFlat:
        if isinstance(payload, ModelsReportUncommited):
            payload = payload.model_dump()
        try:
            instance: ModelsReportTable = await self._update(
                key, value, payload
            )
            return ModelsReportFlat.model_validate(instance)
        except NoResultFound:
            raise NotFoundError(f"No report found with {key} = {value}")
