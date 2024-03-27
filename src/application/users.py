from src.domain.users import (
    UserFlat,
    UsersRepository,
    UserUncommited,
)
from src.infrastructure.application.errors.entities import (
    BadRequestError,
    DatabaseError,
)
from src.infrastructure.database import transaction


async def create(schema: UserUncommited) -> UserFlat:
    """Create a new user db conversion."""

    try:
        async with transaction():
            repository = UsersRepository()
            user_flat: UserFlat = await repository.create(schema)
            rich_user: UserFlat = await repository.get(user_flat.id)
    except DatabaseError:
        raise BadRequestError(message="Username or email has already taken.")

    # Do som other stuff...

    return rich_user
