from src.domain.models import (
    ModelsFlat,
    ModelsRepository,
    ModelsUncommited,
)
from src.infrastructure.database import transaction


async def get_all() -> list[ModelsFlat]:
    """Get all models from the database."""

    async with transaction():
        return [model async for model in ModelsRepository().all()]


async def create(schema: ModelsUncommited) -> ModelsFlat:
    """Create a database record for the model."""

    async with transaction():
        return await ModelsRepository().create(schema)
