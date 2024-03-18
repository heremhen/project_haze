from fastapi import APIRouter, Depends, status

from src.application import authentication, models
from src.domain.models import ModelsFlat
from src.domain.users import UserFlat
from src.infrastructure.application import Response

from .contracts import ModelsCreateRequestBody, ModelsPublic

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


@router.patch("/bg/roll", status_code=status.HTTP_200_OK)
async def randomize_model_background(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.get("/{model_id}", status_code=status.HTTP_200_OK)
async def read_model(
    model_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_model(
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.put("/{model_id}", status_code=status.HTTP_200_OK)
async def update_model(
    model_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()


@router.delete("/{model_id}", status_code=status.HTTP_200_OK)
async def remove_model(
    model_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    raise NotImplementedError()
