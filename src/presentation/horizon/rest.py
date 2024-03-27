from fastapi import APIRouter, Depends, status

from src.application import authentication, horizon
from src.domain.horizon import HorizonFlat
from src.domain.users import UserFlat
from src.infrastructure.application import (
    NotFoundError,
    Response,
    ResponseMulti,
)

from .contracts import HorizonCreateRequestBody, HorizonPublic

router = APIRouter(prefix="/horizon", tags=["Horizon"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_horizon(
    schema: HorizonCreateRequestBody,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[HorizonPublic]:
    """Create a new horizon."""

    _horizon: HorizonFlat = await horizon.create(
        user_id=user.id,
        payload=schema.model_dump(),
    )
    _horizon_public = HorizonPublic.model_validate(_horizon)

    return Response[HorizonPublic](result=_horizon_public)


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

    return Response[HorizonPublic](result=_horizon)


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_horizon(
    user: UserFlat = Depends(authentication.get_current_user),
) -> ResponseMulti[HorizonPublic]:
    """Read horizons."""

    _horizon: list[HorizonFlat] = await horizon.get_all(
        user_id=user.id,
    )

    return ResponseMulti[HorizonPublic](result=_horizon)


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
