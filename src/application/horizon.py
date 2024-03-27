from src.domain.horizon import (
    Horizon_,
    HorizonFlat,
    HorizonRepository,
    HorizonUncommited,
)
from src.infrastructure.application import (
    AuthorizationError,
    DatabaseError,
    NotFoundError,
)
from src.infrastructure.database import transaction


async def get(horizon_id: int, user_id: int) -> HorizonFlat:
    """Get a horizon from the database."""

    try:
        async with transaction():
            _horizon: HorizonFlat = await HorizonRepository().get(
                id_=horizon_id
            )
            if _horizon.user_id != user_id:
                raise AuthorizationError(message="Access denied.")
            return _horizon
    except (DatabaseError, NotFoundError):
        raise NotFoundError(message="Horizon not found.")


async def get_all(user_id: int) -> list[HorizonFlat]:
    """Get all horizon from the database."""

    async with transaction():
        return [
            horizon
            async for horizon in HorizonRepository().all_by_user(
                user_id=user_id
            )
        ]


async def create(user_id: int, payload: dict) -> Horizon_:
    """Create a new horizon db conversion."""

    async with transaction():
        repository = HorizonRepository()
        horizon_flat: HorizonFlat = await repository.create(
            HorizonUncommited(**payload, user_id=user_id)
        )
        rich_horizon: Horizon_ = await repository.get(horizon_flat.id)

    # Do som other stuff...

    return rich_horizon
