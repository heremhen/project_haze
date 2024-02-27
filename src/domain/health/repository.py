from typing import AsyncGenerator

from src.domain.users.repository import UsersRepository, UsersTable
from src.infrastructure.database import BaseRepository

__all__ = ("HealthRepository",)


class HealthRepository(BaseRepository[UsersTable]):
    schema_class = UsersTable

    async def ping(self) -> AsyncGenerator[int, None]:
        instance = await UsersRepository().count()
        return instance
