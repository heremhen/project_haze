from typing import Optional

from fastapi import APIRouter, Depends, status

from src.application import authentication, predict
from src.domain.predict import PredictFlat
from src.domain.users import UserFlat
from src.infrastructure.application import (
    NotFoundError,
    Response,
    ResponseMulti,
)

from .contracts import PredictCreateRequestBody, PredictPublic

router = APIRouter(prefix="/predict", tags=["Predict"])


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_prediction(
    schema: PredictCreateRequestBody,
    horizon_id: int,
    pipeline_id: int,
    data_type: Optional[str] = "json",
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[PredictPublic]:
    """Create a new prediction."""

    _predict: PredictFlat = await predict.create(
        horizon_id=horizon_id,
        pipeline_id=pipeline_id,
        data_type=data_type,
        user=user,
        payload=schema.data,
    )
    _predict_public = PredictPublic.model_validate(_predict)

    return Response[PredictPublic](result=_predict_public)


@router.get("/{prediction_id}", status_code=status.HTTP_200_OK)
async def read_prediction(
    prediction_id: int,
    user: UserFlat = Depends(authentication.get_current_user),
) -> Response[PredictPublic]:
    """Read prediction."""

    _model: PredictFlat = await predict.get(
        model_id=prediction_id,
        user_id=user.id,
    )

    return Response[PredictPublic](result=_model)


@router.get("", status_code=status.HTTP_200_OK)
async def read_all_predictions(
    user: UserFlat = Depends(authentication.get_current_user),
    limit: Optional[int] = None,
) -> ResponseMulti[PredictPublic]:
    """Read prediction."""

    _predict: list[PredictFlat] = await predict.get_all(
        user_id=user.id,
        limit=limit,
    )
    return ResponseMulti[PredictPublic](result=_predict)


@router.put("/{prediction_id}", status_code=status.HTTP_200_OK)
async def update_predictions(
    prediction_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Update prediction."""

    raise NotImplementedError()


@router.delete("/{prediction_id}", status_code=status.HTTP_200_OK)
async def remove_predictions(
    prediction_id,
    user: UserFlat = Depends(authentication.get_current_user),
):
    """Remove prediction."""

    raise NotImplementedError()
