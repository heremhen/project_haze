from typing import Any, AsyncGenerator, Optional, Union

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound

from src.infrastructure.application import NotFoundError
from src.infrastructure.database import BaseRepository, ModelsPredictTable

from .entities import PredictFlat, PredictUncommited, PredictUncommitedOptional

all = ("PredictRepository",)


class PredictRepository(BaseRepository[ModelsPredictTable]):
    schema_class = ModelsPredictTable

    async def all(self) -> AsyncGenerator[PredictFlat, None]:
        async for instance in self._all():
            yield PredictFlat.model_validate(instance)

    async def get(self, id_: int) -> PredictFlat:
        instance = await self._get(key="id", value=id_)
        return PredictFlat.model_validate(instance)

    async def create(self, schema: PredictUncommited) -> PredictFlat:
        instance: ModelsPredictTable = await self._save(schema.model_dump())
        return PredictFlat.model_validate(instance)

    async def update(
        self,
        key: str,
        value: Any,
        payload: Union[dict[str, Any], PredictUncommitedOptional],
    ) -> PredictFlat:
        if isinstance(payload, PredictUncommitedOptional):
            payload = payload.model_dump()
        try:
            instance: ModelsPredictTable = await self._update(
                key, value, payload
            )
            return PredictFlat.model_validate(instance)
        except NoResultFound:
            raise NotFoundError(f"No model found with {key} = {value}")

    async def all_by_user(
        self,
        user_id: int,
        models_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> AsyncGenerator[PredictFlat, None]:
        query = select(self.schema_class).where(
            self.schema_class.user_id == user_id
        )
        query = query.order_by(self.schema_class.updated_at.desc())
        if limit is not None:
            query = query.limit(limit)
        if models_id is not None:
            query = query.where(self.schema_class.models_id == models_id)
        async for instance in self._all(query=query):
            yield PredictFlat.model_validate(instance)
