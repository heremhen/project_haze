from fastapi import APIRouter, Depends, status

from src.application import authentication, horizon, models
from src.domain.horizon import HorizonFlat
from src.domain.models.entities import ModelsFlat
from src.domain.users import UserFlat
from src.infrastructure.application import (
    NotFoundError,
    Response,
    ResponseMulti,
)
from src.presentation.models.contracts import ModelsPublicEssentials

from .contracts import HorizonCreateRequestBody, HorizonPublic, HorizonsPublic

router = APIRouter(prefix="/horizon", tags=["Horizon"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_horizon(
    schema: HorizonCreateRequestBody,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[HorizonsPublic]:
    """Create a new horizon."""

    _horizon: HorizonFlat = await horizon.create(
        user_id=user.id,
        payload=schema.model_dump(),
    )
    _horizon_public = HorizonPublic.model_validate(_horizon)

    return Response[HorizonsPublic](result=_horizon_public)


@router.get("/{horizon_id}", status_code=status.HTTP_200_OK)
async def read_horizon(
    horizon_id: int,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[HorizonPublic]:
    """Read an horizon."""

    _horizon: HorizonFlat = await horizon.get(
        horizon_id=horizon_id,
        user_id=user.id,
    )
    _models: list[ModelsFlat] = await models.get_all(
        user_id=user.id, horizon_id=horizon_id
    )
    model_dumps = [
        ModelsPublicEssentials(**model.model_dump()) for model in _models
    ]

    return Response[HorizonPublic](
        result=HorizonPublic(**_horizon.model_dump(), models=model_dumps)
    )


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_horizon(
    user: UserFlat = Depends(authentication.get_current_user),
) -> ResponseMulti[HorizonsPublic]:
    """Read horizons."""

    _horizon: list[HorizonFlat] = await horizon.get_all(
        user_id=user.id,
    )

    return ResponseMulti[HorizonsPublic](result=_horizon)


@router.put("/{horizon_id}", status_code=status.HTTP_200_OK)
async def update_horizon(
    horizon_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Update horizons."""

    raise NotImplementedError()


@router.delete("/{horizon_id}", status_code=status.HTTP_200_OK)
async def remove_horizon(
    horizon_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Remove horizons."""

    raise NotImplementedError()
