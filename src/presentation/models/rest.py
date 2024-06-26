from typing import Optional

from fastapi import APIRouter, Depends, status

from src.application import authentication, models
from src.domain.models import ModelsFlat
from src.domain.users import UserFlat
from src.infrastructure.application import (
    NotFoundError,
    Response,
    ResponseMulti,
)

from .contracts import (
    ModelsCreateRequestBody,
    ModelsPublic,
    ModelsPublicEssentials,
)

router = APIRouter(prefix="/models", tags=["Models"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_autoML_model(
    schema: ModelsCreateRequestBody,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[ModelsPublic]:
    """Create a new model."""

    _models: ModelsFlat = await models.create(
        user=user, payload=schema.model_dump()
    )
    _models_public = ModelsPublic.model_validate(_models)

    return Response[ModelsPublic](result=_models_public)


@router.patch("/{model_id}/bg/roll", status_code=status.HTTP_200_OK)
async def randomize_model_background(
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Roll the background color of the model."""

    raise NotImplementedError()


@router.get("/{model_id}", status_code=status.HTTP_200_OK)
async def read_model(
    model_id: int,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[ModelsPublic]:
    """Read a model."""

    _model: ModelsFlat = await models.get(
        model_id=model_id,
        user_id=user.id,
    )

    return Response[ModelsPublic](result=_model)


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_model(
    user: UserFlat = Depends(authentication.get_current_user),
    horizon_id: Optional[int] = None,
    limit: Optional[int] = None,
    status: Optional[str] = None,
) -> ResponseMulti[ModelsPublicEssentials]:
    """Read models."""

    _models: list[ModelsFlat] = await models.get_all(
        user_id=user.id, horizon_id=horizon_id, limit=limit, status=status
    )
    return ResponseMulti[ModelsPublicEssentials](result=_models)


@router.put("/{model_id}", status_code=status.HTTP_200_OK)
async def update_model(
    model_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Update models."""

    raise NotImplementedError()


@router.delete("/{model_id}", status_code=status.HTTP_200_OK)
async def remove_model(
    model_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Remove models."""

    raise NotImplementedError()
